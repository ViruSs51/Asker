from ..Bot import verification as check
from ..Bot import ActionRegister as reg
from ..Bot import Menu as menu
from ..Bot import Action as Action
from ..FileControl import FileManage as fm
from ..FileControl.GoogleDrive.GoogleDriveManage import Drive
from ..DataBase import get_db_connection

import asyncio
from copy import deepcopy

from aiogram import Bot
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.enums import ParseMode
#from aiogram.utils.keyboard import InlineKeyboardBuilder

class Answer:

    def __init__(self,
                 bot: Bot,
                 drive: Drive
                 ) -> None:
        self.bot = bot
        self.drive = drive
        self.db = get_db_connection()

    async def start(self,
                    message: Message
                    ) -> None:
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        user_data = message.from_user
        lang = await Action.get_language(user=user_data)
        connected_id = self.db.SQL(f"SELECT `connected_id` FROM `users`")
        
        user = check.User(user=user_data)
        username = await user.get_name()

        connected = False
        for connect in connected_id:
            if str(user_data.id) in connect[0].split(','):
                connected = True
                break   
        
        if connected:
            upath.data[str(message.from_user.id)] = 'user-cabinet'
            upath.update()

            await message.answer(
                                text='Приветствую вас снова!\nВыберите, что вы хотите сделать в меню снизу, или пришлите сюда пригласительное сообщение к данному боту, если хотите пройти какой-либо опрос.',
                                reply_markup=await menu.get_menu(menu='start', user=user_data)
            )
        else:
            upath.data[str(message.from_user.id)] = ''
            upath.update()

            await message.answer(
                                text=f'{lang.welcome.format(username=username)}\n{lang.about}\n\n{lang.help}',
                                reply_markup=await menu.get_menu(menu='start', user=user_data)
            )
    
    async def get_answers(self,
                          message: Message
                          ):
        answrs_data = []
        asker_keys = self.db.SQL(f"SELECT `asker_key` FROM `users` WHERE `connected_id` LIKE '%{message.from_user.id}%'")[0][0].split(',')

        send_message = await message.answer(text="Идет обработка данных...",
                                            reply_markup=ReplyKeyboardRemove())
        
        if asker_keys: 
            for answer in asker_keys:
                if answer == '':
                    asker_keys.remove('')
            asker_keys = [f"asker_key = '{answer.split(':')[0]}'" for answer in asker_keys]

            answers = self.db.SQL(f"SELECT `ask_id`, `asker_key`, `answer` FROM `answers` WHERE {' OR '.join(asker_keys)}")
            if answers:
                for answer in answers:
                    anw = list(answer)
                    anw.insert(2, self.db.SQL(f"SELECT `ask` FROM `asks` WHERE `asker_key` = '{answer[1]}' AND `queue` = '{answer[0]}'")[0][0])

                    answrs_data.append(anw)

        file_link = self.drive.create_table_file(file_name='data/users/answers.csv', 
                                                 file_name_drive=str(message.from_user.id), 
                                                 column_title=['Последовательность', 'Ключевое слово/фраза', 'Вопрос', 'Ответ'],
                                                 columns=answrs_data)
        
        await self.bot.delete_message(chat_id=send_message.chat.id, message_id=send_message.message_id)
        await self.bot.send_message(message.chat.id, text=f'[Вот ссылка на таблицу с ответами на ваши опросы.]({file_link})', parse_mode=ParseMode.MARKDOWN)
    
    async def get_asks(self,
                       message: Message):
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        
        upath.data[str(message.from_user.id)] = 'user-cabinet/question'
        upath.update()

        await message.answer(text="Выберите действие или опрос:",
                             reply_markup=await menu.get_menu_myasks(message.from_user))
        
    async def exit_asks(self, message:Message):
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        
        upath.data[str(message.from_user.id)] = 'user-cabinet'
        upath.update()

        await message.answer(text="Выберите действие:",
                             reply_markup=await menu.get_menu(menu='start', user=message.from_user))
        
    async def get_ask(self,
                       message: Message):
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        new_text = message.text.replace("'", "''")

        upath.data[str(message.from_user.id)] = f'user-cabinet/question/{new_text}'
        upath.update()

        await message.answer(text="Выберите действие:",
                             reply_markup=await menu.get_menu_myask(asker_key=new_text))
        
    async def get_askask(self,
                         message: Message):
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        new_text = message.text.replace("'", "''")

        upath.data[str(message.from_user.id)] = f'{upath.data[str(message.from_user.id)]}/{new_text}'
        upath.update()

        await message.answer(text="Выберите действие:",
                             reply_markup=await menu.get_menu_myaskask())
        
    async def edit_askask_text(self,
                           message: Message):
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        
        upath.data[str(message.from_user.id)] = upath.data[str(message.from_user.id)] + '/edit-text'
        upath.update()

        await self.bot.send_message(chat_id=message.from_user.id,
                                    text="Напишите ваш новый текст для вопроса:",
                                    reply_markup=await menu.get_exit_button())
        
    async def exit_edit_askask_text(self,
                           message: Message):
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        split_path = upath.data[str(message.from_user.id)].split('/')
        
        upath.data[str(message.from_user.id)] = '/'.join(split_path[:4])
        upath.update()

        await self.bot.send_message(chat_id=message.from_user.id,
                                    text="Выберите действие:",
                                    reply_markup=await menu.get_menu_myaskask())
    
    async def set_edit_askask_text(self,
                           message: Message):
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        split_path = upath.data[str(message.from_user.id)].split('/')
        new_text = message.text.replace("'", "''")

        self.db.SQL(f"UPDATE `asks` SET `ask` = '{new_text}' WHERE `asker_key` = '{split_path[2]}' AND `ask` = '{split_path[3]}'")

        upath.data[str(message.from_user.id)] = '/'.join(split_path[:3]) + f'/{message.text}'
        upath.update()

        await self.bot.send_message(chat_id=message.from_user.id,
                                    text="Вы успешно заменили текст данного вопроса!\nВыберите действие:",
                                    reply_markup=await menu.get_menu_myaskask())
        
    async def delete_askask(self,
                           message: Message):
        
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        split_path = upath.data[str(message.from_user.id)].split('/')

        queue_ask = self.db.SQL(f"SELECT `queue` FROM `asks` WHERE `asker_key` = '{split_path[2]}' AND `ask` = '{split_path[3]}'")

        self.db.SQL(f"DELETE FROM `asks` WHERE `asker_key` = '{split_path[2]}' AND `queue` = '{queue_ask[0][0]}'")
        self.db.SQL(f"UPDATE `asks` SET `queue`=`queue`-1 WHERE `asker_key`='{split_path[2]}' AND `queue` > {queue_ask[0][0]}")

        self.db.SQL(f"DELETE FROM `answers` WHERE `asker_key` = '{split_path[2]}' AND `ask_id` = '{queue_ask[0][0]}'")
        self.db.SQL(f"UPDATE `answers` SET `ask_id`=`ask_id`-1 WHERE `asker_key`='{split_path[2]}' AND `ask_id` > {queue_ask[0][0]}")

        upath.data[str(message.from_user.id)] = '/'.join(split_path[:3])
        upath.update()

        await message.answer(text="Вы успешно удалили вопрос!\nВыберите действие:",
                             reply_markup=await menu.get_menu_myask(asker_key=split_path[2]))
    
    async def exit_askask(self,
                         message: Message):
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        split_path = upath.data[str(message.from_user.id)].split('/')

        upath.data[str(message.from_user.id)] = '/'.join(split_path[:3])
        upath.update()

        await message.answer(text="Выберите действие:",
                             reply_markup=await menu.get_menu_myask(asker_key=split_path[2]))
        
    async def create_ask(self,
                        message: Message):  
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        split_path = upath.data[str(message.from_user.id)].split('/')

        username = self.db.SQL(f"SELECT `username` FROM `users` WHERE `asker_key` LIKE '%,{split_path[2]}:ru%'")
        asks = self.db.SQL(f"SELECT `asker_key` FROM `asks` WHERE `asker_key` = '{split_path[2]}'")
        queue_ask = len(asks)+1 if asks else 1
        self.db.SQL(f"INSERT INTO `asks` (`user_id`, `username`, `asker_key`, `queue`, `ask`, `type`, `answers`) VALUES ('{message.from_user.id}', '{username[0][0]}', '{split_path[2]}', '{queue_ask}', '', '', '')")
        
        upath.data[str(message.from_user.id)] = f'user-cabinet/question/{split_path[2]}/create'
        upath.update()

        send_message = await message.answer(text="Идет обработка данных...",
                                            reply_markup=ReplyKeyboardRemove())
        await self.bot.delete_message(chat_id=send_message.chat.id, message_id=send_message.message_id)

        await message.answer(text="Выберите тип ответа на вопрос",
                             reply_markup=await menu.get_ask_type())
        
    async def set_type_ask(self,
                           callback: CallbackQuery):
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        split_path = upath.data[str(callback.from_user.id)].split('/')

        self.db.SQL(f"UPDATE `asks` SET `type` = '{callback.data.split(':')[1]}' WHERE `asker_key` = '{split_path[2]}' ORDER BY id DESC LIMIT 1")
        
        await self.bot.delete_message(chat_id=callback.message.chat.id,
                                      message_id=callback.message.message_id)

        ask = self.db.SQL(f"SELECT `ask` FROM `asks` WHERE `asker_key` = '{split_path[2]}' ORDER BY id DESC LIMIT 1")
        if ask and ask[0][0] == '':
            await self.bot.send_message(chat_id=callback.from_user.id,
                                        text="Напишите ваш вопрос:",
                                        reply_markup=await menu.get_exit_button())

        await callback.answer()
        
    async def exit_create_ask(self,
                              callback: CallbackQuery):
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        split_path = upath.data[str(callback.from_user.id)].split('/')

        ask = self.db.SQL(f"SELECT `ask` FROM `asks` WHERE `asker_key` = '{split_path[2]}' ORDER BY id DESC LIMIT 1")
        if ask and ask[0][0] == '':
            self.db.SQL(f"DELETE FROM `asks` WHERE `asker_key` = '{split_path[2]}' ORDER BY id DESC LIMIT 1")

        upath.data[str(callback.from_user.id)] = f'user-cabinet/question/{split_path[2]}'
        upath.update()

        await self.bot.delete_message(chat_id=callback.message.chat.id,
                                      message_id=callback.message.message_id)

        await self.bot.send_message(chat_id=callback.from_user.id,
                                    text="Выберите действие:",
                                    reply_markup=await menu.get_menu_myask(asker_key=split_path[2]))
        
        await callback.answer()

    async def set_ask_text(self,
                           message: Message):
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        split_path = upath.data[str(message.from_user.id)].split('/')
        
        new_text = message.text.replace("'", "''")

        self.db.SQL(f"UPDATE `asks` SET `ask` = '{new_text}' WHERE `asker_key` = '{split_path[2]}' ORDER BY id DESC LIMIT 1")

        ask_type = self.db.SQL(f"SELECT `type` FROM `asks` WHERE `asker_key` = '{split_path[2]}' ORDER BY id DESC LIMIT 1")
        if ask_type and ask_type[0][0] == 'note':
            upath.data[str(message.from_user.id)] = f'user-cabinet/question/{split_path[2]}/create-answer'
            upath.update()
            await self.bot.send_message(chat_id=message.from_user.id,
                                        text="Напишите ваши варианты ответов, разделенные через запятую (,):",
                                        reply_markup=await menu.get_exit_button())
        
        else:
            upath.data[str(message.from_user.id)] = f'user-cabinet/question/{split_path[2]}/{new_text}'
            upath.update()

            await message.answer(text="Выберите действие:",
                                 reply_markup=await menu.get_menu_myaskask())
        
    async def set_ask_answer(self,
                           message: Message):
        new_text = message.text.replace("'", "''")
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        split_path = upath.data[str(message.from_user.id)].split('/')

        self.db.SQL(f"UPDATE `asks` SET `answers` = '{new_text}' WHERE `asker_key` = '{split_path[2]}' ORDER BY id DESC LIMIT 1")
        
        ask = self.db.SQL(f"SELECT `ask` FROM `asks` WHERE `asker_key` = '{split_path[2]}' ORDER BY id DESC LIMIT 1")
        upath.data[str(message.from_user.id)] = f'user-cabinet/question/{split_path[2]}/{ask[0][0]}'
        upath.update()

        await message.answer(text="Выберите действие:",
                             reply_markup=await menu.get_menu_myaskask())
        

    async def exit_create_ask_text(self,
                                   message: Message):
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        split_path = upath.data[str(message.from_user.id)].split('/')

        ask = self.db.SQL(f"SELECT `ask` FROM `asks` WHERE `asker_key` = '{split_path[2]}' ORDER BY id DESC LIMIT 1")
        if ask and ask[0][0] == '':
            self.db.SQL(f"DELETE FROM `asks` WHERE `asker_key` = '{split_path[2]}' ORDER BY id DESC LIMIT 1")

        upath.data[str(message.from_user.id)] = f'user-cabinet/question/{split_path[2]}'
        upath.update()

        await self.bot.send_message(chat_id=message.from_user.id,
                                    text="Выберите действие:",
                                    reply_markup=await menu.get_menu_myask(asker_key=split_path[2]))


    async def create_asker(self, message: Message):
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        upath.data[str(message.from_user.id)] = 'user-cabinet/question/create'
        upath.update()

        await message.answer(text="Ведите ключевое слово или фразу, по которым другие будут получать доступ к вашему опросу:",
                             reply_markup=await menu.get_exit_button())
    
    async def set_asker_name(self, message: Message):
        new_text = message.text.replace("'", "''")
        text = ''.join(new_text.split('/'))
        exist_key = self.db.SQL(f"SELECT `id` FROM `users` WHERE `asker_key` LIKE '%{',' + text + ':ru'}%'")

        if exist_key:
            await message.answer(text="Данное ключевое слово/фраза уже существует!\nПожалуйста, введите другое:",
                             reply_markup=await menu.get_exit_button())
            
            return

        data_connected = self.db.SQL(f"SELECT `id`, `asker_key` FROM `users` WHERE `connected_id` LIKE '%{message.from_user.id}%'")
        self.db.SQL(f"UPDATE `users` SET `asker_key` = '{data_connected[0][1]+','+text+':ru'}' WHERE `id` = '{data_connected[0][0]}'")
  
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        upath.data[str(message.from_user.id)] = f'user-cabinet/question/{text}'
        upath.update()

        await message.answer(text="Вы успешно создали новый опрос!\nВыберите действие:",
                             reply_markup=await menu.get_menu_myask(asker_key=text))
    
    async def delete_asker(self,
                           message: Message):
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')

        self.db.SQL(f"DELETE FROM `asks` WHERE `asker_key` = '{upath.data[str(message.from_user.id)].split('/')[2]}'")
        self.db.SQL(f"DELETE FROM `answers` WHERE `asker_key` = '{upath.data[str(message.from_user.id)].split('/')[2]}'")

        data_connected = self.db.SQL(f"SELECT `id`, `asker_key` FROM `users` WHERE `connected_id` LIKE '%{message.from_user.id}%'")
        new_asker_list = data_connected[0][1].split(',')
        new_asker_list.remove(upath.data[str(message.from_user.id)].split('/')[2] + ':ru')

        new_asker= ','.join(new_asker_list)
        self.db.SQL(f"UPDATE `users` SET `asker_key` = '{new_asker}' WHERE `id` = '{data_connected[0][0]}'")

        upath.data[str(message.from_user.id)] = 'user-cabinet/question'
        upath.update()

        await message.answer(text="Вы успешно удалили опрос!\nВыберите действие:",
                             reply_markup=await menu.get_menu_myasks(user_data=message.from_user))


    async def login_start(self,
                          message: Message
                          ):
        id_connected = self.db.SQL(f"SELECT `id`, `connected_id` FROM `users`")

        if id_connected:
            for id in id_connected:
                all_id = id[1].split(',')

                if str(message.from_user.id) in all_id:
                    all_id.remove(str(message.from_user.id))
                    self.db.SQL(f"UPDATE `users` SET `connected_id` = '{','.join(all_id)}' WHERE `id` = '{id[0]}'")

        file = fm.OpenJson(file_name='Module/Bot/data/login_procces.json')
        file.data[str(message.from_user.id)] = {
            'username': '',
            'password': ''
        }
        file.update()
        
        await message.answer(text="Введите имя пользователя:",
                             reply_markup=await menu.get_exit_button())
        
    async def exit_login(self,
                          message: Message
                          ) -> None:
        await message.answer(text="Вы вышли из меню входа в аккаунт!",
                             reply_markup=await menu.get_menu(menu='start', user=message.from_user))
        
    async def login_name(self,
                          message: Message
                          ):
        new_text = message.text.replace("'", "''")
        usernames = self.db.SQL(f"SELECT `username` FROM `users`")

        if usernames:
            exist = False
            for username in usernames:
                if username[0] == new_text:
                    exist = True 
                    break
            
            if not exist:
                await message.answer(text="Этого имени не существует!\nВведите, пожалуйста, существующее имя:",
                                        reply_markup=await menu.get_exit_button())
                
                return

        file = fm.OpenJson(file_name='Module/Bot/data/login_procces.json')
        file.data[str(message.from_user.id)]['username'] = new_text
        file.update()
        
        await message.answer(text="Введите пароль от аккаунта:",
                             reply_markup=await menu.get_exit_button())
    
    async def login_password(self,
                          message: Message
                          ):
        new_text = message.text.replace("'", "''")
        file = fm.OpenJson(file_name='Module/Bot/data/login_procces.json')
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        password = self.db.SQL(f"SELECT `password`, `connected_id` FROM `users` WHERE `username` = '{file.data[str(message.from_user.id)]['username']}'")

        await self.bot.delete_message(chat_id=message.chat.id,
                                      message_id=message.message_id)

        if password[0][0] == new_text:
            connected_id = password[0][1].split(',')
            connected_id.append(str(message.from_user.id))
            connected_id = ','.join(connected_id)

            self.db.SQL(f"UPDATE `users` SET `connected_id` = '{connected_id}' WHERE `username` = '{file.data[str(message.from_user.id)]['username']}'")
            
            await message.answer(text="Вы успешно вошли в аккаунт!",
                                    reply_markup=await menu.get_menu(menu='start', user=message.from_user))
            
            upath.data[str(message.from_user.id)] = 'user-cabinet'
            upath.update()
            
            del file.data[str(message.from_user.id)]
            file.update()

            return
        
        await message.answer(text="Пароль неверен!\nПожалуйста, попробуйте снова:",
                                    reply_markup=await menu.get_exit_button())
    
    async def signin_start(self,
                     message: Message
                     ) -> None:
        id_connected = self.db.SQL(f"SELECT `id`, `connected_id` FROM `users`")
        
        if id_connected:
            for id in id_connected:
                all_id = id[1].split(',')

                if str(message.from_user.id) in all_id:
                    all_id.remove(str(message.from_user.id))
                    self.db.SQL(f"UPDATE `users` SET `connected_id` = '{','.join(all_id)}' WHERE `id` = '{id[0]}'")
        
        self.db.SQL(f"INSERT INTO `users` (`id`, `user_id`, `connected_id`, `username`, `password`, `salt`, `balance`, `premium`, `asker_key`) VALUES (NULL, '{message.from_user.id}', '{message.from_user.id}', '', '', '', '0', '0', '')")
        
        await message.answer(text="Создайте имя для вашего аккаунта:",
                             reply_markup=await menu.get_exit_button())

    async def exit_signin(self,
                          message: Message
                          ) -> None:
        self.db.SQL(f"DELETE FROM `users` WHERE (`username` = '' OR `password` = '') AND (`user_id` = {message.from_user.id}) ORDER BY id DESC LIMIT 1;")

        await message.answer(text="Вы вышли из меню регистрации!",
                             reply_markup=await menu.get_menu(menu='start', user=message.from_user))


    async def signin_create_name(self,
                     message: Message
                     ) -> None:
        new_text = message.text.replace("'", "''")
        exit_username = self.db.SQL(f"SELECT `username` FROM `users` WHERE `username` = '{new_text}'")

        if exit_username:
            await message.answer(text="Данное имя уже занято!\nВыберите другое:",
                             reply_markup=await menu.get_exit_button())

        else:
            self.db.SQL(f"UPDATE `users` SET `username` = '{new_text}' WHERE `user_id` = '{message.from_user.id}' AND `username` = '' ORDER BY id DESC LIMIT 1")

            await message.answer(text="Создайте пароль для вашего аккаунта:",
                             reply_markup=await menu.get_exit_button())

    async def signin_create_password(self,
                     message: Message
                     ) -> None:
        new_text = message.text.replace("'", "''")
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')

        await self.bot.delete_message(chat_id=message.chat.id,
                                      message_id=message.message_id)

        self.db.SQL(f"UPDATE `users` SET `password` = '{new_text}' WHERE `user_id` = '{message.from_user.id}' AND `password` = '' ORDER BY id DESC LIMIT 1")
        
        await message.answer(text="Вы успешно зарегистрировались!",
                             reply_markup=await menu.get_menu(menu='start', user=message.from_user))
        
        upath.data[str(message.from_user.id)] = 'user-cabinet'
        upath.update()

    async def exit_from_account(self,
                                message: Message
                                ):
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        user_data = message.from_user
        connected_id = self.db.SQL(f"SELECT `id`, `connected_id` FROM `users`")
        
        user = check.User(user=user_data)

        for connect in connected_id:
            if str(user_data.id) in connect[1].split(','):
                new_connected_id_list = connect[1].split(',')
                new_connected_id_list.remove(str(user_data.id))
                new_connected_id = ','.join(new_connected_id_list)

                self.db.SQL(f"UPDATE `users` SET `connected_id` = '{new_connected_id}' WHERE `id` = '{connect[0]}'")
            
        upath.data[str(user_data.id)] = ''
        upath.update()

        await message.answer(
                                text='Вы вышли из своего аккаунта.',
                                reply_markup=await menu.get_menu(menu='start', user=user_data)
            )

    async def start_questions(self,
                              message: Message
                              ) -> None:
        new_text = message.text.replace("'", "''")
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        upath.data[str(message.from_user.id)] = 'in-question'
        upath.update()

        asker_key = new_text.split('"')[1]
        user_data = message.from_user
    
        #Get ask from databse
        ask_data = await Action.get_ask(asker_key=asker_key,
                                        ask_queue=1)

        if not ask_data:
            return
        
        keyboard = await menu.get_ask_keyboard(ask_data=ask_data)
        
        if not keyboard:
            keyboard = await menu.get_exit_button()

        if keyboard:
            send_message = await message.answer(text="Идет обработка данных...",
                                                reply_markup=ReplyKeyboardRemove())
            await self.bot.delete_message(chat_id=send_message.chat.id, message_id=send_message.message_id)

        await message.answer(text=ask_data[0][1],
                                reply_markup=keyboard)

        await Action.add_user_answer_template(user_id=user_data.id, 
                                                ask_data=ask_data, 
                                                asker_key=asker_key)

    async def get_answer(self,
                         message: Message|CallbackQuery
                         ) -> None:
        new_text = message.text.replace("'", "''") if type(message) == Message else message.data.replace("'", "''")
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        upath.data[str(message.from_user.id)] = 'in-question'
        upath.update()

        user_answer: tuple
        user_data = message.from_user
        lang = await Action.get_language(user=user_data)

        user_answers = await Action.get_user_answers(user_id=message.from_user.id)

        if user_answers:
            for answer in user_answers:
                if not answer[3]:
                    user_answer = answer

                    break
            else:
                return

            #download voice message
            #voice = await self.bot.get_file(message.voice.file_id)
            #file = await self.bot.download_file(voice.file_path)
            #with open(f"voice_{message.voice.file_id}.ogg", 'wb') as new_file:
            #    new_file.write(file.read())

            await Action.add_user_answer(answer=message.data.split(':')[1] if type(message) != Message else new_text if not message.voice else message.voice.file_id,
                                   user_id=user_data.id,
                                   ask_id=user_answer[0],
                                   asker_key=user_answer[1])
            
            await self.bot.send_message(chat_id=user_data.id,
                                        text=lang.confirm_ask,
                                        reply_markup=await menu.get_confirmed_ask(user=user_data))    

            if type(message) == CallbackQuery:
                await message.answer() 
    
    async def confirmed_answer(self,
                               callback: CallbackQuery
                               ) -> None:
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        upath.data[str(callback.from_user.id)] = 'in-question'
        upath.update()

        user_answer: tuple
        message = callback.message
        user_data = callback.from_user
        lang = await Action.get_language(user=user_data)

        await self.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        
        user_answers = await Action.get_user_answers(user_id=user_data.id)

        if user_answers:
            user_answer = await Action.get_answer_from_list(list=user_answers)

            if not user_answer:
                return
            
            await Action.confirm_user_answer(user_id=user_data.id,
                                             ask_id=user_answer[0],
                                             asker_key=user_answer[1])
            
            #Get ask from databse
            ask_data = await Action.get_ask(asker_key=user_answer[1],
                                            ask_queue=user_answer[0]+1)

            if not ask_data:
                upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
                upath.data[str(callback.from_user.id)] = f'user-cabinet'
                upath.update()

                await self.bot.send_message(chat_id=message.chat.id,
                                                       text=lang.finished_question,
                                                       reply_markup=await menu.get_menu(menu='start', user=user_data))
            
            else:
                keyboard = await menu.get_ask_keyboard(ask_data=ask_data)

                if not keyboard:
                    keyboard = await menu.get_exit_button()

                await self.bot.send_message(chat_id=message.chat.id,
                                                           text=ask_data[0][1],
                                                           reply_markup=keyboard)
               
                await Action.add_user_answer_template(user_id=user_data.id, 
                                                      ask_data=ask_data, 
                                                      asker_key=user_answer[1])
            
            await callback.answer()
    
    async def no_confirmed_answer(self,
                                  callback: CallbackQuery
                                  ) -> None:
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        upath.data[str(callback.from_user.id)] = 'in-question'
        upath.update()

        user_answer: tuple
        message = callback.message
        user_data = callback.from_user
        lang = await Action.get_language(user=user_data)

        await self.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        
        user_answers = await Action.get_user_answers(user_id=user_data.id)

        if user_answers:
            user_answer = await Action.get_answer_from_list(list=user_answers)

            if not user_answer:
                return

            await Action.reset_user_answer(user_id=user_data.id,
                                           ask_id=user_answer[0],
                                           asker_key=user_answer[1])
            
            #Get ask from databse
            ask_data = await Action.get_ask(asker_key=user_answer[1],
                                            ask_queue=user_answer[0])
            
            keyboard = await menu.get_exit_button()
            if ask_data:
                keyboard = await menu.get_ask_keyboard(ask_data=ask_data)
   
            await self.bot.send_message(chat_id=message.chat.id,
                                                text=lang.message_for_edit,
                                                reply_markup=keyboard)

            await callback.answer()
    
    async def another_message(self,
                              message: Message
                              ) -> None:
        await self.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
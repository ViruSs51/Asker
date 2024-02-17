from ..Bot import verification as check
from ..Bot import ActionRegister as reg
from ..Bot import Menu as menu
from ..Bot import Action as Action
from ..FileControl import FileManage as fm
from ..DataBase import get_db_connection

import asyncio

from aiogram import Bot
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
#from aiogram.enums import ParseMode
#from aiogram.utils.keyboard import InlineKeyboardBuilder

class Answer:

    def __init__(self,
                 bot: Bot
                 ) -> None:
        self.bot = bot
        self.db = get_db_connection()

    async def start(self,
                    message: Message
                    ) -> None:
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
            await message.answer(
                                text='Приветствую вас снова!\nВыберите, что вы хотите сделать в меню снизу, или пришлите сюда пригласительное сообщение к данному боту, если хотите пройти какой-либо опрос.',
                                reply_markup=await menu.get_menu(menu='start', user=user_data)
            )
        else:
            await message.answer(
                                text=f'{lang.welcome.format(username=username)}\n{lang.about}\n\n{lang.help}',
                                reply_markup=await menu.get_menu(menu='start', user=user_data)
            )
    
    async def get_asks(self,
                       message: Message):
        await message.answer(text="Выберите действие или опрос.",
                             reply_markup=await menu.get_menu_myasks(message.from_user))

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
        usernames = self.db.SQL(f"SELECT `username` FROM `users`")

        if usernames:
            for username in usernames:
                if username[0] != message.text:
                    await message.answer(text="Этого имени не существует!\nВведите, пожалуйста, существующее имя:",
                                        reply_markup=await menu.get_exit_button())
                    
                    return

        file = fm.OpenJson(file_name='Module/Bot/data/login_procces.json')
        file.data[str(message.from_user.id)]['username'] = message.text
        file.update()
        
        await message.answer(text="Введите пароль от аккаунта:",
                             reply_markup=await menu.get_exit_button())
    
    async def login_password(self,
                          message: Message
                          ):
        file = fm.OpenJson(file_name='Module/Bot/data/login_procces.json')
        password = self.db.SQL(f"SELECT `password`, `connected_id` FROM `users` WHERE `username` = '{file.data[str(message.from_user.id)]['username']}'")

        if password[0][0] == message.text:
            connected_id = password[0][1].split(',')
            connected_id.append(str(message.from_user.id))
            connected_id = ','.join(connected_id)

            self.db.SQL(f"UPDATE `users` SET `connected_id` = '{connected_id}' WHERE `username` = '{file.data[str(message.from_user.id)]['username']}'")
            
            await message.answer(text="Вы успешно вошли в аккаунт!",
                                    reply_markup=await menu.get_menu(menu='start', user=message.from_user))
            
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
        exit_username = self.db.SQL(f"SELECT `username` FROM `users` WHERE `username` = '{message.text}'")

        if exit_username:
            await message.answer(text="Данное имя уже занято!\nВыберите другое:",
                             reply_markup=await menu.get_exit_button())

        else:
            self.db.SQL(f"UPDATE `users` SET `username` = '{message.text}' WHERE `user_id` = '{message.from_user.id}' AND `username` = '' ORDER BY id DESC LIMIT 1")

            await message.answer(text="Создайте пароль для вашего аккаунта:",
                             reply_markup=await menu.get_exit_button())

    async def signin_create_password(self,
                     message: Message
                     ) -> None:
        self.db.SQL(f"UPDATE `users` SET `password` = '{message.text}' WHERE `user_id` = '{message.from_user.id}' AND `password` = '' ORDER BY id DESC LIMIT 1")

        await message.answer(text="Вы успешно зарегистрировались!",
                             reply_markup=await menu.get_menu(menu='start', user=message.from_user))

    async def start_questions(self,
                              message: Message
                              ) -> None:
        asker_key = message.text.split('"')[1]
        user_data = message.from_user
    
        #Get ask from databse
        ask_data = await Action.get_ask(asker_key=asker_key,
                                        ask_queue=1)

        if not ask_data:
            return
        
        keyboard = await menu.get_ask_keyboard(ask_data=ask_data)
        
        await message.answer(text=ask_data[0][1],
                                reply_markup=keyboard)

        await Action.add_user_answer_template(user_id=user_data.id, 
                                                ask_data=ask_data, 
                                                asker_key=asker_key)

    async def get_answer(self,
                         message: Message|CallbackQuery
                         ) -> None:
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

            await Action.add_user_answer(answer=message.text if type(message) == Message else message.data.split(':')[1],
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
                await self.bot.send_message(chat_id=message.chat.id,
                                                       text=lang.finished_question,
                                                       reply_markup=await menu.get_menu(menu='start', user=user_data))
            
            else:
                keyboard = await menu.get_ask_keyboard(ask_data=ask_data)

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
            
            keyboard = None
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
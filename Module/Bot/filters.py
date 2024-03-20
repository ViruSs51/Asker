from ..Bot import verification as check
from ..Bot import Action as Action
from ..Bot import Menu as menu
from ..FileControl import FileManage as fm
from ..DataBase import get_db_connection

import asyncio

from aiogram import Bot
from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message

class Start(Filter):

    async def __call__(self,
                       message: Message
                       ) -> bool:
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')

        if message.text == '/start' and (str(message.from_user.id) not in upath.data or upath.data[str(message.from_user.id)] in ['user-cabinet', '']):
            return True

        return False
    
class IsAskerKey(Filter):

    async def __call__(self,
                       message: Message
                       ) -> bool:
        message_check = check.Message(message=message)
        is_asker_key = await message_check.asker_key_in_message()

        return is_asker_key

class UserKeyboardAnswer(Filter):

    async def __call__(self,
                       callback: CallbackQuery
                       ) -> bool:
        user_answers = await Action.get_user_answers(user_id=callback.from_user.id)

        if user_answers:
            for answer in user_answers:
                if not answer[3]:
                    #Get ask from databse
                    ask_data = await Action.get_ask(asker_key=answer[1],
                                                    ask_queue=answer[0])
                    
                    if ask_data[0][2] == 'note':
                        
                        callback_split = callback.data.split(':')

                        if callback_split[0] == 'UserAnswer' and len(callback_split) >= 2 and callback_split[1] in ask_data[0][3].split('#'):
                            return True

        return False

class WaitingUserKeyboardAnswer(Filter):

    async def __call__(self,
                       message: Message
                       ) -> bool:
        if message.text == '⬅️':
            return
        
        user_answers = await Action.get_user_answers(user_id=message.from_user.id)

        if user_answers:
            for answer in user_answers:
                if not answer[3]:
                    #Get ask from databse
                    ask_data = await Action.get_ask(asker_key=answer[1],
                                                    ask_queue=answer[0])
                    
                    if ask_data[0][2] == 'note':
                        return True
                    
                    else:
                        return False
                    
                elif answer[3] and not answer[4]:
                    return True
                
                else:
                    return False

        return False

class UserAnswer(Filter):

    async def __call__(self,
                       message: Message
                       ) -> bool:
        if message.text == '⬅️':
            return
    
        user_answers = await Action.get_user_answers(user_id=message.from_user.id)

        if user_answers:
            for answer in user_answers:
                if not answer[3]:
                    #Get ask from databse
                    ask_data = await Action.get_ask(asker_key=answer[1],
                                                    ask_queue=answer[0])
                    
                    if ask_data[0][2] != 'note':
                        return True
                    
                    else:
                        return False

        return False
        
class UserConfirmed(Filter):

    async def __call__(self,
                       callback: CallbackQuery
                       ) -> bool:
        if callback.data == 'answer-confirmed':
            user_answers = await Action.get_user_answers(user_id=callback.from_user.id)

            if user_answers:
                return await Action.get_answer_from_list(list=user_answers)
                    
        return False
    
class UserNoConfirmed(Filter):

    async def __call__(self,
                       callback: CallbackQuery
                       ) -> bool:
        if callback.data == 'answer-no-confirmed':
            user_answers = await Action.get_user_answers(user_id=callback.from_user.id)

            if user_answers:
                return await Action.get_answer_from_list(list=user_answers)
                    
        return False
    
class UserExitAsker(Filter):

    async def __call__(self,
                       message: Message
                       ) -> bool:
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')

        if str(message.from_user.id) in upath.data and upath.data[str(message.from_user.id)] == 'in-question' and message.text.lower() == '⬅️':
            db = get_db_connection()
            db.SQL(f"DELETE FROM `answers` WHERE `user_id` = '{message.from_user.id}' AND (`is_answer` = '0' OR `confirmed` = '0')")

            return True
                    
        return False
    
class UserCreateName(Filter):
    
    async def __call__(self,
                       message: Message
                       ) -> bool:
        db = get_db_connection()
        id_usernames = db.SQL(f"SELECT `username` FROM `users` WHERE `user_id` = '{message.from_user.id}'")        

        if id_usernames:
            for row in id_usernames:
                if not row[0]:
                    return True

        return False
    
class UserCreatePassword(Filter):

    async def __call__(self,
                       message: Message
                       ) -> bool:
        db = get_db_connection()
        id_passwords = db.SQL(f"SELECT `password` FROM `users` WHERE `user_id` = '{message.from_user.id}'")        

        if id_passwords:
            for row in id_passwords:
                if not row[0]:
                    return True

        return False
    
class UserExitSignin(Filter):

    async def __call__(self,
                       message: Message
                       ) -> bool:
        if message.text.lower() == '⬅️':
            db = get_db_connection()
            id_rows = db.SQL(f"SELECT `username`, `password` FROM `users` WHERE `user_id` = '{message.from_user.id}'")        

            if id_rows:
                for row in id_rows:
                    if not row[0] or not row[1]:
                        return True

        return False
    
class UserExitLogin(Filter):

    async def __call__(self,
                       message: Message
                       ) -> bool:
        if message.text.lower() == '⬅️':
            file = fm.OpenJson(file_name='Module/Bot/data/login_procces.json')

            if str(message.from_user.id) in file.data:
                del file.data[str(message.from_user.id)]
                file.update()

                return True

        return False
    
class UserLoginName(Filter):

    async def __call__(self,
                       message: Message
                       ) -> bool:
        file = fm.OpenJson(file_name='Module/Bot/data/login_procces.json')
        
        if str(message.from_user.id) in file.data and not file.data[str(message.from_user.id)]['username']:
            return True

        return False
    
class UserLoginPassword(Filter):

    async def __call__(self,
                       message: Message
                       ) -> bool:
        file = fm.OpenJson(file_name='Module/Bot/data/login_procces.json')
        
        if str(message.from_user.id) in file.data and not file.data[str(message.from_user.id)]['password']:
            return True

        return False

class UserExitAccount(Filter):

    async def __call__(self,
                       message: Message
                       ) -> bool:
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        
        if str(message.from_user.id) in upath.data and upath.data[str(message.from_user.id)] == 'user-cabinet' and message.text.lower() == '⬅️':
            db = get_db_connection()
            db.SQL(f"DELETE FROM `answers` WHERE `user_id` = '{message.from_user.id}' AND (`is_answer` = '0' OR `confirmed` = '0')")

            return True
                    
        return False

class GetAnswer(Filter):

    async def __call__(self,
                       message: Message
                       ) -> bool:
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')

        if str(message.from_user.id) in upath.data and upath.data[str(message.from_user.id)] == 'user-cabinet':
            db = get_db_connection()
            connected_id = db.SQL(f"SELECT `id` FROM `users` WHERE `connected_id` LIKE '%{message.from_user.id}%'")

            if connected_id and message.text.lower() == 'ответы':
                return True

        return False
    
class GetAsks(Filter):

    async def __call__(self,
                       message: Message
                       ) -> bool:
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')

        if str(message.from_user.id) in upath.data and upath.data[str(message.from_user.id)] == 'user-cabinet':
            db = get_db_connection()
            connected_id = db.SQL(f"SELECT `connected_id` FROM `users`")

            if connected_id:
                connected = False
                for connect in connected_id:
                    if str(message.from_user.id) in connect[0].split(','):
                        connected = True
                        break
                    
                if connected and message.text.lower() == 'мой опросы':
                    return True

            return False
        
class ExitAsks(Filter):

    async def __call__(self,
                       message: Message
                       ) -> bool:
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')

        if str(message.from_user.id) in upath.data and upath.data[str(message.from_user.id)] == 'user-cabinet/question':
            db = get_db_connection()
            connected_id = db.SQL(f"SELECT `id` FROM `users` WHERE `connected_id` LIKE '%{message.from_user.id}%'")

            if connected_id and message.text.lower() == '⬅️':
                return True

        return False
    
class NewAsk(Filter):

    async def __call__(self,
                       message: Message
                       ) -> bool:
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')

        if str(message.from_user.id) in upath.data and upath.data[str(message.from_user.id)] == 'user-cabinet/question':
            db = get_db_connection()
            connected_id = db.SQL(f"SELECT `connected_id` FROM `users`")

            if connected_id:
                connected = False
                for connect in connected_id:
                    if str(message.from_user.id) in connect[0].split(','):
                        connected = True
                        break
                    
                if connected and message.text.lower() == 'новый опрос':
                    return True

        return False
        
class NewAskName(Filter):

    async def __call__(self,
                       message: Message
                       ) -> bool:
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')

        if str(message.from_user.id) in upath.data and upath.data[str(message.from_user.id)] == 'user-cabinet/question/create':
            db = get_db_connection()
            connected_id = db.SQL(f"SELECT `id` FROM `users` WHERE `connected_id` LIKE '%{message.from_user.id}%'")

            if connected_id:
                return True

        return False
        
class ExitAsk(Filter):

    async def __call__(self,
                       message: Message
                       ) -> bool:
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        if str(message.from_user.id) in upath.data:
            path = upath.data[str(message.from_user.id)].split('/')
            db = get_db_connection()
            data_connected = db.SQL(f"SELECT `id`, `asker_key` FROM `users` WHERE `connected_id` LIKE '%{message.from_user.id}%'")

            if message.text.lower() == '⬅️' and data_connected and str(message.from_user.id) in upath.data and (('/'.join(path[:-1]) == 'user-cabinet/question' and path[-1] in data_connected[0][1]) or (upath.data[str(message.from_user.id)] == 'user-cabinet/question/create')):
                return True

        return False
    
class GetAsk(Filter):
    
    async def __call__(self,
                       message: Message
                       ) -> bool:
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')

        if str(message.from_user.id) in upath.data and upath.data[str(message.from_user.id)] == 'user-cabinet/question':
            db = get_db_connection()
            asker_keys = db.SQL(f"SELECT `asker_key` FROM `users` WHERE `connected_id` LIKE '%{message.from_user.id}%'")

            if asker_keys and message.text in asker_keys[0][0]:
                return True

        return False

class DeleteAsk(Filter):
    
    async def __call__(self,
                       message: Message
                       ) -> bool:
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        if str(message.from_user.id) in upath.data:
            split_path = upath.data[str(message.from_user.id)].split('/')

            db = get_db_connection()
            asker_keys = db.SQL(f"SELECT `asker_key` FROM `users` WHERE `connected_id` LIKE '%{message.from_user.id}%'")

            if message.text == '🚫Удалить опрос🚫' and asker_keys and len(split_path) == 3 and '/'.join(split_path[:2]) == 'user-cabinet/question' and split_path[2] in asker_keys[0][0]:
                return True

            return False
    
class GetAskAsk(Filter):
    
    async def __call__(self,
                       message: Message
                       ) -> bool:
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        if str(message.from_user.id) in upath.data:
            split_path = upath.data[str(message.from_user.id)].split('/')

            db = get_db_connection()
            asker_keys = db.SQL(f"SELECT `asker_key` FROM `users` WHERE `connected_id` LIKE '%{message.from_user.id}%'")

            if asker_keys and len(split_path) == 3 and '/'.join(split_path[:2]) == 'user-cabinet/question' and split_path[2] in asker_keys[0][0]:
                queue_ask = db.SQL(f"SELECT `queue` FROM `asks` WHERE `asker_key` = '{split_path[2]}' AND `ask` = '{message.text}'")

                if queue_ask:
                    return True

            return False
    
class EditAskAskText(Filter):
    
    async def __call__(self,
                       message: Message
                       ) -> bool:
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        if str(message.from_user.id) in upath.data:
            split_path = upath.data[str(message.from_user.id)].split('/')

            db = get_db_connection()
            asker_keys = db.SQL(f"SELECT `asker_key` FROM `users` WHERE `connected_id` LIKE '%{message.from_user.id}%'")

            if message.text == 'Редактировать' and asker_keys and len(split_path) == 4 and '/'.join(split_path[:2]) == 'user-cabinet/question' and split_path[2] in asker_keys[0][0]:
                queue_ask = db.SQL(f"SELECT `queue` FROM `asks` WHERE `asker_key` = '{split_path[2]}' AND `ask` = '{split_path[3]}'")

                if queue_ask:
                    return True

            return False

class ExitEditAskAskText(Filter):

    async def __call__(self,
                       message: Message
                       ) -> bool:
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        if str(message.from_user.id) in upath.data:
            split_path = upath.data[str(message.from_user.id)].split('/')

            db = get_db_connection()
            asker_keys = db.SQL(f"SELECT `asker_key` FROM `users` WHERE `connected_id` LIKE '%{message.from_user.id}%'")

            if message.text == '⬅️' and asker_keys and len(split_path) == 5 and '/'.join(split_path[:2]) == 'user-cabinet/question' and split_path[2] in asker_keys[0][0] and split_path[4] == 'edit-text':
                queue_ask = db.SQL(f"SELECT `queue` FROM `asks` WHERE `asker_key` = '{split_path[2]}' AND `ask` = '{split_path[3]}'")

                if queue_ask:
                    return True

            return False
    
class SetEditAskAskText(Filter):

    async def __call__(self,
                       message: Message
                       ) -> bool:
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        if str(message.from_user.id) in upath.data:
            split_path = upath.data[str(message.from_user.id)].split('/')

            db = get_db_connection()
            asker_keys = db.SQL(f"SELECT `asker_key` FROM `users` WHERE `connected_id` LIKE '%{message.from_user.id}%'")

            if asker_keys and len(split_path) == 5 and '/'.join(split_path[:2]) == 'user-cabinet/question' and split_path[2] in asker_keys[0][0] and split_path[4] == 'edit-text':
                queue_ask = db.SQL(f"SELECT `queue` FROM `asks` WHERE `asker_key` = '{split_path[2]}' AND `ask` = '{split_path[3]}'")

                if queue_ask:
                    return True

            return False

class DeleteAskAsk(Filter):
    
    async def __call__(self,
                       message: Message
                       ) -> bool:
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        if str(message.from_user.id) in upath.data:
            split_path = upath.data[str(message.from_user.id)].split('/')

            db = get_db_connection()
            asker_keys = db.SQL(f"SELECT `asker_key` FROM `users` WHERE `connected_id` LIKE '%{message.from_user.id}%'")

            if message.text == '🚫Удалить вопрос🚫' and asker_keys and len(split_path) == 4 and '/'.join(split_path[:2]) == 'user-cabinet/question' and split_path[2] in asker_keys[0][0]:
                queue_ask = db.SQL(f"SELECT `queue` FROM `asks` WHERE `asker_key` = '{split_path[2]}' AND `ask` = '{split_path[3]}'")

                if queue_ask:
                    return True

            return False
    
class ExitAskAsk(Filter):
    
    async def __call__(self,
                       message: Message
                       ) -> bool:
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        if str(message.from_user.id) in upath.data:    
            split_path = upath.data[str(message.from_user.id)].split('/')

            db = get_db_connection()
            asker_keys = db.SQL(f"SELECT `asker_key` FROM `users` WHERE `connected_id` LIKE '%{message.from_user.id}%'")

            if asker_keys and len(split_path) == 4 and '/'.join(split_path[:2]) == 'user-cabinet/question' and split_path[2] in asker_keys[0][0]:
                queue_ask = db.SQL(f"SELECT `queue` FROM `asks` WHERE `asker_key` = '{split_path[2]}' AND `ask` = '{split_path[3]}'")

                if queue_ask and message.text.lower() == '⬅️':
                    return True

            return False
        
class CreateAsk(Filter):
    
    async def __call__(self,
                       message: Message
                       ) -> bool:
        if message.text == 'Новый вопрос':
            upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
            if str(message.from_user.id) in upath.data:
                split_path = upath.data[str(message.from_user.id)].split('/')

                if len(split_path) == 3:
                    db = get_db_connection()
                    asker_keys = db.SQL(f"SELECT `asker_key` FROM `users` WHERE `connected_id` LIKE '%{message.from_user.id}%'")

                    if asker_keys and '/'.join(split_path[:2]) == 'user-cabinet/question' and split_path[2] in asker_keys[0][0]:
                    
                        return True
            
        return False
    
class ExitCreateAsk(Filter):

    async def __call__(self,
                       callback: CallbackQuery
                       ) -> bool:
        if callback.data == 'SetNewAskType:⬅️':
            upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')

            if str(callback.from_user.id) in upath.data:
                split_path = upath.data[str(callback.from_user.id)].split('/')

                if len(split_path) == 4:
                    db = get_db_connection()
                    asker_keys = db.SQL(f"SELECT `asker_key` FROM `users` WHERE `connected_id` LIKE '%{callback.from_user.id}%'")
                    
                    if asker_keys and '/'.join(split_path[:2]) == 'user-cabinet/question' and split_path[2] in asker_keys[0][0] and split_path[3] == 'create':
                        return True

        return False
    
class SetAskType(Filter):

    async def __call__(self,
                       callback: CallbackQuery
                       ) -> bool:
        if callback.data in ['SetNewAskType:text', 'SetNewAskType:note']:
            upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')

            if str(callback.from_user.id) in upath.data:
                split_path = upath.data[str(callback.from_user.id)].split('/')

                if len(split_path) == 4:
                    db = get_db_connection()
                    asker_keys = db.SQL(f"SELECT `asker_key` FROM `users` WHERE `connected_id` LIKE '%{callback.from_user.id}%'")
                    
                    if asker_keys and '/'.join(split_path[:2]) == 'user-cabinet/question' and split_path[2] in asker_keys[0][0] and split_path[3] == 'create':
                        return True

        return False
    
class ExitCreateAskText(Filter):

    async def __call__(self,
                       message: Message
                       ) -> bool:
        if message.text.lower() == '⬅️':
            upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
            if str(message.from_user.id) in upath.data:
                split_path = upath.data[str(message.from_user.id)].split('/')
                db = get_db_connection()
                asker_keys = db.SQL(f"SELECT `asker_key` FROM `users` WHERE `connected_id` LIKE '%{message.from_user.id}%'")
    
                if asker_keys and len(split_path) == 4 and '/'.join(split_path[:2]) == 'user-cabinet/question' and split_path[2] in asker_keys[0][0] and (split_path[3] == 'create' or split_path[3] == 'create-answer'):
                    return True
    
        return False
    
class SetAskText(Filter):

    async def __call__(self,
                       message: Message
                       ) -> bool:
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        if str(message.from_user.id) in upath.data:
            split_path = upath.data[str(message.from_user.id)].split('/')

            if len(split_path) == 4:
                db = get_db_connection()
                asker_keys = db.SQL(f"SELECT `asker_key` FROM `users` WHERE `connected_id` LIKE '%{message.from_user.id}%'")
                ask_type = db.SQL(f"SELECT `type` FROM `asks` WHERE `asker_key` = '{split_path[2]}' ORDER BY id DESC LIMIT 1")
                
                if ask_type[0][0] in ['note', 'text'] and asker_keys and '/'.join(split_path[:2]) == 'user-cabinet/question' and split_path[2] in asker_keys[0][0] and split_path[3] == 'create':
                    return True

        return False

class SetAskAnswer(Filter):

    async def __call__(self,
                       message: Message
                       ) -> bool:
        upath = fm.OpenJson(file_name='Module/Bot/data/userpath.json')
        if str(message.from_user.id) in upath.data:
            split_path = upath.data[str(message.from_user.id)].split('/')

            if len(split_path) == 4:
                db = get_db_connection()
                asker_keys = db.SQL(f"SELECT `asker_key` FROM `users` WHERE `connected_id` LIKE '%{message.from_user.id}%'")
                
                if asker_keys and '/'.join(split_path[:2]) == 'user-cabinet/question' and split_path[2] in asker_keys[0][0] and split_path[3] == 'create-answer':
                    return True

        return False
from ..Bot import verification as check
from ..Bot import Action as Action
from ..Bot import Menu as menu
from ..DataBase import get_db_connection

from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message
    
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

                        if callback_split[0] == 'UserAnswer' and len(callback_split) >= 2 and callback_split[1] in ask_data[0][3].split(','):
                            return True

        return False

class WaitingUserKeyboardAnswer(Filter):

    async def __call__(self,
                       message: Message
                       ) -> bool:
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
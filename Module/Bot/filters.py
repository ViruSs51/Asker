from ..Bot import verification as check
from ..Bot import Action as Action
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
    
class UserAnswer(Filter):

    async def __call__(self,
                       message: Message
                       ) -> bool:
        user_answers = await Action.get_user_answers(user_id=message.from_user.id)

        if user_answers:
            for answer in user_answers:
                if not answer[3]:
                    return True

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
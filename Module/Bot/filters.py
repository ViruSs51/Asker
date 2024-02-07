from ..Bot import verification as check

from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message

class Answer(Filter):

    async def __call__(self,
                       callback: CallbackQuery
                       ) -> bool:
        return callback.data.split('|S|')[0] == 'answer'
    
class IsAskerKey(Filter):

    async def __call__(self,
                       message: Message
                       ) -> bool:
        message_check = check.Message(message=message)
        is_asker_key = await message_check.asker_key_in_message()

        return is_asker_key
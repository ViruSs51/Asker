from aiogram.filters import Filter
from aiogram.types import CallbackQuery

class Answer(Filter):

    async def __call__(self,
                 callback: CallbackQuery
                 ) -> None:
        return callback.data.split('|S|')[0] == 'answer'
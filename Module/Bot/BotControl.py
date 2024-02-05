from ..Bot.Language import lang

from aiogram import types#, F
#from aiogram.enums import ParseMode
#from aiogram.utils.keyboard import InlineKeyboardBuilder

class Answer:

    async def start(self,
                    message: types.Message
                    ) -> None:
        await message.answer(
            text=lang.welcome.format(username=message.from_user.full_name)
        )
from ..Bot import verification as check
from ..Bot import ActionRegister as reg
from ..Bot import Menu as menu
from ..Bot import Action as Action
from ..DataBase import get_db_connection

from aiogram import Bot
from aiogram.types import Message
#from aiogram.enums import ParseMode
#from aiogram.utils.keyboard import InlineKeyboardBuilder

class Answer:

    def __init__(self,
                 bot: Bot
                 ) -> None:
        self.message_register = reg.Message()
        self.bot = bot
        self.db = get_db_connection()

    async def start(self,
                    message: Message
                    ) -> None:
        user_data = message.from_user
        lang = await Action.get_language(user=user_data)

        await self.message_register.delete_message(bot=self.bot,
                                                   message=message,
                                                   n=2)
        
        user = check.User(user=user_data)
        username = await user.get_name()

        #Register message(id and time)
        await self.message_register.register_message(message=message)

        #Welcome and description message
        send_message = await message.answer(
            text=f'{lang.welcome.format(username=username)}\n{lang.about}\n\n{lang.help}',
            reply_markup=await menu.get_menu(menu='start', user=user_data)
        )
        await self.message_register.register_message(message=send_message)

    async def start_questions(self,
                            message: Message
                            ) -> None:
        asker_key = message.text.split('"')[1]

        #Register message(id and time)
        await self.message_register.register_message(message=message)

        await self.message_register.delete_message(bot=self.bot,
                                                   message=message,
                                                   n=3)

    async def another_message(self,
                              message: Message
                              ) -> None:
        #Register message(id and time)
        await self.message_register.register_message(message=message)
            
        await self.message_register.delete_message(bot=self.bot,
                                                   message=message,
                                                   n=1)

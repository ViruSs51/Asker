from aiogram import types

class Action:

    async def start(self,
                    message: types.Message
                    ) -> None:
        await message.answer(text=f'Hello {message.from_user.username}!')
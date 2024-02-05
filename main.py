import NewType
import answer
import filters as f
import FileManage as fm
import SQLCommand as sql

import asyncio
from dataclasses import asdict

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder

class MainBot:
    dp = Dispatcher()

    def __init__(self
                 ) -> None:
        self.loadData()

        self.__database = sql.SQLRequest(
            user=self.__config.config.data['database']['db_username'],
            password=self.__config.config.data['database']['db_password'],
            host=self.__config.config.data['database']['db_host'],
            database=self.__config.config.data['database']['db_name']
        )
        self.bot = Bot(self.bot_data.token)

    def loadData(self
                  ) -> None:
        self.__config = NewType.Config(
            config=fm.OpenJson(file_name='data/config.json')
        )

        self.bot_data = NewType.BotData(
            token=self.__config.config.data['bot']['TOKEN']
        )

    def updateData(self
                ) -> None:
        [file.update() for file in asdict(self.__config).values()]

    async def run(self
                  ) -> None:
        await self.dp.start_polling(self.bot)

class AskerBot(MainBot, answer.Action):

    def __init__(self
                 ) -> None:
        super().__init__()
        self.register()

    def register(self
                 ) -> None:
        self.dp.message(Command('start'))(self.start)

if __name__ == '__main__':
    bot = AskerBot()
    asyncio.run(bot.run())
import Module.Bot.BotControl as BotControl
#import Module.Bot.filters as f

import Module.MultyType.ConfigType as ConfigType

import Module.FileControl.FileManage as fm

from Module.DataBase import get_db_connection

import asyncio
from dataclasses import asdict

from aiogram import Bot, Dispatcher
from aiogram.filters import Command

class MainBot:
    dp = Dispatcher()

    def __init__(self
                 ) -> None:
        self.loadData()
        self.db = get_db_connection()
        
        self.bot = Bot(self.bot_data.token)

    def loadData(self
                  ) -> None:
        self.__config = ConfigType.Config(
            config=fm.OpenJson(file_name='data/config.json')
        )

        self.bot_data = ConfigType.BotData(
            token=self.__config.config.data['bot']['TOKEN']
        )

    def updateData(self
                ) -> None:
        [file.update() for file in asdict(self.__config).values()]

    async def run(self
                  ) -> None:
        await self.dp.start_polling(self.bot)

class AskerBot(MainBot, BotControl.Answer):

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
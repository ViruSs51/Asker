import Module.Bot.BotControl as BotControl
import Module.Bot.filters as f

import Module.MultyType.ConfigType as ConfigType

import Module.FileControl.FileManage as fm

import asyncio
from dataclasses import asdict

from aiogram import Bot, Dispatcher#, F
from aiogram.filters import Command

class MainBot:
    dp = Dispatcher()

    def __init__(self
                 ) -> None:
        self.loadData()
        
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

class AskerBot(MainBot):

    def __init__(self
                 ) -> None:
        super().__init__()
        self.bot_control = BotControl.Answer(bot=self.bot)
        self.register()

        print('Bot started!')

    def register(self
                 ) -> None:
        #Confirmed answer
        self.dp.callback_query((f.UserConfirmed()))(self.bot_control.confirmed_answer)
        self.dp.callback_query((f.UserNoConfirmed()))(self.bot_control.no_confirmed_answer)

        #Question
        self.dp.message(f.UserAnswer())(self.bot_control.get_answer)
        
        #Start questions
        self.dp.message(f.IsAskerKey())(self.bot_control.start_questions)

        #Another command
        self.dp.message(Command('start'))(self.bot_control.start)
        self.dp.message()(self.bot_control.another_message)

if __name__ == '__main__':
    bot = AskerBot()
    asyncio.run(bot.run())
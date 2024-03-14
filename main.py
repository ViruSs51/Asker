import Module.Bot.BotControl as BotControl
import Module.Bot.filters as f

import Module.MultyType.ConfigType as ConfigType

import Module.FileControl.FileManage as fm

import asyncio
from dataclasses import asdict

from aiogram import Bot, Dispatcher, F
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

        #Callback user asks
        self.dp.callback_query((f.SetAskType()))(self.bot_control.set_type_ask)
        self.dp.callback_query((f.ExitCreateAsk()))(self.bot_control.exit_create_ask)

        #Confirmed answer
        self.dp.callback_query((f.UserConfirmed()))(self.bot_control.confirmed_answer)
        self.dp.callback_query((f.UserNoConfirmed()))(self.bot_control.no_confirmed_answer)

        #Keyboard ask register
        self.dp.message(f.WaitingUserKeyboardAnswer())(self.bot_control.another_message)

        #Question
        self.dp.message(f.UserAnswer())(self.bot_control.get_answer)
        self.dp.callback_query(f.UserKeyboardAnswer())(self.bot_control.get_answer)

        #Login
        self.dp.message(f.UserExitLogin())(self.bot_control.exit_login)
        self.dp.message(f.UserLoginName())(self.bot_control.login_name)
        self.dp.message(f.UserLoginPassword())(self.bot_control.login_password)
        self.dp.message(F.text.lower() == 'войти в аккаунт')(self.bot_control.login_start)

        #signin
        self.dp.message(f.UserExitSignin())(self.bot_control.exit_signin)
        self.dp.message(f.UserCreateName())(self.bot_control.signin_create_name)
        self.dp.message(f.UserCreatePassword())(self.bot_control.signin_create_password)
        self.dp.message(F.text.lower() == 'зарегистрироваться')(self.bot_control.signin_start)

        #User asks
        self.dp.message(f.ExitCreateAskText())(self.bot_control.exit_create_ask_text)
        self.dp.message(f.ExitAsk())(self.bot_control.get_asks)
        self.dp.message(f.ExitAsks())(self.bot_control.exit_asks)
        self.dp.message(f.SetAskAnswer())(self.bot_control.set_ask_answer)
        self.dp.message(f.SetAskText())(self.bot_control.set_ask_text)
        self.dp.message(f.CreateAsk())(self.bot_control.create_ask)
        self.dp.message(f.GetAsk())(self.bot_control.get_ask)
        self.dp.message(f.GetAsks())(self.bot_control.get_asks)
        self.dp.message(f.NewAsk())(self.bot_control.create_asker)
        self.dp.message(f.NewAskName())(self.bot_control.set_asker_name)
        
        #Start questions
        self.dp.message(f.IsAskerKey())(self.bot_control.start_questions)

        #Another command
        self.dp.message(f.UserExitAsker())(self.bot_control.start)
        self.dp.message(f.Start(), Command('start'))(self.bot_control.start)
        self.dp.message()(self.bot_control.another_message)

if __name__ == '__main__':
    bot = AskerBot()
    asyncio.run(bot.run())
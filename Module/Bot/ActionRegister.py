from ..FileControl import FileManage as fm
from ..MultyType import ConfigType as ConfigType
from ..DataBase import get_db_connection

from types import FunctionType
from typing import Any

from aiogram import Bot
from aiogram.types import Message

class Register:

    @staticmethod
    def load(func: FunctionType
             ) -> Any:
        async def wrapper(self,
                    *args,
                    **kwargs
                    ) -> Any:
            self.config.config.load()

            result = await func(self,
                          *args,
                          **kwargs
                          )
            
            self.config.config.update()

            return result
        return wrapper

class Language(Register):

    def __init__(self
                 ) -> None:
        self.config = ConfigType.Config(
            config=fm.OpenJson(file_name='Module/Bot/data/LanguageConfig.json')
        )
    
    @Register.load
    async def register_language(self,
                                lang: str,
                                message: Message
                                ) -> None:
        chat_id = str(message.chat.id)
        
        self.config.config.data[chat_id] = lang
    

class Message(Register):

    def __init__(self
                 ) -> None:
        self.config = ConfigType.Config(
            config=fm.OpenJson(file_name='Module/Bot/data/MessageConfig.json')
        )

    #Not use
    @Register.load
    async def __register_message(self,
                               message: Message
                               ) -> None:
        chat_id = str(message.chat.id)

        if chat_id not in self.config.config.data:
            self.config.config.data[chat_id] = [message.message_id]

        else:
            self.config.config.data[chat_id].append(message.message_id)
    
    #Not use
    @Register.load
    async def __delete_message(self,
                             bot: Bot,
                             message: Message,
                             n: int=2,
                             all: bool=False
                             ) -> None:
        '''
            n - cate message se vor fi sterge
        '''

        chat_id = str(message.chat.id)
        
        if chat_id in self.config.config.data:
            message_length = len(self.config.config.data[chat_id])
            if message_length:
                n = message_length if n > message_length else n
                await bot.delete_messages(chat_id=message.chat.id, 
                                          message_ids=self.config.config.data[chat_id][-n:] if not all else self.config.config.data[chat_id])
                self.config.config.data[chat_id] = self.config.config.data[chat_id][:-n]
                
                if all: self.config.config.data[chat_id] = []
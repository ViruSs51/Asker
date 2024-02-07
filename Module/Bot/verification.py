from ..DataBase import get_db_connection
from ..MultyType import ConfigType as ConfigType
from ..FileControl import FileManage as fm
from ..Bot import ActionRegister as reg

from aiogram.types import user, Message

class Language:

    def __init__(self,
                 user: user.User
                 ) -> None:
        self.data = user
        self.language_config = ConfigType.Config(
            config=fm.OpenJson(file_name='Module/Bot/data/LanguageConfig.json')
        )

    async def lang_init(self
                        ) -> bool:
        return str(self.data.id) in self.language_config.config.data
        

class User:

    def __init__(self,
                 user: user.User
                 ) -> None:
        self.data = user
        self.__db = get_db_connection()

    async def get_name(self
                       ) -> str:
        if self.data.username: name = self.data.username
        elif self.data.first_name: name = self.data.first_name
        elif self.data.last_name: name = self.data.last_name
        else: name = str(self.data.id)

        return name
    
    async def in_db(self
                    ) -> bool:
        user_id = self.__db.get_from_table(
            table_name='users',
            column='user_id',
            index='user_id',
            index_value=self.data.id
        )

        return user_id != []
    
class Message:

    def __init__(self,
                 message: Message
                 ) -> None:
        self.data = message
        self.key = None if not message.text.count('"') >= 2 else  message.text.split('"')[1]
        self.__db = get_db_connection()

    async def asker_key_in_message(self
                                   ) -> str|bool:
        asker_key = self.__db.SQL(sql_command='SELECT asker_key FROM `users` WHERE 1')

        if self.key:
            for keys in asker_key:
                for key in keys[0].split(','):
                    if key.split(':')[0] == self.key:
                        language_register = reg.Language()
                        await language_register.register_language(lang=key.split(':')[1],
                                                                  message=self.data)

                        return key.split(':')[0]

        return False
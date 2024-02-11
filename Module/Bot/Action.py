from ..Bot import verification as check
from ..Bot.Language import get_lang
from ..MultyType import LangType
from ..DataBase import get_db_connection

from aiogram.types import user

async def get_language(user: user.User
                       ) -> LangType.Language:
    language = check.Language(user=user)
    lang = await get_lang() if not await language.lang_init() else await get_lang(lang=language.language_config.config.data[str(user.id)])

    return lang

async def get_ask(asker_key: str,
                  ask_queue: int
                  ) -> list[tuple]:
    db = get_db_connection()

    return db.SQL(sql_command=f"SELECT queue, ask, type, answers FROM asks WHERE asker_key='{asker_key}' AND queue={ask_queue}")

async def get_user_answers(user_id: int
                          ) -> list[tuple]:
    db = get_db_connection()

    return db.SQL(sql_command=f"SELECT ask_id, asker_key, answer, is_answer, confirmed FROM answers WHERE user_id='{user_id}'")

async def add_user_answer_template(user_id: int,
                                   ask_data: list[tuple],
                                   asker_key: str
                                   ) -> None:
    db = get_db_connection()
    
    db.SQL(sql_command=f"INSERT INTO `answers` (`user_id`, `ask_id`, `asker_key`, `answer`, `is_answer`, `confirmed`) VALUES ('{user_id}', '{ask_data[0][0]}', '{asker_key}', '', '0', '0')")

async def add_user_answer(answer: str,
                          user_id: int,
                          ask_id: int,
                          asker_key: str
                          ) -> None:
    db = get_db_connection()

    db.SQL(sql_command=f"UPDATE `answers` SET `answer`='{answer}', `is_answer`='1' WHERE `user_id`='{user_id}' AND `ask_id`='{ask_id}' AND `asker_key`='{asker_key}' ORDER BY id DESC LIMIT 1")

async def confirm_user_answer(user_id: int,
                              ask_id: int,
                              asker_key: str
                              ) -> None:
    db = get_db_connection()

    db.SQL(sql_command=f"UPDATE `answers` SET `confirmed`='1' WHERE `user_id`='{user_id}' AND `ask_id`='{ask_id}' AND `asker_key`='{asker_key}' ORDER BY id DESC LIMIT 1")

async def reset_user_answer(user_id: int,
                            ask_id: int,
                            asker_key: str
                            ) -> None:
    db = get_db_connection()

    db.SQL(sql_command=f"UPDATE `answers` SET `answer`='', `is_answer`='0', `confirmed`='0' WHERE `user_id`='{user_id}' AND `ask_id`='{ask_id}' AND `asker_key`='{asker_key}' ORDER BY `id` DESC LIMIT 1")

async def get_answer_from_list(list: list[tuple]
                               ) -> tuple|None:
    for answer in list:
        if answer[3] and not answer[4]:
            return answer
        
    else:
        return None

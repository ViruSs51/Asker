from ..DataBase import config
from ..DataBase import SQLCommand as sql

def get_db_connection() -> sql.SQLRequest:
    db = sql.SQLRequest(
        user=config.data.db_user,
        password=config.data.db_password,
        host=config.data.db_host,
        database=config.data.db_name
    )

    return db
from ..FileControl import FileManage as fm

from dataclasses import dataclass


@dataclass
class Config:
    config: fm.OpenJson

@dataclass
class BotData:
    token: str

@dataclass
class ConfigDataBase:
    db_name: str
    db_user: str
    db_password: str
    db_host: str
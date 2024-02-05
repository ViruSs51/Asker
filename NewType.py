import FileManage as fm

from dataclasses import dataclass


@dataclass
class Config:
    config: fm.OpenJson

@dataclass
class BotData:
    token: str
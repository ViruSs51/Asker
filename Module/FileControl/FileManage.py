import typing
from json import dump, loads

import pandas as pd

class OpenJson:

    def __init__(self,
                 file_name: str,
                 load_file: bool = True
                 ):
        self.__file = file_name
        self.load()

    def load(self
             ) -> None:
        with open(self.__file, 'r', encoding='utf-8') as file:
            self.data = loads(file.read())

    def update(self
               ) -> None:
        with open(self.__file, 'w', encoding='utf-8') as file:
            dump(self.data, file, indent=4)

class OpenCSV:

    def __init__(self, 
                 file_name: str
                 ) -> None:
        self.__file = file_name

    def create(self,
               column_title: list[str]|tuple[str],
               columns: list[list]|list[tuple]|tuple[list]|tuple[tuple]
               ):
        self.data = pd.DataFrame(columns, columns=column_title)
        self.data.to_csv(self.__file, index=False)

    def load(self
             ) -> None:
        self.data = pd.read_csv(self.__file)

    def update(self
               ) -> None:
        self.data.to_csv(self.__file, index=False)
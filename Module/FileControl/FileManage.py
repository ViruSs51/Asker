from json import dump, loads

class OpenJson:

    def __init__(self, 
                 file_name: str
                 ) -> None:
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
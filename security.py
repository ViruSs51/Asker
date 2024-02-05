import hashlib
import secrets

class Encrypting:

    def __init__(self,
                 data: str
                 ) -> None:
        self.__data = data.encode()
        self.__salt = secrets.token_hex(nbytes=20).encode()

    def set_salt(self,
                 salt
                 ) -> None:
        self.__salt = salt

    def encrypt(self
                ) -> None:
        self.hash_data = [hashlib.sha256(string=self.__salt+self.__data+self.__salt).hexdigest(), self.__salt]

    def verification(self,
                     data: str
                     ) -> bool:
        hash = Encrypting(data=data)
        hash.set_salt(salt=self.hash_data[1])
        hash.encrypt()

        return self.hash_data[0] == hash.hash_data[0]
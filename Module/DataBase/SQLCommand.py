from types import FunctionType
from typing import Any

from mysql.connector import connect, Error
from mysql.connector.cursor_cext import CMySQLCursor

class SQLRequest:

    def __init__(self,
                 user: str,
                 password: str,
                 host: str='localhost',
                 database: None|str=None
                 ) -> None:
        self.__user = user
        self.__password = password
        self.__host = host
        self.__database = database
    
    def connect(func: FunctionType
                ) -> Any:
        def wrapper(self,
                    *args,
                    **kwargs
                    ) -> Any:
            try:
                with connect(host=self.__host,
                             user=self.__user,
                             password=self.__password,
                             database=self.__database,
                             raise_on_warnings=True
                             ) as connector:
                    with connector.cursor() as cursor:
                        cursor.execute("SET NAMES 'utf8'")

                        result = func(self, 
                                      cursor=cursor,
                                      *args,
                                      **kwargs
                                      )

                return result
            
            except Error as err:
                print(err)
                return err

        return wrapper

    @connect
    def SQL(self,
            sql_command: str,
            cursor: CMySQLCursor|None=None
            ) -> list|None:
        cursor.execute(sql_command)
        output = cursor.fetchall()

        return output if output else None

    @connect
    def delete_table(self,
             table_name: str,
             cursor: CMySQLCursor|None=None
             ) -> None:
        ''' DROP TABLE `table-name` '''
        cursor.execute(f"DROP TABLE `{table_name}`")

    @connect
    def create_table(self,
             table_name: str,
             column: tuple|list,
             cursor: CMySQLCursor|None=None
             ) -> None:
        ''' CREATE TABLE `table-name` (id INT(10) NOT NULL AUTO_INCREMENT, text VARCHAR(200) NOT NULL) '''
        cursor.execute(f"CREATE TABLE `{table_name}` (id INT(10) NOT NULL AUTO_INCREMENT, {','.join(column)}, PRIMARY KEY(id))")

    @connect
    def insert_in_table(self,
             table_name: str,
             column_name: tuple|list,
             values: tuple|list,
             cursor: CMySQLCursor|None=None
             ) -> None:
        ''' INSERT INTO `table-name` (`text`) VALUES('Hello world!') '''
        cursor.execute(f"INSERT INTO `{table_name}` ({','.join(column_name)}) VALUES({','.join(values)})")

    @connect
    def delete_from_table(self,
             table_name: str,
             index: str,
             index_value: str,
             cursor: CMySQLCursor|None=None
             ) -> None:
        ''' DELETE FROM `table-name` WHERE `id` = id-value '''
        cursor.execute(f"DELETE FROM `{table_name}` WHERE `{index}` = {index_value}")

    @connect
    def update_row_in_table(self,
             table_name: str,
             column: str,
             value: str,
             index: str,
             index_value: str,
             cursor: CMySQLCursor|None=None
             ) -> None:
        ''' UPDATE `table-name` SET `column-name` = 'new-value' WHERE `id` = id-value '''
        cursor.execute(f"UPDATE `{table_name}` SET `{column}` = '{value}' WHERE `{index}` = {index_value}")

    @connect
    def get_from_table(self,
             table_name: str,
             column: str,
             index: str,
             index_value: str,
             cursor: CMySQLCursor|None=None
             ) -> list:
        ''' SELECT `column` FROM `table-name` '''
        cursor.execute(f"SELECT {column} FROM {table_name} WHERE {index} = '{index_value}'")

        return cursor.fetchall()
    
    @connect
    def get_tables(self,
                   column: str,
                   cursor: CMySQLCursor|None=None
                   ) -> list:
        ''' SELECT `column` FROM information_schema.tables FROM table_schema = 'database-name' '''
        cursor.execute(f"SELECT {column} FROM information_schema.tables WHERE table_schema = '{self.__database}'")

        return cursor.fetchall()
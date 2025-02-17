import pymysql
from pymysql.cursors import Cursor
from pymysql.connections import Connection
from typing import Optional, Dict

class DBConnector:

    def __init__(self, dbconfig: Dict):
        self._dbconfig: Dict = dbconfig
        self._connection: Optional[Connection] = self._set_connection()
        self._cursor: Optional[Cursor] = self._set_cursor()

    def _set_connection(self) -> Optional[Connection]:
        try:
            connection: Connection = pymysql.connect(**self._dbconfig)
            return connection
        except pymysql.MySQLError as e:
            print(f"Ошибка подключения к БД: {e}")
            return None

    def _set_cursor(self) -> Optional[Cursor]:
        if self._connection:
            try:
                cursor: Cursor = self._connection.cursor()
                return cursor
            except Exception as e:
                print(f"Ошибка курсора: {e}")
            return None

    def get_connection(self) -> Optional[Connection]:
        return self._connection

    def get_cursor(self) -> Optional[Cursor]:
        return self._cursor

    def close(self):
        if self._connection.open:
            self._cursor.close()
            self._connection.close()
            print("Подключение к БД и курсор закрыты.")


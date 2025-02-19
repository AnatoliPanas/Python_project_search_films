import pymysql
from pymysql.cursors import Cursor, DictCursor
from pymysql.connections import Connection
from typing import Optional, Dict, Tuple


class LoggingDictCursor(DictCursor):
    def execute(self, query, params: Tuple = ()):

        print(f"Выполняется запрос: {query} с параметрами {params}")
        # # Записываем запрос в таблицу query_logs
        # try:
        #     # Предполагается, что у нас уже есть соединение с БД
        #     self._connection.ping(reconnect=True)  # Проверяем соединение
        #     log_query = """
        #     INSERT INTO query_logs (query, params)
        #     VALUES (%s, %s)
        #     """
        #     self._connection.cursor().execute(log_query, (query, params))
        #     self._connection.commit()
        # except pymysql.MySQLError as e:
        #     print(f"Ошибка при записи лога в базу данных: {e}")

        return super().execute(query, params)

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

    def commit(self):
        try:
            self._connection.commit()
        except pymysql.Error as e:
            print(f"Ошибка при вставке в БД: {e}")
            self._connection.rollback()

    def rollback(self):
        try:
            self._connection.rollback()
        except pymysql.Error as e:
            print(f"Ошибка при вставке в БД: {e}")

    def close(self):
        if hasattr(self, '_connection') and hasattr(self, '_cursor'):
            self._cursor.close()
            self._connection.close()
            print("Подключение к БД и курсор закрыты.")


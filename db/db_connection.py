import pymysql
from pymysql.cursors import Cursor
from pymysql.connections import Connection
from typing import Optional, Dict
from Utils.custom_logger import CustomLogger


class DBConnector(CustomLogger):

    def __init__(self, dbconfig: Dict):
        super().__init__(name=__name__)
        self._dbconfig: Dict = dbconfig
        self.db_name: str = dbconfig.get("database")
        self._connection: Optional[Connection] = self._set_connection()
        self._cursor: Optional[Cursor] = self._set_cursor()
        self.get_logger().info(f"Создание DBConnector с конфигурацией БД: {self.db_name} - выполнено.")

    def _set_connection(self) -> Optional[Connection]:
        try:
            connection: Connection = pymysql.connect(**self._dbconfig)
            self.get_logger().info(f"Подключение к БД: {self.db_name} - выполнено.")
            return connection
        except pymysql.MySQLError as e:
            self.get_logger().error(f"Ошибка подключения к БД: {self.db_name} - {e}")
            raise ConnectionError(f"Ошибка подключения к БД: {self.db_name} - {e}")

    def _set_cursor(self) -> Optional[Cursor]:
        if self._connection:
            try:
                cursor = self._connection.cursor()
                self.get_logger().info("Создание курсор для выполнения запросов в БД: {self.db_name} - выполнено.")
                return cursor
            except pymysql.MySQLError as e:
                self.get_logger().error(f"Ошибка создания курсора: {e}")
                raise pymysql.MySQLError("Ошибка создания курсора!")

    def get_connection(self) -> Optional[Connection]:
        return self._connection

    def get_cursor(self) -> Optional[Cursor]:
        return self._cursor

    def get_bd_name(self):
        return self.db_name

    def commit(self):
        try:
            self._connection.commit()
            self.get_logger().info(f"Фиксация изменения в БД: {self.db_name} - выполнено.")
        except pymysql.MySQLError as e:
            self.get_logger().error(f"Ошибка при попытке фиксации изменения в БД: {self.db_name} - {e}")
            self._connection.rollback()

    def rollback(self):
        try:
            self._connection.rollback()
        except pymysql.Error as e:
            self.get_logger().error(f"Ошибка при попытке отката фиксации изменения в БД: {self.db_name} - {e}")

    def close(self):
        if hasattr(self, '_connection') and hasattr(self, '_cursor'):
            self._cursor.close()
            self._connection.close()
            self.get_logger().info(f"Подключение и курсор к БД: {self.db_name} закрыты.")


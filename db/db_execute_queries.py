import pymysql
from db.db_connection import DBConnector
from typing import List, Tuple, Optional, Dict


class DBExecuteQueries(DBConnector):
    def __init__(self, dbconfig):
        super().__init__(dbconfig)

    def get_records(self, query: str, params: Tuple = ()) -> Optional[List]:
        cursor = self.get_cursor()
        try:
            cursor.execute(query, params)
            records = cursor.fetchall()
            return records
        except pymysql.MySQLError as e:
            print(f"Ошибка выполнения запроса: {e}")
            return None

    def get_record(self, query, params: Tuple = ()) -> Optional[Dict]:
        cursor = self.get_cursor()
        try:
            cursor.execute(query, params)
            record = cursor.fetchone()
            return record
        except pymysql.MySQLError as e:
            print(f"Ошибка выполнения запроса: {e}")
            return None

    def execute_ins_upd_del(self, query, params: Tuple = ()) -> bool:
        cursor = self.get_cursor()
        try:
            cursor.execute(query, params)
            self.commit()
            return True
        except pymysql.MySQLError as e:
            print(f"Ошибка выполнения запроса: {e}")
            self.rollback()
            return False



import pymysql
from pymysql.cursors import DictCursor
from db.db_connection import DBConnector
from typing import List, Tuple, Optional, Dict

from db.sql_queries import FilmQueries, SearchCriteriaFilm


class LoggingDictCursor(DictCursor):
    def execute(self, query, params: Tuple = ()):

        print(f"Выполняется запрос: {query} с параметрами {params}")
        # try:
            # log_query = """
            # log_query = SearchCriteriaFilm.INSERT_CRITERIAFILM
            # self._connection.cursor().execute(log_query, (','.join(params), query))
            # self._connection.commit()
        # except pymysql.MySQLError as e:
        #     print(f"Ошибка при записи лога в базу данных: {e}")

        return super().execute(query, params)

class DBQueriesManager(DBConnector):
    def __init__(self, dbconfig):
        self._dbconfig = dbconfig
        super().__init__(dbconfig)

    def get_records(self, query: str, params = ()) -> Optional[List]:
        cursor = self.get_cursor()
        try:
            cursor.execute(query, params)
            records = cursor.fetchall()
            return records
        except pymysql.MySQLError as e:
            print(f"Ошибка выполнения запроса: {e}")
            return None

    def get_record(self, query, params = ()) -> Optional[Dict]:
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

    def get_bd_name(self):
        return self._dbconfig.get("database")

    def get_converting_SQLquery(self, query: str, *args ):
        placeholders = []
        for arg in args:
            if arg and arg != [''] and isinstance(arg, list):
                placeholder = ', '.join(['%s'] * len(arg))
                if placeholder:
                    placeholders.append(placeholder)
            elif isinstance(arg, dict):
                query = query.format(*arg.get('s'))
            elif isinstance(arg, str):
                placeholder = '%s'
                if placeholder:
                    placeholders.append(placeholder)

        query = query % tuple(placeholders)

        # params = [item for arg in args for item in arg if arg != [''] and isinstance(arg, list)]
        params = [item for arg in args for item in arg if arg != ['']]
        return query, params
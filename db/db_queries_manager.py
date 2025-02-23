import pymysql, logging
from pymysql.cursors import DictCursor
from db.db_connection import DBConnector
from typing import List, Tuple, Optional, Dict

from db.sql_queries import FilmQueries, SearchCriteriaFilm

logging.basicConfig(level=logging.INFO)
# Чтобы знать с какого модуля сообщение
logger = logging.getLogger(__name__)

class LoggingDictCursor(DictCursor):
    def execute(self, query: str, params: Tuple = ()):

        logger.info(f"Выполняется запрос: {query} с параметрами {params}")
        # try:
            # log_query = """
            # log_query = SearchCriteriaFilm.INSERT_CRITERIAFILM
            # self._connection.cursor().execute(log_query, (','.join(params), query))
            # self._connection.commit()
        # except pymysql.MySQLError as e:
        #     print(f"Ошибка при записи лога в базу данных: {e}")
        try:
            return super().execute(query, params)
        except pymysql.MySQLError as e:
            logger.error(f"Ошибка выполнения запроса: {e}")

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
            logger.error(f"Ошибка выполнения запроса [get_records]: {e}")
            return None

    def get_record(self, query: str, params = ()) -> Optional[Dict]:
        cursor = self.get_cursor()
        try:
            cursor.execute(query, params)
            record = cursor.fetchone()
            return record
        except pymysql.MySQLError as e:
            logger.error(f"Ошибка выполнения запроса [get_record]: {e}")
            return None

    def execute_ins_upd_del(self, query: str, params: Tuple = ()) -> bool:
        cursor = self.get_cursor()
        try:
            cursor.execute(query, params)
            self.commit()
            return True
        except pymysql.MySQLError as e:
            logger.error(f"Ошибка выполнения запроса [execute_ins_upd_del]: {e}")
            self.rollback()
            return False

    def get_bd_name(self):
        return self._dbconfig.get("database")

    def get_converting_SQLquery(self, query: str, *args) -> Tuple[str, List]:
        placeholders = []
        params = []

        for arg in args:
            if arg and arg != [''] and isinstance(arg, list):
                placeholder = ', '.join(['%s'] * len(arg))
                placeholders.append(placeholder)
                params.extend(arg)
            elif isinstance(arg, dict):
                query = query.format(**arg)
            elif isinstance(arg, str):
                placeholders.append('%s')
                params.append(arg)

        query = query % tuple(placeholders) if placeholders else query
        return query, params
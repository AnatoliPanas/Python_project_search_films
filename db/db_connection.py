import pymysql

class DBConnector:

    def __init__(self, dbconfig: dict):
        self._dbconfig = dbconfig
        self._connection = self._set_connection()
        self._cursor = self._set_cursor()

    def _set_connection(self):
        connecion = pymysql.connect(**self._dbconfig)
        return connecion

    def _set_cursor(self):
        cursor = self._connection.cursor()
        return cursor

    def get_connection(self):
        return self._connection

    def get_cursor(self):
        return self._cursor

    def close(self):
        if self._connection.open:
            self._cursor.close()
            self._connection.close()


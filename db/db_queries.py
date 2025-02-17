from pymysql.cursors import DictCursor

from db_connection import DBConnector

class QueryHandler(DBConnector):
    def __init__(self, dbconfig):
        super().__init__(dbconfig)

    def get_all_roles(self, t_name):
        cursor = self.get_cursor()
        cursor.execute(f"select * from {t_name}")
        records = cursor.fetchall()
        return records

    def get_role_id_by_name(self, name_role: str):
        cursor = self.get_cursor()
        cursor.execute("select id from Role where name = %s", (name_role,))
        records = cursor.fetchone()
        if records:
            return records
        return None

    # def get_field_name(self, t_name: str):
    #     cursor = self.get_cursor()
    #     cursor.execute(f"select * from {t_name} limit 1")
    #     return cursor.fetchone()

    def get_field_name_new(self, t_name: str):
        cursor = self.get_cursor()
        cursor.execute(f"describe {t_name}")
        return [column['Field'] for column in cursor.fetchall()]


    def get_user_query(self, t_name: str, operator: str, value: str, field_name: str):
        cursor = self.get_cursor()
        cursor.execute(f"select * from {t_name} where {field_name} {operator} {value}")
        return cursor.fetchall()


dbconfig = {
            'host': 'ich-edit.edu.itcareerhub.de',
            'user': 'ich1',
            'password': 'ich1_password_ilovedbs',
            'database': '160924_social_blogs',
            'charset': 'utf8mb4',
        'cursorclass': DictCursor
        }

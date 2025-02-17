import os, ast
from dotenv import load_dotenv
from pymysql.cursors import DictCursor

class DBConfig:
    def __init__(self):
        load_dotenv()
        self._all_name_configs = self._set_all_name_configs()


    def _set_all_name_configs(self) -> list[str]:
        env_variables = [key for key in os.environ.keys() if key.startswith('DBCONFIG_')]
        return env_variables

    def get_config(self, db_name: str = None, cursor_class: bool=True) -> dict | None:
        if db_name in self._all_name_configs:
            dbconfig_str = os.getenv(db_name)
            dbconfig_dict = ast.literal_eval(dbconfig_str)
            if cursor_class:
                dbconfig_dict['cursorclass'] = DictCursor
            return dbconfig_dict
        return None

    def get_all_name_configs(self) -> list[str]:
        return self._all_name_configs

# db_conf = DBConfig()
# test  = db_conf.get_all_name_configs()
# bd_sakila = db_conf.get_config("DBCONFIG_SAKILA")
#
# print(test)
# print(bd_sakila)

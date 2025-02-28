import os, ast
from dotenv import load_dotenv
from typing import Optional, Dict, List
from Utils.custom_logger import CustomLogger
from db.db_queries_manager import LoggingDictCursor


class DBConfigManager(CustomLogger):
    def __init__(self):
        super().__init__(name=__name__)
        load_dotenv()
        self._all_name_configs = self._set_all_name_configs()

    def _set_all_name_configs(self) -> List[str]:
        env_variables = [key for key in os.environ if key.startswith('DBCONFIG_')]
        return env_variables

    def get_config(self, db_name: Optional[str] = None, cursor_class: bool=True) -> Optional[Dict]:
        if db_name in self._all_name_configs:
            dbconfig_str = os.getenv(db_name)
            if dbconfig_str:
                try:
                    dbconfig_dict = ast.literal_eval(dbconfig_str)
                    if cursor_class:
                        dbconfig_dict['cursorclass'] = LoggingDictCursor
                    return dbconfig_dict
                except (ValueError, SyntaxError) as e:
                    self.get_logger().error(f"Ошибка при попытке преобразовать конфигурацию {db_name} в словарь: {e}")
        return None

    def get_all_name_configs(self) -> List[str]:
        return self._all_name_configs

# db_conf = DBConfig()
# test  = db_conf.get_all_name_configs()
# bd_sakila = db_conf.get_config("DBCONFIG_SAKILA")
#
# print(test)
# print(bd_sakila)

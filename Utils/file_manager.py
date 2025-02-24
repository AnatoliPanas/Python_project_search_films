from datetime import datetime
from pathlib import Path
from typing import Optional
from Utils.custom_logger import CustomLogger


class FileManager(CustomLogger):
    def __init__(self, data: str, name_file_dir: str = "downloaded_files"):
        super().__init__(name=__name__)
        self._data = data
        self._name_file_dir = name_file_dir
        self._target_dir = self.create_dir()

    def create_dir(self) -> Optional[Path]:
        try:
            dir_path = Path(__file__).parent.parent / self._name_file_dir
            if not dir_path.exists():
                dir_path.mkdir()
                self.get_logger().info(f"Создание директории: {dir_path} - выполнено.")
            else:
                self.get_logger().info(f"Директория - {dir_path} существует.")
            return dir_path
        except Exception as e:
            self.get_logger().error(f"Ошибка при создании директории: {e}")
            return None

    def save_file(self) -> bool:
        file_path = self._target_dir / f"file_{datetime.now().date()}"
        try:
            with open(file_path, "w", encoding="utf-8") as obj_file:
                obj_file.write(self._data)
                self.get_logger().info(f"Запись в файл: {file_path} - выполнено.")
                return True
        except FileNotFoundError as e:
            self.get_logger().error(f"Ошибка! Файл не найден: {e}")
            return False
        except Exception as e:
            self.get_logger().error(f"Ошибка: {e}")
            return False

# file_manager = FileManager("Ntcn")
# result = file_manager.save_file()
#
# if result:
#     print("Данные успешно записаны в файл.")
# else:
#     print("Произошла ошибка при записи в файл.")

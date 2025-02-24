import tkinter as tk
from tkinter import messagebox
from typing import Optional
from Utils.custom_logger import CustomLogger
from conrlols.CustomButton import CustomButton
from conrlols.MultiSelectCombobox import MultiSelectCombobox
from db.db_configs_manager import DBConfigManager
from db.db_queries_manager import DBQueriesManager
from db.sql_queries import CategoryQueries, FilmQueries, SearchCriteriaFilm
import re
from Utils.file_manager import FileManager


class FilmSearchUI(CustomLogger):
    def __init__(self, root):
        self.root = root
        self.root.title("Поиск фильмов")
        self.root.geometry("800x830")
        self.root.resizable(False, False)

        self.memo_field = None
        self.title_discr_entry = None
        self.genre_cb = None
        self.year_cb = None
        self.handler_read = None
        self.handler_write = None
        self.genres = []
        self.years = []

        self.initialize_handlers()
        self.create_ui()

    def create_ui(self):
        search_frame = tk.Frame(self.root)
        search_frame.grid(row=0, column=0, padx=10, pady=5)

        self.memo_field = tk.Text(self.root, wrap="word", state="disabled", font=("Arial", 12))
        self.memo_field.grid(row=1, column=0, padx=10, pady=5)

        bottom_frame = tk.Frame(self.root)
        bottom_frame.grid(row=2, column=0, padx=10, pady=5, sticky="es")

        label_frame = tk.LabelFrame(search_frame, text="Введите критерий поиска", font=("Arial", 12, "bold"), padx=10,
                                    pady=10)
        label_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        title_discr_label = tk.Label(label_frame, text="Ключевое слово (через запятую):", font=("Arial", 10))
        title_discr_label.grid(row=0, column=0, sticky="w", padx=10, pady=1)
        self.title_discr_entry = tk.Text(label_frame, wrap="word", font=("Arial", 12), width=25, height=5)
        self.title_discr_entry.grid(row=1, column=0, padx=10, pady=1)

        genre_label = tk.Label(label_frame, text="Жанр (через запятую):", font=("Arial", 10))
        genre_label.grid(row=0, column=1, sticky="w", padx=10, pady=1)
        self.genre_cb = MultiSelectCombobox(label_frame, self.genres)
        self.genre_cb.frame.grid(row=1, column=1, padx=10, pady=1, sticky="n")

        year_label = tk.Label(label_frame, text="Год:", font=("Arial", 10))
        year_label.grid(row=0, column=2, sticky="w", padx=10, pady=1)
        self.year_cb = MultiSelectCombobox(label_frame, self.years)
        self.year_cb.frame.grid(row=1, column=2, padx=10, pady=1, sticky="n")

        CustomButton(bottom_frame, "Поиск", self.search, 0, 1, "#3e8e41", "#4CAF50")
        CustomButton(bottom_frame, "Посл. запросы", self.last_search, 0, 2, "#3e8e41", "#4CAF50")
        CustomButton(bottom_frame, "В файл", self.save_file, 0, 3, "#3e8e41", "#4CAF50")
        CustomButton(bottom_frame, "Выход", self.exit_program, 0, 4, "#D32F2F", "#f44336")

        db_name_label = tk.Label(bottom_frame, text="БД:", font=("Arial", 10))
        db_name_label.config(text=f"БД на чтение: {self.handler_read.get_bd_name()}\n"
                                  f"БД на запись: {self.handler_write.get_bd_name()}")
        db_name_label.grid(row=0, column=0, sticky="w", padx=10, pady=1)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def set_data_in_memo(self, data):
        self.memo_field.config(state="normal")
        self.memo_field.delete(1.0, tk.END)
        self.memo_field.insert(tk.END, data)
        self.memo_field.config(state="disabled")

    def last_search(self):
        query = SearchCriteriaFilm.GET_LAST_SEARCH
        try:
            records = self.handler_write.get_records(query)
            if records:
                result_search = "\n".join(
                    [f"Дата: {record.get('cdate')} - {record.get('category_by_words')}" for record in records])
            final_memo = f"Последние 20 поисков:\n\n{result_search}"
            self.set_data_in_memo(final_memo)
        except Exception as e:
            self.get_logger().error(f"Ошибка при получении последних запросов: {e}")

    def exit_program(self):
        try:
            self.handler_read.close()
            self.handler_write.close()
            self.root.quit()
        except Exception as e:
            self.get_logger().error(f"Ошибка при закрытии программы: {e}")

    def save_file(self):
        try:
            text_from_memo = self.memo_field.get("1.0", tk.END).strip()
            file_manager = FileManager(text_from_memo)
            file_manager.save_file()

            messagebox.showinfo("Успех", "Данные успешно сохранены в файл.")
        except Exception as e:
            self.get_logger().error(f"Ошибка при сохранении в файл: {e}")

    def search(self):
        try:
            selected_years = [var.get() for var in self.year_cb.check_vars if var.get()]
            selected_genres = [var.get() for var in self.genre_cb.check_vars if var.get()]
            text_title_discr = self.title_discr_entry.get("1.0", tk.END).strip()

            query = FilmQueries.GET_FILM_BY_CATEGORYS
            if selected_years:
                query = query.replace('--where', 'where').replace('--SET_PARAM_YEARS', FilmQueries.SET_PARAM_YEARS)
            if selected_genres:
                query = query.replace('--where', 'where').replace('--SET_PARAM_CATEGORYS',
                                                                  FilmQueries.SET_PARAM_CATEGORYS)
            if text_title_discr:
                query = query.replace('--where', 'where')
                text_title_discr = re.sub(r'\s*,\s*', ',', re.sub(r'\s+', ' ', text_title_discr)).strip(',')
                temp_query = ""
                temp_text_title_discr = ""
                for i, text in enumerate(text_title_discr.split(','), 1):
                    query = query.replace('--(', '(')
                    temp_query += f"{FilmQueries.SET_PARAM_TEXT} or \n"
                    temp_text_title_discr += f'%{text}%,'

                    if i == len(text_title_discr.split(',')):
                        temp_query = re.sub(r'\s(and|or)\s*$', '', temp_query, flags=re.I)

                text_title_discr = [[x] for x in temp_text_title_discr.strip(',').split(',')]
                query = query.replace('--SET_PARAM_TEXT', temp_query)

            query = re.sub(r'--.*\n', '', query)
            query = re.sub(r'\s(and|or)\s*$', '', query, flags=re.I)

            if self.handler_read:
                query, params = self.handler_read.get_converting_SQLquery(query, selected_genres, selected_years,
                                                                          *text_title_discr)
                res = self.handler_read.get_records(query, params)

                execute_params = [','.join(params), query]
                self.execute_query(execute_params)

                result_search = ""
                if res:
                    result_search = "\n".join([
                                                  f"Название: {i.get('title')} ({i.get('length')} мин)\nЖанр: {i.get('name_category')} Год: {i.get('release_year')}\nОписание: {i.get('description')}\n{'-' * 50}"
                                                  for i in res])

                search_criteria = f"Ключевое слово: {self.title_discr_entry.get('1.0', 'end-1c')}\nЖанр: {', '.join(selected_genres)}\nГод: {', '.join(selected_years)}"
                final_memo = f"Критерии поиска:\n{search_criteria}\n\nНайдено: {len(res)}\n{result_search}"
                self.set_data_in_memo(final_memo)
        except Exception as e:
            self.get_logger().error(f"Ошибка при поиске фильмов: {e}")

    def execute_query(self, params) -> None:
        try:
            if self.handler_write:
                self.handler_write.execute_ins_upd_del(SearchCriteriaFilm.INSERT_CRITERIAFILM, params)
        except Exception as e:
            self.get_logger().error(f"Ошибка при выполнении запроса: {e}")

    def initialize_handlers(self):
        self.handler_read = self.get_query_handler("DBCONFIG_SAKILA")
        self.handler_write = self.get_query_handler("DBCONFIG_ICH_EDIT")
        if self.handler_read and self.handler_write:
            record = self.handler_read.get_records(query=CategoryQueries.GET_ALL_CATEGORYS)
            self.genres = [name_category["name_categorys"] for name_category in record]

            record = self.handler_read.get_records(query=FilmQueries.GET_ALL_YEAR)
            self.years = [year["release_year"] for year in record]


    def get_query_handler(self, par_db_name: str) -> Optional[DBQueriesManager]:
        try:
            obj_dbconfig = DBConfigManager()
            dbconfig = obj_dbconfig.get_config(db_name=par_db_name)
            return DBQueriesManager(dbconfig)
        except Exception as e:
            self.get_logger().error(f"Ошибка [get_query_handler]: {e}")
            return None


if __name__ == "__main__":
    root = tk.Tk()
    ui = FilmSearchUI(root)
    root.mainloop()

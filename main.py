import tkinter as tk
from tkinter import messagebox
from typing import Optional
from Utils.custom_logger import CustomLogger
from conrlols.CustomButton import CustomButton
from conrlols.MultiSelectCombobox import MultiSelectCombobox
from db.db_configs_manager import DBConfigManager
from db.db_queries_manager import DBQueriesManager
from db.sql_queries import CategoryQueries, FilmQueries, PopularCriteriaFilm
import re
from Utils.file_manager import FileManager

# Константы для цветов
FRAME_BG = "#fafafa"
CONTROL_BG = "#333333"
CONTROL_FG = "#FFFFFF"

class FilmSearchDBManager(CustomLogger):
    def __init__(self):
        super().__init__(name=__name__)
        self.handler_read = None
        self.handler_write = None

    def initialize_handlers(self):
        self.handler_read = self.get_query_handler("DBCONFIG_SAKILA")
        self.handler_write = self.get_query_handler("DBCONFIG_ICH_EDIT")
        if self.handler_read and self.handler_write:
            record = self.handler_read.get_records(query=CategoryQueries.GET_ALL_CATEGORYS)
            genres = [name_category["name_categorys"] for name_category in record]

            record = self.handler_read.get_records(query=FilmQueries.GET_ALL_YEAR)
            years = [year["release_year"] for year in record]
            return genres, years

    def get_query_handler(self, par_db_name: str) -> Optional[DBQueriesManager]:
        try:
            obj_dbconfig = DBConfigManager()
            dbconfig = obj_dbconfig.get_config(db_name=par_db_name)
            return DBQueriesManager(dbconfig)
        except Exception as e:
            self.get_logger().error(f"Ошибка [get_query_handler]: {e}")
            raise

class FilmSearchLogic(CustomLogger):
    def __init__(self, handler_read, handler_write):
        super().__init__(name=__name__)
        self.handler_read = handler_read
        self.handler_write = handler_write

    def search_films(self, selected_years, selected_genres, text_title_discr):
        query = FilmQueries.GET_FILM_BY_CRITERIA
        conditions = []
        formated_text_title_discr = []

        if selected_genres:
            conditions.append(FilmQueries.SET_PARAM_CATEGORYS)
        if selected_years:
            conditions.append(FilmQueries.SET_PARAM_YEARS)
        if text_title_discr:
            text_title_discr = re.sub(r'\s*,\s*', ',', re.sub(r'\s+', ' ', text_title_discr)).strip(',')

            formated_text_title_discr = [f'%{term}%' for term in text_title_discr.split(',')]
            temp = [FilmQueries.SET_PARAM_TEXT] * len(formated_text_title_discr)
            conditions.append(f"({' or '.join(temp)})")

        if conditions:
            combined_conditions = ' where ' + ' and '.join(conditions)
            query = query.replace('-- SET_PARAM_CONDITIONS', combined_conditions)

        if self.handler_read:
            query, params = self.handler_read.get_converting_SQLquery(query, selected_genres, selected_years, *formated_text_title_discr)
            records = self.handler_read.get_records(query, params)

            execute_params = [','.join(params), query % tuple(params)]
            self.execute_query(execute_params)

            result_search = self._format_search_results(records)
            search_criteria = self._format_search_criteria(text_title_discr, selected_genres, selected_years)
            final_memo = f"Критерии поиска:\n{search_criteria}\n\nНайдено: {len(records)}\n{result_search}"
            return final_memo

    def _format_search_results(self, rec):
        if rec:
            return "\n".join([
                f"{i.get('title')} ({i.get('release_year')})\nЖанр: {i.get('name_category')} ({i.get('length')} мин)\nОписание: {i.get('description')}\n{'-' * 50}"
                for i in rec])
        return ""

    def _format_search_criteria(self, text_title_discr, selected_genres, selected_years):
        return f"Ключевое слово: {text_title_discr}\nЖанр: {', '.join(selected_genres)}\nГод: {', '.join(selected_years)}"

    def execute_query(self, params) -> None:
        try:
            if self.handler_write:
                self.handler_write.execute_ins_upd_del(PopularCriteriaFilm.INSERT_CRITERIA, params)
        except Exception as e:
            self.get_logger().error(f"Ошибка при выполнении запроса: {e}")
            raise

    def get_last_search(self):
        query = PopularCriteriaFilm.GET_LAST_SEARCH
        try:
            records = self.handler_write.get_records(query)
            result_search = ""
            if records:
                result_search = "\n".join(
                    [f"Дата: {record.get('create_date')} - {record.get('category_by_words')}" for record in records])
            final_memo = f"Последние 20 поисков:\n\n{result_search}"
            return final_memo
        except Exception as e:
            self.get_logger().error(f"Ошибка при получении последних запросов: {e}")
            raise

class FilmSearchUI(CustomLogger):
    def __init__(self, par_root_tk):
        super().__init__(name=__name__)
        self.root_tk = par_root_tk
        self.root_tk.title("Поиск фильмов")
        self.root_tk.geometry("800x830")
        self.root_tk.resizable(False, False)
        self.root_tk.configure(bg=FRAME_BG)

        self.memo_field = None
        self.title_discr_entry = None
        self.genre_cb = None
        self.year_cb = None
        self.genres = []
        self.years = []

        self.db_manager = FilmSearchDBManager()
        self.genres, self.years = self.db_manager.initialize_handlers()
        self.handler_read = self.db_manager.handler_read
        self.handler_write = self.db_manager.handler_write

        self.logic = FilmSearchLogic(self.handler_read, self.handler_write)

        self.create_ui()

    def create_ui(self):
        search_frame = tk.Frame(self.root_tk, bg=FRAME_BG)
        search_frame.grid(row=0, column=0, padx=10, pady=5)

        self.memo_field = tk.Text(self.root_tk, wrap="word",
                                  state="disabled",
                                  font=("Courier New", 12),
                                  bg=CONTROL_BG,
                                  bd=0,
                                  highlightthickness=1,
                                  highlightbackground="#c0c0c0",
                                  highlightcolor="#c0c0c0",
                                  relief="flat",
                                  fg=CONTROL_FG)
        self.memo_field.grid(row=1, column=0, padx=10, pady=5)

        bottom_frame = tk.Frame(self.root_tk, bg=FRAME_BG)
        bottom_frame.grid(row=2, column=0, padx=10, pady=5, sticky="es")

        label_frame = tk.LabelFrame(search_frame, text="Введите критерий поиска", font=("Courier New", 12, "bold"),
                                    padx=10,
                                    pady=10, bg=FRAME_BG)
        label_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        title_discr_label = tk.Label(label_frame, text="Ключевое слово (через запятую):", font=("Courier New", 10),
                                     bg=FRAME_BG)
        title_discr_label.grid(row=0, column=0, sticky="w", padx=10, pady=1)
        self.title_discr_entry = tk.Text(label_frame,
                                         wrap="word",
                                         font=("Courier New", 12),
                                         bg="#f0f0f0",
                                         bd=0,
                                         highlightthickness=1,
                                         highlightbackground="#c0c0c0",
                                         highlightcolor="#c0c0c0",
                                         relief="flat",
                                         width=25,
                                         height=10)
        self.title_discr_entry.grid(row=1, column=0, padx=10, pady=1)

        genre_label = tk.Label(label_frame, text="Жанр:", font=("Courier New", 10), bg=FRAME_BG)
        genre_label.grid(row=0, column=1, sticky="w", padx=10, pady=1)
        self.genre_cb = MultiSelectCombobox(label_frame, self.genres)
        self.genre_cb.frame.grid(row=1, column=1, padx=10, pady=1, sticky="n")

        year_label = tk.Label(label_frame, text="Год:", font=("Courier New", 10), bg=FRAME_BG)
        year_label.grid(row=0, column=2, sticky="w", padx=10, pady=1)
        self.year_cb = MultiSelectCombobox(label_frame, self.years)
        self.year_cb.frame.grid(row=1, column=2, padx=10, pady=1, sticky="n")

        CustomButton(bottom_frame, "Поиск", self.search, 0, 1, "#4b7a4f", "#6c8e6b")
        CustomButton(bottom_frame, "Посл. запросы", self.last_search, 0, 2, "#4b7a4f", "#6c8e6b")
        CustomButton(bottom_frame, "В файл", self.save_file, 0, 3, "#4b7a4f", "#6c8e6b")
        CustomButton(bottom_frame, "Выход", self.exit_program, 0, 4, "#c0392b", "#e74c3c")

        db_name_label = tk.Label(bottom_frame, text="БД:", font=("Courier New", 10), bg=FRAME_BG)
        db_name_label.config(text=f"БД на чтение: {self.handler_read.get_bd_name()}\n"
                                  f"БД на запись: {self.handler_write.get_bd_name()}")
        db_name_label.grid(row=0, column=0, sticky="w", padx=10, pady=1)

        self.root_tk.grid_rowconfigure(0, weight=1)
        self.root_tk.grid_columnconfigure(0, weight=1)

    def set_data_in_memo(self, data):
        self.memo_field.config(state="normal")
        self.memo_field.delete(1.0, tk.END)
        self.memo_field.insert(tk.END, data)
        self.memo_field.config(state="disabled")

    def last_search(self):
        try:
            final_memo = self.logic.get_last_search()
            self.set_data_in_memo(final_memo)
        except Exception as e:
            self.get_logger().error(f"Ошибка при получении последних запросов: {e}")

    def exit_program(self):
        try:
            self.handler_read.close()
            self.handler_write.close()
            self.root_tk.quit()
        except Exception as e:
            self.get_logger().error(f"Ошибка при закрытии программы: {e}")

    def save_file(self):
        try:
            text_from_memo = self.memo_field.get("1.0", tk.END).strip()
            file_manager = FileManager(text_from_memo)
            file_manager.save_file()

            messagebox.showinfo("Сохранение в файл", "Данные успешно сохранены в файл!")
        except Exception as e:
            self.get_logger().error(f"Ошибка при сохранении в файл: {e}")

    def search(self):
        try:
            selected_years = [var.get() for var in self.year_cb.check_vars if var.get()]
            selected_genres = [var.get() for var in self.genre_cb.check_vars if var.get()]
            text_title_discr = self.title_discr_entry.get("1.0", tk.END).strip()

            final_memo = self.logic.search_films(selected_years, selected_genres, text_title_discr)
            self.set_data_in_memo(final_memo)
        except Exception as e:
            self.get_logger().error(f"Ошибка при поиске фильмов: {e}")

if __name__ == "__main__":
    root_tk = tk.Tk()
    ui = FilmSearchUI(root_tk)
    root_tk.mainloop()
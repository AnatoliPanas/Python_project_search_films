import tkinter as tk
from typing import Optional
from conrlols.CustomButton import CustomButton
from conrlols.MultiSelectCombobox import MultiSelectCombobox
from db.db_configs_manager import DBConfigManager
from db.db_queries_manager import DBQueriesManager
from db.sql_queries import CategoryQueries, FilmQueries, SearchCriteriaFilm
import re
from file_manager import FileManager


# Получаем объект работы с БД
def get_query_handler(par_db_name: str) -> Optional[DBQueriesManager]:
    try:
        obj_dbconfig = DBConfigManager()
        dbconfig = obj_dbconfig.get_config(db_name=par_db_name)
        return DBQueriesManager(dbconfig)
    except Exception as e:
        print(f"Ошибка [get_query_handler] : {e}")
        return None

# Вставка в БД критериев поиска
def execute_query(params) -> None:
    if handler_write:
        handler_write.execute_ins_upd_del(SearchCriteriaFilm.INSERT_CRITERIAFILM, params)

# Берем последние 20 запросов
def last_search():
    query = SearchCriteriaFilm.GET_LAST_SEARCH
    records = handler_write.get_records(query)
    if records:
        result_search = "\n".join([f"Дата: {record.get('cdate')} - {record.get('category_by_words')}" for record in records])

    final_memo = f"Последние 20 поисков:\n\n{result_search}"
    set_data_in_memo(final_memo)

# Выход из программы
def exit_program():
    handler_read.close()
    handler_write.close()
    root.quit()

# Запись в файл
def save_file():
    text_from_memo = memo_field.get("1.0", tk.END).strip()
    file_manager = FileManager(text_from_memo)
    file_manager.save_file()

# Функция поиска фильмов по критериям
def search():
    selected_years = [var.get() for var in year_cb.check_vars if var.get()]
    selected_genres = [var.get() for var in genre_cb.check_vars if var.get()]
    text_title_discr = title_discr_entry.get("1.0", tk.END).strip()

# --> Получаем и формируем нужный запрос
    query = FilmQueries.GET_FILM_BY_CATEGORYS
    if selected_years:
        query = query.replace('--where', 'where').replace('--SET_PARAM_YEARS', FilmQueries.SET_PARAM_YEARS)
    if selected_genres:
        query = query.replace('--where', 'where').replace('--SET_PARAM_CATEGORYS', FilmQueries.SET_PARAM_CATEGORYS)
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
# <--

    # handler = get_query_handler("DBCONFIG_SAKILA")
    if handler_read:
        query, params = handler_read.get_converting_SQLquery(query, selected_genres, selected_years, *text_title_discr)
        res = handler_read.get_records(query, params)

        execute_params = [','.join(params), query]
        execute_query(execute_params)

        result_search = ""
        if res:
            result_search = "\n".join([f"Название: {i.get('title')} ({i.get('length')} мин)\nЖанр: {i.get('name_category')} Год: {i.get('release_year')}\nОписание: {i.get('description')}\n{'-' * 50}" for i in res])

        search_criteria = f"Ключевое слово: {title_discr_entry.get('1.0', 'end-1c')}\nЖанр: {', '.join(selected_genres)}\nГод: {', '.join(selected_years)}"
        final_memo = f"Критерии поиска:\n{search_criteria}\n\nНайдено: {len(res)}\n{result_search}"
        set_data_in_memo(final_memo)

def set_data_in_memo(data):
    memo_field.config(state="normal")
    memo_field.delete(1.0, tk.END)
    memo_field.insert(tk.END, data)
    memo_field.config(state="disabled")

# Создание интерфейса
def create_ui():
    root = tk.Tk()
    root.title("Поиск фильмов")
    root.geometry("800x830")
    root.resizable(False, False)


    search_frame = tk.Frame(root)
    search_frame.grid(row=0, column=0, padx=10, pady=5)

    global memo_field
    memo_field = tk.Text(root, wrap="word", state="disabled", font=("Arial", 12))
    memo_field.grid(row=1, column=0, padx=10, pady=5)

    bottom_frame = tk.Frame(root)
    bottom_frame.grid(row=2, column=0, padx=10, pady=5, sticky="es")

    label_frame = tk.LabelFrame(search_frame, text="Введите критерий поиска", font=("Arial", 12, "bold"), padx=10, pady=10)
    label_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Поля для ввода
    title_discr_label = tk.Label(label_frame, text="Ключевое слово (через запятую):", font=("Arial", 10))
    title_discr_label.grid(row=0, column=0, sticky="w", padx=10, pady=1)
    global title_discr_entry
    title_discr_entry = tk.Text(label_frame, wrap="word", font=("Arial", 12), width=25, height=5)
    title_discr_entry.grid(row=1, column=0, padx=10, pady=1)

    genre_label = tk.Label(label_frame, text="Жанр (через запятую):", font=("Arial", 10))
    genre_label.grid(row=0, column=1, sticky="w", padx=10, pady=1)
    global genre_cb
    genre_cb = MultiSelectCombobox(label_frame, genres)
    genre_cb.frame.grid(row=1, column=1, padx=10, pady=1, sticky="n")

    year_label = tk.Label(label_frame, text="Год:", font=("Arial", 10))
    year_label.grid(row=0, column=2, sticky="w", padx=10, pady=1)
    global year_cb
    year_cb = MultiSelectCombobox(label_frame, years)
    year_cb.frame.grid(row=1, column=2, padx=10, pady=1, sticky="n")

    # Кнопки
    search_button = CustomButton(bottom_frame, "Поиск", search, 0, 1, "#3e8e41", "#4CAF50")
    report_button = CustomButton(bottom_frame, "Посл. запросы", last_search, 0, 2, "#3e8e41", "#4CAF50")
    file_button = CustomButton(bottom_frame, "В файл", save_file, 0, 3, "#3e8e41", "#4CAF50")
    exit_button = CustomButton(bottom_frame, "Выход", exit_program, 0, 4, "#D32F2F", "#f44336")

    db_name_label = tk.Label(bottom_frame, text="БД:", font=("Arial", 10))
    db_name_label.config(text=f"БД на чтение: {handler_read.get_bd_name()}\n"
                              f"БД на запись: {handler_write.get_bd_name()}")
    db_name_label.grid(row=0, column=0, sticky="w", padx=10, pady=1)

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    return root

if __name__ == "__main__":
    handler_read = get_query_handler("DBCONFIG_SAKILA")
    handler_write = get_query_handler("DBCONFIG_ICH_EDIT")
    if handler_read:
        record = handler_read.get_records(query=CategoryQueries.GET_ALL_CATEGORYS)
        genres = [name_category["name_categorys"] for name_category in record]

        record = handler_read.get_records(query=FilmQueries.GET_ALL_YEAR)
        years = [year["release_year"] for year in record]

    root = create_ui()
    root.mainloop()

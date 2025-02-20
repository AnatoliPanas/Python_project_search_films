import tkinter as tk

from conrlols.CustomButton import CustomButton
from conrlols.MultiSelectCombobox import MultiSelectCombobox
from db.db_configs_manager import DBConfigManager
from db.db_queries_manager import DBQueriesManager
from db.sql_queries import CategoryQueries, FilmQueries
import re

def get_query_handler(par_db_name):
    obj_dbconfig = DBConfigManager()
    dbconfig = obj_dbconfig.get_config(db_name=par_db_name)
    query_handler = DBQueriesManager(dbconfig)
    return query_handler

# Функция выхода из программы
def exit_program():
    handler.close()
    root.quit()

def search():
    selected_years = [var.get() for var in year_cb.check_vars if var.get() != ""]
    selected_genres = [var.get() for var in genre_cb.check_vars if var.get() != ""]
    text_title_discr = keyword_entry.get("1.0", tk.END).strip()


    query = FilmQueries.GET_FILM_BY_CATEGORYS

    if selected_years:
        query = query.replace('--where', 'where')
        query = query.replace('--SET_PARAM_YEARS', FilmQueries.SET_PARAM_YEARS)

    if selected_genres:
        query = query.replace('--where', 'where')
        query = query.replace('--SET_PARAM_CATEGORYS', FilmQueries.SET_PARAM_CATEGORYS)

    if text_title_discr:
        query = query.replace('--where', 'where')
        text_title_discr = re.sub(r'\s+', '', text_title_discr)
        text_title_discr = text_title_discr.strip(',')
        temp_query = ""
        for text in text_title_discr.split(','):
            temp_query += FilmQueries.SET_PARAM_TEXT + '\n'
        text_title_discr = {'s':text_title_discr.split(',')}
        query = query.replace('--SET_PARAM_TEXT', temp_query)


    query = re.sub(r'--.*\n', '', query)
    query = re.sub(r'\sAND\s*$', '', query, flags=re.I)

    query, params = handler.get_converting_SQLquery(query, selected_genres, selected_years, text_title_discr)
    res = handler.get_records(query, params)

    search_criteri1 = ""
    if res:
        for i in res:
            search_criteri1 += f"""\nНазвание: {i.get("title")} ({i.get("length")} мин)\nЖанр: {i.get("name_category")} Год: {i.get("release_year")}\nОписание: {i.get("description")}\n{'-'*50}"""


    search_criteria = f"Ключевое слово: {keyword_entry.get("1.0", "end-1c")}\nЖанр: {', '.join(selected_genres)}\nГод: {', '.join(selected_years)}"
    memo_field.config(state="normal")
    memo_field.delete(1.0, tk.END)
    memo_field.insert(tk.END, f"Критерии поиска:\n{search_criteria}\n\nНайдено: {len(res)}\n{search_criteri1}")
    memo_field.config(state="disabled")

handler = get_query_handler("DBCONFIG_SAKILA")

record = handler.get_records(query=CategoryQueries.GET_ALL_CATEGORYS)
genres = [name_category["name_categorys"] for name_category in record]

record = handler.get_records(query=FilmQueries.GET_ALL_YEAR)
years = [year["release_year"] for year in record]

root = tk.Tk()
root.title("Поиск фильмов")
root.geometry("800x830")

# Основной контейнер для формы поиска
search_frame = tk.Frame(root)
search_frame.grid(row=0, column=0, padx=10, pady=5)

# Центральное текстовое поле (Memo), с отключением редактирования
memo_field = tk.Text(root, wrap="word", state="disabled", font=("Arial", 12))
memo_field.grid(row=1, column=0, padx=10, pady=5)

# Основной контейнер для нижних кнопок
bottom_frame = tk.Frame(root)
bottom_frame.grid(row=2, column=0, padx=10, pady=5, sticky="es")

# Рамка с заголовком "Введите критерий поиска"
label_frame = tk.LabelFrame(search_frame,
                            text="Введите критерий поиска",
                            font=("Arial", 12, "bold"),
                            padx=10,
                            pady=10)
label_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

keyword_label = tk.Label(label_frame, text="Ключевое слово (через запятую):", font=("Arial", 10))
keyword_label.grid(row=0, column=0, sticky="w", padx=10, pady=1)
keyword_entry = tk.Text(label_frame, wrap="word", font=("Arial", 12), width=25, height=10)
keyword_entry.grid(row=1, column=0, padx=10, pady=1)

genre_label = tk.Label(label_frame, text="Жанр (через запятую):", font=("Arial", 10))
genre_label.grid(row=0, column=1, sticky="w", padx=10, pady=1)
genre_cb = MultiSelectCombobox(label_frame, genres)
genre_cb.frame.grid(row=1, column=1, padx=10, pady=1, sticky="n")

year_label = tk.Label(label_frame, text="Год:", font=("Arial", 10))
year_label.grid(row=0, column=2, sticky="w", padx=10, pady=1)
year_cb = MultiSelectCombobox(label_frame, years)
year_cb.frame.grid(row=1, column=2, padx=10, pady=1, sticky="n")

search_button = CustomButton(bottom_frame, "Поиск", search, 0, 1, "#3e8e41", "#4CAF50")
report_button = CustomButton(bottom_frame, "Поп. запросы", exit_program, 0, 2, "#3e8e41", "#4CAF50")
file_button = CustomButton(bottom_frame, "В файл", exit_program, 0, 3, "#3e8e41", "#4CAF50")
exit_button = CustomButton(bottom_frame, "Выход", exit_program, 0, 4, "#D32F2F", "#f44336")

db_name_label = tk.Label(bottom_frame, text="БД:", font=("Arial", 10))
db_name_label.config(text="БД: " + handler.get_bd_name())
db_name_label.grid(row=0, column=0, sticky="w", padx=10, pady=1)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

if __name__ == "__main__":
    root.mainloop()
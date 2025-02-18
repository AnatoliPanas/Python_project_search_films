import tkinter as tk
from conrlols.MultiSelectCombobox import MultiSelectCombobox

genres = ['Action','Animation','Children','Classics','Comedy','Documentary','Drama','Family','Foreign','Games','Horror','Music','New','Sci-Fi','Sports','Travel']
years = [str(year) for year in range(1960, 2025)]
# Функция для изменения цвета кнопки при наведении
def on_enter(event, background):
    event.widget.config(bg=background)  # Цвет при наведении

def on_leave(event, background):
    event.widget.config(bg=background) # Цвет по умолчанию

# Функция выхода из программы
def exit_program():
    root.quit()

def search():
    # Обработчик для поиска
    selected_years = [var.get() for var in year_cb.check_vars if var.get() != ""]
    selected_genres = [var.get() for var in genre_cb.check_vars if var.get() != ""]
    search_criteria = f"Ключевое слово: {keyword_entry.get("1.0", "end-1c")}\nЖанр: {', '.join(selected_genres)}\nГод: {', '.join(selected_years)}"
    memo_field.config(state="normal")
    memo_field.delete(1.0, tk.END)
    memo_field.insert(tk.END, f"Результаты поиска:\n{search_criteria}")
    memo_field.config(state="disabled")

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

search_button = tk.Button(bottom_frame,
                          text="Поиск",
                          command=search,
                          font=("Arial", 12, "bold"),
                          fg="white",
                          bg="#3e8e41",
                          height=2,
                          width=10)
search_button.grid(row=0, column=0, padx=10, pady=10)
search_button.bind("<Enter>", lambda event: on_enter(event, "#4CAF50"))
search_button.bind("<Leave>", lambda event: on_leave(event, "#3e8e41"))

exit_button = tk.Button(bottom_frame,
                        text="Выход",
                        command=exit_program,
                        font=("Arial", 12, "bold"),
                        fg="white",
                        bg="#D32F2F",
                        height=2,
                        width=10)
exit_button.grid(row=0, column=1, padx=10, pady=10)
exit_button.bind("<Enter>", lambda event: on_enter(event, "#f44336"))
exit_button.bind("<Leave>", lambda event: on_leave(event, "#D32F2F"))



root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()

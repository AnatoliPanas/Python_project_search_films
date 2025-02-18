import tkinter as tk
from tkinter import messagebox


class MultiSelectCombobox:
    def __init__(self, frame, options):

        # Создаем основной фрейм
        self.frame = tk.Frame(frame)
        # self.frame.grid(row=1, column=1, padx=1, pady=1)
        # Список элементов для выбора
        self.options = options
        # Список переменных для чекбоксов
        self.check_vars = []

        # Создаем Canvas для прокрутки
        self.canvas = tk.Canvas(self.frame, width=150, height=180)
        self.canvas.grid(row=0, column=1)

        # Создаем Scrollbar для Canvas
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview, width=10)
        self.scrollbar.grid(row=0, column=2,sticky="ns")

        # Связываем Scrollbar с Canvas
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # Создаем фрейм, который будет размещен внутри Canvas
        self.checkbutton_frame = tk.Frame(self.canvas)

        # Размещение фрейма на Canvas
        self.canvas.create_window((0, 0), window=self.checkbutton_frame)

        # Добавляем функциональность прокрутки колесиком мыши
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)

        # Создаем чекбоксы
        self.create_checkbuttons()

    def create_checkbuttons(self):
        for i, option in enumerate(self.options):
            var = tk.StringVar()
            self.check_vars.append(var)
            checkbutton = tk.Checkbutton(self.checkbutton_frame, text=option, variable=var, onvalue=option, offvalue="")
            checkbutton.grid(row=i, column=0, sticky="w")

        # Обновляем область канваса, чтобы прокрутка работала
        self.checkbutton_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def on_mouse_wheel(self, event):
        delta = event.delta
        if delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif delta < 0:
            self.canvas.yview_scroll(1, "units")



# root = tk.Tk()
# root.title("Мульти-выбор в выпадающем меню")
# root.geometry("300x300")
#

# options = ["Опция 1", "Опция 2", "Опция 3", "Опция 4", "Опция 5", "Опция 6", "Опция 7", "Опция 8",
#            "Опция 9", "Опция 10", "Опция 11", "Опция 12", "Опция 13", "Опция 14", "Опция 15"]
#

# app = MultiSelectMenu(root, options)
# app.create_checkbuttons()
# root.mainloop()

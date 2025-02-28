import tkinter as tk


class MultiSelectCombobox:
    def __init__(self, frame, options):

        self.frame = tk.Frame(frame, bg="#f0f0f0", bd=1, relief="flat")

        self.options = options
        self.check_vars = []

        # Создаем Canvas для прокрутки
        self.canvas = tk.Canvas(self.frame,
                                width=180,
                                height=200,
                                bg="#f0f0f0",
                                bd=0,
                                highlightthickness=0)
        self.canvas.grid(row=0, column=1)

        # Создаем Scrollbar для Canvas
        self.scrollbar = tk.Scrollbar(self.frame,
                                      orient="vertical",
                                      command=self.canvas.yview,
                                      width=12,
                                      bg="#f0f0f0")
        self.scrollbar.grid(row=0, column=2, sticky="ns")

        # Связываем Scrollbar с Canvas
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.checkbutton_frame = tk.Frame(self.canvas, bg="#f0f0f0")
        self.canvas.create_window((0, 0), window=self.checkbutton_frame)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)

        self.create_checkbuttons()

        self.canvas.yview_moveto(0)

    def create_checkbuttons(self):
        for i, option in enumerate(self.options):
            var = tk.StringVar()
            self.check_vars.append(var)
            checkbutton = tk.Checkbutton(self.checkbutton_frame,
                                         text=option,
                                         variable=var,
                                         onvalue=option,
                                         offvalue="",
                                         font=("Courier New", 10),
                                         fg="#333333",
                                         bg="#f0f0f0",
                                         selectcolor="white",
                                         activebackground="#fdfdfd",
                                         activeforeground="#333333")
            checkbutton.grid(row=i, column=0, sticky="w", padx=5, pady=2)

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
# root.geometry("300x350")
# root.configure(bg="#fdfdfd")
#
# options = ["Опция 1", "Опция 2", "Опция 3", "Опция 4", "Опция 5", "Опция 6", "Опция 7", "Опция 8",
#            "Опция 9", "Опция 10", "Опция 11", "Опция 12", "Опция 13", "Опция 14", "Опция 15"]
#
# app = MultiSelectCombobox(root, options)
# app.frame.pack(padx=20, pady=20)
# root.mainloop()

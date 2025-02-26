import tkinter as tk

class CustomButton:
    def __init__(self, parent, text, command, row, column, bg, hover_bg, font=("Helvetica", 10, "bold"), fg="white",
                 height=2, width=9):
        self.button = tk.Button(parent,
                                text=text,
                                command=command,
                                font=font,
                                fg=fg,
                                bg=bg,
                                height=height,
                                width=width,
                                relief="solid",
                                bd=1,
                                activebackground=hover_bg,
                                activeforeground="white",
                                padx=10, pady=5)
        self.button.grid(row=row, column=column, padx=2, pady=10)

        self.button.bind("<Enter>", lambda event: self.on_enter(event, hover_bg))
        self.button.bind("<Leave>", lambda event: self.on_leave(event, bg))

    def on_enter(self, event, background):
        event.widget.config(bg=background)

    def on_leave(self, event, background):
        event.widget.config(bg=background)


# def search():
#     print("Поиск")
#
# def exit_program():
#     print("Выход")
#
# root = tk.Tk()
#
# bottom_frame = tk.Frame(root)
# bottom_frame.pack(pady=20)
#
# search_button = CustomButton(bottom_frame, "Поиск", search, 0, 1, "#4b7a4f", "#6c8e6b")
# report_button = CustomButton(bottom_frame, "Поп. запросы", exit_program, 0, 2, "#4b7a4f", "#6c8e6b")
# file_button = CustomButton(bottom_frame, "В файл", exit_program, 0, 3, "#4b7a4f", "#6c8e6b")
# exit_button = CustomButton(bottom_frame, "Выход", exit_program, 0, 4, "#c0392b", "#e74c3c")
#
# root.mainloop()

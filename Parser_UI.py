import tkinter as tk
from tkinter import scrolledtext, messagebox
import sys
from Parser_admin import *
import threading


progress = "Progress"

def redirect_stdout_to_text_widget():

    class WriteToTextWidget:
        def write(self, s):

            if progress in s:
                update_status(s)
            add_log(s)

    sys.stdout = WriteToTextWidget()

def on_button_click(category):
    result = messagebox.askquestion("Confirmation", "Start parsing " + category + " category?")
    if result == 'yes':
        threading.Thread(target=lets_go_background, args=(category,), daemon=True).start()


def lets_go_background(category):
    lets_go(category)
def on_stop_button_click():
    result = messagebox.askquestion("Confirmation", "Do you really want to stop parsing?")
    if result == 'yes':
        add_log("Parsing stopped.")
    else:
        add_log("Parsing continued.")

def add_log(message):
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, message)
    log_text.see(tk.END)
    log_text.config(state=tk.DISABLED)

def update_status(status):
    status_label.config(text=status)

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_position = (screen_width - width) // 2
    y_position = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x_position}+{y_position}")

root = tk.Tk()
root.title("Readbookfreeonline PARSER")

categories = [
    'romance', 'adventure', 'thriller', 'fantasy', 'young-adult', 'mystery', 'historical', 'horror', 'science-fiction', 'humorous', 'christian', 'western'
]

button_width = 12
button_height = 1

button_frame = tk.Frame(root)
button_frame.pack(side=tk.TOP, pady=10)

log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10)
log_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
log_text.config(state=tk.DISABLED)  # Начальное состояние: только для чтения


for i, cat in enumerate(categories):
    row = i // 4
    col = i % 4
    button = tk.Button(button_frame, text=cat, width=button_width, height=button_height, command=lambda c=cat: on_button_click(category=c))
    button.grid(row=row, column=col, padx=0, pady=0)

stop_button = tk.Button(root, text="STOP", width=button_width, height=button_height, command=on_stop_button_click)
stop_button.pack(side=tk.RIGHT, padx=10, pady=10)

status_label = tk.Label(root, text=progress, fg="white")
status_label.pack(side=tk.LEFT, padx=10, pady=5)

root.resizable(width=False, height=False)

center_window(root, 800, 600)

redirect_stdout_to_text_widget()

root.mainloop()


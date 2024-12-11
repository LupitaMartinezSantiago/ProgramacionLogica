
import tkinter as tk

def centrar_frame_principal(window):
   
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    position_top = int(screen_height / 2 - height / 2)
    position_right = int(screen_width / 2 - width / 2)
    window.geometry(f'{width}x{height}+{position_right}+{position_top}')

def crear_label(text, window):
    return tk.Label(window, text=text, font=("Arial", 12))

def create_entry(window):
    return tk.Entry(window, font=("Arial", 12))

def create_button(window, text, command):
    return tk.Button(window, text=text, command=command, font=("Arial", 12))

import tkinter as tk
def generate_label(place, text, row, column):
    label = tk.Label(place, text=text)
    label.grid(row=row, column=column, padx=10, pady=10)
    return label
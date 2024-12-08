import tkinter as tk

def generate_label(place, text, row, column, isBold: bool = False) -> tk.Label:
    if isBold:
        label = tk.Label(place, text=text, font=("Arial", 12, "bold"))
    else:
        label = tk.Label(place, text=text)
    
    label.grid(row=row, column=column, padx=2, pady=2)
    return label    
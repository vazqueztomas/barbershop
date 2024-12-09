import csv
import tkinter as tk

def update_info_in_display(label_income: tk.Label, label_haircuts: tk.Label) -> None:
    try:
        with open("register_haircuts.csv", "r") as archive:
            reader = csv.reader(archive)
            
            income = 0
            total_haircuts = 0
            for fila in reader:
                income += float(fila[2])
                total_haircuts += 1
            
            label_income.config(text=f"Total ganado: ${income}")
            label_haircuts.config(text=f"Cortes realizados: {total_haircuts}")
    except FileNotFoundError:
        label_income.config(text="Total ganado: $0")
        
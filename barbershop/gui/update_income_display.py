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
            
            label_income.config(text=f"Total Income: ${income}")
            label_haircuts.config(text=f"Total Haircuts: {total_haircuts}")
    except FileNotFoundError:
        label_income.config(text="Total Income: $0")
        
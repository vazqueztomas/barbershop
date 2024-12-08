import csv
import tkinter as tk
from tkinter import messagebox, ttk


def read_register():
    try:
        with open("register_haircuts.csv", "r") as archive:
            reader = csv.reader(archive)
            data = [row for row in reader]
            return data
    except FileNotFoundError:
        messagebox.showerror("Error", "There are no haircut records yet.")
        return []
    
def show_table(data):
    root = tk.Tk()
    root.title("Registro de Cortes de Pelo")

    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    table = ttk.Treeview(frame, columns=("Cliente", "Corte", "Precio", "Fecha"), show="headings")
    table.heading("Cliente", text="Cliente")
    table.heading("Corte", text="Corte")
    table.heading("Precio", text="Precio")
    table.heading("Fecha", text="Fecha")

    for row in data:
        table.insert("", tk.END, values=row)

    table.pack(fill=tk.BOTH, expand=True)
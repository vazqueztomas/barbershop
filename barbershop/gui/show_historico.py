import tkinter as tk
from tkinter import ttk

from barbershop.gui.constants import FILE_PATH


def show_historico(tree: ttk.Treeview):
    window = tk.Tk()
    window.title("Historico de cortes")

    def filter_by_date_part(date_part_index: int, value: str):
        tree.delete(*tree.get_children())
        with open(FILE_PATH) as archive:
            for row in archive:
                row = row.strip().split(",")
                if row[3].split("-")[date_part_index] == value:
                    tree.insert("", tk.END, values=row)

    # Filter by month
    def filter_by_month():
        month = entry_month.get()
        filter_by_date_part(1, month)

    def filter_by_day():
        day = entry_day.get()
        filter_by_date_part(2, day)

    def filter_by_type():
        selected_option = combobox_type.get()
        tree.delete(*tree.get_children())
        with open(FILE_PATH) as archive:
            for row in archive:
                row = row.strip().split(",")
                if row[4] == selected_option:
                    tree.insert("", tk.END, values=row)

    entry_month = ttk.Entry(window)
    entry_month.grid(row=1, column=0, padx=10, pady=10)
    button_filter_by_month = ttk.Button(
        window, text="Filtrar por mes", command=filter_by_month
    )
    button_filter_by_month.grid(row=3, column=0)

    entry_day = ttk.Entry(window)
    entry_day.grid(row=1, column=2)
    button_filter = ttk.Button(window, text="Filtrar por dia", command=filter_by_day)
    button_filter.grid(row=3, column=2)

    combobox_type = ttk.Combobox(window, values=["Pelo", "Pelo y Barba", "Barba"])
    combobox_type.grid(row=1, column=1)
    button_filter_by_type = ttk.Button(
        window, text="Filtrar por tipo", command=filter_by_type
    )
    button_filter_by_type.grid(row=3, column=1)

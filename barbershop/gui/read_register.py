import csv
from tkinter import messagebox, ttk

from barbershop.gui.update_information_in_display import update_info_in_display

import customtkinter as ctk  # type: ignore


def read_register(file_path: str) -> list[list[str]]:
    try:
        with open(file_path, "r") as archive:
            reader = csv.reader(archive)
            data = [row for row in reader]
            return data
    except FileNotFoundError:
        messagebox.showerror("Error", "There are no haircut records yet.")  # type: ignore
        return []


def remove_cuts_from_table(
    table: ttk.Treeview, label_income: ctk.CTkLabel, label_total_haircuts: ctk.CTkLabel
):
    selected_item = table.selection()
    if not selected_item:
        messagebox.showwarning(  # type: ignore
            "Selección inválida", "Por favor, seleccione un corte para eliminar."
        )
        return

    selected_row = table.item(selected_item[0])["values"]

    with open("register_haircuts.csv", "r") as archive:
        rows = list(csv.reader(archive))

    with open("register_haircuts.csv", "w", newline="") as archive:
        writer = csv.writer(archive)
        for row in rows:
            if row != selected_row:
                writer.writerow(row)

    table.delete(selected_item[0])

    for i, item in enumerate(table.get_children(), start=1):
        table.item(item, values=(i, *table.item(item)["values"][1:]))

    update_info_in_display(
        label_income=label_income, label_haircuts=label_total_haircuts
    )

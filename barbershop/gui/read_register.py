import csv
from tkinter import messagebox, ttk

from barbershop.gui.update_information_in_display import update_info_in_display
from barbershop.gui.constants import FILE_PATH
import requests

from barbershop.models.haircut import Haircut


def read_register() -> list[Haircut] | None:
    try:
        get_haircuts = requests.get("http://localhost:8000/haircuts")
        return get_haircuts.json()
    except FileNotFoundError:
        messagebox.showerror("Error", "There are no haircut records yet.")  # type: ignore
        return None


def remove_cuts_from_table(
    table: ttk.Treeview, label_income: ttk.Label, label_total_haircuts: ttk.Label
):
    selected_item = table.selection()
    if not selected_item:
        messagebox.showwarning(  # type: ignore
            "Selección inválida", "Por favor, seleccione un corte para eliminar."
        )
        return

    selected_row = table.item(selected_item[0])["values"]

    try:
        requests.delete(f"http://localhost:8000/haircuts/{selected_row[0]}")
    except requests.exceptions.RequestException:
        messagebox.showerror("Error", "No se pudo eliminar el corte.")

    for i, item in enumerate(table.get_children(), start=1):
        table.item(item, values=(i, *table.item(item)["values"][1:]))
        
    update_info_in_display(
        label_income=label_income, label_haircuts=label_total_haircuts
    )

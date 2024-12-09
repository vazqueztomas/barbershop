import csv
import tkinter as tk
from tkinter import messagebox, ttk

from barbershop.gui.update_income_display import update_info_in_display


def read_register() -> list[list[str]]:
    try:
        with open("register_haircuts.csv", "r") as archive:
            reader = csv.reader(archive)
            data = [row for row in reader]
            return data
    except FileNotFoundError:
        messagebox.showerror("Error", "There are no haircut records yet.")  # type: ignore
        return []


def _delete_selected_cut(
    table: ttk.Treeview, label_income: tk.Label, label_total_haircuts: tk.Label
) -> None:
    selected_item = table.selection()
    if not selected_item:
        messagebox.showwarning(  # type: ignore
            "Selección inválida", "Por favor, seleccione un corte para eliminar."
        )  # type: ignore
        return

    # Obtener el índice de la fila seleccionada
    selected_row = table.item(selected_item[0])["values"]
    row_index = (
        int(selected_row[0]) - 1
    )  # La fila en la tabla corresponde a la posición en la lista

    # Eliminar la fila del archivo CSV
    with open("register_haircuts.csv", "r") as archive:
        rows = list(csv.reader(archive))

    with open("register_haircuts.csv", "w", newline="") as archive:
        writer = csv.writer(archive)
        for i, row in enumerate(rows):
            if i != row_index:
                writer.writerow(row)

    table.delete(selected_item[0])

    for i, item in enumerate(table.get_children(), start=1):
        table.item(item, values=(i, *table.item(item)["values"][1:]))

    update_info_in_display(
        label_income=label_income, label_haircuts=label_total_haircuts
    )


def show_table(
    data: list[list[str]], label_income: tk.Label, label_total_haircuts: tk.Label
) -> None:
    root = tk.Tk()
    root.title("Registro de Cortes de Pelo")

    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    table = ttk.Treeview(
        frame,
        columns=("Numero", "Cliente", "Corte", "Precio", "Fecha"),
        show="headings",
    )
    table.heading("Numero", text="Numero")
    table.heading("Cliente", text="Cliente")
    table.heading("Corte", text="Corte")
    table.heading("Precio", text="Precio")
    table.heading("Fecha", text="Fecha")

    for i, row in enumerate(data, start=1):
        table.insert("", tk.END, values=(i, *row))

    table.pack(fill=tk.BOTH, expand=True)

    # Botón para eliminar el corte seleccionado
    button_delete = ttk.Button(
        frame, text="Eliminar Corte", command=lambda: _delete_selected_cut(table, label_income, label_total_haircuts)
    )
    button_delete.pack(pady=10)

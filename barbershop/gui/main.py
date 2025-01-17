import tkinter as tk
from tkinter import messagebox, ttk

import requests
from tkcalendar import Calendar  # type: ignore

from barbershop.gui.constants import BASE_URL
from barbershop.gui.haircut_registration import register_new_haircut
from barbershop.gui.show_historico import show_historico
from barbershop.gui.update_information_in_display import (
    get_haircuts_list,
    update_info_in_display,
)
from barbershop.gui.utils.generate_label import generate_label
from customtkinter import CTkButton

columns = ("id", "Cliente", "Corte", "Precio", "Fecha", "Tipo")


root = tk.Tk()
root.title("Barbershop")
tree = ttk.Treeview(columns=columns, show="headings")

for column in columns:
    tree.heading(column, text=column)

tabControl = ttk.Notebook(root)
tabControl.pack(fill="both", expand=True, padx=10, pady=10)

tab_register_haircut = ttk.Frame(tabControl)
tab_statistics = ttk.Frame(tabControl)
tabControl.add(tab_register_haircut, text="Registro")
tabControl.add(tab_statistics, text="Graficos")

label_cliente = generate_label(tab_register_haircut, text="Cliente:", isBold=False)
label_cliente.pack(padx=10, pady=5, anchor="w")
entry_cliente = ttk.Entry(tab_register_haircut)
entry_cliente.pack(padx=10, pady=5, fill="x")


label_corte = generate_label(tab_register_haircut, text="Tipo de Corte:", isBold=False)
label_corte.pack(padx=10, pady=5, anchor="w")
entry_corte = ttk.Entry(tab_register_haircut)
entry_corte.pack(padx=10, pady=5, fill="x")

label_precio = generate_label(tab_register_haircut, text="Precio:", isBold=False)
label_precio.pack(padx=10, pady=5, anchor="w")
entry_precio = ttk.Entry(tab_register_haircut)
entry_precio.pack(padx=10, pady=5, fill="x")

label_fecha = generate_label(tab_register_haircut, text="Fecha:", isBold=False)
label_fecha.pack(padx=10, pady=5, anchor="w")
entry_fecha = Calendar(
    tab_register_haircut, selectmode="day", date_pattern="mm/dd/yyyy"
)
entry_fecha.pack(padx=10, pady=5, fill="x")

frame_radio_buttons = ttk.Frame(tab_register_haircut)
frame_radio_buttons.pack(anchor="w")

selected_option = tk.IntVar()
rb_pelo = ttk.Radiobutton(
    frame_radio_buttons, text="Pelo", variable=selected_option, value=1
)
rb_pelo.pack(padx=10, pady=5, anchor="w", side="left")

rb_pelo_y_barba = ttk.Radiobutton(
    frame_radio_buttons, text="Pelo y Barba", variable=selected_option, value=2
)
rb_pelo_y_barba.pack(padx=10, pady=5, anchor="w", side="left")

rb_barba = ttk.Radiobutton(
    frame_radio_buttons, text="Barba", variable=selected_option, value=3
)
rb_barba.pack(padx=10, pady=5, anchor="w", side="left")
# Frame to hold the buttons side by side
button_frame = ttk.Frame(tab_register_haircut)
button_frame.pack(fill="x")

button_registrar = CTkButton(
    button_frame,
    text="Registrar nuevo corte",
    command=lambda: [
        register_new_haircut(
            label_income,
            label_total_haircuts,
            entry_cliente,
            entry_corte,
            entry_precio,
            calendar=entry_fecha,
            checkbox_pelo=rb_pelo,
            checkbox_pelo_y_barba=rb_pelo_y_barba,
            checkbox_barba=rb_barba,
        ),
        update_treeview(),
    ],
)


def update_treeview():
    tree.delete(*tree.get_children())
    try:
        haircuts_list = get_haircuts_list()
        for haircut in haircuts_list:
            tree.insert(
                "",
                tk.END,
                values=(
                    haircut["id"],
                    haircut["client"],
                    haircut["haircut"],
                    haircut["prize"],
                    haircut["date"],
                    haircut["selected_option"],
                ),
            )
    except requests.exceptions.RequestException:
        messagebox.showerror("Error", "No se pudo obtener la lista de cortes.")  # type: ignore
        tree.insert("", tk.END, values=("Error", "Error", "Error", "Error", "Error"))


button_registrar.pack(pady=20, padx=10, fill="x", side="left")


frame_bold_labels = ttk.Frame(tab_register_haircut)
frame_bold_labels.pack(anchor="w")

label_income = generate_label(frame_bold_labels, text="Total ganado: $0", isBold=True)
label_income.pack(padx=10, pady=5, anchor="w", side="left")
label_total_haircuts = generate_label(
    frame_bold_labels, text="Cortes realizados: 0", isBold=True
)
label_total_haircuts.pack(padx=10, pady=5, anchor="w", side="right")


def remove_haircut_from_database() -> None:
    # get haircut id from the selected row
    haircut_id_from_row = tree.item(tree.selection()[0])["values"]
    try:
        requests.delete(f"{BASE_URL}/haircuts/{haircut_id_from_row[0]}")
    except requests.exceptions.RequestException:
        messagebox.showerror("Error", "No se pudo eliminar el corte.")  # type: ignore
        return

    update_info_in_display(
        label_income=label_income, label_haircuts=label_total_haircuts
    )


button_delete = ttk.Button(
    button_frame,
    text="Eliminar Corte",
    command=lambda: [remove_haircut_from_database(), update_treeview()],
)
button_delete.pack(padx=10, pady=10, fill="x", side="right")


button_mostrar_historico = ttk.Button(
    tab_register_haircut,
    text="Historico",
    command=lambda: show_historico(tree),
)
button_mostrar_historico.pack(padx=10, pady=10, fill="x")


tree.pack(padx=10, pady=10, fill="both", expand=True)


def populate_haircuts_tree(tree):
    try:
        haircuts_list = get_haircuts_list()
        for haircut in haircuts_list:
            tree.insert(
                "",
                tk.END,
                values=(
                    haircut["id"],
                    haircut["client"],
                    haircut["haircut"],
                    haircut["prize"],
                    haircut["date"],
                    haircut["selected_option"],
                ),
            )
    except requests.exceptions.RequestException:
        messagebox.showerror("Error", "No se pudo obtener la lista de cortes.")  # type: ignore
        tree.insert("", tk.END, values=("Error", "Error", "Error", "Error", "Error"))


populate_haircuts_tree(tree)


update_info_in_display(label_income=label_income, label_haircuts=label_total_haircuts)

root.mainloop()  # type: ignore

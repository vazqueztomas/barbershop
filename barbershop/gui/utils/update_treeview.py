import tkinter as tk
from tkinter import messagebox

import requests

from barbershop.gui.update_information_in_display import get_haircuts_list


def update_treeview(tree) -> None:
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

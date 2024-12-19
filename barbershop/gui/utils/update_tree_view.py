import tkinter as tk
from tkinter import ttk
from barbershop.gui.constants import FILE_PATH


def update_tree_view(tree: ttk.Treeview) -> None:
    for item in tree.get_children():
        tree.delete(item)

    with open(FILE_PATH) as archive:
        for row in archive:
            row = row.strip().split(",")
            tree.insert("", tk.END, values=row)

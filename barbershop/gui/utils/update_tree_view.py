import tkinter as tk
from tkinter import ttk


def update_tree_view(tree: ttk.Treeview) -> None:
    with open("register_haircuts.csv") as archive:
        for row in archive:
            row = row.strip().split(",")
            tree.insert("", tk.END, values=row)

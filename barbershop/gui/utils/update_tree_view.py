from tkinter import ttk
import tkinter as tk


def update_tree_view(tree: ttk.Treeview) -> None:
    with open("register_haircuts.csv", "r") as archive:
        for row in archive:
            row = row.strip().split(",")
            tree.insert("", tk.END, values=row)

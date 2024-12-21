import tkinter as tk
from tkinter import ttk


def generate_label(root: tk.Tk | ttk.Frame, text: str, isBold: bool) -> ttk.Label:
    if not isBold:
        label = ttk.Label(root, text=text)

    label = ttk.Label(root, text=text, font=("Arial", 16, "bold"))

    label.pack(padx=10, pady=10)  # type: ignore
    return label

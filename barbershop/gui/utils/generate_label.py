import tkinter as tk
import customtkinter as ctk #type: ignore

def generate_label(
    place: tk.Misc, text: str, row: int, column: int, isBold: bool = False
) -> ctk.CTkLabel:
    if isBold:
        label = ctk.CTkLabel(place, text=text, font=("Arial", 16, "bold"))
    else:
        label = ctk.CTkLabel(place, text=text)

    label.grid(row=row, column=column, padx=10, pady=10) # type: ignore
    return label

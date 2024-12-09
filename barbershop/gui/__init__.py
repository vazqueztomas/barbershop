
import tkinter as tk
from barbershop.gui.show_register import show_register


def refresh_haircuts_list(text_registros: tk.Text) -> None:
    show_register(text_registros)
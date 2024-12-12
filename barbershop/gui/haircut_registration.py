import csv
from tkinter import messagebox
import tkinter as tk
from datetime import datetime
from tkcalendar import Calendar  # type: ignore
from barbershop.gui import refresh_haircuts_list
from barbershop.gui.update_income_display import update_info_in_display

import customtkinter as ctk #type: ignore


def get_selected_option(
    checkbox_pelo: ctk.CTkRadioButton,
    checkbox_pelo_y_barba: ctk.CTkRadioButton,
    checkbox_barba: ctk.CTkRadioButton,
):
    if checkbox_pelo.instate(["selected"]):  # type: ignore
        return "Pelo"
    elif checkbox_pelo_y_barba.instate(["selected"]):  # type: ignore
        return "Pelo y Barba"
    elif checkbox_barba.instate(["selected"]):  # type:ignore
        return "Barba"
    return "No aclarado"


def register_new_haircut(
    label_income: ctk.CTkLabel,
    label_total_haircuts: ctk.CTkLabel,
    entry_cliente: ctk.CTkEntry,
    entry_corte: ctk.CTkEntry,
    entry_precio: ctk.CTkEntry,
    calendar: Calendar,
    text_registros: tk.Text,
    checkbox_pelo: ctk.CTkRadioButton,
    checkbox_pelo_y_barba: ctk.CTkRadioButton,
    checkbox_barba: ctk.CTkRadioButton,
):
    client = entry_cliente.get()
    haircut = entry_corte.get()
    selected_option = get_selected_option(
        checkbox_pelo, checkbox_pelo_y_barba, checkbox_barba
    )
    try:
        prize = float(entry_precio.get())
    except ValueError:
        messagebox.showerror("Error", "El precio debe ser un numero")  # type: ignore
        return

    selected_date = calendar.get_date()

    date = datetime.strptime(selected_date, "%m/%d/%Y").strftime("%Y-%m-%d")

    register: list[str | float] = [client, haircut, prize, date, selected_option]

    with open("register_haircuts.csv", "a", newline="") as archive:
        writer = csv.writer(archive)
        writer.writerow(register)
        print(register)

    entry_cliente.delete(0, tk.END) #type: ignore
    entry_corte.delete(0, tk.END) #type: ignore
    entry_precio.delete(0, tk.END) #type: ignore

    update_info_in_display(label_income, label_total_haircuts)
    refresh_haircuts_list(text_registros=text_registros)
    messagebox.showinfo(  # type: ignore
        "Corte registrado", f"Corte registrado - Cliente: {client}"
    )

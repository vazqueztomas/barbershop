import csv
import tkinter as tk
from datetime import datetime
from pydantic import ValidationError
from tkcalendar import Calendar  # type: ignore

from barbershop.gui.update_information_in_display import update_info_in_display
from barbershop.models import Haircut

import customtkinter as ctk  # type: ignore


def get_selected_option(
    checkbox_pelo: ttk.Radiobutton,
    checkbox_pelo_y_barba: ttk.Radiobutton,
    checkbox_barba: ttk.Radiobutton,
):
    if checkbox_pelo.instate(["selected"]):  # type: ignore
        return "Pelo"
    if checkbox_pelo_y_barba.instate(["selected"]):  # type: ignore
        return "Pelo y Barba"
    if checkbox_barba.instate(["selected"]):  # type:ignore
        return "Barba"
    return "No aclarado"


def register_new_haircut(
    label_income: ctk.CTkLabel,
    label_total_haircuts: ctk.CTkLabel,
    entry_cliente: ctk.CTkEntry,
    entry_corte: ctk.CTkEntry,
    entry_precio: ctk.CTkEntry,
    calendar: Calendar,
    checkbox_pelo: ttk.Radiobutton,
    checkbox_pelo_y_barba: ttk.Radiobutton,
    checkbox_barba: ttk.Radiobutton,
):
    client = entry_cliente.get()
    haircut = entry_corte.get()
    selected_option = get_selected_option(
        checkbox_pelo, checkbox_pelo_y_barba, checkbox_barba
    )
    prize = float(entry_precio.get())

    selected_date = calendar.get_date()

    date = datetime.strptime(selected_date, "%m/%d/%Y").strftime("%Y-%m-%d")

    try:
        haircut_data = Haircut(
            client=client,
            haircut=haircut,
            prize=prize,
            date=date,
            selected_option=selected_option,
        )
    except ValidationError as e:
        messagebox.showerror("Error", str(e))
        print(e)
        return

    with open("register_haircuts.csv", "a", newline="") as archive:
        writer = csv.writer(archive)

        writer.writerow(haircut_data.model_dump().values())
        print(haircut_data.model_dump(exclude={"id"}).values())

    entry_cliente.delete(0, tk.END)  # type: ignore
    entry_corte.delete(0, tk.END)  # type: ignore
    entry_precio.delete(0, tk.END)  # type: ignore

    update_info_in_display(label_income, label_total_haircuts)
    messagebox.showinfo(  # type: ignore
        "Corte registrado", f"Corte registrado - Cliente: {client}"
    )

import csv
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

import requests
from pydantic import ValidationError
from tkcalendar import Calendar  # type: ignore

from barbershop.gui.constants import FILE_PATH
from barbershop.gui.update_information_in_display import update_info_in_display
from barbershop.models.haircut import Haircut


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
    label_income: ttk.Label,
    label_total_haircuts: ttk.Label,
    entry_cliente: ttk.Entry,
    entry_corte: ttk.Entry,
    entry_precio: ttk.Entry,
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
        messagebox.showerror("Error", str(e))  # type: ignore
        return

    with open(FILE_PATH, "a", newline="") as archive:
        writer = csv.writer(archive)
        writer.writerow(haircut_data.model_dump().values())

    # create a haircut in the database
    url = "http://127.0.0.1:8000/haircuts"
    response = requests.post(url, json=haircut_data.model_dump())
    if response.status_code != 201:
        messagebox.showerror("Error", "No se pudo registrar el corte")  # type: ignore
        return

    entry_cliente.delete(0, tk.END)  # type: ignore
    entry_corte.delete(0, tk.END)  # type: ignore
    entry_precio.delete(0, tk.END)  # type: ignore

    update_info_in_display(label_income, label_total_haircuts)
    messagebox.showinfo(  # type: ignore
        "Corte registrado", f"Corte registrado - Cliente: {client}"
    )

import csv
from tkinter import messagebox
import tkinter as tk
from datetime import datetime
from tkcalendar import Calendar
from barbershop.gui import refresh_haircuts_list
from update_income_display import update_info_in_display

def register_new_haircut(label_income, label_total_haircuts ,entry_cliente: str, entry_corte: str, entry_precio: float, calendar: Calendar):
    client = entry_cliente.get()
    haircut = entry_corte.get()
    try: 
        prize = float(entry_precio.get())
    except ValueError:
        messagebox.showerror("Error", "Prize must be a number")
        return
    
    selected_date = calendar.get_date()


    date = datetime.strptime(selected_date, "%m/%d/%Y").strftime("%Y-%m-%d")
    
    register = [client, haircut, prize, date]
    
    with open("register_haircuts.csv", "a", newline="") as archive:
        writer = csv.writer(archive)
        writer.writerow(register)
        
    entry_cliente.delete(0, tk.END)
    entry_corte.delete(0, tk.END)
    entry_precio.delete(0, tk.END)
    
    update_info_in_display(label_income, label_total_haircuts)
    refresh_haircuts_list(text_registros=text_registros)
    messagebox.showinfo("Register successfully", f"Haircut registered - Client: {client}")
    

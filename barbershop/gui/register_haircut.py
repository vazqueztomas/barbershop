import csv
from tkinter import messagebox
import tkinter as tk
from datetime import datetime
from tkcalendar import Calendar, DateEntry

def register_haircut(entry_cliente: str, entry_corte: str, entry_precio: float, calendar: Calendar):
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
    
    messagebox.showinfo("Register successfully", f"Haircut registered - Client: {client}")
    

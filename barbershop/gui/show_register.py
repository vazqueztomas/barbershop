import csv
from tkinter import messagebox
import tkinter as tk

def show_register(text_registros: tk.Text) -> None:
    try:
        with open("register_haircuts.csv", "r") as archive:
            reader = csv.reader(archive)
            
            registers = ""
            
            for fila in reader:
                registers += f"Cliente: {fila[0]}, Corte: {fila[1]}, Precio: ${fila[2]}, Fecha: {fila[3]}\n"

            # Mostrar los registros en un cuadro de texto
            text_registros.config(state=tk.NORMAL)  # Habilitar el cuadro de texto para editar
            text_registros.delete(1.0, tk.END)  # Limpiar el cuadro de texto
            text_registros.insert(tk.END, registers)
            text_registros.config(state=tk.DISABLED)  # Deshabilitar el cuadro de texto para evitar edición
    
    except FileNotFoundError:
        messagebox.showerror("Error", "Aún no hay registros de cortes de pelo.") # type: ignore
        

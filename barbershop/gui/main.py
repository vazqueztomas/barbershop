import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import csv

def register_haircut():
    client = entry_cliente.get()
    haircut = entry_corte.get()
    try: 
        prize = float(entry_precio.get())
    except ValueError:
        messagebox.showerror("Error", "Prize must be a number")
        return
    
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    register = [client, haircut, prize, date]
    
    with open("register_haircuts.csv", "a", newline="") as archive:
        writer = csv.writer(archive)
        writer.writerow(register)
        
    entry_cliente.delete(0, tk.END)
    entry_corte.delete(0, tk.END)
    entry_precio.delete(0, tk.END)
    
    messagebox.showinfo("Register succesfully", f"Haircut registered - Client: {client}")
    
def show_register():
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
        messagebox.showerror("Error", "Aún no hay registros de cortes de pelo.")
        
def update_income_display():
    try:
        with open("register_haircuts.csv", "r") as archive:
            reader = csv.reader(archive)
            
            income = 0
            
            for fila in reader:
                income += float(fila[2])
            
            label_income.config(text=f"Total Income: ${income}")
    except FileNotFoundError:
        label_income.config(text="Total Income: $0")
        
root = tk.Tk()
root.title("Barbershop")

label_cliente = tk.Label(root, text="Cliente:")
label_cliente.grid(row=0, column=0, padx=10, pady=10)
entry_cliente = tk.Entry(root)
entry_cliente.grid(row=0, column=1, padx=10, pady=10)

label_income = tk.Label(root, text="Total Income: $0", font=("Arial", 12, "bold"))	
label_income.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

label_corte = tk.Label(root, text="Tipo de Corte:")
label_corte.grid(row=1, column=0, padx=10, pady=10)
entry_corte = tk.Entry(root)
entry_corte.grid(row=1, column=1, padx=10, pady=10)

label_precio = tk.Label(root, text="Precio:")
label_precio.grid(row=2, column=0, padx=10, pady=10)
entry_precio = tk.Entry(root)
entry_precio.grid(row=2, column=1, padx=10, pady=10)

# Botón para registrar el corte de pelo
button_registrar = tk.Button(root, text="Registrar Corte", command=register_haircut)
button_registrar.grid(row=3, column=0, columnspan=2, pady=20)

# Botón para mostrar los registros
button_mostrar = tk.Button(root, text="Mostrar Registros", command=show_register)
button_mostrar.grid(row=4, column=0, columnspan=2, pady=10)

# Cuadro de texto para mostrar los registros
text_registros = tk.Text(root, height=10, width=50, wrap=tk.WORD, state=tk.DISABLED)
text_registros.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

update_income_display()
root.mainloop()
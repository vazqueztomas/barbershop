import csv
import tkinter as tk
from tkinter import messagebox, ttk


def read_register():
    try:
        with open("register_haircuts.csv", "r") as archive:
            reader = csv.reader(archive)
            data = [row for row in reader]
            return data
    except FileNotFoundError:
        messagebox.showerror("Error", "There are no haircut records yet.")
        return []
    
def show_table(data):
    root = tk.Tk()
    root.title("Registro de Cortes de Pelo")

    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    table = ttk.Treeview(frame, columns=("Numero", "Cliente", "Corte", "Precio", "Fecha"), show="headings")
    table.heading("Numero", text="Numero")
    table.heading("Cliente", text="Cliente")
    table.heading("Corte", text="Corte")
    table.heading("Precio", text="Precio")
    table.heading("Fecha", text="Fecha")

    for i, row in enumerate(data, start=1):
        table.insert("", tk.END, values=(i, *row))

    table.pack(fill=tk.BOTH, expand=True)
    
# Función para eliminar un corte seleccionado
    def delete_selected_cut(table):
        selected_item = table.selection()
        if not selected_item:
            messagebox.showwarning("Selección inválida", "Por favor, seleccione un corte para eliminar.")
            return

        # Obtener el índice de la fila seleccionada
        selected_row = table.item(selected_item[0])["values"]
        row_index = int(selected_row[0]) - 1  # La fila en la tabla corresponde a la posición en la lista

        # Leer los registros
        data = read_register()

        # Eliminar la fila correspondiente
        if 0 <= row_index < len(data):
            del data[row_index]

            # Escribir de nuevo el archivo CSV sin la fila eliminada
            with open("register_haircuts.csv", "w", newline="") as archive:
                writer = csv.writer(archive)
                writer.writerows(data)

            messagebox.showinfo("Corte Eliminado", "El corte de pelo ha sido eliminado correctamente.")  # Cerrar la ventana de la tabla
            show_table(data)

        delete_button = tk.Button(root, text="Eliminar Corte", command=lambda: delete_selected_cut)
        delete_button.grid(pady=10)
    root.mainloop()

    

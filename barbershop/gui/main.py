import tkinter as tk
from utils.generate_label import generate_label
from update_income_display import update_income_display
from register_haircut import register_haircut
from show_register import show_register
from read_register import read_register, show_table

root = tk.Tk()
root.title("Barbershop")

# Etiquetas y campos de entrada
label_cliente = generate_label(root, text="Cliente:", row=0, column=0)
entry_cliente = tk.Entry(root)
entry_cliente.grid(row=0, column=1, padx=10, pady=10)

label_income = generate_label(root, text="Total Income: $0", row=6, column=0)

label_corte = generate_label(root, text="Tipo de Corte:", row=1, column=0)
entry_corte = tk.Entry(root)
entry_corte.grid(row=1, column=1, padx=10, pady=10)

label_precio = generate_label(root, text="Precio:", row=2, column=0)
entry_precio = tk.Entry(root)
entry_precio.grid(row=2, column=1, padx=2, pady=2)

# Botón para registrar el corte de pelo
button_registrar = tk.Button(
    root,
    text="Registrar Corte",
    command=lambda: register_haircut(entry_cliente, entry_corte, entry_precio),
)
button_registrar.grid(row=3, column=0, columnspan=3, pady=20, padx=10, sticky="ew")

# Cuadro de texto para mostrar los registros
text_registros = tk.Text(root, height=10, width=50, wrap=tk.WORD, state=tk.DISABLED)
text_registros.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

show_register(text_registros)

# Botón para mostrar la tabla
button_mostrar_tabla = tk.Button(
    root, text="Mostrar Tabla", command=lambda: show_table(read_register())
)
button_mostrar_tabla.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

# Actualizar los ingresos
update_income_display(label_income=label_income)

root.mainloop()

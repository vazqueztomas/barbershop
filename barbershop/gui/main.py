import tkinter as tk
from tkinter import ttk
from barbershop.gui.utils.generate_label import generate_label
from barbershop.gui.update_income_display import update_info_in_display
from barbershop.gui.haircut_registration import register_new_haircut
from barbershop.gui.show_register import show_register
from barbershop.gui.read_register import read_register, show_table
from tkcalendar import Calendar  # type: ignore
from barbershop.gui.constants import FILE_PATH

def refresh_haircuts_list():
    show_register(text_registros)


root = tk.Tk()
root.title("Barbershop")

# Etiquetas y campos de entrada
label_cliente = generate_label(root, text="Cliente:", row=0, column=0)
entry_cliente = tk.Entry(root)
entry_cliente.grid(row=0, column=1, padx=10, pady=10)

label_fecha = generate_label(root, text="Fecha:", row=4, column=0)

label_income = generate_label(
    root, text="Total ganado: $0", row=7, column=0, isBold=True
)
label_total_haircuts = generate_label(
    root, text="Cortes realizados: 0", row=7, column=2, isBold=True
)

label_corte = generate_label(root, text="Tipo de Corte:", row=1, column=0)
entry_corte = tk.Entry(root)
entry_corte.grid(row=1, column=1, padx=10, pady=10)

label_precio = generate_label(root, text="Precio:", row=2, column=0)
entry_precio = tk.Entry(root)
entry_precio.grid(row=2, column=1, padx=2, pady=2)


style = ttk.Style()
style.configure("TButton", font=("Comic Sans", 12), padding=5)  # type: ignore

calendar = Calendar(root, selectmode="day", date_pattern="mm/dd/yyyy")
calendar.grid(row=4, column=1, padx=10, pady=10)  # type: ignore

# Botón para registrar el corte de pelo
button_registrar = ttk.Button(
    root,
    text="Registrar nuevo corte",
    command=lambda: register_new_haircut(
        label_income,
        label_total_haircuts,
        entry_cliente,
        entry_corte,
        entry_precio,
        calendar=calendar,
        text_registros=text_registros,
    ),
    style="TButton",
)
button_registrar.grid(row=5, column=0, columnspan=3, pady=20, padx=10, sticky="ew")

# Cuadro de texto para mostrar los registros
text_registros = tk.Text(root, height=10, width=50, wrap=tk.WORD, state=tk.DISABLED)
text_registros.grid(row=8, column=0, columnspan=3, padx=10, pady=10)


# Botón para mostrar la tabla
button_mostrar_tabla = ttk.Button(
    root,
    text="Cortes",
    command=lambda: show_table(
        read_register(FILE_PATH),
        label_income=label_income,
        label_total_haircuts=label_total_haircuts,
    ),
    style="TButton",
)
button_mostrar_tabla.grid(row=6, column=0, padx=10, pady=10, sticky="ew")


# Actualizar los ingresos
update_info_in_display(label_income=label_income, label_haircuts=label_total_haircuts)
refresh_haircuts_list()

root.mainloop()

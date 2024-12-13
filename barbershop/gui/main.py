import tkinter as tk
from barbershop.gui.utils.generate_label import generate_label
from barbershop.gui.update_income_display import update_info_in_display
from barbershop.gui.haircut_registration import register_new_haircut
from barbershop.gui.show_register import show_register
from barbershop.gui.read_register import read_register, show_table
from barbershop.gui.show_historico import show_historico
from tkcalendar import Calendar  # type: ignore
from barbershop.gui.constants import FILE_PATH
import customtkinter as ctk  # type: ignore
from tkinter import ttk


def refresh_haircuts_list():
    show_register(text_registros)


root = ctk.CTk()
root.title("Barbershop")

label_cliente = generate_label(root, text="Cliente:", row=0, column=0)
entry_cliente = ctk.CTkEntry(root)
entry_cliente.grid(row=0, column=1, padx=10, pady=10)  # type: ignore

label_fecha = generate_label(root, text="Fecha:", row=4, column=0)

label_income = generate_label(
    root, text="Total ganado: $0", row=7, column=0, isBold=True
)
label_total_haircuts = generate_label(
    root, text="Cortes realizados: 0", row=7, column=2, isBold=True
)

label_corte = generate_label(root, text="Tipo de Corte:", row=1, column=0)
entry_corte = ctk.CTkEntry(root)
entry_corte.grid(row=1, column=1, pady=10)  # type: ignore

label_precio = generate_label(root, text="Precio:", row=2, column=0)
entry_precio = ctk.CTkEntry(root)
entry_precio.grid(row=2, column=1)  # type: ignore


calendar = Calendar(root, selectmode="day", date_pattern="mm/dd/yyyy")
calendar.grid(row=4, column=1, padx=10, pady=10)  # type: ignore

selected_option = tk.IntVar()
rb_pelo = ttk.Radiobutton(root, text="Pelo", variable=selected_option, value=1)
rb_pelo.grid(row=3, column=0, padx=10, pady=10)  # type: ignore

rb_pelo_y_barba = ttk.Radiobutton(
    root, text="Pelo y Barba", variable=selected_option, value=2
)
rb_pelo_y_barba.grid(row=3, column=1, padx=10, pady=10)  # type: ignore

rb_barba = ttk.Radiobutton(root, text="Barba", variable=selected_option, value=3)
rb_barba.grid(row=3, column=2, padx=10, pady=10)  # type: ignore

button_registrar = ctk.CTkButton(
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
        checkbox_pelo=rb_pelo,
        checkbox_pelo_y_barba=rb_pelo_y_barba,
        checkbox_barba=rb_barba,
    ),
)
button_registrar.grid(row=5, column=0, columnspan=3, pady=20, padx=10, sticky="ew")  # type: ignore

text_registros = tk.Text(root, height=10, width=50, wrap=tk.WORD, state=tk.DISABLED)
text_registros.grid(row=8, column=0, columnspan=3, padx=10, pady=10)


button_mostrar_tabla = ctk.CTkButton(
    root,
    text="Cortes",
    command=lambda: show_table(
        read_register(FILE_PATH),
        label_income=label_income,
        label_total_haircuts=label_total_haircuts,
    ),
    font=("Arial", 16),
)
button_mostrar_tabla.grid(row=6, column=0, padx=10, pady=10, sticky="ew")  # type: ignore


button_mostrar_historico = ctk.CTkButton(
    root,
    text="Historico",
    command=lambda: show_historico(),
    font=("Arial", 16),
)
button_mostrar_historico.grid(row=6, column=1, padx=10, pady=10, sticky="ew")  # type: ignore


update_info_in_display(label_income=label_income, label_haircuts=label_total_haircuts)
refresh_haircuts_list()

root.mainloop()  # type: ignore

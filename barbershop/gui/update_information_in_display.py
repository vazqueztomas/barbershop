import csv
from tkinter import ttk
from pathlib import Path
from barbershop.gui.constants import FILE_PATH


def update_info_in_display(label_income: ttk.Label, label_haircuts: ttk.Label) -> None:
    try:
        with Path(FILE_PATH).open() as archive:
            reader = csv.reader(archive)

            income = 0
            total_haircuts = 0
            for fila in reader:
                income += float(fila[3])
                total_haircuts += 1

            label_income.configure(text=f"Total ganado: ${income}")  # type: ignore
            label_haircuts.configure(text=f"Cortes realizados: {total_haircuts}")  # type: ignore
    except FileNotFoundError:
        label_income.configure(text="Total ganado: $0")  # type: ignore

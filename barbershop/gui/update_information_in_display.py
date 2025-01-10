from tkinter import ttk

import requests

from barbershop.models.haircut import Haircut
from barbershop.gui.constants import BASE_URL


def get_haircuts_list() -> list[dict[str, Haircut]]:
    return requests.get(f"{BASE_URL}/haircuts").json()


def update_info_in_display(label_income: ttk.Label, label_haircuts: ttk.Label) -> None:
    try:
        haircut_list = get_haircuts_list()
        if haircut_list:
            income = 0
            total_haircuts = 0
            for haircut in haircut_list:
                income += float(haircut["prize"])
                total_haircuts += 1

            label_income.configure(text=f"Total ganado: ${income}")  # type: ignore
            label_haircuts.configure(text=f"Cortes realizados: {total_haircuts}")  # type: ignore
    except FileNotFoundError:
        label_income.configure(text="Total ganado: $0")  # type: ignore

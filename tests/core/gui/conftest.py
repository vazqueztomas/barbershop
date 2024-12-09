from typing import Generator, Literal, Any

import pytest
import csv
import os


@pytest.fixture
def file_path() -> str:
    return "register_haircuts.csv"


dummy_data: list[list[Any]] = [
    ["John Doe", "", 4500.0, "2024-11-01 08:30:00"],
    ["Jane Smith", "", 5200.0, "2024-11-02 09:15:20"],
    ["Test User", "mullet", 3000.0, "2024-11-03 10:45:10"],
    ["Mark Test", "cresta", 5500.0, "2024-11-04 11:00:30"],
    ["Anna Test", "mullet", 3100.0, "2024-11-05 14:20:40"],
    ["David T", "cresta", 5300.0, "2024-11-06 15:35:50"],
    ["Lucas R", "Fade alto", 4800.0, "2024-11-07 16:50:00"],
    ["Sophia L", "Cresta baja", 5100.0, "2024-11-08 17:05:10"],
    ["Emily W", "Fade bajo", 4700.0, "2024-11-09 18:15:30"],
    ["Chris H", "fade alto", 4600.0, "2024-11-10 19:30:00"],
]


@pytest.fixture
def create_csv() -> Generator[Literal["test_haircuts.csv"], None, None]:
    """Fixture para crear un archivo CSV con datos de prueba."""
    file_path = "test_haircuts.csv"

    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Client", "Haircut", "Price", "Date"])  # Escribir encabezado
        writer.writerows(dummy_data)  # Escribir datos de prueba

    yield file_path

    if os.path.exists(file_path):
        os.remove(file_path)

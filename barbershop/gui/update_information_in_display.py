import csv
import customtkinter as ctk #type: ignore

def update_info_in_display(label_income: ctk.CTkLabel, label_haircuts: ctk.CTkLabel) -> None:
    try:
        with open("register_haircuts.csv", "r") as archive:
            reader = csv.reader(archive)
            
            income = 0
            total_haircuts = 0
            for fila in reader:
                print(fila)
                income += float(fila[3])
                total_haircuts += 1
            
            label_income.configure(text=f"Total ganado: ${income}") #type: ignore
            label_haircuts.configure(text=f"Cortes realizados: {total_haircuts}") #type: ignore 
    except FileNotFoundError:
        label_income.configure(text="Total ganado: $0")#type: ignore 
        
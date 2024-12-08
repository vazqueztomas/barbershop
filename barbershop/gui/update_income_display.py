import csv
def update_income_display(label_income):
    try:
        with open("register_haircuts.csv", "r") as archive:
            reader = csv.reader(archive)
            
            income = 0
            
            for fila in reader:
                income += float(fila[2])
            
            label_income.config(text=f"Total Income: ${income}")
    except FileNotFoundError:
        label_income.config(text="Total Income: $0")
        
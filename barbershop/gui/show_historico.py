import tkinter as tk
from tkinter import ttk, messagebox


def show_historico():
    window = tk.Tk()
    window.title("Historico")
    window.geometry("800x600")
    window.config(bg="white")

    tree = ttk.Treeview(
        window, columns=("Cliente", "Corte", "Precio", "Fecha", "Tipo"), show="headings"
    )
    tree.heading("Cliente", text="Cliente")
    tree.heading("Corte", text="Corte")
    tree.heading("Precio", text="Precio")
    tree.heading("Fecha", text="Fecha")
    tree.pack()

    with open("register_haircuts.csv", "r") as archive:
        for row in archive:
            row = row.strip().split(",")
            tree.insert("", tk.END, values=row)

    # Filter by month
    def filter_by_month():
        month = entry_month.get()
        tree.delete(*tree.get_children())
        with open("register_haircuts.csv", "r") as archive:
            for row in archive:
                row = row.strip().split(",")
                if row[3].split("-")[1] == month:
                    tree.insert("", tk.END, values=row)

        show_total_month()

    entry_month = ttk.Entry(window)
    entry_month.pack()
    button_filter = ttk.Button(window, text="Filtrar por mes", command=filter_by_month)
    button_filter.pack()

    def filter_by_day():
        day = entry_day.get()
        tree.delete(*tree.get_children())
        with open("register_haircuts.csv", "r") as archive:
            for row in archive:
                row = row.strip().split(",")
                if row[3].split("-")[2] == day:
                    tree.insert("", tk.END, values=row)

    entry_day = ttk.Entry(window)
    entry_day.pack()
    button_filter = ttk.Button(window, text="Filtrar por dia", command=filter_by_day)
    button_filter.pack()

    # Show total month in a label automatically when filter by month
    def show_total_month():
        total = 0
        for child in tree.get_children():
            total += float(tree.item(child)["values"][2])
        label_total_month.config(text=f"Total del mes: ${total}")

    label_total_month = ttk.Label(window, text="Total del mes: $0")
    label_total_month.pack()

    window.mainloop()

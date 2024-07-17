import os
import sys
import platform
import subprocess
import tkinter as tk
from tkinter import ttk

LIMITS = [
    (100, "#8b0000"),  # Dark red for expenses over $100
    (50, "#808000"),   # Olive for expenses between $50 and $100
    (20, "#556b2f"),   # Dark olive green for expenses between $20 and $50
]

def add_expense():
    date, category, amount = date_entry.get(), category_entry.get(), amount_entry.get()
    if date and category and amount:
        try:
            month, day, year = map(int, date.split('-'))
            formatted_date = f"{month:02d}-{day:02d}-{year}"
            amount = float(amount)
        except ValueError:
            status_label.config(text="Please enter a valid date or amount!", fg="red")
            return

        with open("expenses.txt", "a") as file:
            file.write(f"{formatted_date},{category},{amount}\n")
        status_label.config(text="Expense added successfully!", fg="green")
        date_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        display_expenses()
    else:
        status_label.config(text="Please fill all the fields!", fg="red")

def get_tag_for_amount(amount):
    for limit, color in LIMITS:
        if amount > limit:
            return color
    return ""

def display_expenses():
    if os.path.exists("expenses.txt"):
        total_expense = 0
        expenses_tree.delete(*expenses_tree.get_children())
        with open("expenses.txt", "r") as file:
            for line in file:
                date, category, amount = line.strip().split(",")
                amount = float(amount)
                total_expense += amount
                tag = get_tag_for_amount(amount)
                expenses_tree.insert("", tk.END, values=(date, category, amount), tags=(tag,))
        total_label.config(text=f"Total Expense: ${total_expense:.2f}")
    else:
        total_label.config(text="No expenses recorded.")

def open_expenses_file():
    if os.path.exists("expenses.txt"):
        current_os = platform.system()
        if current_os == "Windows":
            os.system(f'start "" "expenses.txt"')
        elif current_os == "Darwin":  # macOS
            os.system(f'open "expenses.txt"')
        elif current_os == "Linux":
            os.system(f'xdg-open "expenses.txt"')

def close_program():
    root.destroy()

def adjust_expense():
    selected_item = expenses_tree.selection()
    if selected_item:
        item_text = expenses_tree.item(selected_item, "values")
        date, category, amount = item_text

        adjust_window = tk.Toplevel(root)
        adjust_window.title("Adjust Expense")

        tk.Label(adjust_window, text="Date (MM-DD-YYYY):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        adjust_date_entry = tk.Entry(adjust_window)
        adjust_date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        adjust_date_entry.insert(0, date)

        tk.Label(adjust_window, text="Category:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        adjust_category_entry = tk.Entry(adjust_window)
        adjust_category_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        adjust_category_entry.insert(0, category)

        tk.Label(adjust_window, text="Amount:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        adjust_amount_entry = tk.Entry(adjust_window)
        adjust_amount_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        adjust_amount_entry.insert(0, amount)

        # Adjustment button code 
        def save_adjustment():
            new_date, new_category, new_amount = adjust_date_entry.get(), adjust_category_entry.get(), adjust_amount_entry.get()
            if new_date and new_category and new_amount:
                try:
                    month, day, year = map(int, new_date.split('-'))
                    formatted_new_date = f"{month:02d}-{day:02d}-{year}"
                    new_amount = float(new_amount)
                except ValueError:
                    adjust_status_label.config(text="Please enter a valid date or amount!", fg="red")
                    return

                with open("expenses.txt", "r") as file:
                    lines = file.readlines()
                with open("expenses.txt", "w") as file:
                    for line in lines:
                        if line.strip() == f"{date},{category},{amount}":
                            file.write(f"{formatted_new_date},{new_category},{new_amount}\n")
                        else:
                            file.write(line)

                status_label.config(text="Expense adjusted successfully!", fg="green")
                adjust_window.destroy()
                display_expenses()
            else:
                status_label.config(text="Please fill all the fields!", fg="red")
# import os module file and operating system related functions 
import os
# import the platform module to detect os
import platform 
# Import tkinter module for creating GUI application
import tkinter as tk
# import ttk from tkinter for widgets 
from tkinter import ttk

LIMITS = [
    (100, "#8b0000"),  # Dark red for expenses over $100
    (50, "#808000"),   # Olive for expenses between $50 and $100
    (20, "#556b2f"),   # Dark olive green for expenses between $20 and $50
]

# Function to add an expense 
def add_expense():
    date, category, amount = date_entry.get(), category_entry.get(), amount_entry.get()
    # to check if all required fields are filled 
    if date and category and amount:
        try:
            # formate to eneter date and amount 
            month, day, year = map(int, date.split('-'))
            formatted_date = f"{month:02d}-{day:02d}-{year}"
            amount = float(amount)
        except ValueError:
            # let user know if theres an error in value
            status_label.config(text="Please enter a valid date or amount!", fg="red")
            return
           # writes expense to text file 
        with open("expenses.txt", "a") as file:
            file.write(f"{formatted_date},{category},{amount}\n")
            # indicates. lets user know change is saved 
        status_label.config(text="Expense added successfully!", fg="green")
        # deletes the enter 
        date_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        # refreshes dispay 
        display_expenses()
    else:
        # error msg if any fiels are empty 
        status_label.config(text="Please fill all the fields!", fg="red")
# function to determine change of color by amount 
def get_tag_for_amount(amount):
    for limit, color in LIMITS:
        if amount > limit:
            return color
    return ""
# function to display all expenses 
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
                adjust_status_label.config(text="Please fill all the fields!", fg="red")

        save_button = tk.Button(adjust_window, text="Save Adjustment", command=save_adjustment)
        save_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        adjust_status_label = tk.Label(adjust_window, text="", fg="green")
        adjust_status_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
    else:
        status_label.config(text="Please select an expense to adjust!", fg="red")

def delete_expense():
    selected_item = expenses_tree.selection()
    if selected_item:
        item_text = expenses_tree.item(selected_item, "values")
        date, category, amount = item_text

        with open("expenses.txt", "r") as file:
            lines = file.readlines()
        with open("expenses.txt", "w") as file:
            for line in lines:
                if line.strip() != f"{date},{category},{amount}":
                    file.write(line)

        status_label.config(text="Expense deleted successfully!", fg="green")
        display_expenses()
    else:
        status_label.config(text="Please select an expense to delete!", fg="red")

# Create the main application window
root = tk.Tk()
root.title("Expense Tracker")

tk.Label(root, text="Date (MM-DD-YYYY):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
date_entry = tk.Entry(root)
date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

tk.Label(root, text="Category:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
category_entry = tk.Entry(root)
category_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

tk.Label(root, text="Amount:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
amount_entry = tk.Entry(root)
amount_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

tk.Button(root, text="Add Expense", command=add_expense).grid(row=3, column=0, columnspan=2, padx=5, pady=10)

columns = ("Date", "Category", "Amount")
expenses_tree = ttk.Treeview(root, columns=columns, show="headings")
expenses_tree.heading("Date", text="Date")
expenses_tree.heading("Category", text="Category")
expenses_tree.heading("Amount", text="Amount")
expenses_tree.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

for limit, color in LIMITS:
    expenses_tree.tag_configure(color, background=color)

total_label = tk.Label(root, text="")
total_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

status_label = tk.Label(root, text="", fg="green")
status_label.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

tk.Button(root, text="View Expenses", command=open_expenses_file).grid(row=7, column=0, padx=5, pady=10)
tk.Button(root, text="Adjust Expense", command=adjust_expense).grid(row=7, column=1, padx=5, pady=10)
tk.Button(root, text="Delete Expense", command=delete_expense).grid(row=7, column=2, padx=5, pady=10)
tk.Button(root, text="Close", command=close_program).grid(row=8, column=0, columnspan=3, padx=5, pady=10)

if not os.path.exists("expenses.txt"):
    with open("expenses.txt", "w"):
        pass

display_expenses()
root.mainloop()

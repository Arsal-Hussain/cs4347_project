import tkinter as tk
import re
from tkinter import messagebox, ttk
from lib.fines import update_fines, display_fines, pay_fines, generate_test_data, update_fines

def open_fines_nav(parent):
    window = tk.Toplevel(parent)
    window.title("Fines Navigation")

    # Create buttons for different actions
    update_fines_btn = tk.Button(window, text="Refresh Fines", command=lambda: get_latest_fines(window))
    update_fines_btn.grid(row=0, columnspan=2, sticky="ew", padx=10, pady=5)
    #update_fines_btn.pack(pady=10)

    display_fines_btn = tk.Button(window, text="Display Fines", command=lambda: open_display_fines_form(window))
    display_fines_btn.grid(row=1, column=0, padx=10, pady=5)
    #display_fines_btn.pack(pady=10)

    pay_fines_btn = tk.Button(window, text="Pay Fines", command=lambda: open_pay_fines_form(window))
    pay_fines_btn.grid(row=1, column=1, padx=10, pady=5)
    #pay_fines_btn.pack(pady=10)

def open_display_fines_form(parent):
    window = tk.Toplevel(parent)
    window.title("Display Fines")

    fines = display_fines()
    print(fines)

    column_names = ['Card ID', 'Name', 'Total Fine ($)']
    tree = ttk.Treeview(window, columns=column_names, show="headings")  # Use window, not parent
    for col in column_names:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    tree.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    for row in fines:
        tree.insert("", "end", values=tuple(row))

def open_pay_fines_form(parent):
    window = tk.Toplevel(parent)
    window.title("Pay Fines")

    tk.Label(window, text="Card ID:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
    id_entry = tk.Entry(window, width=40)
    id_entry.grid(row=0, column=1, padx=10, pady=5)

    def submit_fines():
        print('fine submitted')
        card_id = id_entry.get().strip()
        if not card_id:
            messagebox.showerror("Validation Error", "Card ID cannot be empty.")
            return

        # Validate Card ID format: "ID######"
        if not re.fullmatch(r"ID\d{6}", card_id):
            messagebox.showerror("Validation Error", "Card ID must be in the format ID######.")
            return

        response = pay_fines(card_id)
        if response is not None and "Success:" in response:
            messagebox.showinfo("Success", "The fine has been paid successfully.")
        else:
            messagebox.showerror("Error in payment", "There was an error processing the payment. Please check the Card ID and try again.")

    submit_btn = tk.Button(window, text="Pay Fines", command=submit_fines)
    submit_btn.grid(row=4, column=0, columnspan=2, pady=20)

def get_latest_fines(parent):
    window = tk.Toplevel(parent)
    window.title("Refresh Fines")

    response = update_fines()
    if response is not None and "Success:" in response:
        messagebox.showinfo("Success", "Fines have been updated successfully.")
    else:
        messagebox.showerror("Error", "There was an error updating the fines. Please try again.")
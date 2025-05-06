import tkinter as tk
import re
from tkinter import messagebox, ttk
from lib.fines import update_fines, display_fines, pay_fines
from lib.database import get_connection

def open_fines_nav(parent):
    window = tk.Toplevel(parent)
    window.title("Fines Navigation")

    tk.Button(window, text="Refresh Fines", command=lambda: get_latest_fines(window)).grid(row=0, columnspan=2, sticky="ew", padx=10, pady=5)
    tk.Button(window, text="Display Fines", command=lambda: open_display_fines_form(window)).grid(row=1, column=0, padx=10, pady=5)
    tk.Button(window, text="Pay Fines", command=lambda: open_pay_fines_form(window)).grid(row=1, column=1, padx=10, pady=5)

def open_display_fines_form(parent):
    window = tk.Toplevel(parent)
    window.title("Display Fines")

    fines = display_fines()

    column_names = ['Card ID', 'Name', 'Total Fine ($)']
    tree = ttk.Treeview(window, columns=column_names, show="headings")
    for col in column_names:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    tree.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    for row in fines:
        # Ensure tuple format: (Card_id, Name, Fine_amount)
        card_id = row['Card_id'] if 'Card_id' in row else row[0]
        name = row['Name'] if 'Name' in row else row[1]
        amount = row['Fine'] if 'Fine' in row else row[2]
        tree.insert("", "end", values=(card_id, name, f"{amount:.2f}"))

def open_pay_fines_form(parent):
    window = tk.Toplevel(parent)
    window.title("Pay Fines")

    tk.Label(window, text="Card ID:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
    id_entry = tk.Entry(window, width=40)
    id_entry.grid(row=0, column=1, padx=10, pady=5)

    def submit_fines():
        card_id = id_entry.get().strip()
        if not card_id:
            messagebox.showerror("Validation Error", "Card ID cannot be empty.")
            return

        if not re.fullmatch(r"(B\d{3,}|ID\d{6,})", card_id):
            messagebox.showerror("Validation Error", "Card ID must be in the format B### or ID######.")
            return


        # Check if Card ID exists in the database
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM BORROWER WHERE Card_id = ?", (card_id,))
        if cursor.fetchone() is None:
            messagebox.showerror("Invalid Card ID", "This Card ID does not exist in the system.")
            return

        response = pay_fines(card_id)
        if response and "Success:" in response:
            messagebox.showinfo("Success", response)
            window.destroy()
        elif response and "Info:" in response:
            messagebox.showinfo("Info", response)
        else:
            messagebox.showerror("Error", "Error processing payment. Check card and try again.")

            window.destroy()

    tk.Button(window, text="Pay Fines", command=submit_fines).grid(row=1, column=0, columnspan=2, pady=20)

def get_latest_fines(parent):
    update_fines()
    messagebox.showinfo("Fines Updated", "Fines have been refreshed successfully.")

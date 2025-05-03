# borrower_form.py
import tkinter as tk
import re
from tkinter import messagebox
from lib.borrower import create_borrower

def open_borrower_form(parent):
    window = tk.Toplevel(parent)
    window.title("Register New Borrower")

    # Define form labels and entries
    tk.Label(window, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
    name_entry = tk.Entry(window, width=40)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(window, text="SSN:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
    ssn_entry = tk.Entry(window, width=40)
    ssn_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(window, text="Address:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
    address_entry = tk.Entry(window, width=40)
    address_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(window, text="Phone:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
    phone_entry = tk.Entry(window, width=40)
    phone_entry.grid(row=3, column=1, padx=10, pady=5)

    # Define the submit action inside to capture the entries
    def submit_borrower():
        name = name_entry.get().strip()
        ssn = ssn_entry.get().strip()
        address = address_entry.get().strip()
        phone = phone_entry.get().strip()

            # Validate name (must have at least two words)
        if len(name.split()) < 2:
            messagebox.showerror("Validation Error", "Please enter at least a first and last name.")
            return

        # Validate SSN format: "###-##-####"
        if not re.fullmatch(r"\d{3}-\d{2}-\d{4}", ssn):
            messagebox.showerror("Validation Error", "SSN must be in the format ###-##-####.")
            return

        # Validate phone number format: "(###) ### ####"
        if not re.fullmatch(r"\(\d{3}\) \d{3}-\d{4}", phone):
            messagebox.showerror("Validation Error", "Phone must be in the format (###) ###-####.")
            return


        response = create_borrower(name, ssn, address, phone)
        if "Success:" in response:
            messagebox.showinfo("Success", response)
            window.destroy()
        else:
            messagebox.showerror("Error", response)


    # Submit button
    submit_btn = tk.Button(window, text="Register Borrower", command=submit_borrower)
    submit_btn.grid(row=4, column=0, columnspan=2, pady=20)
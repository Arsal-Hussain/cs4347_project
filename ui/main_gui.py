import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox
from lib.search import search_books
from lib.borrower import create_borrower
from lib.loaning import checkout, checkin
from ui.fines_form import open_fines_nav  # NEW IMPORT

class LibraryGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library System")
        self.geometry("700x500")
        self.create_widgets()

    def create_widgets(self):
        options = [
            ("Search Books", self.search_books_ui),
            ("Register Borrower", self.register_borrower_ui),
            ("Fines", lambda: open_fines_nav(self)),
            ("Check Out Book", self.checkout_ui),
            ("Check In Book", self.checkin_ui),
        ]
        for _, (text, command) in enumerate(options):
            btn = ttk.Button(self, text=text, command=command)
            btn.pack(pady=5, fill='x')

    def search_books_ui(self):
        top = tk.Toplevel(self)
        top.title("Search Books")

        tk.Label(top, text="Enter Title, Author, or ISBN:").pack(pady=5)
        entry = tk.Entry(top, width=50)
        entry.pack(pady=5)

        columns = ("ISBN", "Title", "Authors", "Checked Out", "Borrower ID")
        tree = ttk.Treeview(top, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")
        tree.pack(pady=10, padx=10, fill="both", expand=True)

        def search_action():
            keyword = entry.get()
            results = search_books(keyword)
            tree.delete(*tree.get_children())  # Clear previous results
            for row in results:
                tree.insert("", "end", values=(
                    row['Isbn'],
                    row['Title'],
                    row['Authors'],
                    row['Status'],
                    row['Borrower_id'] if row['Borrower_id'] else ""
                ))

        tk.Button(top, text="Search", command=search_action).pack(pady=5)



    def register_borrower_ui(self):
        top = tk.Toplevel(self)
        top.title("Register Borrower")

        labels = ["First Name", "Last Name", "SSN", "Address", "Phone"]
        entries = []

        for label in labels:
            tk.Label(top, text=label).pack()
            entry = tk.Entry(top)
            entry.pack()
            entries.append(entry)

        def register_action():
            fname, lname, ssn, address, phone = [e.get().strip() for e in entries]
            full_name = f"{fname} {lname}"
            response = create_borrower(full_name, ssn, address, phone)
            if response.startswith("Success"):
                messagebox.showinfo("Success", f"Borrower Registered.\n{response}")
                top.destroy()
            else:
                messagebox.showerror("Error", response)

        tk.Button(top, text="Register", command=register_action).pack()

    def checkout_ui(self):
        top = tk.Toplevel(self)
        top.title("Check Out Book")

        tk.Label(top, text="ISBN:").pack()
        isbn_entry = tk.Entry(top)
        isbn_entry.pack()

        tk.Label(top, text="Borrower ID:").pack()
        card_entry = tk.Entry(top)
        card_entry.pack()

        def checkout_action():
            checkout(isbn_entry.get(), card_entry.get())
            messagebox.showinfo("Success", "Book Checked Out")
            top.destroy()

        tk.Button(top, text="Check Out", command=checkout_action).pack()

    def checkin_ui(self):
        top = tk.Toplevel(self)
        top.title("Check In Book")

        tk.Label(top, text="ISBN:").pack()
        isbn_entry = tk.Entry(top)
        isbn_entry.pack()

        tk.Label(top, text="Card ID:").pack()
        card_entry = tk.Entry(top)
        card_entry.pack()

        tk.Label(top, text="Borrower Name (optional):").pack()
        name_entry = tk.Entry(top)
        name_entry.pack()

        def checkin_action():
            checkin(isbn_entry.get(), card_entry.get(), name_entry.get())
            messagebox.showinfo("Success", "Check-in operation completed.")
            top.destroy()

        tk.Button(top, text="Check In", command=checkin_action).pack()

if __name__ == "__main__":
    app = LibraryGUI()
    app.mainloop()

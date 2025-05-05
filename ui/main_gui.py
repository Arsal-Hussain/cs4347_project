import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tkinter as tk
from tkinter import ttk, messagebox
from lib.search import search_books
from lib.borrower import create_borrower
from lib.loaning import checkout, checkin
from lib.fines import update_fines, display_fines, pay_fines

class LibraryGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library System")
        self.geometry("700x500")
        self.create_widgets()

    def create_widgets(self):
        # Menu Buttons
        options = [
            ("Search Books", self.search_books_ui),
            ("Register Borrower", self.register_borrower_ui),
            ("Update Fines", self.update_fines_ui),
            ("Display Fines", self.display_fines_ui),
            ("Pay Fines", self.pay_fines_ui),
            ("Check Out Book", self.checkout_ui),
            ("Check In Book", self.checkin_ui),
        ]

        for idx, (text, command) in enumerate(options):
            btn = ttk.Button(self, text=text, command=command)
            btn.pack(pady=5, fill='x')

    def search_books_ui(self):
        top = tk.Toplevel(self)
        top.title("Search Books")

        tk.Label(top, text="Enter Title, Author, or ISBN:").pack()
        entry = tk.Entry(top)
        entry.pack()

        output = tk.Text(top, height=10)
        output.pack()

        def search_action():
            keyword = entry.get()
            results = search_books(keyword)
            output.delete("1.0", tk.END)
            for row in results:
                output.insert(tk.END, f"{row['Isbn']} | {row['Title']} | {row['Authors']} | {row['Status']}\n")

        tk.Button(top, text="Search", command=search_action).pack()

    def register_borrower_ui(self):
        top = tk.Toplevel(self)
        top.title("Register Borrower")

        labels = ["First Name", "Last Name", "Address", "Phone (optional)"]
        entries = []

        for label in labels:
            tk.Label(top, text=label).pack()
            entry = tk.Entry(top)
            entry.pack()
            entries.append(entry)

        def register_action():
            fname, lname, address, phone = [e.get() for e in entries]
            card_id = create_borrower(fname, lname, address, phone)
            messagebox.showinfo("Success", f"Borrower Registered. Card ID: {card_id}")
            top.destroy()

        tk.Button(top, text="Register", command=register_action).pack()

    def update_fines_ui(self):
        update_fines()
        messagebox.showinfo("Fines", "Fines updated successfully.")

    def display_fines_ui(self):
        fines = display_fines()
        top = tk.Toplevel(self)
        top.title("Display Fines")
        text = tk.Text(top)
        text.pack()
        for fine in fines:
            text.insert(tk.END, f"{fine}\n")

    def pay_fines_ui(self):
        top = tk.Toplevel(self)
        top.title("Pay Fines")

        tk.Label(top, text="Enter Card ID:").pack()
        entry = tk.Entry(top)
        entry.pack()

        def pay_action():
            card_id = entry.get()
            pay_fines(card_id)
            messagebox.showinfo("Success", f"Fines paid for Card ID: {card_id}")

        tk.Button(top, text="Pay", command=pay_action).pack()

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

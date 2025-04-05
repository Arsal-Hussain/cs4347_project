from lib.search import search_books
from lib.borrower import create_borrower
from lib.fines import update_fines, display_fines, pay_fines
from lib.loaning import checkin, checkout

def main():
    while True:
        print("\n--- Library Menu ---")
        print("1. Search Books")
        print("2. Register Borrower")
        print("3. Update Fines")
        print("4. Display Fines")
        print("5. Pay Fines")
        print("6. Check Out Book")
        print("7. Check In Book")
        print("8. Exit")

        choice = input("Enter choice: ").strip()

        if choice == '1':
            keyword = input("Enter title, author, or ISBN: ").strip()
            results = search_books(keyword)
            for idx, row in enumerate(results, start=1):
                print(f"{idx:02}. {row['Isbn']} | {row['Title']} | {row['Authors']} | {row['Status']}")
        
        elif choice == '2':
            name = input("Borrower Name: ").strip()
            ssn = input("SSN (###-##-####): ").strip()
            address = input("Address: ").strip()
            phone = input("Phone: ").strip()
            response = create_borrower(name, ssn, address, phone)
            print(response)

        elif choice == '3':
            update_fines()
            print("Fines updated.")

        elif choice == '4':
            show_all = input("Show paid fines too? (y/n): ").strip().lower() == 'y'
            display_fines(show_all)

        elif choice == '5':
            card_id = input("Enter Card ID to pay fines: ").strip()
            pay_fines(card_id)

        elif choice == '6':
            # check out books
            isbn = input("Enter ISBN of the book to check out: ").strip()
            borrower_id = input("Enter Borrower ID: ").strip()
            checkout(isbn, borrower_id)

        elif choice == '7':
            # check in books
            isbn = input("Enter ISBN of the book to check in: ").strip()
            card_no = input("Enter Card ID: ").strip()
            name = input("Enter Borrower Name: ").strip()
            checkin(isbn, card_no, name)
        
        elif choice == '8':
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

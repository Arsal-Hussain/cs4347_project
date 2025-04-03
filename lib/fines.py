from lib.database import get_connection
from datetime import datetime, timedelta

def generate_test_data():
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO BOOK_LOANS (Isbn, Card_id, Date_out, Due_date) VALUES (?, ?, ?, ?)",
            ('0195153448', 'ID000009', '2025-04-01', '2025-04-15'))
        cursor.execute(
            "INSERT INTO BOOK_LOANS (Isbn, Card_id, Date_out, Due_date, Date_in) VALUES (?, ?, ?, ?, ?)",
            ('0425176428', 'ID000013', '2025-03-14', '2025-03-28', '2025-04-02'))
        cursor.execute(
            "INSERT INTO BOOK_LOANS (Isbn, Card_id, Date_out, Due_date, Date_in) VALUES (?, ?, ?, ?, ?)",
            ('0440234743', 'ID000013', '2025-03-14', '2025-03-28', '2025-04-02'))
        cursor.execute(
            "INSERT INTO BOOK_LOANS (Isbn, Card_id, Date_out, Due_date) VALUES (?, ?, ?, ?)",
            ('0393045218', 'ID000020', '2025-03-14', '2025-03-28'))
        cursor.execute(
            "INSERT INTO BOOK_LOANS (Isbn, Card_id, Date_out, Due_date, Date_in) VALUES (?, ?, ?, ?, ?)",
            ('1552041778', 'ID000012', '2025-03-14', '2025-03-28', '2025-03-31'))
        cursor.execute(
            "INSERT INTO BOOK_LOANS (Isbn, Card_id, Date_out, Due_date) VALUES (?, ?, ?, ?)",
            ('0671870432', 'ID000005', '2025-03-18', '2025-04-01'))
        conn.commit()
    except Exception as e:
        print(f"Initialization error: {e}")
        return []
    finally:
        conn.close()

def update_fines():
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        today = datetime.today().date()
        fine_rate = 0.25

        # Get overdue books that have been returned
        cursor.execute("SELECT Loan_id, Due_date, Date_in FROM BOOK_LOANS WHERE Date_in IS NOT NULL AND Date_in > Due_date")
        returned_loans = cursor.fetchall()

        # Get overdue books that are still out
        cursor.execute("SELECT Loan_id, Due_date FROM BOOK_LOANS WHERE Date_in IS NULL AND Due_date < ?", (today,))
        outstanding_loans = cursor.fetchall()
        #print(returned_loans)
        #print(outstanding_loans)

        # Update fines for returned books
        for loan_id, due_date, date_in in returned_loans:
            return_date = datetime.strptime(date_in, "%Y-%m-%d").date()
            date_due = datetime.strptime(due_date, "%Y-%m-%d").date()
            days_late = (return_date - date_due).days
            fine_amt = round(days_late * fine_rate, 2)

            cursor.execute("SELECT Paid FROM FINES WHERE Loan_id = ?", (loan_id,))
            existing_fine = cursor.fetchone()
            if existing_fine:
                if existing_fine[0] == 0:
                    cursor.execute("UPDATE FINES SET Fine_amt = ? WHERE Loan_id = ?", (fine_amt, loan_id))
            else:
                cursor.execute("INSERT INTO FINES (Loan_id, Fine_amt) VALUES (?, ?)", (loan_id, fine_amt))
        
        # Update fines for outstanding books
        for loan_id, due_date in outstanding_loans:
            date_due = datetime.strptime(due_date, "%Y-%m-%d").date()
            days_late = (today - date_due).days
            fine_amt = round(days_late * fine_rate, 2)

            cursor.execute("SELECT Paid FROM FINES WHERE Loan_id = ?", (loan_id,))
            existing_fine = cursor.fetchone()
            if existing_fine:
                if existing_fine[0] == 0: 
                    cursor.execute("UPDATE FINES SET Fine_amt = ? WHERE Loan_id = ?", (fine_amt, loan_id))
            else:
                cursor.execute("INSERT INTO FINES (Loan_id, Fine_amt) VALUES (?, ?)", (loan_id, fine_amt))

        conn.commit()
    except Exception as e:
        print(f"Error Updating Fines: {e}")
        return []
    finally:
        conn.close()

def display_fines(show_paid = False):
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()

        # Query for All Fines that are due by users with overdue books
        query = """SELECT B.Card_id, B.Bname, SUM(F.Fine_amt) FROM FINES F 
                   JOIN BOOK_LOANS BL ON F.Loan_id = BL.Loan_id 
                   JOIN BORROWER B ON BL.Card_id = B.Card_id 
                   WHERE F.Paid = 0 GROUP BY B.Card_id, B.Bname;"""
        # Option to include fines already paid
        if show_paid:
            query = query.replace("WHERE F.Paid = 0", "")

        cursor.execute(query)
        results = cursor.fetchall()
        
        # Print Fines
        print("Fines Due:")
        for card_id, name, total_fine in results:
            print(f"Borrower: {name} (Card ID: {card_id}) - Total Fine: ${total_fine:.2f}")
    except Exception as e:
        print(f"Error Displaying Fines: {e}")
        return []
    finally:
        conn.close()

def pay_fines(card_id):
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()

        # Query to get all fines currently due by user:
        # Paid = 0 and Date_in not NULL ensure only returned books whose overdue fines
        # are not paid are returned
        cursor.execute("""SELECT SUM(Fine_amt) FROM BOOK_LOANS B, FINES F 
                          WHERE F.Loan_id = B.Loan_id AND B.Card_id = ? 
                          AND Paid = 0 AND B.Date_in IS NOT NULL;""", (card_id,))
        result = cursor.fetchone()

        # If result has a fine, pay fine and update FINES Table, otherwise, do nothing
        if result and result[0] is not None:
            total_fine = result[0]
            cursor.execute("""UPDATE FINES SET Paid = 1 
                              WHERE Loan_id IN (SELECT B.Loan_id FROM FINES F, BOOK_LOANS B 
                              WHERE F.Loan_id = B.Loan_id AND B.Card_id = ? 
                              AND F.Paid = 0 AND B.Date_in IS NOT NULL);""", (card_id,))
            conn.commit()
            print(f"Member with Card ID: {card_id} has paid the total fine of: ${total_fine:.2f}")
        else:
            print("No outstanding fines detected at this time. Please ensure that all books previously checked out have been returned.")
    except Exception as e:
        print(f"Error Displaying Fines: {e}")
        return []
    finally:
        conn.close()
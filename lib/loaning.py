# deals with checkin and checkout

from lib.database import get_connection
from datetime import date, timedelta

def checkin(isbn=None, card_no=None, name=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = '''
        SELECT BOOK_LOANS.*, BOOK.Title, BORROWER.Bname
        FROM BOOK_LOANS
        JOIN BOOK ON BOOK_LOANS.Isbn = BOOK.Isbn
        JOIN BORROWER ON BOOK_LOANS.Card_id = BORROWER.Card_id
        WHERE Date_in IS NULL
    '''

    params = []

    if isbn:
        query += ' AND BOOK.Isbn = ?'
        params.append(isbn)
    if card_no:
        query += ' AND BORROWER.Card_id = ?'
        params.append(card_no)
    if name:
        query += ' AND BORROWER.Bname LIKE ?'
        params.append(f'%{name}%')

    query += ' LIMIT 3;'

    cursor.execute(query, params)
    checked_out_books = cursor.fetchall()

    if not checked_out_books:
        print("No matching checked-out books found.")
        return

    print("Checked out books:")
    for idx, row in enumerate(checked_out_books, start=1):
        print(f"{idx:02}. {row['Isbn']} | {row['Title']} | {row['Bname']} | {row['Date_out']} | {row['Due_date']}")

    conn.close()


def checkout(isbn, borrower_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Check active loans
    cursor.execute('''
        SELECT * FROM BOOK_LOANS
        WHERE Card_id = ? AND Date_in IS NULL;
    ''', (borrower_id,))
    if len(cursor.fetchall()) >= 3:
        print("ERROR: You have 3 active book loans.")
        conn.close()
        return

    # Check if book is already checked out
    cursor.execute('''
        SELECT * FROM BOOK_LOANS
        WHERE Isbn = ? AND Date_in IS NULL;
    ''', (isbn,))
    if cursor.fetchall():
        print("ERROR: This book is already checked out.")
        conn.close()
        return

    # Check unpaid fines
    cursor.execute('''
        SELECT * FROM FINES
        JOIN BOOK_LOANS ON FINES.Loan_id = BOOK_LOANS.Loan_id
        WHERE Card_id = ? AND Paid = 0;
    ''', (borrower_id,))
    if cursor.fetchall():
        print("ERROR: You have unpaid fines.")
        conn.close()
        return

    # Proceed with checkout
    today = date.today()
    due = today + timedelta(days=14)

    cursor.execute('''
        INSERT INTO BOOK_LOANS (Isbn, Card_id, Date_out, Due_date)
        VALUES (?, ?, ?, ?);
    ''', (isbn, borrower_id, today.isoformat(), due.isoformat()))

    # Also mark book as OUT in BOOK table
    cursor.execute('''
        UPDATE BOOK SET Status = 'OUT' WHERE Isbn = ?;
    ''', (isbn,))

    conn.commit()
    conn.close()
    print("Book checked out successfully.")

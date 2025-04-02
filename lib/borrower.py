# lib/borrower.py

from lib.database import get_connection


""" Example test case for borrowing add this snippet to the main to test 
response = create_borrower(
    name="Jane Doe",
    ssn="999887777",
    address="456 Oak St, Dallas, TX",
    phone="555-987-6543"
)

print(response)
"""
def generate_new_card_no():
    #Generate a new unique card_no by incrementing the max existing value
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(CAST(SUBSTR(card_id, 2) AS INTEGER)) AS max_id FROM BORROWER") #find the max card 
        result = cursor.fetchone()
        max_id = result["max_id"] if result["max_id"] is not None else 0
        new_id = max_id + 1
        return f'B{new_id:03}'
    except Exception as e:
        print(f"Error generating card_no: {e}")
        return None
    finally:
        conn.close()

#Create a new borrower if SSN is unique
def create_borrower(name, ssn, address, phone):
    
    if not all([name, ssn, address, phone]):
        return "Error: All fields (name, SSN, address, phone) are required."

    conn = get_connection()
    if not conn:
        return "Database connection failed."

    try:
        cursor = conn.cursor()

        # Check if SSN already exists
        cursor.execute("SELECT * FROM BORROWER WHERE ssn = ?", (ssn,))
        if cursor.fetchone():
            return "Error: A borrower with this SSN already exists."

        new_card_id = generate_new_card_no()
        if not new_card_id:
            return "Error generating new card number."


        cursor.execute("INSERT INTO BORROWER (card_id, bname, ssn, address, phone) VALUES (?, ?, ?, ?, ?)",
               (new_card_id, name, ssn, address, phone))


        conn.commit()
        return f"Success: Borrower created with Card ID {new_card_id}."
    except Exception as e:
        return f"Error creating borrower: {e}"
    finally:
        conn.close()

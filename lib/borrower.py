# lib/borrower.py

from lib.database import get_connection
import re

def normalize_ssn(ssn):
    """Strip all non-digit characters from SSN for comparison."""
    return re.sub(r'\D', '', ssn)

def generate_new_card_no():
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(CAST(SUBSTR(card_id, 3) AS INTEGER)) AS max_id FROM BORROWER")
        result = cursor.fetchone()
        max_id = result["max_id"] if result["max_id"] is not None else 0
        new_id = max_id + 1
        return f'ID{new_id:06}'
    except Exception as e:
        print(f"Error generating card_id: {e}")
        return None
    finally:
        conn.close()

def create_borrower(name, ssn, address, phone):
    if not all([name, ssn, address, phone]):
        return "Error: All fields (name, SSN, address, phone) are required."

    normalized_ssn = normalize_ssn(ssn)
    conn = get_connection()
    if not conn:
        return "Database connection failed."

    try:
        cursor = conn.cursor()

        # Fetch all existing SSNs and compare after normalization
        cursor.execute("SELECT ssn FROM BORROWER")
        existing_ssns = [normalize_ssn(row["ssn"]) for row in cursor.fetchall()]
        if normalized_ssn in existing_ssns:
            return "Error: A borrower with this SSN already exists."

        new_card_id = generate_new_card_no()
        if not new_card_id:
            return "Error generating new card number."

        cursor.execute(
            "INSERT INTO BORROWER (card_id, bname, ssn, address, phone) VALUES (?, ?, ?, ?, ?)",
            (new_card_id, name, ssn, address, phone)
        )

        conn.commit()
        return f"Success: Borrower created with Card ID {new_card_id}."
    except Exception as e:
        return f"Error creating borrower: {e}"
    finally:
        conn.close()

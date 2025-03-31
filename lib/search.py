# lib/search.py

from lib.database import get_connection

def search_books(keyword):
    """
    Search for books by ISBN, title, or author substring (case-insensitive).
    Returns a list of dicts with ISBN, Title, Authors, Status ("IN" or "OUT").
    """
    keyword = f"%{keyword.lower()}%"
    conn = get_connection()
    if not conn:
        return []

    query = """
    SELECT
        b.Isbn,
        b.Title,
        GROUP_CONCAT(a.Name, ', ') AS Authors,
        CASE
            WHEN EXISTS (
                SELECT 1 FROM BOOK_LOANS bl
                WHERE bl.Isbn = b.Isbn AND bl.Date_in IS NULL
            ) THEN 'OUT'
            ELSE 'IN'
        END AS Status
    FROM BOOK b
    JOIN BOOK_AUTHORS ba ON b.Isbn = ba.Isbn
    JOIN AUTHORS a ON ba.Author_id = a.Author_id
    WHERE LOWER(b.Isbn) LIKE ?
       OR LOWER(b.Title) LIKE ?
       OR LOWER(a.Name) LIKE ?
    GROUP BY b.Isbn, b.Title
    ORDER BY b.Title ASC;
    """

    try:
        cursor = conn.cursor()
        cursor.execute(query, (keyword, keyword, keyword))
        results = cursor.fetchall()
        return [dict(row) for row in results]
    except Exception as e:
        print(f"Search error: {e}")
        return []
    finally:
        conn.close()

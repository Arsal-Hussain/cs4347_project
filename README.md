# CS4347 Library Database Project

## 📚 Project Description
This project implements a simplified Library Management System using Python and SQLite. It supports:

- Searching books by title, author, or ISBN  
- Registering new borrowers  
- Checking out and checking in books  
- Managing and paying fines  

## 🛠️ Technologies Used

| Component        | Version     |
|------------------|-------------|
| Language         | Python 3.12 |
| Database         | SQLite 3    |
| IDE (Optional)   | VS Code     |

## 📦 Dependencies

No external libraries are required. The following built-in Python modules are used:

- `sqlite3`
- `datetime`

## 📁 Project Structure

```
cs4347_project/
│
├── main.py                # Entry point
├── lib/
│   ├── database.py        # DB connection setup
│   ├── search.py          # Book search logic
│   ├── borrower.py        # Borrower registration
│   ├── fines.py           # Fine logic
│   └── loaning.py         # Checkout/checkin logic
│
├── db/
│   ├── library.db         # SQLite DB file
│   ├── schema.sql         # Table schema
│   └── init_data.sql      # Initial data
```

## 🚀 Setup and Run Instructions

### 1. Prerequisites

- Python 3.12 installed  
- SQLite 3 installed (CLI or DB Browser)

### 2. Initialize the Database

Run the following from the `db` directory:

```bash
sqlite3 library.db < schema.sql
sqlite3 library.db < init_data.sql
```

If needed, add the `Status` column to the `BOOK` table:

```sql
ALTER TABLE BOOK ADD COLUMN Status TEXT DEFAULT 'IN';
```

### 3. Run the Program

From the root folder:

```bash
python main.py
```

## 📝 Notes

- Close DB Browser or any tool locking the `.db` file before running Python.
- Use parameterized queries to prevent SQL injection and locking issues.
- Book availability is tracked using a `Status` column in `BOOK`.

---

Developed for CS4347 – Database Systems  
Milestone 2 Submission
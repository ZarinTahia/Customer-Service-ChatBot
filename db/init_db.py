import sqlite3 #create and interact sqllite database
from pathlib import Path #manage path safely

DB_PATH = Path("db/customer_support.db")

def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH) #create database file of it's not there
    cur = conn.cursor() #execute sql command

    # Customers table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        city TEXT,
        created_at TEXT
    );
    """)

    # Support tickets table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        ticket_id INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL,
        subject TEXT NOT NULL,
        status TEXT NOT NULL,
        priority TEXT NOT NULL,
        created_at TEXT,
        last_update TEXT,
        resolution_summary TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    );
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
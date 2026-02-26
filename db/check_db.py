import sqlite3
from pathlib import Path

DB_PATH = Path("db/customer_support.db")

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    print("\n--- Customers ---")
    for row in cur.execute("SELECT customer_id, name, email, city FROM customers;"):
        print(row)

    print("\n--- Tickets (first 10) ---")
    for row in cur.execute("SELECT ticket_id, customer_id, subject, status, priority FROM tickets LIMIT 10;"):
        print(row)

    conn.close()

if __name__ == "__main__":
    main()
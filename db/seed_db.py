import sqlite3
from pathlib import Path

DB_PATH = Path("db/customer_support.db")

CUSTOMERS = [
    (1, "Ema Johnson", "ema.johnson@example.com", "+1-416-555-0101", "Toronto", "2025-10-05"),
    (2, "Noah Smith", "noah.smith@example.com", "+1-647-555-0199", "Mississauga", "2025-11-12"),
    (3, "Ava Patel", "ava.patel@example.com", "+1-519-555-0133", "London", "2026-01-08"),
    (5, "Zarin Tahia","zarin.hossain@uwo.ca","437-329-5207","Kitchener","2025-02-12")
]

TICKETS = [
    (101, 1, "Refund request for order #A1023", "Closed", "High", "2026-01-15", "2026-01-17",
     "Verified eligibility and processed refund to original payment method."),
    (102, 1, "Address change for shipment", "Closed", "Medium", "2026-02-02", "2026-02-02",
     "Updated shipping address before dispatch."),
    (103, 2, "Login issues after password reset", "Open", "High", "2026-02-20", "2026-02-24",
     "Escalated to engineering; temporary workaround provided."),
    (104, 3, "Billing clarification for subscription", "Pending", "Low", "2026-02-10", "2026-02-11",
     "Awaiting customer confirmation on plan details."),
]

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Insert customers (ignore if already exists)
    cur.executemany("""
        INSERT OR IGNORE INTO customers (customer_id, name, email, phone, city, created_at)
        VALUES (?, ?, ?, ?, ?, ?);
    """, CUSTOMERS)

    # Insert tickets (ignore if already exists)
    cur.executemany("""
        INSERT OR IGNORE INTO tickets (ticket_id, customer_id, subject, status, priority, created_at, last_update, resolution_summary)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, TICKETS)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
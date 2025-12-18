import sqlite3

def init_db():
    conn = sqlite3.connect("contacts.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            number TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()

    new_conn = sqlite3.connect("contacts.db")

    new_cursor = new_conn.cursor()

    rows = new_cursor.execute("SELECT name FROM sqlite_master")

    return rows.fetchone() is None
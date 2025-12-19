import sqlite3

DATABASE_FILENAME = 'contacts.db'

def init_db():

    with sqlite3.connect(DATABASE_FILENAME) as conn:
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

    return True

def get_contacts(page,limit):

    offset_rows = (page - 1) * limit

    with sqlite3.connect(DATABASE_FILENAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, number FROM contacts ORDER BY id ASC LIMIT ? OFFSET ?',(limit,offset_rows,))
        rows = cursor.fetchall()
    
    return map_rows_to_contacts(rows)

def count_contacts():

    with sqlite3.connect(DATABASE_FILENAME) as conn:
        cursor = conn.cursor()
        row = cursor.execute('SELECT COUNT(*) FROM contacts').fetchone()
    
    return row[0]

def get_contact_by_id(contact_id):

    with sqlite3.connect(DATABASE_FILENAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id,name,number FROM contacts WHERE id = ?', (contact_id,))
        row = cursor.fetchone()
    
    return map_values_to_contact(row) if row else None

def create_contact(name, number):

    with sqlite3.connect(DATABASE_FILENAME) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO contacts (name,number) VALUES(?,?)',(name,number,))
        conn.commit()
    
    return cursor.lastrowid

def update_contact(contact_id, name, number):

    with sqlite3.connect(DATABASE_FILENAME) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE contacts SET name = ?, number = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',(name, number, contact_id,))
        conn.commit()
    
    return cursor.rowcount > 0
    
def remove_contact(contact_id):

    with sqlite3.connect(DATABASE_FILENAME) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM contacts WHERE id = ?',(contact_id,))
        conn.commit()
    
    return cursor.rowcount > 0

def map_values_to_contact(row):

    if not row:
        return None

    contact = {
        'id' : int(row[0]),
        'name' : row[1],
        'number' : row[2]
    }

    return contact

def map_rows_to_contacts(rows):

    if not rows:
        return []

    contacts = []

    for row in rows:
        contact = map_values_to_contact(row)
        contacts.append(contact)

    return contacts
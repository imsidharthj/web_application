import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('form_data.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table for storing form data
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    contact_no TEXT NOT NULL,
    city TEXT NOT NULL
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

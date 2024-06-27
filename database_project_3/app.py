from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Connect to the database and create the table
def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")
    conn.execute('''
        CREATE TABLE IF NOT EXISTS participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            contact_no TEXT NOT NULL,
            city TEXT NOT NULL
        )
    ''')
    print("Table created successfully")
    conn.close()

init_sqlite_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        try:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            contact_no = request.form['contact_no']
            city = request.form['city']

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO participants (first_name, last_name, email, contact_no, city) VALUES (?, ?, ?, ?, ?)", 
                            (first_name, last_name, email, contact_no, city))
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "Error in insert operation"
        finally:
            return redirect(url_for('participants'))
            con.close()

@app.route('/participants')
def participants():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM participants")
    rows = cur.fetchall()
    return render_template('participants.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Function to insert form data into the database
def insert_data(first_name, last_name, email, contact_no, city):
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO users (first_name, last_name, email, contact_no, city)
    VALUES (?, ?, ?, ?, ?)
    ''', (first_name, last_name, email, contact_no, city))
    conn.commit()
    conn.close()

# Route to display the form
@app.route('/')
def form():
    return render_template_string()

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    contact_no = request.form['contact_no']
    city = request.form['city']
    insert_data(first_name, last_name, email, contact_no, city)
    return 'Form submitted successfully!'

if __name__ == '__main__':
    app.run(debug=True)

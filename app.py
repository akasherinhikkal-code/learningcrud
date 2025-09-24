from flask import Flask, render_template, request, redirect, url_for
from database import get_connection, create_table

app = Flask(__name__)
create_table()

@app.route('/')
def index():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()
    conn.close()
    return render_template('index.html', contacts=contacts)

@app.route('/add', methods=['GET','POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        conn = get_connection()
        conn.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
                     (name, phone, email))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:contact_id>', methods=['GET','POST'])
def edit_contact(contact_id):
    conn = get_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        cursor.execute("UPDATE contacts SET name=?, phone=?, email=? WHERE id=?",
                       (name, phone, email, contact_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        cursor.execute("SELECT * FROM contacts WHERE id=?", (contact_id,))
        contact = cursor.fetchone()
        conn.close()
        return render_template('edit.html', contact=contact)

@app.route('/delete/<int:contact_id>')
def delete_contact(contact_id):
    conn = get_connection()
    conn.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)

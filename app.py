from flask import Flask, request, redirect, url_for, render_template
import sqlite3

app = Flask(__name__)

# SQLite3 setup
def init_sqlite_db():
    conn = sqlite3.connect('users.db')
    conn.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, firstname TEXT, lastname TEXT, email TEXT)')
    conn.close()

init_sqlite_db()

@app.route('/')
def home():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']

    with sqlite3.connect('users.db') as con:
        cur = con.cursor()
        cur.execute("INSERT INTO users (username, password, firstname, lastname, email) VALUES (?, ?, ?, ?, ?)",
                    (username, password, firstname, lastname, email))
        con.commit()

    return redirect(url_for('success', firstname=firstname, lastname=lastname, email=email))

@app.route('/success')
def success():
    firstname = request.args.get('firstname')
    lastname = request.args.get('lastname')
    email = request.args.get('email')
    return f"Welcome, {firstname} {lastname}. Your email is {email}"

if __name__ == '__main__':
    app.run(host='0.0.0.0')

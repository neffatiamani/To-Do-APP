from flask import Flask, render_template, request, session, redirect
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "1025")
load_dotenv()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Lina&mimi2706'
app.config['MYSQL_DB'] = 'mydatabase'

mysql = MySQL(app)

@app.route('/')
def home():
    if 'username' in session:
        # Get the user's to-do list
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE id=%s", [session['id']])
        tasks = cur.fetchall()
        cur.close()
        return render_template('home.html', tasks=tasks)
    else:
        return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cur.fetchone()
        cur.close()
        if user:
            session['username'] = username
            session['id'] = user[0]
            return redirect('/')
        else:
            return render_template('login.html', error='Invalid login')
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s", [username])
        user = cur.fetchone()
        if user:
            return render_template('register.html', error='Username already taken')
        else:
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            mysql.connection.commit()
            cur.close()
            return redirect('/login')
    else:
        return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('id', None)
    return redirect('/')

@app.route('/profile')
def profile():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE id=%s", [session['id']])
        user = cur.fetchone()
        cur.close()
        return render_template('profile.html', user=user)
    else:
        return redirect('/login')


@app.route('/add', methods=['POST'])
def add_task():
    if request.method == 'POST':
        task = request.form['task']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tasks (user_id, task) VALUES (%s, %s)", (session['id'], task))
        mysql.connection.commit()
        cur.close()
    return redirect('/')

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'username' in session:
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            cur = mysql.connection.cursor()
            cur.execute("UPDATE users SET name=%s, email=%s WHERE id=%s", (name, email, session['id']))
            mysql.connection.commit()
            cur.close()
            return redirect('/profile')
        else:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE id=%s", [session['id']])
            user = cur.fetchone()
            cur.close()
            return render_template('edit_profile.html', user=user)
    else:
        return redirect('/login')



if __name__ == '__main__':
    app.run(debug=True)

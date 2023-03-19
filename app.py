from flask import Flask, render_template, request, session, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "1025"  # Replace with a secure key
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Lina&mimi2706'  # Replace with your MySQL password
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
            session['id'] = user[1]
            return redirect('/')
        else:
            return render_template('login.html', error='Invalid login')
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect('/')


@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tasks (user_id, task) VALUES (%d, %s)", (int(session['user_id']), task))
    mysql.connection.commit()
    cur.close()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)

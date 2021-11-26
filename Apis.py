from flask import Flask, jsonify, request, render_template, redirect, url_for, session
import mysql.connector, sys, os, webbrowser
import requests, signal
from dao import close, DB
import datetime, time
from mysql.connector import Error
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import uuid

id = uuid.uuid4()

app = Flask(__name__, static_url_path='/templates/static')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.environ.get("Pass")
app.config['MYSQL_DB'] = 'CricStats'

mysql = MySQL(app)

@app.route('/app/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE userName = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['userId']
            session['username'] = account['userName']
            msg = 'Logged in successfully !'
            return render_template('index.html', isLoggedIn=True)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html')

@app.route('/app/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/app/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE userName = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO users VALUES (%s, %s, %s, %s)', (id, username, email, password))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html')

# signal
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    close()
    sys.exit(0)

# Home page that returns an html page !!
@app.route('/app')
def home_page():
    try:
        logIn = session["loggedin"]
    except KeyError:
        logIn = False
    return render_template('index.html', isLoggedIn=logIn)

# Login page that returns an html page !!
@app.route('/app/loginPage')
def login_page():
    return render_template('login.html')

# Register page that returns an html page !!
@app.route('/app/registerPage')
def register_page():
    return render_template('register.html')

# Series page
@app.route('/app/series')
def series_page():
    try:
        logIn = session["loggedin"]
    except KeyError:
        logIn = False
    return render_template('series.html', isLoggedIn=logIn)

# Series cat page
@app.route('/app/series_cat')
def seriesCat_page():
    try:
        logIn = session["loggedin"]
    except KeyError:
        logIn = False
    return render_template('series_cat.html', isLoggedIn=logIn)

# Fixtures Page
@app.route('/app/fixtures')
def fixtures_page():
    try:
        logIn = session["loggedin"]
    except KeyError:
        logIn = False
    return render_template('fixtures.html', isLoggedIn=logIn)

# results Page
@app.route('/app/results')
def results_page():
    try:
        logIn = session["loggedin"]
    except KeyError:
        logIn = False
    return render_template('results.html', isLoggedIn=logIn)

if __name__ == '__main__':
    app.secret_key = DB.secretKey
    # signal to close the DB connection
    signal.signal(signal.SIGINT, signal_handler)
    app.run(port=5000, debug=False)

# Working on Heroku without DB interactions
# port = int(os.environ.get("PORT", 5001))
# app.run(host='0.0.0.0', port=port)
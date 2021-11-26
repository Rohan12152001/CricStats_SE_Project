from flask import Flask, jsonify, request, render_template, redirect, url_for
import mysql.connector, sys, os, webbrowser
import requests, signal
from dao import close, DB
import datetime, time
from mysql.connector import Error

app = Flask(__name__)

# signal
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    close()
    sys.exit(0)

# Home page that returns an html page !!
@app.route('/app')
def home_page():
    return render_template('Home.html')

if __name__ == '__main__':
    app.secret_key = DB.secretKey
    # signal to close the DB connection
    signal.signal(signal.SIGINT, signal_handler)
    app.run(port=5000, debug=False)

# Working on Heroku without DB interactions
# port = int(os.environ.get("PORT", 5001))
# app.run(host='0.0.0.0', port=port)
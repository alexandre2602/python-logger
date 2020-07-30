import requests, sqlite3
from os import environ
from flask import Flask, request, make_response, jsonify

app = Flask(__name__)
app.url_map.strict_slashes = False

conn = sqlite3.connect('logger.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
if not c.fetchone():
    c.execute('CREATE TABLE logs ')
    print('ok')

@app.route('/find')
def find():
    pass

@app.route('/insert', methods=['POST'])
def insert():
    pass

@app.route('/delete')
def delete():
    pass

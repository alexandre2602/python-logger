import requests, sqlite3
from os import environ
from flask import Flask, request, make_response, jsonify

app = Flask(__name__)
app.url_map.strict_slashes = False

con = sqlite3.connect('logger.db')
c = con.cursor()
try:
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = 'logs'")
    if not c.fetchone():
        con.execute('CREATE TABLE logs (data REAL, texto TEXT)')
finally:
    c.close()
    con.close()

@app.route('/find')
def find():
    pass

@app.route('/insert', methods=['POST'])
def insert():

    try:
        data = request.get_json()
        if not data or 'data' not in data or 'texto' not in data:
            raise Exception("Especifique as propriedades 'data' e 'texto'")
    except Exception as e:
        return make_response(jsonify({'message' : str(e)}), 400)

    con = sqlite3.connect('logger.db')
    try:
        con.execute('INSERT INTO logs (data, texto) VALUES (?, ?)', (data['data'], data['texto']))
        con.commit()
    except Exception as e:
        return make_response(jsonify({'message' : str(e)}), 500)
    finally:
        con.close()

    return jsonify({'message' : 'Log inserido'})

@app.route('/delete')
def delete():
    pass

#!/usr/bin/env python3

import requests, sqlite3, time

from os import environ
from functools import wraps
from datetime import datetime, timedelta
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

def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = requests.get('{}/check'.format(environ['AUTH_HOST']), headers={'Authorization' : request.headers['Authorization']})
        if response.status_code != 200:
            return make_response(jsonify(response.json()), 500)
        return f(*args, **kwargs)
    return decorated_function

@app.route('/find/')
@app.route('/find/<date>')
def find(date=None):
    if not date and not ('ini' in request.args or 'end' in request.args):
        return make_response(jsonify({'message' : "Especifique 'date' ou ini/end na query string"}), 400)

    if date:

        try:
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            date = datetime.strptime(date, '%Y-%m-%d')

        date_ini = date + timedelta(seconds=-1)
        date_end = date + timedelta(seconds=1)
    else:
        try:
            date_ini = datetime.strptime(request.args['ini'], '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            date_ini = datetime.strptime(request.args['ini'], '%Y-%m-%d')
        try:
            date_end = datetime.strptime(request.args['end'], '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            date_end = datetime.strptime(request.args['end'], '%Y-%m-%d')

    con = sqlite3.connect('logger.db')
    c = con.cursor()
    try:
        logs = []
        #print("SELECT * FROM logs WHERE data BETWEEN '{}' AND '{}'".format(date + timedelta(seconds=-1), date + timedelta(seconds=1)))
        for row in c.execute("SELECT * FROM logs WHERE data BETWEEN ? AND ?", (date_ini, date_end)):
            logs.append({'data' : row[0], 'texto': row[1]})
    finally:
        c.close()
        con.close()

    return jsonify(logs)

@app.route('/insert', methods=['POST'])
@jwt_required
def insert():

    try:
        data = request.get_json()
        if not data or 'data' not in data or 'texto' not in data:
            raise Exception("Especifique as propriedades 'data' e 'texto'")
    except Exception as e:
        return make_response(jsonify({'message' : str(e)}), 400)

    try:
        date = datetime.strptime(data['data'], '%Y-%m-%d %H:%M:%S')
    except Exception as e:
        date = datetime.strptime(date['data'], '%Y-%m-%d')

    con = sqlite3.connect('logger.db')
    try:
        con.execute('INSERT INTO logs (data, texto) VALUES (?, ?)', (date, data['texto']))
        con.commit()
    except Exception as e:
        return make_response(jsonify({'message' : str(e)}), 500)
    finally:
        con.close()

    return jsonify({'message' : 'Log inserido'})

@app.route('/remove/', methods=['DELETE'])
@app.route('/remove/<date>', methods=['DELETE'])
@jwt_required
def remove(date=None):
    if not date and not ('ini' in request.args or 'end' in request.args):
        return make_response(jsonify({'message' : "Especifique 'date' ou ini/end na query string"}), 400)

    if date:

        try:
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            date = datetime.strptime(date, '%Y-%m-%d')

        date_ini = date + timedelta(seconds=-1)
        date_end = date + timedelta(seconds=1)
    else:
        try:
            date_ini = datetime.strptime(request.args['ini'], '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            date_ini = datetime.strptime(request.args['ini'], '%Y-%m-%d')
        try:
            date_end = datetime.strptime(request.args['end'], '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            date_end = datetime.strptime(request.args['end'], '%Y-%m-%d')

    con = sqlite3.connect('logger.db')
    try:
        con.execute("DELETE FROM logs WHERE data BETWEEN ? AND ?", (date_ini, date_end))
        con.commit()
    except:
        return make_response(jsonify({'message' : 'Problemas ao remover os registros'}), 500)
    finally:
        con.close()

    return jsonify({'message' : 'Registros removidos'})

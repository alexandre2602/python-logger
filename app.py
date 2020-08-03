#!/usr/bin/env python3

import requests, sqlite3, time

from os import environ
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
        # implementar lógica da verificação do JWT
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

    # abrir conexão
    # criar array de logs
    # fazer consulta populando o array com um objeto {'data': '', 'texto' : ''} e seus respectivos valores
    # retornar o arrauy, mesmo que vazio


@app.route('/insert', methods=['POST'])
# adicionar decorator
def insert():

    # verificar JWT

    try:
        data = None # capturar o JSON da requisição
        if not data or 'data' not in data or 'texto' not in data:
            raise Exception("Especifique as propriedades 'data' e 'texto'")
    except Exception as e:
        return make_response(jsonify({'message' : str(e)}), 400)

    try:
        date = datetime.strptime(data['data'], '%Y-%m-%d %H:%M:%S')
    except Exception as e:
        date = datetime.strptime(date['data'], '%Y-%m-%d')

    # abrir conexão
    # inserir loga, commit
    # retornar mensagem de sucesso ou
    # mensagem de erro caso ocorra algum problema

@app.route('/remove/', methods=['DELETE'])
@app.route('/remove/<date>', methods=['DELETE'])
# adicionar decorator
def remove(date=None):
    
    # verificar JWT

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

    # abrir conexão
    # remover registros
    # retornar mensagem de sucesso

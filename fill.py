#!/usr/bin/env python3

from faker import Faker
import requests, sqlite3
from datetime import datetime, timezone

con = sqlite3.connect('logger.db')
c = con.cursor()
try:
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = 'logs'")
    if not c.fetchone():
        con.execute('CREATE TABLE logs (data TEXT, texto TEXT)')
finally:
    c.close()

faker = Faker()

for i in range(1, 1000):
  con.execute('INSERT INTO logs (data, texto) VALUES (?, ?)', (datetime.utcnow(), faker.text()))

con.commit()
con.close()    

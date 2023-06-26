import json
import sqlite3


with open('logs.json') as logs_file:
    data = json.load(logs_file)


columns = []
for item in data:
    ip = item.split(' - - ')[0]
    time = item.split('[')[1].split(']')[0]
    code = item.split('" ')[1].split(' ')[0]
    dan = item.split('"')[len(item.split('"'))-2]
    columns.append((ip, time, code, dan))


conn = sqlite3.connect('logs.db')
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS log
             (ip TEXT, time TEXT, code TEXT, dan TEXT)''')


c.executemany('INSERT INTO log VALUES (?, ?, ?, ?)', columns)


conn.commit()
conn.close()

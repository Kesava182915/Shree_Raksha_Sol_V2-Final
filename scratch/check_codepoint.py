import sqlite3, json
conn = sqlite3.connect('sreeraksha.db')
cur = conn.execute("SELECT data_json FROM app_store WHERE key = 'main_data'")
row = cur.fetchone()
d = json.loads(row[0])
t = d['estimates'][0]['terms']
print('First char code point:', ord(t[0]))
assert ord(t[0]) == 8226
print('Confirmed: First char is valid unicode bullet • (8226)')
conn.close()


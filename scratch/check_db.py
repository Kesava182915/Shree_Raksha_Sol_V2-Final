import sqlite3
import json

conn = sqlite3.connect('sreeraksha.db')
c = conn.cursor()
c.execute("SELECT key, length(data_json), updated_at FROM app_store")
print("app_store entries:", c.fetchall())

c.execute("SELECT data_json FROM app_store WHERE key = 'main_data'")
row = c.fetchone()
if row:
    d = json.loads(row[0])
    print("main_data estimates count:", len(d.get('estimates', [])))
    print("main_data invoices count:", len(d.get('invoices', [])))
else:
    print("main_data not found!")

c.execute("SELECT COUNT(*) FROM quotations")
print("quotations table count:", c.fetchone()[0])
c.execute("SELECT COUNT(*) FROM invoices")
print("invoices table count:", c.fetchone()[0])
c.execute("SELECT COUNT(*) FROM email_logs")
print("email_logs table count:", c.fetchone()[0])

conn.close()

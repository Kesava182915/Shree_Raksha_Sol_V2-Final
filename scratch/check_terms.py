import sqlite3, json

conn = sqlite3.connect('sreeraksha.db')
cur = conn.execute("SELECT data_json FROM app_store WHERE key = 'main_data'")
row = cur.fetchone()
if row:
    d = json.loads(row[0])
    print('Org defaultTerms:\n', d.get('org', {}).get('defaultTerms'))
    invoices = d.get('invoices', [])
    for inv in invoices:
        print(f"Invoice {inv.get('number')} terms:\n", inv.get('terms'))
    estimates = d.get('estimates', [])
    for est in estimates:
        print(f"Estimate {est.get('number')} terms:\n", est.get('terms'))


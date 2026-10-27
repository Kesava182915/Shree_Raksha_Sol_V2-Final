import sqlite3
import json

conn = sqlite3.connect('sreeraksha.db')
c = conn.cursor()
c.execute("SELECT data_json FROM app_store WHERE key = 'main_data'")
data = json.loads(c.fetchone()[0])
org = data.get('organization', {})
for k in ['bankName', 'accountName', 'accountNumber', 'branch', 'ifscCode', 'bankDetails']:
    print(k, ':', repr(org.get(k)))

# Also check customer ids for invoices
invoices = data.get('invoices', [])
print("\nInvoices customer IDs:")
for inv in invoices:
    print(inv['id'], inv['number'], 'customerId:', repr(inv.get('customerId')))

customers = data.get('customers', [])
print("\nCustomers:")
for cust in customers:
    print(cust['id'], repr(cust.get('name')))

conn.close()

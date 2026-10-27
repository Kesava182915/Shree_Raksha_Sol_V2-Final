import sqlite3
import json

std_terms = """• Above prices are FOR Destination.
• Please mention our Estimate number on all future correspondence.
• Please share your valid GSTIN in your Purchase Order.
• Payment Terms: As agreed (30 Days net).
• In case of Refurbished requirement
  * The defective part need to be returned - against delivery.
• Delivery will be within 3-4 weeks from date of PO.
  * Goods indicated above in stock are accurate as of the quote date.
  * If goods are out of stock at the time of release of PO, standard lead time would apply.
• Payment will be 50% advance and balance against delivery."""

# Clean default_data.json
with open('default_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

if 'organization' in data:
    data['organization']['defaultTerms'] = std_terms

for col in ['invoices', 'estimates', 'purchaseOrders', 'debitCreditNotes']:
    if col in data:
        for item in data[col]:
            t = item.get('terms', '')
            if not t or '\ufffd' in t or 'Above prices' in t or 'Payment due' in t or 'Payment 30' in t:
                item['terms'] = std_terms

with open('default_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print("Updated default_data.json with clean UTF-8 terms.")

# Update sreeraksha.db
conn = sqlite3.connect('sreeraksha.db')
cur = conn.execute("SELECT data_json FROM app_store WHERE key = 'main_data'")
row = cur.fetchone()
if row:
    db_data = json.loads(row[0])
    if 'organization' in db_data:
        db_data['organization']['defaultTerms'] = std_terms
    for col in ['invoices', 'estimates', 'purchaseOrders', 'debitCreditNotes']:
        if col in db_data:
            for item in db_data[col]:
                t = item.get('terms', '')
                if not t or '\ufffd' in t or 'Above prices' in t or 'Payment due' in t or 'Payment 30' in t:
                    item['terms'] = std_terms
    conn.execute("UPDATE app_store SET data_json = ? WHERE key = 'main_data'", (json.dumps(db_data, ensure_ascii=False),))
    conn.commit()
    print("Updated sreeraksha.db with clean UTF-8 terms.")
conn.close()


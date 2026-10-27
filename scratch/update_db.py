import sqlite3
import json
from datetime import datetime

DB_PATH = 'sreeraksha.db'

def update():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    with conn:
        cur = conn.execute("SELECT data_json FROM app_store WHERE key = 'main_data'")
        row = cur.fetchone()
        if not row:
            print("No main_data found in app_store!")
            return

        data = json.loads(row['data_json'])
        org = data.setdefault('organization', {})
        org['bankName'] = 'State Bank of India'
        org['accountName'] = 'SHREERAKSHA SOLUTIONS'
        org['accountNumber'] = '45666081503'
        org['branch'] = 'PARKALA'
        org['ifscCode'] = 'SBIN0016869'
        org['proformaPrefix'] = 'SHRKS/PI/26-27/'
        org['bankDetails'] = (
            "Bank Name:\tState Bank of India\n"
            "Name of the Account:\tSHREERAKSHA SOLUTIONS\n"
            "Account number:\t45666081503\n"
            "Branch Name:\tPARKALA\n"
            "Branch IFSC:\tSBIN0016869"
        )

        with open('default_data.json', 'r', encoding='utf-8') as f:
            default_data = json.load(f)

        existing_custs = data.setdefault('customers', [])
        existing_ids = {c.get('id') for c in existing_custs}

        for dc in default_data.get('customers', []):
            if dc['id'] not in existing_ids:
                existing_custs.append(dc)
                existing_ids.add(dc['id'])

        existing_notes = data.setdefault('debitCreditNotes', [])
        if len(existing_notes) == 0:
            data['debitCreditNotes'] = default_data.get('debitCreditNotes', [])
            print("Seeded debitCreditNotes count:", len(data['debitCreditNotes']))

        now_iso = datetime.now().isoformat()
        conn.execute(
            "UPDATE app_store SET data_json = ?, updated_at = ? WHERE key = 'main_data'",
            (json.dumps(data, indent=2), now_iso)
        )
        print("Updated main_data in app_store! Total customers:", len(existing_custs))
        print("Updated org bank:", org['bankName'], org['accountNumber'], org['branch'])

if __name__ == '__main__':
    update()

import json
import sqlite3
import os

STANDARD_TERMS = (
    "• Above prices are FOR Destination.\n"
    "• Please mention our Estimate number on all future correspondence.\n"
    "• Please share your valid GSTIN in your Purchase Order.\n"
    "• Payment Terms: As agreed (30 Days net).\n"
    "• In case of Refurbished requirement\n"
    "  * The defective part need to be returned - against delivery.\n"
    "• Delivery will be within 3-4 weeks from date of PO.\n"
    "  * Goods indicated above in stock are accurate as of the quote date.\n"
    "  * If goods are out of stock at the time of release of PO, standard lead time would apply.\n"
    "• Payment will be 50% advance and balance against delivery."
)

# 1. Update default_data.json
print("Updating default_data.json...")
with open('default_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

if 'org' in data:
    data['org']['defaultTerms'] = STANDARD_TERMS

for est in data.get('estimates', []):
    est['terms'] = STANDARD_TERMS

for inv in data.get('invoices', []):
    # Only keep custom DC / PI terms if specific, or restore standard
    if inv.get('invoiceType') == 'tax_invoice' or not inv.get('invoiceType'):
        inv['terms'] = STANDARD_TERMS

with open('default_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print("default_data.json updated successfully!")

# 2. Update sreeraksha.db
print("Updating sreeraksha.db...")
conn = sqlite3.connect('sreeraksha.db')
with conn:
    cur = conn.execute("SELECT data_json FROM app_store WHERE key = 'main_data'")
    row = cur.fetchone()
    if row:
        db_data = json.loads(row[0])
        if 'org' in db_data:
            db_data['org']['defaultTerms'] = STANDARD_TERMS
        for est in db_data.get('estimates', []):
            est['terms'] = STANDARD_TERMS
        for inv in db_data.get('invoices', []):
            if inv.get('invoiceType') == 'tax_invoice' or not inv.get('invoiceType'):
                inv['terms'] = STANDARD_TERMS
        conn.execute("UPDATE app_store SET data_json = ?, updated_at = datetime('now') WHERE key = 'main_data'",
                     (json.dumps(db_data, ensure_ascii=False),))
        print("sreeraksha.db updated successfully!")
conn.close()

# 3. Update js/components/gst-document-template.js
print("Updating js/components/gst-document-template.js...")
with open('js/components/gst-document-template.js', 'r', encoding='utf-8') as f:
    tmpl_code = f.read()

target_terms = """    renderTermsList(termsStr, paymentTerms) {
      if (!termsStr || !String(termsStr).trim()) {
        const payTerm = paymentTerms || '30 Days net';
        return `
          <li>Above prices are FOR Destination.</li>
          <li>Please mention our Estimate number on all future correspondence.</li>
          <li>Please share your valid GSTIN in your Purchase Order.</li>
          <li>Payment Terms: As agreed (${payTerm}).</li>
          <li>In case of Refurbished requirement</li>
          <li class="sr-sub-bullet">The defective part need to be returned - against delivery.</li>
          <li>Delivery will be within 3-4 weeks from date of PO.</li>
          <li class="sr-sub-bullet">Goods indicated above in stock are accurate as of the quote date.</li>
          <li class="sr-sub-bullet">If goods are out of stock at the time of release of PO, standard lead time would apply.</li>
          <li>Payment will be 50% advance and balance against delivery.</li>
        `;
      }"""

replacement_terms = """    renderTermsList(termsStr, paymentTerms) {
      const payTerm = paymentTerms || '30 Days net';
      const defaultTermsHtml = `
        <li>Above prices are FOR Destination.</li>
        <li>Please mention our Estimate number on all future correspondence.</li>
        <li>Please share your valid GSTIN in your Purchase Order.</li>
        <li>Payment Terms: As agreed (${payTerm}).</li>
        <li>In case of Refurbished requirement</li>
        <li class="sr-sub-bullet">The defective part need to be returned - against delivery.</li>
        <li>Delivery will be within 3-4 weeks from date of PO.</li>
        <li class="sr-sub-bullet">Goods indicated above in stock are accurate as of the quote date.</li>
        <li class="sr-sub-bullet">If goods are out of stock at the time of release of PO, standard lead time would apply.</li>
        <li>Payment will be 50% advance and balance against delivery.</li>
      `;

      if (!termsStr || !String(termsStr).trim()) {
        return defaultTermsHtml;
      }

      const str = String(termsStr).trim();
      // If terms contains corrupted characters or previous merged 4-line snippet or short placeholder, restore original terms
      if (str.includes('\\ufffd') || str.includes('Above prices are FOR Destination &') || str === 'Payment due within 30 days.' || str === 'Payment 30 Days Net from date of installation.' || str === 'Payment due within 30 days of invoice receipt.' || str === 'Payment 30 Days Net from date of delivery.') {
        return defaultTermsHtml;
      }"""

if target_terms in tmpl_code:
    tmpl_code = tmpl_code.replace(target_terms, replacement_terms, 1)
    with open('js/components/gst-document-template.js', 'w', encoding='utf-8') as f:
        f.write(tmpl_code)
    print("js/components/gst-document-template.js updated successfully!")
else:
    print("target_terms not found in js/components/gst-document-template.js")

# 4. Update js/store.js
print("Updating js/store.js...")
with open('js/store.js', 'r', encoding='utf-8') as f:
    store_code = f.read()

# Replace corrupted characters in store.js if any
store_code = store_code.replace("description: '250mmx4.6mm, 5m'", "description: '250mmx4.6mm, 5μm'")
store_code = store_code.replace("description: '250mm x 4.6mm, 5m'", "description: '250mm x 4.6mm, 5μm'")
store_code = store_code.replace("description: '250mm x 4.6mm, 5m base-deactivated analytical column'", "description: '250mm x 4.6mm, 5μm base-deactivated analytical column'")
store_code = store_code.replace("description: '250mm x 4.6mm, 5m (Material dispatch under Delivery Challan)'", "description: '250mm x 4.6mm, 5μm (Material dispatch under Delivery Challan)'")

with open('js/store.js', 'w', encoding='utf-8') as f:
    f.write(store_code)
print("js/store.js updated successfully!")

print("\n--- ALL FILES RESTORED SUCCESSFULLY ---")


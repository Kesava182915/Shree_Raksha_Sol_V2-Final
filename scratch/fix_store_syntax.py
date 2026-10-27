with open('js/store.js', 'r', encoding='utf-8') as f:
    c = f.read()

import re

# Fix defaultNotes and defaultTerms in js/store.js
pattern = r"defaultNotes:\s*['\"].*?name:\s*'GST 18%',\s*rate:\s*18\.0\s*\},"
replacement = """defaultNotes: 'Order to be placed on "Shreeraksha Solutions" & Below Address mentioned',
      defaultTerms: '• Above prices are FOR Destination.\\n• Please mention our Estimate number on all future correspondence.\\n• Please share your valid GSTIN in your Purchase Order.\\n• Payment Terms: As agreed (30 Days net).\\n• In case of Refurbished requirement\\n  * The defective part need to be returned - against delivery.\\n• Delivery will be within 3-4 weeks from date of PO.\\n  * Goods indicated above in stock are accurate as of the quote date.\\n  * If goods are out of stock at the time of release of PO, standard lead time would apply.\\n• Payment will be 50% advance and balance against delivery.'
    },
    taxes: [
      { id: 'tax-18', name: 'GST 18%', rate: 18.0 },"""

c, count = re.subn(pattern, replacement, c, flags=re.DOTALL)
print(f"Replacement count: {count}")

with open('js/store.js', 'w', encoding='utf-8') as f:
    f.write(c)
print("Saved js/store.js cleanly!")


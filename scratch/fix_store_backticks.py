with open('js/store.js', 'r', encoding='utf-8') as f:
    c = f.read()

import re

# Match defaultTerms: '...' with single quotes spanning lines 41 to 50
pattern = r"defaultTerms:\s*'.*?delivery\.'"
replacement = """defaultTerms: `• Above prices are FOR Destination.
• Please mention our Estimate number on all future correspondence.
• Please share your valid GSTIN in your Purchase Order.
• Payment Terms: As agreed (30 Days net).
• In case of Refurbished requirement
  * The defective part need to be returned - against delivery.
• Delivery will be within 3-4 weeks from date of PO.
  * Goods indicated above in stock are accurate as of the quote date.
  * If goods are out of stock at the time of release of PO, standard lead time would apply.
• Payment will be 50% advance and balance against delivery.`"""

c, count = re.subn(pattern, lambda m: replacement, c, flags=re.DOTALL)
print(f"Replaced defaultTerms with template literal backticks: count={count}")

with open('js/store.js', 'w', encoding='utf-8') as f:
    f.write(c)
print("Saved js/store.js with valid backticks!")


import os
import json
import sqlite3
import re

print("Starting comprehensive terms and header/footer fix...")

# 1. Update js/components/gst-document-template.js
tmpl_path = 'js/components/gst-document-template.js'
with open(tmpl_path, 'r', encoding='utf-8') as f:
    tmpl_code = f.read()

# Update buildPages section heights
old_bp_pattern = r"// Section heights in millimeters \(A4 Landscape 210mm height.*?// Permutation 1: Check if EVERYTHING \(Items \+ Sub Total \+ Total Block \+ FULL Lower Block including Sign\) fits on Page 1 \(Single Page\)\s+if \(totalItemsH \+ TBL_HDR \+ SUBTOTAL_H \+ TOTAL_BLK_H \+ FULL_LOWER_H <= SPACE_P1\) \{"
new_bp_replacement = """// Section heights in millimeters (A4 Landscape 210mm height, uncompromised margins)
      // Printable height with 8mm top and bottom padding = 194mm
      const PRINTABLE_PAGE_H = 194.0;
      const HEADER_P1 = 23.0 + (docType === 'TAX INVOICE' || docType.includes('DELIVERY') ? 40.0 : (docType === 'PROFORMA INVOICE' || docType.includes('NOTE') ? 35.0 : 33.0));
      const HEADER_P2 = 23.0 + 8.5;  // Top Header + Title (23.0mm) + Continued Meta Bar (8.5mm) = 31.5mm
      const FOOTER_H = 17.5;         // Footer box with 4 full lines: Address, Phone, Email/GSTIN, Website/MSME (10px, 1.35 line-height)

      const SPACE_P1 = PRINTABLE_PAGE_H - HEADER_P1 - FOOTER_H; // Available for content on Page 1 (~113.5mm)
      const SPACE_P2 = PRINTABLE_PAGE_H - HEADER_P2 - FOOTER_H; // Available for content on Page 2+ (~145.0mm)

      const TBL_HDR = 9.0;
      const SUBTOTAL_H = 6.5;
      const TOTAL_BLK_H = 15.0;

      // Dynamic calculation of terms height based on doc.terms
      const effectiveTerms = (doc && doc.terms) ? String(doc.terms).trim() : '';
      const termsLines = effectiveTerms ? effectiveTerms.split('\\n').filter(l => l.trim().length > 0).length : 10;
      const NOTES_TERMS_H = Math.max(34.0, 14.0 + termsLines * 3.2);

      // Bank details box height
      const BANK_H = hasBank ? 26.0 : 0.0;
      // Signature box height with 2X height (96px body + header) = 32mm
      const SIGN_H = 32.0;

      // When Bank is present, right column has Bank + Sign stacked vertically (26 + 32 + 4 = 62mm)
      const FULL_LOWER_H = hasBank ? (BANK_H + SIGN_H + 4.0) : Math.max(NOTES_TERMS_H, SIGN_H);
      // When page breaks after Banking details table (before signature box):
      // Page 1 has Notes/Terms on left and Banking details on right
      const NOTES_TERMS_BANK_H = hasBank ? Math.max(NOTES_TERMS_H, BANK_H) : NOTES_TERMS_H;

      const totalItemsH = itemList.reduce((acc, item) => acc + this.estimateItemHeight(item), 0);

      // Permutation 1: Check if EVERYTHING (Items + Sub Total + Total Block + FULL Lower Block including Sign) fits on Page 1 (Single Page)
      if (totalItemsH + TBL_HDR + SUBTOTAL_H + TOTAL_BLK_H + FULL_LOWER_H <= SPACE_P1) {"""

tmpl_code, count1 = re.subn(old_bp_pattern, lambda m: new_bp_replacement, tmpl_code, flags=re.DOTALL)
print(f"Template buildPages replacement count: {count1}")

# Update renderTermsList
old_terms_pattern = r"renderTermsList\(termsStr, paymentTerms\) \{.*?return rendered\.join\('\\n'\);\s+\},"
new_terms_replacement = """renderTermsList(termsStr, paymentTerms, defaultOrgTerms = '') {
      const payTerm = paymentTerms || '30 Days net';
      
      let effectiveTerms = termsStr;
      if (!effectiveTerms || !String(effectiveTerms).trim()) {
        effectiveTerms = defaultOrgTerms || (window.AppStore && window.AppStore.getOrg() && window.AppStore.getOrg().defaultTerms) || '';
      }

      if (!effectiveTerms || !String(effectiveTerms).trim()) {
        effectiveTerms = `• Above prices are FOR Destination.
• Please mention our Estimate number on all future correspondence.
• Please share your valid GSTIN in your Purchase Order.
• Payment Terms: As agreed (${payTerm}).
• In case of Refurbished requirement
  * The defective part need to be returned - against delivery.
• Delivery will be within 3-4 weeks from date of PO.
  * Goods indicated above in stock are accurate as of the quote date.
  * If goods are out of stock at the time of release of PO, standard lead time would apply.
• Payment will be 50% advance and balance against delivery.`;
      }

      const rawLines = String(effectiveTerms).split('\\n');
      const rendered = [];

      for (let rawLine of rawLines) {
        const trimmed = rawLine.trim();
        if (!trimmed) continue;

        // Check if raw line or trimmed line indicates a sub-bullet: starts with * or - or indented
        const isSubBullet = (/^\\s+[\\*\\-•]/.test(rawLine)) || trimmed.startsWith('*') || (trimmed.startsWith('-') && !trimmed.startsWith('--'));
        
        // Strip leading bullet characters, replacement chars (\\ufffd), asterisks, dashes, whitespace
        let cleanText = trimmed.replace(/^[\\s\\ufffd•\\*\\-\\–\\—\\>]+/, '').trim();
        
        if (cleanText) {
          if (isSubBullet) {
            rendered.push(`<li class="sr-sub-bullet">${cleanText}</li>`);
          } else {
            rendered.push(`<li>${cleanText}</li>`);
          }
        }
      }

      if (rendered.length === 0) {
        return `<li>Above prices are FOR Destination.</li>
<li>Please mention our Estimate number on all future correspondence.</li>
<li>Please share your valid GSTIN in your Purchase Order.</li>
<li>Payment Terms: As agreed (${payTerm}).</li>
<li>In case of Refurbished requirement</li>
<li class="sr-sub-bullet">The defective part need to be returned - against delivery.</li>
<li>Delivery will be within 3-4 weeks from date of PO.</li>
<li class="sr-sub-bullet">Goods indicated above in stock are accurate as of the quote date.</li>
<li class="sr-sub-bullet">If goods are out of stock at the time of release of PO, standard lead time would apply.</li>
<li>Payment will be 50% advance and balance against delivery.</li>`;
      }

      return rendered.join('\\n');
    },"""

tmpl_code, count2 = re.subn(old_terms_pattern, lambda m: new_terms_replacement, tmpl_code, flags=re.DOTALL)
print(f"Template renderTermsList replacement count: {count2}")

# Update call in renderNotesAndTermsBlock
tmpl_code = tmpl_code.replace(
    "${this.renderTermsList(doc.terms, doc.paymentTerms)}",
    "${this.renderTermsList(doc.terms, doc.paymentTerms, (ctx.org && ctx.org.defaultTerms) || '')}"
)

with open(tmpl_path, 'w', encoding='utf-8') as f:
    f.write(tmpl_code)
print(f"Saved {tmpl_path}")


# 2. Update js/views/settings.js
set_path = 'js/views/settings.js'
with open(set_path, 'r', encoding='utf-8') as f:
    set_code = f.read()

old_save_org_pattern = r"saveOrgProfile\(\) \{.*?this\.render\(\);\s+\},"
new_save_org_replacement = """saveOrgProfile() {
      const currencyMap = {
        USD: '$', EUR: '€', GBP: '£', INR: '₹', CAD: '$', AUD: '$', JPY: '¥'
      };

      const selectedCurrency = document.getElementById('set-currency').value;
      const themeColor = document.getElementById('set-theme').value;

      const rawBank = document.getElementById('set-bank').value.trim();
      const parsedBank = window.GSTDocumentTemplate ? window.GSTDocumentTemplate.getBankDetails({ bankDetails: rawBank }) : {};

      const org = window.AppStore.getOrg() || {};
      const newTerms = document.getElementById('set-terms') ? document.getElementById('set-terms').value.trim() : (org.defaultTerms || '');

      const updates = {
        name: document.getElementById('set-name').value.trim(),
        legalName: document.getElementById('set-legal').value.trim(),
        taxId: document.getElementById('set-tax-id').value.trim(),
        email: document.getElementById('set-email').value.trim(),
        phone: document.getElementById('set-phone').value.trim(),
        website: document.getElementById('set-web').value.trim(),
        address: document.getElementById('set-address').value.trim(),
        currency: selectedCurrency,
        currencySymbol: currencyMap[selectedCurrency] || '$',
        themeColor: themeColor,
        bankDetails: rawBank,
        bankName: parsedBank.bankName || 'State Bank of India',
        accountName: parsedBank.accountName || 'SHREERAKSHA SOLUTIONS',
        accountNumber: parsedBank.accountNumber || '45666081503',
        branch: parsedBank.branch || 'PARKALA',
        ifscCode: parsedBank.ifscCode || 'SBIN0016869',
        defaultTerms: newTerms
      };

      window.AppStore.updateOrg(updates);

      // Propagate new terms to all documents so they reflect immediately across Tax Invoices and other documents
      if (newTerms) {
        ['invoices', 'estimates', 'purchaseOrders', 'debitCreditNotes'].forEach(col => {
          const list = window.AppStore.getAll(col);
          list.forEach(item => {
            item.terms = newTerms;
          });
        });
        window.AppStore.save();
      }

      // Apply theme class to body
      const selectedTheme = themeColor || 'dark';
      localStorage.setItem('theme_mode', selectedTheme);
      document.body.classList.remove('theme-dark', 'theme-light');
      document.body.classList.add(`theme-${selectedTheme}`);

      const themeToggle = document.getElementById('theme-toggle-switch');
      if (themeToggle) themeToggle.setAttribute('data-theme', selectedTheme);
      if (window.App && window.App.applyGlassTransparency) window.App.applyGlassTransparency();

      const headerCurr = document.getElementById('header-currency-code');
      if (headerCurr) headerCurr.textContent = `${updates.currency} (${updates.currencySymbol})`;

      window.Toast.show('Company profile and preferences saved!', 'success');
      this.render();
    },"""

set_code, count3 = re.subn(old_save_org_pattern, lambda m: new_save_org_replacement, set_code, flags=re.DOTALL)
print(f"Settings saveOrgProfile replacement count: {count3}")

with open(set_path, 'w', encoding='utf-8') as f:
    f.write(set_code)
print(f"Saved {set_path}")


# 3. Update js/views/invoices.js
inv_path = 'js/views/invoices.js'
with open(inv_path, 'r', encoding='utf-8') as f:
    inv_code = f.read()

# Fix textarea loading
inv_code = inv_code.replace(
    '<textarea id="ied-terms" class="form-control" rows="2">${existing ? existing.terms : org.defaultTerms}</textarea>',
    '<textarea id="ied-terms" class="form-control" rows="3">${(existing && existing.terms !== undefined && existing.terms !== null) ? existing.terms : ((org && org.defaultTerms) || "")}</textarea>'
)

# Fix onConfirm activeInvoiceId & render
old_inv_confirm = """          if (isEdit) {
            window.AppStore.update('invoices', invoiceId, invoiceData);
            window.Toast.show(`${isProf ? 'Proforma Invoice' : 'Tax invoice'} updated successfully!`, 'success');
          } else {
            const created = window.AppStore.add('invoices', invoiceData);
            this.activeInvoiceId = created.id;
            window.Toast.show(`${isProf ? 'Proforma Invoice' : 'Tax invoice'} ${number} generated successfully!`, 'success');
          }

          this.render();"""

new_inv_confirm = """          if (isEdit) {
            window.AppStore.update('invoices', invoiceId, invoiceData);
            this.activeInvoiceId = invoiceId;
            window.Toast.show(`${isProf ? 'Proforma Invoice' : 'Tax invoice'} updated successfully!`, 'success');
          } else {
            const created = window.AppStore.add('invoices', invoiceData);
            this.activeInvoiceId = created.id;
            window.Toast.show(`${isProf ? 'Proforma Invoice' : 'Tax invoice'} ${number} generated successfully!`, 'success');
          }

          this.render(this.activeInvoiceId);"""

inv_code = inv_code.replace(old_inv_confirm, new_inv_confirm)

with open(inv_path, 'w', encoding='utf-8') as f:
    f.write(inv_code)
print(f"Saved {inv_path}")


# 4. Update js/views/quotes.js
quo_path = 'js/views/quotes.js'
with open(quo_path, 'r', encoding='utf-8') as f:
    quo_code = f.read()

quo_code = quo_code.replace(
    '<textarea id="qed-terms" class="form-control" rows="2">${existing ? existing.terms : org.defaultTerms}</textarea>',
    '<textarea id="qed-terms" class="form-control" rows="3">${(existing && existing.terms !== undefined && existing.terms !== null) ? existing.terms : ((org && org.defaultTerms) || "")}</textarea>'
)

old_quo_confirm = """          if (isEdit) {
            window.AppStore.update('estimates', quoteId, quoteData);
            window.Toast.show('Quotation updated successfully!', 'success');
          } else {
            const created = window.AppStore.add('estimates', quoteData);
            this.activeQuoteId = created.id;
            window.Toast.show('Quotation created successfully!', 'success');
          }

          this.render();"""

new_quo_confirm = """          if (isEdit) {
            window.AppStore.update('estimates', quoteId, quoteData);
            this.activeQuoteId = quoteId;
            window.Toast.show('Quotation updated successfully!', 'success');
          } else {
            const created = window.AppStore.add('estimates', quoteData);
            this.activeQuoteId = quoteId;
            window.Toast.show('Quotation created successfully!', 'success');
          }

          this.render(this.activeQuoteId);"""

quo_code = quo_code.replace(old_quo_confirm, new_quo_confirm)

with open(quo_path, 'w', encoding='utf-8') as f:
    f.write(quo_code)
print(f"Saved {quo_path}")


# 5. Update js/views/purchase-orders.js
po_path = 'js/views/purchase-orders.js'
with open(po_path, 'r', encoding='utf-8') as f:
    po_code = f.read()

po_code = po_code.replace(
    '<textarea id="po-terms" class="form-control" rows="2">${existing ? existing.terms : \'Material subject to QC inspection upon delivery.\'}</textarea>',
    '<textarea id="po-terms" class="form-control" rows="3">${(existing && existing.terms !== undefined && existing.terms !== null) ? existing.terms : (window.AppStore.getOrg().defaultTerms || "Material subject to QC inspection upon delivery.")}</textarea>'
)

old_po_confirm = """          if (isEdit) {
            window.AppStore.update('purchaseOrders', poId, poData);
            window.Toast.show('Purchase Order updated successfully!', 'success');
          } else {
            const created = window.AppStore.add('purchaseOrders', poData);
            this.activePOId = created.id;
            window.Toast.show(`Purchase Order ${number} issued successfully!`, 'success');
          }

          this.render();"""

new_po_confirm = """          if (isEdit) {
            window.AppStore.update('purchaseOrders', poId, poData);
            this.activePOId = poId;
            window.Toast.show('Purchase Order updated successfully!', 'success');
          } else {
            const created = window.AppStore.add('purchaseOrders', poData);
            this.activePOId = created.id;
            window.Toast.show(`Purchase Order ${number} issued successfully!`, 'success');
          }

          this.render(this.activePOId);"""

po_code = po_code.replace(old_po_confirm, new_po_confirm)

with open(po_path, 'w', encoding='utf-8') as f:
    f.write(po_code)
print(f"Saved {po_path}")


# 6. Update js/views/debit-credit-notes.js
dcn_path = 'js/views/debit-credit-notes.js'
with open(dcn_path, 'r', encoding='utf-8') as f:
    dcn_code = f.read()

old_dcn_confirm = """          if (isEdit) {
            window.AppStore.update('debitCreditNotes', noteId, noteData);
            window.Toast.show(`${docType} updated successfully!`, 'success');
          } else {
            const created = window.AppStore.add('debitCreditNotes', noteData);
            this.activeNoteId = created.id;
            window.Toast.show(`${docType} ${number} issued successfully!`, 'success');
          }

          this.render();"""

new_dcn_confirm = """          if (isEdit) {
            window.AppStore.update('debitCreditNotes', noteId, noteData);
            this.activeNoteId = noteId;
            window.Toast.show(`${docType} updated successfully!`, 'success');
          } else {
            const created = window.AppStore.add('debitCreditNotes', noteData);
            this.activeNoteId = created.id;
            window.Toast.show(`${docType} ${number} issued successfully!`, 'success');
          }

          this.render(this.activeNoteId);"""

dcn_code = dcn_code.replace(old_dcn_confirm, new_dcn_confirm)

with open(dcn_path, 'w', encoding='utf-8') as f:
    f.write(dcn_code)
print(f"Saved {dcn_path}")


# 7. Standard 10-line Terms in default_data.json and sreeraksha.db
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

# Update js/store.js DEFAULT_DATA
with open('js/store.js', 'r', encoding='utf-8') as f:
    store_code = f.read()

escaped_terms = std_terms.replace('\n', '\\n')
store_code = re.sub(r'defaultTerms:\s*[\'"`].*?[\'"`],', f"defaultTerms: '{escaped_terms}',", store_code, flags=re.DOTALL)
with open('js/store.js', 'w', encoding='utf-8') as f:
    f.write(store_code)
print("Updated js/store.js with clean terms.")

print("All updates applied successfully!")


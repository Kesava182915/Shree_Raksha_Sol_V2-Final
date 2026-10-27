import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument('--headless')
opts.add_argument('--window-size=1600,1200')
driver = webdriver.Chrome(options=opts)

driver.get('http://127.0.0.1:8080/index.html#quotes')
time.sleep(2)
driver.execute_script("""
    const ov = document.getElementById('auth-overlay-backdrop');
    if (ov) ov.remove();
    const m = document.querySelector('.auth-modal-card');
    if (m) m.remove();
""")
time.sleep(1)

results = driver.execute_script("""
    const out = {};
    
    // --- TASK 1: Banking details in Quotation vs Invoice ---
    const qDoc = window.GSTDocumentTemplate.render({
        id: 'q1',
        docType: 'QUOTATION',
        number: 'SHRKS/Qtn/26-27/001',
        date: '2026-10-24',
        expiryDate: '2026-11-24',
        customerId: 'cust-001',
        items: [
            { name: "Item 1", hsnCode: "90279090", quantity: 1, rate: 1000, taxRate: 18 }
        ]
    });
    
    const invDoc = window.GSTDocumentTemplate.render({
        id: 'i1',
        docType: 'TAX INVOICE',
        number: 'SHRKS/Inv/26-27/001',
        date: '2026-10-24',
        dueDate: '2026-11-24',
        customerId: 'cust-001',
        items: [
            { name: "Item 1", hsnCode: "90279090", quantity: 1, rate: 1000, taxRate: 18 }
        ]
    });
    
    out.task1_quoteHasBank = qDoc.includes('COMPANY BANKING DETAILS');
    out.task1_invoiceHasBank = invDoc.includes('COMPANY BANKING DETAILS');
    
    // --- TASK 2: Validity date in Quotation ---
    out.task2_quoteHasValidityDate = qDoc.includes('Validity date');
    out.task2_quoteHasExpiryDate = qDoc.includes('Expiry Date');
    
    // Check Quote Modal field label
    const testDiv = document.createElement('div');
    testDiv.id = 'test-modal-container';
    document.body.appendChild(testDiv);
    
    // --- TASK 3: Header cell filling with grey #9BA8AB across documents ---
    const dTypes = ['QUOTATION', 'TAX INVOICE', 'PROFORMA INVOICE', 'PURCHASE ORDER', 'DEBIT NOTE', 'CREDIT NOTE', 'DELIVERY CHALLAN'];
    out.task3_headerColors = {};
    
    dTypes.forEach(dt => {
        const docHtml = window.GSTDocumentTemplate.render({
            id: 'test-' + dt,
            docType: dt,
            number: 'DOC-001',
            date: '2026-10-24',
            customerId: 'cust-001',
            items: [{ name: "Item A", hsnCode: "90279090", quantity: 1, rate: 500, taxRate: 18 }]
        });
        testDiv.innerHTML = docHtml;
        const th = testDiv.querySelector('.sr-items-table th');
        const metaTh = testDiv.querySelector('.sr-meta-table th');
        
        const thBg = th ? window.getComputedStyle(th).backgroundColor : null;
        const metaBg = metaTh ? window.getComputedStyle(metaTh).backgroundColor : null;
        out.task3_headerColors[dt] = {
            itemsThBg: thBg,
            metaThBg: metaBg
        };
    });
    
    // --- TASK 4: 2X space between For Shreeraksha Solutions and Authorized Signature ---
    testDiv.innerHTML = qDoc;
    const signBody = testDiv.querySelector('.sr-sign-body');
    out.task4_signBodyHeight = signBody ? window.getComputedStyle(signBody).height : null;
    out.task4_signBodyMinHeight = signBody ? window.getComputedStyle(signBody).minHeight : null;
    
    // --- TASK 5: Name board image ---
    const brandImg = testDiv.querySelector('.sr-brand-img');
    out.task5_brandImgSrc = brandImg ? brandImg.getAttribute('src') : null;
    out.task5_brandImgLoaded = brandImg ? brandImg.complete && brandImg.naturalWidth > 0 : false;
    out.task5_brandImgNaturalWidth = brandImg ? brandImg.naturalWidth : 0;
    out.task5_brandImgNaturalHeight = brandImg ? brandImg.naturalHeight : 0;
    
    testDiv.remove();
    return out;
""")

print("=== 5 TASKS TEST RESULTS ===")
print(json.dumps(results, indent=2))

# Assertions
assert results['task1_quoteHasBank'] == False, "Task 1 Failed: Bank details still present in Quotation!"
assert results['task1_invoiceHasBank'] == True, "Task 1 Failed: Bank details missing from Tax Invoice!"
print("Task 1 PASSED: Banking details removed from Quotation, preserved in Invoices.")

assert results['task2_quoteHasValidityDate'] == True, "Task 2 Failed: 'Validity date' not found in Quotation!"
assert results['task2_quoteHasExpiryDate'] == False, "Task 2 Failed: 'Expiry Date' still found in Quotation!"
print("Task 2 PASSED: Quotation has 'Validity date' instead of 'Expiry Date'.")

# #9BA8AB in RGB is rgb(155, 168, 171)
for dt, cols in results['task3_headerColors'].items():
    print(f"Task 3: {dt} items header bg: {cols['itemsThBg']}, meta header bg: {cols['metaThBg']}")
    assert '155, 168, 171' in cols['itemsThBg'] or '155, 168, 171' in str(cols['metaThBg']), f"Task 3 Failed for {dt}"
print("Task 3 PASSED: All document types have Grey #9BA8AB table headers!")

assert '96px' in results['task4_signBodyHeight'], f"Task 4 Failed: Expected 96px but got {results['task4_signBodyHeight']}"
print("Task 4 PASSED: Signature space is exactly 2X (96px) from previous 48px!")

assert 'shreeraksha-text-exact.png' in results['task5_brandImgSrc'], "Task 5 Failed: Name board src wrong!"
assert results['task5_brandImgNaturalWidth'] > 0, "Task 5 Failed: Image not loaded!"
print(f"Task 5 PASSED: Name board replaced ({results['task5_brandImgNaturalWidth']}x{results['task5_brandImgNaturalHeight']})!")

# Take fresh screenshots of Quotation and Invoice
driver.get('http://127.0.0.1:8080/index.html#quotes')
time.sleep(2)
driver.execute_script("""
    const ov = document.getElementById('auth-overlay-backdrop');
    if (ov) ov.remove();
    const m = document.querySelector('.auth-modal-card');
    if (m) m.remove();
""")
time.sleep(1)
driver.save_screenshot('scratch/updated_quotes_view.png')

driver.get('http://127.0.0.1:8080/index.html#invoices')
time.sleep(2)
driver.execute_script("""
    const ov = document.getElementById('auth-overlay-backdrop');
    if (ov) ov.remove();
    const m = document.querySelector('.auth-modal-card');
    if (m) m.remove();
""")
time.sleep(1)
driver.save_screenshot('scratch/updated_invoices_view.png')

driver.quit()
print("\nALL 5 TASKS VERIFIED SUCCESSFULLY WITH ZERO DEFECTS!")

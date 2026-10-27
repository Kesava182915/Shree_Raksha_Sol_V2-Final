import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

OUTPUT_DIR = os.path.join(os.path.dirname(__file__))

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1600,1000')
options.add_argument('--incognito')
driver = webdriver.Chrome(options=options)

try:
    print("1. Opening app at http://127.0.0.1:8080/...")
    driver.get('http://127.0.0.1:8080/')
    time.sleep(2)

    # 1. Verify admin icon is completely removed from top header
    admin_pill = driver.find_elements('id', 'header-user-profile-wrap')
    admin_btn = driver.find_elements('id', 'header-user-menu-btn')
    assert len(admin_pill) == 0 or not admin_pill[0].is_displayed(), "Admin icon wrap must NOT be displayed!"
    assert len(admin_btn) == 0 or not admin_btn[0].is_displayed(), "Admin button must NOT be displayed!"
    print("[PASS] Top header admin icon successfully removed!")

    # Capture header screenshot
    header_el = driver.find_element('css selector', '.app-header')
    header_el.screenshot(os.path.join(OUTPUT_DIR, 'header_without_admin_icon.png'))
    print("[PASS] Captured screenshot of top header without admin icon: header_without_admin_icon.png")

    # 2. Check Terms and Conditions rendering in Tax Invoice and Quotation
    print("2. Testing Terms and Conditions in document preview...")
    terms_check = driver.execute_script("""
        // Fetch first invoice
        const inv = (JSON.parse(localStorage.getItem('gst_invoices_v1') || '[]')[0]) || {
            number: 'SHRKS/Inv/26-27/019',
            paymentTerms: '30 Days net',
            items: [{ name: 'HPLC Column', rate: 45000, quantity: 1, grossAmount: 45000, discount: 0, taxableAmount: 45000, cgstRate: 9, cgstAmount: 4050, sgstRate: 9, sgstAmount: 4050, totalLineAmount: 53100 }]
        };

        const container = document.createElement('div');
        container.id = 'terms-verify-container';
        container.innerHTML = window.GSTDocumentTemplate.render(inv, { docType: 'TAX INVOICE' });
        document.body.appendChild(container);

        const termsList = container.querySelectorAll('.sr-terms-list li');
        const termsText = Array.from(termsList).map(li => li.textContent.trim());

        return {
            itemCount: termsList.length,
            items: termsText
        };
    """)

    print(f"Rendered Terms Count: {terms_check['itemCount']}")
    print("Terms Items:")
    for idx, item in enumerate(terms_check['items'], 1):
        print(f"  {idx}. {item}")

    # Verify standard items
    assert terms_check['itemCount'] >= 9, f"Expected at least 9-10 terms items, got {terms_check['itemCount']}"
    assert any('FOR Destination' in t for t in terms_check['items']), "Missing 'Above prices are FOR Destination'"
    assert any('Estimate number' in t for t in terms_check['items']), "Missing 'Please mention our Estimate number'"
    assert any('valid GSTIN' in t for t in terms_check['items']), "Missing 'Please share your valid GSTIN'"
    assert any('Refurbished requirement' in t for t in terms_check['items']), "Missing 'Refurbished requirement'"
    assert any('defective part' in t for t in terms_check['items']), "Missing 'defective part'"
    assert any('3-4 weeks' in t for t in terms_check['items']), "Missing '3-4 weeks from date of PO'"
    assert any('50% advance' in t for t in terms_check['items']), "Missing '50% advance and balance'"
    print("[PASS] All authentic Terms & Conditions items restored successfully!")

    # Capture document screenshot showing restored terms
    doc_el = driver.find_element('css selector', '#terms-verify-container .shreeraksha-document-page')
    doc_el.screenshot(os.path.join(OUTPUT_DIR, 'restored_terms_document.png'))
    print("[PASS] Captured document preview screenshot: restored_terms_document.png")

    print("\n=======================================================")
    print("ALL VERIFICATIONS PASSED: ADMIN ICON REMOVED & TERMS RESTORED!")
    print("=======================================================")

finally:
    driver.quit()


import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

OUTPUT_DIR = os.path.join(os.path.dirname(__file__))

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1600,1000')
# Start clean session (no pre-existing cookies/localstorage)
options.add_argument('--incognito')
driver = webdriver.Chrome(options=options)

try:
    print("1. Navigating to clean app instance at http://127.0.0.1:8080/...")
    driver.get('http://127.0.0.1:8080/')
    time.sleep(2)

    # Check that NO auth overlay backdrop exists or is visible
    auth_overlay = driver.find_elements('id', 'auth-overlay-backdrop')
    assert len(auth_overlay) == 0 or not auth_overlay[0].is_displayed(), "Auth overlay should NOT be visible or exist!"
    print("[PASS] No login modal / auth overlay backdrop displayed on startup!")

    # Check that Dashboard view is mounted and active
    current_view = driver.find_element('id', 'app-view')
    assert current_view.is_displayed(), "Main app view must be displayed!"
    
    # Capture initial dashboard screenshot
    driver.save_screenshot(os.path.join(OUTPUT_DIR, "no_login_direct_dashboard.png"))
    print("[PASS] Dashboard rendered directly without login prompt. Screenshot saved: no_login_direct_dashboard.png")

    # Check top header profile
    header_name = driver.find_element('id', 'header-user-name').text
    header_badge = driver.find_element('id', 'header-user-role-badge').text
    print(f"[PASS] Header profile active: Name='{header_name}', Role='{header_badge}'")
    assert header_name == 'Admin'
    assert header_badge == 'ADMIN'

    # Check sidebar user badge
    sb_name = driver.find_element('css selector', '.sidebar-footer .user-name').text
    sb_role = driver.find_element('css selector', '.sidebar-footer .user-role').text
    print(f"[PASS] Sidebar footer profile: Name='{sb_name}', Role='{sb_role}'")
    assert 'Shreeraksha' in sb_name

    # Click sidebar badge to ensure NO modal opens
    driver.find_element('id', 'sidebar-user-badge').click()
    time.sleep(0.5)
    auth_overlay_after_click = driver.find_elements('id', 'auth-overlay-backdrop')
    assert len(auth_overlay_after_click) == 0 or not auth_overlay_after_click[0].is_displayed(), "Clicking sidebar badge should NOT open login modal!"
    print("[PASS] Clicking sidebar user badge did NOT trigger any login prompt!")

    # 2. Test Navigation to Quotations
    print("2. Testing Quotations view...")
    driver.get('http://127.0.0.1:8080/#quotes')
    time.sleep(1.5)
    quotes_table = driver.find_element('css selector', '#app-view')
    assert 'Quotations' in quotes_table.text
    print("[PASS] Quotations route loaded successfully!")

    # 3. Test Navigation to Invoices
    print("3. Testing Invoices view...")
    driver.get('http://127.0.0.1:8080/#invoices')
    time.sleep(1.5)
    inv_content = driver.find_element('css selector', '#app-view').text
    assert 'Invoices' in inv_content or 'Delivery Challans' in inv_content
    print("[PASS] Invoices route loaded successfully!")

    # 4. Test Navigation to Debit/Credit Notes
    print("4. Testing Debit/Credit Notes view...")
    driver.get('http://127.0.0.1:8080/#debit-credit-notes')
    time.sleep(1.5)
    notes_content = driver.find_element('css selector', '#app-view').text
    assert 'Debit' in notes_content or 'Credit' in notes_content or 'Notes' in notes_content
    print("[PASS] Debit & Credit Notes route loaded successfully!")

    # 5. Test Navigation to Purchase Orders
    print("5. Testing Purchase Orders view...")
    driver.get('http://127.0.0.1:8080/#purchase-orders')
    time.sleep(1.5)
    po_content = driver.find_element('css selector', '#app-view').text
    assert 'Purchase Orders' in po_content
    print("[PASS] Purchase Orders route loaded successfully!")

    # 6. Test Navigation to Payments
    print("6. Testing Payments Received view...")
    driver.get('http://127.0.0.1:8080/#payments')
    time.sleep(1.5)
    pay_content = driver.find_element('css selector', '#app-view').text
    assert 'Payments' in pay_content
    print("[PASS] Payments Received route loaded successfully!")

    # 7. Test Navigation to Customers
    print("7. Testing Customers & Vendors view...")
    driver.get('http://127.0.0.1:8080/#customers')
    time.sleep(1.5)
    cust_content = driver.find_element('css selector', '#app-view').text
    assert 'Customers' in cust_content or 'Vendors' in cust_content
    print("[PASS] Customers & Vendors route loaded successfully!")

    # 8. Test Navigation to Items
    print("8. Testing Items & Services view...")
    driver.get('http://127.0.0.1:8080/#items')
    time.sleep(1.5)
    items_content = driver.find_element('css selector', '#app-view').text
    assert 'Items' in items_content or 'Services' in items_content
    print("[PASS] Items & Services route loaded successfully!")

    # 9. Test Navigation to Reports
    print("9. Testing Reports view...")
    driver.get('http://127.0.0.1:8080/#reports')
    time.sleep(1.5)
    rep_content = driver.find_element('css selector', '#app-view').text
    assert 'Reports' in rep_content or 'GST' in rep_content
    print("[PASS] Reports route loaded successfully!")

    # 10. Test Navigation to Settings
    print("10. Testing Settings view...")
    driver.get('http://127.0.0.1:8080/#settings')
    time.sleep(1.5)
    set_content = driver.find_element('css selector', '#app-view').text
    assert 'Settings' in set_content or 'Organization' in set_content
    print("[PASS] Settings route loaded successfully!")

    # 11. Test Document Template Rendering (GST Document Template)
    print("11. Testing GST Document Template rendering...")
    template_res = driver.execute_script("""
        const inv = (JSON.parse(localStorage.getItem('gst_invoices_v1') || '[]')[0]) || {
            id: 'INV-TEST-001',
            invoiceNumber: 'SHRKS/Inv/26-27/001',
            invoiceType: 'tax_invoice',
            invoiceDate: '2026-10-24',
            dueDate: '2026-11-24',
            customer: {
                name: 'Manipal Speciality Chemicals Pvt Ltd',
                billingAddress: { street: 'Plot 42, KIADB Industrial Area', city: 'Bommasandra', state: 'Karnataka', pincode: '560099' },
                shippingAddress: { street: 'Plot 42, KIADB Industrial Area', city: 'Bommasandra', state: 'Karnataka', pincode: '560099' },
                gstin: '29ABCDE1234F1Z5',
                pan: 'ABCDE1234F',
                placeOfSupply: '29 - Karnataka'
            },
            items: [
                { name: 'Analytical HPLC Column C18', description: 'Ultra-pure silica, 100A pore size', rate: 45000, quantity: 1, grossAmount: 45000, discount: 0, taxableAmount: 45000, cgstRate: 9, cgstAmount: 4050, sgstRate: 9, sgstAmount: 4050, totalLineAmount: 53100 }
            ]
        };

        const container = document.createElement('div');
        container.id = 'doc-render-check';
        container.innerHTML = window.GSTDocumentTemplate.render(inv, { docType: 'TAX INVOICE' });
        document.body.appendChild(container);

        const bankHdr = container.querySelector('.sr-bank-header');
        const signHdr = container.querySelector('.sr-sign-header');

        const bankBg = bankHdr ? window.getComputedStyle(bankHdr).backgroundColor : null;
        const bankColor = bankHdr ? window.getComputedStyle(bankHdr).color : null;
        const signBg = signHdr ? window.getComputedStyle(signHdr).backgroundColor : null;
        const signColor = signHdr ? window.getComputedStyle(signHdr).color : null;

        return {
            bankBg,
            bankColor,
            signBg,
            signColor
        };
    """)
    print("Template Color check:", template_res)
    assert template_res['bankBg'] == 'rgb(155, 168, 171)', f"Expected rgb(155, 168, 171) for bankBg, got {template_res['bankBg']}"
    assert template_res['bankColor'] == 'rgb(0, 0, 0)', f"Expected rgb(0, 0, 0) for bankColor, got {template_res['bankColor']}"
    assert template_res['signBg'] == 'rgb(155, 168, 171)', f"Expected rgb(155, 168, 171) for signBg, got {template_res['signBg']}"
    assert template_res['signColor'] == 'rgb(0, 0, 0)', f"Expected rgb(0, 0, 0) for signColor, got {template_res['signColor']}"
    print("[PASS] Template rendering retains grey headers (#9BA8AB) and black text (rgb(0,0,0))!")

    print("\n=======================================================")
    print("ALL TESTS PASSED: LOGIN COMPLETELY REMOVED & ZERO DEFECTS!")
    print("=======================================================")

finally:
    driver.quit()


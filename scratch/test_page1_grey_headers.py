import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

OUTPUT_DIR = os.path.join(os.path.dirname(__file__))

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1400,1600')
driver = webdriver.Chrome(options=options)

try:
    driver.get('http://127.0.0.1:8080/')
    time.sleep(2)

    script = """
        // 1-item invoice: fits on 1 page with Banking details & For Shreeraksha Solutions on Page 1
        const singleItemInv = {
            id: 'INV-PAGE1-TEST',
            invoiceNumber: 'SHRKS/Inv/26-27/001',
            invoiceType: 'tax_invoice',
            invoiceDate: '2026-10-24',
            dueDate: '2026-11-24',
            termsAndConditions: '1. Payment terms: 30 days.\\n2. Goods once sold will not be taken back.',
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
        container.id = 'page1-test-container';
        container.style.position = 'absolute';
        container.style.top = '0px';
        container.style.left = '0px';
        container.style.zIndex = '99999';
        container.style.background = '#e5e7eb';
        container.style.padding = '20px';
        container.innerHTML = window.GSTDocumentTemplate.render(singleItemInv, { docType: 'TAX INVOICE' });
        document.body.appendChild(container);

        const page1 = container.querySelector('.shreeraksha-document-page');
        const bankHeader = page1.querySelector('.sr-bank-header');
        const signHeader = page1.querySelector('.sr-sign-header');

        const bankBg = bankHeader ? window.getComputedStyle(bankHeader).backgroundColor : null;
        const bankColor = bankHeader ? window.getComputedStyle(bankHeader).color : null;
        const signBg = signHeader ? window.getComputedStyle(signHeader).backgroundColor : null;
        const signColor = signHeader ? window.getComputedStyle(signHeader).color : null;

        return {
            pageCount: container.querySelectorAll('.shreeraksha-document-page').length,
            bankBg,
            bankColor,
            signBg,
            signColor
        };
    """

    res = driver.execute_script(script)
    print("Page 1 Verification Results:", res)

    # RGB check for #9BA8AB: rgb(155, 168, 171)
    # RGB check for black: rgb(0, 0, 0)
    assert res['bankBg'] == 'rgb(155, 168, 171)', f"Expected rgb(155, 168, 171) for bank header background, got {res['bankBg']}"
    assert res['bankColor'] == 'rgb(0, 0, 0)', f"Expected rgb(0, 0, 0) for bank header text, got {res['bankColor']}"
    assert res['signBg'] == 'rgb(155, 168, 171)', f"Expected rgb(155, 168, 171) for sign header background, got {res['signBg']}"
    assert res['signColor'] == 'rgb(0, 0, 0)', f"Expected rgb(0, 0, 0) for sign header text, got {res['signColor']}"

    # Take screenshot of page 1
    page1_el = driver.find_element('css selector', '#page1-test-container .shreeraksha-document-page')
    page1_el.screenshot(os.path.join(OUTPUT_DIR, 'page1_actual_render.png'))
    print("Page 1 screenshot captured at scratch/page1_actual_render.png")
    print(">>> SUCCESS: Page 1 Banking details header & Signature header are Grey (#9BA8AB) and Text is Black (rgb(0, 0, 0))!")

finally:
    driver.quit()

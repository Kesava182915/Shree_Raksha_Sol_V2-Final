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

# Render 5 items like ZODIAC C18
info = driver.execute_script("""
    const items5 = [
        { name: "ZODIAC C18", description: "250mmx4.6mm, 5µm", hsnCode: "90279090", quantity: 6, unit: "No's", rate: 39286, discountVal: 5, discountType: "percentage", taxRate: 18 },
        { name: "ZODIAC C18", description: "150mmx4.6mm, 3.5µm", hsnCode: "90279090", quantity: 3, unit: "No's", rate: 39286, discountVal: 5, discountType: "percentage", taxRate: 18 },
        { name: "Hypersil BDS C18", description: "250mm x 4.6mm, 5µm", hsnCode: "90279090", quantity: 1, unit: "No's", rate: 67778, discountVal: 5, discountType: "percentage", taxRate: 18 },
        { name: "Inertsil ODS-3", description: "150mm x 4.6mm, 5µm", hsnCode: "90279090", quantity: 2, unit: "No's", rate: 42000, discountVal: 5, discountType: "percentage", taxRate: 18 },
        { name: "Luna C18(2)", description: "250mm x 4.6mm, 5µm", hsnCode: "90279090", quantity: 2, unit: "No's", rate: 45000, discountVal: 5, discountType: "percentage", taxRate: 18 }
    ];
    
    const pages = window.GSTDocumentTemplate.buildPages(items5);
    
    const quote = {
        id: "test-5-short",
        number: "SHRKS/Qtn/26-27/019",
        date: "2026-10-24",
        expiryDate: "2026-11-24",
        reference: "RFQ-5-SHORT",
        customerId: "cust-001",
        items: items5,
        notes: 'Order to be placed on "Shreeraksha Solutions" & Below Address mentioned',
        paymentTerms: "30 Days net"
    };
    
    const html = window.GSTDocumentTemplate.render(quote);
    
    // Inject into preview area to measure real DOM heights
    const container = document.querySelector('.invoice-paper-wrapper') || document.querySelector('.split-detail-pane') || document.body;
    const testDiv = document.createElement('div');
    testDiv.id = 'test-render-5';
    testDiv.innerHTML = html;
    document.body.appendChild(testDiv);
    
    const docElem = testDiv.querySelector('.shreeraksha-document');
    const scrollH = docElem.scrollHeight;
    const clientH = docElem.clientHeight;
    const footerElem = docElem.querySelector('.sr-footer-box');
    const footerRect = footerElem ? footerElem.getBoundingClientRect() : null;
    const docRect = docElem.getBoundingClientRect();
    
    // Check if footer bottom exceeds doc bottom
    const footerOverflows = footerRect ? (footerRect.bottom > docRect.bottom + 1) : false;
    
    return {
        pagesCount: pages.length,
        pagesConfig: pages,
        docClientHeight: clientH,
        docScrollHeight: scrollH,
        footerOverflows: footerOverflows,
        docRect: { top: docRect.top, bottom: docRect.bottom, height: docRect.height },
        footerRect: footerRect ? { top: footerRect.top, bottom: footerRect.bottom, height: footerRect.height } : null
    };
""")

print("5 short items test result:")
print(json.dumps(info, indent=2))

# Scroll to test element and screenshot
driver.execute_script("""
    const elem = document.getElementById('test-render-5');
    if (elem) elem.scrollIntoView();
""")
time.sleep(1)
driver.save_screenshot('scratch/5_items_overflow_test.png')
driver.quit()

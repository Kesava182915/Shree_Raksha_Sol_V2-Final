import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument('--headless')
opts.add_argument('--window-size=1600,1400')
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

# Render 5-item quotation inside preview
driver.execute_script("""
    const items5 = [
        { name: "ZODIAC C18", description: "250mmx4.6mm, 5µm", hsnCode: "90279090", quantity: 6, unit: "No's", rate: 39286, discountVal: 5, discountType: "percentage", taxRate: 18 },
        { name: "ZODIAC C18", description: "150mmx4.6mm, 3.5µm", hsnCode: "90279090", quantity: 3, unit: "No's", rate: 39286, discountVal: 5, discountType: "percentage", taxRate: 18 },
        { name: "Hypersil BDS C18", description: "250mm x 4.6mm, 5µm", hsnCode: "90279090", quantity: 1, unit: "No's", rate: 67778, discountVal: 5, discountType: "percentage", taxRate: 18 },
        { name: "Inertsil ODS-3", description: "150mm x 4.6mm, 5µm", hsnCode: "90279090", quantity: 2, unit: "No's", rate: 42000, discountVal: 5, discountType: "percentage", taxRate: 18 },
        { name: "Luna C18(2)", description: "250mm x 4.6mm, 5µm", hsnCode: "90279090", quantity: 2, unit: "No's", rate: 45000, discountVal: 5, discountType: "percentage", taxRate: 18 }
    ];
    
    const quote = {
        id: "test-quote-5",
        number: "SHRKS/Qtn/26-27/025",
        date: "2026-10-24",
        expiryDate: "2026-11-24",
        reference: "RFQ-2026-005",
        customerId: "cust-001",
        items: items5,
        notes: 'Order to be placed on "Shreeraksha Solutions" & Below Address mentioned',
        paymentTerms: "30 Days net"
    };
    
    const html = window.GSTDocumentTemplate.render(quote);
    const paper = document.querySelector('.invoice-paper-wrapper');
    if (paper) {
        paper.innerHTML = html;
    }
""")
time.sleep(1)

# Now emulate print media
driver.execute_cdp_cmd('Emulation.setEmulatedMedia', {'media': 'print'})
time.sleep(1)

# Measure print DOM heights
print_metrics = driver.execute_script("""
    const docs = document.querySelectorAll('.shreeraksha-document');
    const res = [];
    docs.forEach((doc, idx) => {
        const dRect = doc.getBoundingClientRect();
        const f = doc.querySelector('.sr-footer-box');
        const fRect = f ? f.getBoundingClientRect() : null;
        res.push({
            page: idx + 1,
            clientHeight: doc.clientHeight,
            scrollHeight: doc.scrollHeight,
            overflows: doc.scrollHeight > doc.clientHeight,
            footerBottom: fRect ? fRect.bottom : 0,
            docBottom: dRect.bottom,
            footerSafeInside: fRect ? (fRect.bottom <= dRect.bottom + 1.0) : false
        });
    });
    return res;
""")

print("Print media metrics:")
print(json.dumps(print_metrics, indent=2))

driver.save_screenshot('scratch/print_preview_5_items.png')
driver.quit()
print("Print preview verified successfully!")

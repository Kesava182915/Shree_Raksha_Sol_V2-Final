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

# Check both pages for 5 items
pages_info = driver.execute_script("""
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
    
    const container = document.createElement('div');
    container.id = 'full-preview-container';
    container.style.position = 'absolute';
    container.style.top = '100px';
    container.style.left = '50px';
    container.style.zIndex = '99999';
    container.style.background = '#e2e8f0';
    container.style.padding = '20px';
    container.innerHTML = html;
    document.body.appendChild(container);
    
    const pages = container.querySelectorAll('.shreeraksha-document');
    const results = [];
    
    pages.forEach((p, idx) => {
        const pRect = p.getBoundingClientRect();
        const f = p.querySelector('.sr-footer-box');
        const fRect = f ? f.getBoundingClientRect() : null;
        const footerLines = f ? Array.from(f.querySelectorAll('.sr-footer-left div')).map(d => d.textContent.trim()) : [];
        const pagePill = f ? (f.querySelector('.sr-footer-page-pill') ? f.querySelector('.sr-footer-page-pill').textContent.trim() : '') : '';
        
        results.push({
            pageNumber: idx + 1,
            clientHeight: p.clientHeight,
            scrollHeight: p.scrollHeight,
            overflows: p.scrollHeight > p.clientHeight,
            footerBottom: fRect ? fRect.bottom : 0,
            pageBottom: pRect.bottom,
            footerSafeInside: fRect ? (fRect.bottom <= pRect.bottom + 0.5) : false,
            footerLines: footerLines,
            pagePill: pagePill
        });
    });
    
    return results;
""")

print("Pages verification results:")
print(json.dumps(pages_info, indent=2))

# Take screenshot of Page 1
driver.execute_script("""
    const p1 = document.querySelectorAll('#full-preview-container .shreeraksha-document')[0];
    if (p1) p1.scrollIntoView();
""")
time.sleep(1)
driver.save_screenshot('scratch/quotation_5_items_page1.png')

# Take screenshot of Page 2
driver.execute_script("""
    const p2 = document.querySelectorAll('#full-preview-container .shreeraksha-document')[1];
    if (p2) p2.scrollIntoView();
""")
time.sleep(1)
driver.save_screenshot('scratch/quotation_5_items_page2.png')

driver.quit()
print("Screenshots captured successfully!")

import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument('--headless')
opts.add_argument('--window-size=1600,1000')
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

# Now evaluate GSTDocumentTemplate.buildPages for 5 items
result = driver.execute_script("""
    const sample5Items = [
        { name: "Gas Chromatograph System", description: "High Resolution GC-2030 with FID detector", hsnCode: "90279090", quantity: 1, unit: "No's", rate: 450000, discountVal: 5, discountType: "percentage", taxRate: 18 },
        { name: "Capillary Column DB-5MS", description: "30m x 0.25mm ID x 0.25um film thickness", hsnCode: "90279090", quantity: 2, unit: "No's", rate: 35000, discountVal: 0, discountType: "percentage", taxRate: 18 },
        { name: "Autosampler Syringe 10uL", description: "Fixed needle 23-26s gauge cone tip", hsnCode: "90279090", quantity: 5, unit: "No's", rate: 4200, discountVal: 10, discountType: "percentage", taxRate: 18 },
        { name: "Inlet Septa High Temperature", description: "Premium silicone septa pack of 50", hsnCode: "90279090", quantity: 3, unit: "Pack", rate: 6500, discountVal: 0, discountType: "percentage", taxRate: 18 },
        { name: "Annual Maintenance Contract", description: "Comprehensive maintenance for analytical system", hsnCode: "998719", quantity: 1, unit: "Service", rate: 75000, discountVal: 0, discountType: "percentage", taxRate: 18 }
    ];
    
    const pages = window.GSTDocumentTemplate.buildPages(sample5Items);
    
    // Also render document to test
    const quote = {
        id: "test-5-items",
        number: "SHRKS/Qtn/26-27/099",
        date: "2026-10-24",
        expiryDate: "2026-11-24",
        reference: "RFQ-TEST-5",
        customerId: "cust-001",
        items: sample5Items,
        notes: 'Order to be placed on "Shreeraksha Solutions" & Below Address mentioned',
        paymentTerms: "30 Days net"
    };
    
    const html = window.GSTDocumentTemplate.render(quote);
    
    return {
        pagesCount: pages.length,
        pagesConfig: pages,
        totalItemsH: sample5Items.reduce((acc, i) => acc + window.GSTDocumentTemplate.estimateItemHeight(i), 0)
    };
""")

print("Current 5-item test result:")
print(json.dumps(result, indent=2))
driver.quit()

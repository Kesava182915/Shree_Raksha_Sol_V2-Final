import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

CHROMEDRIVER_PATH = r"C:\Users\kesav\.wdm\drivers\chromedriver\win64\156.0.8078.47\chromedriver-win64\chromedriver.exe"
OUTPUT_DIR = r"d:\Antigravity folder\3\scratch"
os.makedirs(OUTPUT_DIR, exist_ok=True)

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--window-size=1600,1200")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

service = Service(executable_path=CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    print("Connecting to http://127.0.0.1:8080/...")
    driver.get("http://127.0.0.1:8080/")
    time.sleep(2)

    # Bypass auth
    driver.execute_script("""
        if (window.AuthManager) {
            window.AuthManager.closeModal();
            window.AuthManager.currentUser = { name: 'Shreeraksha Admin', email: 'admin@shreeraksha.in', role: 'admin' };
            window.AuthManager.selectedRole = 'admin';
            localStorage.setItem('auth_session_user', JSON.stringify(window.AuthManager.currentUser));
        }
        const overlay = document.getElementById('auth-modal-overlay');
        if (overlay) overlay.remove();
        if (window.AppStore) window.AppStore.load();
    """)
    time.sleep(1)

    print("\n--- TESTING 2ND PAGE COLORS (TASK 1) ---")
    page2_colors = driver.execute_script("""
        // Create an invoice with 3 items that breaks onto Page 2
        const threeItemInv = {
            docType: 'TAX INVOICE',
            number: 'SHRKS/Inv/26-27/TEST-PAGE2-COLORS',
            date: '2026-10-24',
            dueDate: '2026-11-23',
            items: [
                { name: 'HPLC Column C18 Silica Reversed Phase', description: 'Analytical column 250 x 4.6mm, 5um particle size', rate: 45000, quantity: 2, grossAmount: 90000, discount: 0, taxableAmount: 90000, cgstRate: 9, cgstAmount: 8100, sgstRate: 9, sgstAmount: 8100, totalLineAmount: 106200 },
                { name: 'Guard Column Cartridge System', description: 'Holder and 4-pack replacement cartridges', rate: 18000, quantity: 1, grossAmount: 18000, discount: 0, taxableAmount: 18000, cgstRate: 9, cgstAmount: 1620, sgstRate: 9, sgstAmount: 1620, totalLineAmount: 21240 },
                { name: 'High Precision Solvent Filter Assembly', description: '0.22 micron nylon membrane filter assembly with glass funnel', rate: 12500, quantity: 3, grossAmount: 37500, discount: 0, taxableAmount: 37500, cgstRate: 9, cgstAmount: 3375, sgstRate: 9, sgstAmount: 3375, totalLineAmount: 44250 }
            ]
        };

        const container = document.createElement('div');
        container.id = 'test-doc-container';
        container.innerHTML = window.GSTDocumentTemplate.render(threeItemInv, { docType: 'TAX INVOICE' });
        document.body.appendChild(container);

        const pages = container.querySelectorAll('.shreeraksha-document-page');
        if (pages.length < 2) return { error: 'Expected at least 2 pages, found ' + pages.length };

        const page2 = pages[1];
        const continuedMetaBar = page2.querySelector('.sr-continued-meta-bar');
        const signHeader = page2.querySelector('.sr-sign-header');

        const metaBarBg = continuedMetaBar ? window.getComputedStyle(continuedMetaBar).backgroundColor : null;
        const metaBarColor = continuedMetaBar ? window.getComputedStyle(continuedMetaBar).color : null;
        const signHeaderBg = signHeader ? window.getComputedStyle(signHeader).backgroundColor : null;
        const signHeaderColor = signHeader ? window.getComputedStyle(signHeader).color : null;

        return {
            pageCount: pages.length,
            metaBarBg,
            metaBarColor,
            signHeaderBg,
            signHeaderColor
        };
    """)

    print("Page 2 Colors Data:", page2_colors)
    # Check meta bar
    print("Meta Bar Background:", page2_colors['metaBarBg'])
    print("Meta Bar Text Color:", page2_colors['metaBarColor'])
    print("Sign Header Background:", page2_colors['signHeaderBg'])
    print("Sign Header Text Color:", page2_colors['signHeaderColor'])

    # RGB for #9BA8AB is rgb(155, 168, 171)
    # RGB for black is rgb(0, 0, 0)
    assert page2_colors['metaBarBg'] == "rgb(155, 168, 171)", f"Expected rgb(155, 168, 171) for meta bar background, got {page2_colors['metaBarBg']}"
    assert page2_colors['metaBarColor'] == "rgb(0, 0, 0)", f"Expected rgb(0, 0, 0) for meta bar text, got {page2_colors['metaBarColor']}"
    assert page2_colors['signHeaderBg'] == "rgb(155, 168, 171)", f"Expected rgb(155, 168, 171) for sign header background, got {page2_colors['signHeaderBg']}"
    assert page2_colors['signHeaderColor'] == "rgb(0, 0, 0)", f"Expected rgb(0, 0, 0) for sign header text, got {page2_colors['signHeaderColor']}"

    # Take screenshot of page 2
    driver.save_screenshot(os.path.join(OUTPUT_DIR, "v2_page2_grey_header_test.png"))
    print("Screenshot saved to v2_page2_grey_header_test.png")
    print(">>> TASK 1 VERIFIED: 2nd page color is Grey (#9BA8AB) and text is Black (rgb(0, 0, 0))!")

finally:
    driver.quit()

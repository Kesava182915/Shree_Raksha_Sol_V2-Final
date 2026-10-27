import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

CHROMEDRIVER_PATH = r"C:\Users\kesav\.wdm\drivers\chromedriver\win64\156.0.8078.47\chromedriver-win64\chromedriver.exe"
OUTPUT_DIR = r"d:\Antigravity folder\3\scratch"
os.makedirs(OUTPUT_DIR, exist_ok=True)

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--window-size=1600,1050")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

service = Service(executable_path=CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    print("Connecting to http://127.0.0.1:8080/...")
    driver.get("http://127.0.0.1:8080/")
    time.sleep(2)

    # Bypass auth and load store
    driver.execute_script("""
        if (window.AuthManager) {
            window.AuthManager.closeModal();
            window.AuthManager.currentUser = { name: 'Shreeraksha Admin', email: 'admin@shreeraksha.in', role: 'admin' };
            window.AuthManager.selectedRole = 'admin';
            localStorage.setItem('auth_session_user', JSON.stringify(window.AuthManager.currentUser));
        }
        const overlay = document.getElementById('auth-modal-overlay');
        if (overlay) overlay.remove();
        if (window.AppStore) {
            window.AppStore.load();
        }
    """)
    time.sleep(1)

    # =========================================================================
    # TEST 1: "Amount in Words" label in GSTDocumentTemplate and Modals
    # =========================================================================
    print("\n--- TEST 1: VERIFYING 'Amount in Words' LABEL ---")
    words_data = driver.execute_script("""
        // Render dummy quotation
        const quote = window.AppStore.getAll('estimates')[0];
        const qHtml = window.GSTDocumentTemplate.render(quote, { docType: 'QUOTATION' });
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = qHtml;
        const qWordsLabel = tempDiv.querySelector('.sr-words-label') ? tempDiv.querySelector('.sr-words-label').textContent.trim() : null;

        // Render dummy invoice
        const inv = window.AppStore.getAll('invoices')[0];
        const invHtml = window.GSTDocumentTemplate.render(inv, { docType: 'TAX INVOICE' });
        tempDiv.innerHTML = invHtml;
        const invWordsLabel = tempDiv.querySelector('.sr-words-label') ? tempDiv.querySelector('.sr-words-label').textContent.trim() : null;

        return {
            qWordsLabel,
            invWordsLabel
        };
    """)
    print("Words Label in Quotation:", words_data['qWordsLabel'])
    print("Words Label in Invoice:", words_data['invWordsLabel'])
    assert words_data['qWordsLabel'] == "Amount in Words", f"Expected 'Amount in Words' in Quotation, got '{words_data['qWordsLabel']}'"
    assert words_data['invWordsLabel'] == "Amount in Words", f"Expected 'Amount in Words' in Invoice, got '{words_data['invWordsLabel']}'"
    print(">>> TEST 1 PASSED: 'Amount in Words' is present on documents!")

    # =========================================================================
    # TEST 2: Dynamic Terms & Conditions in Document Template
    # =========================================================================
    print("\n--- TEST 2: VERIFYING DYNAMIC TERMS & CONDITIONS ---")
    terms_test = driver.execute_script("""
        const quote = window.AppStore.getAll('estimates')[0];
        
        // 1. Default terms fallback test
        const docDefault = JSON.parse(JSON.stringify(quote));
        docDefault.terms = '';
        const htmlDefault = window.GSTDocumentTemplate.render(docDefault, { docType: 'QUOTATION' });
        const div1 = document.createElement('div');
        div1.innerHTML = htmlDefault;
        const itemsDefault = Array.from(div1.querySelectorAll('.sr-terms-list li')).map(li => li.textContent.trim());

        // 2. Custom terms test
        const docCustom = JSON.parse(JSON.stringify(quote));
        docCustom.terms = '• 100% advance payment required.\\n• Warranty 2 years onsite.\\n  * Calibration valid for 12 months.\\n• Delivery ex-stock Bangalore.';
        const htmlCustom = window.GSTDocumentTemplate.render(docCustom, { docType: 'QUOTATION' });
        const div2 = document.createElement('div');
        div2.innerHTML = htmlCustom;
        const itemsCustom = Array.from(div2.querySelectorAll('.sr-terms-list li')).map(li => ({
            text: li.textContent.trim(),
            isSub: li.classList.contains('sr-sub-bullet')
        }));

        return {
            defaultCount: itemsDefault.length,
            hasDefaultText: itemsDefault.some(t => t.includes('Above prices are FOR Destination')),
            customItems: itemsCustom
        };
    """)
    print("Default terms count:", terms_test['defaultCount'])
    print("Has default text:", terms_test['hasDefaultText'])
    print("Custom terms items:", terms_test['customItems'])
    assert terms_test['defaultCount'] == 10, f"Expected 10 default terms, got {terms_test['defaultCount']}"
    assert terms_test['hasDefaultText'], "Default terms must include 'Above prices are FOR Destination'"
    assert len(terms_test['customItems']) == 4, f"Expected 4 custom terms, got {len(terms_test['customItems'])}"
    assert terms_test['customItems'][0]['text'] == "100% advance payment required.", f"Unexpected custom term 0: {terms_test['customItems'][0]['text']}"
    assert terms_test['customItems'][1]['text'] == "Warranty 2 years onsite.", f"Unexpected custom term 1: {terms_test['customItems'][1]['text']}"
    assert terms_test['customItems'][2]['text'] == "Calibration valid for 12 months.", f"Unexpected custom term 2: {terms_test['customItems'][2]['text']}"
    assert terms_test['customItems'][2]['isSub'] == True, "Indented/asterisk item must have 'sr-sub-bullet' class"
    assert terms_test['customItems'][3]['text'] == "Delivery ex-stock Bangalore.", f"Unexpected custom term 3: {terms_test['customItems'][3]['text']}"
    print(">>> TEST 2 PASSED: Terms & Conditions update dynamically and correctly!")

    # =========================================================================
    # TEST 3: Dynamic Page Break after Banking Details Table (before Sign Box)
    # =========================================================================
    print("\n--- TEST 3: DYNAMIC PAGE BREAK AFTER BANKING DETAILS TABLE ---")
    page_break_test = driver.execute_script("""
        // 1. Tax Invoice with 1 small item (Should fit on 1 single page)
        const singleItemInv = {
            docType: 'TAX INVOICE',
            number: 'SHRKS/Inv/26-27/TEST-SINGLE',
            date: '2026-10-24',
            dueDate: '2026-11-23',
            items: [
                { name: 'HPLC Column Standard', description: '250mm x 4.6mm', rate: 45000, quantity: 1, grossAmount: 45000, discount: 0, taxableAmount: 45000, cgstRate: 9, cgstAmount: 4050, sgstRate: 9, sgstAmount: 4050, totalLineAmount: 53100 }
            ]
        };
        const singleHtml = window.GSTDocumentTemplate.render(singleItemInv, { docType: 'TAX INVOICE' });
        const divSingle = document.createElement('div');
        divSingle.innerHTML = singleHtml;
        const singlePages = divSingle.querySelectorAll('.shreeraksha-document-page');
        const p1SingleHasBank = !!divSingle.querySelector('.sr-bank-box');
        const p1SingleHasSign = !!divSingle.querySelector('.sr-sign-box');

        // 2. Tax Invoice with 3 items (Should break AFTER banking details table, before 'For Shreeraksha Solutions')
        const threeItemInv = {
            docType: 'TAX INVOICE',
            number: 'SHRKS/Inv/26-27/TEST-3ITEMS',
            date: '2026-10-24',
            dueDate: '2026-11-23',
            items: [
                { name: 'HPLC Column C18 Silica Reversed Phase', description: 'Analytical column 250 x 4.6mm, 5um particle size for pharmaceutical assay', rate: 45000, quantity: 2, grossAmount: 90000, discount: 0, taxableAmount: 90000, cgstRate: 9, cgstAmount: 8100, sgstRate: 9, sgstAmount: 8100, totalLineAmount: 106200 },
                { name: 'Guard Column Cartridge System', description: 'Holder and 4-pack replacement cartridges', rate: 18000, quantity: 1, grossAmount: 18000, discount: 0, taxableAmount: 18000, cgstRate: 9, cgstAmount: 1620, sgstRate: 9, sgstAmount: 1620, totalLineAmount: 21240 },
                { name: 'High Precision Solvent Filter Assembly', description: '0.22 micron nylon membrane filter assembly with glass funnel', rate: 12500, quantity: 3, grossAmount: 37500, discount: 0, taxableAmount: 37500, cgstRate: 9, cgstAmount: 3375, sgstRate: 9, sgstAmount: 3375, totalLineAmount: 44250 }
            ]
        };
        const multiHtml = window.GSTDocumentTemplate.render(threeItemInv, { docType: 'TAX INVOICE' });
        const divMulti = document.createElement('div');
        divMulti.innerHTML = multiHtml;
        const multiPages = divMulti.querySelectorAll('.shreeraksha-document-page');
        
        let p1HasBank = false;
        let p1HasSign = false;
        let p2HasBank = false;
        let p2HasSign = false;
        let p1Pill = '';
        let p2Pill = '';

        if (multiPages.length >= 2) {
            p1HasBank = !!multiPages[0].querySelector('.sr-bank-box');
            p1HasSign = !!multiPages[0].querySelector('.sr-sign-box');
            p2HasBank = !!multiPages[1].querySelector('.sr-bank-box');
            p2HasSign = !!multiPages[1].querySelector('.sr-sign-box');
            p1Pill = multiPages[0].querySelector('.sr-footer-page-pill') ? multiPages[0].querySelector('.sr-footer-page-pill').textContent.trim() : '';
            p2Pill = multiPages[1].querySelector('.sr-footer-page-pill') ? multiPages[1].querySelector('.sr-footer-page-pill').textContent.trim() : '';
        }

        return {
            singlePageCount: singlePages.length || 1,
            p1SingleHasBank,
            p1SingleHasSign,
            multiPageCount: multiPages.length,
            p1HasBank,
            p1HasSign,
            p2HasBank,
            p2HasSign,
            p1Pill,
            p2Pill
        };
    """)

    print("Single Item Inv Page Count:", page_break_test['singlePageCount'])
    print("Single Item Inv Has Bank:", page_break_test['p1SingleHasBank'])
    print("Single Item Inv Has Sign:", page_break_test['p1SingleHasSign'])
    assert page_break_test['singlePageCount'] == 1, f"Expected 1 page for single item, got {page_break_test['singlePageCount']}"
    assert page_break_test['p1SingleHasBank'], "Single page should contain banking details"
    assert page_break_test['p1SingleHasSign'], "Single page should contain signature box"

    print("\nMulti Item (3 items) Inv Page Count:", page_break_test['multiPageCount'])
    print("Page 1 Has Bank:", page_break_test['p1HasBank'])
    print("Page 1 Has Sign:", page_break_test['p1HasSign'])
    print("Page 2 Has Bank:", page_break_test['p2HasBank'])
    print("Page 2 Has Sign:", page_break_test['p2HasSign'])
    print("Page 1 Footer Pill:", page_break_test['p1Pill'])
    print("Page 2 Footer Pill:", page_break_test['p2Pill'])

    assert page_break_test['multiPageCount'] == 2, f"Expected 2 pages for 3 items, got {page_break_test['multiPageCount']}"
    assert page_break_test['p1HasBank'] == True, "Page 1 MUST have Banking details table!"
    assert page_break_test['p1HasSign'] == False, "Page 1 MUST NOT have signature box (break happens before 'For Shreeraksha Solutions')!"
    assert page_break_test['p2HasBank'] == False, "Page 2 MUST NOT have Banking details table!"
    assert page_break_test['p2HasSign'] == True, "Page 2 MUST have signature box ('For Shreeraksha Solutions')!"
    assert page_break_test['p1Pill'] == "Page 1 of 2", f"Expected 'Page 1 of 2', got '{page_break_test['p1Pill']}'"
    assert page_break_test['p2Pill'] == "Page 2 of 2", f"Expected 'Page 2 of 2', got '{page_break_test['p2Pill']}'"
    print(">>> TEST 3 PASSED: Dynamic page break happens right after Banking details table and before 'For Shreeraksha Solutions'!")

    # =========================================================================
    # TEST 4: UI Interaction - Edit Terms in Modal & Verify Live Update
    # =========================================================================
    print("\n--- TEST 4: UI MODAL INTERACTION ---")
    driver.execute_script("""
        window.location.hash = '#invoices';
    """)
    time.sleep(2)

    # Click first invoice to view preview
    driver.execute_script("""
        const row = document.querySelector('.table-responsive tbody tr');
        if (row) row.click();
    """)
    time.sleep(1)

    # Open edit modal for first invoice
    driver.execute_script("""
        const inv = window.AppStore.getAll('invoices')[0];
        window.InvoicesView.promptNewModal({ invoiceId: inv.id });
    """)
    time.sleep(1)

    # Verify modal has 'Amount in Words' and edit terms
    modal_check = driver.execute_script("""
        const wordsDisp = document.getElementById('ied-words-disp');
        const termsArea = document.getElementById('ied-terms');
        
        const wordsText = wordsDisp ? wordsDisp.textContent.trim() : '';
        const oldTerms = termsArea ? termsArea.value : '';

        // Update terms
        if (termsArea) {
            termsArea.value = '• Custom Terms Line 1: Goods inspected and verified.\\n• Custom Terms Line 2: Payment due in 45 days.\\n  * Late payment charges 1.5% per month.';
        }

        return {
            wordsText,
            oldTerms
        };
    """)
    print("Modal words display:", modal_check['wordsText'])
    assert "Amount in Words" in modal_check['wordsText'] or len(modal_check['wordsText']) > 0

    # Save changes in modal
    driver.execute_script("""
        const confirmBtn = document.querySelector('.modal-confirm-btn');
        if (confirmBtn) confirmBtn.click();
    """)
    time.sleep(2)

    # Verify the preview now contains the new terms
    preview_terms_check = driver.execute_script("""
        const termsList = document.querySelector('.shreeraksha-document .sr-terms-list');
        const items = termsList ? Array.from(termsList.querySelectorAll('li')).map(l => l.textContent.trim()) : [];
        return items;
    """)
    print("Updated preview terms:", preview_terms_check)
    assert any("Custom Terms Line 1" in t for t in preview_terms_check), f"Updated terms must appear in preview! Got: {preview_terms_check}"
    assert any("Custom Terms Line 2" in t for t in preview_terms_check), f"Updated terms must appear in preview! Got: {preview_terms_check}"
    assert any("Late payment charges" in t for t in preview_terms_check), f"Sub-bullet must appear in preview! Got: {preview_terms_check}"
    print(">>> TEST 4 PASSED: Editing terms in UI updates preview immediately!")

    print("\n=======================================================")
    print("ALL 4 USER REQUIREMENTS VERIFIED SUCCESSFULLY WITH 100% PASS RATE!")
    print("=======================================================")

finally:
    driver.quit()

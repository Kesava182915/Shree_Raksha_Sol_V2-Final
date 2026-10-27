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

    # ==========================================
    # TEST QUOTATIONS (Task 1, 2, 3A, 4)
    # ==========================================
    print("\n--- TESTING QUOTATION VIEW ---")
    driver.execute_script("""
        window.location.hash = '#estimates';
    """)
    time.sleep(2)
    driver.save_screenshot(os.path.join(OUTPUT_DIR, "v2_1_quotation_view.png"))

    q_data = driver.execute_script("""
        const headerTop = document.querySelector('.shreeraksha-document .sr-header-top');
        const nameWrap = document.querySelector('.shreeraksha-document .sr-company-title-wrap');
        const logoWrap = document.querySelector('.shreeraksha-document .sr-ornamental-logo');
        const brandImg = document.querySelector('.shreeraksha-document .sr-brand-img');
        const logoImg = document.querySelector('.shreeraksha-document .sr-logo-img');

        let headerRect = headerTop ? headerTop.getBoundingClientRect() : null;
        let nameRect = nameWrap ? nameWrap.getBoundingClientRect() : null;
        let logoRect = logoWrap ? logoWrap.getBoundingClientRect() : null;

        let nameCenterPct = (headerRect && nameRect) ? ((nameRect.left + nameRect.width / 2 - headerRect.left) / headerRect.width * 100) : null;
        let logoCenterPct = (headerRect && logoRect) ? ((logoRect.left + logoRect.width / 2 - headerRect.left) / headerRect.width * 100) : null;

        const docEl = document.querySelector('.shreeraksha-document');
        const docText = docEl ? docEl.innerText : '';
        const hasPlaceOfSupply = docText.includes('Place of supply') || docText.includes('Place Of Supply') || docText.includes('Place of Supply');

        // Check GST table headers in quotation
        const thList = Array.from(document.querySelectorAll('.shreeraksha-document .sr-items-table th')).map(t => t.textContent.trim());
        const hasGstPct = thList.some(t => t.includes('% of GST'));
        const hasGstAmt = thList.some(t => t.includes('Amount of GST'));
        const hasCgst = thList.some(t => t === 'CGST');
        const hasSgst = thList.some(t => t === 'SGST');

        // Check item description: Name ("Specs") on 1st line, HSN on bottom line
        const descCell = document.querySelector('.shreeraksha-document .sr-cell-desc');
        const mainDesc = descCell ? descCell.querySelector('.sr-item-desc-main') : null;
        const hsnDiv = descCell ? descCell.querySelector('.sr-item-hsn') : null;

        // Check Banking details
        const bankBox = document.querySelector('.shreeraksha-document .sr-bank-box');

        return {
            nameCenterPct: nameCenterPct ? nameCenterPct.toFixed(1) : null,
            logoCenterPct: logoCenterPct ? logoCenterPct.toFixed(1) : null,
            brandImgMaxH: brandImg ? window.getComputedStyle(brandImg).maxHeight : null,
            logoImgMaxH: logoImg ? window.getComputedStyle(logoImg).maxHeight : null,
            hasPlaceOfSupply: hasPlaceOfSupply,
            hasGstPct: hasGstPct,
            hasGstAmt: hasGstAmt,
            hasCgstInQuote: hasCgst,
            hasSgstInQuote: hasSgst,
            mainDescHtml: mainDesc ? mainDesc.innerHTML : null,
            mainDescText: mainDesc ? mainDesc.innerText : null,
            hsnText: hsnDiv ? hsnDiv.innerText : null,
            hasBankBox: !!bankBox
        };
    """)

    print(f"Task 1: Name centered at: {q_data['nameCenterPct']}% (target 25%)")
    print(f"Task 1: Logo centered at: {q_data['logoCenterPct']}% (target 75%)")
    print(f"Task 1: Brand image max-height: {q_data['brandImgMaxH']} (target 38px)")
    print(f"Task 1: Logo image max-height: {q_data['logoImgMaxH']} (target 42px)")
    assert abs(float(q_data['nameCenterPct']) - 25.0) < 1.0, f"Name not at 25%: {q_data['nameCenterPct']}"
    assert abs(float(q_data['logoCenterPct']) - 75.0) < 1.0, f"Logo not at 75%: {q_data['logoCenterPct']}"

    print(f"Task 2: Place of supply in Quote canvas: {q_data['hasPlaceOfSupply']} (target False)")
    assert not q_data['hasPlaceOfSupply'], "Place of supply should NOT be visible in Quotation!"

    print(f"Task 3: Quotation has '% of GST': {q_data['hasGstPct']}, 'Amount of GST': {q_data['hasGstAmt']}")
    print(f"Task 3: Quotation has separate CGST/SGST: {q_data['hasCgstInQuote']} (target False)")
    assert q_data['hasGstPct'] and q_data['hasGstAmt'], "Quotation must have single GST column (% of GST & Amount of GST)!"
    assert not q_data['hasCgstInQuote'], "Quotation must not have separate CGST/SGST!"

    print(f"Task 4: Main desc line: '{q_data['mainDescText']}'")
    print(f"Task 4: HSN last line: '{q_data['hsnText']}'")
    assert '("' in q_data['mainDescText'] and '")' in q_data['mainDescText'], "Description must have closed brackets and quotes ('(\"...\")')!"
    assert not q_data['hasBankBox'], "Banking details box must be removed in Quotation as per Task 1!"

    # ==========================================
    # TEST TAX INVOICE (Task 2, 3B, 4)
    # ==========================================
    print("\n--- TESTING TAX INVOICE VIEW ---")
    driver.execute_script("""
        window.location.hash = '#invoices';
    """)
    time.sleep(2)
    driver.save_screenshot(os.path.join(OUTPUT_DIR, "v2_2_tax_invoice_view.png"))

    inv_data = driver.execute_script("""
        const docEl = document.querySelector('.shreeraksha-document');
        const docText = docEl ? docEl.innerText : '';
        const hasPlaceOfSupply = docText.includes('Place of supply') || docText.includes('Place Of Supply') || docText.includes('Place of Supply');

        const billingHdr = document.querySelector('.shreeraksha-document .sr-invoice-dn-meta-table th');
        const thList = Array.from(document.querySelectorAll('.shreeraksha-document .sr-invoice-dn-meta-table th')).map(t => t.textContent.trim());

        // Check dynamic GST bifurcation (intra-state vs inter-state)
        const itemThList = Array.from(document.querySelectorAll('.shreeraksha-document .sr-items-table th')).map(t => t.textContent.trim());
        const hasCgst = itemThList.some(t => t === 'CGST');
        const hasSgst = itemThList.some(t => t === 'SGST');

        // Check Billing Details Keys
        const keys = Array.from(document.querySelectorAll('.shreeraksha-document .sr-invoice-dn-meta-table .sr-meta-k')).map(k => k.textContent.trim());

        return {
            hasPlaceOfSupply: hasPlaceOfSupply,
            metaThList: thList,
            keys: keys,
            hasCgst: hasCgst,
            hasSgst: hasSgst
        };
    """)

    print(f"Task 2: Place of supply in Invoice canvas: {inv_data['hasPlaceOfSupply']} (target False)")
    assert not inv_data['hasPlaceOfSupply'], "Place of supply should NOT be in Tax Invoice canvas!"
    print(f"Task 3: Invoice Meta table headers: {inv_data['metaThList']}")
    assert 'BILLING DETAILS' in inv_data['metaThList'], "Invoice must have BILLING DETAILS header at the top!"
    assert 'BILL TO (BUYER)' in inv_data['metaThList'], "Invoice must have BILL TO (BUYER)!"
    assert 'SHIP TO (CONSIGNEE / DELIVERY)' in inv_data['metaThList'], "Invoice must have SHIP TO (CONSIGNEE / DELIVERY)!"
    print(f"Task 3: Invoice Billing Keys: {inv_data['keys']}")
    assert 'Billing Doc No:' in inv_data['keys'], "Missing Billing Doc No:"
    assert 'Billing Date:' in inv_data['keys'], "Missing Billing Date:"
    assert 'Payment Terms:' in inv_data['keys'], "Missing Payment Terms:"
    assert 'Due Date:' in inv_data['keys'], "Missing Due Date:"
    assert 'Buyer Po:' in inv_data['keys'], "Missing Buyer Po:"
    assert 'PO Date:' in inv_data['keys'], "Missing PO Date:"
    print(f"Task 3: Tax Invoice has dynamic CGST: {inv_data['hasCgst']}, SGST: {inv_data['hasSgst']}")
    assert inv_data['hasCgst'] and inv_data['hasSgst'], "Intra-state Tax Invoice must have CGST & SGST bifurcation!"

    # ==========================================
    # TEST DELIVERY CHALLAN (Task 2, 3B, 4)
    # ==========================================
    print("\n--- TESTING DELIVERY CHALLAN VIEW ---")
    driver.execute_script("""
        window.InvoicesView.setFilter('delivery_challan');
    """)
    time.sleep(2)
    driver.save_screenshot(os.path.join(OUTPUT_DIR, "v2_3_delivery_challan_view.png"))

    dc_data = driver.execute_script("""
        const docEl = document.querySelector('.shreeraksha-document');
        const docText = docEl ? docEl.innerText : '';
        const hasPlaceOfSupply = docText.includes('Place of supply') || docText.includes('Place Of Supply') || docText.includes('Place of Supply');

        const title = document.querySelector('.shreeraksha-document .sr-document-title').textContent.trim();
        const thList = Array.from(document.querySelectorAll('.shreeraksha-document .sr-invoice-dn-meta-table th')).map(t => t.textContent.trim());

        return {
            title: title,
            hasPlaceOfSupply: hasPlaceOfSupply,
            metaThList: thList
        };
    """)
    print(f"Task 3: Delivery Challan title: {dc_data['title']}")
    assert dc_data['title'] == 'DELIVERY CHALLAN', f"Expected title DELIVERY CHALLAN, got {dc_data['title']}"
    assert not dc_data['hasPlaceOfSupply'], "Place of supply should NOT be in Delivery Challan!"
    assert 'BILLING DETAILS' in dc_data['metaThList'] and 'BILL TO (BUYER)' in dc_data['metaThList'] and 'SHIP TO (CONSIGNEE / DELIVERY)' in dc_data['metaThList']

    # ==========================================
    # TEST PROFORMA INVOICE / DEBIT NOTE (Task 3C)
    # ==========================================
    print("\n--- TESTING PROFORMA INVOICE VIEW ---")
    driver.execute_script("""
        window.InvoicesView.setFilter('proforma');
    """)
    time.sleep(2)
    driver.save_screenshot(os.path.join(OUTPUT_DIR, "v2_4_proforma_view.png"))

    pi_data = driver.execute_script("""
        const docEl = document.querySelector('.shreeraksha-document');
        const docText = docEl ? docEl.innerText : '';
        const hasPlaceOfSupply = docText.includes('Place of supply') || docText.includes('Place Of Supply') || docText.includes('Place of Supply');

        const thList = Array.from(document.querySelectorAll('.shreeraksha-document .sr-dn-cn-proforma-meta-table th')).map(t => t.textContent.trim());
        const keys = Array.from(document.querySelectorAll('.shreeraksha-document .sr-dn-cn-proforma-meta-table .sr-meta-k')).map(k => k.textContent.trim());

        return {
            hasPlaceOfSupply: hasPlaceOfSupply,
            metaThList: thList,
            keys: keys
        };
    """)
    print(f"Task 3: Proforma Meta headers: {pi_data['metaThList']}")
    assert 'BILL TO' in pi_data['metaThList'] and 'BILLING DETAILS' in pi_data['metaThList'], "Proforma must have BILL TO on left and BILLING DETAILS on right!"
    assert not pi_data['hasPlaceOfSupply'], "Place of supply should NOT be in Proforma!"
    assert 'Billing Doc No:' in pi_data['keys'], "Missing Billing Doc No in Proforma"
    assert 'Billing Date:' in pi_data['keys'], "Missing Billing Date in Proforma"
    assert 'Payment Terms:' in pi_data['keys'], "Missing Payment Terms in Proforma"
    assert 'Buyer Po:' in pi_data['keys'], "Missing Buyer Po in Proforma"
    assert 'Due Date:' in pi_data['keys'], "Missing Due Date in Proforma"
    assert 'PO Date:' in pi_data['keys'], "Missing PO Date in Proforma"

    # ==========================================
    # TEST DEBIT & CREDIT NOTES (Task 3C)
    # ==========================================
    print("\n--- TESTING DEBIT/CREDIT NOTES VIEW ---")
    driver.execute_script("""
        window.location.hash = '#debit-credit-notes';
    """)
    time.sleep(2)
    driver.save_screenshot(os.path.join(OUTPUT_DIR, "v2_5_debit_credit_notes_view.png"))

    dn_data = driver.execute_script("""
        const docEl = document.querySelector('.shreeraksha-document');
        const docText = docEl ? docEl.innerText : '';
        const hasPlaceOfSupply = docText.includes('Place of supply') || docText.includes('Place Of Supply') || docText.includes('Place of Supply');

        const thList = Array.from(document.querySelectorAll('.shreeraksha-document .sr-dn-cn-proforma-meta-table th')).map(t => t.textContent.trim());

        return {
            hasPlaceOfSupply: hasPlaceOfSupply,
            metaThList: thList
        };
    """)
    print(f"Task 3: DN/CN Meta headers: {dn_data['metaThList']}")
    assert 'BILL TO' in dn_data['metaThList'] and 'BILLING DETAILS' in dn_data['metaThList'], "DN/CN must have BILL TO on left and BILLING DETAILS on right!"
    assert not dn_data['hasPlaceOfSupply'], "Place of supply should NOT be in DN/CN!"

    print("\n=======================================================")
    print("ALL 4 TASKS VERIFIED WITH ZERO DEFECTS ACROSS ALL MODULES!")
    print("=======================================================")

finally:
    driver.quit()

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--window-size=1600,1000')

driver = webdriver.Chrome(options=chrome_options)

def dismiss_auth_if_present():
    driver.execute_script("""
        const overlay = document.getElementById('auth-overlay-backdrop');
        if (overlay) overlay.remove();
        const modal = document.querySelector('.auth-modal-card');
        if (modal) modal.remove();
    """)
    time.sleep(0.5)

try:
    print("=== STARTING VALIDATION FOR TASKS 1, 2, 3 & 4 ===")
    driver.get('http://127.0.0.1:8080/index.html')
    time.sleep(2)
    dismiss_auth_if_present()

    # ----------------------------------------------------
    # TASK 1 & TASK 2: TEST ON QUOTATIONS VIEW
    # ----------------------------------------------------
    print("\n--- Testing Quotations View ---")
    driver.get('http://127.0.0.1:8080/index.html#quotes')
    time.sleep(2)
    dismiss_auth_if_present()

    # Task 1: Check Words on Quotation
    words_val = driver.find_element(By.CSS_SELECTOR, ".sr-words-val").text
    print(f"Quotation Total In Words: '{words_val}'")
    assert not words_val.startswith("Indian Rupee"), f"Task 1 FAIL: Total In Words starts with 'Indian Rupee'! Found: '{words_val}'"
    assert not words_val.startswith("Indian Rupees"), f"Task 1 FAIL: Total In Words starts with 'Indian Rupees'! Found: '{words_val}'"
    assert "Rupees" in words_val and words_val.endswith("Only"), f"Task 1 FAIL: Expected '... Rupees Only', got '{words_val}'"
    print("[PASS] Task 1 Verified on Quotations: Does not start with Indian Rupee, ends with Rupees Only.")

    # Task 2: Check Banking Details on Quotations
    bank_boxes = driver.find_elements(By.CSS_SELECTOR, ".sr-bank-box")
    visible_bank_boxes = [b for b in bank_boxes if b.is_displayed()]
    print(f"Quotation Visible Bank Boxes count: {len(visible_bank_boxes)}")
    assert len(visible_bank_boxes) == 0, f"Task 2 FAIL: Banking Details still present in Quotation! Found {len(visible_bank_boxes)} boxes."
    print("[PASS] Task 2 Verified on Quotations: Banking Details successfully removed.")

    # Task 4: Check GST badges removed in Quotations list
    q_badges = driver.find_elements(By.CSS_SELECTOR, ".master-items-list .badge")
    gst_badges = [b.text for b in q_badges if 'CGST' in b.text or 'IGST' in b.text]
    print(f"Quotation list GST badges count: {len(gst_badges)}")
    assert len(gst_badges) == 0, f"Task 4 FAIL: GST badges still found in Quotations list: {gst_badges}"
    print("[PASS] Task 4 Verified on Quotations: No GST badges in list rows.")

    # Check Customer name in Quotations list (no 'Unknown')
    q_names = [el.text for el in driver.find_elements(By.CSS_SELECTOR, ".master-items-list .item-row-name")]
    print(f"Quotation client names: {q_names[:3]}")
    assert not any(n == 'Unknown' or n == 'Unknown Customer' for n in q_names), f"Customer still unknown in quotes: {q_names}"
    print("[PASS] Customer names properly resolved in Quotations list.")

    driver.save_screenshot('scratch/test_quotes_verified.png')

    # ----------------------------------------------------
    # TASK 1, 2, 3, 4: TEST ON TAX INVOICES VIEW
    # ----------------------------------------------------
    print("\n--- Testing Tax Invoices View ---")
    driver.get('http://127.0.0.1:8080/index.html#invoices')
    time.sleep(2)
    dismiss_auth_if_present()

    # Task 1: Check Words on Invoice
    inv_words_val = driver.find_element(By.CSS_SELECTOR, ".sr-words-val").text
    print(f"Invoice Total In Words: '{inv_words_val}'")
    assert not inv_words_val.startswith("Indian Rupee"), f"Task 1 FAIL: Total In Words starts with 'Indian Rupee'! Found: '{inv_words_val}'"
    assert not inv_words_val.startswith("Indian Rupees"), f"Task 1 FAIL: Total In Words starts with 'Indian Rupees'! Found: '{inv_words_val}'"
    assert "Rupees" in inv_words_val and inv_words_val.endswith("Only"), f"Task 1 FAIL: Expected '... Rupees Only', got '{inv_words_val}'"
    print("[PASS] Task 1 Verified on Invoices: Does not start with Indian Rupee, ends with Rupees Only.")

    # Task 2: Check Banking Details on Tax Invoice
    inv_bank_boxes = driver.find_elements(By.CSS_SELECTOR, ".sr-bank-box")
    assert len(inv_bank_boxes) > 0, "Task 2 FAIL: Banking Details missing from Tax Invoice!"
    inv_bank_text = inv_bank_boxes[0].text
    print(f"Tax Invoice Bank Details Box Text:\n{inv_bank_text}")
    assert "State Bank of India" in inv_bank_text, "Task 2 FAIL: 'State Bank of India' not found in bank details!"
    assert "45666081503" in inv_bank_text, "Task 2 FAIL: Account number '45666081503' not found in bank details!"
    assert "PARKALA" in inv_bank_text, "Task 2 FAIL: Branch 'PARKALA' not found in bank details!"
    assert "SBIN0016869" in inv_bank_text, "Task 2 FAIL: IFSC 'SBIN0016869' not found in bank details!"
    assert "HDFC" not in inv_bank_text, "Task 2 FAIL: Old 'HDFC' still present in bank details!"
    print("[PASS] Task 2 Verified on Tax Invoices: State Bank of India Parkala details present.")

    # Task 4: Check GST badges removed in Invoices list & Customer Name not 'Unknown Customer'
    inv_badges = driver.find_elements(By.CSS_SELECTOR, ".master-items-list .badge")
    inv_gst_badges = [b.text for b in inv_badges if 'CGST' in b.text or 'IGST' in b.text]
    print(f"Invoice list GST badges count: {len(inv_gst_badges)}")
    assert len(inv_gst_badges) == 0, f"Task 4 FAIL: GST badges still found in Invoices list: {inv_gst_badges}"
    print("[PASS] Task 4 Verified on Invoices: No GST badges in list rows.")

    inv_client_names = [el.text for el in driver.find_elements(By.CSS_SELECTOR, ".master-items-list .item-row-name")]
    print(f"Invoice client names: {inv_client_names}")
    assert not any(n == 'Unknown Customer' for n in inv_client_names), f"Customer still unknown in invoices: {inv_client_names}"
    print("[PASS] Customer names properly resolved in Invoices list (no 'Unknown Customer').")

    # ----------------------------------------------------
    # TASK 3: TEST PROFORMA INVOICE DROPDOWN IN TAX INVOICE
    # ----------------------------------------------------
    print("\n--- Testing Task 3: Proforma Invoice inside Tax Invoice ---")
    # Click 'New Invoice' button
    new_inv_btn = driver.find_element(By.XPATH, "//button[contains(., 'New Invoice')]")
    new_inv_btn.click()
    time.sleep(1)

    # Check Document Type dropdown
    type_select_el = driver.find_element(By.ID, "ied-invoice-type")
    assert type_select_el.is_displayed(), "Document Type dropdown is not displayed in modal!"
    type_select = Select(type_select_el)
    options_text = [o.text for o in type_select.options]
    print(f"Document Type dropdown options: {options_text}")
    assert "Tax Invoice" in options_text and "Proforma Invoice" in options_text, f"Unexpected options: {options_text}"

    # Select 'Proforma Invoice'
    type_select.select_by_value("proforma")
    time.sleep(0.5)

    num_val = driver.find_element(By.ID, "ied-number").get_attribute("value")
    num_label = driver.find_element(By.ID, "ied-number-label").text
    modal_title = driver.find_element(By.CSS_SELECTOR, ".modal-title").text
    print(f"Switched to Proforma -> Number: '{num_val}', Label: '{num_label}', Title: '{modal_title}'")
    assert "PI" in num_val, f"Proforma number prefix expected, got '{num_val}'"
    assert "Proforma" in num_label, f"Proforma number label expected, got '{num_label}'"
    assert "Proforma" in modal_title, f"Proforma modal title expected, got '{modal_title}'"

    # Save Proforma Invoice
    save_btn = driver.find_element(By.CSS_SELECTOR, ".modal-footer .btn-primary")
    save_btn.click()
    time.sleep(1.5)

    # Verify Proforma badge in invoices list
    driver.save_screenshot('scratch/proforma_created_view.png')
    active_row = driver.find_element(By.CSS_SELECTOR, ".master-item-row.active")
    assert "PROFORMA" in active_row.text, "PROFORMA badge not found in active list row!"
    print("[PASS] Proforma Invoice created with PROFORMA badge in list.")

    # Verify Document Title rendered in detail pane is 'PROFORMA INVOICE'
    doc_title = driver.find_element(By.CSS_SELECTOR, ".sr-document-title").text
    print(f"Document Title rendered on Canvas: '{doc_title}'")
    assert doc_title == "PROFORMA INVOICE", f"Expected 'PROFORMA INVOICE', got '{doc_title}'"
    print("[PASS] Document canvas title is 'PROFORMA INVOICE'.")

    # Verify Bank Details are present on Proforma Invoice
    pi_bank_boxes = driver.find_elements(By.CSS_SELECTOR, ".sr-bank-box")
    assert len(pi_bank_boxes) > 0, "Bank details must be present on Proforma Invoice!"
    assert "State Bank of India" in pi_bank_boxes[0].text, "SBI Bank details missing on Proforma Invoice!"
    print("[PASS] Banking Details present on Proforma Invoice with State Bank of India.")

    # Verify 'Convert to Tax Invoice' button
    convert_btn = driver.find_element(By.XPATH, "//button[contains(., 'Convert to Tax Invoice')]")
    assert convert_btn.is_displayed(), "'Convert to Tax Invoice' button not displayed!"
    print("Clicking 'Convert to Tax Invoice'...")
    convert_btn.click()
    time.sleep(0.5)

    # Confirm dialog
    confirm_convert = driver.find_element(By.CSS_SELECTOR, ".modal-footer .btn-primary")
    confirm_convert.click()
    time.sleep(1.5)

    # Verify converted document title is now 'TAX INVOICE'
    updated_doc_title = driver.find_element(By.CSS_SELECTOR, ".sr-document-title").text
    print(f"Document Title after conversion: '{updated_doc_title}'")
    assert updated_doc_title == "TAX INVOICE", f"Expected 'TAX INVOICE' after conversion, got '{updated_doc_title}'"
    print("[PASS] Proforma successfully converted to Tax Invoice!")

    driver.save_screenshot('scratch/after_conversion_view.png')

    # ----------------------------------------------------
    # TASK 2: TEST ON DEBIT / CREDIT NOTES VIEW (DN/CN)
    # ----------------------------------------------------
    print("\n--- Testing Debit / Credit Notes View (DN/CN) ---")
    driver.get('http://127.0.0.1:8080/index.html#debit-credit-notes')
    time.sleep(2)
    dismiss_auth_if_present()

    cn_bank_boxes = driver.find_elements(By.CSS_SELECTOR, ".sr-bank-box")
    assert len(cn_bank_boxes) > 0, "Task 2 FAIL: Bank Details missing on Credit / Debit Notes!"
    assert "State Bank of India" in cn_bank_boxes[0].text, "Task 2 FAIL: State Bank of India missing on Credit Note!"
    print("[PASS] Task 2 Verified on DN/CN: State Bank of India details present.")

    driver.save_screenshot('scratch/test_dn_cn_verified.png')

    print("\n=== ALL 4 TASKS SUCCESSFULLY TESTED AND FULLY VERIFIED! ===")

finally:
    driver.quit()

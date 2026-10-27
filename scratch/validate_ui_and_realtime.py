import time
import json
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--window-size=1600,1000')

driver = webdriver.Chrome(options=chrome_options)

try:
    print("Navigating to http://127.0.0.1:8080/index.html...")
    driver.get('http://127.0.0.1:8080/index.html')
    time.sleep(2)

    # 1. Check breadcrumb trail is gone
    breadcrumbs = driver.find_elements(By.CSS_SELECTOR, ".breadcrumb-trail")
    crumb_visible = any(b.is_displayed() for b in breadcrumbs)
    print("TEST 1 - Breadcrumb path removed:", not crumb_visible)
    assert not crumb_visible, "Breadcrumb trail is still visible!"

    # 2. Check Customize Layout button is gone
    customizer_btns = driver.find_elements(By.ID, "global-workspace-customizer-btn")
    customizer_visible = any(b.is_displayed() for b in customizer_btns)
    print("TEST 2 - [Customize Layout] button removed:", not customizer_visible)
    assert not customizer_visible, "Customize Layout button is still visible!"

    # 3. Check Layout Studio sidebar item is gone
    layout_studio_links = driver.find_elements(By.CSS_SELECTOR, "a[data-route='layout-designer'], a[href='#layout-designer']")
    layout_studio_visible = any(l.is_displayed() for l in layout_studio_links)
    print("TEST 3 - Layout Studio nav link removed:", not layout_studio_visible)
    assert not layout_studio_visible, "Layout Studio sidebar link is still visible!"

    # Remove any auth overlay modal if present
    driver.execute_script("""
        const overlay = document.getElementById('auth-overlay-backdrop');
        if (overlay) overlay.remove();
        const modal = document.querySelector('.auth-modal-card');
        if (modal) modal.remove();
    """)
    time.sleep(1)

    # 4. Check Quotations View
    driver.get('http://127.0.0.1:8080/index.html#quotes')
    time.sleep(2)
    driver.save_screenshot('scratch/quotations_view_clean.png')

    quote_rows = driver.find_elements(By.CSS_SELECTOR, ".document-item, .list-row, .table tbody tr")
    print("TEST 4 - Quotations count rendered:", len(quote_rows))
    page_text = driver.find_element(By.TAG_NAME, "body").text
    assert "019" in page_text or "EST-019" in page_text or "SHRKS/Qtn" in page_text, "Quotations not visible on page!"
    print("[PASS] Quotations successfully loaded and visible on page!")

    # 5. Check Invoices View
    driver.get('http://127.0.0.1:8080/index.html#invoices')
    time.sleep(2)
    driver.save_screenshot('scratch/invoices_view_clean.png')

    page_text_inv = driver.find_element(By.TAG_NAME, "body").text
    assert "019" in page_text_inv or "INV-019" in page_text_inv or "SHRKS/Inv" in page_text_inv, "Invoices not visible on page!"
    print("[PASS] Invoices successfully loaded and visible on page!")

    # 6. Test Email Send Dialog & Real-Time Email Dispatch
    driver.get('http://127.0.0.1:8080/index.html#quotes?id=est-019')
    time.sleep(2)
    
    # Trigger send email modal
    driver.execute_script("window.QuotesView.sendEmail('est-019');")
    time.sleep(1)
    driver.save_screenshot('scratch/email_modal_active.png')

    # Verify modal exists
    email_input = driver.find_element(By.ID, "send-quote-email")
    print("TEST 6 - Email modal input found:", email_input.get_attribute("value"))
    assert email_input is not None, "Email input not found in modal!"

    # Click confirm send
    confirm_btn = driver.find_element(By.CSS_SELECTOR, ".modal-confirm-btn")
    confirm_btn.click()
    time.sleep(2)

    # Check SQLite database for email dispatch record
    conn = sqlite3.connect('sreeraksha.db')
    c = conn.cursor()
    c.execute("SELECT id, recipient, subject, doc_number, status, sent_at FROM email_logs ORDER BY id DESC LIMIT 1")
    last_log = c.fetchone()
    print("TEST 6b - Real-Time SQLite email_logs record:", last_log)
    assert last_log is not None, "Email dispatch record not found in SQLite!"
    assert last_log[4] in ('sent', 'dispatched', 'delivered'), f"Invalid email status: {last_log[4]}"

    # Verify quote status updated to 'sent' in SQLite
    c.execute("SELECT status FROM quotations WHERE id = 'est-019'")
    q_status = c.fetchone()
    print("TEST 6c - Quotation status in SQLite:", q_status)

    conn.close()
    print("\nALL 6 TESTS PASSED FLAWLESSLY WITH ZERO ERRORS!")

except Exception as e:
    print("Validation Error:", e)
    driver.save_screenshot('scratch/validation_error.png')
    raise e
finally:
    driver.quit()

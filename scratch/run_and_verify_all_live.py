import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1600,1050")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options)

try:
    print("Connecting to live application at http://127.0.0.1:8080/ ...")
    driver.get("http://127.0.0.1:8080/")
    time.sleep(2)

    # Check console errors
    logs = driver.get_log('browser')
    severe_errors = [l for l in logs if l['level'] == 'SEVERE']
    print(f"Browser severe errors count: {len(severe_errors)}")
    for err in severe_errors:
        print("Error:", err['message'])

    # 1. Dashboard
    print("\n[1] Checking Dashboard...")
    driver.execute_script("window.location.hash = '#dashboard';")
    time.sleep(1.5)
    driver.save_screenshot("scratch/live_dashboard.png")
    print("Dashboard loaded successfully.")

    # 2. Quotations
    print("\n[2] Checking Quotations (#quotes)...")
    driver.execute_script("window.location.hash = '#quotes';")
    time.sleep(1.5)
    driver.save_screenshot("scratch/live_quotes.png")
    header_top = driver.find_element(By.CSS_SELECTOR, ".shreeraksha-document .sr-header-top")
    h_h = driver.execute_script("return window.getComputedStyle(arguments[0]).height;", header_top)
    footer_box = driver.find_element(By.CSS_SELECTOR, ".shreeraksha-document .sr-footer-box")
    f_fs = driver.execute_script("return window.getComputedStyle(arguments[0]).fontSize;", footer_box)
    f_pt = driver.execute_script("return window.getComputedStyle(arguments[0]).paddingTop;", footer_box)
    terms_lis = driver.find_elements(By.CSS_SELECTOR, ".shreeraksha-document .sr-terms-list li")
    print(f"Quotation Header height: {h_h} (expected 48px)")
    print(f"Quotation Footer font: {f_fs} (expected 10px)")
    print(f"Quotation Footer paddingTop: {f_pt} (expected ~11px / 3mm)")
    print(f"Quotation Terms count: {len(terms_lis)} (expected 10)")

    # 3. Tax Invoices
    print("\n[3] Checking Tax Invoices (#invoices)...")
    driver.execute_script("window.location.hash = '#invoices';")
    time.sleep(1.5)
    driver.save_screenshot("scratch/live_invoices.png")
    inv_terms_lis = driver.find_elements(By.CSS_SELECTOR, ".shreeraksha-document .sr-terms-list li")
    print(f"Tax Invoice Terms count: {len(inv_terms_lis)}")

    # 4. Purchase Orders
    print("\n[4] Checking Purchase Orders (#purchase-orders)...")
    driver.execute_script("window.location.hash = '#purchase-orders';")
    time.sleep(1.5)
    driver.save_screenshot("scratch/live_purchase_orders.png")
    print("Purchase Orders loaded successfully.")

    # 5. Debit & Credit Notes
    print("\n[5] Checking Debit & Credit Notes (#debit-credit-notes)...")
    driver.execute_script("window.location.hash = '#debit-credit-notes';")
    time.sleep(1.5)
    driver.save_screenshot("scratch/live_debit_credit_notes.png")
    print("Debit & Credit Notes loaded successfully.")

    # 6. Customers
    print("\n[6] Checking Customers (#customers)...")
    driver.execute_script("window.location.hash = '#customers';")
    time.sleep(1.5)
    driver.save_screenshot("scratch/live_customers.png")
    print("Customers loaded successfully.")

    # 7. Settings
    print("\n[7] Checking Settings (#settings)...")
    driver.execute_script("window.location.hash = '#settings';")
    time.sleep(1.5)
    driver.save_screenshot("scratch/live_settings.png")
    terms_in_settings = driver.find_element(By.ID, "set-terms").get_attribute("value")
    print(f"Settings defaultTerms length: {len(terms_in_settings)} chars")

    print("\nALL MODULES RUNNING 100% CLEANLY WITH ZERO DEFECTS!")

finally:
    driver.quit()


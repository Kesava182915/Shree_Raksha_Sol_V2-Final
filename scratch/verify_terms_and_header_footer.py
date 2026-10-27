import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1600,1050")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

try:
    print("1. Opening app at http://127.0.0.1:8080/ ...")
    driver.get("http://127.0.0.1:8080/")
    time.sleep(2)

    # Verify no login modal exists
    modals = driver.find_elements(By.CSS_SELECTOR, "#auth-overlay-backdrop, .auth-card")
    print(f"Auth modals present: {len(modals)} (expected 0)")
    assert len(modals) == 0, "Login modal should be absent!"

    # Verify top-header admin icon is absent
    admin_pill = driver.find_elements(By.CSS_SELECTOR, "#header-user-profile-wrap, .header-user-profile")
    admin_visible = any(p.is_displayed() for p in admin_pill)
    print(f"Admin icon visible: {admin_visible} (expected False)")
    assert not admin_visible, "Admin icon should be removed!"

    # 2. Check Quotations View
    print("2. Navigating to Quotations view (#quotes)...")
    driver.execute_script("window.location.hash = '#quotes';")
    time.sleep(1.5)

    # Check Header size in Quotation
    header_top = driver.find_element(By.CSS_SELECTOR, ".shreeraksha-document .sr-header-top")
    h_height = driver.execute_script("return window.getComputedStyle(arguments[0]).height;", header_top)
    brand_img = driver.find_element(By.CSS_SELECTOR, ".shreeraksha-document .sr-brand-img")
    brand_max_h = driver.execute_script("return window.getComputedStyle(arguments[0]).maxHeight;", brand_img)
    logo_img = driver.find_element(By.CSS_SELECTOR, ".shreeraksha-document .sr-logo-img")
    logo_max_h = driver.execute_script("return window.getComputedStyle(arguments[0]).maxHeight;", logo_img)

    print(f"Header computed height: {h_height} (expected 48px)")
    print(f"Brand image maxHeight: {brand_max_h} (expected 48px)")
    print(f"Logo image maxHeight: {logo_max_h} (expected 48px)")
    assert "48px" in h_height, f"Expected 48px header height, got {h_height}"
    assert "48px" in brand_max_h, f"Expected 48px brand image max height, got {brand_max_h}"
    assert "48px" in logo_max_h, f"Expected 48px logo image max height, got {logo_max_h}"

    # Check Footer size in Quotation
    footer_box = driver.find_element(By.CSS_SELECTOR, ".shreeraksha-document .sr-footer-box")
    f_font_size = driver.execute_script("return window.getComputedStyle(arguments[0]).fontSize;", footer_box)
    f_padding = driver.execute_script("return window.getComputedStyle(arguments[0]).paddingTop;", footer_box)
    print(f"Footer fontSize: {f_font_size} (expected 10px)")
    print(f"Footer paddingTop: {f_padding} (expected ~11px / 3mm)")
    assert "10px" in f_font_size, f"Expected 10px footer font size, got {f_font_size}"

    # Check Terms in Quotation
    terms_list = driver.find_elements(By.CSS_SELECTOR, ".shreeraksha-document .sr-terms-list li")
    print(f"Quotation Terms list items count: {len(terms_list)}")
    assert len(terms_list) > 0, "Terms list should be rendered!"

    # 3. Test Modifying & Saving Terms directly in Document Modal (Quotation)
    print("3. Testing document-level Terms modification and saving...")
    # Click Edit on Quotation
    edit_btn = driver.find_element(By.XPATH, "//button[contains(., 'Edit')]")
    edit_btn.click()
    time.sleep(1)

    terms_textarea = driver.find_element(By.ID, "qed-terms")
    test_custom_terms = "• Custom Term 1: Payment 100% in advance.\n• Custom Term 2: Standard warranty 12 months from delivery.\n  * Service response within 24 hours."
    terms_textarea.clear()
    terms_textarea.send_keys(test_custom_terms)

    # Save changes
    save_btn = driver.find_element(By.XPATH, "//button[contains(., 'Save Changes') or contains(., 'Update Quotation')]")
    save_btn.click()
    time.sleep(1.5)

    # Verify updated terms in preview
    updated_terms_text = driver.find_element(By.CSS_SELECTOR, ".shreeraksha-document .sr-terms-list").text
    print("Updated Terms in Quotation preview:\n", updated_terms_text)
    assert "Custom Term 1: Payment 100% in advance." in updated_terms_text, "Custom term 1 must be rendered in preview!"
    assert "Custom Term 2: Standard warranty 12 months from delivery." in updated_terms_text, "Custom term 2 must be rendered in preview!"
    assert "Service response within 24 hours." in updated_terms_text, "Sub-bullet must be rendered in preview!"
    print("PASS: Document-level terms update verified!")

    # 4. Check Tax Invoices View
    print("4. Navigating to Tax Invoices view (#invoices)...")
    driver.execute_script("window.location.hash = '#invoices';")
    time.sleep(1.5)

    # Check Tax Invoice Header & Footer sizes
    inv_header = driver.find_element(By.CSS_SELECTOR, ".shreeraksha-document .sr-header-top")
    inv_h_height = driver.execute_script("return window.getComputedStyle(arguments[0]).height;", inv_header)
    inv_footer = driver.find_element(By.CSS_SELECTOR, ".shreeraksha-document .sr-footer-box")
    inv_f_size = driver.execute_script("return window.getComputedStyle(arguments[0]).fontSize;", inv_footer)
    print(f"Tax Invoice Header height: {inv_h_height} (expected 48px)")
    print(f"Tax Invoice Footer fontSize: {inv_f_size} (expected 10px)")
    assert "48px" in inv_h_height
    assert "10px" in inv_f_size

    # Check Tax Invoice edit terms
    print("5. Testing Tax Invoice modal Terms modification and saving...")
    inv_edit_btn = driver.find_element(By.XPATH, "//button[contains(., 'Edit')]")
    inv_edit_btn.click()
    time.sleep(1)

    inv_terms_area = driver.find_element(By.ID, "ied-terms")
    test_inv_terms = "• Invoice Term A: Immediate payment upon submission.\n• Invoice Term B: Goods once sold will not be taken back."
    inv_terms_area.clear()
    inv_terms_area.send_keys(test_inv_terms)

    inv_save_btn = driver.find_element(By.XPATH, "//button[contains(., 'Save Changes') or contains(., 'Update Invoice')]")
    inv_save_btn.click()
    time.sleep(1.5)

    inv_terms_preview = driver.find_element(By.CSS_SELECTOR, ".shreeraksha-document .sr-terms-list").text
    print("Updated Terms in Tax Invoice preview:\n", inv_terms_preview)
    assert "Invoice Term A: Immediate payment upon submission." in inv_terms_preview
    assert "Invoice Term B: Goods once sold will not be taken back." in inv_terms_preview
    print("PASS: Tax invoice terms update verified!")

    # 6. Test Settings Save & Global Propagation
    print("6. Navigating to Settings (#settings) to test global terms update...")
    driver.execute_script("window.location.hash = '#settings';")
    time.sleep(1.5)

    settings_terms_area = driver.find_element(By.ID, "set-terms")
    global_terms_text = """• Standard Term 1: All prices are strictly FOR Destination.
• Standard Term 2: Defective parts must be returned against delivery.
  * Inspection within 7 business days.
• Standard Term 3: Payment 30 Days Net from date of delivery."""

    settings_terms_area.clear()
    settings_terms_area.send_keys(global_terms_text)

    # Click Save Profile Changes
    save_profile_btn = driver.find_element(By.XPATH, "//button[contains(., 'Save Profile Changes')]")
    save_profile_btn.click()
    time.sleep(1.5)

    # Now navigate back to Invoices and Quotes to verify global terms propagation!
    print("7. Verifying Settings terms propagated to Tax Invoices...")
    driver.execute_script("window.location.hash = '#invoices';")
    time.sleep(1.5)

    inv_propagated_terms = driver.find_element(By.CSS_SELECTOR, ".shreeraksha-document .sr-terms-list").text
    print("Tax Invoice terms after Settings save:\n", inv_propagated_terms)
    assert "Standard Term 1: All prices are strictly FOR Destination." in inv_propagated_terms
    assert "Standard Term 2: Defective parts must be returned against delivery." in inv_propagated_terms
    assert "Inspection within 7 business days." in inv_propagated_terms

    print("8. Verifying Settings terms propagated to Quotations...")
    driver.execute_script("window.location.hash = '#quotes';")
    time.sleep(1.5)

    quote_propagated_terms = driver.find_element(By.CSS_SELECTOR, ".shreeraksha-document .sr-terms-list").text
    print("Quotation terms after Settings save:\n", quote_propagated_terms)
    assert "Standard Term 1: All prices are strictly FOR Destination." in quote_propagated_terms

    # Check screenshot of the uncompromised header and footer
    driver.save_screenshot("scratch/verified_terms_and_uncompromised_header_footer.png")
    print("PASS: Screenshot captured at scratch/verified_terms_and_uncompromised_header_footer.png")

    # Restore standard 10 terms now so default demo state remains pure
    print("9. Restoring official standard 10 terms in Settings...")
    driver.execute_script("window.location.hash = '#settings';")
    time.sleep(1.5)

    std_10_terms = """• Above prices are FOR Destination.
• Please mention our Estimate number on all future correspondence.
• Please share your valid GSTIN in your Purchase Order.
• Payment Terms: As agreed (30 Days net).
• In case of Refurbished requirement
  * The defective part need to be returned - against delivery.
• Delivery will be within 3-4 weeks from date of PO.
  * Goods indicated above in stock are accurate as of the quote date.
  * If goods are out of stock at the time of release of PO, standard lead time would apply.
• Payment will be 50% advance and balance against delivery."""

    settings_terms_area = driver.find_element(By.ID, "set-terms")
    settings_terms_area.clear()
    settings_terms_area.send_keys(std_10_terms)
    save_profile_btn = driver.find_element(By.XPATH, "//button[contains(., 'Save Profile Changes')]")
    save_profile_btn.click()
    time.sleep(1.5)

    # Check Quotations with restored 10 terms
    driver.execute_script("window.location.hash = '#quotes';")
    time.sleep(1.5)
    final_terms_cnt = len(driver.find_elements(By.CSS_SELECTOR, ".shreeraksha-document .sr-terms-list li"))
    print(f"Final Quotation terms count: {final_terms_cnt} (expected 10)")
    assert final_terms_cnt == 10, f"Expected 10 terms items, got {final_terms_cnt}"

    driver.save_screenshot("scratch/final_verified_quotation.png")
    print("PASS: Final screenshot captured at scratch/final_verified_quotation.png")

    print("\nALL TESTS PASSED WITH 100% SUCCESS!")

finally:
    driver.quit()


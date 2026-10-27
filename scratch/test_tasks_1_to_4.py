import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_tests():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1440,900')
    chrome_options.add_argument('--no-sandbox')
    
    driver = webdriver.Chrome(options=chrome_options)
    artifacts_dir = r"C:\Users\kesav\.gemini\antigravity-ide\brain\ad7e935c-f4ad-4174-839e-ccd236310a67"
    
    try:
        print("[TEST] 1. Loading Dashboard...")
        driver.get("http://127.0.0.1:8080/index.html#dashboard")
        time.sleep(2)
        
        # --- TASK 2: KPI AMOUNT FONT SIZE & AUTO-FIT ---
        print("[TEST] Checking Task 2: Dashboard KPI Cards Auto-fit...")
        kpi_values = driver.find_elements(By.CSS_SELECTOR, ".kpi-value")
        assert len(kpi_values) >= 5, f"Expected at least 5 KPI cards, found {len(kpi_values)}"
        
        for idx, kpi in enumerate(kpi_values):
            text = kpi.text.strip()
            parent = kpi.find_element(By.XPATH, "..")
            card_title = parent.find_element(By.CSS_SELECTOR, ".kpi-title").text
            is_single_line = driver.execute_script("""
                const el = arguments[0];
                const card = arguments[1];
                const style = window.getComputedStyle(el);
                const rect = el.getBoundingClientRect();
                const cardRect = card.getBoundingClientRect();
                // Number of lines can be inferred from height vs line-height
                const lineHeight = parseFloat(style.lineHeight) || (parseFloat(style.fontSize) * 1.2);
                const lines = Math.round(rect.height / lineHeight);
                return {
                    text: el.textContent.trim(),
                    lines: lines,
                    fontSize: style.fontSize,
                    whiteSpace: style.whiteSpace,
                    fitsInsideCard: el.scrollWidth <= (card.clientWidth - 10)
                };
            """, kpi, parent)
            
            print(f"  KPI '{card_title}': text='{text}', fontSize={is_single_line['fontSize']}, lines={is_single_line['lines']}, fits={is_single_line['fitsInsideCard']}")
            assert is_single_line['whiteSpace'] == 'nowrap', f"KPI {card_title} should have white-space: nowrap"
            assert is_single_line['lines'] <= 1, f"KPI {card_title} wrapped to {is_single_line['lines']} lines!"
            assert is_single_line['fitsInsideCard'], f"KPI {card_title} overflows card box!"
        
        driver.save_screenshot(os.path.join(artifacts_dir, "test_task2_dashboard_kpi_autofit.png"))
        print("  -> Task 2 PASSED!")
        
        # --- TASK 3: RECENT INVOICES SINGLE ROW & AUTO-FIT ---
        print("\n[TEST] Checking Task 3: Recent Invoices Single Row & Column Auto-fit...")
        recent_rows = driver.find_elements(By.CSS_SELECTOR, ".recent-invoices-table tbody tr")
        assert len(recent_rows) > 0, "No rows found in recent invoices table!"
        
        for idx, row in enumerate(recent_rows):
            row_info = driver.execute_script("""
                const row = arguments[0];
                const cells = Array.from(row.querySelectorAll('td'));
                const cellTexts = cells.map(c => c.textContent.trim());
                const cellHeights = cells.map(c => c.getBoundingClientRect().height);
                const maxH = Math.max(...cellHeights);
                const nowrap = cells.every(c => window.getComputedStyle(c).whiteSpace === 'nowrap');
                return {
                    texts: cellTexts,
                    height: maxH,
                    nowrap: nowrap
                };
            """, row)
            
            print(f"  Invoice Row {idx+1}: Height={row_info['height']}px | Nowrap={row_info['nowrap']} | Data={row_info['texts'][:5]}")
            assert row_info['nowrap'], f"Row {idx+1} cells should all have white-space: nowrap"
            assert row_info['height'] < 60, f"Row {idx+1} height {row_info['height']}px indicates multi-line wrapping!"
        
        driver.save_screenshot(os.path.join(artifacts_dir, "test_task3_recent_invoices_singlerow.png"))
        print("  -> Task 3 PASSED!")
        
        # --- TASK 1: QUOTATION REFERENCE & REFERENCE DATE INPUTS & DOCUMENT CANVAS ---
        print("\n[TEST] Checking Task 1: Quotation Reference & Date Inputs...")
        driver.get("http://127.0.0.1:8080/index.html#quotes?id=est-019")
        time.sleep(2)
        
        # Verify reference display on document canvas
        doc_meta = driver.execute_script("""
            const metaKeys = Array.from(document.querySelectorAll('.sr-meta-k')).map(el => el.textContent.trim());
            const metaVals = Array.from(document.querySelectorAll('.sr-meta-v')).map(el => el.textContent.trim());
            const refIdx = metaKeys.findIndex(k => k.includes('Reference') || k.includes('Ref'));
            return {
                keys: metaKeys,
                refVal: refIdx >= 0 ? metaVals[refIdx] : null
            };
        """)
        print("  Document Reference on Canvas:", doc_meta['refVal'])
        assert doc_meta['refVal'] is not None and len(doc_meta['refVal']) > 0, "Expected Reference to be present on canvas"
        
        # Open Edit Modal
        print("  Opening Quotation Modal to verify manual editing of Reference & Date...")
        driver.execute_script("window.QuotesView.promptQuoteModal('est-019');")
        time.sleep(1)
        
        ref_input = driver.find_element(By.ID, "qed-reference")
        ref_date_input = driver.find_element(By.ID, "qed-reference-date")
        
        assert ref_input.is_displayed(), "Reference input (#qed-reference) not visible in modal!"
        assert ref_date_input.is_displayed(), "Reference date input (#qed-reference-date) not visible in modal!"
        
        print(f"  Existing values in modal: Ref='{ref_input.get_attribute('value')}', Date='{ref_date_input.get_attribute('value')}'")
        
        # Manually edit reference & reference date
        ref_input.clear()
        ref_input.send_keys("UPDATED-RFQ-8840")
        driver.execute_script("arguments[0].value = '2026-10-28';", ref_date_input)
        
        # Click Confirm Save
        confirm_btn = driver.find_element(By.CSS_SELECTOR, ".modal-confirm-btn")
        driver.execute_script("arguments[0].click();", confirm_btn)
        time.sleep(1.5)
        
        # Re-check document canvas for updated reference
        updated_ref = driver.execute_script("""
            const metaKeys = Array.from(document.querySelectorAll('.sr-meta-k')).map(el => el.textContent.trim());
            const metaVals = Array.from(document.querySelectorAll('.sr-meta-v')).map(el => el.textContent.trim());
            const refIdx = metaKeys.findIndex(k => k.includes('Reference') || k.includes('Ref'));
            return refIdx >= 0 ? metaVals[refIdx] : null;
        """)
        print("  Updated Reference on Canvas:", updated_ref)
        assert "UPDATED-RFQ-8840" in updated_ref, f"Expected 'UPDATED-RFQ-8840' on canvas, got {updated_ref}"
        assert "28-10-2026" in updated_ref, f"Expected '28-10-2026' on canvas, got {updated_ref}"
        
        driver.save_screenshot(os.path.join(artifacts_dir, "test_task1_quotation_reference_edited.png"))
        print("  -> Task 1 PASSED!")
        
        # --- TASK 4: REMOVE BANK DETAILS IN VENDOR PO ---
        print("\n[TEST] Checking Task 4: Remove Banking details in Vendor PO...")
        driver.get("http://127.0.0.1:8080/index.html#purchase-orders")
        time.sleep(2)
        
        po_bank_boxes = driver.find_elements(By.CSS_SELECTOR, ".sr-bank-box")
        print(f"  Bank boxes in Vendor PO: {len(po_bank_boxes)}")
        assert len(po_bank_boxes) == 0, f"Expected 0 bank boxes in Vendor PO, found {len(po_bank_boxes)}"
        
        # Check Quotation also has 0 bank boxes
        driver.get("http://127.0.0.1:8080/index.html#quotes?id=est-019")
        time.sleep(1)
        quote_bank_boxes = driver.find_elements(By.CSS_SELECTOR, ".sr-bank-box")
        print(f"  Bank boxes in Quotation: {len(quote_bank_boxes)}")
        assert len(quote_bank_boxes) == 0, f"Expected 0 bank boxes in Quotation, found {len(quote_bank_boxes)}"
        
        # Check Tax Invoice retains bank box
        driver.get("http://127.0.0.1:8080/index.html#invoices")
        time.sleep(1)
        invoice_bank_boxes = driver.find_elements(By.CSS_SELECTOR, ".sr-bank-box")
        print(f"  Bank boxes in Tax Invoice: {len(invoice_bank_boxes)}")
        assert len(invoice_bank_boxes) >= 1, f"Expected bank box in Tax Invoice, found {len(invoice_bank_boxes)}"
        
        driver.save_screenshot(os.path.join(artifacts_dir, "test_task4_vendor_po_no_bank.png"))
        print("  -> Task 4 PASSED!")
        
        print("\nALL 4 TASKS SUCCESSFULLY TESTED AND VERIFIED!")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    run_tests()

import time
import json
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get('http://127.0.0.1:8080/index.html')
    time.sleep(1.5)

    # Dismiss any auth overlay
    driver.execute_script("""
        const overlay = document.getElementById('auth-overlay-backdrop');
        if (overlay) overlay.remove();
        const modal = document.querySelector('.auth-modal-card');
        if (modal) modal.remove();
    """)

    # 1. Add a test quotation via AppStore
    new_quote_id = f"est-realtime-{int(time.time())}"
    new_quote_num = "SHRKS/Qtn/26-27/999"
    driver.execute_script(f"""
        window.AppStore.add('estimates', {{
            id: '{new_quote_id}',
            number: '{new_quote_num}',
            customerId: 'cust-1',
            attention: 'Real-Time Verification Client',
            date: '2026-10-24',
            expiryDate: '2026-11-24',
            status: 'draft',
            items: [
                {{
                    itemId: 'item-1',
                    name: 'ZODIAC C18',
                    description: '250mmx4.6mm, 5µm',
                    itemType: 'product',
                    hsnCode: '90279090',
                    quantity: 2.0,
                    rate: 39286.0,
                    taxRate: 18.0
                }}
            ],
            total: 92715.0
        }});
    """)

    # Give 200ms for immediate SQLite sync
    time.sleep(0.5)

    # 2. Check SQLite database
    conn = sqlite3.connect('sreeraksha.db')
    c = conn.cursor()
    c.execute("SELECT id, number, total, status FROM quotations WHERE id = ?", (new_quote_id,))
    q_row = c.fetchone()
    print("TEST A: Quotation in SQLite database:", q_row)
    assert q_row is not None, "Quotation was not saved to SQLite!"
    assert q_row[1] == new_quote_num, f"Quotation number mismatch: {q_row[1]}"

    # Check app_store table
    c.execute("SELECT data_json FROM app_store WHERE key = 'main_data'")
    store_data = json.loads(c.fetchone()[0])
    store_quote = next((e for e in store_data.get('estimates', []) if e['id'] == new_quote_id), None)
    print("TEST B: Quotation in app_store table:", store_quote is not None)
    assert store_quote is not None, "Quotation not found in app_store main_data!"

    # 3. Refresh browser
    driver.refresh()
    time.sleep(1.5)

    # 4. Verify quotation is loaded in the browser after refresh
    loaded_quote = driver.execute_script(f"return window.AppStore.getById('estimates', '{new_quote_id}');")
    print("TEST C: Quotation loaded in browser after reload:", loaded_quote is not None)
    assert loaded_quote is not None, "Quotation disappeared after reload!"
    print("Loaded Quote Number:", loaded_quote.get('number'))

    # Clean up test quotation
    c.execute("DELETE FROM quotations WHERE id = ?", (new_quote_id,))
    store_data['estimates'] = [e for e in store_data['estimates'] if e['id'] != new_quote_id]
    c.execute("UPDATE app_store SET data_json = ? WHERE key = 'main_data'", (json.dumps(store_data),))
    conn.commit()
    conn.close()

    print("\nREAL-TIME DATABASE PERSISTENCE VERIFIED 100% SUCCESFULLY!")

except Exception as e:
    print("Error:", e)
    raise e
finally:
    driver.quit()

import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

OUTPUT_DIR = "scratch"
os.makedirs(OUTPUT_DIR, exist_ok=True)

opts = Options()
opts.add_argument('--headless')
opts.add_argument('--window-size=1600,1000')
driver = webdriver.Chrome(options=opts)

print("Navigating to http://127.0.0.1:8080/index.html#quotes...")
driver.get('http://127.0.0.1:8080/index.html#quotes')
time.sleep(2)

driver.execute_script("""
    const ov = document.getElementById('auth-overlay-backdrop');
    if (ov) ov.remove();
    const m = document.querySelector('.auth-modal-card');
    if (m) m.remove();
""")
time.sleep(1)
driver.save_screenshot(os.path.join(OUTPUT_DIR, "live_running_quotes.png"))
print("Saved live_running_quotes.png")

print("Navigating to http://127.0.0.1:8080/index.html#invoices...")
driver.get('http://127.0.0.1:8080/index.html#invoices')
time.sleep(2)
driver.execute_script("""
    const ov = document.getElementById('auth-overlay-backdrop');
    if (ov) ov.remove();
    const m = document.querySelector('.auth-modal-card');
    if (m) m.remove();
""")
time.sleep(1)
driver.save_screenshot(os.path.join(OUTPUT_DIR, "live_running_invoices.png"))
print("Saved live_running_invoices.png")

driver.quit()
print("Run completed successfully!")

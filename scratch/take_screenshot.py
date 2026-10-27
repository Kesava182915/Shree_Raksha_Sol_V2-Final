import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument('--headless')
opts.add_argument('--window-size=1600,900')
driver = webdriver.Chrome(options=opts)
driver.get('http://127.0.0.1:8080/index.html#quotes')
time.sleep(2)
driver.execute_script("""
    const ov = document.getElementById('auth-overlay-backdrop');
    if (ov) ov.remove();
    const m = document.querySelector('.auth-modal-card');
    if (m) m.remove();
""")
time.sleep(1)
driver.save_screenshot('scratch/clean_header_and_quotes.png')
driver.quit()
print('Screenshot saved successfully!')

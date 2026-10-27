# scratch/capture_theme_screenshots.py
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

sys.stdout.reconfigure(encoding='utf-8')

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--window-size=1600,1050")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver_path = r"C:\Users\kesav\.wdm\drivers\chromedriver\win64\156.0.8078.47\chromedriver-win64\chromedriver.exe"
driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)

try:
    print("Navigating to http://127.0.0.1:8080/ ...")
    driver.get("http://127.0.0.1:8080/")
    time.sleep(1.5)

    # Bypass auth modal
    driver.execute_script("""
        localStorage.setItem('shreeraksha_auth_token', 'test_admin_token');
        localStorage.setItem('shreeraksha_auth_user', JSON.stringify({ name: 'Admin', role: 'admin' }));
        if (window.AuthManager && window.AuthManager.closeModal) window.AuthManager.closeModal();
        const ov = document.getElementById('auth-overlay-backdrop');
        if (ov) ov.remove();
    """)
    time.sleep(1)

    # 1. Dark Theme Dashboard
    driver.execute_script("""
        localStorage.setItem('theme_mode', 'dark');
        document.body.classList.remove('theme-light');
        document.body.classList.add('theme-dark', 'theme-zoho');
        window.location.hash = '#dashboard';
    """)
    time.sleep(1.5)
    dark_path = r"C:\Users\kesav\.gemini\antigravity-ide\brain\ad7e935c-f4ad-4174-839e-ccd236310a67\scratch\ui_dark_theme.png"
    driver.save_screenshot(dark_path)
    print("Saved Dark Dashboard:", dark_path)

    # 2. Light Theme Dashboard
    driver.execute_script("""
        localStorage.setItem('theme_mode', 'light');
        document.body.classList.remove('theme-dark');
        document.body.classList.add('theme-light');
        window.location.hash = '#dashboard';
    """)
    time.sleep(1.5)
    light_path = r"C:\Users\kesav\.gemini\antigravity-ide\brain\ad7e935c-f4ad-4174-839e-ccd236310a67\scratch\ui_light_theme.png"
    driver.save_screenshot(light_path)
    print("Saved Light Dashboard:", light_path)

    # 3. Light Theme Invoices Tab & Detail View
    driver.execute_script("""
        localStorage.setItem('theme_mode', 'light');
        document.body.classList.remove('theme-dark');
        document.body.classList.add('theme-light');
        window.location.hash = '#invoices';
    """)
    time.sleep(1.5)
    # Click the first invoice item if present
    driver.execute_script("""
        const row = document.querySelector('.master-item-row');
        if (row) row.click();
    """)
    time.sleep(1.5)
    light_inv_path = r"C:\Users\kesav\.gemini\antigravity-ide\brain\ad7e935c-f4ad-4174-839e-ccd236310a67\scratch\ui_light_invoices.png"
    driver.save_screenshot(light_inv_path)
    print("Saved Light Invoices Detail view:", light_inv_path)

    # 4. Dark Theme Invoices Tab & Detail View
    driver.execute_script("""
        localStorage.setItem('theme_mode', 'dark');
        document.body.classList.remove('theme-light');
        document.body.classList.add('theme-dark', 'theme-zoho');
        window.location.hash = '#invoices';
    """)
    time.sleep(1.5)
    driver.execute_script("""
        const row = document.querySelector('.master-item-row');
        if (row) row.click();
    """)
    time.sleep(1.5)
    dark_inv_path = r"C:\Users\kesav\.gemini\antigravity-ide\brain\ad7e935c-f4ad-4174-839e-ccd236310a67\scratch\ui_dark_invoices.png"
    driver.save_screenshot(dark_inv_path)
    print("Saved Dark Invoices Detail view:", dark_inv_path)

finally:
    driver.quit()
    print("Screenshots captured successfully!")

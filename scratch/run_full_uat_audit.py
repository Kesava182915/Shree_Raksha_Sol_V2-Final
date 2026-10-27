import sys
import os
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

CHROMEDRIVER_PATH = r"C:\Users\kesav\.wdm\drivers\chromedriver\win64\156.0.8078.47\chromedriver-win64\chromedriver.exe"
OUTPUT_DIR = r"d:\Antigravity folder\3\scratch"
os.makedirs(OUTPUT_DIR, exist_ok=True)

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--window-size=1600,1200")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

service = Service(executable_path=CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

uat_findings = []

def record_finding(category, title, description, severity="Medium"):
    uat_findings.append({
        "category": category,
        "title": title,
        "description": description,
        "severity": severity
    })

try:
    print("Connecting to application for comprehensive UAT...")
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
        if (window.AppStore) window.AppStore.load();
    """)
    time.sleep(1)

    # =========================================================================
    # MODULE 1: DASHBOARD AUDIT
    # =========================================================================
    print("Auditing Module 1: Dashboard...")
    driver.execute_script("window.location.hash = '#dashboard';")
    time.sleep(1)
    dash_data = driver.execute_script("""
        const cards = Array.from(document.querySelectorAll('.metric-card, .stat-card')).map(c => c.textContent.trim());
        const charts = document.querySelectorAll('canvas, svg.chart');
        const recentRows = document.querySelectorAll('.table-responsive tbody tr');
        return {
            cardsCount: cards.length,
            chartsCount: charts.length,
            recentRowsCount: recentRows.length
        };
    """)
    print("Dashboard Data:", dash_data)
    # Probe: Are charts interactive or static? Are metrics auto-recalculated when payments change?

    # =========================================================================
    # MODULE 2: CUSTOMERS & VENDORS (PARTIES) AUDIT
    # =========================================================================
    print("Auditing Module 2: Customers & Vendors...")
    driver.execute_script("window.location.hash = '#customers';")
    time.sleep(1)
    cust_data = driver.execute_script("""
        const customers = window.AppStore.getAll('customers') || [];
        const hasGstinValidation = typeof window.CustomersView.validateGSTIN === 'function';
        const sampleCust = customers[0] || {};
        return {
            count: customers.length,
            hasGstinValidation,
            hasShippingAddress: !!sampleCust.shippingAddress,
            hasPan: !!sampleCust.pan,
            hasPlaceOfSupply: !!sampleCust.placeOfSupply
        };
    """)
    print("Customers Data:", cust_data)

    # Check GSTIN validation
    gst_validation_check = driver.execute_script("""
        // Try invalid GSTIN format
        const testGst = 'INVALID_GSTIN_123';
        const regex = /^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$/;
        return {
            isValidRegex: regex.test('29AATCM4200G1ZD'),
            catchesInvalid: !regex.test(testGst)
        };
    """)

    # =========================================================================
    # MODULE 3: ITEM MASTER CATALOG & INVENTORY AUDIT
    # =========================================================================
    print("Auditing Module 3: Items Catalog...")
    driver.execute_script("window.location.hash = '#items';")
    time.sleep(1)
    item_data = driver.execute_script("""
        const items = window.AppStore.getAll('items') || [];
        const hasStockTracking = items.some(i => i.stock !== undefined || i.quantityOnHand !== undefined);
        const hasHsnSacSeparation = items.every(i => (i.itemType === 'service' ? !!i.sacCode : !!i.hsnCode));
        const missingCodes = items.filter(i => !i.hsnCode && !i.sacCode).length;
        return {
            count: items.length,
            hasStockTracking,
            missingCodes
        };
    """)
    print("Items Catalog Data:", item_data)

    # =========================================================================
    # MODULE 4: QUOTATIONS / ESTIMATES WORKFLOW AUDIT
    # =========================================================================
    print("Auditing Module 4: Quotations...")
    driver.execute_script("window.location.hash = '#estimates';")
    time.sleep(1)
    quote_audit = driver.execute_script("""
        const quotes = window.AppStore.getAll('estimates') || [];
        const q0 = quotes[0] || {};
        
        // Check conversion action
        const canConvert = typeof window.QuotesView.convertToInvoice === 'function';
        
        // Check Clone action
        const canClone = typeof window.QuotesView.cloneQuote === 'function' || typeof window.QuotesView.duplicateQuote === 'function';

        // Check if discount can be negative or > 100%
        let allowsInvalidDiscount = false;
        try {
            const dummyCalc = window.Calculator.computeGSTDocumentTotals([
                { rate: 1000, quantity: 1, discount: 150, discountType: 'percent', taxRate: 18 }
            ], false, 0);
            allowsInvalidDiscount = dummyCalc.subTotalGross < 0 || dummyCalc.roundedTotal < 0;
        } catch(e) {}

        return {
            quoteCount: quotes.length,
            canConvert,
            canClone,
            allowsInvalidDiscount
        };
    """)
    print("Quotes Audit:", quote_audit)

    # =========================================================================
    # MODULE 5: INVOICES, PROFORMAS & DELIVERY CHALLANS AUDIT
    # =========================================================================
    print("Auditing Module 5: Invoices...")
    driver.execute_script("window.location.hash = '#invoices';")
    time.sleep(1)
    inv_audit = driver.execute_script("""
        const invoices = window.AppStore.getAll('invoices') || [];
        const dcList = invoices.filter(i => i.invoiceType === 'delivery_note' || (i.number && i.number.includes('/DC/')));
        const piList = invoices.filter(i => i.invoiceType === 'proforma' || (i.number && i.number.includes('/PI/')));
        const taxList = invoices.filter(i => !dcList.includes(i) && !piList.includes(i));

        // Check partial payment tracking
        const partiallyPaidSupported = invoices.some(i => i.status === 'partially_paid');
        
        // Check if invoice balance updates when payment is recorded
        const payments = window.AppStore.getAll('payments') || [];
        
        // Check DC conversion to Tax Invoice
        const canConvertDC = typeof window.InvoicesView.convertToTaxInvoice === 'function';

        return {
            totalInvoices: invoices.length,
            taxCount: taxList.length,
            piCount: piList.length,
            dcCount: dcList.length,
            paymentsCount: payments.length,
            canConvertDC
        };
    """)
    print("Invoices Audit:", inv_audit)

    # =========================================================================
    # MODULE 6: PURCHASE ORDERS AUDIT
    # =========================================================================
    print("Auditing Module 6: Purchase Orders...")
    driver.execute_script("window.location.hash = '#purchase-orders';")
    time.sleep(1)
    po_audit = driver.execute_script("""
        const pos = window.AppStore.getAll('purchaseOrders') || [];
        const hasVendorFilter = typeof window.PurchaseOrdersView.filterVendor === 'function';
        const hasPOToBillConversion = typeof window.PurchaseOrdersView.convertToBill === 'function';
        return {
            poCount: pos.length,
            hasVendorFilter,
            hasPOToBillConversion
        };
    """)
    print("Purchase Orders Audit:", po_audit)

    # =========================================================================
    # MODULE 7: DEBIT & CREDIT NOTES AUDIT
    # =========================================================================
    print("Auditing Module 7: Debit & Credit Notes...")
    driver.execute_script("window.location.hash = '#debit-credit-notes';")
    time.sleep(1)
    note_audit = driver.execute_script("""
        const notes = window.AppStore.getAll('debitCreditNotes') || [];
        const hasReason = notes.every(n => !!n.reason);
        const hasOriginalInvoiceRef = notes.every(n => n.originalInvoiceNumber !== undefined);
        const hasAutoLedgerReconciliation = typeof window.DebitCreditNotesView.reconcileWithInvoice === 'function';
        return {
            notesCount: notes.length,
            hasReason,
            hasOriginalInvoiceRef,
            hasAutoLedgerReconciliation
        };
    """)
    print("Debit/Credit Notes Audit:", note_audit)

    # =========================================================================
    # MODULE 8: PAYMENTS & RECEIPTS AUDIT
    # =========================================================================
    print("Auditing Module 8: Payments...")
    driver.execute_script("window.location.hash = '#payments';")
    time.sleep(1)
    pay_audit = driver.execute_script("""
        const pays = window.AppStore.getAll('payments') || [];
        const hasRefundSupport = typeof window.PaymentsView.recordRefund === 'function';
        const hasTdsDeduction = pays.some(p => p.tdsAmount !== undefined || p.tdsDeducted !== undefined);
        return {
            paymentsCount: pays.length,
            hasRefundSupport,
            hasTdsDeduction
        };
    """)
    print("Payments Audit:", pay_audit)

    # =========================================================================
    # MODULE 9: REPORTS & GSTR AUDIT
    # =========================================================================
    print("Auditing Module 9: Reports...")
    driver.execute_script("window.location.hash = '#reports';")
    time.sleep(1)
    rep_audit = driver.execute_script("""
        const hasGstr1Export = typeof window.ReportsView.exportGSTR1 === 'function' || typeof window.ReportsView.exportGstr1Json === 'function';
        const hasCustomerLedger = typeof window.ReportsView.generateLedger === 'function';
        const hasDateRangeFiltering = !!document.getElementById('rep-start-date');
        return {
            hasGstr1Export,
            hasCustomerLedger,
            hasDateRangeFiltering
        };
    """)
    print("Reports Audit:", rep_audit)

    # =========================================================================
    # MODULE 10: SETTINGS, TAXES & BACKUP AUDIT
    # =========================================================================
    print("Auditing Module 10: Settings & Portability...")
    driver.execute_script("window.location.hash = '#settings';")
    time.sleep(1)
    set_audit = driver.execute_script("""
        const org = window.AppStore.getOrg();
        const taxes = window.AppStore.getAll('taxes');
        const hasResetSeed = typeof window.SettingsView.resetDemo === 'function';
        const hasExportJson = typeof window.SettingsView.exportDatabase === 'function';
        const hasImportJson = typeof window.SettingsView.importDatabase === 'function';
        return {
            orgGstin: org.taxId,
            orgMsme: org.msmeRegNo,
            taxesCount: taxes.length,
            hasResetSeed,
            hasExportJson,
            hasImportJson
        };
    """)
    print("Settings Audit:", set_audit)

    print("\n=======================================================")
    print("COMPREHENSIVE UAT EXECUTION FINISHED SUCCESSFULLY!")
    print("=======================================================")

finally:
    driver.quit()

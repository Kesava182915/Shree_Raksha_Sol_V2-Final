import shutil
import os

src = r"D:\Antigravity folder\3"
dst = r"D:\Shree_Raksha_Soft\Shree_Raksha_Sol_V2"

files = [
    "index.html",
    "server.py",
    "default_data.json",
    "sreeraksha.db",
    "test_backend.py",
    os.path.join("css", "main.css"),
    os.path.join("css", "components.css"),
    os.path.join("css", "sidebar.css"),
    os.path.join("css", "shreeraksha-template.css"),
    os.path.join("css", "print.css"),
    os.path.join("css", "auth.css"),
    os.path.join("js", "calculator.js"),
    os.path.join("js", "store.js"),
    os.path.join("js", "app.js"),
    os.path.join("js", "components", "auth-modal.js"),
    os.path.join("js", "components", "gst-document-template.js"),
    os.path.join("js", "views", "dashboard.js"),
    os.path.join("js", "views", "quotes.js"),
    os.path.join("js", "views", "invoices.js"),
    os.path.join("js", "views", "debit-credit-notes.js"),
    os.path.join("js", "views", "purchase-orders.js"),
    os.path.join("js", "views", "payments.js"),
    os.path.join("js", "views", "settings.js"),
    os.path.join("js", "views", "customers.js")
]

for f in files:
    s = os.path.join(src, f)
    d = os.path.join(dst, f)
    if os.path.exists(s):
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(s, d)
        print(f"Copied: {f} -> {d}")

print("All files synchronized successfully to secondary workspace!")

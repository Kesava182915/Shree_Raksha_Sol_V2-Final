with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

target = 'id="sidebar-user-badge" style="cursor: pointer;" title="Manage Account / Switch User"'
replacement = 'id="sidebar-user-badge" style="cursor: default;" title="Shreeraksha Solutions - GST Compliance Admin"'
if target in content:
    content = content.replace(target, replacement, 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("index.html updated successfully!")
else:
    print("Target not found in index.html, checking if already updated...")


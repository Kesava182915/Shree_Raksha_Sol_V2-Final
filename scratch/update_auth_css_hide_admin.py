with open('css/auth.css', 'r', encoding='utf-8') as f:
    content = f.read()

target = """/* Top Header User Profile Pill & Dropdown */
.header-user-profile {
  position: relative;
  display: flex;
  align-items: center;
}"""

replacement = """/* Top Header User Profile Pill & Dropdown (Removed per user request) */
#header-user-profile-wrap,
.header-user-profile {
  display: none !important;
}"""

if target in content:
    content = content.replace(target, replacement, 1)
    with open('css/auth.css', 'w', encoding='utf-8') as f:
        f.write(content)
    print("css/auth.css updated successfully!")
else:
    print("Target not found in css/auth.css")


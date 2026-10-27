with open('css/auth.css', 'r', encoding='utf-8') as f:
    content = f.read()

target = """.auth-overlay-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(10, 22, 28, 0.78);
  backdrop-filter: blur(28px) saturate(190%);
  -webkit-backdrop-filter: blur(28px) saturate(190%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1.25rem;
  overflow-y: auto;
  opacity: 1;
  transition: opacity 0.3s ease, visibility 0.3s ease;
}

.auth-overlay-backdrop.hidden {
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  display: none !important;
}"""

replacement = """.auth-overlay-backdrop,
.auth-overlay-backdrop.hidden {
  display: none !important;
  opacity: 0 !important;
  visibility: hidden !important;
  pointer-events: none !important;
}"""

if target in content:
    content = content.replace(target, replacement, 1)
    with open('css/auth.css', 'w', encoding='utf-8') as f:
        f.write(content)
    print("css/auth.css updated successfully!")
else:
    print("Target not found in css/auth.css")


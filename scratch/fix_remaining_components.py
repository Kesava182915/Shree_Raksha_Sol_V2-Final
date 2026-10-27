# scratch/fix_remaining_components.py
import re

path = r"d:\Antigravity folder\3\css\components.css"
with open(path, "r", encoding="utf-8") as f:
    c = f.read()

# 1. badge-credit
c = c.replace("""badge-credit {
  background-color: rgba(155, 242, 114, 0.16);
  color: #7ABF5A;
  border: 1px solid rgba(122, 191, 90, 0.35);
}""", """badge-credit {
  background-color: rgba(146, 144, 195, 0.20);
  color: #9290c3;
  border: 1px solid rgba(146, 144, 195, 0.4);
}

body.theme-light .badge-credit {
  background-color: #e1afd1;
  color: #000000;
  font-weight: 700;
  border: 1.5px solid #ad88c6;
}""")

# 2. select focus
c = c.replace(""".input-select:focus, select:focus {
  background-color: #10222b !important;
  color: #ffffff !important;
  border-color: #9BF272 !important;
}""", """.input-select:focus, select:focus {
  background-color: #070f2b !important;
  color: #ffffff !important;
  border-color: #9290c3 !important;
}
body.theme-light .input-select:focus,
body.theme-light select:focus {
  background-color: #ffffff !important;
  color: #000000 !important;
  border-color: #7469b6 !important;
}""")

# 3. theme-glass-toggle hover
c = c.replace("""box-shadow: 0 0 18px rgba(155, 242, 114, 0.35), 0 0 12px rgba(186, 200, 217, 0.3);""", """box-shadow: 0 0 18px rgba(146, 144, 195, 0.35), 0 0 12px rgba(83, 92, 145, 0.3);""")

# 4. theme-toggle-slider
c = c.replace("""body.theme-light .theme-toggle-slider {
  transform: translateX(0px);
  background: linear-gradient(135deg, #7ABF5A, #9BF272);
  box-shadow: 0 0 14px rgba(155, 242, 114, 0.8);
}
body.theme-dark .theme-toggle-slider,
body:not(.theme-light) .theme-toggle-slider {
  transform: translateX(28px);
  background: linear-gradient(135deg, #193440 0%, #204554 100%);
  border: 1px solid rgba(155, 242, 114, 0.6);
  box-shadow: 0 0 16px rgba(155, 242, 114, 0.75), 0 0 8px rgba(186, 200, 217, 0.4);
}""", """body.theme-light .theme-toggle-slider {
  transform: translateX(0px);
  background: linear-gradient(135deg, #e1afd1, #7469b6);
  box-shadow: 0 0 14px rgba(116, 105, 182, 0.6);
}
body.theme-dark .theme-toggle-slider,
body:not(.theme-light) .theme-toggle-slider {
  transform: translateX(28px);
  background: linear-gradient(135deg, #1b1a55 0%, #535c91 100%);
  border: 1px solid #9290c3;
  box-shadow: 0 0 16px rgba(146, 144, 195, 0.75);
}""")

# 5. dropdown menu
c = c.replace("""  background-color: #10222b !important; /* Rich Dark Background */
  border: 1px solid rgba(186, 200, 217, 0.25) !important;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.75), 0 0 20px rgba(155, 242, 114, 0.15);""", """  background-color: #1b1a55 !important;
  border: 1px solid rgba(83, 92, 145, 0.45) !important;
  box-shadow: 0 16px 40px rgba(7, 15, 43, 0.75), 0 0 20px rgba(146, 144, 195, 0.2);""")

c = c.replace("""body.theme-light .dropdown-menu {
  background-color: #ffffff !important;
  border: 1.5px solid #ad88c6 !important;
  box-shadow: 0 16px 40px rgba(116, 105, 182, 0.18) !important;
}""", "")

# 6. dropdown items
c = c.replace("""color: #BAC8D9 !important; /* Lighter color text */
  text-decoration: none;
  font-size: 0.835rem;
  font-weight: 400;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.dropdown-item:hover,
.dropdown-item:focus {
  background-color: rgba(155, 242, 114, 0.18) !important;
  color: #9BF272 !important; /* Lighter neon lime text */
}""", """color: #ffffff !important;
  text-decoration: none;
  font-size: 0.835rem;
  font-weight: 500;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.dropdown-item:hover,
.dropdown-item:focus {
  background-color: #535c91 !important;
  color: #ffffff !important;
}

body.theme-light .dropdown-menu {
  background-color: #ffffff !important;
  border: 1.5px solid #ad88c6 !important;
  box-shadow: 0 16px 40px rgba(116, 105, 182, 0.18) !important;
}

body.theme-light .dropdown-item {
  color: #000000 !important;
  font-weight: 600 !important;
}

body.theme-light .dropdown-item:hover,
body.theme-light .dropdown-item:focus {
  background-color: #e1afd1 !important;
  color: #000000 !important;
  font-weight: 700 !important;
}""")

# 7. notifications
c = c.replace("background-color: rgba(155, 242, 114, 0.12);", "background-color: rgba(146, 144, 195, 0.15);")
c = c.replace("color: #BAC8D9 !important;", "color: #9290c3 !important;")
c = c.replace("border-color: rgba(155, 242, 114, 0.45);", "border-color: rgba(146, 144, 195, 0.45);")
c = c.replace("box-shadow: 0 6px 22px rgba(0, 0, 0, 0.2), 0 0 14px rgba(155, 242, 114, 0.18);", "box-shadow: 0 6px 22px rgba(0, 0, 0, 0.2), 0 0 14px rgba(146, 144, 195, 0.18);")
c = c.replace("box-shadow: 0 4px 14px rgba(25, 52, 64, 0.35), 0 0 10px rgba(155, 242, 114, 0.30) !important;", "box-shadow: 0 4px 14px rgba(83, 92, 145, 0.35), 0 0 10px rgba(146, 144, 195, 0.30) !important;")

# 8. Remaining light theme minimized-tab-pill and pulse
c = c.replace("""body.theme-light .minimized-tab-pill {
  border-color: rgba(25, 52, 64, 0.2);
  background: rgba(25, 52, 64, 0.08);
  color: #193440;
}

body.theme-light .minimized-tab-pill:hover,
body.theme-light .minimized-tab-pill.active {
  background: #7ABF5A;
  color: #ffffff;
  border-color: #7ABF5A;
}""", """body.theme-light .minimized-tab-pill {
  border-color: #ad88c6;
  background: #ffffff;
  color: #000000;
  font-weight: 700;
}

body.theme-light .minimized-tab-pill:hover,
body.theme-light .minimized-tab-pill.active {
  background: #7469b6;
  color: #ffffff;
  border-color: #7469b6;
}""")

c = c.replace("""body.theme-light .minimized-live-pulse {
  background-color: #7ABF5A;
  box-shadow: 0 0 8px #7ABF5A;
}""", """body.theme-light .minimized-live-pulse {
  background-color: #7469b6;
  box-shadow: 0 0 8px #7469b6;
}""")

# Clean comments
c = c.replace("#9BF272", "#9290c3")
c = c.replace("#193440", "#000000")

with open(path, "w", encoding="utf-8") as f:
    f.write(c)

print("Cleaned up remaining components.css")

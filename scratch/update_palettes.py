# scratch/update_palettes.py
import re
import os

BASE_DIR = r"d:\Antigravity folder\3"

def update_components_css():
    path = os.path.join(BASE_DIR, "css", "components.css")
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()

    # 1. Primary Button
    old_btn_pri = """.btn-primary {
  background: linear-gradient(135deg, #193440 0%, #204554 45%, #7ABF5A 100%);
  color: #ffffff !important;
  border: 1px solid rgba(155, 242, 114, 0.55);
  box-shadow: 0 4px 18px -2px rgba(122, 191, 90, 0.45), 0 0 12px 0 rgba(155, 242, 114, 0.35);
  position: relative;
  overflow: hidden;
  letter-spacing: 0.02em;
  font-weight: 400;
}
.btn-primary::after {
  content: '';
  position: absolute;
  top: 0; left: -100%; width: 100%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.25), transparent);
  transition: 0.5s;
}
.btn-primary:hover::after {
  left: 100%;
}
.btn-primary:hover {
  transform: translateY(-2px);
  border-color: #9BF272;
  box-shadow: 0 8px 24px -2px rgba(155, 242, 114, 0.65), 0 0 20px rgba(186, 200, 217, 0.45);
  filter: brightness(1.1);
}"""

    new_btn_pri = """.btn-primary {
  background: linear-gradient(135deg, #1b1a55 0%, #303375 45%, #535c91 100%);
  color: #ffffff !important;
  border: 1px solid rgba(146, 144, 195, 0.55);
  box-shadow: 0 4px 18px -2px rgba(83, 92, 145, 0.55), 0 0 12px 0 rgba(146, 144, 195, 0.40);
  position: relative;
  overflow: hidden;
  letter-spacing: 0.02em;
  font-weight: 600;
}
.btn-primary::after {
  content: '';
  position: absolute;
  top: 0; left: -100%; width: 100%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.25), transparent);
  transition: 0.5s;
}
.btn-primary:hover::after {
  left: 100%;
}
.btn-primary:hover {
  transform: translateY(-2px);
  border-color: #9290c3;
  box-shadow: 0 8px 24px -2px rgba(146, 144, 195, 0.65), 0 0 20px rgba(146, 144, 195, 0.45);
  filter: brightness(1.1);
}

body.theme-light .btn-primary {
  background: linear-gradient(135deg, #7469b6 0%, #5d539e 100%) !important;
  color: #ffffff !important;
  border: 1px solid #7469b6 !important;
  box-shadow: 0 4px 18px -2px rgba(116, 105, 182, 0.45), 0 0 12px 0 rgba(173, 136, 198, 0.35) !important;
  font-weight: 700 !important;
}
body.theme-light .btn-primary:hover {
  transform: translateY(-2px);
  border-color: #5d539e !important;
  box-shadow: 0 8px 24px -2px rgba(116, 105, 182, 0.65) !important;
}"""

    if old_btn_pri in c:
        c = c.replace(old_btn_pri, new_btn_pri)

    # 2. Secondary Button
    old_btn_sec = """.btn-secondary {
  background-color: var(--surface);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  color: var(--text-main);
  border: 1px solid var(--border-light);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.12);
  font-weight: 400;
}
.btn-secondary:hover {
  background-color: var(--surface-hover);
  border-color: #7ABF5A;
  color: var(--text-main);
  box-shadow: 0 4px 16px rgba(122, 191, 90, 0.3), 0 0 12px rgba(155, 242, 114, 0.25);
  transform: translateY(-1.5px);
}"""

    new_btn_sec = """.btn-secondary {
  background-color: var(--surface);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  color: #ffffff !important;
  border: 1px solid var(--border-light);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.12);
  font-weight: 500;
}
.btn-secondary:hover {
  background-color: #535c91;
  border-color: #9290c3;
  color: #ffffff !important;
  box-shadow: 0 4px 16px rgba(83, 92, 145, 0.4), 0 0 12px rgba(146, 144, 195, 0.35);
  transform: translateY(-1.5px);
}

body.theme-light .btn-secondary {
  background-color: #e1afd1 !important;
  color: #000000 !important;
  border: 1.5px solid #ad88c6 !important;
  box-shadow: 0 2px 10px rgba(116, 105, 182, 0.15) !important;
  font-weight: 700 !important;
}
body.theme-light .btn-secondary:hover {
  background-color: #ad88c6 !important;
  border-color: #7469b6 !important;
  color: #000000 !important;
  box-shadow: 0 4px 16px rgba(116, 105, 182, 0.3) !important;
}"""

    if old_btn_sec in c:
        c = c.replace(old_btn_sec, new_btn_sec)

    # 3. Sunset / Warning and Outline buttons
    old_btn_sunset = """.btn-sunset, .btn-warning {
  background: linear-gradient(135deg, #7ABF5A 0%, #89d065 50%, #9BF272 100%);
  color: #193440 !important;
  border: 1px solid rgba(25, 52, 64, 0.25);
  box-shadow: 0 4px 18px rgba(122, 191, 90, 0.45), 0 0 12px rgba(155, 242, 114, 0.35);
  font-weight: 400;
}
.btn-sunset:hover, .btn-warning:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(122, 191, 90, 0.65), 0 0 20px rgba(155, 242, 114, 0.5);
  filter: brightness(1.08);
}

.btn-outline {
  background-color: transparent;
  color: var(--text-main);
  border: 1px solid var(--border-light);
  backdrop-filter: blur(8px);
  font-weight: 400;
}
.btn-outline:hover {
  background-color: var(--primary-light);
  border-color: #9BF272;
  color: #9BF272;
  box-shadow: 0 0 16px var(--secondary-glow);
  transform: translateY(-1.5px);
}"""

    new_btn_sunset = """.btn-sunset, .btn-warning {
  background: linear-gradient(135deg, #535c91 0%, #6872a8 50%, #9290c3 100%);
  color: #ffffff !important;
  border: 1px solid rgba(146, 144, 195, 0.45);
  box-shadow: 0 4px 18px rgba(83, 92, 145, 0.45);
  font-weight: 600;
}
.btn-sunset:hover, .btn-warning:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(146, 144, 195, 0.65);
  filter: brightness(1.08);
}

body.theme-light .btn-sunset,
body.theme-light .btn-warning {
  background: linear-gradient(135deg, #ad88c6 0%, #7469b6 100%) !important;
  color: #ffffff !important;
  border: 1px solid #7469b6 !important;
  box-shadow: 0 4px 18px rgba(116, 105, 182, 0.35) !important;
  font-weight: 700 !important;
}

.btn-outline {
  background-color: transparent;
  color: #ffffff !important;
  border: 1px solid var(--border-light);
  backdrop-filter: blur(8px);
  font-weight: 500;
}
.btn-outline:hover {
  background-color: var(--primary-light);
  border-color: #9290c3;
  color: #9290c3 !important;
  box-shadow: 0 0 16px var(--secondary-glow);
  transform: translateY(-1.5px);
}

body.theme-light .btn-outline {
  background-color: transparent !important;
  color: #000000 !important;
  border: 1.5px solid #ad88c6 !important;
  font-weight: 700 !important;
}
body.theme-light .btn-outline:hover {
  background-color: #ffe6e6 !important;
  border-color: #7469b6 !important;
  color: #7469b6 !important;
}"""

    if old_btn_sunset in c:
        c = c.replace(old_btn_sunset, new_btn_sunset)

    # 4. KPI Cards
    old_kpi_accents = """.kpi-card.accent-receivables { --card-accent: #193440; }
.kpi-card.accent-received { --card-accent: #9BF272; }
.kpi-card.accent-overdue { --card-accent: #ef4444; }
.kpi-card.accent-expenses { --card-accent: #7ABF5A; }
.kpi-card.accent-projects { --card-accent: #BAC8D9; }
.kpi-card.accent-profit { --card-accent: #9BF272; }"""

    new_kpi_accents = """.kpi-card.accent-receivables { --card-accent: #9290c3; }
.kpi-card.accent-received { --card-accent: #535c91; }
.kpi-card.accent-overdue { --card-accent: #f87171; }
.kpi-card.accent-expenses { --card-accent: #9290c3; }
.kpi-card.accent-projects { --card-accent: #535c91; }
.kpi-card.accent-profit { --card-accent: #9290c3; }

body.theme-light .kpi-card.accent-receivables { --card-accent: #7469b6; }
body.theme-light .kpi-card.accent-received { --card-accent: #ad88c6; }
body.theme-light .kpi-card.accent-overdue { --card-accent: #ef4444; }
body.theme-light .kpi-card.accent-expenses { --card-accent: #7469b6; }
body.theme-light .kpi-card.accent-projects { --card-accent: #e1afd1; }
body.theme-light .kpi-card.accent-profit { --card-accent: #7469b6; }"""

    if old_kpi_accents in c:
        c = c.replace(old_kpi_accents, new_kpi_accents)

    # 5. Table Search Input Focus
    old_search_focus = """.table-search-input:focus {
  background-color: var(--surface);
  border-color: #9BF272;
  box-shadow: 0 0 0 3px rgba(155, 242, 114, 0.2);
}"""

    new_search_focus = """.table-search-input:focus {
  background-color: var(--surface);
  border-color: #9290c3;
  box-shadow: 0 0 0 3px rgba(146, 144, 195, 0.25);
}
body.theme-light .table-search-input:focus {
  border-color: #7469b6;
  box-shadow: 0 0 0 3px rgba(116, 105, 182, 0.25);
}"""

    if old_search_focus in c:
        c = c.replace(old_search_focus, new_search_focus)

    # 6. Form control focus
    old_form_focus = """.form-control:focus, .input-select:focus {
  border-color: #9BF272;
  box-shadow: 0 0 0 3px rgba(155, 242, 114, 0.25), 0 0 12px rgba(186, 200, 217, 0.25);
}"""

    new_form_focus = """.form-control:focus, .input-select:focus {
  border-color: #9290c3;
  box-shadow: 0 0 0 3px rgba(146, 144, 195, 0.25), 0 0 12px rgba(83, 92, 145, 0.35);
}
body.theme-light .form-control:focus,
body.theme-light .input-select:focus {
  border-color: #7469b6;
  box-shadow: 0 0 0 3px rgba(116, 105, 182, 0.25);
}"""

    if old_form_focus in c:
        c = c.replace(old_form_focus, new_form_focus)

    # 7. Quote Number Focus & Colors
    c = c.replace("stroke='%23BAC8D9'", "stroke='%239290c3'")
    c = c.replace("""body.theme-zoho .quote-number-prefix {
  background-color: rgba(155, 242, 114, 0.10);
  color: #BAC8D9;
}

body.theme-light .quote-number-prefix {
  background-color: rgba(25, 52, 64, 0.08);
  color: #193440;
}""", """body.theme-zoho .quote-number-prefix {
  background-color: rgba(146, 144, 195, 0.15);
  color: #ffffff;
}

body.theme-light .quote-number-prefix {
  background-color: #e1afd1;
  color: #000000;
  font-weight: 700;
  border-right: 1.5px solid #ad88c6;
}""")

    c = c.replace(""".quote-number-input-group:focus-within {
  border-color: #9BF272;
  box-shadow: 0 0 0 3px rgba(155, 242, 114, 0.25), 0 0 12px rgba(186, 200, 217, 0.25);
}""", """.quote-number-input-group:focus-within {
  border-color: #9290c3;
  box-shadow: 0 0 0 3px rgba(146, 144, 195, 0.25);
}
body.theme-light .quote-number-input-group:focus-within {
  border-color: #7469b6;
  box-shadow: 0 0 0 3px rgba(116, 105, 182, 0.25);
}""")

    # 8. Reports & Hover block
    old_hover_block = """/* Dark Theme - Financial Reports Tabs & All Buttons Hover Contrast Fix */
body.theme-dark .reports-page .btn:hover,
body.theme-dark .reports-tab-bar .btn:hover,
body.theme-dark .reports-tab-btn:hover,
body.theme-dark .reports-page .glass-capsule-dock .btn:hover {
  color: #9BF272 !important;
  border-color: #9BF272 !important;
  background-color: rgba(16, 34, 43, 0.94) !important;
  box-shadow: 0 4px 18px rgba(155, 242, 114, 0.45), 0 0 14px rgba(155, 242, 114, 0.35) !important;
  transform: translateY(-1.5px);
}

body.theme-dark .reports-page .btn:hover svg,
body.theme-dark .reports-tab-bar .btn:hover svg,
body.theme-dark .reports-tab-btn:hover svg,
body.theme-dark .reports-page .glass-capsule-dock .btn:hover svg {
  stroke: #9BF272 !important;
}

/* Secondary Button Hover State in Dark Theme: ensure text is visible #9BF272 instead of white */
body.theme-dark .btn-secondary:hover {
  background-color: rgba(16, 34, 43, 0.92) !important;
  border-color: #9BF272 !important;
  color: #9BF272 !important;
  box-shadow: 0 4px 16px rgba(155, 242, 114, 0.35), 0 0 12px rgba(155, 242, 114, 0.25);
}

body.theme-dark .btn-secondary:hover svg {
  stroke: #9BF272 !important;
}

/* Light Theme - Financial Reports Tabs & Buttons Hover State */
body.theme-light .reports-page .btn:hover,
body.theme-light .reports-tab-bar .btn:hover,
body.theme-light .reports-tab-btn:hover,
body.theme-light .reports-page .glass-capsule-dock .btn:hover {
  color: #193440 !important;
  border-color: #7ABF5A !important;
  background-color: rgba(255, 255, 255, 0.90) !important;
  box-shadow: 0 4px 16px rgba(122, 191, 90, 0.25), inset 0 1.5px 2px rgba(255, 255, 255, 1) !important;
  transform: translateY(-1.5px);
}

body.theme-light .reports-page .btn:hover svg,
body.theme-light .reports-tab-bar .btn:hover svg,
body.theme-light .reports-tab-btn:hover svg,
body.theme-light .reports-page .glass-capsule-dock .btn:hover svg {
  stroke: #193440 !important;
}"""

    new_hover_block = """/* Dark Theme - Financial Reports Tabs & All Buttons Hover Contrast Fix */
body.theme-dark .reports-page .btn:hover,
body.theme-dark .reports-tab-bar .btn:hover,
body.theme-dark .reports-tab-btn:hover,
body.theme-dark .reports-page .glass-capsule-dock .btn:hover {
  color: #ffffff !important;
  border-color: #9290c3 !important;
  background-color: #535c91 !important;
  box-shadow: 0 4px 18px rgba(146, 144, 195, 0.45) !important;
  transform: translateY(-1.5px);
}

body.theme-dark .reports-page .btn:hover svg,
body.theme-dark .reports-tab-bar .btn:hover svg,
body.theme-dark .reports-tab-btn:hover svg,
body.theme-dark .reports-page .glass-capsule-dock .btn:hover svg {
  stroke: #ffffff !important;
}

/* Secondary Button Hover State in Dark Theme */
body.theme-dark .btn-secondary:hover {
  background-color: #535c91 !important;
  border-color: #9290c3 !important;
  color: #ffffff !important;
  box-shadow: 0 4px 16px rgba(83, 92, 145, 0.45);
}

body.theme-dark .btn-secondary:hover svg {
  stroke: #ffffff !important;
}

/* Light Theme - Financial Reports Tabs & Buttons Hover State */
body.theme-light .reports-page .btn:hover,
body.theme-light .reports-tab-bar .btn:hover,
body.theme-light .reports-tab-btn:hover,
body.theme-light .reports-page .glass-capsule-dock .btn:hover {
  color: #000000 !important;
  font-weight: 700 !important;
  border-color: #7469b6 !important;
  background-color: #e1afd1 !important;
  box-shadow: 0 4px 16px rgba(116, 105, 182, 0.25) !important;
  transform: translateY(-1.5px);
}

body.theme-light .reports-page .btn:hover svg,
body.theme-light .reports-tab-bar .btn:hover svg,
body.theme-light .reports-tab-btn:hover svg,
body.theme-light .reports-page .glass-capsule-dock .btn:hover svg {
  stroke: #000000 !important;
}"""

    if old_hover_block in c:
        c = c.replace(old_hover_block, new_hover_block)

    # 9. Light theme reports tab button & active filter tab pill
    c = c.replace("""body.theme-light .reports-tab-btn.btn-primary {
  background-color: #193440 !important;
  color: #ffffff !important;
  border-color: #193440 !important;
  box-shadow: 0 4px 14px rgba(25, 52, 64, 0.40), 0 0 10px rgba(122, 191, 90, 0.25) !important;
}""", """body.theme-light .reports-tab-btn.btn-primary {
  background-color: #7469b6 !important;
  color: #ffffff !important;
  border-color: #7469b6 !important;
  box-shadow: 0 4px 14px rgba(116, 105, 182, 0.40) !important;
  font-weight: 700 !important;
}""")

    c = c.replace("""body.theme-light .filter-tab-pill.active {
  background: #ffffff !important;
  color: #193440 !important;
  border-color: #7ABF5A !important;
  box-shadow: 0 4px 12px rgba(16, 34, 43, 0.20), 0 0 8px rgba(122, 191, 90, 0.25) !important;
}""", """body.theme-light .filter-tab-pill.active {
  background: #e1afd1 !important;
  color: #000000 !important;
  border-color: #7469b6 !important;
  box-shadow: 0 4px 12px rgba(116, 105, 182, 0.25) !important;
  font-weight: 700 !important;
}""")

    # 10. Minimized dock card & pulse
    c = c.replace("border: 1px solid rgba(155, 242, 114, 0.45);", "border: 1px solid rgba(146, 144, 195, 0.45);")
    c = c.replace("box-shadow: 0 16px 40px rgba(0, 0, 0, 0.35), 0 0 20px rgba(155, 242, 114, 0.25);", "box-shadow: 0 16px 40px rgba(7, 15, 43, 0.55), 0 0 20px rgba(146, 144, 195, 0.25);")
    c = c.replace("background: rgba(16, 34, 43, 0.92);", "background: rgba(27, 26, 85, 0.92);")
    c = c.replace("border-color: #9BF272;", "border-color: #9290c3;")
    c = c.replace("box-shadow: 0 20px 48px rgba(0, 0, 0, 0.42), 0 0 28px rgba(155, 242, 114, 0.35);", "box-shadow: 0 20px 48px rgba(7, 15, 43, 0.65), 0 0 28px rgba(146, 144, 195, 0.35);")

    c = c.replace("""body.theme-light .minimized-dock-card {
  background: rgba(255, 255, 255, 0.94);
  color: #193440;
  border: 1px solid rgba(122, 191, 90, 0.55);
  box-shadow: 0 16px 40px rgba(25, 52, 64, 0.22), 0 4px 14px rgba(0, 0, 0, 0.08);
}

body.theme-light .minimized-dock-card:hover {
  border-color: #7ABF5A;
  box-shadow: 0 20px 48px rgba(25, 52, 64, 0.28), 0 6px 18px rgba(122, 191, 90, 0.35);
}""", """body.theme-light .minimized-dock-card {
  background: rgba(255, 230, 230, 0.95);
  color: #000000;
  border: 1.5px solid #ad88c6;
  box-shadow: 0 16px 40px rgba(116, 105, 182, 0.20), 0 4px 14px rgba(0, 0, 0, 0.08);
  font-weight: 700;
}

body.theme-light .minimized-dock-card:hover {
  border-color: #7469b6;
  box-shadow: 0 20px 48px rgba(116, 105, 182, 0.30);
}""")

    c = c.replace("background: rgba(155, 242, 114, 0.15);", "background: rgba(146, 144, 195, 0.20);")
    c = c.replace("color: #9BF272;", "color: #9290c3;")
    c = c.replace("background: #9BF272;", "background: #9290c3;")
    c = c.replace("background-color: #9BF272;", "background-color: #9290c3;")
    c = c.replace("box-shadow: 0 0 8px #9BF272;", "box-shadow: 0 0 8px #9290c3;")

    c = c.replace("""body.theme-light .minimized-dock-icon {
  background: rgba(122, 191, 90, 0.18);
  color: #276718;
}""", """body.theme-light .minimized-dock-icon {
  background: #e1afd1;
  color: #7469b6;
}""")

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
}

.minimized-live-pulse {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background-color: #9BF272;
  box-shadow: 0 0 8px #9BF272;
  animation: dockPulse 1.8s infinite ease-in-out;
  display: inline-block;
}

body.theme-light .minimized-live-pulse {
  background-color: #7ABF5A;
  box-shadow: 0 0 8px #7ABF5A;
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
}

.minimized-live-pulse {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background-color: #9290c3;
  box-shadow: 0 0 8px #9290c3;
  animation: dockPulse 1.8s infinite ease-in-out;
  display: inline-block;
}

body.theme-light .minimized-live-pulse {
  background-color: #7469b6;
  box-shadow: 0 0 8px #7469b6;
}""")

    # 11. Dropdown options in components.css
    c = c.replace("""select option:checked,
.input-select option:checked {
  background-color: #193440 !important;
  color: #9BF272 !important; /* Lighter Neon Lime for active selection */
  font-weight: 500;
}

select option:hover,
select option:focus,
.input-select option:hover,
.input-select option:focus {
  background-color: #193440 !important;
  color: #9BF272 !important;
}""", """select option:checked,
.input-select option:checked {
  background-color: #535c91 !important;
  color: #ffffff !important;
  font-weight: 600;
}

select option:hover,
select option:focus,
.input-select option:hover,
.input-select option:focus {
  background-color: #535c91 !important;
  color: #ffffff !important;
}""")

    c = c.replace("""select option,
.input-select option,
optgroup {
  background-color: #10222b !important; /* Rich Dark Background */
  color: #f1f5f9 !important; /* Crisp Lighter Text */
  padding: 8px 12px;
  font-size: 0.875rem;
  font-family: inherit;
}""", """select option,
.input-select option,
optgroup {
  background-color: #1b1a55 !important;
  color: #ffffff !important;
  padding: 8px 12px;
  font-size: 0.875rem;
  font-family: inherit;
}""")

    c = c.replace(".toast-item.toast-info { border-left: 4px solid #BAC8D9; }", ".toast-item.toast-info { border-left: 4px solid #9290c3; }")
    c = c.replace(".toast-item.toast-warning { border-left: 4px solid #7ABF5A; }", ".toast-item.toast-warning { border-left: 4px solid #535c91; }")
    c = c.replace("box-shadow: 0 16px 36px rgba(0, 0, 0, 0.45), 0 0 20px rgba(155, 242, 114, 0.25);", "box-shadow: 0 16px 36px rgba(7, 15, 43, 0.45), 0 0 20px rgba(146, 144, 195, 0.25);")
    c = c.replace("box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.6), 0 0 40px rgba(155, 242, 114, 0.2);", "box-shadow: 0 25px 60px -15px rgba(7, 15, 43, 0.6), 0 0 40px rgba(146, 144, 195, 0.2);")

    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
    print("Updated components.css successfully")

def update_sidebar_css():
    path = os.path.join(BASE_DIR, "css", "sidebar.css")
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()

    # Dots
    c = c.replace(""".nav-sub-dot.dot-customer {
  background-color: #7ABF5A;
  box-shadow: 0 0 8px rgba(122, 191, 90, 0.7);
}

.nav-sub-dot.dot-vendor {
  background-color: #9BF272;
  box-shadow: 0 0 8px rgba(155, 242, 114, 0.7);
}""", """.nav-sub-dot.dot-customer {
  background-color: #535c91;
  box-shadow: 0 0 8px rgba(83, 92, 145, 0.7);
}

.nav-sub-dot.dot-vendor {
  background-color: #9290c3;
  box-shadow: 0 0 8px rgba(146, 144, 195, 0.7);
}

body.theme-light .nav-sub-dot.dot-customer {
  background-color: #7469b6;
  box-shadow: 0 0 8px rgba(116, 105, 182, 0.7);
}

body.theme-light .nav-sub-dot.dot-vendor {
  background-color: #ad88c6;
  box-shadow: 0 0 8px rgba(173, 136, 198, 0.7);
}""")

    # User Avatar
    c = c.replace("""background: linear-gradient(135deg, #193440, #7ABF5A);""", """background: linear-gradient(135deg, #1b1a55, #9290c3);""")

    # Omnibar
    c = c.replace("""border-color: rgba(155, 242, 114, 0.50);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15), 0 0 12px rgba(155, 242, 114, 0.18);""", """border-color: rgba(146, 144, 195, 0.50);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15), 0 0 12px rgba(146, 144, 195, 0.18);""")
    c = c.replace(""".search-omnibar:hover svg {
  color: #9BF272;
  transform: scale(1.08);
}

body.theme-light .search-omnibar:hover {
  border-color: #7ABF5A;
  box-shadow: 0 4px 16px rgba(122, 191, 90, 0.20), inset 0 1px 2px rgba(255, 255, 255, 0.95);
}

body.theme-light .search-omnibar:hover svg {
  color: #7ABF5A;
}""", """.search-omnibar:hover svg {
  color: #9290c3;
  transform: scale(1.08);
}

body.theme-light .search-omnibar:hover {
  border-color: #7469b6;
  box-shadow: 0 4px 16px rgba(116, 105, 182, 0.20), inset 0 1px 2px rgba(255, 255, 255, 0.95);
}

body.theme-light .search-omnibar:hover svg {
  color: #7469b6;
}""")

    # Header right dock
    c = c.replace("""border-color: rgba(155, 242, 114, 0.45);
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.22), 0 0 16px rgba(155, 242, 114, 0.16), inset 0 1px 1px rgba(255, 255, 255, 0.25);""", """border-color: rgba(146, 144, 195, 0.45);
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.22), 0 0 16px rgba(146, 144, 195, 0.16), inset 0 1px 1px rgba(255, 255, 255, 0.25);""")

    c = c.replace(""".header-right .icon-btn-ghost:hover {
  background: var(--surface-hover);
  border-color: #9BF272;
  box-shadow: 0 0 12px rgba(155, 242, 114, 0.3);
}""", """.header-right .icon-btn-ghost:hover {
  background: var(--surface-hover);
  border-color: #9290c3;
  box-shadow: 0 0 12px rgba(146, 144, 195, 0.3);
}

body.theme-light .header-right:hover {
  border-color: #7469b6;
}

body.theme-light .header-right .icon-btn-ghost:hover {
  border-color: #7469b6;
  color: #7469b6;
  box-shadow: 0 0 12px rgba(116, 105, 182, 0.25);
}""")

    # Transparency Dock
    c = c.replace("""border-color: rgba(155, 242, 114, 0.50);
  background: var(--surface);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15), 0 0 12px rgba(155, 242, 114, 0.18);""", """border-color: rgba(146, 144, 195, 0.50);
  background: var(--surface);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15), 0 0 12px rgba(146, 144, 195, 0.18);""")

    c = c.replace("""body.theme-light .glass-transparency-dock:hover {
  border-color: #7ABF5A;
  box-shadow: 0 4px 16px rgba(122, 191, 90, 0.20), inset 0 1px 2px rgba(255, 255, 255, 0.95);
}""", """body.theme-light .glass-transparency-dock:hover {
  border-color: #7469b6;
  box-shadow: 0 4px 16px rgba(116, 105, 182, 0.20), inset 0 1px 2px rgba(255, 255, 255, 0.95);
}""")

    c = c.replace(""".glass-transparency-dock:hover .transparency-icon-wrap {
  color: #9BF272;
  transform: scale(1.08);
}

body.theme-light .glass-transparency-dock:hover .transparency-icon-wrap {
  color: #7ABF5A;
}""", """.glass-transparency-dock:hover .transparency-icon-wrap {
  color: #9290c3;
  transform: scale(1.08);
}

body.theme-light .glass-transparency-dock:hover .transparency-icon-wrap {
  color: #7469b6;
}""")

    # Sliders
    c = c.replace("""background: #9BF272;
  border: 2px solid #10222b;
  cursor: pointer;
  box-shadow: 0 0 10px rgba(155, 242, 114, 0.8), 0 2px 5px rgba(0, 0, 0, 0.4);""", """background: #9290c3;
  border: 2px solid #070f2b;
  cursor: pointer;
  box-shadow: 0 0 10px rgba(146, 144, 195, 0.8), 0 2px 5px rgba(0, 0, 0, 0.4);""")

    c = c.replace("""box-shadow: 0 0 16px rgba(155, 242, 114, 1), 0 2px 8px rgba(0, 0, 0, 0.6);""", """box-shadow: 0 0 16px rgba(146, 144, 195, 1), 0 2px 8px rgba(0, 0, 0, 0.6);""")

    c = c.replace("""body.theme-light .spatial-glass-slider::-webkit-slider-thumb {
  background: #7ABF5A;
  border: 2px solid #ffffff;
  box-shadow: 0 0 10px rgba(122, 191, 90, 0.7), 0 2px 6px rgba(25, 52, 64, 0.25);
}

body.theme-light .spatial-glass-slider::-webkit-slider-thumb:hover,
body.theme-light .spatial-glass-slider:active::-webkit-slider-thumb {
  transform: scale(1.25);
  box-shadow: 0 0 16px rgba(122, 191, 90, 0.95), 0 2px 8px rgba(25, 52, 64, 0.35);
}

body.theme-light .spatial-glass-slider::-moz-range-thumb {
  background: #7ABF5A;
  border: 2px solid #ffffff;
  box-shadow: 0 0 10px rgba(122, 191, 90, 0.7), 0 2px 6px rgba(25, 52, 64, 0.25);
}

body.theme-light .spatial-glass-slider::-moz-range-thumb:hover,
body.theme-light .spatial-glass-slider:active::-moz-range-thumb {
  transform: scale(1.25);
  box-shadow: 0 0 16px rgba(122, 191, 90, 0.95), 0 2px 8px rgba(25, 52, 64, 0.35);
}""", """body.theme-light .spatial-glass-slider::-webkit-slider-thumb {
  background: #7469b6;
  border: 2px solid #ffffff;
  box-shadow: 0 0 10px rgba(116, 105, 182, 0.7), 0 2px 6px rgba(116, 105, 182, 0.25);
}

body.theme-light .spatial-glass-slider::-webkit-slider-thumb:hover,
body.theme-light .spatial-glass-slider:active::-webkit-slider-thumb {
  transform: scale(1.25);
  box-shadow: 0 0 16px rgba(116, 105, 182, 0.95), 0 2px 8px rgba(116, 105, 182, 0.35);
}

body.theme-light .spatial-glass-slider::-moz-range-thumb {
  background: #7469b6;
  border: 2px solid #ffffff;
  box-shadow: 0 0 10px rgba(116, 105, 182, 0.7), 0 2px 6px rgba(116, 105, 182, 0.25);
}

body.theme-light .spatial-glass-slider::-moz-range-thumb:hover,
body.theme-light .spatial-glass-slider:active::-moz-range-thumb {
  transform: scale(1.25);
  box-shadow: 0 0 16px rgba(116, 105, 182, 0.95), 0 2px 8px rgba(116, 105, 182, 0.35);
}""")

    # Transparency Pill
    c = c.replace("""color: #9BF272;
  cursor: pointer;
  transition: all var(--transition-fast);
  line-height: 1.2;
}

body.theme-light .transparency-value-pill {
  color: #193440;
  border-color: rgba(186, 200, 217, 0.6);
  background: rgba(255, 255, 255, 0.6);
}

.transparency-value-pill:hover {
  transform: scale(1.05);
  border-color: #9BF272;
  box-shadow: 0 0 10px rgba(155, 242, 114, 0.4);
}

body.theme-light .transparency-value-pill:hover {
  border-color: #7ABF5A;
  box-shadow: 0 0 10px rgba(122, 191, 90, 0.3);
}""", """color: #9290c3;
  cursor: pointer;
  transition: all var(--transition-fast);
  line-height: 1.2;
}

body.theme-light .transparency-value-pill {
  color: #000000;
  font-weight: 700;
  border-color: #ad88c6;
  background: #e1afd1;
}

.transparency-value-pill:hover {
  transform: scale(1.05);
  border-color: #9290c3;
  box-shadow: 0 0 10px rgba(146, 144, 195, 0.4);
}

body.theme-light .transparency-value-pill:hover {
  border-color: #7469b6;
  color: #000000;
  box-shadow: 0 0 10px rgba(116, 105, 182, 0.3);
}""")

    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
    print("Updated sidebar.css successfully")

def update_invoice_view_css():
    path = os.path.join(BASE_DIR, "css", "invoice-view.css")
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()

    c = c.replace("""background: linear-gradient(90deg, rgba(155, 242, 114, 0.28), rgba(186, 200, 217, 0.28));
  color: var(--text-main);
  border-color: #9BF272;
  box-shadow: 0 3px 12px rgba(155, 242, 114, 0.35), 0 2px 5px rgba(0, 0, 0, 0.15);""", """background: linear-gradient(90deg, rgba(83, 92, 145, 0.4), rgba(146, 144, 195, 0.3));
  color: #ffffff;
  border-color: #9290c3;
  box-shadow: 0 3px 12px rgba(146, 144, 195, 0.35), 0 2px 5px rgba(0, 0, 0, 0.15);""")

    c = c.replace(""".master-item-row.active {
  background-color: var(--surface-hover);
  border-left: 4px solid #9BF272;
}""", """.master-item-row.active {
  background-color: var(--surface-hover);
  border-left: 4px solid #9290c3;
}

body.theme-light .filter-tab-pill.active {
  background: #e1afd1 !important;
  color: #000000 !important;
  font-weight: 700 !important;
  border-color: #7469b6 !important;
  box-shadow: 0 3px 12px rgba(116, 105, 182, 0.25) !important;
}

body.theme-light .master-item-row.active {
  border-left: 4px solid #7469b6 !important;
  background-color: rgba(225, 175, 209, 0.35) !important;
}""")

    c = c.replace(".detail-toolbar-right:hover {\n  border-color: rgba(155, 242, 114, 0.4);\n}", """.detail-toolbar-right:hover {
  border-color: rgba(146, 144, 195, 0.5);
}
body.theme-light .detail-toolbar-right:hover {
  border-color: #7469b6;
}""")

    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
    print("Updated invoice-view.css successfully")

def update_auth_css():
    path = os.path.join(BASE_DIR, "css", "auth.css")
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()

    c = c.replace("#193440", "#1b1a55")
    c = c.replace("#9BF272", "#9290c3")
    c = c.replace("#7ABF5A", "#535c91")
    c = c.replace("#BAC8D9", "#cbd5e1")
    c = c.replace("155, 242, 114", "146, 144, 195")
    c = c.replace("122, 191, 90", "83, 92, 145")

    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
    print("Updated auth.css successfully")

def update_app_js():
    path = os.path.join(BASE_DIR, "js", "app.js")
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()

    old_snippet = """      const rgbDark = '20, 44, 55';
      const rgbDarkSurface = '25, 52, 64';
      const rgbLight = '255, 255, 255';
      const blurPx = Math.max(8, Math.min(36, Math.round(12 + val * 0.22)));
      const blurFilter = `blur(${blurPx}px) saturate(190%)`;

      if (isLight) {
        styleTag.textContent = `
          body.theme-light,
          body.theme-light .table-card,
          body.theme-light .kpi-card,
          body.theme-light .modal-dialog,
          body.theme-light .search-modal-card {
            background-color: rgba(${rgbLight}, ${alpha}) !important;
            backdrop-filter: ${blurFilter} !important;
            -webkit-backdrop-filter: ${blurFilter} !important;
          }
          body.theme-light .sidebar {
            background-color: rgba(${rgbLight}, ${alpha}) !important;
            backdrop-filter: ${blurFilter} !important;
            -webkit-backdrop-filter: ${blurFilter} !important;
          }
          body.theme-light .app-header {
            background-color: rgba(${rgbLight}, ${alpha}) !important;
            backdrop-filter: ${blurFilter} !important;
            -webkit-backdrop-filter: ${blurFilter} !important;
          }
          body.theme-light .table-header-toolbar,
          body.theme-light .glass-capsule-dock,
          body.theme-light .glass-transparency-dock,
          body.theme-light .header-right {
            background: rgba(${rgbLight}, ${alpha}) !important;
          }
          body.theme-light .btn-secondary {
            background-color: rgba(${rgbLight}, ${Math.min(1, parseFloat(alpha) + 0.05).toFixed(2)}) !important;
          }
        `;
      } else {
        styleTag.textContent = `
          body.theme-dark,
          body.theme-dark .table-card,
          body.theme-dark .kpi-card,
          body.theme-dark .modal-dialog,
          body.theme-dark .search-modal-card {
            background-color: rgba(${rgbDark}, ${alpha}) !important;
            backdrop-filter: ${blurFilter} !important;
            -webkit-backdrop-filter: ${blurFilter} !important;
          }
          body.theme-dark .sidebar {
            background-color: rgba(${rgbDark}, ${alpha}) !important;
            backdrop-filter: ${blurFilter} !important;
            -webkit-backdrop-filter: ${blurFilter} !important;
          }
          body.theme-dark .app-header {
            background-color: rgba(${rgbDark}, ${alpha}) !important;
            backdrop-filter: ${blurFilter} !important;
            -webkit-backdrop-filter: ${blurFilter} !important;
          }
          body.theme-dark .table-header-toolbar,
          body.theme-dark .glass-capsule-dock,
          body.theme-dark .glass-transparency-dock,
          body.theme-dark .header-right {
            background: rgba(${rgbDarkSurface}, ${alpha}) !important;
          }
          body.theme-dark .btn-secondary {
            background-color: rgba(${rgbDarkSurface}, ${Math.min(1, parseFloat(alpha) + 0.05).toFixed(2)}) !important;
          }
        `;
      }"""

    new_snippet = """      const rgbDark = '7, 15, 43';
      const rgbDarkSurface = '27, 26, 85';
      const rgbLight = '255, 230, 230';
      const blurPx = Math.max(8, Math.min(36, Math.round(12 + val * 0.22)));
      const blurFilter = `blur(${blurPx}px) saturate(190%)`;

      if (isLight) {
        styleTag.textContent = `
          body.theme-light,
          body.theme-light .table-card,
          body.theme-light .kpi-card,
          body.theme-light .modal-dialog,
          body.theme-light .search-modal-card {
            background-color: #ffffff !important;
            backdrop-filter: ${blurFilter} !important;
            -webkit-backdrop-filter: ${blurFilter} !important;
          }
          body.theme-light .sidebar {
            background-color: #ffffff !important;
            backdrop-filter: ${blurFilter} !important;
            -webkit-backdrop-filter: ${blurFilter} !important;
          }
          body.theme-light .app-header {
            background-color: #ffffff !important;
            backdrop-filter: ${blurFilter} !important;
            -webkit-backdrop-filter: ${blurFilter} !important;
          }
          body.theme-light .table-header-toolbar,
          body.theme-light .glass-capsule-dock,
          body.theme-light .glass-transparency-dock,
          body.theme-light .header-right {
            background: #ffffff !important;
          }
          body.theme-light .btn-secondary {
            background-color: #e1afd1 !important;
            color: #000000 !important;
            font-weight: 700 !important;
            border: 1.5px solid #ad88c6 !important;
          }
        `;
      } else {
        styleTag.textContent = `
          body.theme-dark,
          body.theme-dark .table-card,
          body.theme-dark .kpi-card,
          body.theme-dark .modal-dialog,
          body.theme-dark .search-modal-card {
            background-color: rgba(${rgbDarkSurface}, ${alpha}) !important;
            backdrop-filter: ${blurFilter} !important;
            -webkit-backdrop-filter: ${blurFilter} !important;
          }
          body.theme-dark .sidebar {
            background-color: rgba(${rgbDarkSurface}, ${alpha}) !important;
            backdrop-filter: ${blurFilter} !important;
            -webkit-backdrop-filter: ${blurFilter} !important;
          }
          body.theme-dark .app-header {
            background-color: rgba(${rgbDarkSurface}, ${alpha}) !important;
            backdrop-filter: ${blurFilter} !important;
            -webkit-backdrop-filter: ${blurFilter} !important;
          }
          body.theme-dark .table-header-toolbar,
          body.theme-dark .glass-capsule-dock,
          body.theme-dark .glass-transparency-dock,
          body.theme-dark .header-right {
            background: rgba(${rgbDarkSurface}, ${alpha}) !important;
          }
          body.theme-dark .btn-secondary {
            background-color: rgba(${rgbDarkSurface}, ${Math.min(1, parseFloat(alpha) + 0.05).toFixed(2)}) !important;
            color: #ffffff !important;
          }
        `;
      }"""

    if old_snippet in c:
        c = c.replace(old_snippet, new_snippet)

    c = c.replace("""const glowColor = isLight ? '#7ABF5A' : '#9BF272';
        const trackBase = isLight ? 'rgba(186, 200, 217, 0.45)' : 'rgba(186, 200, 217, 0.20)';""", """const glowColor = isLight ? '#7469b6' : '#9290c3';
        const trackBase = isLight ? 'rgba(173, 136, 198, 0.45)' : 'rgba(83, 92, 145, 0.35)';""")

    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
    print("Updated app.js successfully")

def update_auth_modal_js():
    path = os.path.join(BASE_DIR, "js", "components", "auth-modal.js")
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()

    c = c.replace("""<span style="color:#9BF272;">&#9679;</span> Login as Admin""", """<span style="color:#9290c3;">&#9679;</span> Login as Admin""")
    c = c.replace("""<span style="color:#7ABF5A;">&#9679;</span> Login as Customer""", """<span style="color:#535c91;">&#9679;</span> Login as Customer""")

    c = c.replace("""        if (user.role === 'customer') {
          badgeEl.style.color = '#7ABF5A';
          badgeEl.style.borderColor = 'rgba(122, 191, 90, 0.4)';
          badgeEl.style.background = 'rgba(122, 191, 90, 0.15)';
        } else {
          badgeEl.style.color = '#9BF272';
          badgeEl.style.borderColor = 'rgba(155, 242, 114, 0.4)';
          badgeEl.style.background = 'rgba(155, 242, 114, 0.2)';
        }""", """        if (user.role === 'customer') {
          badgeEl.style.color = '#535c91';
          badgeEl.style.borderColor = 'rgba(83, 92, 145, 0.4)';
          badgeEl.style.background = 'rgba(83, 92, 145, 0.15)';
        } else {
          badgeEl.style.color = '#9290c3';
          badgeEl.style.borderColor = 'rgba(146, 144, 195, 0.4)';
          badgeEl.style.background = 'rgba(146, 144, 195, 0.2)';
        }""")

    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
    print("Updated auth-modal.js successfully")

if __name__ == "__main__":
    update_components_css()
    update_sidebar_css()
    update_invoice_view_css()
    update_auth_css()
    update_app_js()
    update_auth_modal_js()
    print("All palette updates completed!")

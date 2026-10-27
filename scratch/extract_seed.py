import re
import json

with open('js/store.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_str = 'const DEFAULT_DATA = '
start_idx = content.find(start_str) + len(start_str)
end_str = '\n  };\n\n  class Store {'
end_idx = content.find(end_str) + 4 # include '};'

js_obj = content[start_idx:end_idx].strip()
if js_obj.endswith(';'):
    js_obj = js_obj[:-1].strip()

# Convert JS object to JSON
# 1. Remove comments
js_obj = re.sub(r'//.*', '', js_obj)
# 2. Quote unquoted keys: e.g. (\w+): -> "\1":
# Be careful not to quote inside strings or URLs
def quote_keys(text):
    # Regex for object keys: at beginning of line or after { or , with optional whitespace
    pattern = r'([{,]\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*:'
    return re.sub(pattern, r'\1"\2":', text)

# Let's do this carefully
# Or simpler: use a quick python regex or jscode
fixed_json = quote_keys(js_obj)
# Clean trailing commas before } or ]
fixed_json = re.sub(r',\s*([}\]])', r'\1', fixed_json)

try:
    data = json.loads(fixed_json)
    with open('default_data.json', 'w', encoding='utf-8') as out:
        json.dump(data, out, indent=2)
    print("SUCCESS: default_data.json created!")
    print("Keys:", list(data.keys()))
    print("Estimates:", len(data.get('estimates', [])))
    print("Invoices:", len(data.get('invoices', [])))
except Exception as e:
    print("JSON parse error:", e)
    # Save scratch to debug
    with open('scratch/debug_json.txt', 'w', encoding='utf-8') as out:
        out.write(fixed_json)
    # Print error snippet
    if hasattr(e, 'pos'):
        pos = e.pos
        snippet = fixed_json[max(0, pos-100):min(len(fixed_json), pos+100)]
        print(f"Error around pos {pos}:\n{snippet}")

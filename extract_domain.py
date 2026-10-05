import os
import re
import json
from collections import Counter

DOMAIN_DIR = r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\domain"

def extract_strings(directory):
    strings = set()
    pattern = re.compile(r'"([^"\\]*(?:\\.[^"\\]*)*)"')
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.kt') and not file.endswith('Test.kt'):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    content = f.read()
                    matches = pattern.findall(content)
                    for m in matches:
                        # Exclude strings that look like regexes, format strings, UUIDs, single chars, technical keys
                        if len(m) > 2 and ' ' in m and '{' not in m and '\\' not in m and '/' not in m and not re.match(r'^[A-Z_]+$', m):
                            if not m.startswith('yyyy') and not m.startswith('dd'):
                                strings.add(m)
    
    return sorted(list(strings))

if __name__ == "__main__":
    extracted = extract_strings(DOMAIN_DIR)
    with open("domain_strings.json", "w", encoding="utf-8") as f:
        json.dump(extracted, f, indent=2, ensure_ascii=False)
    print(f"Extracted {len(extracted)} domain strings.")

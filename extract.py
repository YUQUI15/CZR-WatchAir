import os
import re
import json

UI_DIR = r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair"

def extract_strings(directory):
    strings = set()
    # Simple regex for finding double-quoted strings that look like human text
    # Avoid things that look like code (no spaces, pure camelCase, etc)
    # Match strings that have at least one space or start with a capital letter and are 3+ chars
    pattern = re.compile(r'"([^"\\]*(?:\\.[^"\\]*)*)"')
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.kt'):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    content = f.read()
                    matches = pattern.findall(content)
                    for m in matches:
                        if len(m) > 2 and (m[0].isupper() or ' ' in m) and '{' not in m and '\\' not in m and '/' not in m:
                            strings.add(m)
    
    return sorted(list(strings))

if __name__ == "__main__":
    extracted = extract_strings(UI_DIR)
    with open("strings_to_translate.json", "w", encoding="utf-8") as f:
        json.dump(extracted, f, indent=2, ensure_ascii=False)
    print(f"Extracted {len(extracted)} strings.")

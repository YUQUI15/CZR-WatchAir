import os
import re
import json
from collections import Counter

UI_DIR = r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\ui"

def extract_ui_strings(directory):
    strings = Counter()
    
    # Matches Text("...") or StableCaption("...") or contentDescription = "..."
    # We only capture the inner string.
    patterns = [
        re.compile(r'Text\s*\(\s*"([^"\\]*(?:\\.[^"\\]*)*)"\s*\)'),
        re.compile(r'Text\s*\(\s*text\s*=\s*"([^"\\]*(?:\\.[^"\\]*)*)"'),
        re.compile(r'contentDescription\s*=\s*"([^"\\]*(?:\\.[^"\\]*)*)"'),
        re.compile(r'StableCaption\s*\(\s*"([^"\\]*(?:\\.[^"\\]*)*)"\s*\)')
    ]
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.kt'):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    content = f.read()
                    for pattern in patterns:
                        matches = pattern.findall(content)
                        for m in matches:
                            if len(m) > 1 and not m.isupper():
                                strings[m] += 1
    
    return [s for s, _ in strings.most_common()]

if __name__ == "__main__":
    extracted = extract_ui_strings(UI_DIR)
    with open("ui_strings.json", "w", encoding="utf-8") as f:
        json.dump(extracted, f, indent=2, ensure_ascii=False)
    print(f"Extracted {len(extracted)} pure UI strings.")

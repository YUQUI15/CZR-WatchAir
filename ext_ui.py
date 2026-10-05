import os
import re
import json

directories = [
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\ui\screen",
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\ui"
]

all_strings = set()

for d in directories:
    for file in os.listdir(d):
        if file.endswith('.kt') and file != 'SettingsScreen.kt':
            filepath = os.path.join(d, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            pattern = re.compile(r'"([^"\\]*(?:\\.[^"\\]*)*)"')
            matches = set(pattern.findall(content))
            
            for m in matches:
                # Filter out pure code/keys
                if len(m) > 2 and ' ' in m and not '{' in m and not re.match(r'^[A-Z0-9_]+$', m):
                    # Also filter out strings that look already Spanish
                    if not re.search(r'\b(de|la|el|en|y|que|los|por|para|con|las|una|un|es)\b', m.lower()):
                        all_strings.add(m)

with open('ui_strings.json', 'w', encoding='utf-8') as f:
    json.dump(sorted(list(all_strings)), f, indent=2, ensure_ascii=False)

import re
import json

with open('app/src/main/java/app/czrwatchair/ui/screen/SettingsScreen.kt', 'r', encoding='utf-8') as f:
    content = f.read()

matches = set(re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', content))
strings = [m for m in matches if ' ' in m and len(m) > 2 and '{' not in m and not re.match(r'^[A-Z_]+$', m)]

with open('settings_strings.json', 'w', encoding='utf-8') as f:
    json.dump(sorted(strings), f, indent=2, ensure_ascii=False)

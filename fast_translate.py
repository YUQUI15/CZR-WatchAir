import os
import re
import sys
import json
import urllib.request
import urllib.parse
import time

sys.stdout.reconfigure(encoding='utf-8')

def translate_text(text):
    if not text.strip():
        return text
    url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=es&dt=t&q=" + urllib.parse.quote(text)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return "".join([x[0] for x in data[0]])
    except Exception as e:
        print(f"API Error for '{text}': {e}")
        return text

files_to_check = [
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\domain\DebriefReport.kt",
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\domain\DebriefPdf.kt",
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\domain\SitExport.kt",
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\domain\DeviceExplain.kt",
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\domain\SitDiff.kt",
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\domain\Sit.kt",
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\domain\DeviceDetailText.kt"
]

placeholder_pattern = re.compile(r'(\$[a-zA-Z0-9]+|\$\{[a-zA-Z0-9_.]+\}|%\.[0-9]+[a-z]|%[a-z])')

def protect_string(text):
    placeholders = []
    def repl(m):
        placeholders.append(m.group(1))
        return f"__PH{len(placeholders)-1}__"
    protected = placeholder_pattern.sub(repl, text)
    return protected, placeholders

def unprotect_string(text, placeholders):
    for i, ph in enumerate(placeholders):
        text = text.replace(f"__PH{i}__", ph).replace(f"__ PH{i} __", ph).replace(f"__ PH {i}__", ph).replace(f"__PH {i}__", ph)
    return text

def run():
    for filepath in files_to_check:
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        pattern = re.compile(r'"([^"\\]*(?:\\.[^"\\]*)*)"')
        matches = list(set(pattern.findall(content)))
        
        modified = False
        
        for m in matches:
            if len(m) < 3 or not ' ' in m or re.match(r'^[A-Z_]+$', m) or '{' in m and not m.startswith('$'):
                continue
                
            protected_text, phs = protect_string(m)
            translated = translate_text(protected_text)
            final_text = unprotect_string(translated, phs)
            
            if final_text and final_text != m:
                esc_m = re.escape(m)
                rep_pattern = re.compile(r'"' + esc_m + r'"')
                new_content = rep_pattern.sub(f'"{final_text}"', content)
                if new_content != content:
                    content = new_content
                    modified = True
                    print(f"[{os.path.basename(filepath)}] '{m}' -> '{final_text}'")
                
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == "__main__":
    run()
    print("Done translating.")

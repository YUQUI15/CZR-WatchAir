import os
import re
import sys
import time
from googletrans import Translator

sys.stdout.reconfigure(encoding='utf-8')

files_to_check = [
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\domain\DebriefReport.kt",
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\domain\DebriefPdf.kt",
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\domain\SitExport.kt",
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\domain\DeviceExplain.kt",
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\domain\SitDiff.kt",
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\domain\Sit.kt",
    r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\domain\DeviceDetailText.kt"
]

translator = Translator()

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
        text = text.replace(f"__PH{i}__", ph)
        text = text.replace(f"__ PH{i} __", ph)
        text = text.replace(f"__ PH {i}__", ph)
        text = text.replace(f"__PH {i}__", ph)
    return text

def translate_exact_strings():
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
            try:
                translated = translator.translate(protected_text, src='en', dest='es').text
                final_text = unprotect_string(translated, phs)
                
                if final_text and final_text != m:
                    esc_m = re.escape(m)
                    rep_pattern = re.compile(r'"' + esc_m + r'"')
                    new_content = rep_pattern.sub(f'"{final_text}"', content)
                    if new_content != content:
                        content = new_content
                        modified = True
                        print(f"[{os.path.basename(filepath)}] '{m}' -> '{final_text}'")
            except Exception as e:
                pass
                
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == "__main__":
    translate_exact_strings()
    print("Done translating domains.")

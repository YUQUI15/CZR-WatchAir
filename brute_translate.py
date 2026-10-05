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
    # Avoid translating single words that might be code keys unless they are capitalized like a label.
    if len(text.split()) == 1 and not text[0].isupper():
        return text

    url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=es&dt=t&q=" + urllib.parse.quote(text)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode('utf-8'))
            return "".join([x[0] for x in data[0]])
    except Exception as e:
        print(f"API Error for '{text}': {e}")
        return text

def get_all_kt_files(directory):
    kt_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.kt'):
                kt_files.append(os.path.join(root, file))
    return kt_files

files_to_check = get_all_kt_files(r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\ui")

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
    total_translated = 0
    for filepath in files_to_check:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find all strings
        pattern = re.compile(r'"([^"\\]*(?:\\.[^"\\]*)*)"')
        matches = list(set(pattern.findall(content)))
        
        modified = False
        
        for m in matches:
            # Skip likely code constants
            if len(m) < 2 or re.match(r'^[A-Z0-9_]+$', m) or m.startswith('/') or m.startswith('yyyy') or m.startswith('MM'):
                continue
            
            # Skip if it's already Spanish (very rough heuristic, just skip if it contains certain Spanish words)
            if re.search(r'\b(de|la|el|en|y|que|los|por|para|con|las|una|un|es)\b', m.lower()) and not "default" in m.lower():
                continue
                
            # If it's just one word and lowercase, probably a route or key
            if len(m.split()) == 1 and m.islower():
                continue

            protected_text, phs = protect_string(m)
            translated = translate_text(protected_text)
            final_text = unprotect_string(translated, phs)
            
            if final_text and final_text != m and "API Error" not in final_text:
                esc_m = re.escape(m)
                rep_pattern = re.compile(r'"' + esc_m + r'"')
                new_content = rep_pattern.sub(f'"{final_text}"', content)
                if new_content != content:
                    content = new_content
                    modified = True
                    total_translated += 1
                    print(f"[{os.path.basename(filepath)}] '{m}' -> '{final_text}'")
                
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
                
    print(f"Done translating UI. Total strings translated: {total_translated}")

if __name__ == "__main__":
    run()

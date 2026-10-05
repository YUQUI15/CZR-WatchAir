import os
import re
from googletrans import Translator

UI_DIR = r"C:\Users\cf039\.gemini\antigravity\scratch\Fieldwatch\app\src\main\java\app\czrwatchair\ui"

def translate_file(filepath, translator):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Patterns to match and replace
    # Pattern 1: Text("Something")
    pattern_text = re.compile(r'(Text\s*\(\s*")([^"\\]*(?:\\.[^"\\]*)*)("\s*\))')
    # Pattern 2: Text(text = "Something")
    pattern_text_named = re.compile(r'(Text\s*\(\s*text\s*=\s*")([^"\\]*(?:\\.[^"\\]*)*)("\s*(?:,|\)))')
    # Pattern 3: contentDescription = "Something"
    pattern_desc = re.compile(r'(contentDescription\s*=\s*")([^"\\]*(?:\\.[^"\\]*)*)(")')
    # Pattern 4: StableCaption("Something")
    pattern_caption = re.compile(r'(StableCaption\s*\(\s*")([^"\\]*(?:\\.[^"\\]*)*)("\s*\))')
    
    patterns = [pattern_text, pattern_text_named, pattern_desc, pattern_caption]
    
    modified = False
    
    for pattern in patterns:
        def repl(match):
            nonlocal modified
            prefix = match.group(1)
            text_to_translate = match.group(2)
            suffix = match.group(3)
            
            # Skip if already looks translated or short
            if len(text_to_translate) < 2 or text_to_translate.isupper():
                return match.group(0)
            
            try:
                translated = translator.translate(text_to_translate, src='en', dest='es').text
                # A bit of sanity check, if translation failed, keep original
                if translated and translated != text_to_translate:
                    modified = True
                    print(f"[{os.path.basename(filepath)}] '{text_to_translate}' -> '{translated}'")
                    return prefix + translated + suffix
            except Exception as e:
                print(f"Error translating '{text_to_translate}': {e}")
            
            return match.group(0)
            
        content = pattern.sub(repl, content)

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    translator = Translator()
    for root, _, files in os.walk(UI_DIR):
        for file in files:
            if file.endswith('.kt'):
                filepath = os.path.join(root, file)
                translate_file(filepath, translator)
    print("Done translating UI files.")

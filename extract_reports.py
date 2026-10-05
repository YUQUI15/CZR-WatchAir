import os
import re

files_to_check = [
    "app/src/main/java/app/czrwatchair/domain/DebriefReport.kt",
    "app/src/main/java/app/czrwatchair/domain/DebriefPdf.kt",
    "app/src/main/java/app/czrwatchair/domain/SitExport.kt",
    "app/src/main/java/app/czrwatchair/domain/DeviceExplain.kt",
    "app/src/main/java/app/czrwatchair/domain/SitDiff.kt",
    "app/src/main/java/app/czrwatchair/domain/Sit.kt",
    "app/src/main/java/app/czrwatchair/domain/DeviceDetailText.kt"
]

strings = set()
pattern = re.compile(r'"([^"\\]*(?:\\.[^"\\]*)*)"')

for filepath in files_to_check:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            matches = pattern.findall(content)
            for m in matches:
                if ' ' in m and not re.match(r'^[A-Z_]+$', m) and '{' not in m and '\\' not in m:
                    strings.add(m)

with open("report_strings.txt", "w", encoding="utf-8") as f:
    for s in sorted(list(strings)):
        f.write(f"{s}\n")

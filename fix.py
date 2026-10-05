import os
import shutil

# Rename content
for root, dirs, files in os.walk("."):
    if ".git" in root or "build" in root: continue
    for f in files:
        if not f.endswith((".kt", ".xml", ".kts", ".md", ".json", ".pro")): continue
        path = os.path.join(root, f)
        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
        except:
            continue
        
        orig = content
        if "strings.xml" in f:
            content = content.replace("Fieldwatch", "CZR WatchAir")
        if "README.md" in f:
            content = content.replace("Fieldwatch", "CZR WatchAir").replace("OffGridPete", "YUQUI15").replace("fieldwatch", "czrwatchair")
        if "settings.gradle.kts" in f:
            content = content.replace("Fieldwatch", "CZR-WatchAir")
        if "build.gradle.kts" in f:
            content = content.replace('applicationId = "app.fieldwatch"', 'applicationId = "app.czrwatchair"')
            
        content = content.replace("app.fieldwatch", "app.czrwatchair")
        
        if orig != content:
            with open(path, 'w', encoding='utf-8') as file:
                file.write(content)

# Rename directories safely
base = "app/src/main/java/app/"
if os.path.exists(base + "fieldwatch"):
    os.rename(base + "fieldwatch", base + "czrwatchair")
    
base_test = "app/src/test/java/app/"
if os.path.exists(base_test + "fieldwatch"):
    os.rename(base_test + "fieldwatch", base_test + "czrwatchair")

base_androidTest = "app/src/androidTest/java/app/"
if os.path.exists(base_androidTest + "fieldwatch"):
    os.rename(base_androidTest + "fieldwatch", base_androidTest + "czrwatchair")

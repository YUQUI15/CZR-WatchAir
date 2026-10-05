import re
content=open('app/src/main/java/app/czrwatchair/ui/NestedTabChrome.kt', encoding='utf-8').read()
for s in set(re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', content)):
    if ' ' in s or len(s)>3: print(s)

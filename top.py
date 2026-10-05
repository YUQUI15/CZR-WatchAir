import sys
lines = open('report_strings.txt', encoding='utf-8').readlines()
lines = [x.strip() for x in lines if len(x.strip()) > 10 and not x.strip().startswith('$')]
lines.sort(key=len, reverse=True)
with open('top100.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines[:100]))

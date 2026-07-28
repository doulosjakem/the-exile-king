with open(r'D:\the-exile-king\review_art_ollama.py', 'r', encoding='utf-8') as f:
    content = f.read()
import re
keys = re.findall(r'^\s+"([^"]+)":', content, re.MULTILINE)
for k in keys:
    if 'scout' in k or 'elite' in k or 'loyal' in k or 'guard' in k:
        print(k)

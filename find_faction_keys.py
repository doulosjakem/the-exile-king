with open(r'D:\the-exile-king\review_art_ollama.py', 'r', encoding='utf-8') as f:
    content = f.read()
import re
keys = re.findall(r'^\s+"([^"]+)":', content, re.MULTILINE)
for k in keys:
    if k.endswith('_david') or k.endswith('_jonathan') or k.endswith('_achish') or k.endswith('_ekron'):
        print(k)

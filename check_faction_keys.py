with open(r'D:\the-exile-king\review_art_ollama.py', 'r', encoding='utf-8') as f:
    content = f.read()
import re
keys = re.findall(r'^\s+"([^"]+)":', content, re.MULTILINE)
needed = ['swordsman_david', 'spearman_david', 'slinger_david', 'archer_david', 'scout_david']
for k in needed:
    print(f'{k}: {"PRESENT" if k in keys else "MISSING"}')

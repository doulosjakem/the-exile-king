with open(r'D:\the-exile-king\review_art_ollama.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1. Add 'prototype' to PROMPT_CHECK_FOLDERS
for i, line in enumerate(lines):
    if line.strip() == 'PROMPT_CHECK_FOLDERS = {':
        lines[i] = 'PROMPT_CHECK_FOLDERS = {\n    "prototype", '
        break

with open(r'D:\the-exile-king\review_art_ollama.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('Added prototype to PROMPT_CHECK_FOLDERS')

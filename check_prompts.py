import re

with open('review_art_ollama.py', encoding='utf-8') as f:
    content = f.read()

matches = re.findall(r'"(box-art[^"]*)"\s*:', content)
print('Box-art keys in EXPECTED_PROMPTS:')
for m in sorted(matches):
    print(' ', m)
print('Total:', len(matches))
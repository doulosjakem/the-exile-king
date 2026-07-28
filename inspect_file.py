with open(r'D:\the-exile-king\review_art_ollama.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find all function/block definitions and their line numbers
defs = []
for i, line in enumerate(lines, start=1):
    stripped = line.strip()
    if stripped.startswith('def ') or stripped.startswith('CHARACTER_KEYS') or stripped.startswith('TILE_KEYS') or stripped.startswith('UI_KEYS') or stripped.startswith('EQUIPMENT_KEYS') or stripped.startswith('CARD_KEYS') or stripped.startswith('PROMPT_CHECK_FOLDERS') or stripped.startswith('PROMPT_ALIASES') or stripped.startswith('PROTOTYPE_STEM_ALIASES'):
        defs.append((i, stripped[:80]))

for d in defs:
    print(f'{d[0]}: {d[1]}')

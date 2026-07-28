with open(r'D:\the-exile-king\review_art_ollama.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines, start=1):
    if '"david_commander":' in line or '"jonathan_commander":' in line or '"philistine_lord_commander":' in line or '"giant_achish":' in line:
        print(f'{i}: {line.strip()}')

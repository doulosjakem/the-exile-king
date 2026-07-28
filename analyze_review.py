import json
from collections import Counter

with open(r'D:\the-exile-king\prototype_review.json', 'r') as f:
    d = json.load(f)

print('=== TRASH FILES ===')
for img in d['images']:
    if img['decision'] == 'TRASH':
        print(f"{img['filename']} | score={img['score']} | {img['reason']}")

print('\n=== KEEP FILES WITH LOW SCORES (1-3) ===')
low_keep = [img for img in d['images'] if img['decision'] == 'KEEP' and img['score'] <= 3]
print(f'Count: {len(low_keep)}')
for img in low_keep[:20]:
    print(f"{img['filename']} | score={img['score']} | {img['reason']}")

# Categorize by failure type
trash_reasons = Counter()
for img in d['images']:
    if img['decision'] == 'TRASH':
        for reason in img['reason'].split('; '):
            trash_reasons[reason] += 1

keep_reasons = Counter()
for img in d['images']:
    if img['decision'] == 'KEEP':
        for reason in img['reason'].split('; '):
            keep_reasons[reason] += 1

print('\n=== FAILURE BREAKDOWN (TRASH) ===')
for reason, count in trash_reasons.most_common():
    print(f'  {count:3d} | {reason}')

print('\n=== ISSUE BREAKDOWN (KEEP, score<=3) ===')
low_keep_reasons = Counter()
for img in low_keep:
    for reason in img['reason'].split('; '):
        low_keep_reasons[reason] += 1
for reason, count in low_keep_reasons.most_common():
    print(f'  {count:3d} | {reason}')

# By asset type
print('\n=== BY ASSET CATEGORY ===')
for asset in ['character', 'card', 'tile', 'equipment', 'ui']:
    imgs = [i for i in d['images'] if i.get('asset_type') == asset]
    if imgs:
        keep = sum(1 for i in imgs if i['decision'] == 'KEEP')
        trash = sum(1 for i in imgs if i['decision'] == 'TRASH')
        avg_score = sum(i['score'] for i in imgs) / len(imgs)
        print(f'{asset}: {len(imgs)} total, KEEP={keep}, TRASH={trash}, avg_score={avg_score:.1f}')
        
# By subfolder
print('\n=== BY SUBFOLDER (top 15) ===')
subfolder_stats = {}
for img in d['images']:
    sf = img['filename'].split('\\')[0] if '\\' in img['filename'] else 'root'
    if sf not in subfolder_stats:
        subfolder_stats[sf] = {'total': 0, 'trash': 0, 'low_keep': 0}
    subfolder_stats[sf]['total'] += 1
    if img['decision'] == 'TRASH':
        subfolder_stats[sf]['trash'] += 1
    if img['decision'] == 'KEEP' and img.get('score', 5) <= 3:
        subfolder_stats[sf]['low_keep'] += 1

for sf, stats in sorted(subfolder_stats.items(), key=lambda x: -x[1]['total'])[:15]:
    print(f"  {sf}: {stats['total']} total, {stats['trash']} trash, {stats['low_keep']} low-keep")

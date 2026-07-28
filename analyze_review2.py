import json

with open(r'D:\the-exile-king\prototype_review.json', 'r') as f:
    d = json.load(f)

print('=== SUMMARY ===')
print(f'Total: {d["total_reviewed"]}')
print(f'KEEP: {d["keep"]}')
print(f'TRASH: {d["trash"]}')
print(f'Errors: {d["errors"]}')
print(f'No prompt match: {d["no_prompt_match"]}')
print(f'Model: {d["model"]}')

print('\n=== TRASH FILES ===')
for img in d['images']:
    if img['decision'] == 'TRASH':
        print(f"{img['filename']}")
        print(f"  score={img['score']}")
        print(f"  reason={img['reason']}")

print('\n=== LOW-SCORE KEEP BY CATEGORY ===')
low_keep = [img for img in d['images'] if img['decision'] == 'KEEP' and img.get('score', 5) <= 3]
for img in low_keep[:5]:
    print(f"{img['filename']} | score={img['score']} | {img['reason']}")
print(f'... and {len(low_keep) - 5} more low-score KEEP files')

# Group by asset type
from collections import defaultdict
by_type = defaultdict(list)
for img in d['images']:
    by_type[img.get('asset_type', 'unknown')].append(img)

for asset_type, imgs in sorted(by_type.items()):
    keep = sum(1 for i in imgs if i['decision'] == 'KEEP')
    trash = sum(1 for i in imgs if i['decision'] == 'TRASH')
    avg_score = sum(i.get('score', 0) for i in imgs) / len(imgs) if imgs else 0
    print(f'{asset_type}: {len(imgs)} total, KEEP={keep}, TRASH={trash}, avg_score={avg_score:.1f}')

# Group low-keep by subfolder
from collections import Counter
subfolder_issues = Counter()
for img in low_keep:
    sf = img['filename'].split('\\')[0]
    subfolder_issues[sf] += 1

print('\n=== LOW-KEEP BY SUBFOLDER ===')
for sf, count in subfolder_issues.most_common():
    print(f'  {sf}: {count} low-keep files')

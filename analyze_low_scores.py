import json
from collections import Counter

with open('full_review.json', 'r') as f:
    data = json.load(f)

low = [img for img in data['images'] if img['score'] <= 3]
print("Total low-scored:", len(low))
print("Score 1:", len([x for x in low if x["score"]==1]))
print("Score 2:", len([x for x in low if x["score"]==2]))
print("Score 3:", len([x for x in low if x["score"]==3]))

# Check score-3 reasons
reasons3 = Counter()
for img in low:
    if img['score'] == 3:
        reasons3[img['reason']] += 1
print("\nScore 3 reasons:")
for r, c in reasons3.most_common():
    print("  {}: {}".format(r, c))

# Check score 1-2 reasons
reasons12 = Counter()
for img in low:
    if img['score'] <= 2:
        reasons12[img['reason']] += 1
print("\nScore 1-2 reasons:")
for r, c in reasons12.most_common():
    print("  {}: {}".format(r, c))

# Score 3 decisions
decisions = Counter()
for img in low:
    if img['score'] == 3:
        decisions[img['decision']] += 1
print("\nScore 3 decisions: KEEP={}, TRASH={}".format(decisions.get("KEEP",0), decisions.get("TRASH",0)))

# Group by expected_prompt_key
keys = Counter()
for img in low:
    k = img.get('expected_prompt_key') or 'null'
    keys[k] += 1
print("\nBy expected_prompt_key:")
for k, c in keys.most_common():
    print("  {}: {}".format(k, c))

# Group by asset_type
types = Counter()
for img in low:
    t = img.get('asset_type') or 'unknown'
    types[t] += 1
print("\nBy asset_type:")
for t, c in types.most_common():
    print("  {}: {}".format(t, c))

# Show all unique filenames for null expected_prompt_key
null_files = [img for img in low if img.get('expected_prompt_key') is None]
print("\nNull expected_prompt_key files ({}):".format(len(null_files)))
for img in null_files:
    print("  {} (score={}, reason={})".format(img["filename"], img["score"], img["reason"]))

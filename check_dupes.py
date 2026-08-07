import json, os
from collections import Counter

with open("re_review_report.json") as f:
    report = json.load(f)

basenames = [os.path.basename(img["filename"]) for img in report["images"]]
dupes = [b for b, c in Counter(basenames).items() if c > 1]
print(f"Report entries: {len(report['images'])}")
print(f"Unique basenames: {len(set(basenames))}")
print(f"Duplicate basenames: {len(dupes)}")
for d in dupes[:5]:
    print(f"  {d}")

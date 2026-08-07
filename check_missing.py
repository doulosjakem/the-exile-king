import json

with open("re_review_report.json") as f:
    report = json.load(f)

missing_basename = "slinger-david_00003_.png"
found = False
for img in report["images"]:
    if img["filename"].endswith(missing_basename):
        found = True
        print(f"Found in re_review_report:")
        print(f"  filename: {img['filename']}")
        print(f"  score: {img['score']}")
        print(f"  decision: {img['decision']}")
        print(f"  reason: {img['reason']}")
        break

if not found:
    print(f"NOT found in re_review_report")
    
with open("rereview_queue.json") as f:
    queue = json.load(f)

for item in queue:
    if item["filename"].endswith(missing_basename):
        print(f"Found in rereview_queue:")
        print(f"  filename: {item['filename']}")
        print(f"  old_score: {item['old_score']}")
        break
else:
    print(f"NOT found in rereview_queue")

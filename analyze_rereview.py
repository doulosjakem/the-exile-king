import json
from collections import Counter

with open("re_review_report.json") as f:
    report = json.load(f)

print("=== Re-review Results ===")
print(f"Total reviewed: {report['total_reviewed']}")
print(f"KEEP: {report['keep']}")
print(f"TRASH: {report['trash']}")
print(f"No prompt match: {report['no_prompt_match']}")
print()

scores = Counter(img["score"] for img in report["images"])
print("Score distribution (new reviews):")
for s in sorted(scores.keys(), reverse=True):
    print(f"  Score {s}: {scores[s]} files")
print()

improved = sum(1 for img in report["images"] if img["score"] > img["old_score"])
degraded = sum(1 for img in report["images"] if img["score"] < img["old_score"])
same = sum(1 for img in report["images"] if img["score"] == img["old_score"])
print(f"Score changes: improved={improved}, degraded={degraded}, same={same}")
print()

print("Improved examples:")
count = 0
for img in report["images"]:
    if img["score"] > img["old_score"]:
        print(f"  {img['filename']}: {img['old_score']} -> {img['score']} ({img['reason']})")
        count += 1
        if count >= 5:
            break

print()
print("Degraded examples:")
count = 0
for img in report["images"]:
    if img["score"] < img["old_score"]:
        print(f"  {img['filename']}: {img['old_score']} -> {img['score']} ({img['reason']})")
        count += 1
        if count >= 5:
            break

print()
print("Still score 3 examples:")
count = 0
for img in report["images"]:
    if img["score"] == 3:
        print(f"  {img['filename']}: {img['reason']}")
        count += 1
        if count >= 10:
            break

import json
from collections import Counter

with open("re_review_report.json") as f:
    report = json.load(f)

print(f"Total reviewed: {report['total_reviewed']}")
print(f"KEEP: {report['keep']}")
print(f"TRASH: {report['trash']}")
print()

scores = Counter(img["score"] for img in report["images"])
print("Score distribution:")
for s in sorted(scores.keys(), reverse=True):
    print(f"  Score {s}: {scores[s]}")
print()

improved = sum(1 for img in report["images"] if img["score"] > img["old_score"])
degraded = sum(1 for img in report["images"] if img["score"] < img["old_score"])
same = sum(1 for img in report["images"] if img["score"] == img["old_score"])
print(f"Score changes vs old: improved={improved}, degraded={degraded}, same={same}")
print()

print("Improved:")
for img in report["images"]:
    if img["score"] > img["old_score"]:
        print(f"  {img['filename']}: {img['old_score']} -> {img['score']} ({img['reason']})")

print()
print("Degraded:")
for img in report["images"]:
    if img["score"] < img["old_score"]:
        print(f"  {img['filename']}: {img['old_score']} -> {img['score']} ({img['reason']})")

print()
score3_reasons = Counter()
for img in report["images"]:
    if img["score"] == 3:
        score3_reasons[img["reason"]] += 1
print("Score 3 reasons:")
for reason, count in score3_reasons.most_common():
    print(f"  {count}: {reason}")

print()
score5_examples = [img for img in report["images"] if img["score"] == 5]
print(f"Score 5 examples ({len(score5_examples)}):")
for img in score5_examples[:5]:
    print(f"  {img['filename']}: {img['reason']}")

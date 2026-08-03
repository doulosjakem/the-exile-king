"""Merge re_review_report.json results into full_review.json.
For each image in the re-review report, replace ALL entries in full_review.json
that match the same basename with the new review result.
"""
import json
import os
import sys
from collections import Counter

# Load full_review.json
with open("full_review.json", "r", encoding="utf-8") as f:
    full = json.load(f)

# Load re-review report
with open("re_review_report.json", "r", encoding="utf-8") as f:
    re_review = json.load(f)

# Build a map of basename -> new review entry
new_by_basename = {}
for img in re_review["images"]:
    basename = os.path.basename(img["filename"])
    new_by_basename[basename] = img

print(f"New review entries: {len(new_by_basename)}")

# Remove old entries for files that are being re-reviewed, then add new entries
old_images = full["images"]
removed = 0
kept = 0
updated = []

for img in old_images:
    basename = os.path.basename(img["filename"])
    if basename in new_by_basename:
        removed += 1
    else:
        updated.append(img)
        kept += 1

# Add new entries
for basename, img in new_by_basename.items():
    # Reconstruct the entry in the full_review.json format
    new_entry = {
        "filename": img["filename"],
        "score": img["score"],
        "decision": img["decision"],
        "reason": img["reason"],
        "answers": img.get("answers", []),
        "raw_response": img.get("raw_response", ""),
        "expected_prompt_key": img.get("expected_prompt_key"),
        "asset_type": img.get("asset_type"),
        "expected_prompt": img.get("expected_prompt"),
        "old_score": img.get("old_score"),
        "old_decision": img.get("old_decision"),
        "review_model": img.get("review_model"),
        "timestamp": img.get("timestamp"),
    }
    updated.append(new_entry)

# Sort by filename for consistency
updated.sort(key=lambda x: x["filename"])

# Update counts
full["images"] = updated
full["total_reviewed"] = len(updated)
full["keep"] = sum(1 for img in updated if img["decision"] == "KEEP")
full["trash"] = sum(1 for img in updated if img["decision"] == "TRASH")
full["errors"] = sum(1 for img in updated if img["decision"] == "ERROR")
full["no_prompt_match"] = sum(1 for img in updated if img["expected_prompt_key"] is None)
full["timestamp"] = json.dumps({})  # just update timestamp to now
import time
full["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")

# Save
with open("full_review.json", "w", encoding="utf-8") as f:
    json.dump(full, f, indent=2, ensure_ascii=False)

print(f"Removed old entries: {removed}")
print(f"Kept existing entries: {kept}")
print(f"Added new entries: {len(new_by_basename)}")
print(f"Total entries: {len(updated)}")
print(f"KEEP: {full['keep']}")
print(f"TRASH: {full['trash']}")
print(f"Errors: {full['errors']}")
print(f"No prompt match: {full['no_prompt_match']}")
print()

# Score distribution for current 458 files on disk
outputBase = r"D:\Jake\ComfyUI_windows_portable\ComfyUI\output\ComfyUI\annointed-exile\prototype"
protoDirs = ["card-backs", "commander-cards", "equipment", "hex-tiles", "ui", "unit-cards", "unit-discs"]
score_dist = Counter()
decision_dist = Counter()
total_on_disk = 0
for d in protoDirs:
    dirPath = os.path.join(outputBase, d)
    if os.path.isdir(dirPath):
        for f in os.listdir(dirPath):
            if f.endswith(".png"):
                total_on_disk += 1
                if f in new_by_basename:
                    # Use new review
                    img = new_by_basename[f]
                    score_dist[img["score"]] += 1
                    decision_dist[img["decision"]] += 1
                else:
                    # Find in full_review.json
                    for img in updated:
                        if os.path.basename(img["filename"]) == f:
                            score_dist[img["score"]] += 1
                            decision_dist[img["decision"]] += 1
                            break

print(f"Score distribution for {total_on_disk} files on disk:")
for s in sorted(score_dist.keys(), reverse=True):
    print(f"  Score {s}: {score_dist[s]} files")
print()
print("Decision distribution:")
for dec in sorted(decision_dist.keys()):
    print(f"  {dec}: {decision_dist[dec]} files")

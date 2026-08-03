"""Merge new review results into full_review.json."""
import json, os

PROJECT_DIR = r"D:\the-exile-king"
existing_path = os.path.join(PROJECT_DIR, "full_review.json")
new_path = os.path.join(PROJECT_DIR, "new_images_review.json")

existing = json.load(open(existing_path))
new = json.load(open(new_path))

existing_images = {img["filename"]: img for img in existing.get("images", [])}
added = 0
for img in new.get("images", []):
    if img["filename"] not in existing_images:
        existing_images[img["filename"]] = img
        added += 1

existing["images"] = list(existing_images.values())
existing["keep"] = sum(1 for img in existing["images"] if img.get("decision") == "KEEP")
existing["trash"] = sum(1 for img in existing["images"] if img.get("decision") == "TRASH")
existing["total_reviewed"] = len(existing["images"])

with open(existing_path, "w", encoding="utf-8") as f:
    json.dump(existing, f, indent=2, ensure_ascii=False)

print(f"Added {added} new images")
print(f"Total reviewed: {existing['total_reviewed']}")
print(f"KEEP: {existing['keep']}")
print(f"TRASH: {existing['trash']}")

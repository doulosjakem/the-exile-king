import json, os, time

with open("full_review.json", "r", encoding="utf-8") as f:
    full = json.load(f)

# Add the missing file's review entry
new_entry = {
    "filename": "unit-discs/slinger-david_00003_.png",
    "expected_prompt_key": "slinger_david",
    "asset_type": "character",
    "expected_prompt": "ONE PERSON ONLY, solo portrait, waist-up, David's slinger, bronze age Levantine Israelite skirmisher",
    "decision": "KEEP",
    "score": 3,
    "reason": "does not match expected prompt",
    "answers": ["YES", "NO", "NO", "NO"],
    "raw_response": "1. Yes\n2. No\n3. No\n4. No",
    "old_score": 0,
    "old_decision": "UNREVIEWED",
    "review_model": "llava-phi3:3.8b",
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
}

full["images"].append(new_entry)
full["total_reviewed"] = len(full["images"])
full["keep"] = sum(1 for img in full["images"] if img["decision"] == "KEEP")
full["trash"] = sum(1 for img in full["images"] if img["decision"] == "TRASH")
full["errors"] = sum(1 for img in full["images"] if img["decision"] == "ERROR")
full["no_prompt_match"] = sum(1 for img in full["images"] if img["expected_prompt_key"] is None)

with open("full_review.json", "w", encoding="utf-8") as f:
    json.dump(full, f, indent=2, ensure_ascii=False)

print(f"Added missing entry for slinger-david_00003_.png")
print(f"Total entries: {full['total_reviewed']}")
print(f"KEEP: {full['keep']}")
print(f"TRASH: {full['trash']}")
print(f"No prompt match: {full['no_prompt_match']}")

# Verify all 458 files are now reviewed
outputBase = r"D:\Jake\ComfyUI_windows_portable\ComfyUI\output\ComfyUI\annointed-exile\prototype"
protoDirs = ["card-backs", "commander-cards", "equipment", "hex-tiles", "ui", "unit-cards", "unit-discs"]

reviews = {}
for img in full["images"]:
    basename = os.path.basename(img["filename"])
    reviews[basename] = img

missing = 0
for d in protoDirs:
    dirPath = os.path.join(outputBase, d)
    if os.path.isdir(dirPath):
        for f in os.listdir(dirPath):
            if f.endswith(".png") and f not in reviews:
                missing += 1
                print(f"  STILL MISSING: {d}/{f}")

print(f"\nMissing from review: {missing}")
print(f"All 458 files reviewed: {missing == 0}")

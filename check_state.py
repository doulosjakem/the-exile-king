import json, os

with open("full_review.json") as f:
    full = json.load(f)

reviews = {}
for img in full["images"]:
    basename = os.path.basename(img["filename"])
    if basename not in reviews:
        reviews[basename] = img

outputBase = r"D:\Jake\ComfyUI_windows_portable\ComfyUI\output\ComfyUI\annointed-exile\prototype"
protoDirs = ["card-backs", "commander-cards", "equipment", "hex-tiles", "ui", "unit-cards", "unit-discs"]

missing = []
low_score = []
for d in protoDirs:
    dirPath = os.path.join(outputBase, d)
    if os.path.isdir(dirPath):
        for f in os.listdir(dirPath):
            if f.endswith(".png"):
                if f not in reviews:
                    missing.append(f"{d}/{f}")
                elif reviews[f].get("score", 0) < 3:
                    low_score.append(f"{d}/{f} (score={reviews[f]['score']}, decision={reviews[f]['decision']})")

print(f"Missing from review: {len(missing)}")
for m in missing[:5]:
    print(f"  {m}")

print(f"\nFiles with score < 3 on disk: {len(low_score)}")
for l in low_score[:5]:
    print(f"  {l}")

# Check TRASH files
trash_files = [img for img in full["images"] if img.get("decision") == "TRASH"]
print(f"\nTotal TRASH entries in full_review.json: {len(trash_files)}")
on_disk_trash = 0
for img in trash_files:
    basename = os.path.basename(img["filename"])
    for d in protoDirs:
        dirPath = os.path.join(outputBase, d)
        if os.path.isdir(dirPath) and basename in os.listdir(dirPath):
            on_disk_trash += 1
            print(f"  ON DISK: {d}/{basename} (score={img['score']})")
print(f"TRASH files still on disk: {on_disk_trash}")

# Check if prep_regen_batch sees 458 files as complete
print(f"\n=== Full state ===")
total = 0
for d in protoDirs:
    dirPath = os.path.join(outputBase, d)
    if os.path.isdir(dirPath):
        count = len([f for f in os.listdir(dirPath) if f.endswith(".png")])
        total += count
print(f"Total files on disk: {total}")
print(f"All KEEP, no TRASH on disk: {on_disk_trash == 0}")

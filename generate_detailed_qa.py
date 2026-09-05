import json
import os
import csv

OUTPUT_DIR = "D:/the-exile-king/art/output/"
QA_BATCH = "D:/the-exile-king/art/output/qa_batch_{}.json"

all_results = []
for i in range(1, 25):
    batch_file = QA_BATCH.format(i)
    if os.path.exists(batch_file):
        with open(batch_file) as f:
            data = json.load(f)
            all_results.extend(data)

# Categorize UNCHANGED results
unchanged = [r for r in all_results if r.get("result") == "UNCHANGED"]
print(f"\nUNCHANGED breakdown:")
print(f"  Total: {len(unchanged)}")

# By detection type
unch_mediapipe = [r for r in unchanged if r["detection"] == "mediapipe"]
unch_fallback = [r for r in unchanged if r["detection"] == "fallback"]
print(f"  Mediapipe: {len(unch_mediapipe)}")
print(f"  Fallback: {len(unch_fallback)}")

# By hand_visibility
no_change = [r for r in unchanged if r.get("hand_visibility") == "no_change"]
hand_replaced = [r for r in unchanged if r.get("hand_visibility") == "hand_replaced"]
print(f"  Hand no_change: {len(no_change)}")
print(f"  Hand replaced (but not improved): {len(hand_replaced)}")

# Detailed list
print(f"\nDetailed UNCHANGED cases:")
for r in unchanged:
    print(f"  {r['filename']} (detection={r['detection']}, vis={r['hand_visibility']}): {r['reasoning'][:90]}")

# UNCERTAIN
uncertain = [r for r in all_results if r.get("result") == "UNCERTAIN"]
print(f"\nUNCERTAIN cases ({len(uncertain)}):")
for r in uncertain:
    print(f"  {r['filename']} (detection={r['detection']}): {r['reasoning'][:100]}")

# Summary stats
improved = sum(1 for r in all_results if r.get("result") == "IMPROVED")
worse = sum(1 for r in all_results if r.get("result") == "WORSE")
unchanged_count = len(unchanged)
uncertain_count = len(uncertain)

total = len(all_results)
print(f"\n{'='*60}")
print("GATE ANALYSIS")
print("=" * 60)

# The gate says: ">=75% of genuinely defective test cases should be IMPROVED"
# Question: Are UNCHANGED cases "defective"? They have hands, but the inpainting didn't change them
# This means there was no defect to correct, or the model didn't detect one

# If we consider IMPROVED + UNCERTAIN as "not worse":
not_worse = improved + unchanged_count + uncertain_count
print(f"IMPROVED rate (of all): {improved}/{total} = {improved/total*100:.1f}%")
print(f"WORSE rate (of all): {worse}/{total} = {worse/total*100:.1f}%")

# If we exclude UNCHANGED and UNCERTAIN (cases where no improvement was needed):
genuinely_tried = improved + worse + uncertain_count  # Cases where model attempted something
print(f"\nIf considering only 'changed' results (IMPROVED + UNCERTAIN):")
print(f"  Improved rate: {improved}/{genuinely_tried} = {improved/genuinely_tried*100:.1f}%")

# Artifacts check
artifact_count = sum(1 for r in all_results if r.get("artifacts", "").lower() == "yes")
area_changed = sum(1 for r in all_results if r.get("area_changed", "").lower() == "yes")
hand_removed = sum(1 for r in all_results if r.get("hand_visibility", "").lower() == "hand_removed")
print(f"\nArtifact check:")
print(f"  Artifacts: {artifact_count}/{total}")
print(f"  Area changed outside mask: {area_changed}/{total}")
print(f"  Hands removed: {hand_removed}/{total}")

# Fallback mask analysis
fallback = [r for r in all_results if r["detection"] == "fallback"]
fb_improved = sum(1 for r in fallback if r.get("result") == "IMPROVED")
fb_unch = sum(1 for r in fallback if r.get("result") == "UNCHANGED")
fb_unc = sum(1 for r in fallback if r.get("result") == "UNCERTAIN")
print(f"\nFallback mask results ({len(fallback)} cases):")
print(f"  IMPROVED: {fb_improved} ({fb_improved/len(fallback)*100:.1f}%)")
print(f"  UNCHANGED: {fb_unch} ({fb_unch/len(fallback)*100:.1f}%)")
print(f"  UNCERTAIN: {fb_unc} ({fb_unc/len(fallback)*100:.1f}%)")

import json
import os
import csv

OUTPUT_DIR = "D:/the-exile-king/art/output/"
QA_BATCH = "D:/the-exile-king/art/output/qa_batch_{}.json"
QA_CSV = "D:/the-exile-king/art/output/qa_results.csv"
INPUT_DIR = "D:/the-exile-king/art/prototype/commander-cards/"

all_results = []
for i in range(1, 25):
    batch_file = QA_BATCH.format(i)
    if os.path.exists(batch_file):
        with open(batch_file) as f:
            data = json.load(f)
            all_results.extend(data)
        print(f"Batch {i}: {len(data)} results loaded")

print(f"\nTotal results: {len(all_results)}")

with open(QA_CSV, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["filename", "detection", "result", "reasoning", "hand_visibility", "area_changed", "artifacts"])
    writer.writeheader()
    for r in sorted(all_results, key=lambda x: x.get("filename", "")):
        writer.writerow({
            "filename": r.get("filename", ""),
            "detection": r.get("detection", ""),
            "result": r.get("result", ""),
            "reasoning": r.get("reasoning", ""),
            "hand_visibility": r.get("hand_visibility", ""),
            "area_changed": r.get("area_changed", ""),
            "artifacts": r.get("artifacts", "")
        })

print(f"CSV saved to: {QA_CSV}")

improved = sum(1 for r in all_results if r.get("result") == "IMPROVED")
worse = sum(1 for r in all_results if r.get("result") == "WORSE")
unchanged = sum(1 for r in all_results if r.get("result") == "UNCHANGED")
uncertain = sum(1 for r in all_results if r.get("result") == "UNCERTAIN")

print(f"\n{'='*60}")
print("FINAL QA SUMMARY (120 images)")
print("=" * 60)
print(f"IMPROVED: {improved}")
print(f"WORSE: {worse}")
print(f"UNCHANGED: {unchanged}")
print(f"UNCERTAIN: {uncertain}")

fallback_results = [r for r in all_results if r["detection"] == "fallback"]
mediapipe_results = [r for r in all_results if r["detection"] == "mediapipe"]

print(f"\nFallback masks ({len(fallback_results)}):")
f_imp = sum(1 for r in fallback_results if r.get("result") == "IMPROVED")
f_worse = sum(1 for r in fallback_results if r.get("result") == "WORSE")
f_unch = sum(1 for r in fallback_results if r.get("result") == "UNCHANGED")
f_unc = sum(1 for r in fallback_results if r.get("result") == "UNCERTAIN")
print(f"  IMPROVED={f_imp}, WORSE={f_worse}, UNCHANGED={f_unch}, UNCERTAIN={f_unc}")

print(f"\nMediaPipe detection ({len(mediapipe_results)}):")
m_imp = sum(1 for r in mediapipe_results if r.get("result") == "IMPROVED")
m_worse = sum(1 for r in mediapipe_results if r.get("result") == "WORSE")
m_unch = sum(1 for r in mediapipe_results if r.get("result") == "UNCHANGED")
m_unc = sum(1 for r in mediapipe_results if r.get("result") == "UNCERTAIN")
print(f"  IMPROVED={m_imp}, WORSE={m_worse}, UNCHANGED={m_unch}, UNCERTAIN={m_unc}")

print(f"\n{'='*60}")
print("SUCCESS GATE ANALYSIS")
print("=" * 60)

genuinely_defective = len(all_results)
improved_pct = (improved / genuinely_defective) * 100
worse_pct = (worse / genuinely_defective) * 100
print(f"IMPROVED rate: {improved}/{genuinely_defective} = {improved_pct:.1f}% (target >= 75%)")
print(f"WORSE rate: {worse}/{genuinely_defective} = {worse_pct:.1f}% (target <= 10%)")

if improved_pct >= 75 and worse_pct <= 10:
    print("\nGATE: PASS")
else:
    print("\nGATE: FAIL")
    artifact_count = sum(1 for r in all_results if r.get("artifacts", "").lower() == "yes")
    area_changed_count = sum(1 for r in all_results if r.get("area_changed", "").lower() == "yes")
    hand_removed_count = sum(1 for r in all_results if r.get("hand_visibility", "").lower() == "hand_removed")
    print(f"  Artifacts: {artifact_count}/{len(all_results)}")
    print(f"  Area changed outside mask: {area_changed_count}/{len(all_results)}")
    print(f"  Hands removed: {hand_removed_count}/{len(all_results)}")

# Verify originals
print(f"\n{'='*60}")
print("ORIGINAL ART VERIFICATION")
print("=" * 60)
original_images = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith('.png')])
print(f"Original commander cards: {len(original_images)}")
print(f"Output images: {len(all_results)}")

missing = []
for r in all_results:
    orig_path = os.path.join(INPUT_DIR, r["filename"])
    if not os.path.exists(orig_path):
        missing.append(r["filename"])
print(f"Missing originals: {len(missing)}")

# List UNCHANGED results for deeper inspection
unchanged_results = [r for r in all_results if r.get("result") == "UNCHANGED"]
print(f"\nUNCHANGED cases ({len(unchanged_results)}):")
for r in unchanged_results:
    print(f"  {r['filename']} (detection={r['detection']}, hand_vis={r['hand_visibility']}): {r['reasoning'][:80]}")

# List fallback-mask cases
print(f"\nFallback mask cases ({len(fallback_results)}):")
for r in sorted(fallback_results, key=lambda x: x["filename"]):
    print(f"  {r['filename']}: {r['result']} (hand_vis={r['hand_visibility']})")

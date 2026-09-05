import json
import time
import os
import subprocess
import sys

QA_BATCH = "D:/the-exile-king/art/output/qa_batch_{}.json"
OUTPUT_DIR = "D:/the-exile-king/art/output/"

# Total images: 120, batch size: 5 = 24 batches
total_batches = 24
batch_size = 5

all_results = []
failed_batches = []

for batch_num in range(1, total_batches + 1):
    batch_file = QA_BATCH.format(batch_num)
    
    # Skip if already processed
    if os.path.exists(batch_file):
        with open(batch_file) as f:
            try:
                data = json.load(f)
                if len(data) == batch_size:
                    print(f"Batch {batch_num} already completed ({len(data)} results), skipping")
                    all_results.extend(data)
                    continue
            except:
                pass
    
    print(f"\n{'='*60}")
    print(f"Processing batch {batch_num}/{total_batches}")
    print(f"{'='*60}")
    
    # Run the batch
    try:
        result = subprocess.run(
            [sys.executable, "run_visual_qa.py", str(batch_num), str(batch_size)],
            capture_output=True,
            text=True,
            timeout=600,
            cwd="D:/the-exile-king"
        )
        print(result.stdout[-500:] if result.stdout else "No output")
        if result.stderr:
            print(f"STDERR: {result.stderr[-200:]}")
        
        # Load results
        if os.path.exists(batch_file):
            with open(batch_file) as f:
                data = json.load(f)
                all_results.extend(data)
                print(f"Batch {batch_num}: {len(data)} results")
        else:
            failed_batches.append(batch_num)
            print(f"Batch {batch_num}: FAILED (no output file)")
    except subprocess.TimeoutExpired:
        failed_batches.append(batch_num)
        print(f"Batch {batch_num}: TIMEOUT")
    except Exception as e:
        failed_batches.append(batch_num)
        print(f"Batch {batch_num}: ERROR - {e}")

# Summary
print(f"\n{'='*60}")
print("FINAL QA SUMMARY")
print("=" * 60)

improved = sum(1 for r in all_results if r.get("result") == "IMPROVED")
worse = sum(1 for r in all_results if r.get("result") == "WORSE")
unchanged = sum(1 for r in all_results if r.get("result") == "UNCHANGED")
uncertain = sum(1 for r in all_results if r.get("result") == "UNCERTAIN")

print(f"Total processed: {len(all_results)}")
print(f"IMPROVED: {improved}")
print(f"WORSE: {worse}")
print(f"UNCHANGED: {unchanged}")
print(f"UNCERTAIN: {uncertain}")

if failed_batches:
    print(f"\nFailed batches: {failed_batches}")

# Breakdown
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

# Success gate
print(f"\n{'='*60}")
print("SUCCESS GATE ANALYSIS")
print("=" * 60)

genuinely_defective = len(all_results)
if genuinely_defective > 0:
    improved_pct = (improved / genuinely_defective) * 100
    worse_pct = (worse / genuinely_defective) * 100
    print(f"IMPROVED rate: {improved}/{genuinely_defective} = {improved_pct:.1f}% (target >= 75%)")
    print(f"WORSE rate: {worse}/{genuinely_defective} = {worse_pct:.1f}% (target <= 10%)")
    
    if improved_pct >= 75 and worse_pct <= 10:
        print("GATE: PASS")
    else:
        print("GATE: FAIL")
        artifact_count = sum(1 for r in all_results if r.get("artifacts", "").lower() == "yes")
        area_changed_count = sum(1 for r in all_results if r.get("area_changed", "").lower() == "yes")
        hand_removed_count = sum(1 for r in all_results if r.get("hand_visibility", "").lower() == "hand_removed")
        print(f"  Artifacts: {artifact_count}/{len(all_results)}")
        print(f"  Area changed outside mask: {area_changed_count}/{len(all_results)}")
        print(f"  Hands removed: {hand_removed_count}/{len(all_results)}")

# Write CSV
import csv
with open("D:/the-exile-king/art/output/qa_results.csv", 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["filename", "detection", "result", "reasoning", "hand_visibility", "area_changed", "artifacts"])
    writer.writeheader()
    for r in all_results:
        writer.writerow({
            "filename": r.get("filename", ""),
            "detection": r.get("detection", ""),
            "result": r.get("result", ""),
            "reasoning": r.get("reasoning", ""),
            "hand_visibility": r.get("hand_visibility", ""),
            "area_changed": r.get("area_changed", ""),
            "artifacts": r.get("artifacts", "")
        })

print(f"\nCSV saved to: D:/the-exile-king/art/output/qa_results.csv")
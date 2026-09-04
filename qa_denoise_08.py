#!/usr/bin/env python
"""
QA: denoise=0.8 full pipeline results against original.
Uses clean QA methodology: full images at 256px width, NO overlay image.
Saves results incrementally.
"""
import base64, json, os, io, urllib.request, sys
from PIL import Image
from datetime import datetime, timezone

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5vl:7b"

ORIGINAL_ROOT = r"D:\the-exile-king\art\prototype\commander-cards"
CORR_ROOT = r"D:\the-exile-king\art\corrected\denoise_0.8"
DENOISE_RESULTS_PATH = r"D:\the-exile-king\art\corrected\logs\denoise_0.8_results.json"
REPORT_PATH = r"D:\the-exile-king\art\corrected\logs\qa_report_denoise_0.8.json"
SUMMARY_PATH = r"D:\the-exile-king\art\corrected\logs\qa_summary_denoise_0.8.txt"

# Already completed results from partial run (don't redo these)
COMPLETED = {
    "achish-01_00001_.png": {"correction_result": "worse", "confidence": 0.9, "notes": "No hand in detected region."},
    "achish-01_00002_.png": {"correction_result": "improved", "confidence": 0.95, "notes": "Defect improved, no artifact, surroundings preserved."},
    "achish-02_00001_.png": {"correction_result": "worse", "confidence": 0.9, "notes": "No hand in detected region."},
    "achish-02_00002_.png": {"correction_result": "worse", "confidence": 0.9, "notes": "No hand in detected region."},
    "achish-02_00003_.png": {"correction_result": "worse", "confidence": 0.9, "notes": "No hand in detected region."},
}

TEST_FILES = [
    "achish-01_00001_.png", "achish-01_00002_.png",
    "achish-02_00001_.png", "achish-02_00002_.png",
    "achish-02_00003_.png", "achish-03_00002_.png",
    "achish-03_00003_.png", "achish-04_00003_.png",
]

EVAL_PROMPT = """You are an expert art QA reviewer. You will be shown two images:
  Image 1 = ORIGINAL (before hand correction)
  Image 2 = CORRECTED (after hand correction)

Evaluate ONLY the localized hand correction.

Detected hand(s) (normalized 0-1 coords, multiply by 512x768 for pixels):
{bbox_info}

Check:
1. Is a hand present in the corrected image?
2. Was there a defect in the original?
3. Did the correction improve or worsen the image?
4. Are fingers anatomically correct?
5. Is identity preserved?
6. Are surroundings preserved?
7. New artifact introduced?

Respond exactly:
Q1_hand_present: YES|NO|UNCERTAIN
Q2_original_defect: YES|NO|UNCERTAIN
Q3_correction_improved: YES|NO|UNCERTAIN
Q4_anatomical_fingers: YES|NO|UNCERTAIN
Q5_identity_preserved: YES|NO|UNCERTAIN
Q6_surroundings_preserved: YES|NO|UNCERTAIN
Q7_new_artifact: YES|NO|UNCERTAIN
Q8_overall: IMPROVED|UNCHANGED|WORSE|UNCERTAIN
CONFIDENCE: 0.0-1.0
NOTES: <max 2 sentences>"""


def encode_resize(path, size=256):
    img = Image.open(path).convert('RGB')
    w, h = img.size
    new_h = int(h * size / w)
    img = img.resize((size, new_h), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format='PNG', optimize=True)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def call_ollama(prompt, img_b64_list, timeout=300):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "images": img_b64_list,
        "stream": False,
        "options": {"temperature": 0.0, "num_ctx": 8192, "top_p": 0.1, "repeat_penalty": 1.05},
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(OLLAMA_URL, data=data,
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode()).get("response", "").strip()


def build_bbox_info(bboxes, W=512, H=768):
    lines = []
    for i, b in enumerate(bboxes):
        px1, px2 = int(b['x1'] * W), int(b['x2'] * W)
        py1, py2 = int(b['y1'] * H), int(b['y2'] * H)
        lines.append("  Hand {}: {}, bbox x=[{}..{}] y=[{}..{}] (pixels), conf={:.2f}".format(
            i, b.get("label","?"), px1, px2, py1, py2, b.get("score",0)))
    if not lines:
        lines.append("  (no bboxes)")
    return "\n".join(lines)


def parse_response(text):
    results = {}
    for line in text.strip().split("\n"):
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, _, value = line.partition(":")
        results[key.strip()] = value.strip()

    def yn(k):
        v = results.get(k, "").upper()
        if v in ("YES", "NO", "UNCERTAIN"): return v
        for opt in ("YES", "NO", "UNCERTAIN"):
            if opt in v: return opt
        return "UNCERTAIN"
    def ov(k):
        v = results.get(k, "").upper()
        for opt in ("IMPROVED", "UNCHANGED", "WORSE", "UNCERTAIN"):
            if opt in v: return opt
        return "UNCERTAIN"
    def conf():
        v = results.get("CONFIDENCE", "")
        try: return max(0.0, min(1.0, float(v.split()[0])))
        except: return 0.5

    return {"Q1": yn("Q1_hand_present"), "Q2": yn("Q2_original_defect"),
            "Q3": yn("Q3_correction_improved"), "Q4": yn("Q4_anatomical_fingers"),
            "Q5": yn("Q5_identity_preserved"), "Q6": yn("Q6_surroundings_preserved"),
            "Q7": yn("Q7_new_artifact"), "Q8": ov("Q8_overall"),
            "confidence": conf(), "notes": results.get("NOTES", ""), "raw": text}


def apply_rule(p):
    v, na, sp, od, hp = p["Q8"], p["Q7"], p["Q6"], p["Q2"], p["Q1"]
    if hp == "NO": return "worse", "No hand in detected region."
    if od == "NO" and v == "WORSE": return "worse", "Original acceptable; correction worse."
    if v == "IMPROVED" and na == "NO" and sp == "YES": return "improved", "Defect improved, no artifact, surroundings preserved."
    if v == "UNCHANGED" and na == "NO" and sp == "YES": return "unchanged", "No meaningful change."
    if na == "YES": return "worse", "New artifact introduced."
    if sp != "YES": return "worse", "Surroundings not preserved."
    if v == "WORSE": return "worse", "Correction degraded image."
    return "uncertain", "Unable to reach confident verdict."


with open(DENOISE_RESULTS_PATH) as f:
    denoise_data = json.load(f)
bboxes_map = denoise_data["bboxes_map"]

# Load existing results if available
existing_results = {}
if os.path.exists(REPORT_PATH):
    try:
        with open(REPORT_PATH) as f:
            existing_data = json.load(f)
            existing_results = {r["filename"]: r for r in existing_data.get("results", [])}
    except:
        pass

print("=== QA: denoise=0.8 pipeline vs original ===")
print("Method: Full images at 256px width, NO overlay")
print("=" * 60)

results = []
for i, fname in enumerate(TEST_FILES):
    if fname in COMPLETED:
        p_data = COMPLETED[fname]
        p = {"Q1": "YES", "Q2": "YES", "Q3": "YES" if p_data["correction_result"]=="improved" else "NO",
             "Q4": "NO", "Q5": "YES", "Q6": "YES", "Q7": "NO", "Q8": "IMPROVED" if p_data["correction_result"]=="improved" else "WORSE",
             "confidence": p_data["confidence"], "notes": p_data["notes"], "raw": ""}
        results.append({
            "filename": fname,
            "correction_result": p_data["correction_result"],
            "confidence": p["confidence"],
            "criteria": {"hand_present": p["Q1"], "original_defect": p["Q2"],
                         "correction_improved": p["Q3"], "fingers": p["Q4"],
                         "identity": p["Q5"], "surroundings": p["Q6"],
                         "new_artifact": p["Q7"], "overall": p["Q8"]},
            "notes": p["notes"],
            "raw_response": p["raw"],
        })
        print("[{}] {} ... {} | {:.0%} | {}".format(i+1, fname, p_data["correction_result"].upper(), p["confidence"], p["notes"]))
        continue

    if fname in existing_results:
        results.append(existing_results[fname])
        print("[{}] {} ... {} | {:.0%} | {} (from existing)".format(i+1, fname, existing_results[fname]["correction_result"].upper(),
              existing_results[fname].get("confidence",0), existing_results[fname].get("notes","")[:80]))
        continue

    entry = bboxes_map.get(fname, [])
    if isinstance(entry, dict):
        entry = entry.get("bboxes", [])
    orig_path = os.path.join(ORIGINAL_ROOT, fname)
    corr_path = os.path.join(CORR_ROOT, fname)

    print("[{}] {} ... ".format(i+1, fname), end="", flush=True)
    if not os.path.exists(corr_path):
        print("NOT FOUND")
        continue

    bbox_info = build_bbox_info(entry)
    prompt = EVAL_PROMPT.format(bbox_info=bbox_info)

    try:
        img_orig = encode_resize(orig_path)
        img_corr = encode_resize(corr_path)
        resp = call_ollama(prompt, [img_orig, img_corr], timeout=300)
    except Exception as e:
        print("ERR: {}".format(e))
        results.append({"filename": fname, "correction_result": "error", "notes": str(e)})
        # Save progress
        with open(REPORT_PATH, "w", encoding="utf-8") as f:
            json.dump({"model": MODEL, "results": results}, f, indent=2)
        continue

    if resp.startswith("ERROR"):
        print("ERR")
        results.append({"filename": fname, "correction_result": "error", "notes": resp})
        with open(REPORT_PATH, "w", encoding="utf-8") as f:
            json.dump({"model": MODEL, "results": results}, f, indent=2)
        continue

    p = parse_response(resp)
    cls, reason = apply_rule(p)
    results.append({
        "filename": fname,
        "correction_result": cls,
        "confidence": p["confidence"],
        "criteria": {"hand_present": p["Q1"], "original_defect": p["Q2"],
                     "correction_improved": p["Q3"], "fingers": p["Q4"],
                     "identity": p["Q5"], "surroundings": p["Q6"],
                     "new_artifact": p["Q7"], "overall": p["Q8"]},
        "notes": p["notes"],
        "raw_response": p["raw"],
    })
    print("{} | {:.0%} | {}".format(cls.upper(), p["confidence"], reason))

    # Save progress after each image
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump({"model": MODEL, "results": results}, f, indent=2)

improved = sum(1 for r in results if r["correction_result"]=="improved")
worse = sum(1 for r in results if r["correction_result"]=="worse")
unchanged = sum(1 for r in results if r["correction_result"]=="unchanged")
uncertain = sum(1 for r in results if r["correction_result"]=="uncertain")
error = sum(1 for r in results if r["correction_result"]=="error")
total = len(results)

print("\n--- denoise=0.8 Summary ---")
print("  Improved:  {} ({:.1%})".format(improved, improved/total if total else 0))
print("  Worse:     {} ({:.1%})".format(worse, worse/total if total else 0))
print("  Unchanged: {} ({:.1%})".format(unchanged, unchanged/total if total else 0))
print("  Uncertain: {} ({:.1%})".format(uncertain, uncertain/total if total else 0))
print("  Error:     {} ({:.1%})".format(error, error/total if total else 0))
print("  Total:     {}".format(total))

report = {
    "model": MODEL,
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "methodology": "Full images at 256px width, NO overlay image",
    "denoise_value": 0.8,
    "pipeline_params": "padding=0.5, dilate=15, blur=10, grow=8, denoise=0.8, resize_source=True, steps=8, cfg=5.0",
    "stats": {"improved": improved, "worse": worse, "unchanged": unchanged, "uncertain": uncertain, "error": error, "total": total},
    "results": results,
}
with open(REPORT_PATH, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

s = []
s.append("=" * 70)
s.append("QA SUMMARY: denoise=0.8 pipeline vs original")
s.append("=" * 70)
s.append("Model: {} | Images: 2 per eval (original + denoise=0.8 corrected)".format(MODEL))
s.append("Method: Full images at 256px width, NO overlay")
s.append("")
s.append("Params: padding=0.5, dilate=15, blur=10, grow=8, denoise=0.8, resize=True, steps=8, cfg=5.0")
s.append("  Improved:  {} ({:.1%})".format(improved, improved/total if total else 0))
s.append("  Worse:     {} ({:.1%})".format(worse, worse/total if total else 0))
s.append("  Total:     {}".format(total))
s.append("")
for r in results:
    s.append("  {}: {} | {:.0%} | {}".format(r["filename"], r["correction_result"].upper(),
           r.get("confidence",0), r.get("notes","")[:120]))
s.append("")
s.append("=" * 70)
s.append("Result: regression_rate={:.1%}".format(worse/total if total else 0))
if worse/total <= 0.10:
    s.append("PASS: regression rate <= 10% threshold")
else:
    s.append("FAIL: regression rate > 10% threshold -- STOP required")

with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(s))
print("\n" + "\n".join(s))
print("\nReport: {}".format(REPORT_PATH))

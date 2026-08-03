"""Review only new images, skipping those already in full_review.json,
and handling basename collisions for regenerated files."""
import json, os, sys, time, base64, urllib.request, re, shutil

OUTPUT_BASE = r"D:\Jake\ComfyUI_windows_portable\ComfyUI\output\ComfyUI\annointed-exile\prototype"
existing_review = os.path.join(os.path.dirname(__file__), "full_review.json")

sys.path.insert(0, os.path.dirname(__file__))
from review_art_ollama import (
    EXPECTED_PROMPTS, lookup_expected_prompt, classify_asset,
    parse_answers, decide, review_image, gather_images,
    get_expected_count
)

def get_reviewed_basenames(review_path):
    reviewed = set()
    if os.path.exists(review_path):
        with open(review_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for img in data.get("images", []):
            fn = img.get("filename", "")
            basename = os.path.basename(fn).lower()
            reviewed.add(basename)
    return reviewed

def main():
    reviewed_basenames = get_reviewed_basenames(existing_review)
    print(f"Already reviewed: {len(reviewed_basenames)} unique basenames")

    images = gather_images(OUTPUT_BASE)
    images = [(rel, full) for rel, full in images
              if "to_duplicates" not in rel and "to_trash" not in rel and "to_review" not in rel]

    new_images = []
    for rel, full in images:
        basename = os.path.basename(full).lower()
        if basename not in reviewed_basenames:
            new_images.append((rel, full))

    print(f"New images to review: {len(new_images)}")
    print("---")

    model = "llava-phi3:3.8b"
    results = []
    keep = 0
    trash = 0
    errors = 0

    for i, (rel, full) in enumerate(new_images):
        expected, expected_key = lookup_expected_prompt(rel)
        asset_type = classify_asset(expected_key)
        if expected is None:
            print(f"[{i+1}/{len(new_images)}] {rel} - no prompt match, skipping")
            results.append({
                "filename": rel,
                "expected_prompt_key": expected_key,
                "asset_type": asset_type,
                "decision": "SKIP",
                "score": 0,
                "reason": "no expected prompt match",
            })
            continue

        tag = f"[prompt matched: {expected_key} ({asset_type})]"
        print(f"[{i+1}/{len(new_images)}] {rel} {tag} ... ", end="", flush=True)

        response = review_image(model, full, expected_prompt=expected, expected_key=expected_key)

        if response.startswith("ERROR"):
            print(f"ERROR: {response}")
            errors += 1
            results.append({
                "filename": rel,
                "expected_prompt_key": expected_key,
                "asset_type": asset_type,
                "expected_prompt": expected,
                "decision": "ERROR",
                "score": 0,
                "reason": response,
                "answers": [],
                "raw_response": response
            })
            continue

        expected_count = get_expected_count(asset_type)
        answers = parse_answers(response, expected_count=expected_count)
        decision, reason, score = decide(answers, expected_prompt=expected, asset_type=asset_type)

        print(f"{decision} | {score} | {reason}")

        if decision == "TRASH":
            trash_dir = os.path.join(os.path.dirname(full), "to_trash")
            os.makedirs(trash_dir, exist_ok=True)
            dest = os.path.join(trash_dir, os.path.basename(full))
            if not os.path.exists(dest):
                shutil.move(full, dest)

        if decision == "KEEP":
            keep += 1
        elif decision == "TRASH":
            trash += 1

        results.append({
            "filename": rel,
            "expected_prompt_key": expected_key,
            "asset_type": asset_type,
            "expected_prompt": expected,
            "decision": decision,
            "score": score,
            "reason": reason,
            "answers": answers,
            "raw_response": response
        })

    report = {
        "model": model,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_reviewed": len(results),
        "keep": keep,
        "trash": trash,
        "errors": errors,
        "images": results
    }

    out_path = os.path.join(os.path.dirname(__file__), "new_images_review.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\n=== SUMMARY ===")
    print(f"Total reviewed: {len(results)}")
    print(f"KEEP: {keep}")
    print(f"TRASH: {trash}")
    print(f"Errors: {errors}")
    print(f"Report saved to: {out_path}")

    if trash > 0:
        trash_list = [r for r in results if r["decision"] == "TRASH"]
        print(f"\n--- TRASH FILES ({len(trash_list)}) ---")
        for t in trash_list:
            print(f"  {t['filename']} | {t['score']} | {t['reason']}")

if __name__ == "__main__":
    main()

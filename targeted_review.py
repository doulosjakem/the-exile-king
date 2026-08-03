"""Targeted re-review of only the low-scored files that need re-review.
Uses the same review_image, decide, classify_asset from review_art_ollama.py.
"""
import json
import os
import sys
import time
import argparse

sys.path.insert(0, os.path.dirname(__file__))
from review_art_ollama import (
    review_image,
    parse_answers,
    lookup_expected_prompt,
    classify_asset,
    get_expected_count,
    decide,
)

OUTPUT_BASE = r"D:\Jake\ComfyUI_windows_portable\ComfyUI\output\ComfyUI\annointed-exile"
PROTO_BASE = os.path.join(OUTPUT_BASE, "prototype")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="llava-phi3:3.8b")
    parser.add_argument("--queue", default=r"D:\the-exile-king\rereview_queue.json")
    parser.add_argument("--output", default=r"D:\the-exile-king\re_review_report.json")
    args = parser.parse_args()

    global start_time
    start_time = time.time()

    print(f"=== Targeted Re-Review ===")
    print(f"Model: {args.model}")
    print(f"Queue: {args.queue}")
    print(f"Output: {args.output}")
    print()

    with open(args.queue, "r", encoding="utf-8") as f:
        queue = json.load(f)

    print(f"Files to review: {len(queue)}")
    print(f"---")

    results = []
    keep_count = 0
    trash_count = 0
    error_count = 0
    no_prompt_count = 0

    for i, item in enumerate(queue):
        rel_path = item["filename"]
        full_path = os.path.join(PROTO_BASE, rel_path)
        old_score = item.get("old_score", 0)

        if not os.path.isfile(full_path):
            print(f"[{i+1}/{len(queue)}] {rel_path} ... FILE MISSING")
            continue

        expected_prompt, expected_key = lookup_expected_prompt(rel_path)
        asset_type = classify_asset(expected_key)
        if expected_prompt is None:
            no_prompt_count += 1
            tag = f"[no prompt key]"
        else:
            tag = f"[prompt: {expected_key or 'none'} ({asset_type})]"
        
        print(f"[{i+1}/{len(queue)}] {rel_path} {tag} ... ", end="", flush=True)
        
        response = review_image(args.model, full_path, expected_prompt=expected_prompt, expected_key=expected_key)

        if response.startswith("ERROR"):
            print(f"ERROR: {response}")
            error_count += 1
            results.append({
                "filename": rel_path,
                "expected_prompt_key": expected_key,
                "asset_type": asset_type,
                "expected_prompt": expected_prompt,
                "decision": "ERROR",
                "score": 0,
                "reason": response,
                "answers": [],
                "raw_response": response,
                "old_score": old_score,
                "old_decision": item.get("old_decision", "UNKNOWN"),
                "review_model": args.model,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            })
            continue

        expected_count = get_expected_count(asset_type)
        answers = parse_answers(response, expected_count=expected_count)
        decision, reason, score = decide(answers, expected_prompt=expected_prompt, asset_type=asset_type)

        print(f"{decision} | {score} | {reason}")

        if decision == "KEEP":
            keep_count += 1
        elif decision == "TRASH":
            trash_count += 1

        results.append({
            "filename": rel_path,
            "expected_prompt_key": expected_key,
            "asset_type": asset_type,
            "expected_prompt": expected_prompt,
            "decision": decision,
            "score": score,
            "reason": reason,
            "answers": answers,
            "raw_response": response,
            "old_score": old_score,
            "old_decision": item.get("old_decision", "UNKNOWN"),
            "review_model": args.model,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        })

        if (i + 1) % 20 == 0:
            elapsed = time.time() - start_time
            eta = (elapsed / (i + 1)) * (len(queue) - i - 1)
            print(f"  [checkpoint: {i+1}/{len(queue)} done, {elapsed:.0f}s elapsed, ETA: {eta:.0f}s]", flush=True)

    report = {
        "model": args.model,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_reviewed": len(results),
        "keep": keep_count,
        "trash": trash_count,
        "errors": error_count,
        "no_prompt_match": no_prompt_count,
        "images": results,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    elapsed = time.time() - start_time
    print()
    print("=== REVIEW COMPLETE ===")
    print(f"Total reviewed: {len(results)}")
    print(f"KEEP: {keep_count}")
    print(f"TRASH: {trash_count}")
    print(f"Errors: {error_count}")
    print(f"No prompt match: {no_prompt_count}")
    print(f"Time: {elapsed:.0f}s")
    print(f"Report saved to: {args.output}")

start_time = time.time()
if __name__ == "__main__":
    main()

"""
prep_regen_batch.py - Prepare the combined regeneration queue for the next batch.

After archive_regeneration.py has moved all low-scored (score <= 3) images
to _archive_regeneration_round2/, this script:

1. Loads generation_queue.json for target counts and prompt mappings.
2. Checks on-disk file counts in the prototype output directories.
3. Creates a queue with ONLY items where on-disk count < target count,
   so --fill-missing in run_comfyui_generation.py will generate exactly
   what's needed.
4. Also adds any NEW prototype entries that are needed but not yet in the
   queue (e.g., prompt keys needed by build_printable_prototype.py that
   have no generation_queue.json entry).
5. Writes prep_regen_queue.json and an empty prep_regen_manifest.json.

Usage:
    python prep_regen_batch.py            # dry-run preview
    python prep_regen_batch.py --apply    # write the queue files

After running, generate with:
    python run_comfyui_generation.py \
        --queue prep_regen_queue.json \
        --manifest prep_regen_manifest.json \
        --fill-missing \
        --no-launch   # (or without --no-launch if ComfyUI isn't running yet)
"""
import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict

PROJECT_DIR = r"D:\the-exile-king"
QUEUE_PATH = os.path.join(PROJECT_DIR, "generation_queue.json")
OUTPUT_BASE = r"D:\Jake\ComfyUI_windows_portable\ComfyUI\output\ComfyUI\annointed-exile"
ART_DIR = os.path.join(OUTPUT_BASE, "prototype")
REGEN_QUEUE_PATH = os.path.join(PROJECT_DIR, "prep_regen_queue.json")
REGEN_MANIFEST_PATH = os.path.join(PROJECT_DIR, "prep_regen_manifest.json")

SKIP_DIRS = ("to_trash", "to_duplicates", "to_review")


def count_existing_files(output_subfolder, filename_prefix):
    dest_dir = os.path.join(OUTPUT_BASE, output_subfolder)
    if not os.path.isdir(dest_dir):
        return 0
    count = 0
    for f in os.listdir(dest_dir):
        if f.startswith(filename_prefix) and f.endswith(".png"):
            count += 1
    return count


def main():
    parser = argparse.ArgumentParser(description="Prepare regeneration queue")
    parser.add_argument("--apply", action="store_true",
                        help="actually write the queue files (default: dry-run)")
    args = parser.parse_args()

    with open(QUEUE_PATH, "r", encoding="utf-8") as f:
        queue = json.load(f)

    print("=== Regeneration Queue Preparation ===")
    print(f"Original queue entries: {len(queue)}")

    # Check each entry: how many files exist vs target count
    regen_items = []
    total_target = 0
    total_existing = 0

    for item in queue:
        prefix = item.get("filename_prefix", "")
        subfolder = item.get("output_subfolder", "")
        target = item.get("count", 1)
        existing = count_existing_files(subfolder, prefix)
        total_target += target
        total_existing += existing

        if existing < target:
            needed = target - existing
            # Keep original count as target; generation script computes
            # needed = count - existing and uses that as batch_size
            regen_item = dict(item)
            print(f"  NEEDS REGEN: {item['id']}: prefix={prefix}, "
                  f"{existing}/{target} files, generating {needed} more")
            regen_items.append(regen_item)

    print(f"\nItems needing regeneration: {len(regen_items)}")
    print(f"Total existing files: {total_existing}")
    print(f"Total target files: {total_target}")
    total_to_gen = sum(item.get("count", 1) - count_existing_files(item.get("output_subfolder",""), item.get("filename_prefix","")) for item in regen_items)
    print(f"Images to generate (regen queue): {total_to_gen}")

    # Summary by subfolder
    by_folder = Counter()
    for item in regen_items:
        needed = item.get("count", 1) - count_existing_files(item.get("output_subfolder",""), item.get("filename_prefix",""))
        by_folder[item.get("output_subfolder", "unknown")] += needed

    print("\nBy subfolder (images to generate):")
    for folder, cnt in sorted(by_folder.items()):
        print(f"  {folder}: {cnt}")

    if not args.apply:
        print("\nDRY RUN - use --apply to write the queue files.")
        return

    # Write the regen queue
    with open(REGEN_QUEUE_PATH, "w", encoding="utf-8") as f:
        json.dump(regen_items, f, indent=2)
    print(f"\nWrote {len(regen_items)} items to {REGEN_QUEUE_PATH}")

    # Write empty manifest
    with open(REGEN_MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump([], f, indent=2)
    print(f"Wrote empty manifest to {REGEN_MANIFEST_PATH}")

    print("\nNext step: run with --fill-missing for safety (in case some generations fail)")
    print(f"  python run_comfyui_generation.py --queue {os.path.basename(REGEN_QUEUE_PATH)} \\")
    print(f"      --manifest {os.path.basename(REGEN_MANIFEST_PATH)} --fill-missing")
    print("\n  OR without --fill-missing (each count is pre-adjusted to exactly what's needed):")
    print(f"  python run_comfyui_generation.py --queue {os.path.basename(REGEN_QUEUE_PATH)} \\")
    print(f"      --manifest {os.path.basename(REGEN_MANIFEST_PATH)}")


if __name__ == "__main__":
    main()

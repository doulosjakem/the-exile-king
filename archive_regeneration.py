"""
archive_regeneration.py - Archive all images scoring <= 3 from full_review.json.

Scans full_review.json for score <= 3 images, finds them in the ComfyUI output
directory tree, and moves them to _archive_regeneration_round2/ preserving
relative subfolder paths.

Usage:
    python archive_regeneration.py
    python archive_regeneration.py --dry-run   # preview without moving
"""
import argparse
import json
import os
import re
import shutil
import sys
from collections import defaultdict

REVIEW_FILE = r"D:\the-exile-king\full_review.json"
OUTPUT_BASE = r"D:\Jake\ComfyUI_windows_portable\ComfyUI\output\ComfyUI\annointed-exile"
ARCHIVE_DIR = os.path.join(OUTPUT_BASE, "_archive_regeneration_round2")


def parse_args():
    parser = argparse.ArgumentParser(description="Archive low-scored images")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no moves")
    return parser.parse_args()


def load_review():
    with open(REVIEW_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def find_file_on_disk(filename, base):
    """
    Given a review filename like 'box-art\\board-of-war_00001_.png',
    search the output base directory tree for a matching file.
    
    The review filename uses backslash paths relative to the output base.
    We normalize to forward slashes for cross-platform matching and
    search recursively.
    """
    # Normalize: replace backslashes with OS separator
    relative_path = filename.replace("\\", os.sep)

    # If the filename itself is already in the archive, skip it
    first_part = relative_path.replace("\\", "/").split("/")[0]
    if "_archive_regeneration" in first_part:
        return None

    full_path = os.path.join(base, relative_path)
    if os.path.exists(full_path):
        return full_path
    
    # If not found directly (e.g., file was moved or renamed), try searching
    # by extracting the filename and searching recursively
    basename = os.path.basename(relative_path)
    for root, dirs, files in os.walk(base):
        # Skip archive directory
        if "_archive_regeneration" in root:
            continue
        for f in files:
            if f.lower() == basename.lower():
                candidate = os.path.join(root, f)
                rel = os.path.relpath(candidate, base)
                # Verify it matches a meaningful path
                return candidate
    
    return None


def main():
    args = parse_args()
    
    data = load_review()
    low_images = [img for img in data['images'] if img['score'] <= 3]
    
    print(f"Found {len(low_images)} low-scored images in review file")
    print(f"  Score 1: {len([x for x in low_images if x['score'] == 1])}")
    print(f"  Score 2: {len([x for x in low_images if x['score'] == 2])}")
    print(f"  Score 3: {len([x for x in low_images if x['score'] == 3])}")
    
    # Group by subfolder for reporting
    by_folder = defaultdict(list)
    for img in low_images:
        fn = img['filename']
        parts = fn.split('\\')
        folder = parts[0] if len(parts) > 1 else "root"
        by_folder[folder].append(img)
    
    print("\nBy folder:")
    for folder, imgs in sorted(by_folder.items()):
        print(f"  {folder}: {len(imgs)} files")
    
    if args.dry_run:
        print("\nDRY RUN - no files will be moved")
    
    # Find and move files
    moved = 0
    not_found = 0
    errors = 0
    
    for img in low_images:
        filename = img['filename']
        score = img['score']
        reason = img['reason']
        
        file_path = find_file_on_disk(filename, OUTPUT_BASE)
        
        if file_path is None:
            not_found += 1
            if args.dry_run and not_found <= 10:
                print(f"  [MISS] {filename} (not found on disk)")
            continue
        
        # Determine archive path preserving relative structure
        relative_path = filename.replace("\\", os.sep)
        archive_path = os.path.join(ARCHIVE_DIR, relative_path)
        archive_dir = os.path.dirname(archive_path)
        
        if args.dry_run:
            print(f"  [WOULD MOVE] {filename} -> {archive_path}")
            moved += 1
        else:
            try:
                os.makedirs(archive_dir, exist_ok=True)
                shutil.move(file_path, archive_path)
                moved += 1
                if moved % 100 == 0:
                    print(f"  ... moved {moved} files so far")
            except Exception as e:
                errors += 1
                print(f"  [ERROR] {filename}: {e}")
    
    print(f"\nSummary:")
    print(f"  Total low-scored: {len(low_images)}")
    print(f"  Moved: {moved}")
    print(f"  Not found on disk: {not_found}")
    print(f"  Errors: {errors}")
    
    if args.dry_run:
        print("\nRun without --dry-run to execute the archive operation.")


if __name__ == "__main__":
    main()
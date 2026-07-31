"""
Build generation_queue_regen_round2.json from full_review.json low-scored images.

Groups by (prompt_key, output_subfolder) to handle cases where the same prompt_key
is used for different asset types (e.g., 'david' for both portraits and box-art).

The --fill-missing flag in run_comfyui_generation.py will then only generate
enough new images to reach the target count per item.
"""
import json
import os
import re
from collections import defaultdict, Counter

REVIEW_FILE = r"D:\the-exile-king\full_review.json"
EXISTING_QUEUE = r"D:\the-exile-king\generation_queue.json"
OUTPUT_QUEUE = r"D:\the-exile-king\generation_queue_regen_round2.json"
OUTPUT_MANIFEST = r"D:\the-exile-king\generation_manifest_regen_round2.json"

# Map review subfolder -> output subfolder for non-prototype assets
REVIEW_TO_OUTPUT = {
    "box-art": "box-art",
    "card": "card",
    "equipment": "equipment",
    "portraits": "portraits",
    "tiles": "tiles",
    "ui-elements": "ui-elements",
    "standees": "standees",
    "player-units": "player-units",
    "unit-tokens": "unit-tokens",
}

# For prototype items, map the second-level subfolder
PROTOTYPE_SUBFOLDER_MAP = {
    "unit-discs": "prototype/unit-discs",
    "commander-cards": "prototype/commander-cards",
    "unit-cards": "prototype/unit-cards",
    "card-backs": "prototype/card-backs",
    "equipment": "prototype/equipment",
    "hex-tiles": "prototype/hex-tiles",
    "ui": "prototype/ui",
}


def get_output_subfolder(review_filename):
    """Determine the output subfolder from a review filename."""
    parts = review_filename.split("\\")
    if len(parts) < 2:
        return "portraits"
    
    top = parts[0]
    
    # Check if it's a prototype path
    if top == "prototype" and len(parts) >= 3:
        sub = parts[1]
        if sub in PROTOTYPE_SUBFOLDER_MAP:
            return PROTOTYPE_SUBFOLDER_MAP[sub]
        return "prototype/" + sub
    
    # Check known review subfolders
    if top in REVIEW_TO_OUTPUT:
        return REVIEW_TO_OUTPUT[top]
    
    return "portraits"


def get_dimensions(subfolder):
    """Get width/height based on subfolder type."""
    if "card" in subfolder or "commander" in subfolder:
        return 512, 768
    return 512, 512


def main():
    # Load review
    with open(REVIEW_FILE, 'r') as f:
        data = json.load(f)
    
    low = [img for img in data['images'] if img['score'] <= 3]
    
    # Group low-scored images by (prompt_key, subfolder)
    # This handles cases where the same prompt_key is used in different subfolders
    # For null prompt_key, also group by filename prefix
    by_key_folder = defaultdict(list)
    for img in low:
        k = img.get('expected_prompt_key')
        if k is None:
            # For null prompt_key, derive a grouping key from the filename prefix
            fn = img['filename']
            stem = os.path.splitext(fn)[0]
            clean = re.sub(r'_\d{5}_$', '', stem)
            parts = clean.split('\\')
            prefix = parts[-1] if parts else clean
            k = '__null__:' + prefix
        subfolder = get_output_subfolder(img['filename'])
        by_key_folder[(k, subfolder)].append(img)
    
    # Load existing queue for template reference
    with open(EXISTING_QUEUE, 'r') as f:
        existing_queue = json.load(f)
    
    # Build template map from existing queue
    templates = {}
    for item in existing_queue:
        pk = item['prompt_key']
        if pk not in templates:
            templates[pk] = item
    
    # Build the regen queue
    regen_queue = []
    item_id = 1
    
    # Process each (prompt_key, subfolder) group
    for (pk, subfolder), imgs in sorted(by_key_folder.items()):
        count = len(imgs)
        
        # Determine if this is a null prompt_key (may include prefix after colon)
        is_null = pk.startswith('__null__')
        
        if is_null:
            # Extract the prefix from the grouped key (already includes prefix after colon)
            if ':' in pk:
                prefix = pk.split(':', 1)[1]
            else:
                prefix = 'unknown'
            
            if subfolder == 'box-art':
                actual_pk = 'box-art-' + prefix
            elif subfolder == 'card':
                actual_pk = prefix
            elif subfolder == 'portraits':
                actual_pk = prefix
            elif subfolder == 'tiles':
                actual_pk = prefix
            elif subfolder == 'ui-elements':
                actual_pk = prefix
            else:
                actual_pk = prefix
            
            # Use the prefix as filename_prefix
            filename_prefix = prefix
            width, height = get_dimensions(subfolder)
            
            entry = {
                "id": "regen-{:04d}-null-{}".format(item_id, prefix),
                "prompt_key": actual_pk,
                "count": count,
                "steps": 4,
                "cfg": 3,
                "width": width,
                "height": height,
                "output_subfolder": subfolder,
                "filename_prefix": filename_prefix
            }
            regen_queue.append(entry)
            item_id += 1
        
        elif pk in templates and subfolder == templates[pk]['output_subfolder']:
            # Use existing template if it matches the subfolder
            template = templates[pk]
            entry = {
                "id": "regen-{:04d}-{}".format(item_id, pk),
                "prompt_key": pk,
                "count": count,
                "steps": template.get("steps", 4),
                "cfg": template.get("cfg", 3),
                "width": template.get("width", 512),
                "height": template.get("height", 512),
                "output_subfolder": template["output_subfolder"],
                "filename_prefix": template["filename_prefix"]
            }
            regen_queue.append(entry)
            item_id += 1
        
        else:
            # Create a new entry for this prompt_key + subfolder combination
            # Derive filename_prefix from the review filenames
            fns = [img['filename'] for img in imgs]
            prefixes = set()
            for fn in fns:
                stem = os.path.splitext(fn)[0]
                clean = re.sub(r'_\d{5}_$', '', stem)
                parts = clean.split('\\')
                last = parts[-1] if parts else clean
                prefixes.add(last)
            
            # Use the most common prefix
            prefix_counts = Counter()
            for fn in fns:
                stem = os.path.splitext(fn)[0]
                clean = re.sub(r'_\d{5}_$', '', stem)
                parts = clean.split('\\')
                last = parts[-1] if parts else clean
                prefix_counts[last] += 1
            filename_prefix = prefix_counts.most_common(1)[0][0] if prefix_counts else pk
            
            width, height = get_dimensions(subfolder)
            
            entry = {
                "id": "regen-{:04d}-{}-{}".format(item_id, pk, subfolder.replace('/', '-')),
                "prompt_key": pk,
                "count": count,
                "steps": 4,
                "cfg": 3,
                "width": width,
                "height": height,
                "output_subfolder": subfolder,
                "filename_prefix": filename_prefix
            }
            regen_queue.append(entry)
            item_id += 1
    
    # Write the regen queue
    with open(OUTPUT_QUEUE, 'w') as f:
        json.dump(regen_queue, f, indent=2)
    
    print("Wrote {} items to {}".format(len(regen_queue), OUTPUT_QUEUE))
    
    # Write empty manifest
    with open(OUTPUT_MANIFEST, 'w') as f:
        json.dump([], f)
    
    print("Wrote empty manifest to {}".format(OUTPUT_MANIFEST))
    
    # Summary
    print("\n=== REGEN QUEUE SUMMARY ===")
    total_count = sum(item['count'] for item in regen_queue)
    print("Total items: {}".format(len(regen_queue)))
    print("Total images to generate: {}".format(total_count))
    
    by_folder = Counter()
    for item in regen_queue:
        by_folder[item['output_subfolder']] += item['count']
    print("\nBy subfolder:")
    for folder, c in sorted(by_folder.items()):
        print("  {}: {} images".format(folder, c))
    
    # Show some sample entries
    print("\nSample entries:")
    for item in regen_queue[:5]:
        print("  {}: pk={}, sub={}, prefix={}, count={}".format(
            item['id'], item['prompt_key'], item['output_subfolder'],
            item['filename_prefix'], item['count']))


if __name__ == "__main__":
    main()
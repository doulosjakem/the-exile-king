"""
Analyze full_review.json to determine exact regeneration scope.
Outputs:
1. Per-prompt_key counts of score <= 3 images
2. Per-subfolder counts
3. Which prompt_keys are missing from generation_queue.json
4. Which prompt_keys are missing from EXPECTED_PROMPTS
"""
import json
import os
from collections import Counter, defaultdict

# Load review
with open('full_review.json', 'r') as f:
    data = json.load(f)

low = [img for img in data['images'] if img['score'] <= 3]
print("=== REGENERATION SCOPE ===")
print("Total low-scored images: {}".format(len(low)))
print("Score 1: {}".format(len([x for x in low if x["score"]==1])))
print("Score 2: {}".format(len([x for x in low if x["score"]==2])))
print("Score 3: {}".format(len([x for x in low if x["score"]==3])))

# Group by expected_prompt_key
print("\n=== BY PROMPT KEY ===")
keys = Counter()
for img in low:
    k = img.get('expected_prompt_key') or 'null'
    keys[k] += 1
for k, c in keys.most_common():
    print("  {}: {}".format(k, c))

# Group by subfolder (extract from filename)
print("\n=== BY SUBFOLDER ===")
folders = Counter()
for img in low:
    fn = img['filename']
    parts = fn.split('\\')
    if len(parts) >= 2:
        folder = parts[0]
        folders[folder] += 1
    else:
        folders['root'] += 1
for f, c in folders.most_common():
    print("  {}: {}".format(f, c))

# Load generation_queue.json
with open('generation_queue.json', 'r') as f:
    queue = json.load(f)

queue_prompt_keys = set()
queue_prefixes = {}
for item in queue:
    pk = item.get('prompt_key', '')
    queue_prompt_keys.add(pk)
    prefix = item.get('filename_prefix', '')
    if prefix:
        queue_prefixes[prefix] = pk

# Load EXPECTED_PROMPTS from review_art_ollama.py
# Parse the file to extract keys
expected_prompts_keys = set()
with open('review_art_ollama.py', 'r', encoding='utf-8') as f:
    content = f.read()
# Find all EXPECTED_PROMPTS keys
import re
# Match patterns like "key": "value" or "key": (multi-line)
for m in re.finditer(r'^\s+"([^"]+)"\s*:', content, re.MULTILINE):
    expected_prompts_keys.add(m.group(1))

# Check which low-scored prompt keys are missing from queue
print("\n=== PROMPT KEYS IN LOW-SCORED BUT NOT IN generation_queue.json ===")
missing_from_queue = []
for k in keys:
    if k == 'null':
        continue
    if k not in queue_prompt_keys:
        # Check with underscore/hyphen normalization
        normalized = k.replace('-', '_')
        if normalized not in queue_prompt_keys:
            missing_from_queue.append(k)
for k in sorted(missing_from_queue):
    print("  {} (count: {})".format(k, keys[k]))

# Check which are missing from EXPECTED_PROMPTS
print("\n=== PROMPT KEYS IN LOW-SCORED BUT NOT IN EXPECTED_PROMPTS ===")
missing_from_ep = []
for k in keys:
    if k == 'null':
        continue
    if k not in expected_prompts_keys:
        normalized = k.replace('-', '_')
        if normalized not in expected_prompts_keys:
            missing_from_ep.append(k)
for k in sorted(missing_from_ep):
    print("  {} (count: {})".format(k, keys[k]))

# For null expected_prompt_key, extract the filename prefix
print("\n=== NULL PROMPT KEY FILES (by filename prefix) ===")
null_prefixes = Counter()
null_files = [img for img in low if img.get('expected_prompt_key') is None]
for img in null_files:
    fn = img['filename']
    stem = os.path.splitext(fn)[0]
    # Remove _00001_ style suffix
    stem_clean = re.sub(r'_\d{5}_$', '', stem)
    # Get the last meaningful part
    parts = stem_clean.split('\\')
    prefix = parts[-1] if parts else stem_clean
    null_prefixes[prefix] += 1
for p, c in null_prefixes.most_common():
    print("  {}: {}".format(p, c))

# Show the actual filenames for null prompt key
print("\n=== ALL NULL PROMPT KEY FILENAMES ===")
for img in null_files:
    print("  {} (score={})".format(img['filename'], img['score']))
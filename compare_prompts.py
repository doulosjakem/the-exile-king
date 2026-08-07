import json
import sys
sys.path.insert(0, r"D:\the-exile-king")

from review_art_ollama import EXPECTED_PROMPTS, FILENAME_TO_PROMPT, lookup_expected_prompt
from run_comfyui_generation import resolve_prompt

# Load the generation queue
with open("prep_regen_queue.json") as f:
    queue = json.load(f)

# Check a card-back item
for item in queue:
    if "card-back" in item["id"]:
        print(f"Queue item: {item['id']}")
        print(f"  prompt_key: {item['prompt_key']}")
        gen_prompt = resolve_prompt(item["prompt_key"])
        print(f"  Gen prompt (first 200 chars): {gen_prompt[:200]}")
        print()

# Check what review expects for card-back files
rel_path = "card-backs/card-back_00001_.png"
expected, key = lookup_expected_prompt(rel_path)
print(f"Review lookup for card-backs/card-back_00001_.png:")
print(f"  expected_key: {key}")
if expected:
    print(f"  Review prompt (first 200 chars): {expected[:200]}")
print()

# Check a commander card
rel_path2 = "commander-cards/david-01_00001_.png"
expected2, key2 = lookup_expected_prompt(rel_path2)
print(f"Review lookup for commander-cards/david-01_00001_.png:")
print(f"  expected_key: {key2}")
if expected2:
    print(f"  Review prompt (first 200 chars): {expected2[:200]}")

# Find the corresponding queue item
for item in queue:
    if item["id"] == "commander-card-david-01":
        print(f"  Queue prompt_key: {item['prompt_key']}")
        gen_prompt = resolve_prompt(item["prompt_key"])
        print(f"  Gen prompt (first 200 chars): {gen_prompt[:200]}")
        if expected2:
            print(f"  Match: {gen_prompt == expected2}")
        break

print()

# Check a unit-disc
rel_path3 = "unit-discs/david_00001_.png"
expected3, key3 = lookup_expected_prompt(rel_path3)
print(f"Review lookup for unit-discs/david_00001_.png:")
print(f"  expected_key: {key3}")
if expected3:
    print(f"  Review prompt (first 200 chars): {expected3[:200]}")

for item in queue:
    if item["id"] == "unit-disc-david":
        print(f"  Queue prompt_key: {item['prompt_key']}")
        gen_prompt = resolve_prompt(item["prompt_key"])
        print(f"  Gen prompt (first 200 chars): {gen_prompt[:200]}")
        if expected3:
            print(f"  Match: {gen_prompt == expected3}")
        break

print()

# Check a unit-card
rel_path4 = "unit-cards/swordsmen-advance-01_00001_.png"
expected4, key4 = lookup_expected_prompt(rel_path4)
print(f"Review lookup for unit-cards/swordsmen-advance-01_00001_.png:")
print(f"  expected_key: {key4}")
if expected4:
    print(f"  Review prompt (first 200 chars): {expected4[:200]}")
print()
print("FILENAME_TO_PROMPT entries:")
for k, v in FILENAME_TO_PROMPT.items():
    if k.startswith("swordsmen") or k.startswith("spearman") or k.startswith("slinger"):
        print(f"  {k}: prompt_key={v}")

import json
import sys
sys.path.insert(0, r"D:\the-exile-king")

from review_art_ollama import EXPECTED_PROMPTS, lookup_expected_prompt
from run_comfyui_generation import resolve_prompt, load_prompts

# Load prompts into the generation module
load_prompts()

from run_comfyui_generation import resolve_prompt as rp

# Check card_back
key = "card_back"
gen_prompt = rp(key)
review_prompt, review_key = lookup_expected_prompt("card-backs/card-back_00001_.png")

print(f"Key: {key}")
print(f"Gen prompt (first 200 chars): {gen_prompt[:200]}")
print(f"Review prompt (first 200 chars): {review_prompt[:200]}")
print(f"Match: {gen_prompt == review_prompt}")
print()

# Check commander card
key2 = "card_front_david"
gen_prompt2 = rp(key2)
review_prompt2, review_key2 = lookup_expected_prompt("commander-cards/david-01_00001_.png")
print(f"Key: {key2}")
print(f"Gen prompt (first 200 chars): {gen_prompt2[:200]}")
print(f"Review prompt (first 200 chars): {review_prompt2[:200]}")
print(f"Match: {gen_prompt2 == review_prompt2}")
print()

# Check unit-disc
key3 = "david_commander"
gen_prompt3 = rp(key3)
review_prompt3, review_key3 = lookup_expected_prompt("unit-discs/david_00001_.png")
print(f"Key: {key3}")
print(f"Gen prompt (first 200 chars): {gen_prompt3[:200]}")
print(f"Review prompt (first 200 chars): {review_prompt3[:200]}")
print(f"Match: {gen_prompt3 == review_prompt3}")
print()

# Check unit-card
key4 = "swordsmen-advance"
gen_prompt4 = rp(key4)
review_prompt4, review_key4 = lookup_expected_prompt("unit-cards/swordsmen-advance-01_00001_.png")
print(f"Key: {key4}")
print(f"Gen prompt (first 200 chars): {gen_prompt4[:200]}")
print(f"Review prompt (first 200 chars): {review_prompt4[:200]}")
print(f"Review key: {review_key4}")
print(f"Match: {gen_prompt4 == review_prompt4}")
print()

# Check what keys are in EXPECTED_PROMPTS
print(f"Total EXPECTED_PROMPTS keys: {len(EXPECTED_PROMPTS)}")
print(f"Has 'card_back': {'card_back' in EXPECTED_PROMPTS}")
print(f"Has 'card_front_david': {'card_front_david' in EXPECTED_PROMPTS}")
print(f"Has 'david_commander': {'david_commander' in EXPECTED_PROMPTS}")
print(f"Has 'swordsmen_advance': {'swordsmen_advance' in EXPECTED_PROMPTS}")
print(f"Has 'swordsmen-advance': {'swordsmen-advance' in EXPECTED_PROMPTS}")
print(f"Has 'spearman_david': {'spearman_david' in EXPECTED_PROMPTS}")
print()

# List all keys
print("All keys:")
for k in sorted(EXPECTED_PROMPTS.keys()):
    print(f"  {k}")

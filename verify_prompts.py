import json

with open("review_art_ollama.py", "r", encoding="utf-8") as f:
    content = f.read()

with open("generation_queue.json", "r") as f:
    queue = json.load(f)

needed_keys = set()
for item in queue:
    pk = item.get("prompt_key", "")
    if pk:
        needed_keys.add(pk)

print(f"Total needed keys: {len(needed_keys)}")

found = set()
missing = set()

for key in needed_keys:
    pattern = '"' + key + '"'
    if pattern in content:
        found.add(key)
    else:
        missing.add(key)

print(f"Found: {len(found)}")
print(f"Missing: {len(missing)}")
for k in sorted(missing):
    print(f"  {k}")

for k in ["refugee", "reward_panel", "camel-rider_amalekite", "box-art-round3-david-as-king"]:
    pat = '"' + k + '"'
    print(f"{k} in file: {pat in content}")

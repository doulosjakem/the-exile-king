"""
Cleanly add all missing prompts to review_art_ollama.py EXPECTED_PROMPTS dict.
"""
import json
import re

with open("review_art_ollama.py", "r", encoding="utf-8") as f:
    content = f.read()
    lines = content.splitlines(keepends=True)

# Find the line with EXPECTED_PROMPTS = {
for i, line in enumerate(lines):
    if "EXPECTED_PROMPTS = {" in line:
        start_idx = i
        break

# Find the FIRST } after start_idx that is on its own line (with only whitespace)
# This is the closing brace of EXPECTED_PROMPTS
end_idx = None
for i in range(start_idx + 1, len(lines)):
    if lines[i].strip() == "}":
        end_idx = i
        break

print(f"EXPECTED_PROMPTS starts at line {start_idx + 1}, ends at line {end_idx + 1}")

# Now build the new entries list
with open("generation_queue.json", "r") as f:
    queue = json.load(f)

needed_keys = set()
for item in queue:
    pk = item.get("prompt_key", "")
    if pk:
        needed_keys.add(pk)

# Extract existing keys from the current file
existing_text = "".join(lines[start_idx:end_idx+1])
existing_keys = set(re.findall(r'"([^"]+)":', existing_text))

missing = needed_keys - existing_keys
print(f"Existing keys: {len(existing_keys)}")
print(f"Needed keys: {len(needed_keys)}")
print(f"Missing keys: {len(missing)}")

# Build prompt dict for missing keys
new_prompts = {}

# Portraits from PROMPTS.md
portraits = {
    "abigail": "ONE PERSON ONLY, solo portrait, waist-up, Abigail wife of Nabal, bronze age Levantine noblewoman, dark hair in woven braids, rich but practical woolen tunic in faded blue, leather belt, small knife at waist, face showing intelligence and caution, standing with a loaded donkey behind her, laden with gifts, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "benjamin-spearman": "ONE PERSON ONLY, solo portrait, waist-up, Benjamite spearman of Jonathan's guard, bronze age Levantine elite infantry, strong fierce build, dark hair, white linen tunic with leather shoulder guards, brown cloak wrapped and fastened, long wooden spear with bronze tip held upright, small hide shield at side, leather cord belt with knife, alert loyal expression, standing in disciplined formation, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "judah-militia": "ONE PERSON ONLY, solo portrait, waist-up, Judah militia defender, bronze age Levantine village warrior, sturdy build, dark hair, simple linen tunic with leather vest, brown wool cloak, bronze short sword in hand, small round hide shield, leather sandals, determined local expression, leaning on spear in resting pose, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "nabal": "ONE PERSON ONLY, solo portrait, waist-up, Nabal the Carmelite, bronze age Levantine wealthy landowner, heavyset build, dark hair and short beard, rich woolen tunic with woven border, bronze rings on fingers, bronze short sword at hip, expression of stubborn pride, seated on a low stool with a wine cup in hand, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "priest-of-nob": "ONE PERSON ONLY, solo portrait, waist-up, priest of Nob, bronze age Levantine priest, older man, white linen ephod over simple tunic, bronze plate on chest with Urim and Thummim, short beard, kind eyes, holding a loaf of showbread, standing before a stone altar, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
}

# Round 3 box art
round3_boxart = {
    "box-art-round3-david-as-king": "game box art, painting in illuminated manuscript style, David crowned at Hebron, elder standing before him with a horn of oil, olive trees and stone walls in background, autumn golden light, his captains behind him, composition is kingship earned through hardship, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-round3-david-at-adullam": "game box art, painting in illuminated manuscript style, David seated at the entrance of a cave at Adullam, surrounded by a ragtag band of outcasts and warriors, one man sharpening a spear, another mending a cloak, warm firelight against dark rock, composition is intimate and raw, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-round3-jonathan-and-david": "game box art, painting in illuminated manuscript style, Jonathan and David standing on a hilltop at Mizpah, Jonathan taking off his robe and giving it to David along with his weapons, wind blowing the fabric between them, golden light, composition is tender and covenant-making, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-round3-the-cave-of-engedi": "game box art, painting in illuminated manuscript style, inside the dark cave at Ein Gedi, David standing in the shadows near Saul who is sleeping, Saul's robe spread wide at the entrance, David's hand hovering near the hem deciding whether to strike, torchlight flickering, composition is the moment of mercy, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-round3-the-wounded-david": "game box art, painting in illuminated manuscript style, David lying wounded and exhausted on a rocky hillside, his armor scattered, a single warrior kneeling beside him offering water, dark storm clouds above, composition is vulnerability and trust, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded indigo, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
}

# Aliases for inconsistent naming in queue
aliases = {}
for key in ["camel-rider_amalekite", "chieftain_amalekite", "raider_amalekite", "reward-panel"]:
    lookup = key.replace("-", "_")
    pattern = '"' + lookup + '":\\s*"([^"]*)"'
    m = re.search(pattern, content)
    if m:
        aliases[key] = m.group(1)
        print(f"Alias: {key} -> {lookup}")
    else:
        print(f"Alias MISSING: {key} (looked for {lookup})")

# Combine all new prompts
all_new = {}
for k, v in portraits.items():
    if k in missing:
        all_new[k] = v
for k, v in round3_boxart.items():
    if k in missing:
        all_new[k] = v
for k, v in aliases.items():
    if k in missing:
        all_new[k] = v

print(f"New prompts to add: {len(all_new)}")

# Build new lines to insert before end_idx
insert_lines = []
for key in sorted(all_new.keys()):
    val = all_new[key]
    escaped = val.replace("\\", "\\\\").replace('"', '\\"')
    insert_lines.append(f'    "{key}": "{escaped}",\n')

# Insert before the closing brace
new_lines = lines[:end_idx] + insert_lines + lines[end_idx:]

with open("review_art_ollama.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print(f"Added {len(insert_lines)} entries before line {end_idx + 1}")

# Verify syntax
try:
    with open("review_art_ollama.py", "r", encoding="utf-8") as f:
        code = f.read()
    compile(code, "review_art_ollama.py", "exec")
    print("Syntax check: PASSED")
except SyntaxError as e:
    print(f"Syntax error: {e}")

# Verify all keys present
with open("review_art_ollama.py", "r", encoding="utf-8") as f:
    new_content = f.read()

still_missing = []
for key in needed_keys:
    if '"' + key + '"' not in new_content:
        still_missing.append(key)

print(f"Still missing keys: {len(still_missing)}")
for k in sorted(still_missing):
    print(f"  {k}")

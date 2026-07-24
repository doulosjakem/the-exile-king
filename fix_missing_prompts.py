"""
Add the 14 remaining missing prompts to review_art_ollama.py
"""
import json

# Read current file
with open("review_art_ollama.py", "r", encoding="utf-8") as f:
    content = f.read()

# Prompts from PROMPTS.md (lines 311-315, 323-327)
portrait_prompts_from_md = {
    "abigail": "ONE PERSON ONLY, solo portrait, waist-up, Abigail wife of Nabal, bronze age Levantine noblewoman, dark hair in woven braids, rich but practical woolen tunic in faded blue, leather belt, small knife at waist, face showing intelligence and caution, standing with a loaded donkey behind her, laden with gifts, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "benjamin-spearman": "ONE PERSON ONLY, solo portrait, waist-up, Benjamite spearman of Jonathan's guard, bronze age Levantine elite infantry, strong fierce build, dark hair, white linen tunic with leather shoulder guards, brown cloak wrapped and fastened, long wooden spear with bronze tip held upright, small hide shield at side, leather cord belt with knife, alert loyal expression, standing in disciplined formation, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "judah-militia": "ONE PERSON ONLY, solo portrait, waist-up, Judah militia defender, bronze age Levantine village warrior, sturdy build, dark hair, simple linen tunic with leather vest, brown wool cloak, bronze short sword in hand, small round hide shield, leather sandals, determined local expression, leaning on spear in resting pose, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "nabal": "ONE PERSON ONLY, solo portrait, waist-up, Nabal the Carmelite, bronze age Levantine wealthy landowner, heavyset build, dark hair and short beard, rich woolen tunic with woven border, bronze rings on fingers, bronze short sword at hip, expression of stubborn pride, seated on a low stool with a wine cup in hand, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "priest-of-nob": "ONE PERSON ONLY, solo portrait, waist-up, priest of Nob, bronze age Levantine priest, older man, white linen ephod over simple tunic, bronze plate on chest with Urim and Thummim, short beard, kind eyes, holding a loaf of showbread, standing before a stone altar, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
}

box_art_round3_prompts = {
    "box-art-round3-david-at-adullam": "game box art, painting in illuminated manuscript style, David seated at the entrance of a cave at Adullam, surrounded by a ragtag band of outcasts and warriors, one man sharpening a spear, another mending a cloak, warm firelight against dark rock, composition is intimate and raw, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-round3-jonathan-and-david": "game box art, painting in illuminated manuscript style, Jonathan and David standing on a hilltop at Mizpah, Jonathan taking off his robe and giving it to David along with his weapons, wind blowing the fabric between them, golden light, composition is tender and covenant-making, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-round3-the-wounded-david": "game box art, painting in illuminated manuscript style, David lying wounded and exhausted on a rocky hillside, his armor scattered, a single warrior kneeling beside him offering water, dark storm clouds above, composition is vulnerability and trust, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded indigo, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-round3-the-cave-of-engedi": "game box art, painting in illuminated manuscript style, inside the dark cave at Ein Gedi, David standing in the shadows near Saul who is sleeping, Saul's robe spread wide at the entrance, David's hand hovering near the hem deciding whether to strike, torchlight flickering, composition is the moment of mercy, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-round3-david-as-king": "game box art, painting in illuminated manuscript style, David crowned at Hebron, elder standing before him with a horn of oil, olive trees and stone walls in background, autumn golden light, his captains behind him, composition is kingship earned through hardship, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
}

# Aliases for inconsistent prompt_keys in queue
aliases = {
    "camel-rider_amalekite": None,  # will be filled from existing camel_rider_amalekite
    "chieftain_amalekite": None,    # will be filled from existing chieftain
    "raider_amalekite": None,       # will be filled from existing raider
    "reward-panel": None,           # will be filled from existing reward_panel
}

# Extract existing values for aliases
import re

def get_existing_prompt(key):
    pattern = '"' + key + '":\\s*"([^"]*)"'
    m = re.search(pattern, content)
    if m:
        return m.group(1)
    return None

aliases["camel-rider_amalekite"] = get_existing_prompt("camel_rider_amalekite")
aliases["chieftain_amalekite"] = get_existing_prompt("chieftain")
aliases["raider_amalekite"] = get_existing_prompt("raider")
aliases["reward-panel"] = get_existing_prompt("reward_panel")

# Build all new entries
entries_to_add = {}

for k, v in portrait_prompts_from_md.items():
    if '"' + k + '"' not in content:
        entries_to_add[k] = v

for k, v in box_art_round3_prompts.items():
    if '"' + k + '"' not in content:
        entries_to_add[k] = v

for k, v in aliases.items():
    if v and ('"' + k + '"' not in content):
        entries_to_add[k] = v

print(f"Entries to add: {len(entries_to_add)}")
for k in sorted(entries_to_add.keys()):
    print(f"  {k}")

# Find closing brace of EXPECTED_PROMPTS
lines = content.splitlines(keepends=True)
closing_idx = None
for i in range(len(lines) - 1, -1, -1):
    if lines[i].strip() == "}" and i > 20:
        context = "".join(lines[max(0, i-10):i+1])
        if "EXPECTED_PROMPTS" in context or "sand" in context or "ui-portrait-frame" in context:
            closing_idx = i
            break

if closing_idx is None:
    print("ERROR: Could not find closing brace")
    exit(1)

print(f"Found closing brace at line {closing_idx + 1}")

# Insert new entries before closing brace
new_lines = []
for k, v in sorted(entries_to_add.items()):
    escaped_v = v.replace("\\", "\\\\").replace('"', '\\"')
    new_lines.append(f'    "{k}": "{escaped_v}",\n')

lines = lines[:closing_idx] + new_lines + lines[closing_idx:]

with open("review_art_ollama.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print(f"Added {len(entries_to_add)} entries to review_art_ollama.py")

# Verify
with open("review_art_ollama.py", "r", encoding="utf-8") as f:
    new_content = f.read()

still_missing = []
for k in list(portrait_prompts_from_md.keys()) + list(box_art_round3_prompts.keys()) + list(aliases.keys()):
    if '"' + k + '"' not in new_content:
        still_missing.append(k)

if still_missing:
    print(f"WARNING: Still missing: {still_missing}")
else:
    print("All missing entries now present!")

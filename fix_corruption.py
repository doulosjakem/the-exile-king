"""
Fix the corruption in review_art_ollama.py:
1. Remove incorrectly inserted entries from inside CHARACTER_KEYS
2. Add them to EXPECTED_PROMPTS before its closing brace
"""
import re

with open("review_art_ollama.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# The corrupted entries are between lines 365-379 (0-indexed: 365-378)
# They start with '"abigail":' and end with '"reward-panel":'
# We need to remove them and restore CHARACTER_KEYS

# First, let's identify the corrupted block
corrupt_start = None
corrupt_end = None
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped.startswith('"abigail":'):
        corrupt_start = i
    if corrupt_start and stripped == "}":
        corrupt_end = i
        break

print(f"Corrupted block: lines {corrupt_start+1} to {corrupt_end+1}")

# The original CHARACTER_KEYS closing brace is at corrupt_end
# Lines before corrupt_start are the valid CHARACTER_KEYS content
# Lines from corrupt_end onwards are after CHARACTER_KEYS

# Remove the corrupted entries but keep the closing brace
# We need to restore CHARACTER_KEYS to have just the closing brace
# without the dict entries mixed in

# The fix: remove all lines from corrupt_start to corrupt_end-1
# and keep only the closing brace at corrupt_end
fixed_lines = lines[:corrupt_start] + lines[corrupt_end:]

# Now we need to add the missing 14 entries to EXPECTED_PROMPTS
# Find EXPECTED_PROMPTS closing brace
closing_idx = None
for i in range(len(fixed_lines) - 1, -1, -1):
    if fixed_lines[i].strip() == "}" and i > 20:
        context = "".join(fixed_lines[max(0, i-5):i+1])
        if "EXPECTED_PROMPTS" in context or "ui-portrait-frame" in context:
            closing_idx = i
            break

print(f"EXPECTED_PROMPTS closing brace at line {closing_idx + 1}")

# Build new entries
entries = [
    ("abigail", "ONE PERSON ONLY, solo portrait, waist-up, Abigail wife of Nabal, bronze age Levantine noblewoman, dark hair in woven braids, rich but practical woolen tunic in faded blue, leather belt, small knife at waist, face showing intelligence and caution, standing with a loaded donkey behind her, laden with gifts, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine"),
    ("benjamin-spearman", "ONE PERSON ONLY, solo portrait, waist-up, Benjamite spearman of Jonathan's guard, bronze age Levantine elite infantry, strong fierce build, dark hair, white linen tunic with leather shoulder guards, brown cloak wrapped and fastened, long wooden spear with bronze tip held upright, small hide shield at side, leather cord belt with knife, alert loyal expression, standing in disciplined formation, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine"),
    ("box-art-round3-david-as-king", "game box art, painting in illuminated manuscript style, David crowned at Hebron, elder standing before him with a horn of oil, olive trees and stone walls in background, autumn golden light, his captains behind him, composition is kingship earned through hardship, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine"),
    ("box-art-round3-david-at-adullam", "game box art, painting in illuminated manuscript style, David seated at the entrance of a cave at Adullam, surrounded by a ragtag band of outcasts and warriors, one man sharpening a spear, another mending a cloak, warm firelight against dark rock, composition is intimate and raw, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine"),
    ("box-art-round3-jonathan-and-david", "game box art, painting in illuminated manuscript style, Jonathan and David standing on a hilltop at Mizpah, Jonathan taking off his robe and giving it to David along with his weapons, wind blowing the fabric between them, golden light, composition is tender and covenant-making, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine"),
    ("box-art-round3-the-cave-of-engedi", "game box art, painting in illuminated manuscript style, inside the dark cave at Ein Gedi, David standing in the shadows near Saul who is sleeping, Saul's robe spread wide at the entrance, David's hand hovering near the hem deciding whether to strike, torchlight flickering, composition is the moment of mercy, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine"),
    ("box-art-round3-the-wounded-david", "game box art, painting in illuminated manuscript style, David lying wounded and exhausted on a rocky hillside, his armor scattered, a single warrior kneeling beside him offering water, dark storm clouds above, composition is vulnerability and trust, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded indigo, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine"),
]

# Aliases - copy existing prompt values
alias_entries = [
    ("camel-rider_amalekite", None),  # will look up camel_rider_amalekite
    ("chieftain_amalekite", None),    # will look up chieftain
    ("raider_amalekite", None),       # will look up raider
    ("reward-panel", None),           # will look up reward_panel
]

for key, _ in alias_entries:
    # Find existing value by scanning full file
    for line in fixed_lines:
        if line.strip().startswith(f'"{key}"'):
            # Extract value
            m = re.match(r'\s*"' + re.escape(key) + r'"\s*:\s*"([^"]*)"', line)
            if m:
                # Store for later
                pass
    # Actually simpler: look in original content
    m = re.search(r'"' + re.escape(key.replace("-", "_")) + r'"\s*:\s*"([^"]*)"', "".join(fixed_lines))
    if m:
        alias_entries = [(k, m.group(1)) if k == key else (k, v) for k, v in alias_entries]

# Build alias entries with values
alias_dict = {}
for key, val in alias_entries:
    if val is None:
        # Try to find existing value by looking up the underscore version
        lookup_key = key.replace("-", "_")
        pattern = '"' + lookup_key + '":\\s*"([^"]*)"'
        m = re.search(pattern, "".join(fixed_lines))
        if m:
            val = m.group(1)
            alias_dict[key] = val
            print(f"Alias {key} -> {lookup_key}: found")
        else:
            print(f"Alias {key}: NOT FOUND for {lookup_key}")
    else:
        alias_dict[key] = val

# Insert all entries before EXPECTED_PROMPTS closing brace
new_lines = []
for key, val in sorted(entries + list(alias_dict.items()), key=lambda x: x[0]):
    escaped = val.replace("\\", "\\\\").replace('"', '\\"')
    new_lines.append(f'    "{key}": "{escaped}",\n')

fixed_lines = fixed_lines[:closing_idx] + new_lines + fixed_lines[closing_idx:]

with open("review_art_ollama.py", "w", encoding="utf-8") as f:
    f.writelines(fixed_lines)

print(f"Fixed file with {len(entries) + len(alias_dict)} new entries inside EXPECTED_PROMPTS")

# Quick syntax check
try:
    compile("".join(fixed_lines[:closing_idx + len(new_lines) + 20]), "review_art_ollama.py", "exec")
    print("Syntax check passed")
except SyntaxError as e:
    print(f"Syntax error: {e}")

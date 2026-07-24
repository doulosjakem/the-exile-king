"""
Script to add all missing prompts to review_art_ollama.py EXPECTED_PROMPTS dict.
Reads from PROMPTS.md and generates character portraits from templates.
"""
import ast
import json
import re
import os

PROJECT_ROOT = r"D:\the-exile-king"

# Read generation queue
with open(f"{PROJECT_ROOT}/generation_queue.json", "r", encoding="utf-8") as f:
    queue = json.load(f)

needed_keys = set()
for item in queue:
    pk = item.get("prompt_key", "")
    if pk:
        needed_keys.add(pk)

print(f"Needed keys: {len(needed_keys)}")

# Parse existing EXPECTED_PROMPTS from review_art_ollama.py
with open(f"{PROJECT_ROOT}/review_art_ollama.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

dict_lines = lines[21:101]
dict_text = "".join(dict_lines)
dict_text = re.sub(r"#.*", "", dict_text)
start = dict_text.find("{")
brace_count = 0
end = start
for i in range(start, len(dict_text)):
    if dict_text[i] == "{":
        brace_count += 1
    elif dict_text[i] == "}":
        brace_count -= 1
        if brace_count == 0:
            end = i + 1
            break
clean_dict = dict_text[start:end]
clean_dict = re.sub(r",\s*\}", "}", clean_dict)

existing_prompts = ast.literal_eval(clean_dict)
print(f"Existing prompts: {len(existing_prompts)}")

# Read PROMPTS.md
with open(f"{PROJECT_ROOT}/PROMPTS.md", "r", encoding="utf-8") as f:
    prompts_md = f.read()

# Extract box art prompts from markdown table
box_art_prompts = {}
for m in re.finditer(r'\| `(box-art-[^`]+)` \| `([^`]+)` \|', prompts_md):
    key = m.group(1)
    val = m.group(2).strip()
    box_art_prompts[key] = val

print(f"Box art prompts extracted: {len(box_art_prompts)}")

# Extract portrait/character prompts
portrait_prompts = {}
name_to_key = {
    "Benjamin Spearman": "benjamin-spearman",
    "Judah Militia": "judah-militia",
    "Abigail": "abigail",
    "Nabal": "nabal",
    "Priest of Nob": "priest-of-nob",
    "Jonathan Precision": "jonathan-precision",
    "Joab Assault": "joab-assault",
    "Amasa Rally": "amasa-rally",
    "Asahel Flank": "asahel-flank",
    "Philistine Charge": "philistine-charge",
    "Goliath Challenge": "goliath-challenge",
    "Amalekite Raid": "amalekite-raid",
}

for display_name, key in name_to_key.items():
    pattern = re.escape(display_name) + r' \| `([^`]+)` \|'
    m = re.search(pattern, prompts_md)
    if m:
        portrait_prompts[key] = m.group(1).strip()

print(f"Portrait prompts extracted: {len(portrait_prompts)}")

# Extract tile prompts
tile_prompts = {
    "hex-tile-desert-night": "top-down flat hex tile, desert at night, cool blue-gray under moonlight, subtle stars, watercolor wash, board game style, seamless, 512x512",
    "hex-tile-stone-path": "top-down flat hex tile, ancient stone path and packed earth, gray-brown, ink wash texture, board game style, seamless, 512x512",
    "hex-tile-ruins": "top-down flat hex tile, broken stone walls and rubble, weathered umber, watercolor and ink wash, board game style, seamless, 512x512",
}

# Extract UI prompts
ui_prompts = {
    "ui-portrait-frame": "ornate rectangular frame for character portrait, aged parchment with dark ink border, corner ornaments, board game UI element, hand-painted illustration, transparent background, NOT medieval, NOT fantasy, NOT European",
    "ui-card-slot": "empty card slot on table, aged parchment background, wooden card border, board game UI element, transparent background, hand-painted illustration, NOT medieval, NOT fantasy, NOT European",
    "ui-commander-aura": "soft glowing circle on ground, commander presence area, warm golden light, board game UI element, transparent background, hand-painted illustration, NOT medieval, NOT fantasy, NOT European",
}

# Generate missing character portrait prompts
CHARACTER_TEMPLATE = "ONE PERSON ONLY, solo portrait, waist-up, {description}, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine"

character_descriptions = {
    "saul": "Saul king of Israel, bronze age Levantine monarch, tall commanding presence, dark hair and short beard, rich purple-blue wool cloak over linen tunic, bronze chest plate with simple geometric engraving, bronze short sword at hip, leather sandals, stern authoritative expression, standing with regal bearing, Mediterranean complexion",
    "abner": "Abner commander of Saul's army, bronze age Levantine military leader, strong build, dark hair and beard, leather vest over linen tunic, brown wool cloak, bronze spear in hand, hardened battle expression, alert posture, standing on rocky ground, Mediterranean complexion",
    "royal-guard": "Israelite royal guard, bronze age Levantine elite infantryman, dark hair, white linen tunic with woven border, leather vest, brown wool cloak pinned at shoulder, bronze short sword, small round hide shield, loyal disciplined expression, standing at attention, Mediterranean complexion",
    "benjamite-spearman": "Benjamite spearman of Jonathan's guard, bronze age Levantine elite infantry, strong fierce build, dark hair, white linen tunic with leather shoulder guards, brown cloak wrapped and fastened, long wooden spear with bronze tip held upright, small hide shield at side, leather cord belt with knife, alert loyal expression, standing in disciplined formation, Mediterranean complexion",
    "israelite-archer": "Israelite archer of Saul's army, bronze age Levantine archer, dark hair, simple linen tunic with leather vest, brown cloak, short composite bow in hand with arrow nocked, quiver on back, knife at waist, focused expression, standing ready, Mediterranean complexion",
    "officer": "Israelite army officer, bronze age Levantine military commander, dark hair and short beard, linen tunic with leather vest, brown wool cloak, bronze short sword at hip, bronze spear in hand, authoritative expression, standing with command presence, Mediterranean complexion",
    "elite-bodyguard": "Israelite elite bodyguard, bronze age Levantine royal protector, dark hair, well-fitted linen tunic with leather armor, brown cloak, large hide shield, bronze short sword, alert protective stance, loyal expression, standing ready to defend, Mediterranean complexion",
    "jonathan": "Jonathan son of Saul, bronze age Levantine prince and warrior, dark hair, handsome features, rich blue-purple cloak over linen tunic, leather vest, composite bow in hand, quiver on back, bronze short sword at hip, noble brave expression, standing confidently, Mediterranean complexion",
    "loyal-guard": "Loyal guard of Jonathan, bronze age Levantine elite warrior, dark hair, white linen tunic with dark border, leather vest, brown cloak, spear in hand, small shield, devoted alert expression, standing beside commander, Mediterranean complexion",
    "elite-archer": "Elite archer of Jonathan's guard, bronze age Levantine master archer, dark hair, fitted linen tunic, leather bracers, brown cloak, composite bow drawn with arrow nocked, quiver, focused precise expression, Mediterranean complexion",
    "jonathan-armor-bearer": "Jonathan's armor-bearer, bronze age Levantine elite warrior, dark hair, linen tunic with leather vest, brown cloak, bronze spear, shield at side, loyal brave expression, standing ready, Mediterranean complexion",
    "jonathan-shield-bearer": "Jonathan's shield-bearer, bronze age Levantine warrior, dark hair, strong build, linen tunic with leather armor, large round hide shield held high, bronze sword at hip, protective stance, determined expression, Mediterranean complexion",
    "jonathan-spearman": "Jonathan's spearman guard, bronze age Levantine Benjamite warrior, dark hair, white linen tunic with leather shoulder guards, brown cloak wrapped, long spear with bronze tip held upright, small shield, alert disciplined expression, Mediterranean complexion",
    "joab": "Joab commander of David's army, bronze age Levantine general, tall strong build, gray-streaked beard, dark hair, leather scale armor over linen tunic, brown cloak, bronze spear raised, ruthless brilliant expression, battle-scarred, Mediterranean complexion",
    "amasa": "Amasa captain of Judah, bronze age Levantine commander, honest earnest expression, dark hair and beard, linen tunic with leather vest, brown cloak, bronze spear in hand, appointed captain bearing, standing with quiet authority, Mediterranean complexion",
    "asahel": "Asahel son of Zeruiah, bronze age Levantine runner warrior, lean swift build, dark hair, light linen tunic with leather vest, wrapped cloak for swift movement, short sword raised, running stance, focused expression, Mediterranean complexion",
    "achish": "Achish lord of Gath, bronze age Levantine Philistine ruler, dark hair, rich purple cloak over linen tunic, bronze chest plate, bronze sword at hip, stern unreadable expression, seated authority, Mediterranean complexion",
    "philistine-lord": "Philistine lord, bronze age Levantine city-state ruler, dark hair, rich embroidered tunic, bronze scale armor, purple cloak, bronze sword, authoritative expression, standing with regal bearing, Mediterranean complexion",
    "philistine-spearman": "Philistine spearman, bronze age Levantine infantry, dark hair, linen tunic with leather vest, large rectangular shield, long bronze-tipped spear, bronze helmet, steady formation stance, Mediterranean complexion",
    "philistine-heavy": "Philistine heavy infantry, bronze age Levantine warrior, large build, dark hair, linen tunic with bronze scale armor, large hide-covered shield with bronze rim, long spear, bronze short sword, imposing slow stance, Mediterranean complexion",
    "philistine-archer": "Philistine archer, bronze age Levantine archer, dark hair, simple tunic with leather vest, short bow drawn, quiver on back, sharp eyes, focused expression, standing ready, Mediterranean complexion",
    "philistine-charioteer": "Philistine charioteer, bronze age Levantine warrior, dark hair, linen tunic with leather armor, brown cloak flowing, standing beside bronze-rimmed chariot, spear in hand, weathered determined expression, Mediterranean complexion",
    "philistine-champion": "Philistine champion, bronze age Levantine elite warrior, dark hair, decorated tunic, bronze scale armor, large shield, spear raised, confident duelist expression, standing in challenge pose, Mediterranean complexion",
    "goliath": "Goliath the Gittite, bronze age Levantine giant champion, enormous build, dark hair and beard, elaborate tunic, bronze scale armor, large bronze shield, massive bronze-tipped spear like a weaver's beam, jawset expression, towering menacing figure, Mediterranean complexion",
    "lahmi": "Lahmi the giant, bronze age Levantine Rephaim warrior, enormous build, dark hair, simple tunic, bronze spear, fierce expression, towering figure, Mediterranean complexion",
    "saph": "Saph the giant, bronze age Levantine Rephaim warrior, enormous build, dark hair, worn tunic, large shield, bronze sword, threatening expression, Mediterranean complexion",
    "girzite-chief": "Girzite chief, bronze age Levantine desert clan leader, dark windblown hair, weathered face, dusty brown cloak wrapped around, leather tunic, bronze spear in hand, bronze short sword at hip, authoritative scorched expression, Mediterranean complexion",
    "girzite-raider": "Girzite raider, bronze age Levantine desert skirmisher, dark windblown hair, lean weathered face, dusty brown cloak, leather tunic, javelin in hand, leather sling, hardened expression, alert stance, Mediterranean complexion",
    "girzite-scout": "Girzite scout, bronze age Levantine desert tracker, lean dark-haired man, dusty brown cloak patched, short javelin, sling at belt, small shield, sharp alert eyes scanning horizon, Mediterranean complexion",
    "girzite-shepherd-raider": "Girzite shepherd-raider, bronze age Levantine desert warrior, lean build, dark windblown hair, dusty brown cloak, leather vest, sling at belt, short spear, shepherd's crook leaning nearby, weathered expression, Mediterranean complexion",
    "geshurite-archer": "Geshurite archer, bronze age Levantine desert archer, dark hair, linen tunic with leather vest, dusty brown cloak, short composite bow drawn with arrow, quiver on back, sharp focused expression, standing on rocky desert ground, Mediterranean complexion",
    "geshurite-spearman": "Geshurite spearman, bronze age Levantine infantry, dark hair, linen tunic with leather shoulder piece, brown cloak, long wooden spear with bronze tip held in both hands, small hide shield, determined expression, Mediterranean complexion",
    "geshurite-camel-rider": "Geshurite camel rider, bronze age Levantine desert warrior, dark hair, dusty brown cloak and headwrap, bronze-tipped spear held upright, riding tall dromedary camel, leather reins in hand, weathered expression, Mediterranean complexion",
    "geshurite-clansman": "Geshurite clansman, bronze age Levantine tribal warrior, dark hair, linen tunic with leather vest, worn brown cloak, bronze short sword, sling at belt, small knife, alert expression, Mediterranean complexion",
    "gezerite-defender": "Gezerite defender, bronze age Levantine Canaanite warrior, dark hair, sturdy build, linen tunic with leather shoulder armor, round hide shield, bronze spear, determined defensive expression, standing firm, Mediterranean complexion",
    "gezerite-archer": "Gezerite archer, bronze age Levantine Canaanite archer, dark hair, linen tunic, leather vest, short composite bow drawn, quiver on back, sharp eyes, focused expression, Mediterranean complexion",
    "gezerite-scout": "Gezerite scout, bronze age Levantine tracker, lean dark-haired man, linen tunic with leather vest, worn cloak, short javelin, sling at belt, alert watchful expression, scanning horizon, Mediterranean complexion",
    "mighty-josheb-basshebeth": "Josheb-basshebeth the Tachmonite, bronze age Levantine mighty man, powerful build, dark hair and beard, bronze scale armor over linen tunic, brown cloak, massive bronze spear held upright, fierce legendary expression, standing with enormous weapon, Mediterranean complexion",
    "mighty-eleazar": "Eleazar son of Dodai, bronze age Levantine mighty man, strong fierce build, dark hair and beard, linen tunic with leather vest, bronze spear raised, small round shield, determined exhausted expression, hand clinging to sword, Mediterranean complexion",
    "mighty-sham": "Shammah son of Agee, bronze age Levantine mighty man, strong build, dark hair, linen tunic with leather armor, bronze spear held ready, standing in defensive stance, weathered devoted expression, Mediterranean complexion",
    "mighty-abishai": "Abishai son of Zeruiah, bronze age Levantine mighty man, tall strong build, dark hair, linen tunic with leather vest, brown cloak, bronze spear raised high, fierce battle expression, leading attack, Mediterranean complexion",
    "mighty-benaiah": "Benaiah son of Jehoiada, bronze age Levantine mighty man, strong build, dark hair, linen tunic with leather vest, brown cloak, bronze sword in hand, lion pelt over one shoulder, brave legendary expression, Mediterranean complexion",
    "elhanan": "Elhanan the Bethlehemite, bronze age Levantine mighty man, strong build, dark hair, linen tunic with leather vest, bronze spear, small shield, determined expression, gazing at fallen giant, Mediterranean complexion",
    "sibbecai": "Sibbecai the Hushathite, bronze age Levantine mighty man, strong build, dark hair, linen tunic with leather armor, bronze spear raised, victorious expression, standing over defeated enemy, Mediterranean complexion",
}

# Card prompts from PROMPTS.md
card_prompts = {}
card_pattern = re.finditer(
    r'\| \*\*(Jonathan Precision|Joab Assault|Amasa Rally|Asahel Flank|Philistine Charge|Goliath Challenge|Amalekite Raid)\*\* \| `([^`]+)` \|',
    prompts_md
)
for m in card_pattern:
    key_map = {
        "Jonathan Precision": "jonathan-precision",
        "Joab Assault": "joab-assault",
        "Amasa Rally": "amasa-rally",
        "Asahel Flank": "asahel-flank",
        "Philistine Charge": "philistine-charge",
        "Goliath Challenge": "goliath-challenge",
        "Amalekite Raid": "amalekite-raid",
    }
    key = key_map.get(m.group(1))
    if key:
        card_prompts[key] = m.group(2).strip()

# Build all new prompts
new_prompts = {}
missing = needed_keys - set(existing_prompts.keys())

for k in missing:
    if k in box_art_prompts:
        new_prompts[k] = box_art_prompts[k]
    elif k in portrait_prompts:
        new_prompts[k] = portrait_prompts[k]
    elif k in card_prompts:
        new_prompts[k] = card_prompts[k]
    elif k in tile_prompts:
        new_prompts[k] = tile_prompts[k]
    elif k in ui_prompts:
        new_prompts[k] = ui_prompts[k]
    elif k in character_descriptions:
        new_prompts[k] = CHARACTER_TEMPLATE.format(description=character_descriptions[k])

# Handle hp-bar aliases
if "hp-bar-bg" in missing:
    new_prompts["hp-bar-bg"] = existing_prompts.get("hp_bar_bg", "")
if "hp-bar-fill" in missing:
    new_prompts["hp-bar-fill"] = existing_prompts.get("hp_bar_fill", "")

print(f"New prompts to add: {len(new_prompts)}")
still_missing = missing - set(new_prompts.keys())
print(f"Still missing after generation: {len(still_missing)}")
for k in sorted(still_missing):
    print(f"  {k}")

# Now add the new prompts to review_art_ollama.py
# Find the closing brace of EXPECTED_PROMPTS dict
closing_line = None
for i in range(len(lines) - 1, -1, -1):
    if lines[i].strip() == "}" and i > 21:
        # Make sure this is the dict closing, not another function's
        context = "".join(lines[max(0, i-5):i+1])
        if "EXPECTED_PROMPTS" in context or "hex_sand" in context or "sand" in context:
            closing_line = i
            break

if closing_line is None:
    # Fallback: find the line with just "}" after the hex_sand entry
    for i in range(95, len(lines)):
        if lines[i].strip() == "}" and "hex_" in "".join(lines[max(0,i-20):i]):
            closing_line = i
            break

print(f"Found closing brace at line {closing_line + 1}")

# Build new lines to insert
new_lines = []
for k, v in sorted(new_prompts.items()):
    # Escape any backslashes and quotes in the value
    escaped_v = v.replace("\\", "\\\\").replace('"', '\\"')
    new_lines.append(f'    "{k}": "{escaped_v}",\n')

# Insert new lines before closing brace
lines = lines[:closing_line] + new_lines + lines[closing_line:]

# Write back
with open(f"{PROJECT_ROOT}/review_art_ollama.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print(f"Updated review_art_ollama.py with {len(new_prompts)} new prompts")

# Save extracted prompts for verification
with open(f"{PROJECT_ROOT}/new_prompts.json", "w", encoding="utf-8") as f:
    json.dump(new_prompts, f, indent=2, ensure_ascii=False)

print("Done!")

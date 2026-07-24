"""
Rebuild EXPECTED_PROMPTS completely with all 151 needed prompts.
"""
import json
import re

with open("review_art_ollama.py", "r", encoding="utf-8") as f:
    content = f.read()
    lines = content.splitlines(keepends=True)

with open("generation_queue.json", "r") as f:
    queue = json.load(f)

needed_keys = set()
for item in queue:
    pk = item.get("prompt_key", "")
    if pk:
        needed_keys.add(pk)

print(f"Needed keys: {len(needed_keys)}")

# Find EXPECTED_PROMPTS block boundaries
block_start = None
block_end = None
for i, line in enumerate(lines):
    if "EXPECTED_PROMPTS = {" in line:
        block_start = i
    if block_start and line.strip() == "}" and i > block_start:
        context = "".join(lines[block_start:i+1])
        if context.count("{") == context.count("}"):
            block_end = i
            break

print(f"EXPECTED_PROMPTS block: lines {block_start+1} to {block_end+1}")

# Extract current prompts from the block
block_text = "".join(lines[block_start:block_end+1])
existing = {}
for m in re.finditer(r'"([^"]+)":\s*"([^"]*)"', block_text):
    existing[m.group(1)] = m.group(2)

# Handle parenthesized strings
for m in re.finditer(r'"([^"]+)":\s*\(', block_text):
    key = m.group(1)
    start_pos = m.end()
    content_start = None
    content_end = None
    for i in range(start_pos, len(block_text)):
        if block_text[i] == '"' and content_start is None:
            content_start = i + 1
        elif block_text[i] == '"' and content_start is not None and content_end is None:
            content_end = i
            break
    if content_start and content_end:
        val = block_text[content_start:content_end]
        existing[key] = val

print(f"Existing prompts: {len(existing)}")
print(f"Needed keys: {len(needed_keys)}")
missing = needed_keys - set(existing.keys())
print(f"Missing keys: {len(missing)}")

# We need to add all missing keys. Build the complete new dict text.
# IMPORTANT: The original file has some multi-line parenthesized string values.
# We need to preserve those for the original 48 entries, and add new entries as single-line strings.

# Strategy: Replace the ENTIRE EXPECTED_PROMPTS block
match = re.search(r'EXPECTED_PROMPTS = \{(.*?)\n\}\n\n', content, re.DOTALL)
if not match:
    print("ERROR: Could not find EXPECTED_PROMPTS block")
    exit(1)

old_block = match.group(0)
print(f"Found EXPECTED_PROMPTS block, length: {len(old_block)}")

# Build all prompts
# Copy all from existing + add new ones
all_prompts = dict(existing)

# Add missing prompts from various sources

# 1. Portraits not in existing
portraits = {
    "abigail": "ONE PERSON ONLY, solo portrait, waist-up, Abigail wife of Nabal, bronze age Levantine noblewoman, dark hair in woven braids, rich but practical woolen tunic in faded blue, leather belt, small knife at waist, face showing intelligence and caution, standing with a loaded donkey behind her, laden with gifts, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "benjamin-spearman": "ONE PERSON ONLY, solo portrait, waist-up, Benjamite spearman of Jonathan's guard, bronze age Levantine elite infantry, strong fierce build, dark hair, white linen tunic with leather shoulder guards, brown cloak wrapped and fastened, long wooden spear with bronze tip held upright, small hide shield at side, leather cord belt with knife, alert loyal expression, standing in disciplined formation, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "judah-militia": "ONE PERSON ONLY, solo portrait, waist-up, Judah militia defender, bronze age Levantine village warrior, sturdy build, dark hair, simple linen tunic with leather vest, brown wool cloak, bronze short sword in hand, small round hide shield, leather sandals, determined local expression, leaning on spear in resting pose, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "nabal": "ONE PERSON ONLY, solo portrait, waist-up, Nabal the Carmelite, bronze age Levantine wealthy landowner, heavyset build, dark hair and short beard, rich woolen tunic with woven border, bronze rings on fingers, bronze short sword at hip, expression of stubborn pride, seated on a low stool with a wine cup in hand, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "priest-of-nob": "ONE PERSON ONLY, solo portrait, waist-up, priest of Nob, bronze age Levantine priest, older man, white linen ephod over simple tunic, bronze plate on chest with Urim and Thummim, short beard, kind eyes, holding a loaf of showbread, standing before a stone altar, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
}

# 2. Round 3 box art
round3_boxart = {
    "box-art-round3-david-as-king": "game box art, painting in illuminated manuscript style, David crowned at Hebron, elder standing before him with a horn of oil, olive trees and stone walls in background, autumn golden light, his captains behind him, composition is kingship earned through hardship, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-round3-david-at-adullam": "game box art, painting in illuminated manuscript style, David seated at the entrance of a cave at Adullam, surrounded by a ragtag band of outcasts and warriors, one man sharpening a spear, another mending a cloak, warm firelight against dark rock, composition is intimate and raw, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-round3-jonathan-and-david": "game box art, painting in illuminated manuscript style, Jonathan and David standing on a hilltop at Mizpah, Jonathan taking off his robe and giving it to David along with his weapons, wind blowing the fabric between them, golden light, composition is tender and covenant-making, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-round3-the-cave-of-engedi": "game box art, painting in illuminated manuscript style, inside the dark cave at Ein Gedi, David standing in the shadows near Saul who is sleeping, Saul's robe spread wide at the entrance, David's hand hovering near the hem deciding whether to strike, torchlight flickering, composition is the moment of mercy, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-round3-the-wounded-david": "game box art, painting in illuminated manuscript style, David lying wounded and exhausted on a rocky hillside, his armor scattered, a single warrior kneeling beside him offering water, dark storm clouds above, composition is vulnerability and trust, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded indigo, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
}

# 3. Aliases for inconsistent naming
aliases = {}
for key in ["camel-rider_amalekite", "chieftain_amalekite", "raider_amalekite", "reward-panel"]:
    lookup = key.replace("-", "_")
    pattern = '"' + lookup + '":\\s*"([^"]*)"'
    m = re.search(pattern, content)
    if m:
        aliases[key] = m.group(1)

# 4. All other missing character prompts
character_descriptions = {
    "saul": "ONE PERSON ONLY, solo portrait, waist-up, Saul king of Israel, bronze age Levantine monarch, tall commanding presence, dark hair and short beard, rich purple-blue wool cloak over linen tunic, bronze chest plate with simple geometric engraving, bronze short sword at hip, leather sandals, stern authoritative expression, standing with regal bearing, Mediterranean complexion",
    "abner": "ONE PERSON ONLY, solo portrait, waist-up, Abner commander of Saul's army, bronze age Levantine military leader, strong build, dark hair and beard, leather vest over linen tunic, brown wool cloak, bronze spear in hand, hardened battle expression, alert posture, standing on rocky ground, Mediterranean complexion",
    "royal-guard": "ONE PERSON ONLY, solo portrait, waist-up, Israelite royal guard, bronze age Levantine elite infantryman, dark hair, white linen tunic with woven border, leather vest, brown wool cloak pinned at shoulder, bronze short sword, small round hide shield, loyal disciplined expression, standing at attention, Mediterranean complexion",
    "benjamite-spearman": "ONE PERSON ONLY, solo portrait, waist-up, Benjamite spearman of Jonathan's guard, bronze age Levantine elite infantry, strong fierce build, dark hair, white linen tunic with leather shoulder guards, brown cloak wrapped and fastened, long wooden spear with bronze tip held upright, small hide shield at side, leather cord belt with knife, alert loyal expression, standing in disciplined formation, Mediterranean complexion",
    "israelite-archer": "ONE PERSON ONLY, solo portrait, waist-up, Israelite archer of Saul's army, bronze age Levantine archer, dark hair, simple linen tunic with leather vest, brown cloak, short composite bow in hand with arrow nocked, quiver on back, knife at waist, focused expression, standing ready, Mediterranean complexion",
    "officer": "ONE PERSON ONLY, solo portrait, waist-up, Israelite army officer, bronze age Levantine military commander, dark hair and short beard, linen tunic with leather vest, brown wool cloak, bronze short sword at hip, bronze spear in hand, authoritative expression, standing with command presence, Mediterranean complexion",
    "elite-bodyguard": "ONE PERSON ONLY, solo portrait, waist-up, Israelite elite bodyguard, bronze age Levantine royal protector, dark hair, well-fitted linen tunic with leather armor, brown cloak, large hide shield, bronze short sword, alert protective stance, loyal expression, standing ready to defend, Mediterranean complexion",
    "jonathan": "ONE PERSON ONLY, solo portrait, waist-up, Jonathan son of Saul, bronze age Levantine prince and warrior, dark hair, handsome features, rich blue-purple cloak over linen tunic, leather vest, composite bow in hand, quiver on back, bronze short sword at hip, noble brave expression, standing confidently, Mediterranean complexion",
    "loyal-guard": "ONE PERSON ONLY, solo portrait, waist-up, Loyal guard of Jonathan, bronze age Levantine elite warrior, dark hair, white linen tunic with dark border, leather vest, brown cloak, spear in hand, small shield, devoted alert expression, standing beside commander, Mediterranean complexion",
    "elite-archer": "ONE PERSON ONLY, solo portrait, waist-up, Elite archer of Jonathan's guard, bronze age Levantine master archer, dark hair, fitted linen tunic, leather bracers, brown cloak, composite bow drawn with arrow nocked, quiver, focused precise expression, Mediterranean complexion",
    "jonathan-armor-bearer": "ONE PERSON ONLY, solo portrait, waist-up, Jonathan's armor-bearer, bronze age Levantine elite warrior, dark hair, linen tunic with leather vest, brown cloak, bronze spear, shield at side, loyal brave expression, standing ready, Mediterranean complexion",
    "jonathan-shield-bearer": "ONE PERSON ONLY, solo portrait, waist-up, Jonathan's shield-bearer, bronze age Levantine warrior, dark hair, strong build, linen tunic with leather armor, large round hide shield held high, bronze sword at hip, protective stance, determined expression, Mediterranean complexion",
    "jonathan-spearman": "ONE PERSON ONLY, solo portrait, waist-up, Jonathan's spearman guard, bronze age Levantine Benjamite warrior, dark hair, white linen tunic with leather shoulder guards, brown cloak wrapped, long spear with bronze tip held upright, small shield, alert disciplined expression, Mediterranean complexion",
    "joab": "ONE PERSON ONLY, solo portrait, waist-up, Joab commander of David's army, bronze age Levantine general, tall strong build, gray-streaked beard, dark hair, leather scale armor over linen tunic, brown cloak, bronze spear raised, ruthless brilliant expression, battle-scarred, Mediterranean complexion",
    "amasa": "ONE PERSON ONLY, solo portrait, waist-up, Amasa captain of Judah, bronze age Levantine commander, honest earnest expression, dark hair and beard, linen tunic with leather vest, brown cloak, bronze spear in hand, appointed captain bearing, standing with quiet authority, Mediterranean complexion",
    "asahel": "ONE PERSON ONLY, solo portrait, waist-up, Asahel son of Zeruiah, bronze age Levantine runner warrior, lean swift build, dark hair, light linen tunic with leather vest, wrapped cloak for swift movement, short sword raised, running stance, focused expression, Mediterranean complexion",
    "achish": "ONE PERSON ONLY, solo portrait, waist-up, Achish lord of Gath, bronze age Levantine Philistine ruler, dark hair, rich purple cloak over linen tunic, bronze chest plate, bronze sword at hip, stern unreadable expression, seated authority, Mediterranean complexion",
    "philistine-lord": "ONE PERSON ONLY, solo portrait, waist-up, Philistine lord, bronze age Levantine city-state ruler, dark hair, rich embroidered tunic, bronze scale armor, purple cloak, bronze sword, authoritative expression, standing with regal bearing, Mediterranean complexion",
    "philistine-spearman": "ONE PERSON ONLY, solo portrait, waist-up, Philistine spearman, bronze age Levantine infantry, dark hair, linen tunic with leather vest, large rectangular shield, long bronze-tipped spear, bronze helmet, steady formation stance, Mediterranean complexion",
    "philistine-heavy": "ONE PERSON ONLY, solo portrait, waist-up, Philistine heavy infantry, bronze age Levantine warrior, large build, dark hair, linen tunic with bronze scale armor, large hide-covered shield with bronze rim, long spear, bronze short sword, imposing slow stance, Mediterranean complexion",
    "philistine-archer": "ONE PERSON ONLY, solo portrait, waist-up, Philistine archer, bronze age Levantine archer, dark hair, simple tunic with leather vest, short bow drawn, quiver on back, sharp eyes, focused expression, standing ready, Mediterranean complexion",
    "philistine-charioteer": "ONE PERSON ONLY, solo portrait, waist-up, Philistine charioteer, bronze age Levantine warrior, dark hair, linen tunic with leather armor, brown cloak flowing, standing beside bronze-rimmed chariot, spear in hand, weathered determined expression, Mediterranean complexion",
    "philistine-champion": "ONE PERSON ONLY, solo portrait, waist-up, Philistine champion, bronze age Levantine elite warrior, dark hair, decorated tunic, bronze scale armor, large shield, spear raised, confident duelist expression, standing in challenge pose, Mediterranean complexion",
    "goliath": "ONE PERSON ONLY, solo portrait, waist-up, Goliath the Gittite, bronze age Levantine giant champion, enormous build, dark hair and beard, elaborate tunic, bronze scale armor, large bronze shield, massive bronze-tipped spear like a weaver's beam, jawset expression, towering menacing figure, Mediterranean complexion",
    "lahmi": "ONE PERSON ONLY, solo portrait, waist-up, Lahmi the giant, bronze age Levantine Rephaim warrior, enormous build, dark hair, simple tunic, bronze spear, fierce expression, towering figure, Mediterranean complexion",
    "saph": "ONE PERSON ONLY, solo portrait, waist-up, Saph the giant, bronze age Levantine Rephaim warrior, enormous build, dark hair, worn tunic, large shield, bronze sword, threatening expression, Mediterranean complexion",
    "girzite-chief": "ONE PERSON ONLY, solo portrait, waist-up, Girzite chief, bronze age Levantine desert clan leader, dark windblown hair, weathered face, dusty brown cloak wrapped around, leather tunic, bronze spear in hand, bronze short sword at hip, authoritative scorched expression, Mediterranean complexion",
    "girzite-raider": "ONE PERSON ONLY, solo portrait, waist-up, Girzite raider, bronze age Levantine desert skirmisher, dark windblown hair, lean weathered face, dusty brown cloak, leather tunic, javelin in hand, leather sling, hardened expression, alert stance, Mediterranean complexion",
    "girzite-scout": "ONE PERSON ONLY, solo portrait, waist-up, Girzite scout, bronze age Levantine desert tracker, lean dark-haired man, dusty brown cloak patched, short javelin, sling at belt, small shield, sharp alert eyes scanning horizon, Mediterranean complexion",
    "girzite-shepherd-raider": "ONE PERSON ONLY, solo portrait, waist-up, Girzite shepherd-raider, bronze age Levantine desert warrior, lean build, dark windblown hair, dusty brown cloak, leather vest, sling at belt, short spear, shepherd's crook leaning nearby, weathered expression, Mediterranean complexion",
    "geshurite-archer": "ONE PERSON ONLY, solo portrait, waist-up, Geshurite archer, bronze age Levantine desert archer, dark hair, linen tunic with leather vest, dusty brown cloak, short composite bow drawn with arrow, quiver on back, sharp focused expression, standing on rocky desert ground, Mediterranean complexion",
    "geshurite-spearman": "ONE PERSON ONLY, solo portrait, waist-up, Geshurite spearman, bronze age Levantine infantry, dark hair, linen tunic with leather shoulder piece, brown cloak, long wooden spear with bronze tip held in both hands, small hide shield, determined expression, Mediterranean complexion",
    "geshurite-camel-rider": "ONE PERSON ONLY, solo portrait, waist-up, Geshurite camel rider, bronze age Levantine desert warrior, dark hair, dusty brown cloak and headwrap, bronze-tipped spear held upright, riding tall dromedary camel, leather reins in hand, weathered expression, Mediterranean complexion",
    "geshurite-clansman": "ONE PERSON ONLY, solo portrait, waist-up, Geshurite clansman, bronze age Levantine tribal warrior, dark hair, linen tunic with leather vest, worn brown cloak, bronze short sword, sling at belt, small knife, alert expression, Mediterranean complexion",
    "gezerite-defender": "ONE PERSON ONLY, solo portrait, waist-up, Gezerite defender, bronze age Levantine Canaanite warrior, dark hair, sturdy build, linen tunic with leather shoulder armor, round hide shield, bronze spear, determined defensive expression, standing firm, Mediterranean complexion",
    "gezerite-archer": "ONE PERSON ONLY, solo portrait, waist-up, Gezerite archer, bronze age Levantine Canaanite archer, dark hair, linen tunic, leather vest, short composite bow drawn, quiver on back, sharp eyes, focused expression, Mediterranean complexion",
    "gezerite-scout": "ONE PERSON ONLY, solo portrait, waist-up, Gezerite scout, bronze age Levantine tracker, lean dark-haired man, linen tunic with leather vest, worn cloak, short javelin, sling at belt, alert watchful expression, scanning horizon, Mediterranean complexion",
    "mighty-josheb-basshebeth": "ONE PERSON ONLY, solo portrait, waist-up, Josheb-basshebeth the Tachmonite, bronze age Levantine mighty man, powerful build, dark hair and beard, bronze scale armor over linen tunic, brown cloak, massive bronze spear held upright, fierce legendary expression, standing with enormous weapon, Mediterranean complexion",
    "mighty-eleazar": "ONE PERSON ONLY, solo portrait, waist-up, Eleazar son of Dodai, bronze age Levantine mighty man, strong fierce build, dark hair and beard, linen tunic with leather vest, bronze spear raised, small round shield, determined exhausted expression, hand clinging to sword, Mediterranean complexion",
    "mighty-sham": "ONE PERSON ONLY, solo portrait, waist-up, Shammah son of Agee, bronze age Levantine mighty man, strong build, dark hair, linen tunic with leather armor, bronze spear held ready, standing in defensive stance, weathered devoted expression, Mediterranean complexion",
    "mighty-abishai": "ONE PERSON ONLY, solo portrait, waist-up, Abishai son of Zeruiah, bronze age Levantine mighty man, tall strong build, dark hair, linen tunic with leather vest, brown cloak, bronze spear raised high, fierce battle expression, leading attack, Mediterranean complexion",
    "mighty-benaiah": "ONE PERSON ONLY, solo portrait, waist-up, Benaiah son of Jehoiada, bronze age Levantine mighty man, strong build, dark hair, linen tunic with leather vest, brown cloak, bronze sword in hand, lion pelt over one shoulder, brave legendary expression, Mediterranean complexion",
    "elhanan": "ONE PERSON ONLY, solo portrait, waist-up, Elhanan the Bethlehemite, bronze age Levantine mighty man, strong build, dark hair, linen tunic with leather vest, bronze spear, small shield, determined expression, gazing at fallen giant, Mediterranean complexion",
    "sibbecai": "ONE PERSON ONLY, solo portrait, waist-up, Sibbecai the Hushathite, bronze age Levantine mighty man, strong build, dark hair, linen tunic with leather armor, bronze spear raised, victorious expression, standing over defeated enemy, Mediterranean complexion",
}

# Card prompts not in existing
card_prompts = {
    "jonathan-precision": "ONE PERSON ONLY, scene in illuminated manuscript style, Jonathan son of Saul drawing his composite bow, arrow aimed, two Israelite archers beside him, aged parchment background, ink outlines with muted watercolor wash in ochre and faded gold, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "joab-assault": "ONE PERSON ONLY, scene in illuminated manuscript style, Joab son of Zeruiah leading a fierce charge, bronze spear raised, Israelite warriors behind him, aged parchment background, ink outlines with muted watercolor wash in ochre and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "amasa-rally": "ONE PERSON ONLY, scene in illuminated manuscript style, Amasa son of Jether rallying troops with hand raised, bronze spear in other hand, soldiers gathering around, aged parchment background, ink outlines with muted watercolor wash in ochre and amber, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "asahel-flank": "ONE PERSON ONLY, scene in illuminated manuscript style, Asahel son of Zeruiah running with incredible speed, short sword raised, dust rising at his feet, single runner outrunning formation, aged parchment background, ink outlines with muted watercolor wash in umber and faded gold, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "philistine-charge": "ONE PERSON ONLY, scene in illuminated manuscript style, Philistine heavy infantry advancing in formation, large shields locked, spears angled forward, dust and determination, aged parchment background, ink outlines with muted watercolor wash in umber ochre and faded indigo, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "goliath-challenge": "ONE PERSON ONLY, scene in illuminated manuscript style, Goliath the Gittite standing immense with spear like a weaver's beam, small figure of David opposite him, bronze shields, dust rising, aged parchment background, ink outlines with muted watercolor wash in umber and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "amalekite-raid": "ONE PERSON ONLY, scene in illuminated manuscript style, Amalekite raiders on camel and foot sweeping through a settlement, spears raised, dust clouds, civilians fleeing, aged parchment background, ink outlines with muted watercolor wash in ochre umber and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
}

# Tile prompts
tile_prompts = {
    "hex-tile-desert-night": "top-down flat hex tile, desert at night, cool blue-gray under moonlight, subtle stars, watercolor wash, board game style, seamless, 512x512",
    "hex-tile-stone-path": "top-down flat hex tile, ancient stone path and packed earth, gray-brown, ink wash texture, board game style, seamless, 512x512",
    "hex-tile-ruins": "top-down flat hex tile, broken stone walls and rubble, weathered umber, watercolor and ink wash, board game style, seamless, 512x512",
}

# UI prompts
ui_prompts = {
    "ui-portrait-frame": "ornate rectangular frame for character portrait, aged parchment with dark ink border, corner ornaments, board game UI element, hand-painted illustration, transparent background, NOT medieval, NOT fantasy, NOT European",
    "ui-card-slot": "empty card slot on table, aged parchment background, wooden card border, board game UI element, transparent background, hand-painted illustration, NOT medieval, NOT fantasy, NOT European",
    "ui-commander-aura": "soft glowing circle on ground, commander presence area, warm golden light, board game UI element, transparent background, hand-painted illustration, NOT medieval, NOT fantasy, NOT European",
}

# Combine all
all_new_prompts = {}
all_new_prompts.update(portraits)
all_new_prompts.update(round3_boxart)
all_new_prompts.update(aliases)
all_new_prompts.update(character_descriptions)
all_new_prompts.update(card_prompts)
all_new_prompts.update(tile_prompts)
all_new_prompts.update(ui_prompts)

# Filter to only missing keys
filtered = {k: v for k, v in all_new_prompts.items() if k in missing}
print(f"Total new prompts to add: {len(filtered)}")

still_missing = missing - set(filtered.keys())
print(f"Still missing (no prompt available): {len(still_missing)}")
for k in sorted(still_missing):
    print(f"  {k}")

# Build replacement block
# We need to preserve the original format for existing entries
# and add new entries as single-line strings at the end before }

# Extract the existing block lines
existing_block_lines = lines[block_start:block_end+1]

# Insert new entries before the last line (})
new_entries_lines = []
for key in sorted(filtered.keys()):
    val = filtered[key]
    escaped = val.replace("\\", "\\\\").replace('"', '\\"')
    new_entries_lines.append(f'    "{key}": "{escaped}",\n')

replacement = existing_block_lines[:-1] + new_entries_lines + [existing_block_lines[-1]]

new_content = "".join(lines[:block_start] + replacement + lines[block_end+1:])

with open("review_art_ollama.py", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Wrote updated review_art_ollama.py")

# Final syntax check
try:
    compile(new_content, "review_art_ollama.py", "exec")
    print("Syntax check: PASSED")
except SyntaxError as e:
    print(f"Syntax error: {e}")

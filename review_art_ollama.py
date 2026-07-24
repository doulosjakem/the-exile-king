"""
Batch art review using Ollama minicpm-v:8b with subject-agnostic checklist.
Reviews all images in output folder and outputs a JSON report.
Auto-moves TRASH candidates to to_trash/ (but keeps KEEP files in place).
Stage 1: dedupe via aHash. Stage 2: quality + anatomical + prompt-match review.
"""
import argparse
import json
import os
import sys
import time
import base64
import urllib.request
import urllib.error
import re
import shutil

from PIL import Image

OLLAMA_URL = "http://localhost:11434/api/generate"

EXPECTED_PROMPTS = {
    # Unit Standees
    "token_david": "board game standee, single full upright figure from head to toe standing on a small circular base disc, hand-painted ink and watercolor illustration, a young bronze age Levantine man, bronze age Israelite, dark curly hair and short beard, simple linen tunic with leather chest piece, brown wool cloak pinned at shoulder, bronze short sword at hip, leather sling in belt, no helmet, sandals, Mediterranean complexion, dark ink outlines, full color, transparent background, centered, NOT medieval, NOT fantasy, NOT European, family friendly",
    "token_swordsman": "board game standee, single full upright figure from head to toe standing on a small circular base disc, hand-painted ink and watercolor illustration, a bronze age Levantine infantryman, bronze age Israelite warrior, dark hair, short beard, simple linen tunic, leather vest, brown wool cloak, small round hide-covered shield on arm, bronze short sword with leaf-shaped blade, sandals, Mediterranean features, dark ink outlines, full color, transparent background, centered, NOT medieval, NOT fantasy, NOT European, family friendly",
    "token_spearman": "board game standee, single full upright figure from head to toe standing on a small circular base disc, hand-painted ink and watercolor illustration, a bronze age Levantine spearman, bronze age Israelite, dark hair, linen tunic with leather shoulder piece, long wooden spear with bronze tip held in both hands, small hide shield on back, knife at waist, sandals, Mediterranean features, dark ink outlines, full color, transparent background, centered, NOT medieval, NOT fantasy, NOT European, family friendly",
    "token_slinger": "board game standee, single full upright figure from head to toe standing on a small circular base disc, hand-painted ink and watercolor illustration, a bronze age Levantine skirmisher, bronze age Israelite slinger, dark hair, linen tunic with leather vest, leather sling raised overhead, pouch of stones at hip, small knife, light ready stance, sandals, alert expression, dark ink outlines, full color, transparent background, centered, NOT medieval, NOT fantasy, NOT European, family friendly",
    "token_archer": "board game standee, single full upright figure from head to toe standing on a small circular base disc, hand-painted ink and watercolor illustration, a bronze age Levantine archer, bronze age Israelite hunter, dark hair, linen tunic, leather vest, short composite bow drawn with arrow nocked, quiver on back, knife at waist, sandals, dark ink outlines, full color, transparent background, centered, NOT medieval, NOT fantasy, NOT European, family friendly",
    "token_scout": "board game standee, single full upright figure from head to toe standing on a small circular base disc, hand-painted ink and watercolor illustration, a lean bronze age Levantine scout, bronze age Israelite tracker, dark hair, light linen tunic, leather vest, worn brown cloak, sling at belt, short spear, small hide shield on back, knife, alert watchful expression, sandals, dark ink outlines, full color, transparent background, centered, NOT medieval, NOT fantasy, NOT European, family friendly",
    "token_chieftain_amalekite": "board game standee, single full upright figure from head to toe standing on a small circular base disc, hand-painted ink and watercolor illustration, a bronze age Levantine warlord, dark red-brown wrapped headdress, dark beard, leather and simple bronze chest piece, bronze short sword at hip, spear in hand, weathered authoritative face, dark ink outlines, full color, transparent background, centered, NOT medieval, NOT fantasy, NOT European, family friendly",
    "token_raider_amalekite": "board game standee, single full upright figure from head to toe standing on a small circular base disc, hand-painted ink and watercolor illustration, a bronze age Levantine desert raider, dark windblown hair, weathered lean face, dusty red-brown wool cloak wrapped around body, leather tunic, bronze-tipped spear, curved knife at belt, sandals, hardened expression, dark ink outlines, full color, transparent background, centered, NOT medieval, NOT fantasy, NOT European, family friendly",
    "token_refugee": "board game standee, single full upright figure from head to toe standing on a small circular base disc, hand-painted ink and watercolor illustration, a bronze age Levantine civilian, simple linen tunic, worn brown cloak, bundle on stick over shoulder, sandals, weary but hopeful expression, no weapons, dark ink outlines, full color, transparent background, centered, NOT medieval, NOT fantasy, NOT European, family friendly",
    # Unit Portraits
    "david": "ONE PERSON ONLY, solo portrait, waist-up, young bronze age Israelite commander, bronze age Levantine man, dark curly hair and trimmed beard, simple linen tunic with leather chest piece, brown wool cloak pinned at shoulder with bronze brooch, bronze short sword at hip, leather sling tucked in belt, shepherd's staff in hand, determined watchful expression, standing on rocky Judean hillside under overcast sky, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "swordsman": "ONE PERSON ONLY, solo portrait, waist-up, young bronze age Israelite swordsman, bronze age Levantine warrior, dark hair and short beard, simple linen tunic with layered leather vest, worn brown wool cloak pinned at shoulder, bronze short sword with leaf-shaped blade in hand, small round hide-covered shield on arm, leather wrapped grip, sandals, alert expression, standing on rocky Judean ground, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European",
    "spearman": "ONE PERSON ONLY, solo portrait, waist-up, young bronze age Israelite spearman, bronze age Levantine warrior, dark hair, linen tunic with leather shoulder piece, brown cloak tied at neck, long wooden spear with bronze tip held in both hands, small hide shield slung across back, knife at waist, sandals, focused expression, standing on hillside overlooking wilderness valleys, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European",
    "slinger": "ONE PERSON ONLY, solo portrait, waist-up, young bronze age Israelite slinger, bronze age Levantine skirmisher, dark hair, simple linen tunic with leather vest, worn brown cloak, leather sling in hand with pouch at belt, pouch of smooth stones at hip, small knife, crouched lightly ready to pivot and throw, alert watchful expression, standing on rocky slope, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European",
    "archer": "ONE PERSON ONLY, solo portrait, waist-up, young bronze age Israelite archer, bronze age Levantine hunter, dark hair, simple linen tunic with leather vest, brown cloak, short composite bow in hand with arrow nocked, quiver of arrows slung across back, knife at waist, sandals, drawing bow with focused precision, standing on ridge overlooking valleys, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European",
    "scout": "ONE PERSON ONLY, solo portrait, waist-up, young bronze age Israelite scout, bronze age Levantine tracker, lean shepherd-skirmisher, dark hair, simple linen tunic with leather vest, worn brown cloak, sandals, sling at belt, short spear, small hide shield on back, knife at waist, alert watchful expression, standing lightly on rocky Judean hillside, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European",
    # Enemy Portraits
    "raider": "ONE PERSON ONLY, solo portrait, waist-up, Amalekite raider, bronze age Levantine nomadic desert warrior, dark windblown hair, weathered lean face, dusty red-brown wool cloak wrapped around body, leather tunic underneath, bronze-tipped spear in hand, curved knife at belt, hardened squinting expression, standing on sandy desert ground with rocky outcrops, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European",
    "chieftain": "ONE PERSON ONLY, solo portrait, waist-up, Amalekite chieftain, bronze age Levantine nomadic warlord, dark hair and gray-streaked beard, dark red-brown wool cloak trimmed with rough fringe, leather and simple bronze chest piece, weathered authoritative face, bronze short sword at hip, spear in hand, wrapped headdress, standing on rocky outcrop overlooking warriors, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European",
    "slinger_amalekite": "ONE PERSON ONLY, solo portrait, waist-up, Amalekite slinger, bronze age Levantine nomadic skirmisher, dark hair, dusty red-brown cloak wrapped loose, leather sling in hand with pouch of stones at hip, simple leather tunic, sandals, crouched low in mobile throwing stance, alert predatory expression, standing on sandy desert terrain, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European",
    "archer_amalekite": "ONE PERSON ONLY, solo portrait, waist-up, Amalekite mounted archer, bronze age Levantine nomadic horseman, dark hair, dusty red-brown cloak flowing, riding small hardy desert horse, composite bow drawn with arrow aimed, quiver strapped to horse flank, weathered focused expression, horse mid-stride on open desert plain, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European",
    "scout_amalekite": "ONE PERSON ONLY, solo portrait, waist-up, Amalekite scout, bronze age Levantine desert tracker, lean wind-hardened build, dark hair, dusty red-brown cloak patched and worn, short javelin in hand, leather sling at belt, small hide shield on back, sandals, crouched and scanning horizon, keen narrowed eyes, standing on rocky desert ridge, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European",
    "camel_rider_amalekite": "ONE PERSON ONLY, solo portrait, waist-up, Amalekite camel rider, bronze age Levantine desert warrior, dark hair, dusty red-brown cloak and headwrap, bronze-tipped spear held upright, riding tall dromedary camel, leather reins in hand, weathered stern expression, camel standing on sandy desert ground with distant mountains, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European",
    # Command Cards
    "swordsmen-advance": "scene in illuminated manuscript style, two bronze age Levantine Israelite swordsmen advancing in formation, bronze short swords raised, hide shields overlapping, dust at their heels, linen tunics and leather vests, determined expressions, aged parchment background, ink outlines with muted watercolor wash in ochre and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare",
    "archer-volley": "scene in illuminated manuscript style, two bronze age Levantine Israelite archers on ridge aiming forward, composite bows drawn, arrows ready to loose, linen tunics, leather arm bracers, quivers on backs, aged parchment background, ink outlines with muted watercolor wash in ochre and faded ochre, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European",
    "spear-wall": "scene in illuminated manuscript style, three bronze age Levantine Israelite spearmen in tight formation, long wooden spears with bronze tips angled outward, shields locked, braced defensive stance, linen tunics, leather armor, grim expressions, aged parchment background, ink outlines with muted watercolor wash in umber and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European",
    "slinger-skirmish": "scene in illuminated manuscript style, two bronze age Levantine Israelite slingers in skirmish formation, leather slings raised, stones in pouches, light armor, crouched mobile stances, alert expressions, aged parchment background, ink outlines with muted watercolor wash in ochre and umber, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European",
    "scout-recon": "scene in illuminated manuscript style, two bronze age Levantine Israelite scouts moving swiftly through rocky terrain, light clothing, scanning horizon, short spears and slings, alert watchful expressions, aged parchment background, ink outlines with muted watercolor wash in ochre and faded ochre, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European",
    "refugee-aid": "scene in illuminated manuscript style, bronze age Levantine civilians being tended to by a soldier, simple linen tunics, worn cloaks, one soldier offering water, lean-to shelter in background, compassionate expressions, aged parchment background, ink outlines with muted watercolor wash in ochre and brown, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European",
    "davids-leadership": "scene in illuminated manuscript style, bronze age Levantine Israelite commander on rocky outcrop with arm raised rallying men, soldiers gathered below looking up, simple cloth banner on wooden pole, linen tunics, leather armor, wool cloaks, aged parchment background, ink outlines with muted watercolor wash in ochre and brown, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European",
    "march": "scene in illuminated manuscript style, bronze age Levantine Israelite soldiers marching in organized column across dusty ground, spears and shields at sides, linen tunics and leather vests, brown wool cloaks, steady pace, aged parchment background, ink outlines with muted watercolor wash in ochre and umber, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European",
    "engage": "scene in illuminated manuscript style, bronze age Levantine Israelite soldiers charging forward with weapons raised, bronze short swords and spears, shields forward, linen tunics, leather vests, dust and motion, aged parchment background, ink outlines with muted watercolor wash in ochre and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European",
    # Equipment & UI
    "bronze-sword": "bronze age short sword, leaf-shaped blade, isolated, hand-painted illustration, watercolor, transparent background, NOT medieval, NOT fantasy, NOT European",
    "leather-shield": "round leather shield, bronze rim, isolated, hand-painted illustration, watercolor, transparent background, NOT medieval, NOT fantasy, NOT European",
    "spear": "bronze-tipped wooden spear, isolated, hand-painted illustration, watercolor, transparent background, NOT medieval, NOT fantasy, NOT European",
    "sling": "leather sling with pouch, isolated, hand-painted illustration, watercolor, transparent background, NOT medieval, NOT fantasy, NOT European",
    "bow": "short composite bow, isolated, hand-painted illustration, watercolor, transparent background, NOT medieval, NOT fantasy, NOT European",
    "camel": "dromedary camel, side view, isolated, hand-painted illustration, watercolor, transparent background, NOT medieval, NOT fantasy, NOT European",
    "end-turn-button": "rounded rectangle button shape, aged warm parchment color, dark ink border outline, flat medieval manuscript style, game UI element, hand-painted texture, isolated on transparent background, family friendly",
    "command-card-back": "blank aged parchment card, rectangular, ink border, hand-painted texture, family friendly",
    "card-frame-template": "blank rectangular playing card, aged parchment background, ornate decorative ink border in dark brown, thin horizontal line dividing the card into top and bottom halves, corner ornaments, medieval manuscript border style, no text, hand-painted board game card",
    "hp_bar_bg": "thin horizontal bar shape, dark brown ink wash texture, rough hand-painted edges, game UI health bar background, isolated on transparent background, family friendly",
    "hp_bar_fill": "thin horizontal bar shape, faded crimson red ink wash, rough hand-painted edges, game UI health bar fill, isolated on transparent background, family friendly",
    "reward_panel": "large aged parchment panel texture, darker edges, vignette effect, ink border with corner ornaments, rounded rectangle shape, game UI panel, hand-painted texture, isolated on transparent background, family friendly",
    # Hex Tiles
    "hex_sand": (
        "top-down view of a flat hexagonal tile, sandy desert terrain, warm beige and light brown, "
        "subtle parchment-like texture, very fine grain, watercolor wash with soft edges, "
        "tileable seamless pattern, board game style, hand-painted texture, no grid lines"
    ),
    "hex_rock": (
        "top-down view of a flat hexagonal tile, rocky gravel and small stones, gray-brown and warm umber tones, "
        "parchment texture overlay, watercolor wash, tileable seamless pattern, board game style, "
        "hand-painted texture, no grid lines"
    ),
    "hex_grass": (
        "top-down view of a flat hexagonal tile, dry savanna grass on hard earth, "
        "warm green-brown and ochre tones, dry grass textures, watercolor wash, "
        "tileable seamless pattern, board game style, hand-painted texture, no grid lines"
    ),
    "grass": (
        "top-down view of a flat hexagonal tile, dry savanna grass on hard earth, "
        "warm green-brown and ochre tones, dry grass textures, watercolor wash, "
        "tileable seamless pattern, board game style, hand-painted texture, no grid lines"
    ),
    "rock": (
        "top-down view of a flat hexagonal tile, rocky gravel and small stones, gray-brown and warm umber tones, "
        "parchment texture overlay, watercolor wash, tileable seamless pattern, board game style, "
        "hand-painted texture, no grid lines"
    ),
    "sand": (
        "top-down view of a flat hexagonal tile, sandy desert terrain, warm beige and light brown, "
        "subtle parchment-like texture, very fine grain, watercolor wash with soft edges, "
        "tileable seamless pattern, board game style, hand-painted texture, no grid lines"
    ),
}


def gather_images(base):
    images = []
    for root, dirs, files in os.walk(base):
        for f in sorted(files):
            if f.lower().endswith((".png", ".jpg", ".jpeg")):
                full = os.path.join(root, f)
                rel = os.path.relpath(full, base)
                images.append((rel, full))
    return images


def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def compute_ahash(path, size=16):
    img = Image.open(path).convert("L").resize((size, size), Image.Resampling.LANCZOS)
    pixels = list(img.getdata())
    avg = sum(pixels) / len(pixels)
    bits = "".join("1" if p >= avg else "0" for p in pixels)
    return int(bits, 2)


def hamming_distance(h1, h2):
    x = h1 ^ h2
    count = 0
    while x:
        count += 1
        x &= x - 1
    return count


def find_duplicates(images, threshold=40):
    groups = []
    hashes = []
    for rel, full in images:
        h = compute_ahash(full)
        merged = False
        for idx, existing_hash in enumerate(hashes):
            if hamming_distance(h, existing_hash) <= threshold:
                groups[idx].append((rel, full))
                merged = True
                break
        if not merged:
            hashes.append(h)
            groups.append([(rel, full)])
    duplicates = []
    for group in groups:
        if len(group) > 1:
            sorted_group = sorted(group, key=lambda x: x[0])
            duplicates.extend(sorted_group[1:])
    return duplicates, groups


PROMPT_CHECK_FOLDERS = {
    "player-units", "unit-tokens", "davids", "amalekite", "amalekites", "standees",
    "portraits", "cards", "card", "assets", "box-art", "equipment", "ui-elements", "to_review"
}

PROMPT_ALIASES = {
    "camel rider": "camel_rider_amalekite",
    "camel-rider": "camel_rider_amalekite",
    "camal rider": "camel_rider_amalekite",
    "camal": "camel_rider_amalekite",
    "chieftain amalekite": "chieftain",
    "amalekite chieftain": "chieftain",
    "amalekite raider": "raider",
    "amalekite slinger": "slinger_amalekite",
    "amalekite archer": "archer_amalekite",
    "amalekite scout": "scout_amalekite",
    "young bronze age israelite commander": "david",
    "israelite commander": "david",
    "bronze age israelite swordsman": "swordsman",
    "israelite swordsman": "swordsman",
    "bronze age israelite spearman": "spearman",
    "israelite spearman": "spearman",
    "bronze age israelite slinger": "slinger",
    "israelite slinger": "slinger",
    "bronze age israelite archer": "archer",
    "israelite archer": "archer",
    "bronze age israelite scout": "scout",
    "israelite scout": "scout",
    "davids leadership": "davids-leadership",
    "swordsmen advance": "swordsmen-advance",
    "archer volley": "archer-volley",
    "spear wall": "spear-wall",
    "slinger skirmish": "slinger-skirmish",
    "scout recon": "scout-recon",
    "refugee aid": "refugee-aid",
    "command card back": "command-card-back",
    "card frame": "card-frame-template",
    "frame template": "card-frame-template",
    "end turn": "end-turn-button",
    "hp bar": "end-turn-button",
    "reward panel": "end-turn-button",
}

def lookup_expected_prompt(rel_path):
    folder = os.path.dirname(rel_path).lower()
    basename = os.path.basename(rel_path).lower()
    stem = os.path.splitext(basename)[0]
    path_no_numbers = re.sub(r'[\d_]+', '', stem)
    path_dashed = path_no_numbers.replace("_", " ").replace("-", " ")

    prompt_check = False
    for allowed in PROMPT_CHECK_FOLDERS:
        if allowed in folder.split(os.sep):
            prompt_check = True
            break

    if not prompt_check:
        return None, None

    parts = [p.lower() for p in re.split(r'[/\\]', folder)] + re.split(r'[\s_-]', basename)
    combined = " ".join(parts)

    best_key = None
    best_len = 0

    for key in EXPECTED_PROMPTS:
        k = key.lower()
        if k in parts or k in path_dashed:
            score = len(k)
            if score > best_len:
                best_len = score
                best_key = key
            continue
        words = k.split()
        if len(words) > 1:
            if all(w in parts or w in path_dashed for w in words):
                score = len(k)
                if score > best_len:
                    best_len = score
                    best_key = key

    if not best_key:
        for alias, canonical in PROMPT_ALIASES.items():
            if alias in combined:
                best_key = canonical
                break

    if best_key:
        return EXPECTED_PROMPTS[best_key], best_key
    return None, None


CHARACTER_KEYS = {
    "token_david", "token_swordsman", "token_spearman", "token_slinger",
    "token_archer", "token_scout", "token_chieftain_amalekite", "token_raider_amalekite",
    "token_refugee", "david", "swordsman", "spearman", "slinger", "archer",
    "scout", "raider", "chieftain", "refugee",
    "slinger_amalekite", "archer_amalekite", "scout_amalekite", "camel_rider_amalekite"
}
TILE_KEYS = {"hex_sand", "hex_rock", "hex_grass", "grass", "rock", "sand"}
UI_KEYS = {"end-turn-button", "command-card-back", "card-frame-template", "hp_bar_bg", "hp_bar_fill", "reward_panel"}
EQUIPMENT_KEYS = {"bronze-sword", "leather-shield", "spear", "sling", "bow", "camel"}
CARD_KEYS = {"swordsmen-advance", "archer-volley", "spear-wall", "slinger-skirmish", "scout-recon", "refugee-aid", "davids-leadership", "march", "engage"}

def classify_asset(expected_key):
    if not expected_key:
        return "generic"
    if expected_key in CHARACTER_KEYS:
        return "character"
    if expected_key in TILE_KEYS:
        return "tile"
    if expected_key in UI_KEYS:
        return "ui"
    if expected_key in EQUIPMENT_KEYS:
        return "equipment"
    if expected_key in CARD_KEYS:
        return "card"
    return "generic"


def build_prompt(expected_prompt, expected_key=None):
    asset_type = classify_asset(expected_key)
    parts = []

    if expected_prompt:
        parts.append(
            "Expected prompt for this image:\n"
            f"\"{expected_prompt}\"\n"
            "Compare the actual image to the expected prompt. If the image does NOT match the requested subject, scene, style, era, or composition, flag it.\n"
        )

    if asset_type == "character":
        parts.append(
            "Look at this image. Judge ONLY these concrete visual features. Do NOT try to identify who or what is depicted.\n"
            "1. Does it look hand-painted (watercolor/ink on parchment)? YES/NO\n"
            "2. Are the colors muted earth tones? YES/NO\n"
            "3. Is there any out-of-place modern object or text? YES/NO\n"
            "4. Is the image blurry or corrupted? YES/NO\n"
            "5. Is the composition centered and usable? YES/NO\n"
            "6. Any extra heads, extra limbs, extra fingers, or misformed body parts? YES/NO\n"
            "7. Any weapons or armor wrong for bronze age Levantine (no longswords, crossguards, plate armor, steel, longbows, medieval helmets, horned helmets, fantasy elements)? YES/NO\n"
            "8. Does the image closely match the expected prompt above? YES/NO\n"
            "Output: ANSWER1,ANSWER2,ANSWER3,ANSWER4,ANSWER5,ANSWER6,ANSWER7,ANSWER8"
        )
    elif asset_type == "tile":
        parts.append(
            "Look at this image. Judge ONLY these concrete visual features.\n"
            "1. Does it look hand-painted (watercolor/ink wash style)? YES/NO\n"
            "2. Are the colors muted earth tones? YES/NO\n"
            "3. Is there any modern object, text, or logo? YES/NO\n"
            "4. Is the image blurry or corrupted? YES/NO\n"
            "5. Does it look like a top-down flat hex tile with seamless edges? YES/NO\n"
            "6. Any visible grid lines or borders? YES/NO\n"
            "7. Does the image closely match the expected prompt above? YES/NO\n"
            "Output: ANSWER1,ANSWER2,ANSWER3,ANSWER4,ANSWER5,ANSWER6,ANSWER7"
        )
    elif asset_type == "ui":
        parts.append(
            "Look at this image. Judge ONLY these concrete visual features.\n"
            "1. Does it look hand-painted (ink/parchment style)? YES/NO\n"
            "2. Are the colors appropriate for the UI element? YES/NO\n"
            "3. Is there any modern object, text, or logo (except intended UI elements)? YES/NO\n"
            "4. Is the image blurry or corrupted? YES/NO\n"
            "5. Is the shape correct for the intended UI element? YES/NO\n"
            "6. Does the image closely match the expected prompt above? YES/NO\n"
            "Output: ANSWER1,ANSWER2,ANSWER3,ANSWER4,ANSWER5,ANSWER6"
        )
    elif asset_type == "equipment":
        parts.append(
            "Look at this image. Judge ONLY these concrete visual features.\n"
            "1. Does it look hand-painted (watercolor/ink)? YES/NO\n"
            "2. Are the colors muted earth tones? YES/NO\n"
            "3. Is there any modern object, text, or logo? YES/NO\n"
            "4. Is the image blurry or corrupted? YES/NO\n"
            "5. Is the object a historically accurate bronze age Levantine item (no modern, medieval, or fantasy variants)? YES/NO\n"
            "6. Does the image closely match the expected prompt above? YES/NO\n"
            "Output: ANSWER1,ANSWER2,ANSWER3,ANSWER4,ANSWER5,ANSWER6"
        )
    elif asset_type == "card":
        parts.append(
            "Look at this image. Judge ONLY these concrete visual features.\n"
            "1. Does it look hand-painted (watercolor/ink on parchment)? YES/NO\n"
            "2. Are the colors muted earth tones? YES/NO\n"
            "3. Is there any modern object, text, or logo (except intended card art)? YES/NO\n"
            "4. Is the image blurry or corrupted? YES/NO\n"
            "5. Is the composition centered and usable for a game card? YES/NO\n"
            "6. Any extra heads, extra limbs, extra fingers, or misformed body parts? YES/NO\n"
            "7. Any weapons or armor wrong for bronze age Levantine? YES/NO\n"
            "8. Does the image closely match the expected prompt above? YES/NO\n"
            "Output: ANSWER1,ANSWER2,ANSWER3,ANSWER4,ANSWER5,ANSWER6,ANSWER7,ANSWER8"
        )
    else:
        parts.append(
            "Look at this image. Judge ONLY these concrete visual features.\n"
            "1. Is the image blurry or corrupted? YES/NO\n"
            "2. Is there any out-of-place modern object, text, or logo? YES/NO\n"
            "3. Is the composition acceptable for its asset type? YES/NO\n"
            "4. Does the image closely match the expected prompt above? YES/NO\n"
            "Output: ANSWER1,ANSWER2,ANSWER3,ANSWER4"
        )

    return "\n".join(parts)


def get_expected_count(asset_type):
    counts = {
        "character": 8,
        "card": 8,
        "tile": 7,
        "ui": 6,
        "equipment": 6,
        "generic": 4,
    }
    return counts.get(asset_type, 4)


def review_image(model, image_path, expected_prompt=None, expected_key=None, timeout=600):
    prompt = build_prompt(expected_prompt, expected_key)
    payload = {
        "model": model,
        "prompt": prompt,
        "images": [encode_image(image_path)],
        "stream": False,
        "options": {"temperature": 0.1, "num_ctx": 4096, "num_gpu": 0}
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("response", "").strip()
    except urllib.error.HTTPError as e:
        return f"ERROR: HTTP {e.code}"
    except Exception as e:
        return f"ERROR: {str(e)}"


def parse_answers(response, expected_count=8):
    lines = response.strip().split("\n")
    for line in lines:
        parts = [p.strip().upper() for p in line.split(",")]
        if len(parts) >= 5 and all(p in ("YES", "NO") for p in parts[:5]):
            while len(parts) < expected_count:
                parts.append("YES")
            return parts[:expected_count]
    matches = re.findall(r'\b(YES|NO)\b', response.upper())
    if len(matches) >= 5:
        while len(matches) < expected_count:
            matches.append("YES")
        return matches[:expected_count]
    return ["YES"] * expected_count


def decide(answers, expected_prompt=None, asset_type="generic"):
    expected_count = get_expected_count(asset_type)
    while len(answers) < expected_count:
        answers.append("YES")

    if asset_type == "tile":
        painted, earth, modern, blurry, tile_shape, grid_lines, prompt_match = answers[:7]
        score = 5
        reasons = []
        if blurry == "YES":
            score -= 2
            reasons.append("blurry/corrupted")
        if modern == "YES":
            score -= 3
            reasons.append("modern object/text detected")
        if tile_shape == "NO":
            score -= 3
            reasons.append("not a top-down flat hex tile")
        if grid_lines == "YES":
            score -= 2
            reasons.append("visible grid lines/borders")
        if expected_prompt and prompt_match == "NO":
            score -= 2
            reasons.append("does not match expected prompt")
        score = max(1, score)
        reason = "; ".join(reasons) if reasons else "all checks passed"
        if modern == "YES" or blurry == "YES" or tile_shape == "NO" or grid_lines == "YES" or score <= 2:
            return "TRASH", reason, score
        return "KEEP", reason, score

    elif asset_type == "ui":
        painted, earth, modern, blurry, shape, prompt_match = answers[:6]
        score = 5
        reasons = []
        if blurry == "YES":
            score -= 2
            reasons.append("blurry/corrupted")
        if modern == "YES":
            score -= 3
            reasons.append("modern object/text detected")
        if shape == "NO":
            score -= 2
            reasons.append("wrong shape for element")
        if expected_prompt and prompt_match == "NO":
            score -= 2
            reasons.append("does not match expected prompt")
        score = max(1, score)
        reason = "; ".join(reasons) if reasons else "all checks passed"
        if modern == "YES" or blurry == "YES" or shape == "NO" or score <= 2:
            return "TRASH", reason, score
        return "KEEP", reason, score

    elif asset_type == "equipment":
        painted, earth, modern, blurry, accurate, prompt_match = answers[:6]
        score = 5
        reasons = []
        if blurry == "YES":
            score -= 2
            reasons.append("blurry/corrupted")
        if modern == "YES":
            score -= 3
            reasons.append("modern object/text detected")
        if accurate == "NO":
            score -= 3
            reasons.append("not historically accurate bronze age")
        if expected_prompt and prompt_match == "NO":
            score -= 2
            reasons.append("does not match expected prompt")
        score = max(1, score)
        reason = "; ".join(reasons) if reasons else "all checks passed"
        if modern == "YES" or blurry == "YES" or accurate == "NO" or score <= 2:
            return "TRASH", reason, score
        return "KEEP", reason, score

    elif asset_type in ("character", "card"):
        painted, earth, modern, blurry, comp, anatomy, weapon_era, prompt_match = answers[:8]
        score = 5
        reasons = []
        if painted == "NO":
            score -= 2
            reasons.append("not hand-painted")
        if earth == "NO":
            score -= 1
            reasons.append("colors off")
        if modern == "YES":
            score -= 3
            reasons.append("modern object/text detected")
        if blurry == "YES":
            score -= 2
            reasons.append("blurry/corrupted")
        if comp == "NO":
            score -= 1
            reasons.append("composition off")
        if anatomy == "YES":
            score -= 3
            reasons.append("anatomical defect")
        if weapon_era == "YES":
            score -= 3
            reasons.append("anachronistic item")
        if expected_prompt and prompt_match == "NO":
            score -= 2
            reasons.append("does not match expected prompt")
        score = max(1, score)
        reason = "; ".join(reasons) if reasons else "all checks passed"
        if modern == "YES" or blurry == "YES" or anatomy == "YES" or weapon_era == "YES" or score <= 2:
            return "TRASH", reason, score
        return "KEEP", reason, score

    else:
        blurry, modern, comp, prompt_match = (answers + ["YES"] * 4)[:4]
        score = 5
        reasons = []
        if blurry == "YES":
            score -= 2
            reasons.append("blurry/corrupted")
        if modern == "YES":
            score -= 3
            reasons.append("modern object/text detected")
        if comp == "NO":
            score -= 1
            reasons.append("composition off")
        if expected_prompt and prompt_match == "NO":
            score -= 2
            reasons.append("does not match expected prompt")
        score = max(1, score)
        reason = "; ".join(reasons) if reasons else "all checks passed"
        if modern == "YES" or blurry == "YES" or score <= 2:
            return "TRASH", reason, score
        return "KEEP", reason, score


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="minicpm-v:8b")
    parser.add_argument("--base", default=r"D:\Jake\ComfyUI_windows_portable\ComfyUI\output\ComfyUI\annointed-exile")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--output", default="art_review_report.json")
    parser.add_argument("--delay", type=float, default=0.0)
    parser.add_argument("--no-move", action="store_true", help="don't auto-move files, just report")
    parser.add_argument("--dedupe", action="store_true", default=True, help="remove duplicate images (default: True)")
    parser.add_argument("--no-dedupe", action="store_false", dest="dedupe", help="skip duplicate removal")
    parser.add_argument("--dedupe-threshold", type=int, default=40, help="aHash Hamming distance threshold for duplicates (default: 40)")
    parser.add_argument("--dedupe-dir", default="to_duplicates", help="directory name for duplicates (relative to each image folder)")
    args = parser.parse_args()

    images = gather_images(args.base)
    if args.limit > 0:
        images = images[:args.limit]

    if args.dedupe:
        duplicate_count = 0
        duplicates, groups = find_duplicates(images, threshold=args.dedupe_threshold)
        dup_paths = {full for _, full in duplicates}
        images = [(rel, full) for rel, full in images if full not in dup_paths]
        print(f"Dedupe removed {len(duplicates)} duplicates ({len(groups)} duplicate groups) [threshold={args.dedupe_threshold}]")
        for _, full in duplicates:
            dup_dir = os.path.join(os.path.dirname(full), args.dedupe_dir)
            os.makedirs(dup_dir, exist_ok=True)
            dest = os.path.join(dup_dir, os.path.basename(full))
            if not os.path.exists(dest):
                shutil.move(full, dest)
            duplicate_count += 1
        print(f"Duplicates moved to '{args.dedupe_dir}/' folders")
        print(f"---\n")

    print(f"=== Ollama Art Review (full folder, anatomy + prompt check) ===")
    print(f"Model: {args.model}")
    print(f"Images to review: {len(images)}")
    print(f"Output: {args.output}")
    if not args.no_move:
        print(f"Auto-moving TRASH files to to_trash/")
    print(f"---\n")

    results = []
    keep_count = 0
    trash_count = 0
    error_count = 0
    no_prompt_count = 0

    for i, (rel, full) in enumerate(images):
        expected, expected_key = lookup_expected_prompt(rel)
        asset_type = classify_asset(expected_key)
        if expected is None:
            no_prompt_count += 1
        tag = f"[prompt matched: {expected_key or 'none'} ({asset_type})]"
        print(f"[{i+1}/{len(images)}] {rel} {tag} ... ", end="", flush=True)
        response = review_image(args.model, full, expected_prompt=expected, expected_key=expected_key)

        if response.startswith("ERROR"):
            print(f"ERROR: {response}")
            error_count += 1
            results.append({
                "filename": rel,
                "expected_prompt_key": expected_key,
                "asset_type": asset_type,
                "expected_prompt": expected,
                "decision": "ERROR",
                "score": 0,
                "reason": response,
                "answers": [],
                "raw_response": response
            })
            continue

        expected_count = get_expected_count(asset_type)
        answers = parse_answers(response, expected_count=expected_count)
        decision, reason, score = decide(answers, expected_prompt=expected, asset_type=asset_type)

        print(f"{decision} | {score} | {reason}")

        if decision == "TRASH" and not args.no_move:
            trash_dir = os.path.join(os.path.dirname(full), "to_trash")
            os.makedirs(trash_dir, exist_ok=True)
            dest = os.path.join(trash_dir, os.path.basename(full))
            if not os.path.exists(dest):
                shutil.move(full, dest)

        if decision == "KEEP":
            keep_count += 1
        elif decision == "TRASH":
            trash_count += 1

        results.append({
            "filename": rel,
            "expected_prompt_key": expected_key,
            "asset_type": asset_type,
            "expected_prompt": expected,
            "decision": decision,
            "score": score,
            "reason": reason,
            "answers": answers,
            "raw_response": response
        })

        if args.delay > 0:
            time.sleep(args.delay)

    report = {
        "model": args.model,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_reviewed": len(results),
        "keep": keep_count,
        "trash": trash_count,
        "errors": error_count,
        "no_prompt_match": no_prompt_count,
        "images": results
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\n=== SUMMARY ===")
    print(f"Total reviewed: {len(results)}")
    print(f"KEEP: {keep_count}")
    print(f"TRASH: {trash_count}")
    print(f"Errors: {error_count}")
    print(f"No prompt match: {no_prompt_count}")
    print(f"Report saved to: {args.output}")

    if trash_count > 0:
        trash_list = [r for r in results if r["decision"] == "TRASH"]
        print(f"\n--- TRASH FILES ({len(trash_list)}) ---")
        for t in trash_list:
            print(f"  {t['filename']} | {t['score']} | {t['reason']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

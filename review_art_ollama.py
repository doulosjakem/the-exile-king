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
    "abigail": "ONE PERSON ONLY, solo portrait, waist-up, Abigail wife of Nabal, bronze age Levantine noblewoman, dark hair in woven braids, rich but practical woolen tunic in faded blue, leather belt, small knife at waist, face showing intelligence and caution, standing with a loaded donkey behind her, laden with gifts, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "benjamin-spearman": "ONE PERSON ONLY, solo portrait, waist-up, Benjamite spearman of Jonathan's guard, bronze age Levantine elite infantry, strong fierce build, dark hair, white linen tunic with leather shoulder guards, brown cloak wrapped and fastened, long wooden spear with bronze tip held upright, small hide shield at side, leather cord belt with knife, alert loyal expression, standing in disciplined formation, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-round3-david-as-king": "game box art, painting in illuminated manuscript style, David crowned at Hebron, elder standing before him with a horn of oil, olive trees and stone walls in background, autumn golden light, his captains behind him, composition is kingship earned through hardship, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-round3-david-at-adullam": "game box art, painting in illuminated manuscript style, David seated at the entrance of a cave at Adullam, surrounded by a ragtag band of outcasts and warriors, one man sharpening a spear, another mending a cloak, warm firelight against dark rock, composition is intimate and raw, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-round3-jonathan-and-david": "game box art, painting in illuminated manuscript style, Jonathan and David standing on a hilltop at Mizpah, Jonathan taking off his robe and giving it to David along with his weapons, wind blowing the fabric between them, golden light, composition is tender and covenant-making, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-round3-the-cave-of-engedi": "game box art, painting in illuminated manuscript style, inside the dark cave at Ein Gedi, David standing in the shadows near Saul who is sleeping, Saul's robe spread wide at the entrance, David's hand hovering near the hem deciding whether to strike, torchlight flickering, composition is the moment of mercy, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-round3-the-wounded-david": "game box art, painting in illuminated manuscript style, David lying wounded and exhausted on a rocky hillside, his armor scattered, a single warrior kneeling beside him offering water, dark storm clouds above, composition is vulnerability and trust, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded indigo, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "camel-rider_amalekite": "ONE PERSON ONLY, solo portrait, waist-up, Amalekite camel rider, bronze age Levantine desert warrior, dark hair, dusty red-brown cloak and headwrap, bronze-tipped spear held upright, riding tall dromedary camel, leather reins in hand, weathered stern expression, camel standing on sandy desert ground with distant mountains, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European",
    "judah-militia": "ONE PERSON ONLY, solo portrait, waist-up, Judah militia defender, bronze age Levantine village warrior, sturdy build, dark hair, simple linen tunic with leather vest, brown wool cloak, bronze short sword in hand, small round hide shield, leather sandals, determined local expression, leaning on spear in resting pose, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "nabal": "ONE PERSON ONLY, solo portrait, waist-up, Nabal the Carmelite, bronze age Levantine wealthy landowner, heavyset build, dark hair and short beard, rich woolen tunic with woven border, bronze rings on fingers, bronze short sword at hip, expression of stubborn pride, seated on a low stool with a wine cup in hand, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "priest-of-nob": "ONE PERSON ONLY, solo portrait, waist-up, priest of Nob, bronze age Levantine priest, older man, white linen ephod over simple tunic, bronze plate on chest with Urim and Thummim, short beard, kind eyes, holding a loaf of showbread, standing before a stone altar, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "reward-panel": "large aged parchment panel texture, darker edges, vignette effect, ink border with corner ornaments, rounded rectangle shape, game UI panel, hand-painted texture, isolated on transparent background, family friendly",
    "abner": "ONE PERSON ONLY, solo portrait, waist-up, Abner commander of Saul's army, bronze age Levantine military leader, strong build, dark hair and beard, leather vest over linen tunic, brown wool cloak, bronze spear in hand, hardened battle expression, alert posture, standing on rocky ground, Mediterranean complexion",
    "achish": "ONE PERSON ONLY, solo portrait, waist-up, Achish lord of Gath, bronze age Levantine Philistine ruler, dark hair, rich purple cloak over linen tunic, bronze chest plate, bronze sword at hip, stern unreadable expression, seated authority, Mediterranean complexion",
    "amalekite-raid": "ONE PERSON ONLY, scene in illuminated manuscript style, Amalekite raiders on camel and foot sweeping through a settlement, spears raised, dust clouds, civilians fleeing, aged parchment background, ink outlines with muted watercolor wash in ochre umber and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "amasa": "ONE PERSON ONLY, solo portrait, waist-up, Amasa captain of Judah, bronze age Levantine commander, honest earnest expression, dark hair and beard, linen tunic with leather vest, brown cloak, bronze spear in hand, appointed captain bearing, standing with quiet authority, Mediterranean complexion",
    "amasa-rally": "ONE PERSON ONLY, scene in illuminated manuscript style, Amasa son of Jether rallying troops with hand raised, bronze spear in other hand, soldiers gathering around, aged parchment background, ink outlines with muted watercolor wash in ochre and amber, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "asahel": "ONE PERSON ONLY, solo portrait, waist-up, Asahel son of Zeruiah, bronze age Levantine runner warrior, lean swift build, dark hair, light linen tunic with leather vest, wrapped cloak for swift movement, short sword raised, running stance, focused expression, Mediterranean complexion",
    "asahel-flank": "ONE PERSON ONLY, scene in illuminated manuscript style, Asahel son of Zeruiah running with incredible speed, short sword raised, dust rising at his feet, single runner outrunning formation, aged parchment background, ink outlines with muted watercolor wash in umber and faded gold, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "benjamite-spearman": "ONE PERSON ONLY, solo portrait, waist-up, Benjamite spearman of Jonathan's guard, bronze age Levantine elite infantry, strong fierce build, dark hair, white linen tunic with leather shoulder guards, brown cloak wrapped and fastened, long wooden spear with bronze tip held upright, small hide shield at side, leather cord belt with knife, alert loyal expression, standing in disciplined formation, Mediterranean complexion",
    "elhanan": "ONE PERSON ONLY, solo portrait, waist-up, Elhanan the Bethlehemite, bronze age Levantine mighty man, strong build, dark hair, linen tunic with leather vest, bronze spear, small shield, determined expression, gazing at fallen giant, Mediterranean complexion",
    "elite-archer": "ONE PERSON ONLY, solo portrait, waist-up, Elite archer of Jonathan's guard, bronze age Levantine master archer, dark hair, fitted linen tunic, leather bracers, brown cloak, composite bow drawn with arrow nocked, quiver, focused precise expression, Mediterranean complexion",
    "elite-bodyguard": "ONE PERSON ONLY, solo portrait, waist-up, Israelite elite bodyguard, bronze age Levantine royal protector, dark hair, well-fitted linen tunic with leather armor, brown cloak, large hide shield, bronze short sword, alert protective stance, loyal expression, standing ready to defend, Mediterranean complexion",
    "geshurite-archer": "ONE PERSON ONLY, solo portrait, waist-up, Geshurite archer, bronze age Levantine desert archer, dark hair, linen tunic with leather vest, dusty brown cloak, short composite bow drawn with arrow, quiver on back, sharp focused expression, standing on rocky desert ground, Mediterranean complexion",
    "geshurite-camel-rider": "ONE PERSON ONLY, solo portrait, waist-up, Geshurite camel rider, bronze age Levantine desert warrior, dark hair, dusty brown cloak and headwrap, bronze-tipped spear held upright, riding tall dromedary camel, leather reins in hand, weathered expression, Mediterranean complexion",
    "geshurite-clansman": "ONE PERSON ONLY, solo portrait, waist-up, Geshurite clansman, bronze age Levantine tribal warrior, dark hair, linen tunic with leather vest, worn brown cloak, bronze short sword, sling at belt, small knife, alert expression, Mediterranean complexion",
    "geshurite-spearman": "ONE PERSON ONLY, solo portrait, waist-up, Geshurite spearman, bronze age Levantine infantry, dark hair, linen tunic with leather shoulder piece, brown cloak, long wooden spear with bronze tip held in both hands, small hide shield, determined expression, Mediterranean complexion",
    "gezerite-archer": "ONE PERSON ONLY, solo portrait, waist-up, Gezerite archer, bronze age Levantine Canaanite archer, dark hair, linen tunic, leather vest, short composite bow drawn, quiver on back, sharp eyes, focused expression, Mediterranean complexion",
    "gezerite-defender": "ONE PERSON ONLY, solo portrait, waist-up, Gezerite defender, bronze age Levantine Canaanite warrior, dark hair, sturdy build, linen tunic with leather shoulder armor, round hide shield, bronze spear, determined defensive expression, standing firm, Mediterranean complexion",
    "gezerite-scout": "ONE PERSON ONLY, solo portrait, waist-up, Gezerite scout, bronze age Levantine tracker, lean dark-haired man, linen tunic with leather vest, worn cloak, short javelin, sling at belt, alert watchful expression, scanning horizon, Mediterranean complexion",
    "girzite-chief": "ONE PERSON ONLY, solo portrait, waist-up, Girzite chief, bronze age Levantine desert clan leader, dark windblown hair, weathered face, dusty brown cloak wrapped around, leather tunic, bronze spear in hand, bronze short sword at hip, authoritative scorched expression, Mediterranean complexion",
    "girzite-raider": "ONE PERSON ONLY, solo portrait, waist-up, Girzite raider, bronze age Levantine desert skirmisher, dark windblown hair, lean weathered face, dusty brown cloak, leather tunic, javelin in hand, leather sling, hardened expression, alert stance, Mediterranean complexion",
    "girzite-scout": "ONE PERSON ONLY, solo portrait, waist-up, Girzite scout, bronze age Levantine desert tracker, lean dark-haired man, dusty brown cloak patched, short javelin, sling at belt, small shield, sharp alert eyes scanning horizon, Mediterranean complexion",
    "girzite-shepherd-raider": "ONE PERSON ONLY, solo portrait, waist-up, Girzite shepherd-raider, bronze age Levantine desert warrior, lean build, dark windblown hair, dusty brown cloak, leather vest, sling at belt, short spear, shepherd's crook leaning nearby, weathered expression, Mediterranean complexion",
    "goliath": "ONE PERSON ONLY, solo portrait, waist-up, Goliath the Gittite, bronze age Levantine giant champion, enormous build, dark hair and beard, elaborate tunic, bronze scale armor, large bronze shield, massive bronze-tipped spear like a weaver's beam, jawset expression, towering menacing figure, Mediterranean complexion",
    "goliath-challenge": "ONE PERSON ONLY, scene in illuminated manuscript style, Goliath the Gittite standing immense with spear like a weaver's beam, small figure of David opposite him, bronze shields, dust rising, aged parchment background, ink outlines with muted watercolor wash in umber and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "hex-tile-desert-night": "top-down flat hex tile, desert at night, cool blue-gray under moonlight, subtle stars, watercolor wash, board game style, seamless, 512x512",
    "hex-tile-ruins": "top-down flat hex tile, broken stone walls and rubble, weathered umber, watercolor and ink wash, board game style, seamless, 512x512",
    "hex-tile-stone-path": "top-down flat hex tile, ancient stone path and packed earth, gray-brown, ink wash texture, board game style, seamless, 512x512",
    "israelite-archer": "ONE PERSON ONLY, solo portrait, waist-up, Israelite archer of Saul's army, bronze age Levantine archer, dark hair, simple linen tunic with leather vest, brown cloak, short composite bow in hand with arrow nocked, quiver on back, knife at waist, focused expression, standing ready, Mediterranean complexion",
    "joab": "ONE PERSON ONLY, solo portrait, waist-up, Joab commander of David's army, bronze age Levantine general, tall strong build, gray-streaked beard, dark hair, leather scale armor over linen tunic, brown cloak, bronze spear raised, ruthless brilliant expression, battle-scarred, Mediterranean complexion",
    "joab-assault": "ONE PERSON ONLY, scene in illuminated manuscript style, Joab son of Zeruiah leading a fierce charge, bronze spear raised, Israelite warriors behind him, aged parchment background, ink outlines with muted watercolor wash in ochre and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "jonathan": "ONE PERSON ONLY, solo portrait, waist-up, Jonathan son of Saul, bronze age Levantine prince and warrior, dark hair, handsome features, rich blue-purple cloak over linen tunic, leather vest, composite bow in hand, quiver on back, bronze short sword at hip, noble brave expression, standing confidently, Mediterranean complexion",
    "jonathan-armor-bearer": "ONE PERSON ONLY, solo portrait, waist-up, Jonathan's armor-bearer, bronze age Levantine elite warrior, dark hair, linen tunic with leather vest, brown cloak, bronze spear, shield at side, loyal brave expression, standing ready, Mediterranean complexion",
    "jonathan-precision": "ONE PERSON ONLY, scene in illuminated manuscript style, Jonathan son of Saul drawing his composite bow, arrow aimed, two Israelite archers beside him, aged parchment background, ink outlines with muted watercolor wash in ochre and faded gold, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "jonathan-shield-bearer": "ONE PERSON ONLY, solo portrait, waist-up, Jonathan's shield-bearer, bronze age Levantine warrior, dark hair, strong build, linen tunic with leather armor, large round hide shield held high, bronze sword at hip, protective stance, determined expression, Mediterranean complexion",
    "jonathan-spearman": "ONE PERSON ONLY, solo portrait, waist-up, Jonathan's spearman guard, bronze age Levantine Benjamite warrior, dark hair, white linen tunic with leather shoulder guards, brown cloak wrapped, long spear with bronze tip held upright, small shield, alert disciplined expression, Mediterranean complexion",
    "lahmi": "ONE PERSON ONLY, solo portrait, waist-up, Lahmi the giant, bronze age Levantine Rephaim warrior, enormous build, dark hair, simple tunic, bronze spear, fierce expression, towering figure, Mediterranean complexion",
    "loyal-guard": "ONE PERSON ONLY, solo portrait, waist-up, Loyal guard of Jonathan, bronze age Levantine elite warrior, dark hair, white linen tunic with dark border, leather vest, brown cloak, spear in hand, small shield, devoted alert expression, standing beside commander, Mediterranean complexion",
    "mighty-abishai": "ONE PERSON ONLY, solo portrait, waist-up, Abishai son of Zeruiah, bronze age Levantine mighty man, tall strong build, dark hair, linen tunic with leather vest, brown cloak, bronze spear raised high, fierce battle expression, leading attack, Mediterranean complexion",
    "mighty-benaiah": "ONE PERSON ONLY, solo portrait, waist-up, Benaiah son of Jehoiada, bronze age Levantine mighty man, strong build, dark hair, linen tunic with leather vest, brown cloak, bronze sword in hand, lion pelt over one shoulder, brave legendary expression, Mediterranean complexion",
    "mighty-eleazar": "ONE PERSON ONLY, solo portrait, waist-up, Eleazar son of Dodai, bronze age Levantine mighty man, strong fierce build, dark hair and beard, linen tunic with leather vest, bronze spear raised, small round shield, determined exhausted expression, hand clinging to sword, Mediterranean complexion",
    "mighty-josheb-basshebeth": "ONE PERSON ONLY, solo portrait, waist-up, Josheb-basshebeth the Tachmonite, bronze age Levantine mighty man, powerful build, dark hair and beard, bronze scale armor over linen tunic, brown cloak, massive bronze spear held upright, fierce legendary expression, standing with enormous weapon, Mediterranean complexion",
    "mighty-sham": "ONE PERSON ONLY, solo portrait, waist-up, Shammah son of Agee, bronze age Levantine mighty man, strong build, dark hair, linen tunic with leather armor, bronze spear held ready, standing in defensive stance, weathered devoted expression, Mediterranean complexion",
    "officer": "ONE PERSON ONLY, solo portrait, waist-up, Israelite army officer, bronze age Levantine military commander, dark hair and short beard, linen tunic with leather vest, brown wool cloak, bronze short sword at hip, bronze spear in hand, authoritative expression, standing with command presence, Mediterranean complexion",
    "philistine-archer": "ONE PERSON ONLY, solo portrait, waist-up, Philistine archer, bronze age Levantine archer, dark hair, simple tunic with leather vest, short bow drawn, quiver on back, sharp eyes, focused expression, standing ready, Mediterranean complexion",
    "philistine-champion": "ONE PERSON ONLY, solo portrait, waist-up, Philistine champion, bronze age Levantine elite warrior, dark hair, decorated tunic, bronze scale armor, large shield, spear raised, confident duelist expression, standing in challenge pose, Mediterranean complexion",
    "philistine-charge": "ONE PERSON ONLY, scene in illuminated manuscript style, Philistine heavy infantry advancing in formation, large shields locked, spears angled forward, dust and determination, aged parchment background, ink outlines with muted watercolor wash in umber ochre and faded indigo, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "philistine-charioteer": "ONE PERSON ONLY, solo portrait, waist-up, Philistine charioteer, bronze age Levantine warrior, dark hair, linen tunic with leather armor, brown cloak flowing, standing beside bronze-rimmed chariot, spear in hand, weathered determined expression, Mediterranean complexion",
    "philistine-heavy": "ONE PERSON ONLY, solo portrait, waist-up, Philistine heavy infantry, bronze age Levantine warrior, large build, dark hair, linen tunic with bronze scale armor, large hide-covered shield with bronze rim, long spear, bronze short sword, imposing slow stance, Mediterranean complexion",
    "philistine-lord": "ONE PERSON ONLY, solo portrait, waist-up, Philistine lord, bronze age Levantine city-state ruler, dark hair, rich embroidered tunic, bronze scale armor, purple cloak, bronze sword, authoritative expression, standing with regal bearing, Mediterranean complexion",
    "philistine-spearman": "ONE PERSON ONLY, solo portrait, waist-up, Philistine spearman, bronze age Levantine infantry, dark hair, linen tunic with leather vest, large rectangular shield, long bronze-tipped spear, bronze helmet, steady formation stance, Mediterranean complexion",
    "royal-guard": "ONE PERSON ONLY, solo portrait, waist-up, Israelite royal guard, bronze age Levantine elite infantryman, dark hair, white linen tunic with woven border, leather vest, brown wool cloak pinned at shoulder, bronze short sword, small round hide shield, loyal disciplined expression, standing at attention, Mediterranean complexion",
    "saph": "ONE PERSON ONLY, solo portrait, waist-up, Saph the giant, bronze age Levantine Rephaim warrior, enormous build, dark hair, worn tunic, large shield, bronze sword, threatening expression, Mediterranean complexion",
    "saul": "ONE PERSON ONLY, solo portrait, waist-up, Saul king of Israel, bronze age Levantine monarch, tall commanding presence, dark hair and short beard, rich purple-blue wool cloak over linen tunic, bronze chest plate with simple geometric engraving, bronze short sword at hip, leather sandals, stern authoritative expression, standing with regal bearing, Mediterranean complexion",
    "sibbecai": "ONE PERSON ONLY, solo portrait, waist-up, Sibbecai the Hushathite, bronze age Levantine mighty man, strong build, dark hair, linen tunic with leather armor, bronze spear raised, victorious expression, standing over defeated enemy, Mediterranean complexion",
    "ui-card-slot": "empty card slot on table, aged parchment background, wooden card border, board game UI element, transparent background, hand-painted illustration, NOT medieval, NOT fantasy, NOT European",
    "ui-commander-aura": "soft glowing circle on ground, commander presence area, warm golden light, board game UI element, transparent background, hand-painted illustration, NOT medieval, NOT fantasy, NOT European",
    "ui-portrait-frame": "ornate rectangular frame for character portrait, aged parchment with dark ink border, corner ornaments, board game UI element, hand-painted illustration, transparent background, NOT medieval, NOT fantasy, NOT European",

    "chieftain_amalekite": "ONE PERSON ONLY, solo portrait, waist-up, Amalekite chieftain, bronze age Levantine nomadic warlord, dark hair and gray-streaked beard, dark red-brown wool cloak trimmed with rough fringe, leather and simple bronze chest piece, weathered authoritative face, bronze short sword at hip, spear in hand, wrapped headdress, standing on rocky outcrop overlooking warriors, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European",
    "raider_amalekite": "ONE PERSON ONLY, solo portrait, waist-up, Amalekite raider, bronze age Levantine nomadic desert warrior, dark windblown hair, weathered lean face, dusty red-brown wool cloak wrapped around body, leather tunic underneath, bronze-tipped spear in hand, curved knife at belt, hardened squinting expression, standing on sandy desert ground with rocky outcrops, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European",
    "hp-bar-bg": "thin horizontal bar shape, dark brown ink wash texture, rough hand-painted edges, game UI health bar background, isolated on transparent background, family friendly",
    "hp-bar-fill": "thin horizontal bar shape, faded crimson red ink wash, rough hand-painted edges, game UI health bar fill, isolated on transparent background, family friendly",
    "refugee": "ONE PERSON ONLY, solo portrait, waist-up, bronze age Levantine civilian, refugee, simple linen tunic, worn brown cloak, bundle on stick over shoulder, sandals, weary but hopeful expression, no weapons, standing on dusty road, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-abigail-intervenes": "game box art, painting in illuminated manuscript style, Abigail kneeling in the dust before David, a servant leading a laden donkey behind her, David's men standing with weapons raised in the background, her face lifted in supplication, his face softening, composition is low and dramatic, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-adullams-cave": "game box art, painting in illuminated manuscript style, interior view of a cave mouth at dusk, David and a ragged group of outcasts huddle inside, faces lit by a small fire, outside Saul's soldiers sprawl on rocks with spears, dramatic light contrast warm firelight vs cool blue dusk, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded indigo, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-anointed-stone": "game box art, painting in illuminated manuscript style, close-up composition a simple shepherd's staff and a sling rest on rough stone, in the background faint golden light breaks through cloud over a hill, no people the objects carry the weight, manuscript border with vine motifs, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-asahel-chases-abner": "game box art, painting in illuminated manuscript style, Asahel running with incredible speed across open ground toward Abner who rides a horse backward, Abner turning with spear butt raised, other warriors frozen in shock on both sides, motion lines and dust, composition is the moment before death, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-before-the-king": "game box art, painting in illuminated manuscript style, David leaning on his spear gazing at a ruined city skyline in the distance, he wears a simple tunic no crown no regalia, two loyal warriors stand nearby arms crossed, dawn light, title treatment sits above in illuminated capitals, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-board-of-war": "game box art, painting in illuminated manuscript style, a stone between two boulders serves as a crude war table, on it a crude clay map, David leans in with three captains pointing, skin scrolls lean against the rocks, punchy ink strokes minimal color, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-chieftains-challenge": "game box art, painting in illuminated manuscript style, face-off across a dusty clearing David and the Amalekite Chieftain mirror each other both armed both looking at a small object on the ground between them a shared water skin or bread, not a duel in motion but a moment of pause before violence, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-covenant-at-mizpah": "game box art, painting in illuminated manuscript style, Jonathan and David standing on a hilltop at Mizpah, a young lamb between them as a witness, both holding the shaft of a single spear pointing toward the ground, wind blowing their cloaks apart, golden light breaking through clouds behind them, composition is solemn and emotional, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-covenant-at-the-cave": "game box art, painting in illuminated manuscript style, David's hand reaches toward Jonathan's within a shadowed cave interior, both wear simple cloaks, a single lit torch between them casts their faces gold, composition is tight and emotional friendship sworn in dangerous times, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-david-among-the-philistines": "game box art, painting in illuminated manuscript style, David standing in a Philistine camp at Ziklag, wearing Philistine-style dress, Achish pointing toward the battlefield in the distance, Israelite warriors looking on with mixed expressions, the moment of uneasy alliance, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded indigo, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-david-anointed-king-of-judah": "game box art, painting in illuminated manuscript style, the elders of Israel standing in a circle around David at Hebron, a horn of oil in the hands of the high priest, olive trees and stone walls of Hebron in the background, golden autumn light, composition is coronation but simple, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-david-counting-israel": "game box art, painting in illuminated manuscript style, David standing on a raised platform with a scroll in hand, census counters moving through the camp below, a prophet in rough garments standing before him pointing heavenward in rebuke, dark clouds gathering, composition is judgment and regret, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded indigo, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-david-fleeing-naioth": "game box art, painting in illuminated manuscript style, David running through a dark stone corridor at Naioth, Samuel's hand raised behind him in benediction, torchlight flickering on rough walls, Saul's soldiers visible at the far end hesitating, composition is vertical and tense, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-david-in-the-wilderness-of-ziph": "game box art, painting in illuminated manuscript style, David and a small band crouched in a dark cave opening overlooking the wilderness of Ziph, Saul's army visible as a dust trail far below on the plateau, heat haze rising, composition is wide and claustrophobic, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-david-mourns-abner": "game box art, painting in illuminated manuscript style, David walking behind Abner's coffin at the gate of Hebron, weeping openly, his captains walking beside him with bowed heads, the people watching from the walls, a single torch casting long shadows, composition is public grief and dignity, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded indigo, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-david-returns-the-ark": "game box art, painting in illuminated manuscript style, the Ark of the Covenant carried on a new cart by oxen, David dancing before it in a linen ephod, the people of Israel cheering with trumpets, Jerusalem's walls visible in the background, celebration and worship, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-david-s-lament": "game box art, painting in illuminated manuscript style, David seated on a rocky ledge, harp in hand but head bowed, ink and tears on parchment, the words \"the beauty of Israel is slain upon thy high places\" faintly visible as if written across the sky, no other figures, composition is grief, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-david-s-mighty-men-at-the-cave": "game box art, painting in illuminated manuscript style, the Three Mighty Men standing in a cave mouth at Adullam, water dripping from the ceiling, their faces weathered and devoted, David looking at them with deep affection, weapons stacked against the wall, composition is loyalty and brotherhood, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-david-spares-saul-in-the-cave": "game box art, painting in illuminated manuscript style, inside a dark cave at Ein Gedi, David crouching near Saul who is entering unaware, Saul's robe spread wide at the cave entrance, David's hand hovering near the hem, torchlight flickering, composition is tight and tense, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-desert-mirage": "game box art, painting in illuminated manuscript style, single figure walking in shimmering heat across white desert ground, the horizon dissolves into heat haze, on the ground faint reflections show the faces of his men back at camp, surreal but controlled the disorientation of the fugitive, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-dry-place": "game box art, painting in illuminated manuscript style, wide desert vista under a single palm, a tiny figure David sits beneath it sling at his side a single waterskin beside him, scale emphasizes solitude, horizon line is low, ochre umber and a single green palm frond, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-fugitives-path": "game box art, painting in illuminated manuscript style, David silhouetted against a rocky Judean cliff face, cloak billowing, looking back toward a distant Philistine encampment on the horizon, three tiny enemy figures pursue along a winding mountain trail, parchment sky with copperpage sepia wash, focus on isolation and pursuit, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-hunter-hunted": "game box art, painting in illuminated manuscript style, three-panel manuscript-page layout left panel shows David and a scout hidden behind rock watching center panel shows Saul's army marching unaware right panel shows a narrow path where David's band will ambush, used as if this were a medieval chronicle page, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-ish-bosheth-assassinated": "game box art, painting in illuminated manuscript style, two captains Baanah and Rechab entering Ishbosheth's bedroom at noon, daylight streaming through the window, Ishbosheth lying on his bed, the murderers lowering a spear, composition is calculated and cold, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-last-stand-at-ziklag": "game box art, painting in illuminated manuscript style, before a burned and looted settlement David kneels among smoldering timbers head bowed, behind him his warriors grip weapons, below them in shadow raiders ride away into the desert, composition is low and crushing, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-nabal-s-whetting": "game box art, painting in illuminated manuscript style, Nabal at his rich table in Carmel, feasting with his sons, golden cups and roasted meat, a servant standing at the edge of the scene looking shocked, outside the window Abigail leads donkeys laden with gifts, contrast between opulence and the dust road beyond, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-narrow-pass": "game box art, painting in illuminated manuscript style, top-down flattened view of a mountain pass at night, small lights flicker along the winding path, the composition reads like a tactical map on parchment, figures are tiny, tension comes from the constricted space, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded indigo, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-philistine-lord": "game box art, painting in illuminated manuscript style, Achish seated on a folding stool in a field tent flanked by two spearmen, he holds a goblet expression unreadable, David stands before him stripped of his armor bowing slightly a fugitive at the mercy of a foreign lord, warm lamplight, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-refugee-column": "game box art, painting in illuminated manuscript style, from behind a moving column of civilians with bundles and children passes through a narrow pass, soldiers guard the flanks, the scene is intimate and human the company aspect of David's warband, parchment tones with faded indigo sky, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded indigo, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-river-crossing": "game box art, painting in illuminated manuscript style, figures fording a shallow stony river at dawn, an ox and a donkey precede a woman with a child, warriors lead the way and guard the rear, mist rises from the water, the scene is pastoral but tense everyone is fleeing, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded indigo, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-saul-and-jonathan-slain": "game box art, painting in illuminated manuscript style, on the heights of Gilboa, Saul leaning on his own sword and falling, Jonathan fallen across him, armor scattered, Philistine chariots visible in the valley, a single Israelite bow abandoned in the foreground, composition is tragic and still, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-saul-at-the-javelin": "game box art, painting in illuminated manuscript style, Saul seated on a high bench in his palace, a javelin in his right hand poised to throw at David who stands near the wall with a harp in hand, court attendants frozen in the background, dramatic tension in the still moment before violence, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-shepherd-king": "game box art, painting in illuminated manuscript style, David seated on a natural stone throne in a cave listening to an elder, lighting from a single torch, around them men repair weapons and tend wounds, a sense of rest before the next journey, warm amber tones, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-shepherds-flute": "game box art, painting in illuminated manuscript style, David seated on a rocky outcrop at sunset resting between journeys, a simple shepherd's pipe is in his hand not a weapon, below a small flock of goats grazes, the image is serene almost pastoral, the tension is in the viewer knowing this peace will end, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-shield-wall": "game box art, painting in illuminated manuscript style, low-angle view from ground level three Israelite spearmen locked in shield wall facing impossibly numerous Amalekite raiders, dust motion lines tension, foreground shows the rear of the shields plain leather no heraldry, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-surprise-attack": "game box art, painting in illuminated manuscript style, dynamic motion composition three Israelite warriors burst through a low brush line at the edge of a camp weapons raised, the enemy camp sprawls behind them figures still sleeping, dust and motion, perspective is from the enemy camp looking toward the attackers, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-the-amalekite-messenger": "game box art, painting in illuminated manuscript style, an Amalekite runner stumbling into David's camp at Ziklag, clothes torn and dusty, holding up a crown and armlet, David's men drawing weapons to kill him, David's hand raised in horror and disbelief, composition is dramatic and tense, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-the-battle-at-gibeon": "game box art, painting in illuminated manuscript style, two armies arrayed at the pool of Gibeon, Israelite spearmen on one side, Joab and Abner watching from opposite hills, Asahel running toward Abner with spear raised, dust and crowd, composition is tactical and tense, hand-painted historical illustration, aged parchment background, ink outlines with muted watercolor wash in ochre umber and faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-the-board-at-rest": "game box art, painting in illuminated manuscript style, the actual game board the 8x8 hex grid rendered as aged parchment sits on a wooden table, two empty command card slots face a single commander token, a bronze sword rests diagonally across the corner of the board, everything still, the viewer is invited to sit down and play, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-the-egyptian-slave": "game box art, painting in illuminated manuscript style, a wounded Egyptian slave sitting under a desert shrub, David kneeling beside him offering bread and water, the slave's face gaunt with exhaustion, a vast empty desert stretching behind them, composition is intimate and compassionate, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-the-pursuit-of-the-amalekites": "game box art, painting in illuminated manuscript style, David's band riding hard across a dusty plain, a slave leading an Egyptian on a donkey ahead, an Amalekite camp visible in the distance spilling over a rocky ridge, composition is motion and dust, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-the-showbread-at-nob": "game box art, painting in illuminated manuscript style, interior of a humble sanctuary at Nob, a priest in simple linen robes places bread on a golden table, David standing nearby with a sword at his hip, stone walls and hanging curtains, lamplight, composition is reverent and quiet, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-the-threshing-floor-of-araunah": "game box art, painting in illuminated manuscript style, an angel of the Lord standing with a drawn sword on a threshing floor outside Jerusalem, David looking up from his knees in supplication, Araunah the Jebusite offering his threshing floor and oxen, smoke rising from a sacrifice already burning, composition is atonement and mercy, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-the-well-of-bethlehem": "game box art, painting in illuminated manuscript style, three mighty men breaking through the Philistine line to reach the well by the gate of Bethlehem, water pouring into a cup, David looking on with gratitude and awe, the gate in the background with Philistine banners, composition is heroism and fellowship, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-warlords-tent": "game box art, painting in illuminated manuscript style, interior of a Philistine commander's tent at dusk, Achish seated on a low couch flanked by two spearmen, he holds a goblet expression unreadable, David stands before him stripped of his armor bowing slightly a fugitive at the mercy of a foreign lord, warm lamplight, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-watcher-on-the-hill": "game box art, painting in illuminated manuscript style, David standing alone on a rocky outcrop, shield at his feet, staff in hand, below in the valley a Philistine camp smolders, smoke in thin wispy lines, composition is vertical to fit box proportions, minimal figures one man one landscape, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-watchfire": "game box art, painting in illuminated manuscript style, night camp on a ridge above a valley, a single watchfire burns, figures sleep wrapped in cloaks around it, one sentry stands at the edge of the light looking out, the sky is ink-black with a few stars, simple quiet tense, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded indigo, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-wilderness-march": "game box art, painting in illuminated manuscript style, wide panoramic composition a winding column of small figures moves through a rocky desert valley, dust rises, perspective from above but not a map more like a medieval chronicle illustration flattened into a single vertical plane, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-wounded-bear": "game box art, painting in illuminated manuscript style, close-up of a hand gripping a spear shaft thrust into fur, a wounded bear rears, David's boot and the lower half of his tunic are visible, blood is implied through a single stroke of faded crimson, mythic and primal grounded in the historical David legend, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "box-art-ziklag-burned": "game box art, painting in illuminated manuscript style, the settlement of Ziklag smoldering at dawn, walls collapsed, smoke rising, David's warriors fall to their knees weeping, the Amalekite raiders visible as tiny dust specks on the horizon fleeing with captives, composition is low and crushing, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",

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

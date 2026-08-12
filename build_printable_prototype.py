#!/usr/bin/env python3
"""
build_printable_prototype.py — Generates a print-and-play PDF for The Exile King prototype.

Usage:
    python build_printable_prototype.py [options]

Options:
    --output PATH              Output PDF path (default: prototype/printable_prototype.pdf)
    --art-dir PATH             ComfyUI output prototype directory
    --queue PATH               generation_queue.json path
    --review-report PATH       full_review.json path for keep/trash filtering
    --dpi N                    Output DPI (default: 300)
    --faction FACTION          Limit to specific faction(s) (comma-separated)
    --scope mvp|full           mvp = 4 core factions, full = all factions
    --unreviewed-ok            Use all non-review-dir images without review filtering
    --no-art                   Generate PDF with placeholders (no art loading)
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path
from collections import defaultdict, OrderedDict
from PIL import Image, ImageDraw, ImageFont

# ============================================================================
# Constants
# ============================================================================

DPI_DEFAULT = 300
CARD_W = 750    # 2.5" @ 300 DPI
CARD_H = 1050   # 3.5" @ 300 DPI
DISC_DIAM = 600  # 2" @ 300 DPI
TOKEN_DIAM = 300  # 1" @ 300 DPI
PAGE_W = 2550   # US Letter @ 300 DPI
PAGE_H = 3300   # US Letter @ 300 DPI
MARGIN = 75     # 0.25" margin

PARCHMENT_BG = (250, 245, 230)
PARCHMENT_BORDER = (160, 140, 100)
DARK_INK = (40, 30, 20)
TEAL = (0, 128, 128)
GOLD = (212, 175, 55)
RED = (220, 20, 60)
PURPLE = (128, 0, 128)
AMBER = (255, 191, 0)
CARD_BACK_COLOR = (80, 60, 40)

MVP_FACTIONS = [
    "David's Company",
    "Jonathan's Followers",
    "Achish's Host",
    "Lord of Ekron's Host",
]

ALL_FACTIONS = MVP_FACTIONS + [
    "Saul's Kingdom",
    "Amalekites",
]

FACTION_DIRS = {
    "David's Company": "DAVIDS_COMPANY",
    "Jonathan's Followers": "JONATHANS_FOLLOWERS",
    "Achish's Host": "PHILISTINES",
    "Lord of Ekron's Host": "EKRONS_HOST",
    "Saul's Kingdom": "SAULS_KINGDOM",
    "Amalekites": "AMALEKITES",
}

FACTION_COLORS = {
    "David's Company": TEAL,
    "Jonathan's Followers": GOLD,
    "Achish's Host": RED,
    "Lord of Ekron's Host": RED,
    "Saul's Kingdom": PURPLE,
    "Amalekites": AMBER,
}

COMMANDER_DISC_NAMES = {
    "David's Company": "David",
    "Jonathan's Followers": "Jonathan",
    "Achish's Host": "Achish",
    "Lord of Ekron's Host": "Philistine Lord",
}

UNIT_STATS = {
    "David": (1, 2, 1, 2, 2),
    "Jonathan": (1, 2, 1, 2, 2),
    "Achish": (1, 2, 1, 2, 2),
    "Philistine Lord": (1, 2, 1, 2, 2),
    "Abner": (1, 2, 1, 2, 2),
    "Chieftain": (1, 2, 1, 2, 2),
    "Swordsman": (1, 2, 1, 2, 2),
    "Spearman": (2, 2, 1, 2, 2),
    "Shield Bearer": (1, 1, 2, 3, 1),
    "Scout": (2, 1, 1, 1, 3),
    "Archer": (2, 2, 1, 2, 2),
    "Slinger": (3, 1, 1, 2, 3),
    "Loyal Guard": (1, 2, 1, 2, 2),
    "Elite Archer": (2, 2, 1, 2, 2),
    "Giant": (1, 3, 2, 4, 1),
    "Heavy Infantry": (1, 2, 2, 3, 1),
    "Champion": (1, 3, 2, 4, 2),
    "Chariot": (1, 2, 1, 2, 3),
    "Raider": (1, 2, 0, 1, 3),
    "Desert Mount": (1, 2, 1, 1, 3),
    "Desert Scout": (1, 1, 0, 1, 4),
    "Israelite Archer": (3, 2, 1, 1, 0),
    "Royal Guard": (1, 2, 2, 3, 1),
    "Benjamite Spearman": (1, 2, 1, 2, 2),
    "Elite Bodyguard": (1, 2, 1, 2, 2),
    "Officer": (1, 1, 0, 2, 2),
    "Outcast": (1, 2, 1, 1, 2),
    "Refugee": (1, 0, 1, 1, 1),
    "Veteran": (1, 2, 1, 2, 2),
    "Mighty Men": (1, 2, 1, 2, 2),
}

# Card name → prompt_key override
CARD_NAME_TO_PROMPT_KEY = {
    "Formation Advance": "phalanx-advance",
    "Benjamin's Arrow": "jonathans-mark",
    "True Aim": "perfect-shot",
    "Covenant Guard": "guard-formation",
    "Philistine Advance": "swordsmen-advance",
    "Iron Resolve": "swordsmen-formation",
    "Shield Advance": "phalanx-advance",
    "Ekron Hedge": "spear-wall",
    "Ekron Line": "spearman-formation",
    "Ekron Screen": "spearman-screen",
    "Iron Bulwark": "shield-wall",
    "Tribe's Wall": "spear-wall",
    "Tribe's Screen": "spearman-screen",
    "Covenant Volley": "archer-volley",
    "Benjamin's Eye": "archer-formation",
    "Covenant Shield": "shield-wall",
    "Commander's Advance": "phalanx-advance",
    "Covenant Advance": "swordsmen-advance",
    "Covenant Hold": "swordsmen-formation",
    "Valley Shot": "circle-and-strike",
    "Benjamite Volley": "stone-volley",
    "Philistine Spearmen": "spear-wall",
    "Giant's Might": "giants-might",
    "Coastal Charge": "chariot-charge",
    "Plain Breaker": "chariot-formation-1",
    "Hit and Run": "chariot-formation-2",
    "Coastal Sling": "circle-and-strike",
    "Stone Storm": "stone-volley",
    "Battle Cry": "battle-cry",
    "Tactical Assessment": "tactical-assessment",
    "Last Resort": "last-resort",
    "Flanking Maneuver": "flanking-maneuver",
    "Siege Engineer": "siege-engineer",
    "Shepherd's Call": "shepherds-call",
    "Jonathan's Charge": "jonathans-charge",
    "Ekron's Decree": "ekrons-decree",
    "Philistine Might": "philistine-might",
}

# Commander card order in .md file
COMMANDER_CARD_ORDER = {
    "David's Company": [
        "Shepherd's Call", "Battle Cry", "Tactical Assessment",
        "Last Resort", "Flanking Maneuver", "Siege Engineer",
    ],
    "Jonathan's Followers": [
        "Jonathan's Charge", "Battle Cry", "Tactical Assessment",
        "Last Resort", "Flanking Maneuver", "Siege Engineer",
    ],
    "Achish's Host": [
        "Philistine Might", "Battle Cry", "Tactical Assessment",
        "Last Resort", "Flanking Maneuver", "Siege Engineer",
    ],
    "Lord of Ekron's Host": [
        "Ekron's Decree", "Battle Cry", "Tactical Assessment",
        "Last Resort", "Flanking Maneuver", "Siege Engineer",
    ],
}

# Unit disc prompt key overrides
UNIT_DISC_PROMPT_KEYS = {
    "David": "david_commander",
    "Jonathan": "jonathan_commander",
    "Achish": "achish_commander",
    "Philistine Lord": "philistine_lord_commander",
    "Abner": "abner",
    "Chieftain": "chieftain",
    "Loyal Guard": "loyal_guard_jonathan",
    "Elite Archer": "elite_archer_jonathan",
    "Giant": "giant_achish",
    "Chariot": "chariot_ekron",
}

# Faction-specific prompt keys for shared unit types
FACTION_UNIT_PROMPT_KEYS = {
    "David's Company": {
        "Swordsman": "swordsman_david",
        "Spearman": "spearman_david",
        "Slinger": "slinger_david",
        "Scout": "scout_david",
        "Shield Bearer": "shield_bearer_david",
        "Archer": "archer_jonathan",
    },
    "Jonathan's Followers": {
        "Archer": "archer_jonathan",
        "Spearman": "spearman_jonathan",
        "Shield Bearer": "shield_bearer_jonathan",
    },
    "Achish's Host": {
        "Swordsman": "swordsman_achish",
        "Spearman": "spearman_achish",
        "Archer": "archer_achish",
        "Shield Bearer": "shield_bearer_achish",
    },
    "Lord of Ekron's Host": {
        "Swordsman": "swordsman_ekron",
        "Spearman": "spearman_ekron",
        "Slinger": "slinger_ekron",
        "Shield Bearer": "shield_bearer_ekron",
    },
}

# Post-MVP files to skip
SKIP_RELATIVE_PATHS = {
    "PHILISTINES/heavy_infantry/HEAVY_INFANTRY.md",
    "PHILISTINES/champion/CHAMPION.md",
    "PHILISTINES/lords/LORDS.md",
    "PHILISTINES/chariot/CHARIOT.md",
    "PHILISTINES/slinger/SLINGER.md",
    "AMALEKITES/raider/RAIDER.md",
    "AMALEKITES/desert_scout/DESERT_SCOUT.md",
    "AMALEKITES/desert_mount/DESERT_MOUNT.md",
    "SAULS_KINGDOM/royal_guard/ROYAL_GUARD.md",
    "SAULS_KINGDOM/benjamite_spearman/BENJAMITE_SPEARMAN.md",
    "SAULS_KINGDOM/israelite_archer/ISRAELITE_ARCHER.md",
    "SAULS_KINGDOM/elite_bodyguard/ELITE_BODYGUARD.md",
    "SAULS_KINGDOM/OFFICER.md",
    "AMALEKITES/chieftain/CHIEFTAIN.md",
    "DAVIDS_COMPANY/outcast/OUTCAST.md",
    "DAVIDS_COMPANY/refugee/REFUGEE.md",
    "DAVIDS_COMPANY/veteran/VETERAN.md",
    "DAVIDS_COMPANY/mighty_man/MIGHTY_MAN.md",
}


# ============================================================================
# Font Management
# ============================================================================

_font_cache = {}

def get_font(size, bold=False):
    """Load Arial font at the specified size."""
    key = (size, bold)
    if key in _font_cache:
        return _font_cache[key]
    font_name = "arialbd.ttf" if bold else "arial.ttf"
    win_fonts = os.path.join(os.getenv("WINDIR", r"C:\Windows"), "Fonts")
    path = os.path.join(win_fonts, font_name)
    if os.path.exists(path):
        font = ImageFont.truetype(path, size)
    else:
        font = ImageFont.load_default()
    _font_cache[key] = font
    return font


def text_width(text, font):
    bbox = font.getbbox(text)
    return bbox[2] - bbox[0]


def text_height(text, font):
    bbox = font.getbbox(text)
    return bbox[3] - bbox[1]


def wrap_text(text, font, max_width):
    """Wrap text to fit within max_width."""
    if not text:
        return []
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = current + (" " if current else "") + word
        if text_width(test, font) <= max_width or not current:
            current = test
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_text_centered(draw, text, cx, y, font, fill=DARK_INK):
    """Draw text centered at x=cx."""
    w = text_width(text, font)
    draw.text((cx - w // 2, y), text, font=font, fill=fill)
    return y + text_height(text, font) + 4


def draw_text_multiline_centered(draw, text, cx, y, font, max_width,
                                  fill=DARK_INK, line_spacing=1.3):
    """Draw wrapped, centered text. Returns final y position."""
    lines = wrap_text(text, font, max_width)
    for line in lines:
        w = text_width(line, font)
        h = text_height(line, font)
        draw.text((cx - w // 2, y), line, font=font, fill=fill)
        y += int(h * line_spacing)
    return y


def draw_text_multiline_left(draw, text, x, y, font, max_width,
                              fill=DARK_INK, line_spacing=1.3):
    """Draw wrapped, left-aligned text. Returns final y position."""
    lines = wrap_text(text, font, max_width)
    for line in lines:
        h = text_height(line, font)
        draw.text((x, y), line, font=font, fill=fill)
        y += int(h * line_spacing)
    return y


def make_rounded_rect(w, h, radius, fill, border_color=None, border_width=0):
    """Create a rounded rectangle image."""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        [0, 0, w, h], radius=radius, fill=fill,
        outline=border_color if border_color else None,
        width=border_width,
    )
    return img


def resize_art_for_area(art_path, target_w, target_h):
    """Load art and resize to fit within target dimensions, preserving aspect ratio."""
    if not art_path or not os.path.exists(art_path):
        return None
    img = Image.open(art_path).convert("RGBA")
    # Resize preserving aspect ratio
    img.thumbnail((target_w, target_h), Image.Resampling.LANCZOS)
    return img


# ============================================================================
# Art Inventory
# ============================================================================

class ArtInventory:
    """Manages art assets from filesystem + generation queue + review report."""

    def __init__(self, art_dir, queue_path, review_path=None, no_art=False):
        self.art_dir = art_dir
        self.queue_path = queue_path
        self.review_path = review_path
        self.no_art = no_art
        self.queue_data = []
        self.prefix_to_prompt_key = {}
        self.prompt_key_to_prefixes = defaultdict(set)
        self.filename_to_status = {}
        self.art_files = defaultdict(list)  # prompt_key → [file paths]
        self.commander_art = defaultdict(dict)  # commander → {card_index: [file paths]}

        if not no_art:
            self._load_queue()
            self._load_review()
            self._scan_art()

    def _load_queue(self):
        if os.path.exists(self.queue_path):
            with open(self.queue_path, "r", encoding="utf-8") as f:
                self.queue_data = json.load(f)
            for item in self.queue_data:
                pk = item.get("prompt_key", "")
                prefix = item.get("filename_prefix", "")
                if pk and prefix:
                    self.prefix_to_prompt_key[prefix] = pk
                    self.prompt_key_to_prefixes[pk].add(prefix)

    def _load_review(self):
        if self.review_path and os.path.exists(self.review_path):
            with open(self.review_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for img in data.get("images", []):
                fn = os.path.basename(img["filename"].replace("\\", "/"))
                self.filename_to_status[fn] = img.get("decision", "UNKNOWN")

    def _scan_art(self):
        if not os.path.exists(self.art_dir):
            return
        for root, dirs, files in os.walk(self.art_dir):
            dirs[:] = [d for d in dirs if d not in
                       ("to_trash", "to_duplicates", "to_review")]
            for f in files:
                if not f.endswith(".png"):
                    continue
                full_path = os.path.join(root, f)
                status = self.filename_to_status.get(f, "unknown")
                if status == "TRASH":
                    continue
                # Determine prompt_key from filename pattern
                m = re.match(r"^(.+?)_(\d{5})_?\.", f)
                if m:
                    prefix = m.group(1)
                    pk = self.prefix_to_prompt_key.get(prefix)
                    if pk:
                        self.art_files[pk].append(full_path)
                    elif prefix in ("card_back", "command-card-back",
                                    "commander-aura-marker", "activation-token",
                                    "lost-pile-marker", "reward-panel",
                                    "end-turn-button", "hp-bar-bg", "hp-bar-fill",
                                    "card-frame-template", "ui-card-slot",
                                    "ui-commander-aura", "ui-portrait-frame"):
                        self.art_files[prefix].append(full_path)
                else:
                    stem = os.path.splitext(f)[0]
                    self.art_files[stem].append(full_path)

    def get_art(self, prompt_key):
        """Get best art file for a prompt key."""
        files = self.art_files.get(prompt_key, [])
        if not files:
            return None
        for f in files:
            fn = os.path.basename(f)
            if self.filename_to_status.get(fn) == "keep":
                return f
        return files[0]

    def get_commander_art(self, faction, card_index=0):
        prefix_map = {
            "David's Company": "david",
            "Jonathan's Followers": "jonathan",
            "Achish's Host": "achish",
            "Lord of Ekron's Host": "philistine-lord",
        }
        prefix = prefix_map.get(faction)
        if not prefix:
            return None
        target = "{}-{:02d}".format(prefix, card_index + 1)
        for pk, files in self.art_files.items():
            for f in files:
                fn = os.path.basename(f)
                if fn.startswith(target + "_"):
                    return f
        return None

    def get_unit_disc_art(self, unit_name, faction=None):
        # Check faction-specific mapping first
        if faction and faction in FACTION_UNIT_PROMPT_KEYS:
            pk = FACTION_UNIT_PROMPT_KEYS[faction].get(unit_name)
            if pk:
                return self.get_art(pk)
        # Check global mapping
        pk = UNIT_DISC_PROMPT_KEYS.get(unit_name)
        if pk:
            return self.get_art(pk)
        # Try normalizing
        norm = unit_name.lower().replace(" ", "-")
        return self.get_art(norm)

    def get_card_back_art(self):
        for pk in ("card_back", "command-card-back"):
            art = self.get_art(pk)
            if art:
                return art
        return None

    def get_hex_tile_art(self, terrain="grass"):
        return self.get_art("hex_" + terrain) or self.get_art("hex-" + terrain) or self.get_art(terrain)

    def get_ui_art(self, name):
        return self.get_art(name)


# ============================================================================
# Card .md Parser
# ============================================================================

class CardData:
    def __init__(self, name, top_initiative, bottom_initiative,
                 top_text, bottom_text, card_type="standard",
                 activations_top=None, activations_bottom=None,
                 unit_name="", faction="", is_formation=False):
        self.name = name
        self.top_initiative = top_initiative
        self.bottom_initiative = bottom_initiative
        self.top_text = top_text
        self.bottom_text = bottom_text
        self.card_type = card_type
        self.activations_top = activations_top
        self.activations_bottom = activations_bottom
        self.unit_name = unit_name
        self.faction = faction
        self.is_formation = is_formation
        self.top_art_path = None
        self.bottom_art_path = None


def parse_table_card(lines, start_idx, card_name, unit_name, faction):
    """Parse a table-format card starting at start_idx.
    Returns (CardData, next_index).
    """
    i = start_idx
    top_init = None
    bot_init = None
    top_effect = ""
    bot_effect = ""

    while i < len(lines):
        line = lines[i].strip()

        # Check for table header: | | Top | Bottom |
        if line.startswith("|") and "Top" in line and "Bottom" in line:
            i += 1
            # Skip separator row
            if i < len(lines) and lines[i].strip().startswith("|") and "---" in lines[i]:
                i += 1
            # Read data rows
            while i < len(lines):
                l = lines[i].strip()
                if not l.startswith("|"):
                    break
                if l.startswith("| ---") or l.startswith("|==="):
                    i += 1
                    continue
                cells = [c.strip() for c in l.strip("|").split("|")]
                cells = [c for c in cells if c]
                if len(cells) >= 2:
                    row_type = cells[0].lower()
                    if "initiative" in row_type:
                        vals = cells[1].split()
                        if vals:
                            try:
                                top_init = int(vals[0])
                            except ValueError:
                                pass
                        if len(cells) >= 3:
                            vals2 = cells[2].split()
                            if vals2:
                                try:
                                    bot_init = int(vals2[0])
                                except ValueError:
                                    pass
                    elif "effect" in row_type or len(cells) == 3 and cells[0]:
                        top_effect = cells[1] if len(cells) > 1 else ""
                        bot_effect = cells[2] if len(cells) > 2 else ""
                i += 1
            break
        i += 1

    card = CardData(
        name=card_name,
        top_initiative=top_init or 0,
        bottom_initiative=bot_init or 0,
        top_text=top_effect,
        bottom_text=bot_effect,
        card_type="standard",
        unit_name=unit_name,
        faction=faction,
    )
    return card, i


def parse_formation_card(lines, start_idx, unit_name, faction):
    """Parse a formation card (TOP ACTION / BOTTOM ACTION format).
    Returns (CardData, next_index).
    """
    i = start_idx
    top_name = ""
    bottom_name = ""
    top_text_parts = []
    bottom_text_parts = []
    top_act = None
    bot_act = None
    current_section = None  # "top" or "bottom"

    # First, try to find the Formation header to get card names
    formation_header = lines[start_idx - 1] if start_idx > 0 else ""

    while i < len(lines):
        line = lines[i].strip()

        # Check for TOP ACTION heading
        if line.startswith("### TOP ACTION —") or line.startswith("### TOP ACTION -"):
            top_name = line.split("—", 1)[-1].strip() if "—" in line else line.split("-", 2)[-1].strip()
            current_section = "top"
            top_text_parts = []
            i += 1
            # Check for activations in same line or next line
            act_match = re.search(r"Activations:\s*(\d+)", line)
            if act_match:
                top_act = int(act_match.group(1))
            continue

        # Check for BOTTOM ACTION heading
        if line.startswith("### BOTTOM ACTION —") or line.startswith("### BOTTOM ACTION -"):
            bottom_name = line.split("—", 1)[-1].strip() if "—" in line else line.split("-", 2)[-1].strip()
            current_section = "bottom"
            bottom_text_parts = []
            i += 1
            act_match = re.search(r"Activations:\s*(\d+)", line)
            if act_match:
                bot_act = int(act_match.group(1))
            continue

        # Check for **Activations:** line
        if line.startswith("**Activations:**"):
            act_match = re.search(r"(\d+)", line)
            if act_match:
                if current_section == "top":
                    top_act = int(act_match.group(1))
                elif current_section == "bottom":
                    bot_act = int(act_match.group(1))
            i += 1
            continue

        # Check for **Purpose:** line (skip)
        if line.startswith("**Purpose:**"):
            i += 1
            continue

        # Check for section separators or new headings
        if line.startswith("---") or line.startswith("### ") or line.startswith("## ") or line.startswith("# "):
            if current_section == "top" and line.startswith("---"):
                i += 1
                continue
            elif current_section == "bottom" and line.startswith("---"):
                i += 1
                continue
            # Hit a new heading - check if both sections have content
            if current_section == "bottom" and (top_text_parts or bottom_text_parts):
                # Save what we have so far as a formation card
                top_text = " ".join(top_text_parts)
                bot_text = " ".join(bottom_text_parts)
                display_name = top_name if top_name else (unit_name + " Formation")
                if not top_text:
                    top_text = top_name
                if not bot_text:
                    bot_text = bottom_name

                card = CardData(
                    name=display_name,
                    top_initiative=top_act or 0,
                    bottom_initiative=bot_act or 0,
                    top_text=top_text,
                    bottom_text=bot_text,
                    card_type="formation",
                    activations_top=top_act,
                    activations_bottom=bot_act,
                    unit_name=unit_name,
                    faction=faction,
                    is_formation=True,
                )
                return card, i
            # Not a formation card, or incomplete
            break

        # Accumulation
        if current_section == "top":
            if line:
                top_text_parts.append(line)
        elif current_section == "bottom":
            if line:
                bottom_text_parts.append(line)

        i += 1

    # End of file - build formation card if we have data
    if current_section in ("top", "bottom") and (top_text_parts or bottom_text_parts):
        top_text = " ".join(top_text_parts)
        bot_text = " ".join(bottom_text_parts)
        display_name = smart_title(top_name) if top_name else (unit_name + " Formation")
        if not top_text:
            top_text = top_name
        if not bot_text:
            bot_text = bottom_name

        card = CardData(
            name=display_name,
            top_initiative=top_act or 0,
            bottom_initiative=bot_act or 0,
            top_text=top_text,
            bottom_text=bot_text,
            card_type="formation",
            activations_top=top_act,
            activations_bottom=bot_act,
            unit_name=unit_name,
            faction=faction,
            is_formation=True,
        )
        return card, i

    return None, i


def parse_card_md(path, unit_name="", faction=""):
    """Parse a card .md file and return a list of CardData objects."""
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().split("\n")

    # Extract unit_name and faction from metadata if not provided
    if not unit_name:
        for line in lines:
            if line.startswith("# "):
                unit_name = line[2:].strip()
                break

    cards = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Formation card header
        if (line.startswith("## Formation Card:") or line.startswith("## Formation:")):
            # Get formation name
            form_text = line.split(":", 1)[1].strip() if ":" in line else ""
            parts = form_text.split("/")
            top_name = parts[0].strip()
            bottom_name = parts[1].strip() if len(parts) > 1 else ""
            top_name = smart_title(top_name)
            if bottom_name:
                bottom_name = smart_title(bottom_name)

            # Skip to TOP ACTION or the first heading after the formation header
            i += 1
            while i < len(lines):
                l = lines[i].strip()
                if l.startswith("### TOP ACTION"):
                    break
                if l.startswith("### ") and not l.startswith("### TOP ACTION"):
                    # Table card or other section before formation
                    break
                if l.startswith("## ") and not l.startswith("## Formation"):
                    break
                i += 1

            # Parse formation card
            card, i = parse_formation_card(lines, i, unit_name, faction)
            if card:
                cards.append(card)
            continue

        # Standard table card
        if line.startswith("### ") and not line.startswith("### TOP") and not line.startswith("### BOTTOM"):
            card_name = line[4:].strip()
            # Skip empty or separator headings
            if card_name and "---" not in card_name:
                card, i = parse_table_card(lines, i + 1, card_name, unit_name, faction)
                if card:
                    cards.append(card)
            continue

        i += 1

    return cards


def parse_all_cards(base_dir, factions=None):
    """Parse all card .md files recursively."""
    all_cards = []
    unit_type_dir = os.path.join(base_dir, "command_cards", "unit_types")

    if not os.path.exists(unit_type_dir):
        return all_cards

    for faction_folder in sorted(os.listdir(unit_type_dir)):
        faction_path = os.path.join(unit_type_dir, faction_folder)
        if not os.path.isdir(faction_path):
            continue

        # Determine faction name
        faction_name = None
        for fn, ff in FACTION_DIRS.items():
            if ff == faction_folder:
                faction_name = fn
                break
        if faction_name and factions and faction_name not in factions:
            continue
        if not faction_name:
            continue

        for root, dirs, files in os.walk(faction_path):
            for f in files:
                if not f.endswith(".md"):
                    continue
                rel_path = os.path.relpath(
                    os.path.join(root, f), unit_type_dir).replace("\\", "/")
                if rel_path in SKIP_RELATIVE_PATHS:
                    continue

                unit_name = os.path.basename(root)
                unit_name_pretty = unit_name.replace("_", " ").title()
                # Fix common names
                name_fixes = {
                    "Achish": "Achish",
                    "Abner": "Abner",
                    "Chieftain": "Chieftain",
                }
                unit_name_pretty = name_fixes.get(unit_name_pretty, unit_name_pretty)

                cards = parse_card_md(
                    os.path.join(root, f),
                    unit_name=unit_name_pretty,
                    faction=faction_name,
                )
                all_cards.extend(cards)

    return all_cards


# ============================================================================
# Card Rendering
# ============================================================================

def render_card(card, inventory, dpi=DPI_DEFAULT):
    """Render a single command card to a PIL Image with top/bottom split art."""
    scale = dpi / DPI_DEFAULT
    w = int(CARD_W * scale)
    h = int(CARD_H * scale)
    img = Image.new("RGBA", (w, h), PARCHMENT_BG)
    draw = ImageDraw.Draw(img)

    ob = int(4 * scale)
    ib = int(2 * scale)
    draw.rectangle([0, 0, w - ob, h - ob], outline=DARK_INK, width=ob)
    draw.rectangle([ib // 2, ib // 2, w - ib // 2 - ib, h - ib // 2 - ib],
                   outline=PARCHMENT_BORDER, width=ib)

    mid_y = h // 2
    divider_h = int(3 * scale)
    draw.rectangle([ob, mid_y - divider_h // 2, w - ob, mid_y + divider_h // 2], fill=DARK_INK)

    title_h = int(20 * scale)
    title_y = h - ob - title_h
    draw.rectangle([ob, title_y, w - ob, h - ob], fill=FACTION_COLORS.get(card.faction, (100, 100, 100)))
    title_font = get_font(int(9 * scale), bold=True)
    draw_text_centered(draw, card.faction.upper(), w // 2, title_y + int(5 * scale),
                       title_font, fill=(255, 255, 255))

    art_w = w - ob - ib * 2
    art_h = int(300 * scale)

    def draw_half(base_y, art_path, action_text, initiative, side):
        art_x = ob + ib
        art_y = base_y + int(10 * scale)

        art = None
        if not inventory.no_art and art_path and os.path.exists(art_path):
            art = resize_art_for_area(art_path, art_w, art_h)

        if art:
            paste_x = art_x + (art_w - art.width) // 2
            paste_y = art_y + (art_h - art.height) // 2
            img.paste(art, (paste_x, paste_y), art)
        else:
            draw.rectangle([art_x, art_y, art_x + art_w, art_y + art_h], fill=(200, 200, 200))

        panel_h = int(140 * scale)
        panel_y = mid_y - divider_h // 2 - ob - ib - panel_h if side == "top" else title_y - int(4 * scale) - panel_h
        panel_x = art_x
        panel_w = art_w

        draw.rectangle([panel_x, panel_y, panel_x + panel_w, panel_y + panel_h],
                       fill=(20, 18, 15, 190))

        badge_r = int(22 * scale)
        badge_x = panel_x + int(8 * scale)
        badge_y = panel_y + int(8 * scale)
        draw.ellipse([badge_x, badge_y, badge_x + badge_r * 2, badge_y + badge_r * 2],
                     fill=(212, 175, 55))
        font_init = get_font(int(13 * scale), bold=True)
        bbox = font_init.getbbox(str(initiative))
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((badge_x + badge_r - tw // 2, badge_y + badge_r - th // 2),
                  str(initiative), font=font_init, fill=(20, 18, 15))

        label_font = get_font(int(10 * scale), bold=True)
        label_y = panel_y + int(8 * scale)
        draw_text_multiline_left(draw, side.upper() + " ACTION:", badge_x + badge_r * 2 + int(8 * scale), label_y,
                                 label_font, panel_w - badge_r * 2 - int(24 * scale), fill=(212, 175, 55))

        body_font = get_font(int(12 * scale))
        body_y = label_y + int(14 * scale)
        draw_text_multiline_left(draw, action_text, panel_x + int(8 * scale), body_y,
                                 body_font, panel_w - int(16 * scale), fill=(245, 240, 225))

    top_base = ob + ib
    bot_base = mid_y + divider_h // 2 + ob + ib

    top_init = card.top_initiative if isinstance(card.top_initiative, (int, float)) else 0
    bot_init = card.bottom_initiative if isinstance(card.bottom_initiative, (int, float)) else 0

    draw_half(top_base, card.top_art_path, card.top_text, top_init, "top")
    draw_half(bot_base, card.bottom_art_path, card.bottom_text, bot_init, "bottom")

    return img


def render_card_sheet(cards_list, inventory, dpi=DPI_DEFAULT):
    """Render a page with up to 9 cards in a 3x3 grid."""
    scale = dpi / DPI_DEFAULT
    cw = int(CARD_W * scale)
    ch = int(CARD_H * scale)
    spacing = int(10 * scale)
    margin = int(MARGIN * scale)

    page = Image.new("RGB", (PAGE_W, PAGE_H), (240, 235, 220))
    draw = ImageDraw.Draw(page)
    title_font = get_font(int(24 * scale), bold=True)
    draw_text_centered(draw, "Command Cards (" + str(len(cards_list)) + ")",
                       PAGE_W // 2, margin // 2, title_font, fill=DARK_INK)

    y = margin + int(10 * scale)
    idx = 0
    while idx < len(cards_list):
        for col in range(3):
            if idx + col >= len(cards_list):
                break
            card_img = render_card(cards_list[idx + col], inventory, dpi)
            x = margin + col * (cw + spacing)
            page.paste(card_img, (x, y), card_img)
        idx += 3
        y += ch + spacing
        if y + ch > PAGE_H - margin:
            break

    return page


# ============================================================================
# Unit Disc Rendering
# ============================================================================

def render_unit_disc(unit_name, faction, stats, inventory, dpi=DPI_DEFAULT):
    """Render a single unit disc."""
    import math
    scale = dpi / DPI_DEFAULT
    diam = int(DISC_DIAM * scale)
    radius = diam // 2
    pad = int(20 * scale)
    iw, ih = diam + pad * 2, diam + pad * 2
    img = Image.new("RGBA", (iw, ih), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    color = FACTION_COLORS.get(faction, (100, 100, 100))
    bw = int(12 * scale)
    cx, cy = iw // 2, ih // 2

    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                 fill=(245, 240, 225), outline=color, width=bw)

    art = None
    if not inventory.no_art:
        art_path = inventory.get_unit_disc_art(unit_name, faction)
        if art_path:
            art = resize_art_for_area(art_path, int(diam * 0.7), int(diam * 0.7))

    if art:
        img.paste(art, (cx - art.width // 2, cy - radius + int(20 * scale)), art)
    else:
        draw.ellipse([cx - radius + int(20 * scale), cy - radius + int(20 * scale),
                      cx + radius - int(20 * scale), cy + radius - int(20 * scale)],
                     fill=(200, 200, 200))

    if stats:
        rng, atk, dfc, hp, mv = stats
        sf = get_font(int(16 * scale), bold=True)
        sy = cy + radius - int(55 * scale)
        stats_text = "R{} A{} D{} H{} M{}".format(rng, atk, dfc, hp, mv)
        tw = text_width(stats_text, sf)
        th = text_height(stats_text, sf)
        draw.rectangle([cx - tw // 2 - int(8 * scale), sy - int(4 * scale),
                        cx + tw // 2 + int(8 * scale), sy + th + int(4 * scale)],
                       fill=(30, 25, 20, 200))
        draw_text_centered(draw, stats_text, cx, sy, sf, fill=(245, 240, 225))

    nf = get_font(int(20 * scale), bold=True)
    ny = cy + radius - int(18 * scale)
    name_text = unit_name
    tw = text_width(name_text, nf)
    th = text_height(name_text, nf)
    draw.rectangle([cx - tw // 2 - int(10 * scale), ny - int(4 * scale),
                    cx + tw // 2 + int(10 * scale), ny + th + int(4 * scale)],
                   fill=(30, 25, 20, 210))
    draw_text_centered(draw, name_text, cx, ny, nf, fill=(245, 240, 225))

    return img


def render_disc_sheet(units, inventory, dpi=DPI_DEFAULT):
    """Render a page with multiple unit discs."""
    scale = dpi / DPI_DEFAULT
    diam = int(DISC_DIAM * scale)
    margin = int(MARGIN * scale)
    spacing = int(20 * scale)

    page = Image.new("RGB", (PAGE_W, PAGE_H), (240, 235, 220))
    draw = ImageDraw.Draw(page)
    title_font = get_font(int(24 * scale), bold=True)
    draw_text_centered(draw, "Unit Discs", PAGE_W // 2, margin // 2,
                       title_font, fill=DARK_INK)

    cols = (PAGE_W - margin * 2) // (diam + spacing)
    rows = (PAGE_H - margin * 2 - int(40 * scale)) // (diam + spacing)

    y = margin + int(30 * scale)
    idx = 0
    row = 0
    while idx < len(units) and row < rows:
        for col in range(min(cols, len(units) - idx)):
            u = units[idx + col]
            dimg = render_unit_disc(u["name"], u["faction"], u["stats"], inventory, dpi)
            x = margin + col * (diam + spacing) + diam // 2
            page.paste(dimg, (x - diam // 2, y), dimg)
        idx += cols
        y += diam + spacing
        row += 1
        if y + diam > PAGE_H - margin:
            break

    return page


# ============================================================================
# Hex Board Rendering
# ============================================================================

def render_hex_board(inventory, dpi=DPI_DEFAULT):
    """Render an 8x8 hex grid board."""
    import math
    scale = dpi / DPI_DEFAULT
    page = Image.new("RGB", (PAGE_W, PAGE_H), (240, 235, 220))
    draw = ImageDraw.Draw(page)

    margin = int(MARGIN * scale)
    hex_size = int(180 * scale)
    cols, rows = 8, 8
    total_w = cols * hex_size
    total_h = int(rows * hex_size * 0.866) + int(hex_size * 0.433)
    page_w_avail = PAGE_W - margin * 2
    page_h_avail = PAGE_H - margin * 2 - int(60 * scale)
    if total_w > page_w_avail:
        s = page_w_avail / total_w
        hex_size = int(hex_size * s)
        total_w = int(total_w * s)
        total_h = int(total_h * s)
    if total_h > page_h_avail:
        s = page_h_avail / total_h
        hex_size = int(hex_size * s)
        total_w = int(total_w * s)
        total_h = int(total_h * s)

    start_x = margin + (PAGE_W - margin * 2 - total_w) // 2
    start_y = margin + int(30 * scale)

    board_art = None
    if not inventory.no_art:
        board_art = inventory.get_art("playable_board")

    if board_art:
        board_img = Image.open(board_art).convert("RGB")
        board_img = board_img.resize((PAGE_W, PAGE_H), Image.Resampling.LANCZOS)
        page.paste(board_img, (0, 0))

        for r in range(rows):
            for c in range(cols):
                x = start_x + c * hex_size + (r % 2) * (hex_size // 2)
                y = start_y + r * int(hex_size * 0.866)

                corners = []
                for i in range(6):
                    angle = 60 * i - 30
                    ax = x + int(hex_size * math.cos(math.radians(angle)) * 0.5)
                    ay = y + int(hex_size * math.sin(math.radians(angle)) * 0.5)
                    corners.append((ax, ay))

                draw.polygon(corners, outline=(80, 70, 60, 120), width=int(1 * scale))

                cf = get_font(int(10 * scale), bold=True)
                draw_text_centered(draw, chr(65 + c) + str(r + 1), x, y, cf, fill=(50, 50, 50, 180))

        title_font = get_font(int(24 * scale), bold=True)
        draw_text_centered(draw, "8x8 Hex Grid Board", PAGE_W // 2, margin,
                           title_font, fill=DARK_INK)

        return page

    grass_art = inventory.get_hex_tile_art("grass") if not inventory.no_art else None
    rock_art = inventory.get_hex_tile_art("rock") if not inventory.no_art else None
    sand_art = inventory.get_hex_tile_art("sand") if not inventory.no_art else None

    pattern = []
    for r in range(8):
        row = []
        for c in range(8):
            row.append("grass" if (r + c) % 2 == 0 else "rock")
        pattern.append(row)

    for r in range(rows):
        for c in range(cols):
            x = start_x + c * hex_size + (r % 2) * (hex_size // 2)
            y = start_y + r * int(hex_size * 0.866)

            corners = []
            for i in range(6):
                angle = 60 * i - 30
                ax = x + int(hex_size * math.cos(math.radians(angle)) * 0.5)
                ay = y + int(hex_size * math.sin(math.radians(angle)) * 0.5)
                corners.append((ax, ay))

            terrain = pattern[r][c]
            tile_img = None
            target_s = hex_size
            if terrain == "grass" and grass_art:
                tile_img = resize_art_for_area(grass_art, target_s, target_s)
            elif terrain == "rock" and rock_art:
                tile_img = resize_art_for_area(rock_art, target_s, target_s)

            if tile_img:
                page.paste(tile_img, (x - tile_img.width // 2, y - tile_img.height // 2), tile_img)
            else:
                color = (200, 200, 180) if terrain == "grass" else (180, 180, 170)
                draw.polygon(corners, fill=color)

            draw.polygon(corners, outline=(80, 70, 60))

            cf = get_font(int(9 * scale), bold=True)
            draw_text_centered(draw, chr(65 + c) + str(r + 1), x, y, cf, fill=(50, 50, 50))

    title_font = get_font(int(24 * scale), bold=True)
    draw_text_centered(draw, "8x8 Hex Grid Board", PAGE_W // 2, margin,
                       title_font, fill=DARK_INK)

    return page


# ============================================================================
# Token Sheet Rendering
# ============================================================================

def render_token_sheet(inventory, dpi=DPI_DEFAULT):
    """Render a sheet of game tokens."""
    scale = dpi / DPI_DEFAULT
    page = Image.new("RGB", (PAGE_W, PAGE_H), (240, 235, 220))
    draw = ImageDraw.Draw(page)
    margin = int(MARGIN * scale)
    diam = TOKEN_DIAM
    spacing = int(20 * scale)

    title_font = get_font(int(24 * scale), bold=True)
    draw_text_centered(draw, "Tokens & Markers", PAGE_W // 2, margin // 2,
                       title_font, fill=DARK_INK)

    cols = (PAGE_W - margin * 2) // (diam + spacing)
    rows = (PAGE_H - margin * 2 - int(40 * scale)) // (diam + spacing)

    tokens = [
        ("Activation", (255, 200, 100), "ACTIVE"),
        ("Activation", (100, 100, 100), "USED"),
        ("Commander", GOLD, "DAVID"),
        ("Commander", TEAL, "JONATHAN"),
        ("Commander", RED, "ACHISH"),
        ("Commander", PURPLE, "SAUL"),
        ("Lost Pile", (180, 80, 80), "LOST"),
        ("Shield", (100, 150, 220), "+1 SHIELD"),
        ("Shield", (80, 120, 180), "+2 SHIELD"),
        ("HP", (220, 50, 50), "1 HP"),
        ("HP", (200, 40, 40), "2 HP"),
    ]

    y = margin + int(30 * scale)
    idx = 0
    row = 0
    while idx < len(tokens) and row < rows:
        for col in range(min(cols, len(tokens) - idx)):
            label, color, sublabel = tokens[idx + col]
            cx = margin + col * (diam + spacing) + diam // 2
            cy = y + diam // 2
            draw.ellipse([cx - diam // 2, cy - diam // 2, cx + diam // 2, cy + diam // 2],
                         fill=color, outline=(50, 40, 30), width=int(3 * scale))
            lf = get_font(int(10 * scale), bold=True)
            draw_text_centered(draw, label.upper(), cx, cy - int(10 * scale),
                               lf, fill=(20, 20, 20))
            sf = get_font(int(9 * scale))
            draw_text_centered(draw, sublabel, cx, cy + int(4 * scale),
                               sf, fill=(20, 20, 20))
        idx += cols
        y += diam + spacing
        row += 1
        if y + diam > PAGE_H - margin:
            break

    return page


# ============================================================================
# Card Back Sheet
# ============================================================================

def render_card_backs(inventory, dpi=DPI_DEFAULT):
    """Render a sheet of card backs."""
    scale = dpi / DPI_DEFAULT
    cw = int(CARD_W * scale)
    ch = int(CARD_H * scale)
    margin = int(MARGIN * scale)
    spacing = int(15 * scale)

    page = Image.new("RGB", (PAGE_W, PAGE_H), (240, 235, 220))
    draw = ImageDraw.Draw(page)
    title_font = get_font(int(24 * scale), bold=True)
    draw_text_centered(draw, "Card Backs", PAGE_W // 2, margin // 2,
                       title_font, fill=DARK_INK)

    cols = (PAGE_W - margin * 2) // (cw + spacing)
    rows = (PAGE_H - margin * 2 - int(40 * scale)) // (ch + spacing)

    back_art = None
    if not inventory.no_art:
        bp = inventory.get_card_back_art()
        if bp:
            back_art = resize_art_for_area(bp, cw, ch)

    y = margin + int(30 * scale)
    for _ in range(rows):
        x = margin
        for _ in range(cols):
            if back_art:
                page.paste(back_art, (x, y), back_art)
            else:
                outer_border = int(4 * scale)
                draw.rectangle([x, y, x + cw - outer_border, y + ch - outer_border],
                               fill=PARCHMENT_BG, outline=DARK_INK, width=outer_border)
                inner_border = int(2 * scale)
                draw.rectangle([x + outer_border // 2, y + outer_border // 2,
                                x + cw - outer_border // 2 - inner_border, y + ch - outer_border // 2 - inner_border],
                               outline=PARCHMENT_BORDER, width=inner_border)
                draw_text_centered(draw, "THE EXILE KING",
                                   x + cw // 2, y + ch // 2,
                                   get_font(int(14 * scale), bold=True), fill=DARK_INK)
            x += cw + spacing
        y += ch + spacing
        if y + ch > PAGE_H - margin:
            break

    return page


# ============================================================================
# Rules Reference
# ============================================================================

def render_rules_reference(dpi=DPI_DEFAULT):
    """Render rules reference page(s). Yields PIL Images."""
    scale = dpi / DPI_DEFAULT
    sections = [
        ("SETUP", [
            "1. Choose army size: Small (6 units), Medium (8), or Large (10)",
            "2. Each side: 1 Commander + units to reach army size",
            "3. At least 3 different unit types required",
            "4. Shuffle Command Deck, deal 4 cards to each player",
        ]),
        ("TURN STRUCTURE", [
            "1. Start of Turn: Draw up to 2 cards (max hand: 4)",
            "2. Play Phase: Play 1 card (Regular, Persistent, or Formation)",
            "3. Command Phase: Resolve the card's effect",
            "4. End of Turn: Persistent effects continue until end of round",
        ]),
        ("CARD RESOLUTION", [
            "Select 2 cards from hand, reveal both simultaneously",
            "Resolve Top action of one card + Bottom action of the other",
            "Higher Initiative acts first within each phase",
            "Formation cards go to Formation zone, track activations",
            "Only 1 Formation card active at a time (new replaces old)",
            "Regular/Persistent cards go to Spent pile after resolution",
        ]),
        ("COMBAT", [
            "Range 1 = melee, Range 2+ = ranged",
            "Ranged attacks fire over allies and enemies",
            "Forests reduce ranged range by 1 per unavoidable crossing",
            "Shield tokens: absorb 1 damage each, removed at start of owner's next turn",
            "Screen = block Line-of-Sight for units behind",
            "Ambush = hidden until first attack (+2 damage, no counter)",
        ]),
        ("RECOVERY", [
            "Camp (full turn): Heal 1 HP to all units, Lose 1 Spent card, refill hand to 4",
            "Brainstorm (free action): No heal, 1 random Spent card is Lost, refill to 4",
        ]),
        ("UNIT STATS", [
            "Range | Attack | Health | Move | Notes",
            "------|--------|--------|------|------",
            "1     | 2      | 2      | 2    | Swordsman (standard melee)",
            "2     | 2      | 2      | 2    | Spearman (reach, anti-charge)",
            "1     | 1      | 3      | 1    | Shield Bearer (tank)",
            "2     | 1      | 1      | 3    | Scout (fast recon)",
            "3     | 1      | 2      | 3    | Slinger (long range)",
            "2     | 2      | 2      | 2    | Archer (standard ranged)",
            "1     | 3      | 4      | 1    | Giant (heavy, slow)",
            "1     | 2      | 1      | 2    | Commander",
        ]),
        ("VICTORY / DEFEAT", [
            "Victory: Eliminate all enemy commanders",
            "Defeat: Lose your commander",
            "If both commanders fall: survivor with more units wins",
            "Co-op: Don't lose either David or Jonathan",
        ]),
    ]

    page = None
    draw = None
    x = 0
    y = 0

    for si, (title, bullets) in enumerate(sections):
        if page is None:
            page = Image.new("RGB", (PAGE_W, PAGE_H), (250, 245, 230))
            draw = ImageDraw.Draw(page)
            x = int(MARGIN * scale)
            y = int(MARGIN * scale)

        hf = get_font(int(16 * scale), bold=True)
        bf = get_font(int(11 * scale))
        th = text_height(title, hf)

        if y + th > PAGE_H - int(MARGIN * scale) - int(80 * scale):
            yield page
            page = Image.new("RGB", (PAGE_W, PAGE_H), (250, 245, 230))
            draw = ImageDraw.Draw(page)
            x = int(MARGIN * scale)
            y = int(MARGIN * scale)

        if si == 0:
            bt = get_font(int(28 * scale), bold=True)
            draw_text_centered(draw, "THE EXILE KING - Rules Reference",
                               PAGE_W // 2, y, bt, fill=DARK_INK)
            y += int(40 * scale)

        draw_text_multiline_left(draw, title, x, y, hf, PAGE_W - x * 2, fill=RED)
        y += th + int(8 * scale)

        for b in bullets:
            draw_text_multiline_left(draw, b, x, y, bf, PAGE_W - x * 2 + int(10 * scale),
                                     fill=DARK_INK, line_spacing=1.4)
            lh = text_height("Ag", bf)
            lc = len(wrap_text(b, bf, PAGE_W - x * 2 + int(10 * scale)))
            y += int(lh * 1.4 * lc) + int(6 * scale)

        y += int(10 * scale)

    if page is not None:
        yield page


# ============================================================================
# Art Mapping
# ============================================================================

def normalize_card_name_to_prompt_key(name):
    if name in CARD_NAME_TO_PROMPT_KEY:
        return CARD_NAME_TO_PROMPT_KEY[name]
    n = name.lower()
    n = n.replace("'s", "").replace("'", "")
    n = n.replace(" ", "-").replace("-+", "-")
    n = re.sub(r"-+", "-", n).rstrip("-")
    return n


def smart_title(s):
    """Title case that handles apostrophes correctly (SHEPHERD'S -> Shepherd's, O'Brien -> O'Brien)."""
    words = s.split()
    result = []
    for word in words:
        if "'" in word:
            parts = word.split("'")
            capitalized = []
            for i, p in enumerate(parts):
                if i == 0:
                    capitalized.append(p.capitalize())
                else:
                    capitalized.append(p.capitalize() if len(p) > 1 else p.lower())
            result.append("'".join(capitalized))
        else:
            result.append(word.capitalize())
    return " ".join(result)


def map_cards_to_art(all_cards, inventory):
    for faction, card_order in COMMANDER_CARD_ORDER.items():
        pm = {"David's Company": "david", "Jonathan's Followers": "jonathan",
              "Achish's Host": "achish", "Lord of Ekron's Host": "philistine-lord"}
        prefix = pm.get(faction)
        if not prefix:
            continue
        for idx, cn in enumerate(card_order):
            for card in all_cards:
                if card.faction == faction and card.name == cn:
                    commander_art = inventory.get_commander_art(faction, idx)
                    pk = normalize_card_name_to_prompt_key(card.name)
                    ability_art = inventory.get_art(pk)
                    if commander_art:
                        card.top_art_path = commander_art
                    if ability_art:
                        card.bottom_art_path = ability_art
                    if not card.top_art_path and ability_art:
                        card.top_art_path = ability_art
                    if not card.bottom_art_path and ability_art:
                        card.bottom_art_path = ability_art

    for card in all_cards:
        if card.top_art_path and card.bottom_art_path:
            continue
        pk = normalize_card_name_to_prompt_key(card.name)
        art = inventory.get_art(pk)
        if art:
            if not card.top_art_path:
                card.top_art_path = art
            if not card.bottom_art_path:
                card.bottom_art_path = art


# ============================================================================
# Unit Collection
# ============================================================================

def collect_mvp_units():
    units = []
    for faction, name in COMMANDER_DISC_NAMES.items():
        units.append({"name": name, "faction": faction,
                       "stats": UNIT_STATS.get(name, (1, 2, 1, 2, 2))})

    common = {
        "David's Company": [("Swordsman", "Swordsman"), ("Spearman", "Spearman"),
                            ("Slinger", "Slinger"), ("Scout", "Scout"),
                            ("Shield Bearer", "Shield Bearer"), ("Archer", "Archer")],
        "Jonathan's Followers": [("Loyal Guard", "Loyal Guard"),
                                  ("Elite Archer", "Elite Archer"),
                                  ("Archer", "Archer"), ("Spearman", "Spearman"),
                                  ("Shield Bearer", "Shield Bearer")],
        "Achish's Host": [("Giant", "Giant"), ("Swordsman", "Swordsman"),
                          ("Spearman", "Spearman"), ("Archer", "Archer"),
                          ("Shield Bearer", "Shield Bearer")],
        "Lord of Ekron's Host": [("Chariot", "Chariot"), ("Slinger", "Slinger"),
                                  ("Swordsman", "Swordsman"), ("Spearman", "Spearman"),
                                  ("Shield Bearer", "Shield Bearer")],
    }

    for faction, ulist in common.items():
        for dn, sk in ulist:
            units.append({"name": dn, "faction": faction,
                          "stats": UNIT_STATS.get(sk, (1, 2, 1, 2, 2))})

    return units


# ============================================================================
# PDF Assembly
# ============================================================================

def build_pdf(all_cards, units, inventory, output_path, dpi=DPI_DEFAULT, scope="mvp"):
    pages = []

    cover = Image.new("RGB", (PAGE_W, PAGE_H), (245, 240, 225))
    d = ImageDraw.Draw(cover)
    tf = get_font(int(48 * (dpi / DPI_DEFAULT)), bold=True)
    sf = get_font(int(24 * (dpi / DPI_DEFAULT)))
    draw_text_centered(d, "THE EXILE KING", PAGE_W // 2, PAGE_H // 3, tf, fill=DARK_INK)
    draw_text_centered(d, "Printable Prototype", PAGE_W // 2,
                       PAGE_H // 3 + int(60 * dpi / DPI_DEFAULT), sf, fill=(80, 60, 40))
    pages.append(cover)

    for p in render_rules_reference(dpi):
        pages.append(p)

    fo = MVP_FACTIONS if scope == "mvp" else ALL_FACTIONS
    fc = {}
    for f in fo:
        fc[f] = []
    for card in all_cards:
        if card.faction in fc:
            fc[card.faction].append(card)

    for faction in fo:
        cards = fc.get(faction, [])
        if not cards:
            continue
        for i in range(0, len(cards), 9):
            batch = cards[i:i + 9]
            pages.append(render_card_sheet(batch, inventory, dpi))

    pages.append(render_disc_sheet(units, inventory, dpi))
    pages.append(render_hex_board(inventory, dpi))
    pages.append(render_token_sheet(inventory, dpi))
    pages.append(render_card_backs(inventory, dpi))

    op = str(output_path)
    if not op.lower().endswith(".pdf"):
        op += ".pdf"

    rgb_pages = []
    for p in pages:
        if p.mode != "RGB":
            rgb_pages.append(p.convert("RGB"))
        else:
            rgb_pages.append(p)
    rgb_pages[0].save(op, "PDF", save_all=True, append_images=rgb_pages[1:], quality=85)

    print("PDF saved to: " + op)
    print("Total pages: " + str(len(pages)))
    print("Cards: " + str(len(all_cards)))
    print("Unit discs: " + str(len(units)))


# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Build printable prototype PDF for The Exile King")
    parser.add_argument("--output", default=None)
    parser.add_argument("--art-dir", default=None)
    parser.add_argument("--queue", default=None)
    parser.add_argument("--review-report", default=None)
    parser.add_argument("--dpi", type=int, default=DPI_DEFAULT)
    parser.add_argument("--faction", default=None)
    parser.add_argument("--scope", default="mvp", choices=["mvp", "full"])
    parser.add_argument("--unreviewed-ok", action="store_true")
    parser.add_argument("--no-art", action="store_true")
    args = parser.parse_args()

    pr = os.path.dirname(os.path.abspath(__file__))
    local_art_dir = os.path.join(pr, "art", "prototype")
    jake_art_dir = os.path.join(
        r"D:\Jake\ComfyUI_windows_portable\ComfyUI\output\ComfyUI\annointed-exile",
        "prototype")
    art_dir = args.art_dir or (local_art_dir if os.path.exists(local_art_dir) else jake_art_dir)
    queue_path = args.queue or os.path.join(pr, "generation_queue.json")
    review_path = args.review_report or os.path.join(pr, "full_review.json")
    output_path = args.output or os.path.join(pr, "prototype", "printable_prototype.pdf")

    od = os.path.dirname(output_path)
    if od and not os.path.exists(od):
        os.makedirs(od)

    factions = None
    if args.faction:
        factions = [f.strip() for f in args.faction.split(",")]
    if args.scope == "mvp" and not factions:
        factions = MVP_FACTIONS
    elif args.scope == "full" and not factions:
        factions = ALL_FACTIONS

    inventory = ArtInventory(art_dir=art_dir, queue_path=queue_path,
                             review_path=review_path, no_art=args.no_art)

    if args.no_art:
        print("Running in --no-art mode (placeholders only)")
    else:
        ta = sum(len(v) for v in inventory.art_files.values())
        print("Art inventory: {} prompt_keys, {} files".format(len(inventory.art_files), ta))

    print("Parsing card .md files...")
    all_cards = parse_all_cards(pr, factions)
    print("Parsed " + str(len(all_cards)) + " cards")

    map_cards_to_art(all_cards, inventory)

    units = collect_mvp_units()

    print("Building PDF...")
    build_pdf(all_cards, units, inventory, output_path, dpi=args.dpi, scope=args.scope)
    print("Done!")


if __name__ == "__main__":
    main()

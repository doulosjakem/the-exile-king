import json
import os

QUEUE_PATH = r"D:\the-exile-king\generation_queue.json"
OUTPUT_BASE = r"D:\Jake\ComfyUI_windows_portable\ComfyUI\output\ComfyUI\annointed-exile"

queue = []

# ------------------ Unit Discs ------------------
unit_discs = [
    ("unit-disc-david", "david_commander", "prototype/unit-discs", "david"),
    ("unit-disc-jonathan", "jonathan_commander", "prototype/unit-discs", "jonathan"),
    ("unit-disc-achish", "achish_commander", "prototype/unit-discs", "achish"),
    ("unit-disc-philistine-lord", "philistine_lord_commander", "prototype/unit-discs", "philistine-lord"),
    ("unit-disc-swordsman-david", "swordsman_david", "prototype/unit-discs", "swordsman-david"),
    ("unit-disc-swordsman-jonathan", "swordsman_jonathan", "prototype/unit-discs", "swordsman-jonathan"),
    ("unit-disc-swordsman-achish", "swordsman_achish", "prototype/unit-discs", "swordsman-achish"),
    ("unit-disc-swordsman-ekron", "swordsman_ekron", "prototype/unit-discs", "swordsman-ekron"),
    ("unit-disc-spearman-david", "spearman_david", "prototype/unit-discs", "spearman-david"),
    ("unit-disc-spearman-jonathan", "spearman_jonathan", "prototype/unit-discs", "spearman-jonathan"),
    ("unit-disc-spearman-achish", "spearman_achish", "prototype/unit-discs", "spearman-achish"),
    ("unit-disc-spearman-ekron", "spearman_ekron", "prototype/unit-discs", "spearman-ekron"),
    ("unit-disc-slinger-david", "slinger_david", "prototype/unit-discs", "slinger-david"),
    ("unit-disc-slinger-ekron", "slinger_ekron", "prototype/unit-discs", "slinger-ekron"),
    ("unit-disc-scout-david", "scout_david", "prototype/unit-discs", "scout-david"),
    ("unit-disc-shield-bearer-david", "shield_bearer_david", "prototype/unit-discs", "shield-bearer-david"),
    ("unit-disc-shield-bearer-jonathan", "shield_bearer_jonathan", "prototype/unit-discs", "shield-bearer-jonathan"),
    ("unit-disc-shield-bearer-achish", "shield_bearer_achish", "prototype/unit-discs", "shield-bearer-achish"),
    ("unit-disc-shield-bearer-ekron", "shield_bearer_ekron", "prototype/unit-discs", "shield-bearer-ekron"),
    ("unit-disc-loyal-guard", "loyal_guard_jonathan", "prototype/unit-discs", "loyal-guard"),
    ("unit-disc-elite-archer", "elite_archer_jonathan", "prototype/unit-discs", "elite-archer"),
    ("unit-disc-archer-jonathan", "archer_jonathan", "prototype/unit-discs", "archer-jonathan"),
    ("unit-disc-archer-achish", "archer_achish", "prototype/unit-discs", "archer-achish"),
    ("unit-disc-giant", "giant_achish", "prototype/unit-discs", "giant"),
    ("unit-disc-chariot", "chariot_ekron", "prototype/unit-discs", "chariot"),
]

for uid, prompt_key, subfolder, prefix in unit_discs:
    queue.append({
        "id": uid,
        "prompt_key": prompt_key,
        "count": 3,
        "steps": 4,
        "cfg": 3,
        "width": 512,
        "height": 512,
        "output_subfolder": subfolder,
        "filename_prefix": prefix,
    })

# ------------------ Commander Cards ------------------
commanders = [
    ("david", 10),
    ("jonathan", 10),
    ("achish", 10),
    ("philistine-lord", 10),
]
for cmd, total in commanders:
    for i in range(1, total + 1):
        queue.append({
            "id": f"commander-card-{cmd}-{i:02d}",
            "prompt_key": f"card_front_{cmd.replace('-', '_')}",
            "count": 3,
            "steps": 4,
            "cfg": 3,
            "width": 512,
            "height": 768,
            "output_subfolder": f"prototype/commander-cards",
            "filename_prefix": f"{cmd}-{i:02d}",
        })

# ------------------ Unit Cards ------------------
unit_card_prompts = {
    # David/Shared
    "swordsmen-advance": ["swordsmen-advance", "swordsmen-formation"] * 3,
    "spearman-david": ["spear-wall", "spearman-formation", "spearman-screen"] * 2,
    "slinger-david": ["circle-and-strike", "stone-volley"] * 3,
    "scout-david": ["scout-recon", "scout-formation"] * 3,
    "shield-bearer-david": ["shield-wall", "phalanx-advance"] * 3,
    # Jonathan
    "loyal-guard-jonathan": ["guard-formation"] * 5,
    "elite-archer-jonathan": ["jonathans-mark", "perfect-shot"] * 3,
    "archer-jonathan": ["archer-volley", "archer-formation"] * 3,
    "spearman-jonathan": ["spear-wall", "spearman-formation", "spearman-screen"] * 2,
    "shield-bearer-jonathan": ["shield-wall", "phalanx-advance"] * 3,
    # Achish
    "giant-achish": ["giants-might", "unstoppable", "berserker-rage"] * 2,
    "swordsman-achish": ["swordsmen-advance", "swordsmen-formation"] * 3,
    "spearman-achish": ["spear-wall", "spearman-formation", "spearman-screen"] * 2,
    "archer-achish": ["ekron-archer-command", "ekron-archer-formation-1", "ekron-archer-formation-2"] * 2,
    "shield-bearer-achish": ["shield-wall", "phalanx-advance"] * 3,
    # Ekron
    "chariot-ekron": ["chariot-charge", "chariot-formation-1", "chariot-formation-2"] * 2,
    "slinger-ekron": ["circle-and-strike", "stone-volley"] * 3,
    "swordsman-ekron": ["swordsmen-advance", "swordsmen-formation"] * 3,
    "spearman-ekron": ["spear-wall", "spearman-formation", "spearman-screen"] * 2,
    "shield-bearer-ekron": ["shield-wall", "phalanx-advance"] * 3,
}

for prefix, prompts in unit_card_prompts.items():
    for i in range(1, 6):
        queue.append({
            "id": f"unit-card-{prefix}-{i:02d}",
            "prompt_key": prompts[i - 1],
            "count": 2,
            "steps": 4,
            "cfg": 3,
            "width": 512,
            "height": 768,
            "output_subfolder": "prototype/unit-cards",
            "filename_prefix": f"{prefix}-{i:02d}",
        })

# ------------------ Card Back ------------------
queue.append({
    "id": "card-back-01",
    "prompt_key": "card_back",
    "count": 3,
    "steps": 4,
    "cfg": 3,
    "width": 512,
    "height": 768,
    "output_subfolder": "prototype/card-backs",
    "filename_prefix": "card-back",
})

# ------------------ Hex Tiles ------------------
hex_types = ["grass", "rock", "sand"]
for htype in hex_types:
    for i in range(1, 11):
        queue.append({
            "id": f"hex-{htype}-{i:02d}",
            "prompt_key": f"hex_{htype}",
            "count": 1,
            "steps": 4,
            "cfg": 3,
            "width": 512,
            "height": 512,
            "output_subfolder": "prototype/hex-tiles",
            "filename_prefix": f"hex-{htype}-{i:02d}",
        })

# ------------------ Equipment ------------------
equipment = [
    "bronze-sword",
    "leather-shield",
    "spear",
    "sling",
    "bow",
    "sword-sheath",
    "quiver",
    "bronze-helm",
    "bronze-greaves",
    "leather-belt",
]
for eq in equipment:
    queue.append({
        "id": f"equipment-{eq}",
        "prompt_key": eq,
        "count": 1,
        "steps": 4,
        "cfg": 3,
        "width": 512,
        "height": 512,
        "output_subfolder": "prototype/equipment",
        "filename_prefix": eq,
    })

# ------------------ UI Elements ------------------
ui_elements = [
    "end-turn-button",
    "command-card-back",
    "card-frame-template",
    "hp-bar-bg",
    "hp-bar-fill",
    "reward-panel",
    "commander-aura-marker",
    "activation-token",
    "lost-pile-marker",
    "setup-sheet",
]
for ui in ui_elements:
    queue.append({
        "id": f"ui-{ui}",
        "prompt_key": ui,
        "count": 1,
        "steps": 4,
        "cfg": 3,
        "width": 512,
        "height": 512,
        "output_subfolder": "prototype/ui",
        "filename_prefix": ui,
    })

os.makedirs(os.path.dirname(QUEUE_PATH), exist_ok=True)
with open(QUEUE_PATH, "w", encoding="utf-8") as f:
    json.dump(queue, f, indent=2)

print(f"Wrote {len(queue)} items to {QUEUE_PATH}")
print(f"Total images: {sum(item.get('count', 1) for item in queue)}")

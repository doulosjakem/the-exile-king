with open(r'D:\the-exile-king\review_art_ollama.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Replace lookup_expected_prompt body (lines 514-547)
new_lookup_body = '''    if "prototype" in folder.split(os.sep):
        proto_key = _prototype_lookup(folder, stem)
        if proto_key and proto_key in EXPECTED_PROMPTS:
            return EXPECTED_PROMPTS[proto_key], proto_key

    parts = [p.lower() for p in re.split(r'[/\\\\]', folder)] + re.split(r'[\\s_-]', basename)
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
        best_key = _prototype_lookup(folder, stem)

    if not best_key:
        for alias, canonical in PROMPT_ALIASES.items():
            if alias in combined:
                best_key = canonical
                break

    if best_key:
        return EXPECTED_PROMPTS[best_key], best_key
    return None, None
'''

# Find the start and end of lookup_expected_prompt body
start_idx = None
end_idx = None
for i, line in enumerate(lines):
    if line.strip() == 'def lookup_expected_prompt(rel_path):':
        start_idx = i
    if start_idx is not None and line.strip() == 'return None, None' and i > start_idx + 5:
        end_idx = i
        break

if start_idx is None or end_idx is None:
    raise RuntimeError("Could not find lookup_expected_prompt boundaries")

final_lines = lines[:start_idx] + [new_lookup_body] + lines[end_idx + 1:]

# Now update KEY sets
new_char_keys = '''CHARACTER_KEYS = {
    "token_david", "token_swordsman", "token_spearman", "token_slinger",
    "token_archer", "token_scout", "token_chieftain_amalekite", "token_raider_amalekite",
    "token_refugee", "david", "swordsman", "spearman", "slinger", "archer",
    "scout", "raider", "chieftain", "refugee",
    "slinger_amalekite", "archer_amalekite", "scout_amalekite", "camel_rider_amalekite",
    "david_commander", "jonathan_commander", "achish_commander", "philistine_lord_commander",
    "shield_bearer_david", "shield_bearer_jonathan", "shield_bearer_achish", "shield_bearer_ekron",
    "giant_achish", "swordsman_jonathan", "swordsman_achish", "swordsman_ekron",
    "spearman_jonathan", "spearman_achish", "spearman_ekron", "slinger_ekron",
    "archer_jonathan", "archer_achish", "chariot_ekron", "loyal_guard_jonathan",
    "elite_archer_jonathan", "jonathan_commander",
}
'''
new_tile_keys = '''TILE_KEYS = {"hex_sand", "hex_rock", "hex_grass", "grass", "rock", "sand"}
'''
new_ui_keys = '''UI_KEYS = {"end-turn-button", "command-card-back", "card-frame-template", "hp_bar_bg", "hp_bar_fill", "reward_panel", "commander-aura-marker", "activation-token", "lost-pile-marker", "setup-sheet"}
'''
new_equip_keys = '''EQUIPMENT_KEYS = {"bronze-sword", "leather-shield", "spear", "sling", "bow", "camel", "sword-sheath", "quiver", "bronze-helm", "bronze-greaves", "leather-belt"}
'''
new_card_keys = '''CARD_KEYS = {"swordsmen-advance", "archer-volley", "spear-wall", "slinger-skirmish", "scout-recon", "refugee-aid", "davids-leadership", "march", "engage",
              "swordsmen-formation", "spearman-formation", "spearman-screen", "circle-and-strike", "stone-volley",
              "archer-formation", "scout-formation", "guard-formation", "jonathans-mark", "perfect-shot",
              "giants-might", "unstoppable", "berserker-rage", "ekron-archer-command", "ekron-archer-formation-1",
              "ekron-archer-formation-2", "chariot-charge", "chariot-formation-1", "chariot-formation-2",
              "shield-wall", "phalanx-advance", "card_back"}
'''

for i, line in enumerate(final_lines):
    if line.strip() == 'CHARACTER_KEYS = {':
        final_lines[i] = new_char_keys
    elif line.strip() == 'TILE_KEYS = {"hex_sand", "hex_rock", "hex_grass", "grass", "rock", "sand"}':
        final_lines[i] = new_tile_keys
    elif line.strip() == 'UI_KEYS = {"end-turn-button", "command-card-back", "card-frame-template", "hp_bar_bg", "hp_bar_fill", "reward_panel"}':
        final_lines[i] = new_ui_keys
    elif line.strip() == 'EQUIPMENT_KEYS = {"bronze-sword", "leather-shield", "spear", "sling", "bow", "camel"}':
        final_lines[i] = new_equip_keys
    elif line.strip() == 'CARD_KEYS = {"swordsmen-advance", "archer-volley", "spear-wall", "slinger-skirmish", "scout-recon", "refugee-aid", "davids-leadership", "march", "engage"}':
        final_lines[i] = new_card_keys

with open(r'D:\the-exile-king\review_art_ollama.py', 'w', encoding='utf-8') as f:
    f.writelines(final_lines)

print('Fixed lookup_expected_prompt and KEY sets')

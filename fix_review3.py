with open(r'D:\the-exile-king\review_art_ollama.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find line 697 (PROMPT_ALIASES closing) and insert new dict + function after it
insert_idx = None
for i, line in enumerate(lines):
    if line.strip() == '}':
        # Check if next few lines are the lookup_expected_prompt definition
        if i + 5 < len(lines) and 'def lookup_expected_prompt' in lines[i + 2]:
            insert_idx = i + 1
            break

if insert_idx is None:
    raise RuntimeError("Could not find insertion point for prototype lookup")

new_code = '''


PROTOTYPE_STEM_ALIASES = {
    "david": "david_commander",
    "jonathan": "jonathan_commander",
    "achish": "achish_commander",
    "philistine-lord": "philistine_lord_commander",
    "giant": "giant_achish",
    "chariot": "chariot_ekron",
    "scout-david": "scout_david",
    "elite-archer": "elite_archer_jonathan",
    "loyal-guard": "loyal_guard_jonathan",
}


def _prototype_lookup(folder, stem):
    parts = [p.lower() for p in re.split(r'[/\\]', folder)]
    subfolder = parts[-1] if parts else folder

    clean = re.sub(r'[-_]\d+', '', stem)
    clean = clean.rstrip('_-')

    if subfolder == "card-backs":
        if "card_back" in EXPECTED_PROMPTS:
            return "card_back"

    elif subfolder == "commander-cards":
        commander = clean.split("-")[0]
        return f"card_front_{commander}"

    elif subfolder == "unit-cards":
        m = re.match(r'^(.+?)(?:-\d+)+$', clean)
        if m:
            return m.group(1)
        return clean

    elif subfolder == "hex-tiles":
        m = re.match(r'^hex-(.+?)(?:-\d+)+$', clean)
        if m:
            return f"hex_{m.group(1)}"
        return clean.replace("-", "_")

    elif subfolder in ("equipment", "ui"):
        return clean

    elif subfolder == "unit-discs":
        if clean in PROTOTYPE_STEM_ALIASES:
            return PROTOTYPE_STEM_ALIASES[clean]
        if "-" in clean:
            return clean.replace("-", "_")
        return clean

    elif subfolder == "prototype":
        return clean

    return None


def lookup_expected_prompt(rel_path):
'''

final_lines = lines[:insert_idx] + [new_code] + lines[insert_idx:]

with open(r'D:\the-exile-king\review_art_ollama.py', 'w', encoding='utf-8') as f:
    f.writelines(final_lines)

print('Inserted prototype lookup logic')

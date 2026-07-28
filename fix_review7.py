with open(r'D:\the-exile-king\review_art_ollama.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_func = '''
def lookup_expected_prompt(rel_path):
    folder = os.path.dirname(rel_path).lower()
    if not folder:
        folder = "."
    basename = os.path.basename(rel_path).lower()
    stem = os.path.splitext(basename)[0]
    path_no_numbers = re.sub(r'[\\d_]+', '', stem)
    path_dashed = path_no_numbers.replace("_", " ").replace("-", " ")

    prompt_check = False
    for allowed in PROMPT_CHECK_FOLDERS:
        if allowed in folder.split(os.sep):
            prompt_check = True
            break

    if not prompt_check:
        return None, None

    if "prototype" in folder.split(os.sep):
        proto_key = _prototype_lookup(folder, stem)
        if proto_key and proto_key in EXPECTED_PROMPTS:
            return EXPECTED_PROMPTS[proto_key], proto_key

    parts = [p.lower() for p in folder.replace('\\\\\\\\', '/').split('/')] + re.split(r'[\\s_-]', basename)
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

# Find line 495: return None (end of _prototype_lookup)
insert_idx = None
for i, line in enumerate(lines):
    if line.strip() == 'return None' and i > 450 and i < 500:
        insert_idx = i + 1
        break

if insert_idx is None:
    raise RuntimeError("Could not find insertion point")

final_lines = lines[:insert_idx] + [new_func] + lines[insert_idx:]

with open(r'D:\the-exile-king\review_art_ollama.py', 'w', encoding='utf-8') as f:
    f.writelines(final_lines)

print('Inserted lookup_expected_prompt')

with open(r'D:\the-exile-king\review_art_ollama.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Replace corrupted lookup_expected_prompt (lines 498-562, 0-indexed: 497-561)
new_func = '''def lookup_expected_prompt(rel_path):
    folder = os.path.dirname(rel_path).lower()
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

final_lines = lines[:497] + [new_func] + lines[562:]

with open(r'D:\the-exile-king\review_art_ollama.py', 'w', encoding='utf-8') as f:
    f.writelines(final_lines)

print('Fixed lookup_expected_prompt')

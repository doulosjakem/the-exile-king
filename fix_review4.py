with open(r'D:\the-exile-king\review_art_ollama.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1. Add prototype fallback call before 'return None, None' in lookup_expected_prompt
for i, line in enumerate(lines):
    if line.strip() == 'return None, None' and i > 0:
        # Check this is inside lookup_expected_prompt
        context = ''.join(lines[max(0, i-20):i])
        if 'def lookup_expected_prompt' in context:
            indent = '    '
            lines[i] = indent + 'if not best_key:\n' + indent + '    best_key = _prototype_lookup(folder, stem)\n\n' + indent + 'if not best_key:\n' + indent + '    for alias, canonical in PROMPT_ALIASES.items():\n' + indent + '        if alias in combined:\n' + indent + '            best_key = canonical\n' + indent + '            break\n\n' + indent + 'if not best_key:\n' + indent + '    for alias, canonical in _PROTOTYPE_STEM_ALIASES.items():\n' + indent + '        if alias in combined:\n' + indent + '            best_key = canonical\n' + indent + '            break\n\n'
            break

with open(r'D:\the-exile-king\review_art_ollama.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('Added prototype fallback call')

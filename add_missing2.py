with open(r'D:\the-exile-king\review_art_ollama.py', 'r', encoding='utf-8') as f:
    content = f.read()

missing = '''    "swordsman_david": "ONE PERSON ONLY, solo portrait, waist-up, David's swordsman, bronze age Levantine Israelite warrior, dark hair and short beard, simple linen tunic with layered leather vest, worn brown wool cloak pinned at shoulder, bronze short sword with leaf-shaped blade in hand, small round hide-covered shield on arm, leather wrapped grip, sandals, alert expression, standing on rocky Judean ground, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European",
    "spearman_david": "ONE PERSON ONLY, solo portrait, waist-up, David's spearman, bronze age Levantine Israelite warrior, dark hair, linen tunic with leather shoulder piece, brown cloak tied at neck, long wooden spear with bronze tip held in both hands, small hide shield slung across back, knife at waist, sandals, focused expression, standing on hillside overlooking wilderness valleys, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European",
    "slinger_david": "ONE PERSON ONLY, solo portrait, waist-up, David's slinger, bronze age Levantine Israelite skirmisher, dark hair, simple linen tunic with leather vest, worn brown cloak, leather sling in hand with pouch at belt, pouch of smooth stones at hip, small knife, crouched lightly ready to pivot and throw, alert watchful expression, standing on rocky slope, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European",
'''

# Find the last entry in EXPECTED_PROMPTS before the closing brace
# We'll insert before the final }
last_entry_marker = '    "setup-sheet"'
insert_pos = content.rfind(last_entry_marker)
if insert_pos == -1:
    raise RuntimeError("Could not find setup-sheet entry")

# Find the end of that line
line_end = content.find('\n', insert_pos)
insert_pos = line_end + 1

new_content = content[:insert_pos] + missing + content[insert_pos:]

with open(r'D:\the-exile-king\review_art_ollama.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Added 3 missing faction variant prompts')

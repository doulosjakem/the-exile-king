with open(r'D:\the-exile-king\review_art_ollama.py', 'r', encoding='utf-8') as f:
    content = f.read()

missing_entries = '''
    "david_commander": "ONE PERSON ONLY, solo portrait, waist-up, young bronze age Israelite commander, bronze age Levantine man, dark curly hair and trimmed beard, simple linen tunic with leather chest piece, brown wool cloak pinned at shoulder with bronze brooch, bronze short sword at hip, leather sling tucked in belt, shepherd's staff in hand, determined watchful expression, standing on rocky Judean hillside under overcast sky, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine",
    "achish_commander": "ONE PERSON ONLY, solo portrait, waist-up, Philistine lord of Gath, bronze age Levantine Philistine ruler, dark hair, rich purple cloak over linen tunic, bronze chest plate, bronze sword at hip, stern unreadable expression, seated authority on folding stool, flanked by spearmen, warm lamplight, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European",
    "scout_david": "ONE PERSON ONLY, solo portrait, waist-up, David's scout, bronze age Levantine tracker and skirmisher, lean shepherd-skirmisher, dark hair, simple linen tunic with leather vest, worn brown cloak, sandals, sling at belt, short spear, small hide shield on back, knife at waist, alert watchful expression, standing lightly on rocky Judean hillside, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European",
    "elite_archer_jonathan": "ONE PERSON ONLY, solo portrait, waist-up, Jonathan's elite archer, bronze age Levantine archer, dark hair, white linen tunic with dark border, leather vest, brown cloak, composite bow drawn with arrow nocked, quiver on back, bronze short sword at hip, noble precise expression, standing with disciplined poise, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European",
    "loyal_guard_jonathan": "ONE PERSON ONLY, solo portrait, waist-up, Jonathan's loyal guard, bronze age Levantine elite infantryman, dark hair, white linen tunic with leather vest, brown cloak, bronze short sword raised, small hide shield, disciplined attack stance, loyal protective expression, standing ready, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European",
'''

# Find the closing brace of EXPECTED_PROMPTS
# Look for the first occurrence of "\n}\n\n" after EXPECTED_PROMPTS = {
marker = content.find('EXPECTED_PROMPTS = {')
if marker == -1:
    raise RuntimeError("Could not find EXPECTED_PROMPTS")

# Find the matching closing brace
brace_count = 0
start = marker + len('EXPECTED_PROMPTS = ')
end = start
while end < len(content):
    if content[end] == '{':
        brace_count += 1
    elif content[end] == '}':
        brace_count -= 1
        if brace_count == 0:
            break
    end += 1

if brace_count != 0:
    raise RuntimeError("Could not find matching } for EXPECTED_PROMPTS")

insert_pos = end + 1  # after the closing }
new_content = content[:insert_pos] + missing_entries + content[insert_pos:]

with open(r'D:\the-exile-king\review_art_ollama.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Added 5 missing expected prompts')

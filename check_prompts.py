with open(r'D:\the-exile-king\review_art_ollama.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract EXPECTED_PROMPTS dict using a simple parser
start = content.find('EXPECTED_PROMPTS = {')
end = content.find('\n\n\ndef gather_images(base):')
dict_text = content[start + len('EXPECTED_PROMPTS = {'):end]

# Find all keys
import re
keys = re.findall(r'^\s+"([^"]+)":', dict_text, re.MULTILINE)
print(f'Total keys: {len(keys)}')

# Check for missing prototype keys
needed = [
    'david_commander', 'achish_commander',
    'card_front_david', 'card_front_jonathan', 'card_front_achish', 'card_front_philistine_lord',
    'shield_bearer_david', 'shield_bearer_jonathan', 'shield_bearer_achish', 'shield_bearer_ekron',
    'giant_achish', 'chariot_ekron', 'scout_david', 'elite_archer_jonathan', 'loyal_guard_jonathan',
    'swordsman_jonathan', 'swordsman_achish', 'swordsman_ekron',
    'spearman_jonathan', 'spearman_achish', 'spearman_ekron',
    'slinger_ekron', 'archer_jonathan', 'archer_achish',
    'swordsmen-advance', 'swordsmen-formation',
    'spear-wall', 'spearman-formation', 'spearman-screen',
    'circle-and-strike', 'stone-volley',
    'archer-volley', 'archer-formation',
    'scout-recon', 'scout-formation',
    'guard-formation', 'jonathans-mark', 'perfect-shot',
    'giants-might', 'unstoppable', 'berserker-rage',
    'ekron-archer-command', 'ekron-archer-formation-1', 'ekron-archer-formation-2',
    'chariot-charge', 'chariot-formation-1', 'chariot-formation-2',
    'shield-wall', 'phalanx-advance', 'card_back',
    'sword-sheath', 'quiver', 'bronze-helm', 'bronze-greaves', 'leather-belt',
    'commander-aura-marker', 'activation-token', 'lost-pile-marker', 'setup-sheet',
    'hex_grass', 'hex_rock', 'hex_sand',
]

missing = [k for k in needed if k not in keys]
print(f'Missing {len(missing)} keys:')
for k in missing:
    print(f'  {k}')

# Check duplicates
from collections import Counter
counts = Counter(keys)
dups = {k: c for k, c in counts.items() if c > 1}
print(f'Duplicate keys: {len(dups)}')
for k, c in dups.items():
    print(f'  {k}: {c}')

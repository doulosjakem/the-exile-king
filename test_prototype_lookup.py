import sys
sys.path.insert(0, r'D:\the-exile-king')
from review_art_ollama import lookup_expected_prompt, classify_asset, _prototype_lookup

# Test _prototype_lookup directly
proto_tests = [
    ('prototype\\unit-discs', 'achish_00001_', 'achish_commander'),
    ('prototype\\unit-discs', 'swordsman-david_00001_', 'swordsman_david'),
    ('prototype\\unit-discs', 'giant_00001_', 'giant_achish'),
    ('prototype\\commander-cards', 'achish-01_00001_', 'card_front_achish'),
    ('prototype\\unit-cards', 'swordsmen-advance-01_00001_', 'swordsmen-advance'),
    ('prototype\\hex-tiles', 'hex-grass-01_00001_', 'hex_grass'),
    ('prototype\\equipment', 'bronze-sword_00001_', 'bronze-sword'),
    ('prototype\\ui', 'activation-token_00001_', 'activation-token'),
    ('prototype\\card-backs', 'card-back_00001_', 'card_back'),
]

print('=== _prototype_lookup tests ===')
for folder, stem, expected in proto_tests:
    result = _prototype_lookup(folder, stem)
    status = 'OK' if result == expected else 'FAIL'
    print(f'{status} {folder}/{stem} -> {result} (expected {expected})')

# Test full lookup_expected_prompt
print('\n=== lookup_expected_prompt tests ===')
full_tests = [
    ('prototype\\unit-discs\\achish_00001_.png', 'achish_commander', 'character'),
    ('prototype\\commander-cards\\david-01_00001_.png', 'card_front_david', 'card'),
]
for rel, expected_key, expected_type in full_tests:
    prompt, key = lookup_expected_prompt(rel)
    asset_type = classify_asset(key)
    status = 'OK' if key == expected_key and asset_type == expected_type else 'FAIL'
    print(f'{status} {rel} -> key={key}, type={asset_type}')

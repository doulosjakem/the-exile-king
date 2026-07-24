import re

with open("review_art_ollama.py", "r", encoding="utf-8") as f:
    content = f.read()

start = content.find("EXPECTED_PROMPTS = {")
end = content.find("def gather_images")
block = content[start:end]

# Find all entries
pattern = re.compile(r'"([^"]+)":\s*"([^"]*)"')
matches = list(pattern.finditer(block))

# Check for internal quotes
issues = []
for m in matches:
    key = m.group(1)
    val = m.group(2)
    if '"' in val:
        issues.append((key, val))

print(f"Total key-value pairs: {len(matches)}")
print(f"Entries with internal double quotes: {len(issues)}")
for key, val in issues:
    print(f"  KEY: {key}")
    print(f"  VAL: {val[:200]}")
    print()

import re

with open("review_art_ollama.py", "r", encoding="utf-8") as f:
    content = f.read()

start = content.find("EXPECTED_PROMPTS = {")
end = content.find("def gather_images")
block = content[start:end]

existing = {}
pattern = re.compile(r'"([^"]+)":\s*"([^"]*)"')
for m in pattern.finditer(block):
    existing[m.group(1)] = m.group(2)

print("refugee in existing:", "refugee" in existing)
print("total existing:", len(existing))

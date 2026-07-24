with open("review_art_ollama.py", "r", encoding="utf-8") as f:
    content = f.read()

start = content.find("EXPECTED_PROMPTS = {")
end = content.find("def gather_images")
block = content[start:end]

print("refugee in block:", "refugee" in block)
for m in __import__("re").finditer(r'"refugee":\s*"([^"]*)"', block):
    print("Match:", m.group(0)[:80])

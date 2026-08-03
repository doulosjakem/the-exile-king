"""Manually review the commander-aura-marker image."""
import base64, json, urllib.request

OLLAMA_URL = "http://localhost:11434/api/generate"

def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

img_path = r"D:\Jake\ComfyUI_windows_portable\ComfyUI\output\ComfyUI\annointed-exile\prototype\ui\commander-aura-marker_00001_.png"
expected = "soft glowing circle on ground, commander presence area, warm golden light, board game UI element, transparent background, hand-painted illustration, NOT medieval, NOT fantasy, NOT European"

prompt = f'''You are a strict image quality reviewer. Analyze this image and answer exactly 4 questions with YES/NO:

1. Is the image hand-painted or digital painting style (no screenshots, photos, or vector graphics)?
2. Does the image contain any modern objects, text, logos, or European medieval/fantasy elements?
3. Is the image blurry, corrupted, or anatomically broken?
4. Does the image match the expected prompt: "{expected}"?

Answer format: YES,NO,NO,YES'''

payload = {
    "model": "llava-phi3:3.8b",
    "prompt": prompt,
    "images": [encode_image(img_path)],
    "stream": False,
    "options": {"temperature": 0.0, "num_ctx": 4096, "num_gpu": 1}
}

req = urllib.request.Request(OLLAMA_URL, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"}, method="POST")
result = json.loads(urllib.request.urlopen(req, timeout=120).read().decode("utf-8"))
print("Response:", result.get("response", "").strip())

# Parse and decide
response = result.get("response", "").strip()
import re
matches = re.findall(r'\b(YES|NO)\b', response.upper())
if len(matches) >= 4:
    painted, modern, blurry, prompt_match = matches[:4]
    print(f"Parsed: painted={painted}, modern={modern}, blurry={blurry}, prompt_match={prompt_match}")
    score = 5
    if painted == "NO": score -= 1
    if modern == "YES": score -= 3
    if blurry == "YES": score -= 2
    if prompt_match == "NO": score -= 2
    score = max(1, score)
    if modern == "YES" or blurry == "YES" or score <= 2:
        decision = "TRASH"
    else:
        decision = "KEEP"
    print(f"Decision: {decision}, Score: {score}")

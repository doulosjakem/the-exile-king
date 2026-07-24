with open("review_art_ollama.py", "r", encoding="utf-8") as f:
    content = f.read()

for k in ["chieftain_amalekite", "raider_amalekite", "camel_rider_amalekite",
          "camel-rider_amalekite", "reward-panel", "reward_panel", "refugee"]:
    pat = '"' + k + '"'
    print(f"{k}: {pat in content}")

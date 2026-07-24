import subprocess, re

result = subprocess.run(["git", "show", "HEAD:review_art_ollama.py"], capture_output=True, text=True, cwd="D:\\the-exile-king")
content = result.stdout

for m in re.finditer(r'"refugee"', content):
    print("Found at pos", m.start())
    print(content[max(0,m.start()-100):m.start()+200])
    print("---")

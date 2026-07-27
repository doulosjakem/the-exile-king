import urllib.request, json

r = urllib.request.urlopen('http://localhost:11434/api/tags', timeout=5)
tags = json.loads(r.read().decode())
print('Available models:')
for m in tags.get('models', []):
    print(f"  {m['name']}")

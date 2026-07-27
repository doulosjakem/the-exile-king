import urllib.request, json, base64, time

# Test Ollama with a small image
OLLAMA_URL = "http://localhost:11434/api/generate"

# Create a tiny 1x1 transparent PNG
png_data = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==")

payload = {
    "model": "minicpm-v:8b",
    "prompt": "Describe this image briefly.",
    "images": [png_data.decode("latin-1")],
    "stream": False,
    "options": {"temperature": 0.1, "num_ctx": 4096, "num_gpu": 0}
}

data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(
    OLLAMA_URL,
    data=data,
    headers={"Content-Type": "application/json"},
    method="POST"
)

start = time.time()
try:
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        print(f"Success in {time.time()-start:.1f}s")
        print(f"Response: {result.get('response', '')[:200]}")
except Exception as e:
    print(f"Error after {time.time()-start:.1f}s: {e}")

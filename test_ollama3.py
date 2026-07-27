import urllib.request, json, base64, time

OLLAMA_URL = "http://localhost:11434/api/generate"
img_path = r"D:\Jake\ComfyUI_windows_portable\ComfyUI\output\ComfyUI\annointed-exile\assets\tiles\grass_00001_.png"

with open(img_path, "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode("latin-1")

payload = {
    "model": "minicpm-v:8b",
    "prompt": "Is this a hand-painted illustration? Answer YES or NO.",
    "images": [img_b64],
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
    with urllib.request.urlopen(req, timeout=180) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        print(f"Success in {time.time()-start:.1f}s")
        print(f"Response: {result.get('response', '')[:200]}")
except Exception as e:
    print(f"Error after {time.time()-start:.1f}s: {e}")

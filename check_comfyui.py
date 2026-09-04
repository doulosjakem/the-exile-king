import urllib.request, json

try:
    req = urllib.request.Request("http://127.0.0.1:8188/system_stats", method="GET")
    with urllib.request.urlopen(req, timeout=5) as resp:
        data = json.loads(resp.read().decode())
        vram = data.get("system", {}).get("vram", {})
        vram_total = vram.get("total", "unknown")
        print(f"ComfyUI is RUNNING")
        print(f"VRAM total: {vram_total} MB")
        print(f"GPU: {data.get('system', {}).get('gpus', 'unknown')}")
except Exception as e:
    print(f"ComfyUI not ready: {e}")

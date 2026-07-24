import json, os, sys, time, subprocess, shutil, urllib.request

COMFYUI_DIR = r"D:\Jake\ComfyUI_windows_portable\ComfyUI"
COMFYUI_ROOT = r"D:\Jake\ComfyUI_windows_portable"
OUTPUT_BASE = os.path.join(COMFYUI_DIR, r"output\ComfyUI\annointed-exile")
BASE_URL = "http://127.0.0.1:8188"

item = {
    "id": "tiles-grass",
    "prompt_key": "hex_grass",
    "count": 1,
    "steps": 4,
    "cfg": 3,
    "width": 512,
    "height": 512,
    "output_subfolder": "assets/tiles",
    "filename_prefix": "hex_grass"
}

UNIVERSAL_NEGATIVE = "photorealistic, hyperrealistic, realistic skin texture, photograph, 3d render, modern clothing, plate armor, steel armor, chainmail, fantasy armor, longbow, long sword, greatsword, crossguard, medieval helmet, horned helmet, knight, crusader, anime, manga, cartoon, text, logo, ugly, deformed, blurry, low quality, person, people, human, hands, fingers, body, figure, face, background, scenery, aged parchment, board game card art"
POSITIVE_SUFFIX = ", top-down flat seamless hex tile texture, parchment texture overlay, watercolor ink wash style, muted earth tones, no grid lines, no borders, no text, board game style, hand-painted texture, family friendly, NOT medieval, NOT fantasy, NOT European"

positive = "top-down view of a flat hexagonal tile, dry savanna grass on hard earth, warm green-brown and ochre tones, dry grass textures, watercolor wash, tileable seamless pattern, board game style, hand-painted texture, no grid lines" + POSITIVE_SUFFIX

workflow = {
    "3": {"class_type": "KSampler", "inputs": {"seed": 1000, "steps": 4, "cfg": 3, "sampler_name": "dpmpp_sde", "scheduler": "karras", "model": ["4", 0], "positive": ["6", 0], "negative": ["7", 0], "latent_image": ["5", 0], "denoise": 1}},
    "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "dreamshaperXL_sfwLightningDPMSDE.safetensors"}},
    "5": {"class_type": "EmptyLatentImage", "inputs": {"width": 512, "height": 512, "batch_size": 1}},
    "6": {"class_type": "CLIPTextEncode", "inputs": {"text": positive, "clip": ["4", 1]}},
    "7": {"class_type": "CLIPTextEncode", "inputs": {"text": UNIVERSAL_NEGATIVE, "clip": ["4", 1]}},
    "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["4", 2]}},
    "9": {"class_type": "SaveImage", "inputs": {"filename_prefix": "hex_grass", "images": ["8", 0]}}
}

print("Submitting workflow...")
payload = {"prompt": workflow}
data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(f"{BASE_URL}/prompt", data=data, headers={"Content-Type": "application/json"}, method="POST")
with urllib.request.urlopen(req, timeout=30) as resp:
    result = json.loads(resp.read().decode("utf-8"))
    prompt_id = result.get("prompt_id")
    print(f"Submitted: {prompt_id}")

print("Waiting for completion...")
for i in range(60):
    time.sleep(5)
    try:
        q = urllib.request.urlopen(f"{BASE_URL}/queue", timeout=5).json()
        running = len(q.get("queue_running", []))
        pending = len(q.get("queue_pending", []))
        print(f"[{i*5}s] running={running} pending={pending}")
        if running == 0 and pending == 0:
            break
    except Exception as e:
        print(f"[{i*5}s] error: {e}")

# Move output
prefix = "hex_grass"
subfolder = "assets/tiles"
dest_dir = os.path.join(OUTPUT_BASE, subfolder)
os.makedirs(dest_dir, exist_ok=True)
comfy_output = os.path.join(COMFYUI_DIR, "output")
files = sorted([f for f in os.listdir(comfy_output) if f.startswith(prefix)])
print(f"Files to move: {files}")
for f in files:
    src = os.path.join(comfy_output, f)
    dest = os.path.join(dest_dir, f)
    if not os.path.exists(dest):
        shutil.move(src, dest)
        print(f"Moved: {f}")

print("Done")

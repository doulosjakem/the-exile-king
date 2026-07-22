"""
ComfyUI automated generation runner.
Reads generation_queue.json, builds workflow JSON, submits to ComfyUI API,
and saves outputs to the target folders.
"""
import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error
import subprocess
import shutil

COMFYUI_DIR = r"D:\Jake\ComfyUI_windows_portable\ComfyUI"
OUTPUT_BASE = os.path.join(COMFYUI_DIR, r"output\ComfyUI\annointed-exile")
CHECKPOINT = "dreamshaperXL_sfwLightningDPMSDE.safetensors"

UNIVERSAL_NEGATIVE = "photorealistic, hyperrealistic, realistic skin texture, photograph, cinematic lighting, ray tracing, 3d render, octane render, unity engine, video game screenshot, modern clothing, plate armor, steel armor, chainmail, scale armor, fantasy armor, elaborate armor, longbow, long sword, greatsword, crossguard, medieval helmet, horned helmet, winged helmet, knight, crusader, viking, samurai, European castle, stone castle, heraldry, coat of arms, shield with cross, shield with lion, glowing, neon, bright colors, anime, manga, cartoon, digital art, illustration, signature, watermark, text, logo, ugly, deformed, blurry, low quality, worst quality, bad anatomy, extra limbs, merged body, duplicate, clone, two people, three people, group, crowd, nsfw, gore, blood"

POSITIVE_SUFFIX = ", hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European"

EXPECTED_PROMPTS = {}

def load_prompts():
    global EXPECTED_PROMPTS
    sys.path.insert(0, r"D:\the-exile-king")
    try:
        from review_art_ollama import EXPECTED_PROMPTS as EP
        EXPECTED_PROMPTS = EP
    except Exception as e:
        print(f"Warning: could not load prompts from review_art_ollama.py: {e}")
        EXPECTED_PROMPTS = {}

def resolve_prompt(prompt_key):
    if prompt_key in EXPECTED_PROMPTS:
        return EXPECTED_PROMPTS[prompt_key]
    return prompt_key.replace("-", " ")

def build_workflow(item, seed):
    prompt_key = item["prompt_key"]
    positive = resolve_prompt(prompt_key) + POSITIVE_SUFFIX
    negative = UNIVERSAL_NEGATIVE
    width = item.get("width", 512)
    height = item.get("height", 512)
    count = item.get("count", 1)
    steps = item.get("steps", 4)
    cfg = item.get("cfg", 3)
    prefix = item.get("filename_prefix", "ComfyUI")

    workflow = {
        "3": {
            "class_type": "KSampler",
            "inputs": {
                "seed": seed,
                "steps": steps,
                "cfg": cfg,
                "sampler_name": "dpmpp_sde",
                "scheduler": "karras",
                "model": ["4", 0],
                "positive": ["6", 0],
                "negative": ["7", 0],
                "latent_image": ["5", 0],
                "denoise": 1
            }
        },
        "4": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {
                "ckpt_name": CHECKPOINT
            }
        },
        "5": {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "width": width,
                "height": height,
                "batch_size": count
            }
        },
        "6": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": positive,
                "clip": ["4", 1]
            }
        },
        "7": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": negative,
                "clip": ["4", 1]
            }
        },
        "8": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": ["3", 0],
                "vae": ["4", 2]
            }
        },
        "9": {
            "class_type": "SaveImage",
            "inputs": {
                "filename_prefix": prefix,
                "images": ["8", 0]
            }
        }
    }
    return workflow


def submit_workflow(workflow):
    payload = {"prompt": workflow}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "http://127.0.0.1:8188/prompt",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        return result.get("prompt_id")


def wait_for_prompt(prompt_id, timeout=600):
    start = time.time()
    while time.time() - start < timeout:
        try:
            req = urllib.request.Request(f"http://127.0.0.1:8188/history/{prompt_id}", method="GET")
            with urllib.request.urlopen(req, timeout=10) as resp:
                history = json.loads(resp.read().decode("utf-8"))
                if prompt_id in history:
                    entry = history[prompt_id]
                    status = entry.get("status", {})
                    if status.get("completed", False):
                        return entry
                    if status.get("interrupted", False):
                        raise RuntimeError("Generation interrupted")
        except Exception:
            pass
        time.sleep(2)
    raise RuntimeError(f"Prompt {prompt_id} timed out after {timeout}s")


def move_outputs(item, manifest_entry):
    prefix = item.get("filename_prefix", "ComfyUI")
    subfolder = item.get("output_subfolder", "")
    dest_dir = os.path.join(OUTPUT_BASE, subfolder)
    os.makedirs(dest_dir, exist_ok=True)

    comfy_output = os.path.join(COMFYUI_DIR, "output")
    files = sorted([f for f in os.listdir(comfy_output) if f.startswith(prefix)])
    moved = []
    for f in files:
        src = os.path.join(comfy_output, f)
        dest = os.path.join(dest_dir, f)
        if not os.path.exists(dest):
            shutil.move(src, dest)
            moved.append(os.path.relpath(dest, OUTPUT_BASE))
    return moved


def start_comfyui():
    python = sys.executable
    cmd = [python, "main.py", "--auto-launch"]
    proc = subprocess.Popen(cmd, cwd=COMFYUI_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc


def wait_for_comfyui(timeout=120):
    start = time.time()
    while time.time() - start < timeout:
        try:
            req = urllib.request.Request("http://127.0.0.1:8188/system_stats", method="GET")
            with urllib.request.urlopen(req, timeout=5) as resp:
                return True
        except Exception:
            pass
        time.sleep(2)
    return False


def stop_comfyui():
    try:
        req = urllib.request.Request("http://127.0.0.1:8188/stop", method="POST")
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", default=r"D:\the-exile-king\generation_queue.json")
    parser.add_argument("--manifest", default=r"D:\the-exile-king\generation_manifest.json")
    parser.add_argument("--no-launch", action="store_true", help="assume ComfyUI already running")
    parser.add_argument("--no-shutdown", action="store_true", help="leave ComfyUI running after queue")
    args = parser.parse_args()

    load_prompts()

    with open(args.queue, "r", encoding="utf-8") as f:
        queue = json.load(f)

    print(f"=== ComfyUI Generation Runner ===")
    print(f"Queue items: {len(queue)}")
    print(f"Checkpoint: {CHECKPOINT}")
    print(f"Output base: {OUTPUT_BASE}")
    print(f"---")

    if not args.no_launch:
        print("Starting ComfyUI...")
        proc = start_comfyui()
        if not wait_for_comfyui():
            print("ERROR: ComfyUI did not start")
            proc.terminate()
            return 1
        print("ComfyUI ready")

    manifest = []
    total_items = len(queue)

    try:
        for idx, item in enumerate(queue):
            item_id = item.get("id", f"item-{idx}")
            count = item.get("count", 1)
            seed = hash(item_id + str(time.time())) % (2**31)
            print(f"[{idx+1}/{total_items}] {item_id} ({count} images, seed={seed}) ... ", end="", flush=True)
            workflow = build_workflow(item, seed)
            prompt_id = submit_workflow(workflow)
            wait_for_prompt(prompt_id)
            moved = move_outputs(item, {})
            print(f"done ({len(moved)} files)")
            manifest.append({
                "id": item_id,
                "prompt_key": item.get("prompt_key"),
                "output_subfolder": item.get("output_subfolder"),
                "count": count,
                "seed": seed,
                "files": moved
            })
    finally:
        if not args.no_shutdown:
            print("Shutting down ComfyUI...")
            stop_comfyui()

    with open(args.manifest, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"\n=== GENERATION COMPLETE ===")
    print(f"Manifest saved to: {args.manifest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

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
COMFYUI_ROOT = r"D:\Jake\ComfyUI_windows_portable"
COMFYUI_PYTHON = r"D:\Jake\ComfyUI_windows_portable\python_embeded\python.exe"
OUTPUT_BASE = os.path.join(COMFYUI_DIR, r"output\ComfyUI\annointed-exile")
CHECKPOINT = "dreamshaperXL_sfwLightningDPMSDE.safetensors"
CYCLE_PROGRESS = os.path.join(r"D:\the-exile-king", "CYCLE_PROGRESS.md")
GOOGLE_DRIVE_ROOT = r"G:\My Drive\ArtOutput\annointed-exile"

UNIVERSAL_NEGATIVE = "photorealistic, hyperrealistic, realistic skin texture, photograph, cinematic lighting, ray tracing, 3d render, octane render, unity engine, video game screenshot, modern clothing, plate armor, steel armor, chainmail, scale armor, fantasy armor, elaborate armor, longbow, long sword, greatsword, crossguard, medieval helmet, horned helmet, winged helmet, knight, crusader, viking, samurai, European castle, stone castle, heraldry, coat of arms, shield with cross, shield with lion, glowing, neon, bright colors, anime, manga, cartoon, digital art, illustration, signature, watermark, text, logo, ugly, deformed, blurry, low quality, worst quality, bad anatomy, extra limbs, merged body, duplicate, clone, two people, three people, group, crowded, person, people, human, hands, fingers, nsfw, gore, blood"

CHARACTER_POSITIVE_SUFFIX = ", hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European"
CHARACTER_NEGATIVE_EXTRA = ""

EQUIPMENT_POSITIVE_SUFFIX = ", isolated single object centered on pure white background, clean cutout, hand-painted historical illustration, watercolor and ink, no background, no person, no hands, family friendly, NOT medieval, NOT fantasy, NOT European"
EQUIPMENT_NEGATIVE_EXTRA = "person, people, human, hands, fingers, body, figure, face, background, scenery, landscape, aged parchment, parchment texture, board game card art, composition, scene"

TILE_POSITIVE_SUFFIX = ", top-down flat seamless hex tile texture, parchment texture overlay, watercolor ink wash style, muted earth tones, no grid lines, no borders, no text, board game style, family friendly, NOT medieval, NOT fantasy, NOT European"
TILE_NEGATIVE_EXTRA = "grid lines, borders, text, logo, modern, perspective, 3d, shadow, person, people, human, building, structure, creature, animal"

UI_POSITIVE_SUFFIX = ", flat vector-like UI element, clean vector art style, simple shape, centered, no text, no background, family friendly, NOT medieval, NOT fantasy, NOT European"
UI_NEGATIVE_EXTRA = "hand-painted, watercolor, aged parchment, aged paper, ink wash, textured paper, background, scene, person, people, human, text, logo"

CARD_POSITIVE_SUFFIX = ", scene in illuminated manuscript style, aged parchment background, ink outlines with muted watercolor wash, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European"
CARD_NEGATIVE_EXTRA = "photorealistic, 3d render, modern clothing, anime, manga, cartoon, digital art, text, logo, watermark, signature, ugly, deformed, blurry, low quality"

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
    normalized = prompt_key.replace("-", "_")
    if normalized in EXPECTED_PROMPTS:
        return EXPECTED_PROMPTS[normalized]
    return prompt_key.replace("-", " ")

def classify_asset_type(item):
    prompt_key = item.get("prompt_key", "")
    subfolder = item.get("output_subfolder", "").lower()
    
    if any(x in prompt_key for x in ["hex_", "tile", "grass", "rock", "sand"]):
        return "tile"
    if any(x in prompt_key for x in ["swordsmen-advance", "archer-volley", "spear-wall", "slinger-skirmish", "scout-recon", "refugee-aid", "davids-leadership", "march", "engage"]):
        return "card"
    if any(x in prompt_key for x in ["end-turn", "command-card", "card-frame", "hp-bar", "reward-panel"]) or "ui" in subfolder:
        return "ui"
    if any(x in prompt_key for x in ["bronze-sword", "leather-shield", "spear", "sling", "bow", "camel"]) or "equipment" in subfolder:
        return "equipment"
    return "character"


def build_workflow(item, seed):
    prompt_key = item["prompt_key"]
    asset_type = classify_asset_type(item)
    
    positive = resolve_prompt(prompt_key)
    
    if asset_type == "character":
        positive += CHARACTER_POSITIVE_SUFFIX
    elif asset_type == "equipment":
        positive += EQUIPMENT_POSITIVE_SUFFIX
    elif asset_type == "tile":
        positive += TILE_POSITIVE_SUFFIX
    elif asset_type == "ui":
        positive += UI_POSITIVE_SUFFIX
    elif asset_type == "card":
        positive += CARD_POSITIVE_SUFFIX
    else:
        positive += CHARACTER_POSITIVE_SUFFIX

    negative_parts = [UNIVERSAL_NEGATIVE]
    if asset_type == "equipment":
        negative_parts.append(EQUIPMENT_NEGATIVE_EXTRA)
    elif asset_type == "tile":
        negative_parts.append(TILE_NEGATIVE_EXTRA)
    elif asset_type == "ui":
        negative_parts.append(UI_NEGATIVE_EXTRA)
    elif asset_type == "card":
        negative_parts.append(CARD_NEGATIVE_EXTRA)
    negative = ", ".join(negative_parts)
    
    width = item.get("width", 512)
    height = item.get("height", 512)
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
                "batch_size": 1
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
    was_running = False
    while time.time() - start < timeout:
        try:
            req = urllib.request.Request(f"http://127.0.0.1:8188/queue", method="GET")
            with urllib.request.urlopen(req, timeout=10) as resp:
                queue = json.loads(resp.read().decode("utf-8"))
                running = queue.get("queue_running", [])
                pending = queue.get("queue_pending", [])
                is_running = any(item.get("prompt_id") == prompt_id for item in running)
                if is_running:
                    was_running = True
                elif was_running:
                    return {}
                elif not running and not pending:
                    time.sleep(2)
                    return {}
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


def generate_one_image(item, seed, retries=3):
    prefix = item.get("filename_prefix", "ComfyUI")
    attempt = 0
    last_error = None
    while attempt < retries:
        try:
            workflow = build_workflow(item, seed)
            prompt_id = submit_workflow(workflow)
            wait_for_prompt(prompt_id)
            moved = move_outputs(item, {})
            if moved:
                return moved, attempt
            last_error = "No outputs moved"
        except Exception as e:
            last_error = str(e)
        attempt += 1
        if attempt < retries:
            time.sleep(3)
    return [], attempt


def upload_to_google_drive(src_path, dest_relative):
    if not os.path.isfile(src_path):
        return None
    dest = os.path.join(GOOGLE_DRIVE_ROOT, dest_relative)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy2(src_path, dest)
    return dest


def update_cycle_progress(item_id, idx, total_items, count, moved_count, status="generating", seed=None, error=None):
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Generation + Review Cycle Progress",
        "",
        f"**Started:** {now}",
        "**Mode:** Generation batch",
        f"**Current GPU:** GTX 1060 6GB",
        "**ComfyUI flags:** `--disable-auto-launch --lowvram --reserve-vram 2.0 --windows-standalone-build`",
        "**Batch size:** 1 image at a time, sequential",
        "**Review:** deferred",
        "",
        "## Current Status",
        "",
        f"**Cycle state:** {status}",
        f"**Current item:** {item_id}",
        f"**Current queue index:** {idx} / {total_items}",
        f"**Images for current item:** {moved_count} / {count}",
    ]
    if seed is not None:
        lines.append(f"**Base seed:** {seed}")
    if error:
        lines.append(f"**Last error:** {error}")
    content = "\n".join(lines) + "\n"
    with open(CYCLE_PROGRESS, "w", encoding="utf-8") as f:
        f.write(content)


def start_comfyui():
    cmd = [COMFYUI_PYTHON, "-s", "ComfyUI\\main.py", "--lowvram", "--windows-standalone-build"]
    proc = subprocess.Popen(cmd, cwd=COMFYUI_ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
    parser.add_argument("--limit", type=int, default=0, help="limit number of queue items to process")
    parser.add_argument("--limit-images", type=int, default=0, help="limit total images generated")
    parser.add_argument("--retries", type=int, default=3, help="retries per image on failure")
    parser.add_argument("--fill-missing", action="store_true", help="scan outputs and regenerate any missing images")
    args = parser.parse_args()

    load_prompts()

    with open(args.queue, "r", encoding="utf-8") as f:
        queue = json.load(f)

    if args.limit > 0:
        queue = queue[:args.limit]

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
    total_attempted = sum(item.get("count", 1) for item in queue)
    total_generated = 0
    total_retries_exhausted = 0
    fill_missing_count = 0

    try:
        for idx, item in enumerate(queue):
            item_id = item.get("id", f"item-{idx}")
            count = item.get("count", 1)
            base_seed = hash(item_id + str(time.time())) % (2**31)
            print(f"[{idx+1}/{total_items}] {item_id} ({count} images) ... ", end="", flush=True)
            moved_all = []
            for i in range(count):
                seed = base_seed + i
                moved, retries = generate_one_image(item, seed, args.retries)
                if not moved and retries >= args.retries:
                    total_retries_exhausted += 1
                moved_all.extend(moved)
                update_cycle_progress(item_id, idx + 1, total_items, count, len(moved_all), status="generating", seed=base_seed)
                for rel_path in moved:
                    try:
                        src_path = os.path.join(OUTPUT_BASE, rel_path)
                        upload_to_google_drive(src_path, rel_path)
                    except Exception as e:
                        print(f"\n  GD upload warning: {e}")
            print(f"done ({len(moved_all)} files)")
            total_generated += len(moved_all)
            update_cycle_progress(item_id, idx + 1, total_items, count, count, status="complete", seed=base_seed)
            manifest.append({
                "id": item_id,
                "prompt_key": item.get("prompt_key"),
                "output_subfolder": item.get("output_subfolder"),
                "count": count,
                "seed": base_seed,
                "files": moved_all
            })

        if args.fill_missing:
            for item in queue:
                item_id = item.get("id")
                count = item.get("count", 1)
                subfolder = item.get("output_subfolder", "")
                prefix = item.get("filename_prefix", "ComfyUI")
                dest_dir = os.path.join(OUTPUT_BASE, subfolder)
                existing = 0
                if os.path.isdir(dest_dir):
                    existing = len([f for f in os.listdir(dest_dir) if f.startswith(prefix)])
                if existing < count:
                    needed = count - existing
                    print(f"Fill-missing: {item_id} needs {needed} more images")
                    for i in range(needed):
                        fill_seed = (int(time.time() * 1000) + i) % (2**31)
                        moved, _ = generate_one_image(item, fill_seed, args.retries)
                        if moved:
                            fill_missing_count += len(moved)
                            total_generated += len(moved)
                            for rel_path in moved:
                                try:
                                    src_path = os.path.join(OUTPUT_BASE, rel_path)
                                    upload_to_google_drive(src_path, rel_path)
                                except Exception as e:
                                    print(f"\n  GD upload warning: {e}")
                        else:
                            total_retries_exhausted += 1
                    for entry in manifest:
                        if entry["id"] == item_id:
                            current_files = set(entry.get("files", []))
                            if os.path.isdir(dest_dir):
                                new_files = [os.path.relpath(os.path.join(dest_dir, f), OUTPUT_BASE) for f in os.listdir(dest_dir) if f.startswith(prefix)]
                                entry["files"] = list(current_files.union(new_files))
                            break
    finally:
        if not args.no_shutdown:
            print("Shutting down ComfyUI...")
            stop_comfyui()

    with open(args.manifest, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    update_cycle_progress("-", total_items, total_items, 0, 0, status="complete")
    print(f"\n=== GENERATION COMPLETE ===")
    print(f"Manifest saved to: {args.manifest}")
    print(f"Total generated: {total_generated}")
    print(f"Retries exhausted: {total_retries_exhausted}")
    if args.fill_missing:
        print(f"Fill-missing images generated: {fill_missing_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

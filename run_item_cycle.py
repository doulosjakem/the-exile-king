"""
Item-by-item generation + review cycle.
For each queue item: generate all images → stop ComfyUI → review → fix prompts → next item.
Designed for limited VRAM systems where ComfyUI and Ollama can't run simultaneously.
"""
import argparse
import json
import os
import sys
import time
import subprocess
import shutil
import urllib.request
import urllib.error
import base64
import re

sys.path.insert(0, r"D:\the-exile-king")
from review_art_ollama import EXPECTED_PROMPTS

COMFYUI_DIR = r"D:\Jake\ComfyUI_windows_portable\ComfyUI"
COMFYUI_ROOT = r"D:\Jake\ComfyUI_windows_portable"
COMFYUI_PYTHON = r"D:\Jake\ComfyUI_windows_portable\python_embeded\python.exe"
OUTPUT_BASE = r"G:\My Drive\Projects\Games\Exile King\Art and Assets"
CHECKPOINT = "dreamshaperXL_sfwLightningDPMSDE.safetensors"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "minicpm-v:8b")
QUEUE_PATH = r"D:\the-exile-king\generation_queue.json"
PROGRESS_PATH = r"D:\the-exile-king\cycle_progress.json"
REVIEW_REPORT = os.path.join(OUTPUT_BASE, "_review_report.json")

UNIVERSAL_NEGATIVE = (
    "photorealistic, hyperrealistic, realistic skin texture, photograph, 3d render, "
    "modern clothing, plate armor, steel armor, chainmail, fantasy armor, longbow, long sword, "
    "greatsword, crossguard, medieval helmet, horned helmet, knight, crusader, anime, manga, "
    "cartoon, text, logo, ugly, deformed, blurry, low quality, person, people, human, hands, "
    "fingers, body, figure, face, background, scenery, aged parchment, board game card art"
)

ASSET_SUFFIXES = {
    "character": (
        ", hand-painted historical illustration, watercolor and ink on aged parchment, "
        "board game card art, centered composition, family friendly, "
        "NOT medieval, NOT fantasy, NOT European"
    ),
    "equipment": (
        ", isolated single object centered on pure white background, clean cutout, "
        "hand-painted illustration, watercolor, no background, no person, no hands, "
        "family friendly, NOT medieval, NOT fantasy, NOT European"
    ),
    "tile": (
        ", top-down flat seamless hex tile texture, parchment texture overlay, "
        "watercolor ink wash style, muted earth tones, no grid lines, no borders, no text, "
        "board game style, hand-painted texture, family friendly, NOT medieval, NOT fantasy, NOT European"
    ),
    "ui": (
        ", flat simple UI element, clean shape, centered, no text, no background, "
        "family friendly, NOT medieval, NOT fantasy, NOT European"
    ),
    "card": (
        ", scene in illuminated manuscript style, aged parchment background, "
        "ink outlines with muted watercolor wash, hand-painted historical illustration, "
        "board game card art, family friendly, NOT medieval, NOT fantasy, NOT European"
    ),
}


def classify_asset_type(item):
    prompt_key = item.get("prompt_key", "")
    subfolder = item.get("output_subfolder", "").lower()

    if any(x in prompt_key for x in ["hex_", "tile", "grass", "rock", "sand"]):
        return "tile"
    if any(x in prompt_key for x in [
        "swordsmen-advance", "archer-volley", "spear-wall", "slinger-skirmish",
        "scout-recon", "refugee-aid", "davids-leadership", "march", "engage"
    ]):
        return "card"
    if any(x in prompt_key for x in ["end-turn", "command-card", "card-frame", "hp-bar", "reward-panel"]) or "ui" in subfolder:
        return "ui"
    if any(x in prompt_key for x in [
        "bronze-sword", "leather-shield", "spear", "sling", "bow", "camel"
    ]) or "equipment" in subfolder:
        return "equipment"
    return "character"


def resolve_prompt(prompt_key):
    base = EXPECTED_PROMPTS.get(prompt_key, prompt_key.replace("-", " "))
    asset_type = classify_asset_type({"prompt_key": prompt_key})
    return base + ASSET_SUFFIXES.get(asset_type, ASSET_SUFFIXES["character"])


def build_workflow(item, seed):
    prompt_key = item["prompt_key"]
    positive = resolve_prompt(prompt_key)
    negative = UNIVERSAL_NEGATIVE
    width = item.get("width", 512)
    height = item.get("height", 512)
    prefix = item.get("filename_prefix", "ComfyUI")

    return {
        "3": {
            "class_type": "KSampler",
            "inputs": {
                "seed": seed,
                "steps": item.get("steps", 4),
                "cfg": item.get("cfg", 3),
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
            "inputs": {"ckpt_name": CHECKPOINT}
        },
        "5": {
            "class_type": "EmptyLatentImage",
            "inputs": {"width": width, "height": height, "batch_size": 1}
        },
        "6": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": positive, "clip": ["4", 1]}
        },
        "7": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": negative, "clip": ["4", 1]}
        },
        "8": {
            "class_type": "VAEDecode",
            "inputs": {"samples": ["3", 0], "vae": ["4", 2]}
        },
        "9": {
            "class_type": "SaveImage",
            "inputs": {"filename_prefix": prefix, "images": ["8", 0]}
        }
    }


def submit_workflow(workflow, retries=5):
    payload = {"prompt": workflow}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "http://127.0.0.1:8188/prompt",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read().decode("utf-8")).get("prompt_id")
        except Exception as e:
            last_err = e
            time.sleep(5)
    return None


def wait_for_queue_empty(timeout=600):
    start = time.time()
    while time.time() - start < timeout:
        try:
            req = urllib.request.Request("http://127.0.0.1:8188/queue", method="GET")
            with urllib.request.urlopen(req, timeout=10) as resp:
                q = json.loads(resp.read().decode("utf-8"))
                if not q.get("queue_running") and not q.get("queue_pending"):
                    return True
        except Exception:
            pass
        time.sleep(3)
    return False


def wait_for_output_file(prefix, timeout=300):
    comfy_output = os.path.join(COMFYUI_DIR, "output")
    start = time.time()
    initial = len([f for f in os.listdir(comfy_output) if f.startswith(prefix)])
    while time.time() - start < timeout:
        current = len([f for f in os.listdir(comfy_output) if f.startswith(prefix)])
        if current > initial:
            return True
        time.sleep(3)
    return False


def move_outputs(item):
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
        if os.path.exists(dest):
            os.remove(dest)
        shutil.move(src, dest)
        moved.append(os.path.relpath(dest, OUTPUT_BASE))
    return moved


def start_comfyui():
    hard_cleanup()
    cmd = [COMFYUI_PYTHON, "-s", "ComfyUI\\main.py", "--disable-auto-launch", "--lowvram", "--reserve-vram", "2.0", "--windows-standalone-build"]
    proc = subprocess.Popen(cmd, cwd=COMFYUI_ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc


def wait_for_comfyui(timeout=300):
    start = time.time()
    while time.time() - start < timeout:
        try:
            req = urllib.request.Request("http://127.0.0.1:8188/system_stats", method="GET")
            with urllib.request.urlopen(req, timeout=5) as resp:
                return True
        except Exception:
            pass
        time.sleep(3)
    return False


def stop_comfyui(proc):
    try:
        req = urllib.request.Request("http://127.0.0.1:8188/stop", method="POST")
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        pass
    try:
        proc.wait(timeout=20)
    except subprocess.TimeoutExpired:
        proc.kill()
    time.sleep(10)


def hard_cleanup():
    for name in ["ollama app", "ollama", "llama-server"]:
        subprocess.run(["taskkill", "/F", "/T", "/IM", f"{name}.exe"], capture_output=True)
    current_pid = os.getpid()
    try:
        out = subprocess.check_output(["tasklist", "/FO", "CSV", "/NH"]).decode("utf-8", errors="ignore")
        for line in out.splitlines():
            if "python.exe" not in line.lower():
                continue
            parts = [p.strip('"') for p in line.split(",")]
            if len(parts) >= 2 and int(parts[1]) != current_pid:
                subprocess.run(["taskkill", "/F", "/T", "/PID", parts[1]], capture_output=True)
    except Exception:
        pass
    time.sleep(5)


def stop_ollama():
    hard_cleanup()


def start_ollama():
    stop_ollama()
    subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    start = time.time()
    while time.time() - start < 60:
        try:
            urllib.request.urlopen("http://127.0.0.1:11434/", timeout=2)
            return True
        except Exception:
            time.sleep(2)
    return False


def ollama_review(image_path, expected_prompt=None, asset_type="generic", timeout=600):
    prompt_parts = [
        "You are an art reviewer for a board game. Judge ONLY these concrete visual features. Do NOT try to identify who or what is depicted.",
        "1. Does it look hand-painted (watercolor/ink)? YES/NO",
        "2. Are the colors muted earth tones or appropriate for the asset type? YES/NO",
        "3. Any modern object, text, logo, person, hands, or background scene? YES/NO",
        "4. Is the image blurry or corrupted? YES/NO",
        "5. Is the composition acceptable? YES/NO",
    ]
    if asset_type in ("character", "card"):
        prompt_parts += [
            "6. Any extra heads, limbs, fingers, or misformed body parts? YES/NO",
            "7. Any weapons or armor wrong for bronze age Levantine? YES/NO",
            "8. Does it match the expected prompt? YES/NO",
            "Output: ANSWER1,ANSWER2,ANSWER3,ANSWER4,ANSWER5,ANSWER6,ANSWER7,ANSWER8",
        ]
    elif asset_type == "tile":
        prompt_parts += [
            "6. Does it look like a top-down flat hex tile with seamless edges? YES/NO",
            "7. Any visible grid lines or borders? YES/NO",
            "8. Does it match the expected prompt? YES/NO",
            "Output: ANSWER1,ANSWER2,ANSWER3,ANSWER4,ANSWER5,ANSWER6,ANSWER7,ANSWER8",
        ]
    else:
        prompt_parts += [
            "6. Does it match the expected prompt? YES/NO",
            "Output: ANSWER1,ANSWER2,ANSWER3,ANSWER4,ANSWER5,ANSWER6",
        ]

    if expected_prompt:
        prompt_parts.insert(1, f"Expected prompt: {expected_prompt}")

    prompt = "\n".join(prompt_parts)

    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "images": [img_b64],
        "stream": False,
        "options": {"temperature": 0.1, "num_ctx": 2048, "num_gpu": -1}
    }

    try:
        req = urllib.request.Request(
            OLLAMA_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("response", "").strip()
    except urllib.error.HTTPError as e:
        if e.code == 500:
            payload["options"]["num_gpu"] = 0
            try:
                req = urllib.request.Request(
                    OLLAMA_URL,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    result = json.loads(resp.read().decode("utf-8"))
                    return "[FALLBACK CPU] " + result.get("response", "").strip()
            except Exception:
                pass
        return f"ERROR: HTTP {e.code}"
    except Exception as e:
        return f"ERROR: {str(e)}"


def parse_answers(response, expected_count=8):
    matches = re.findall(r'\b(YES|NO)\b', response.upper())
    while len(matches) < expected_count:
        matches.append("YES")
    return matches[:expected_count]


def decide(answers, asset_type="generic"):
    expected_count = 8 if asset_type in ("character", "card", "tile") else 6
    while len(answers) < expected_count:
        answers.append("YES")

    painted = answers[0]
    earth = answers[1]
    modern = answers[2]
    blurry = answers[3]
    comp = answers[4]
    extra = answers[5] if expected_count >= 7 else "NO"
    prompt_match = answers[-1]

    score = 5
    reasons = []
    if painted == "NO":
        score -= 1
        reasons.append("not hand-painted")
    if earth == "NO":
        score -= 1
        reasons.append("colors off")
    if modern == "YES":
        score -= 3
        reasons.append("modern object/text/person detected")
    if blurry == "YES":
        score -= 2
        reasons.append("blurry/corrupted")
    if comp == "NO":
        score -= 1
        reasons.append("composition off")
    if extra == "YES":
        score -= 3
        if asset_type == "tile":
            reasons.append("not flat hex tile or has grid")
        else:
            reasons.append("anatomical defect or wrong item")
    if prompt_match == "NO":
        score -= 2
        reasons.append("does not match expected prompt")

    score = max(1, score)
    reason = "; ".join(reasons) if reasons else "all checks passed"

    if modern == "YES" or blurry == "YES" or extra == "YES" or score <= 2:
        return "TRASH", reason, score
    return "KEEP", reason, score


def review_batch(item, files=None):
    subfolder = item.get("output_subfolder", "")
    target_dir = os.path.join(OUTPUT_BASE, subfolder)
    if not os.path.isdir(target_dir):
        return []

    prompt_key = item.get("prompt_key")
    expected = EXPECTED_PROMPTS.get(prompt_key, prompt_key)
    asset_type = classify_asset_type(item)

    if files is None:
        files = sorted([
            f for f in os.listdir(target_dir)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
            and not f.startswith(".")
        ])
    if not files:
        return []

    results = []
    for fname in files:
        fpath = os.path.join(target_dir, fname)
        print(f"  Reviewing {fname} ... ", end="", flush=True)
        response = ollama_review(fpath, expected_prompt=expected, asset_type=asset_type)

        if response.startswith("ERROR"):
            print(f"ERROR: {response}")
            results.append({
                "filename": os.path.relpath(fpath, OUTPUT_BASE),
                "decision": "ERROR",
                "score": 0,
                "reason": response,
                "answers": [],
                "raw_response": response
            })
            continue

        expected_count = 8 if asset_type in ("character", "card", "tile") else 6
        answers = parse_answers(response, expected_count=expected_count)
        decision, reason, score = decide(answers, asset_type=asset_type)
        print(f"{decision} | {score} | {reason}")

        results.append({
            "filename": os.path.relpath(fpath, OUTPUT_BASE),
            "expected_prompt_key": prompt_key,
            "asset_type": asset_type,
            "decision": decision,
            "score": score,
            "reason": reason,
            "answers": answers,
            "raw_response": response
        })
    return results


def summarize(results):
    keep = sum(1 for r in results if r["decision"] == "KEEP")
    trash = sum(1 for r in results if r["decision"] == "TRASH")
    errors = sum(1 for r in results if r["decision"] == "ERROR")
    print(f"  Summary: {keep} KEEP, {trash} TRASH, {errors} ERROR")
    return keep, trash, errors


def suggest_prompt_fixes(results):
    suggestions = {}
    for r in results:
        if r["decision"] != "TRASH" or r["score"] >= 3:
            continue
        key = r.get("expected_prompt_key")
        if not key:
            continue
        response = r.get("raw_response", "").lower()
        fixes = []
        if any(word in response for word in ["person", "people", "human", "hands", "hand"]):
            fixes.append("isolated object, no person, no hands")
        if any(word in response for word in ["background", "parchment", "texture"]):
            if r.get("asset_type") == "equipment":
                fixes.append("pure white background, clean cutout")
        if any(word in response for word in ["blurry", "low quality", "deformed", "ugly"]):
            fixes.append("increase quality keywords")
        if any(word in response for word in ["modern", "not accurate", "wrong", "does not match"]):
            fixes.append("strengthen era-lock language")
        if fixes:
            suggestions[key] = fixes
    return suggestions


def apply_prompt_fixes(suggestions):
    applied = []
    for key, fixes in suggestions.items():
        if key not in EXPECTED_PROMPTS:
            continue
        current = EXPECTED_PROMPTS[key]
        updated = current
        for fix in fixes:
            fix_lower = fix.lower()
            if "isolated object" in fix_lower and "isolated" not in updated.lower():
                updated = updated.rstrip(".") + ", isolated, no person, no hands"
            if "pure white background" in fix_lower and "pure white background" not in updated.lower():
                updated = updated.rstrip(".") + ", pure white background, clean cutout"
            if "increase quality keywords" in fix_lower:
                updated = updated.rstrip(".") + ", high quality, detailed"
            if "strengthen era-lock" in fix_lower:
                updated = updated.rstrip(".") + ", historically accurate bronze age Levantine"
        if updated != current:
            EXPECTED_PROMPTS[key] = updated
            applied.append((key, updated))
    return applied


def save_progress(state):
    with open(PROGRESS_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def load_progress():
    if os.path.exists(PROGRESS_PATH):
        with open(PROGRESS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"last_index": 0, "results": [], "retry_items": []}


def process_item(item, base_seed=1000, skip_review=False, comfy_proc=None):
    item_id = item["id"]
    prompt_key = item["prompt_key"]
    count = item.get("count", 1)
    subfolder = item.get("output_subfolder", "")
    prefix = item.get("filename_prefix", "ComfyUI")

    print(f"\n{'='*60}")
    print(f"ITEM: {item_id}")
    print(f"Prompt: {prompt_key}")
    print(f"Count: {count}")
    print(f"Output: {subfolder}")
    print(f"{'='*60}")

    we_started_comfy = comfy_proc is None

    # Generation phase
    print("\n--- GENERATION ---")
    dest_dir = os.path.join(OUTPUT_BASE, subfolder)
    os.makedirs(dest_dir, exist_ok=True)
    existing = [f for f in os.listdir(dest_dir) if f.startswith(prefix)]
    if len(existing) >= count:
        print(f"  SKIP: {len(existing)}/{count} files already exist in {subfolder}")
        generated = len(existing)
        moved_files = existing
    else:
        if we_started_comfy:
            hard_cleanup()
            proc = start_comfyui()
            if not wait_for_comfyui():
                print("ERROR: ComfyUI did not start")
                return False, {
                    "item_id": item_id,
                    "prompt_key": prompt_key,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "generated": 0,
                    "keep": 0,
                    "trash": 0,
                    "errors": 1,
                    "results": []
                }
        else:
            proc = comfy_proc
            if not wait_for_comfyui(timeout=10):
                print("  ERROR: ComfyUI server unreachable between items")
                return False, {
                    "item_id": item_id,
                    "prompt_key": prompt_key,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "generated": 0,
                    "keep": 0,
                    "trash": 0,
                    "errors": 1,
                    "results": []
                }

        try:
            failed = 0
            generated = 0
            moved_files = []
            for i in range(count):
                if not wait_for_comfyui(timeout=10):
                    print("  ERROR: ComfyUI server unreachable")
                    break
                seed = base_seed + i
                batch_item = dict(item)
                batch_item["batch_size"] = 1
                workflow = build_workflow(batch_item, seed)
                prompt_id = submit_workflow(workflow)
                if not prompt_id:
                    failed += 1
                    print(f"  FAILED image {i+1}/{count} (seed {seed})")
                    if failed >= 3:
                        print("  Too many generation failures, aborting item")
                        break
                    continue

                if not wait_for_queue_empty(timeout=600):
                    failed += 1
                    print(f"  FAILED: queue did not complete for seed {seed}")
                    if failed >= 3:
                        print("  Too many generation failures, aborting item")
                        break
                    continue

                time.sleep(5)

                expected_name = f"{prefix}_{seed:05d}_.png"
                if wait_for_output_file(prefix, timeout=120):
                    print(f"  Generated image {i+1}/{count} (seed {seed})")
                    generated += 1
                else:
                    failed += 1
                    print(f"  FAILED: timeout waiting for {prefix} output")
                    if failed >= 3:
                        print("  Too many generation failures, aborting item")
                        break
                    continue

            moved = move_outputs(item)
            moved_files = moved
            print(f"  Moved {len(moved)} files to {subfolder}")
            if moved:
                generated = len(moved)
        finally:
            if we_started_comfy:
                print("  Stopping ComfyUI to free VRAM...")
                stop_comfyui(proc)
                time.sleep(15)

    # Review phase
    if skip_review:
        print("\n--- REVIEW SKIPPED (--skip-review) ---")
        return True, {
            "item_id": item_id,
            "prompt_key": prompt_key,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "generated": generated,
            "keep": 0,
            "trash": 0,
            "errors": 0,
            "results": []
        }

    print("\n--- REVIEW ---")
    if not start_ollama():
        print("  ERROR: Ollama did not start")
        return True, {
            "item_id": item_id,
            "prompt_key": prompt_key,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "generated": generated,
            "keep": 0,
            "trash": 0,
            "errors": 1,
            "results": []
        }
    results = review_batch(item, files=[os.path.basename(f) for f in moved_files])
    keep, trash, errors = summarize(results)

    # Prompt fix suggestions
    suggestions = suggest_prompt_fixes(results)
    if suggestions:
        print("\n  Prompt fix suggestions:")
        for key, fixes in suggestions.items():
            print(f"    {key}:")
            for fix in fixes:
                print(f"      - {fix}")

        applied = apply_prompt_fixes(suggestions)
        if applied:
            print("\n  Applying fixes...")
            for key, new_prompt in applied:
                print(f"    Updated: {key}")
    else:
        print("  No prompt fixes needed!")

    # Save item results
    item_report = {
        "item_id": item_id,
        "prompt_key": prompt_key,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "generated": generated,
        "keep": keep,
        "trash": trash,
        "errors": errors,
        "results": results
    }

    return True, item_report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", default=QUEUE_PATH)
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--skip-review", action="store_true", help="generate only, skip ollama review phase")
    parser.add_argument("--base-seed", type=int, default=1000)
    parser.add_argument("--max-retries", type=int, default=2)
    args = parser.parse_args()

    with open(args.queue, "r", encoding="utf-8") as f:
        queue = json.load(f)

    progress = load_progress()
    idx = args.start_index if args.start_index > 0 else progress.get("last_index", 0)
    all_results = progress.get("results", [])

    print(f"=== ITEM-BY-ITEM CYCLE ===")
    print(f"Queue: {len(queue)} items")
    print(f"Starting from index: {idx}")
    print(f"Base seed: {args.base_seed}")
    print()

    cycle = 0
    comfy_proc = None
    try:
        if not args.skip_review:
            hard_cleanup()
            comfy_proc = start_comfyui()
            if not wait_for_comfyui(timeout=300):
                print("ERROR: ComfyUI did not start")
                return
            print("ComfyUI started for generation phase\n")

        while idx < len(queue):
            item = queue[idx]
            base_seed = args.base_seed + cycle * 1000

            success, item_report = process_item(
                item,
                base_seed=base_seed,
                skip_review=args.skip_review,
                comfy_proc=comfy_proc,
            )
            all_results.append(item_report)

            state = {
                "last_index": idx + 1,
                "results": all_results,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            save_progress(state)

            if not success:
                print("\nGeneration failed. Moving to next item.")
                idx += 1
                cycle += 1
                continue

            retry_count = 0
            while retry_count < args.max_retries and item_report["trash"] > 0:
                retry_count += 1
                print(f"\n--- RETRY {retry_count}/{args.max_retries} ---")

                bad_keys = list(set(
                    r["expected_prompt_key"] for r in item_report["results"]
                    if r["decision"] == "TRASH" and r.get("expected_prompt_key")
                ))
                if not bad_keys:
                    break

                suggestions = {k: ["increase quality keywords, strengthen era-lock"] for k in bad_keys}
                applied = apply_prompt_fixes(suggestions)
                for key, _ in applied:
                    print(f"  Auto-fixed: {key}")

                retry_seed = base_seed + retry_count * 50
                success, item_report = process_item(
                    item,
                    base_seed=retry_seed,
                    skip_review=args.skip_review,
                    comfy_proc=comfy_proc,
                )
                all_results.append(item_report)
                state["last_index"] = idx + 1
                state["results"] = all_results
                save_progress(state)

            idx += 1
            cycle += 1

            # Status update
            total_keep = sum(1 for r in all_results if r.get("keep", 0) > 0)
            total_trash = sum(r.get("trash", 0) for r in all_results)
            print(f"\n{'='*60}")
            print(f"STATUS: {idx}/{len(queue)} items complete")
            print(f"Total KEEP: {total_keep}, TRASH: {total_trash}")
            print(f"Progress saved to: {PROGRESS_PATH}")
            print(f"{'='*60}")
    finally:
        if comfy_proc is not None:
            print("\nStopping ComfyUI...")
            stop_comfyui(comfy_proc)

    print(f"\n{'='*60}")
    print(f"CYCLE COMPLETE")
    print(f"Processed {idx}/{len(queue)} items")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()

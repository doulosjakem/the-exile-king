"""
Generation + review cycle for limited VRAM systems.
ComfyUI and Ollama cannot both hold large models in ~6GB VRAM at once.
This script alternates: generate batch -> free VRAM -> review -> fix prompts -> repeat.
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
from run_comfyui_generation import (
    build_workflow, submit_workflow, move_outputs, wait_for_prompt
)
from review_art_ollama import EXPECTED_PROMPTS, load_expected_prompts

COMFYUI_DIR = r"D:\Jake\ComfyUI_windows_portable\ComfyUI"
COMFYUI_ROOT = r"D:\Jake\ComfyUI_windows_portable"
COMFYUI_PYTHON = r"D:\Jake\ComfyUI_windows_portable\python_embeded\python.exe"
OUTPUT_BASE = os.path.join(COMFYUI_DIR, r"output\ComfyUI\annointed-exile")
CHECKPOINT = "dreamshaperXL_sfwLightningDPMSDE.safetensors"
OLLAMA_URL = "http://localhost:11434/api/generate"
QUEUE_PATH = r"D:\the-exile-king\generation_queue.json"
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
        return json.loads(resp.read().decode("utf-8")).get("prompt_id")


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
        if not os.path.exists(dest):
            shutil.move(src, dest)
            moved.append(os.path.relpath(dest, OUTPUT_BASE))
    return moved


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


def ollama_review(image_path, expected_prompt=None, asset_type="generic", timeout=180):
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
        "model": "minicpm-v:8b",
        "prompt": prompt,
        "images": [img_b64],
        "stream": False,
        "options": {"temperature": 0.1, "num_ctx": 2048}
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


def review_batch(item):
    subfolder = item.get("output_subfolder", "")
    target_dir = os.path.join(OUTPUT_BASE, subfolder)
    if not os.path.isdir(target_dir):
        return []

    prompt_key = item.get("prompt_key")
    expected = EXPECTED_PROMPTS.get(prompt_key, prompt_key)
    asset_type = classify_asset_type(item)

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
        if "person" in response or "people" in response or "human" in response or "hands" in response or "hand" in response:
            fixes.append("isolated object, no person, no hands")
        if "background" in response or "parchment" in response or "texture" in response:
            if r.get("asset_type") == "equipment":
                fixes.append("pure white background, clean cutout")
        if "blurry" in response or "low quality" in response:
            fixes.append("increase quality keywords")
        if "modern" in response or "not" in response:
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


def generation_phase(queue_items, base_seed=1000):
    print("\n--- GENERATION ---")
    proc = start_comfyui()
    try:
        if not wait_for_comfyui():
            print("ERROR: ComfyUI did not start")
            return False

        for idx, item in enumerate(queue_items):
            item_id = item.get("id", f"item-{idx}")
            count = item.get("count", 1)
            prefix = item.get("filename_prefix", "ComfyUI")

            print(f"\n[{idx+1}/{len(queue_items)}] {item_id} ({count}x) ... ", end="", flush=True)

            dest_dir = os.path.join(OUTPUT_BASE, item.get("output_subfolder", ""))
            existing = len([
                f for f in os.listdir(dest_dir)
                if f.startswith(prefix) and not f.startswith(".")
            ]) if os.path.isdir(dest_dir) else 0

            moved_all = []
            for i in range(count):
                seed = base_seed + idx * 100 + i
                batch_item = dict(item)
                batch_item["batch_size"] = 1
                workflow = build_workflow(batch_item, seed)
                prompt_id = submit_workflow(workflow)
                wait_for_prompt(prompt_id)
                moved = move_outputs(batch_item)
                moved_all.extend(moved)
            print(f"done ({len(moved_all)} moved, {existing} pre-existing)")
        return True
    finally:
        print("Stopping ComfyUI to free VRAM for review...")
        stop_comfyui()
        try:
            proc.wait(timeout=15)
        except subprocess.TimeoutExpired:
            proc.kill()
        time.sleep(5)


def review_phase(items):
    print("\n--- REVIEW ---")
    all_results = []
    for item in items:
        item_id = item.get("id", "unknown")
        prompt_key = item.get("prompt_key", "unknown")
        print(f"\nReviewing {item_id} ({prompt_key}):")
        results = review_batch(item)
        all_results.extend(results)
        keep, trash, errors = summarize(results)

        suggestions = suggest_prompt_fixes(results)
        if suggestions:
            print("\n  Prompt fix suggestions:")
            for key, fixes in suggestions.items():
                print(f"    {key}: {fixes}")
    return all_results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", default=QUEUE_PATH)
    parser.add_argument("--items", type=int, default=2)
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--base-seed", type=int, default=1000)
    args = parser.parse_args()

    with open(args.queue, "r", encoding="utf-8") as f:
        queue = json.load(f)

    cycle = 0
    idx = args.start_index
    while idx < len(queue):
        batch = queue[idx:idx + args.items]
        print(f"\n{'='*60}")
        print(f"CYCLE {cycle+1}: items {idx+1}-{min(idx+args.items, len(queue))} of {len(queue)}")
        print(f"{'='*60}")

        seed = args.base_seed + cycle * 1000
        if not generation_phase(batch, base_seed=seed):
            print("Generation failed. Stopping.")
            break

        results = review_phase(batch)

        suggestions = suggest_prompt_fixes(results)
        if suggestions:
            print("\n=== APPLYING PROMPT FIXES ===")
            applied = apply_prompt_fixes(suggestions)
            for key, new_prompt in applied:
                print(f"  Updated: {key}")
                with open(r"D:\the-exile-king\PROMPTS.md", "a", encoding="utf-8") as f:
                    f.write(f"\nAuto-updated {key}: {new_prompt}\n")

        with open(REVIEW_REPORT, "w", encoding="utf-8") as f:
            json.dump({
                "cycle": cycle + 1,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "items_processed": len(batch),
                "results": results
            }, f, indent=2, ensure_ascii=False)

        idx += len(batch)
        cycle += 1
        print(f"\nCycle {cycle} complete. Next batch starts at index {idx}.")

    print(f"\n{'='*60}")
    print(f"QUEUE COMPLETE: {idx}/{len(queue)} items processed")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()

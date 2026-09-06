"""
EXPERIMENT 1: VAE ROUNDTRIP ONLY
Isolates whether the VAE encode/decode path alone produces substantial
whole-image changes.

Process:
  original -> resize_to_square(1024) -> VAEEncode -> VAEDecode -> reconstructed
  Compare reconstructed vs original (at original resolution after undo_padding).

No KSampler, no InpaintModelConditioning, no diffusion. Pure VAE encode/decode.
"""
import os
import json
import time
import numpy as np
import cv2
import torch
from PIL import Image
import urllib.request
import urllib.error

ORIGINAL_ROOT = r"D:\the-exile-king\art\prototype\commander-cards"
QA_DIR = r"D:\the-exile-king\art\corrected\experiment"
QA_LOGS_DIR = os.path.join(QA_DIR, "logs")

os.makedirs(QA_DIR, exist_ok=True)
os.makedirs(QA_LOGS_DIR, exist_ok=True)

COMFYUI_DIR = r"D:\Jake\ComfyUI_windows_portable\ComfyUI"
COMFYUI_INPUT = os.path.join(COMFYUI_DIR, "input")
COMFYUI_OUTPUT = os.path.join(COMFYUI_DIR, "output")
API_URL = "http://127.0.0.1:8188"

CHECKPOINT = "sdxl_inpainting_v2.safetensors"

TEST_FILES = [
    {"name": "achish-01_00001_.png", "type": "MediaPipe", "notes": "MediaPipe, outside=34.95%"},
    {"name": "david-09_00003_.png", "type": "MediaPipe", "notes": "MediaPipe, lowest outside change (20.2%)"},
    {"name": "achish-03_00001_.png", "type": "Fallback", "notes": "Fallback, outside=26.65%"},
    {"name": "david-05_00002_.png", "type": "Fallback", "notes": "Fallback, outside=29.5%"},
    {"name": "jonathan-08_00002_.png", "type": "MediaPipe-complex", "notes": "MediaPipe, large mask (56k px), outside=38.71%"},
]


def resize_to_square(img, target_size=1024):
    original_size = img.size
    w, h = original_size
    scale = target_size / max(w, h)
    new_w = int(w * scale)
    new_h = int(h * scale)
    resized = img.resize((new_w, new_h), Image.LANCZOS)
    padded = Image.new("RGB", (target_size, target_size), (0, 0, 0))
    offset = ((target_size - new_w) // 2, (target_size - new_h) // 2)
    padded.paste(resized, offset)
    return padded, offset, scale, original_size


def undo_padding(img_padded, offset, scale, original_size):
    target_w = int(original_size[0] * scale)
    target_h = int(original_size[1] * scale)
    crop_box = (offset[0], offset[1], offset[0] + target_w, offset[0] + target_h)
    cropped = img_padded.crop(crop_box)
    result = cropped.resize(original_size, Image.LANCZOS)
    return result


def submit_workflow(workflow):
    data = json.dumps({"prompt": workflow, "client_id": "vae_roundtrip_exp"}).encode()
    req = urllib.request.Request(f"{API_URL}/prompt", data=data,
                                 headers={"Content-Type": "application/json"}, method="POST")
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read())
    except Exception as e:
        return {"error": str(e)}


def wait_prompt_done(prompt_id, timeout=300):
    start = time.time()
    was_running = False
    while time.time() - start < timeout:
        try:
            req = urllib.request.Request(f"{API_URL}/queue", method="GET")
            with urllib.request.urlopen(req, timeout=10) as resp:
                queue = json.loads(resp.read())
                running = queue.get("queue_running", [])
                is_running = any(
                    (isinstance(item, list) and len(item) > 1 and item[1] == prompt_id) or
                    (isinstance(item, dict) and item.get("prompt_id") == prompt_id)
                    for item in running)
                if is_running:
                    was_running = True
                elif was_running:
                    return True
                elif not running and not queue.get("queue_pending", []):
                    time.sleep(1)
                    return True
        except:
            pass
        time.sleep(2)
    return False


def check_success(prompt_id):
    try:
        req = urllib.request.Request(f"{API_URL}/history?prompt_id={prompt_id}", method="GET")
        with urllib.request.urlopen(req, timeout=10) as resp:
            history = json.loads(resp.read())
        if prompt_id in history:
            status = history[prompt_id].get("status", {})
            if status.get("completed", False):
                errors = status.get("errors", [])
                if errors:
                    return False, str(errors)
                return True, None
            return False, "Not completed"
        return False, "No history entry"
    except Exception as e:
        return False, str(e)


def get_vae_roundtrip_workflow(img_filename, prefix):
    """Pure VAE roundtrip: VAEEncode -> VAEDecode (no KSampler, no InpaintModelConditioning)."""
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": CHECKPOINT}},
        "2": {"class_type": "LoadImage", "inputs": {"image": img_filename}},
        "3": {"class_type": "VAEEncode", "inputs": {"pixels": ["2", 0], "vae": ["1", 2]}},
        "4": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["1", 2]}},
        "5": {"class_type": "SaveImage", "inputs": {"images": ["4", 0], "filename_prefix": prefix}},
    }


def compute_metrics(original, reconstructed):
    """Compute MSE, pixel change ratio, and other metrics between two images."""
    orig_arr = np.array(original, dtype=np.float32)
    recon_arr = np.array(reconstructed, dtype=np.float32)

    # MSE
    mse = np.mean((orig_arr - recon_arr) ** 2)

    # Per-channel differences
    diff = np.abs(orig_arr - recon_arr)
    diff_gray = diff.mean(axis=2)

    # Pixel change ratio (threshold: any channel diff > 2)
    changed = np.any(diff > 2, axis=2)
    total_pixels = orig_arr.shape[0] * orig_arr.shape[1]
    changed_pixels = np.count_nonzero(changed)
    change_ratio_pct = (changed_pixels / total_pixels) * 100

    # Mean absolute difference
    mad = np.mean(diff_gray)

    # Max difference
    max_diff = np.max(diff_gray)

    # Standard deviation of differences
    std_diff = np.std(diff_gray)

    # Localize max change region
    max_y, max_x = np.unravel_index(np.argmax(diff_gray), diff_gray.shape)

    return {
        "mse": round(float(mse), 4),
        "rmse": round(float(np.sqrt(mse)), 4),
        "pixel_change_ratio_pct": round(float(change_ratio_pct), 2),
        "changed_pixels": int(changed_pixels),
        "total_pixels": int(total_pixels),
        "mean_abs_diff": round(float(mad), 4),
        "max_abs_diff": round(float(max_diff), 4),
        "std_diff": round(float(std_diff), 4),
        "max_diff_location": [int(max_y), int(max_x)],
    }


def main():
    results = {"vae_roundtrip": []}

    print("=" * 70)
    print("EXPERIMENT 1: VAE ROUNDTRIP ONLY")
    print("Process: original -> VAEEncode -> VAEDecode (no diffusion)")
    print("=" * 70)

    for test in TEST_FILES:
        fname = test["name"]
        prefix = f"vae_rt_{fname.replace('.png', '')}"

        print(f"\n[{fname}] ({test['type']})")
        print(f"  {test['notes']}")

        # Load original
        orig_path = os.path.join(ORIGINAL_ROOT, fname)
        if not os.path.exists(orig_path):
            print(f"  ERROR: Original not found at {orig_path}")
            continue
        img_orig = Image.open(orig_path).convert("RGB")
        print(f"  Original size: {img_orig.size}")

        # Resize to 1024x1024 square (same as pipeline)
        img_padded, offset, scale, orig_size = resize_to_square(img_orig, 1024)
        print(f"  Padded size: {img_padded.size}, offset={offset}, scale={scale:.4f}")

        # Save padded image to ComfyUI input
        img_name = f"{prefix}.png"
        padded_path = os.path.join(COMFYUI_INPUT, img_name)
        img_padded.save(padded_path)
        print(f"  Saved padded image to ComfyUI input: {img_name}")

        # Submit VAE-only roundtrip workflow
        print(f"  Submitting VAE roundtrip workflow...")
        workflow = get_vae_roundtrip_workflow(img_name, prefix)
        result = submit_workflow(workflow)

        if "error" in result:
            print(f"  ERROR submitting: {result['error']}")
            continue

        prompt_id = result["prompt_id"]
        print(f"  Prompt ID: {prompt_id}")

        success = wait_prompt_done(prompt_id, timeout=300)
        if not success:
            print(f"  TIMEOUT waiting for completion")
            continue

        ok, errors = check_success(prompt_id)
        if not ok:
            print(f"  ERROR: {errors}")
            continue

        # Find output
        output_files = sorted([f for f in os.listdir(COMFYUI_OUTPUT) if f.startswith(prefix)])
        if not output_files:
            print(f"  ERROR: No output file found")
            continue

        output_file = output_files[-1]
        output_path = os.path.join(COMFYUI_OUTPUT, output_file)
        recon_padded = Image.open(output_path).convert("RGB")
        print(f"  Output: {output_file}")

        # Undo padding to original dimensions
        recon_orig = undo_padding(recon_padded, offset, scale, orig_size)
        print(f"  Reconstructed size: {recon_orig.size}")

        # Compute metrics
        metrics = compute_metrics(img_orig, recon_orig)

        print(f"  MSE: {metrics['mse']}")
        print(f"  RMSE: {metrics['rmse']}")
        print(f"  Pixel change ratio: {metrics['pixel_change_ratio_pct']}%")
        print(f"  Mean abs diff: {metrics['mean_abs_diff']}")
        print(f"  Max abs diff: {metrics['max_abs_diff']}")
        print(f"  Std diff: {metrics['std_diff']}")
        print(f"  Max diff location: {metrics['max_diff_location']}")

        # Visual assessment
        mad = metrics['mean_abs_diff']
        change_pct = metrics['pixel_change_ratio_pct']

        if mad < 0.5 and change_pct < 1:
            visual = "Negligible change - VAE roundtrip is lossless to human perception"
        elif mad < 2 and change_pct < 5:
            visual = "Minor change - subtle VAE quantization, not visible to human eye"
        elif mad < 5 and change_pct < 15:
            visual = "Noticeable change - visible quality degradation, some artifacts"
        else:
            visual = "Significant change - severe VAE artifacts, substantial degradation"

        results["vae_roundtrip"].append({
            "filename": fname,
            "mask_type": test["type"],
            "metrics": metrics,
            "visual_assessment": visual,
        })

        # Save reconstructed image
        recon_orig.save(os.path.join(QA_DIR, f"{prefix}_recon.png"))

        # Save difference visualization
        diff_img = np.abs(np.array(img_orig, dtype=np.float32) - np.array(recon_orig, dtype=np.float32))
        diff_vis = (diff_img / max(diff_img.max(), 1) * 255).astype(np.uint8)
        Image.fromarray(diff_vis).save(os.path.join(QA_DIR, f"{prefix}_diff.png"))

        # Cleanup ComfyUI files
        for f in [img_name]:
            p = os.path.join(COMFYUI_INPUT, f)
            if os.path.exists(p):
                os.remove(p)
        for f in output_files:
            p = os.path.join(COMFYUI_OUTPUT, f)
            if os.path.exists(p):
                os.remove(p)

    # Save results
    log_path = os.path.join(QA_LOGS_DIR, "vae_roundtrip_results.json")
    with open(log_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n{'=' * 70}")
    print(f"Results saved to: {log_path}")
    print(f"QA artifacts in: {QA_DIR}")

    # Summary
    print(f"\nSUMMARY:")
    avg_mse = np.mean([r["metrics"]["mse"] for r in results["vae_roundtrip"]])
    avg_change = np.mean([r["metrics"]["pixel_change_ratio_pct"] for r in results["vae_roundtrip"]])
    avg_mad = np.mean([r["metrics"]["mean_abs_diff"] for r in results["vae_roundtrip"]])
    print(f"  Avg MSE: {avg_mse:.4f}")
    print(f"  Avg pixel change ratio: {avg_change:.2f}%")
    print(f"  Avg mean abs diff: {avg_mad:.4f}")
    print(f"  Max pixel change ratio: {max(r['metrics']['pixel_change_ratio_pct'] for r in results['vae_roundtrip']):.2f}%")

    return results


if __name__ == "__main__":
    main()

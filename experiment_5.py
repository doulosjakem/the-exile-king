"""
EXPERIMENT 5: Controlled SDXL Inpaint + Original-Image Composite
===============================================================

Tests ONE architectural change: ADD ORIGINAL-IMAGE COMPOSITING AFTER
INPAITING using ImageCompositeMasked.

Pipeline:
  1. Pad original image (512x768) to 1024x1024
  2. Run SDXL inpainting (same checkpoint/settings as existing pipeline)
  3. ImageCompositeMasked composites inpainted result onto padded original
  4. Compute preservation metrics at 1024x1024 (where compositing is clean)
  5. Crop to 512x768 for visual QA artifacts

Settings remain unchanged from existing pipeline (one variable at a time):
  - Checkpoint: sdxl_inpainting_v2.safetensors
  - Sampler: dpmpp_sde, cfg=5.0, steps=8, denoise=0.5
  - Mask: existing masks from art/output/masks/
"""
import os
import sys
import json
import time
import shutil
import numpy as np
import cv2
import urllib.request
import urllib.error
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

COMFYUI_DIR = r"D:\Jake\ComfyUI_windows_portable\ComfyUI"
COMFYUI_INPUT = os.path.join(COMFYUI_DIR, "input")
COMFYUI_OUTPUT = os.path.join(COMFYUI_DIR, "output")
API_URL = "http://127.0.0.1:8188"

CHECKPOINT = "sdxl_inpainting_v2.safetensors"

ORIGINAL_ROOT = r"D:\the-exile-king\art\prototype\commander-cards"
EXISTING_MASK_DIR = r"D:\the-exile-king\art\output\masks"
EXISTING_OUTPUT_DIR = r"D:\the-exile-king\art\output"

QA_DIR = r"D:\the-exile-king\art\corrected\experiment5"
QA_LOGS_DIR = os.path.join(QA_DIR, "logs")

os.makedirs(QA_DIR, exist_ok=True)
os.makedirs(QA_LOGS_DIR, exist_ok=True)

POSITIVE_PROMPT = (
    "anatomically correct hand, five fingers, correct proportions, "
    "properly formed weapon, consistent object geometry, "
    "hand-painted historical illustration, watercolor and ink, "
    "board game card art, family friendly, consistent art style"
)
NEGATIVE_PROMPT = (
    "extra fingers, fused fingers, malformed hand, duplicate weapon, "
    "warped blade, extra limbs, deformed, blurry, low quality, "
    "worst quality, bad anatomy, extra arms, mutation, disfigured"
)

SAMPLER_NAME = "dpmpp_sde"
SCHEDULER = "karras"
CFG = 5.0
STEPS = 8
DENOISE = 0.5
GROW_MASK_BY = 8

TEST_CASES = [
    {"name": "achish-01_00001_.png", "type": "MediaPipe", "notes": "straightforward MediaPipe case"},
    {"name": "jonathan-08_00002_.png", "type": "MediaPipe-complex", "notes": "complex MediaPipe, large mask (56k px)"},
    {"name": "achish-03_00001_.png", "type": "Fallback", "notes": "fallback mask, skin tone 21%, dark area"},
    {"name": "david-09_00003_.png", "type": "Fallback", "notes": "fallback mask, high skin tone 69.3%"},
    {"name": "david-02_00002_.png", "type": "Fallback", "notes": "fallback with weapon+armor overlap"},
]

TARGET_SIZE = 1024


def resize_to_square(img, target_size=TARGET_SIZE):
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
    payload = {"prompt": workflow}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{API_URL}/prompt",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read())
    except Exception as e:
        return {"error": str(e)}


def wait_prompt_done(prompt_id, timeout=600):
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
                    for item in running
                )
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


def get_compositing_workflow(img_filename, mask_filename, seed):
    """Build ComfyUI workflow with ImageCompositeMasked for final compositing.

    ImageCompositeMasked:
    - destination = original padded image (1024x1024)
    - source = VAEDecode output (1024x1024)
    - mask = hand mask (1024x1024)
    - resize_source = False (both are 1024x1024, no resize needed)

    Result: original everywhere outside mask, inpainted result inside mask.
    """
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": CHECKPOINT}},
        "2": {"class_type": "LoadImage", "inputs": {"image": img_filename}},
        "3": {"class_type": "LoadImageMask", "inputs": {"image": mask_filename, "channel": "red"}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {"text": POSITIVE_PROMPT, "clip": ["1", 1]}},
        "5": {"class_type": "CLIPTextEncode", "inputs": {"text": NEGATIVE_PROMPT, "clip": ["1", 1]}},
        "6": {"class_type": "VAEEncodeForInpaint",
              "inputs": {"pixels": ["2", 0], "vae": ["1", 2], "mask": ["3", 0], "grow_mask_by": GROW_MASK_BY}},
        "7": {"class_type": "KSampler",
              "inputs": {"model": ["1", 0], "seed": seed, "steps": STEPS, "cfg": CFG,
                         "sampler_name": SAMPLER_NAME, "scheduler": SCHEDULER,
                         "positive": ["4", 0], "negative": ["5", 0],
                         "latent_image": ["6", 0], "denoise": DENOISE}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["7", 0], "vae": ["1", 2]}},
        "9": {"class_type": "ImageCompositeMasked",
              "inputs": {"destination": ["2", 0], "source": ["8", 0], "x": 0, "y": 0,
                         "resize_source": False, "mask": ["3", 0]}},
        "10": {"class_type": "SaveImage", "inputs": {"images": ["9", 0], "filename_prefix": ""}},
    }


def get_raw_workflow(img_filename, mask_filename, seed):
    """Build workflow WITHOUT ImageCompositeMasked (for raw output comparison)."""
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": CHECKPOINT}},
        "2": {"class_type": "LoadImage", "inputs": {"image": img_filename}},
        "3": {"class_type": "LoadImageMask", "inputs": {"image": mask_filename, "channel": "red"}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {"text": POSITIVE_PROMPT, "clip": ["1", 1]}},
        "5": {"class_type": "CLIPTextEncode", "inputs": {"text": NEGATIVE_PROMPT, "clip": ["1", 1]}},
        "6": {"class_type": "VAEEncodeForInpaint",
              "inputs": {"pixels": ["2", 0], "vae": ["1", 2], "mask": ["3", 0], "grow_mask_by": GROW_MASK_BY}},
        "7": {"class_type": "KSampler",
              "inputs": {"model": ["1", 0], "seed": seed, "steps": STEPS, "cfg": CFG,
                         "sampler_name": SAMPLER_NAME, "scheduler": SCHEDULER,
                         "positive": ["4", 0], "negative": ["5", 0],
                         "latent_image": ["6", 0], "denoise": DENOISE}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["7", 0], "vae": ["1", 2]}},
        "9": {"class_type": "SaveImage", "inputs": {"images": ["8", 0], "filename_prefix": ""}},
    }


def compute_change_stats(orig_arr, output_arr, mask_bin, threshold=2):
    """Compute change statistics between original and output, inside and outside mask.

    All arrays should be at the same resolution.
    - orig_arr: (H, W, 3) uint8
    - output_arr: (H, W, 3) uint8
    - mask_bin: (H, W) bool
    """
    orig_arr = orig_arr.astype(np.float32)
    out_arr = output_arr.astype(np.float32)

    h, w = orig_arr.shape[:2]

    diff = np.abs(orig_arr - out_arr)
    changed = np.any(diff > threshold, axis=2)

    total_pixels = h * w
    mask_pixels = int(np.count_nonzero(mask_bin))
    outside_pixels = total_pixels - mask_pixels

    changed_in_mask = int(np.count_nonzero(np.logical_and(changed, mask_bin)))
    changed_outside_mask = int(np.count_nonzero(np.logical_and(changed, ~mask_bin)))

    mse = float(np.mean((orig_arr - out_arr) ** 2))
    rmse = float(np.sqrt(mse))
    total_change_pct = round(changed.sum() / total_pixels * 100, 2)
    inside_change_pct = round(changed_in_mask / max(mask_pixels, 1) * 100, 2)
    outside_change_pct = round(changed_outside_mask / max(outside_pixels, 1) * 100, 2)

    diff_gray = diff.mean(axis=2)
    mean_diff_masked = float(diff_gray[mask_bin].mean()) if mask_pixels > 0 else 0
    mean_diff_unmasked = float(diff_gray[~mask_bin].mean()) if outside_pixels > 0 else 0
    max_diff_masked = float(diff_gray[mask_bin].max()) if mask_pixels > 0 else 0
    max_diff_unmasked = float(diff_gray[~mask_bin].max()) if outside_pixels > 0 else 0

    # Boundary analysis: 5px ring outside mask
    kernel = np.ones((5, 5), np.uint8)
    mask_dilated = cv2.dilate(mask_bin.astype(np.uint8), kernel, iterations=1)
    outer_ring = np.logical_and(mask_dilated, ~mask_bin)

    boundary_diff = 0
    boundary_changed = 0
    if outer_ring.sum() > 0:
        boundary_diff = float(diff_gray[outer_ring].mean())
        boundary_changed = int(np.count_nonzero(changed[outer_ring]))

    return {
        "total_pixels": int(total_pixels),
        "mask_pixels": mask_pixels,
        "outside_pixels": int(outside_pixels),
        "changed_pixels": int(changed.sum()),
        "changed_in_mask": changed_in_mask,
        "changed_outside_mask": changed_outside_mask,
        "mse": round(mse, 2),
        "rmse": round(rmse, 2),
        "total_change_pct": total_change_pct,
        "inside_change_pct": inside_change_pct,
        "outside_change_pct": outside_change_pct,
        "mean_diff_masked": round(mean_diff_masked, 2),
        "mean_diff_unmasked": round(mean_diff_unmasked, 2),
        "max_diff_masked": round(max_diff_masked, 2),
        "max_diff_unmasked": round(max_diff_unmasked, 2),
        "outer_ring_mean_diff": round(boundary_diff, 4),
        "outer_ring_changed_pct": round(boundary_changed / max(outer_ring.sum(), 1) * 100, 2),
    }


def create_comparison_figure(orig, raw_output, mask_bin, composite, fname, out_path):
    """Create a 4-panel comparison figure."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 4, figsize=(20, 5))

    axes[0].imshow(orig)
    axes[0].set_title("Original (Padded)")
    axes[0].axis("off")

    axes[1].imshow(raw_output)
    axes[1].set_title("Raw SDXL Output (No Composite)")
    axes[1].axis("off")

    mask_viz = np.zeros_like(orig)
    mask_resized = mask_bin.astype(np.uint8) * 255
    mask_viz[:, :, 0] = mask_resized * 0.6
    overlay = cv2.addWeighted(orig, 0.7, mask_viz, 0.3, 0)
    axes[2].imshow(overlay)
    axes[2].set_title("Mask Overlay")
    axes[2].axis("off")

    axes[3].imshow(composite)
    axes[3].set_title("Composite (Original + Inpaint)")
    axes[3].axis("off")

    fig.suptitle(fname, fontsize=14)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()


def process_image_experiment5(image_path, mask_path, seed, output_prefix):
    """Process a single image through the Experiment 5 pipeline.

    Returns results with metrics computed at 1024x1024 (where compositing is clean).
    """
    filename = os.path.basename(image_path)
    basename = os.path.splitext(filename)[0]

    result = {
        "filename": filename,
        "status": "unknown",
        "error": None,
        "processing_time": 0,
    }

    start_time = time.time()

    try:
        # Step 1: Load original and prepare at 1024x1024
        img_orig = Image.open(image_path).convert("RGB")
        print(f"  Original: {img_orig.size}")

        img_padded, offset, scale, orig_size = resize_to_square(img_orig, TARGET_SIZE)
        print(f"  Padded: {img_padded.size}, offset={offset}, scale={scale:.4f}")

        # Step 2: Save padded image and mask to ComfyUI input
        img_name = f"exp5_{basename}_img.png"
        img_padded.save(os.path.join(COMFYUI_INPUT, img_name))

        # Copy mask at 1024x1024
        mask_name = f"exp5_{basename}_mask.png"
        shutil.copy2(mask_path, os.path.join(COMFYUI_INPUT, mask_name))

        # Step 3: Run RAW workflow (no compositing) for comparison
        raw_prefix = f"exp5raw_{basename}"
        workflow_raw = get_raw_workflow(img_name, mask_name, seed)
        workflow_raw["9"]["inputs"]["filename_prefix"] = raw_prefix

        print(f"  Submitting RAW (no composite) workflow...")
        result_raw = submit_workflow(workflow_raw)
        if "error" in result_raw:
            result["status"] = "submit_error_raw"
            result["error"] = f"Raw: {result_raw['error']}"
            result["processing_time"] = time.time() - start_time
            return result

        prompt_id_raw = result_raw["prompt_id"]
        print(f"  Raw prompt ID: {prompt_id_raw}")

        completed_raw = wait_prompt_done(prompt_id_raw, timeout=600)
        if not completed_raw:
            result["status"] = "timeout_raw"
            result["error"] = "ComfyUI timed out on raw workflow"
            result["processing_time"] = time.time() - start_time
            return result

        success_raw, error_raw = check_success(prompt_id_raw)
        if not success_raw:
            result["status"] = "failed_raw"
            result["error"] = f"Raw: {error_raw}"
            result["processing_time"] = time.time() - start_time
            return result

        output_files_raw = sorted([f for f in os.listdir(COMFYUI_OUTPUT) if f.startswith(raw_prefix)])
        if not output_files_raw:
            result["status"] = "no_output_raw"
            result["error"] = "No raw output file found"
            result["processing_time"] = time.time() - start_time
            return result

        raw_output_path = os.path.join(COMFYUI_OUTPUT, output_files_raw[-1])
        raw_output_padded = Image.open(raw_output_path).convert("RGB")

        # Clean up raw output
        for f in output_files_raw:
            fpath = os.path.join(COMFYUI_OUTPUT, f)
            if os.path.exists(fpath):
                os.remove(fpath)

        # Step 4: Run COMPOSITING workflow (with ImageCompositeMasked)
        workflow_comp = get_compositing_workflow(img_name, mask_name, seed)
        workflow_comp["10"]["inputs"]["filename_prefix"] = output_prefix

        print(f"  Submitting COMPOSITING workflow...")
        result_comp = submit_workflow(workflow_comp)
        if "error" in result_comp:
            result["status"] = "submit_error_comp"
            result["error"] = f"Composite: {result_comp['error']}"
            result["processing_time"] = time.time() - start_time
            return result

        prompt_id_comp = result_comp["prompt_id"]
        print(f"  Composite prompt ID: {prompt_id_comp}")

        completed_comp = wait_prompt_done(prompt_id_comp, timeout=600)
        if not completed_comp:
            result["status"] = "timeout_comp"
            result["error"] = "ComfyUI timed out on composite workflow"
            result["processing_time"] = time.time() - start_time
            return result

        success_comp, error_comp = check_success(prompt_id_comp)
        if not success_comp:
            result["status"] = "failed_comp"
            result["error"] = f"Composite: {error_comp}"
            result["processing_time"] = time.time() - start_time
            return result

        output_files_comp = sorted([f for f in os.listdir(COMFYUI_OUTPUT) if f.startswith(output_prefix)])
        if not output_files_comp:
            result["status"] = "no_output_comp"
            result["error"] = "No composite output file found"
            result["processing_time"] = time.time() - start_time
            return result

        comp_output_path = os.path.join(COMFYUI_OUTPUT, output_files_comp[-1])
        composite_padded = Image.open(comp_output_path).convert("RGB")
        print(f"  Composite output: {output_files_comp[-1]}, size={composite_padded.size}")

        # Step 5: Load mask at 1024x1024
        mask_arr = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        mask_bin_1024 = mask_arr > 127

        # Convert PIL images to numpy arrays at 1024x1024
        orig_padded_arr = np.array(img_padded, dtype=np.uint8)
        raw_padded_arr = np.array(raw_output_padded, dtype=np.uint8)
        composite_padded_arr = np.array(composite_padded, dtype=np.uint8)

        # Step 6: Compute metrics at 1024x1024 (where compositing is clean)
        # Raw output vs original (to measure VAE corruption)
        stats_raw = compute_change_stats(orig_padded_arr, raw_padded_arr, mask_bin_1024)
        # Note: stats_raw uses the original padded image as reference

        # Composite vs original (to measure preservation + inpainting)
        stats_composite = compute_change_stats(orig_padded_arr, composite_padded_arr, mask_bin_1024)

        # Step 7: Compute 512x768 metrics using pixel-exact crop (no interpolation)
        # For the 512x768 comparison, we need to:
        # - Crop the composite to the inner region (undo padding)
        # - Use a nearest-neighbor resize to avoid interpolation artifacts
        composite_cropped = undo_padding(composite_padded, offset, scale, orig_size)
        composite_cropped_arr = np.array(composite_cropped, dtype=np.uint8)

        # Resize mask to 512x768 for 512x768 metrics
        mask_512 = cv2.resize(mask_bin_1024.astype(np.uint8) * 255, (orig_size[0], orig_size[1]))
        mask_bin_512 = mask_512 > 127

        orig_arr_512 = np.array(img_orig, dtype=np.uint8)
        stats_composite_512 = compute_change_stats(orig_arr_512, composite_cropped_arr, mask_bin_512)

        # Step 8: Also get existing pipeline output for comparison
        existing_output_path = os.path.join(EXISTING_OUTPUT_DIR, filename.replace(".png", "_inpaint.png"))
        stats_existing = None
        if os.path.exists(existing_output_path):
            existing_arr = np.array(Image.open(existing_output_path).convert("RGB"), dtype=np.uint8)
            stats_existing = compute_change_stats(orig_arr_512, existing_arr, mask_bin_512)

        # Step 9: Save artifacts
        composite_padded.save(os.path.join(QA_DIR, f"exp5_{output_prefix}_padded.png"))
        composite_cropped.save(os.path.join(QA_DIR, f"exp5_{output_prefix}_origsize.png"))
        raw_output_padded.save(os.path.join(QA_DIR, f"exp5_{output_prefix}_raw_padded.png"))
        Image.fromarray(raw_padded_arr).save(os.path.join(QA_DIR, f"exp5_{output_prefix}_raw.png"))

        # Save comparison figure (at 1024x1024 for consistency)
        create_comparison_figure(
            orig_padded_arr, raw_padded_arr, mask_bin_1024, composite_padded_arr,
            filename, os.path.join(QA_DIR, f"comp_{output_prefix}.png")
        )

        # Clean up ComfyUI input files
        for f in [img_name, mask_name]:
            fpath = os.path.join(COMFYUI_INPUT, f)
            if os.path.exists(fpath):
                os.remove(fpath)
        # Clean up composite output
        for f in output_files_comp:
            fpath = os.path.join(COMFYUI_OUTPUT, f)
            if os.path.exists(fpath):
                os.remove(fpath)

        result["status"] = "success"
        result["stats_composite_1024"] = stats_composite
        result["stats_raw_1024"] = stats_raw
        result["stats_composite_512"] = stats_composite_512
        result["stats_existing"] = stats_existing
        result["processing_time"] = time.time() - start_time

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        result["processing_time"] = time.time() - start_time

    return result


def main():
    print("=" * 70)
    print("EXPERIMENT 5: Hard Composite Pipeline (End-to-End)")
    print("Pipeline: SDXL Inpaint -> ImageCompositeMasked -> Crop")
    print(f"Checkpoint: {CHECKPOINT}")
    print(f"Settings: steps={STEPS}, cfg={CFG}, denoise={DENOISE}, grow_mask_by={GROW_MASK_BY}")
    print("=" * 70)

    results = []

    for i, tc in enumerate(TEST_CASES):
        fname = tc["name"]
        basename = os.path.splitext(fname)[0]
        print(f"\n[{i+1}/{len(TEST_CASES)}] {fname} ({tc['type']})")
        print(f"  Notes: {tc['notes']}")

        orig_path = os.path.join(ORIGINAL_ROOT, fname)
        mask_path = os.path.join(EXISTING_MASK_DIR, fname.replace(".png", "_inpaint_mask.png"))

        if not os.path.exists(orig_path):
            print(f"  ERROR: Original not found: {orig_path}")
            results.append({"filename": fname, "status": "missing_original", "type": tc["type"]})
            continue

        if not os.path.exists(mask_path):
            print(f"  ERROR: Mask not found: {mask_path}")
            results.append({"filename": fname, "status": "missing_mask", "type": tc["type"]})
            continue

        seed = hash(basename + "_exp5") % (2**31)

        result = process_image_experiment5(orig_path, mask_path, seed, f"exp5_{basename}")
        result["type"] = tc["type"]
        result["notes"] = tc["notes"]
        results.append(result)

        if result["status"] == "success":
            sc = result["stats_composite_1024"]
            print(f"  Status: success")
            print(f"  [1024x1024] Composite vs Original:")
            print(f"    Outside-mask change: {sc['outside_change_pct']}%")
            print(f"    Mean diff (unmasked): {sc['mean_diff_unmasked']}")
            print(f"    Outer ring mean diff: {sc['outer_ring_mean_diff']}")
            print(f"    MSE: {sc['mse']}")
            print(f"  [512x768] Composite vs Original:")
            s512 = result["stats_composite_512"]
            print(f"    Outside-mask change: {s512['outside_change_pct']}%")
            print(f"    Mean diff (unmasked): {s512['mean_diff_unmasked']}")
            sr = result["stats_raw_1024"]
            print(f"  [1024x1024] Raw output (no composite) vs Original:")
            print(f"    Outside-mask change: {sr['outside_change_pct']}%")
            print(f"    MSE: {sr['mse']}")
            if result.get("stats_existing"):
                se = result["stats_existing"]
                print(f"  [Existing pipeline output] vs Original:")
                print(f"    Outside-mask change: {se['outside_change_pct']}%")
                print(f"    MSE: {se['mse']}")
        else:
            print(f"  Status: {result['status']}")
            if result.get("error"):
                print(f"  Error: {result['error']}")

    # Save results
    log_path = os.path.join(QA_LOGS_DIR, "experiment5_results.json")
    with open(log_path, "w") as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n{'='*70}")
    print("EXPERIMENT 5 SUMMARY (1024x1024 metrics - where compositing is clean)")
    print("=" * 70)

    print(f"\n{'Filename':<35} {'Type':<20} {'OutMask%':>10} {'MAD(unmask)':>12} {'OuterRing':>10} {'MSE':>8}")
    print("-" * 100)
    for r in results:
        if r.get("stats_composite_1024"):
            s = r["stats_composite_1024"]
            print(f"{r['filename'][:35]:<35} {r['type']:<20} {s['outside_change_pct']:>10.2f} {s['mean_diff_unmasked']:>12.2f} {s['outer_ring_mean_diff']:>10.4f} {s['mse']:>8.2f}")
        else:
            print(f"{r['filename'][:35]:<35} {r.get('type','?'):<20} {r['status']:>10}")

    print(f"\n{'='*70}")
    print("COMPARISON: Raw SDXL output vs Composite (1024x1024)")
    print("=" * 70)
    print(f"\n{'Filename':<35} {'Raw OutMask%':>14} {'Comp OutMask%':>14} {'Raw MSE':>10} {'Comp MSE':>10}")
    print("-" * 90)
    for r in results:
        if r.get("stats_composite_1024") and r.get("stats_raw_1024"):
            sr = r["stats_raw_1024"]
            sc = r["stats_composite_1024"]
            print(f"{r['filename'][:35]:<35} {sr['outside_change_pct']:>14.2f} {sc['outside_change_pct']:>14.2f} {sr['mse']:>10.2f} {sc['mse']:>10.2f}")
        else:
            print(f"{r['filename'][:35]:<35} N/A")

    print(f"\n{'='*70}")
    print("512x768 metrics (after undo_padding with LANCZOS resize)")
    print("=" * 70)
    print(f"\n{'Filename':<35} {'Type':<20} {'OutMask%':>10} {'MAD(unmask)':>12} {'MSE':>8}")
    print("-" * 90)
    for r in results:
        if r.get("stats_composite_512"):
            s = r["stats_composite_512"]
            print(f"{r['filename'][:35]:<35} {r['type']:<20} {s['outside_change_pct']:>10.2f} {s['mean_diff_unmasked']:>12.2f} {s['mse']:>8.2f}")
        else:
            print(f"{r['filename'][:35]:<35} {r.get('type','?'):<20} {r.get('status','?'):>10}")

    print(f"\nResults saved to: {log_path}")
    print(f"QA artifacts in: {QA_DIR}")

    # Preservation gate check (at 1024x1024 where compositing is clean)
    print(f"\n{'='*70}")
    print("PRESERVATION GATE CHECK (1024x1024 - compositing space)")
    print("=" * 70)
    all_pass = True
    for r in results:
        if r.get("stats_composite_1024"):
            s = r["stats_composite_1024"]
            outside_ok = s["outside_change_pct"] < 0.5
            mean_diff_ok = s["mean_diff_unmasked"] < 1.0
            boundary_ok = s["outer_ring_mean_diff"] < 0.5
            if not (outside_ok and mean_diff_ok and boundary_ok):
                all_pass = False
            print(f"  {r['filename']}: out={s['outside_change_pct']}%, "
                  f"mad={s['mean_diff_unmasked']}, ring={s['outer_ring_mean_diff']} "
                  f"{'PASS' if (outside_ok and mean_diff_ok and boundary_ok) else 'FAIL'}")

    print(f"\nPreservation gate: {'ALL PASS' if all_pass else 'SOME FAIL'}")
    print(f"Experiment 5 verdict: {'PASS' if all_pass else 'FAIL/INCONCLUSIVE'}")


if __name__ == "__main__":
    main()
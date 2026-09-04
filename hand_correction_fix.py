#!/usr/bin/env python
"""
Hand Correction Pipeline — Diagnostic & Controlled Fix Experiment

Generates 6-panel diagnostic artifacts for the 8 test images, then runs
a FIXED pipeline with conservative parameters to test the hypotheses:

ROOT CAUSE 1: Excessive mask expansion
  - padding: 0.5 -> 0.10  (less bbox growth)
  - morph_dilate: 15 -> 3  (smaller dilation kernel)
  - blur_radius: 10 -> 3   (tight feathering)
  - grow_mask_by: 8 -> 0   (no extra expansion in ComfyUI)

ROOT CAUSE 2: High denoise strength
  - denoise: 0.5 -> 0.3  (conservative inpainting, preserves context)

ROOT CAUSE 3: resize_source=True introduces interpolation artifacts
  - resize_source: True -> False  (dimensions already match 512x768)

NO changes to: detector, model, prompt, sampler.
Original assets are NEVER modified.
"""
import os
import sys
import json
import time
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

import urllib.request
import urllib.error

# ============================================================
# Config — FIXED parameters
# ============================================================
COMFYUI_DIR = r"D:\Jake\ComfyUI_windows_portable\ComfyUI"
COMFYUI_INPUT = os.path.join(COMFYUI_DIR, "input")
COMFYUI_OUTPUT = os.path.join(COMFYUI_DIR, "output")
COMFYUI_PYTHON = r"D:\Jake\ComfyUI_windows_portable\python_embeded\python.exe"
API_URL = "http://127.0.0.1:8188"

CHECKPOINT = "dreamshaperXL_sfwLightningDPMSDE.safetensors"
HAND_MODEL = os.path.join(COMFYUI_DIR, "models", "detection", "hand_landmarker.task")

ORIGINAL_ROOT = r"D:\the-exile-king\art\prototype\commander-cards"
CORRECTED_ROOT = r"D:\the-exile-king\art\corrected\corrected"

# FIXED OUTPUT locations (keep original test results intact)
FIX_OUTPUT_DIR = r"D:\the-exile-king\art\corrected\fixed"
FIX_MASKS_DIR = r"D:\the-exile-king\art\corrected\fixed_masks"
FIX_DIAGNOSTICS_DIR = r"D:\the-exile-king\art\corrected\diagnostics"
FIX_LOGS_DIR = r"D:\the-exile-king\art\corrected\logs"

FIXED_POSITIVE_PROMPT = (
    "anatomically correct hand, five fingers, correct proportions, "
    "properly formed weapon, consistent object geometry, "
    "hand-painted historical illustration, watercolor and ink, "
    "board game card art, family friendly, consistent art style"
)
FIXED_NEGATIVE_PROMPT = (
    "extra fingers, fused fingers, malformed hand, duplicate weapon, "
    "warped blade, extra limbs, deformed, blurry, low quality, "
    "worst quality, bad anatomy, extra arms, mutation, disfigured"
)

# FIXED pipeline settings
FIXED_STEPS = 8
FIXED_CFG = 5.0
FIXED_DENOISE = 0.3       # Reduced from 0.5
FIXED_GROW_MASK_BY = 0    # Removed: was 8
FIXED_MASK_PADDING = 0.10  # Reduced from 0.5
FIXED_MORPH_DILATE = 3    # Reduced from 15
FIXED_BLUR_RADIUS = 3     # Reduced from 10
FIXED_RESIZE_SOURCE = False  # Changed from True

SAMPLER_NAME = "dpmpp_sde"
SCHEDULER = "karras"

TEST_FILES = [
    "achish-01_00001_.png",
    "achish-01_00002_.png",
    "achish-02_00001_.png",
    "achish-02_00002_.png",
    "achish-02_00003_.png",
    "achish-03_00002_.png",
    "achish-03_00003_.png",
    "achish-04_00003_.png",
]


# ============================================================
# Hand Detection
# ============================================================
class HandDetector:
    def __init__(self, model_path=HAND_MODEL, num_hands=4, min_confidence=0.3):
        self.base_options = mp_python.BaseOptions(
            model_asset_path=model_path,
            delegate=mp_python.BaseOptions.Delegate.CPU,
        )
        self.options = vision.HandLandmarkerOptions(
            base_options=self.base_options,
            running_mode=vision.RunningMode.IMAGE,
            num_hands=num_hands,
            min_hand_detection_confidence=min_confidence,
            min_hand_presence_confidence=0.3,
            min_tracking_confidence=0.3,
        )
        self.detector = vision.HandLandmarker.create_from_options(self.options)

    def detect(self, image_path):
        img = Image.open(image_path).convert('RGB')
        W, H = img.size
        img_np = np.array(img)
        mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_np)
        result = self.detector.detect(mp_img)
        bboxes = []
        if result.hand_landmarks:
            for i, landmarks in enumerate(result.hand_landmarks):
                xs = [lm.x for lm in landmarks]
                ys = [lm.y for lm in landmarks]
                handedness = 'unknown'
                score = 0.5
                if i < len(result.handedness):
                    handedness = result.handedness[i][0].category_name
                    score = result.handedness[i][0].score
                bboxes.append({
                    'x1': min(xs), 'x2': max(xs),
                    'y1': min(ys), 'y2': max(ys),
                    'score': float(score),
                    'label': handedness,
                })
        return bboxes, W, H, img

    def close(self):
        self.detector.close()


def create_mask_fixed(bboxes, W, H, padding=0.10, morph_dilate=3, blur_radius=3):
    mask = np.zeros((H, W), dtype=np.float32)
    for bbox in bboxes:
        x1 = int(bbox['x1'] * W)
        x2 = int(bbox['x2'] * W)
        y1 = int(bbox['y1'] * H)
        y2 = int(bbox['y2'] * H)

        bw = max(1, x2 - x1)
        bh = max(1, y2 - y1)
        expand_x = int(bw * padding)
        expand_y = int(bh * padding)

        x1 = max(0, x1 - expand_x)
        x2 = min(W, x2 + expand_x)
        y1 = max(0, y1 - expand_y)
        y2 = min(H, y2 + expand_y)

        mask[y1:y2, x1:x2] = 1.0

    mask_pil = Image.fromarray((mask * 255).astype(np.uint8), mode='L')
    if morph_dilate > 0:
        mask_pil = mask_pil.filter(ImageFilter.MaxFilter(morph_dilate))
    if blur_radius > 0:
        mask_pil = mask_pil.filter(ImageFilter.GaussianBlur(blur_radius))

    arr = np.array(mask_pil, dtype=np.float32) / 255.0
    return arr


def create_mask_original(bboxes, W, H, padding=0.5, morph_dilate=15, blur_radius=10):
    """Same as original pipeline for diagnostic comparison."""
    mask = np.zeros((H, W), dtype=np.float32)
    for bbox in bboxes:
        x1 = int(bbox['x1'] * W)
        x2 = int(bbox['x2'] * W)
        y1 = int(bbox['y1'] * H)
        y2 = int(bbox['y2'] * H)
        bw = max(1, x2 - x1)
        bh = max(1, y2 - y1)
        expand_x = int(bw * padding)
        expand_y = int(bh * padding)
        x1 = max(0, x1 - expand_x)
        x2 = min(W, x2 + expand_x)
        y1 = max(0, y1 - expand_y)
        y2 = min(H, y2 + expand_y)
        mask[y1:y2, x1:x2] = 1.0
    mask_pil = Image.fromarray((mask * 255).astype(np.uint8), mode='L')
    if morph_dilate > 0:
        mask_pil = mask_pil.filter(ImageFilter.MaxFilter(morph_dilate))
    if blur_radius > 0:
        mask_pil = mask_pil.filter(ImageFilter.GaussianBlur(blur_radius))
    arr = np.array(mask_pil, dtype=np.float32) / 255.0
    return arr


def draw_bboxes(img, bboxes, W, H):
    overlay = img.convert('RGBA')
    draw = ImageDraw.Draw(overlay)
    for info in bboxes:
        x1 = int(info['x1'] * W)
        x2 = int(info['x2'] * W)
        y1 = int(info['y1'] * H)
        y2 = int(info['y2'] * H)
        draw.rectangle([x1, y1, x2, y2], outline=(255, 0, 0, 255), width=2)
        draw.text((x1, y1), f"{info['label']} {info['score']:.2f}", fill=(255, 0, 0, 255))
    return overlay.convert('RGB')


def save_mask_overlay(mask, original_img, output_path, bboxes=None):
    W, H = original_img.size
    mask_pil = Image.fromarray((mask * 255).astype(np.uint8), mode='L').resize((W, H))
    overlay = original_img.convert('RGBA')
    colored_mask = Image.new('RGBA', (W, H), (255, 0, 0, 0))
    mask_np = np.array(mask_pil)
    alpha = np.clip(mask_np.astype(np.float32) * 2, 0, 255).astype(np.uint8)
    mask_alpha = Image.fromarray(alpha)
    colored_mask.putalpha(mask_alpha)
    overlay = Image.alpha_composite(overlay, colored_mask).convert('RGB')

    draw = ImageDraw.Draw(overlay)
    if bboxes:
        for info in bboxes:
            x1 = int(info['x1'] * W)
            x2 = int(info['x2'] * W)
            y1 = int(info['y1'] * H)
            y2 = int(info['y2'] * H)
            draw.rectangle([x1, y1, x2, y2], outline=(0, 255, 0), width=2)

    overlay.save(output_path)


def build_fixed_workflow(img_filename, mask_filename, seed):
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": CHECKPOINT}},
        "2": {"class_type": "LoadImage", "inputs": {"image": img_filename}},
        "3": {"class_type": "LoadImageMask", "inputs": {"image": mask_filename, "channel": "red"}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {"text": FIXED_POSITIVE_PROMPT, "clip": ["1", 1]}},
        "5": {"class_type": "CLIPTextEncode", "inputs": {"text": FIXED_NEGATIVE_PROMPT, "clip": ["1", 1]}},
        "6": {"class_type": "VAEEncodeForInpaint",
              "inputs": {"pixels": ["2", 0], "vae": ["1", 2], "mask": ["3", 0], "grow_mask_by": FIXED_GROW_MASK_BY}},
        "7": {"class_type": "KSampler",
              "inputs": {"model": ["1", 0], "seed": seed, "steps": FIXED_STEPS, "cfg": FIXED_CFG,
                         "sampler_name": SAMPLER_NAME, "scheduler": SCHEDULER,
                         "positive": ["4", 0], "negative": ["5", 0],
                         "latent_image": ["6", 0], "denoise": FIXED_DENOISE}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["7", 0], "vae": ["1", 2]}},
        "9": {"class_type": "ImageCompositeMasked",
              "inputs": {"destination": ["2", 0], "source": ["8", 0], "x": 0, "y": 0,
                         "resize_source": FIXED_RESIZE_SOURCE, "mask": ["3", 0]}},
        "10": {"class_type": "SaveImage", "inputs": {"images": ["9", 0], "filename_prefix": ""}},
    }


def submit_workflow(workflow):
    payload = {"prompt": workflow}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(f"{API_URL}/prompt", data=data,
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=300) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        if "error" in result:
            raise RuntimeError(f"ComfyUI API error: {result['error']}")
        return result.get("prompt_id")


def wait_for_prompt(prompt_id, timeout=600):
    start = time.time()
    was_running = False
    while time.time() - start < timeout:
        try:
            req = urllib.request.Request(f"{API_URL}/queue", method="GET")
            with urllib.request.urlopen(req, timeout=10) as resp:
                queue = json.loads(resp.read().decode("utf-8"))
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
        except Exception:
            pass
        time.sleep(2)
    return False


def check_prompt_success(prompt_id):
    try:
        req = urllib.request.Request(f"{API_URL}/history?prompt_id={prompt_id}", method="GET")
        with urllib.request.urlopen(req, timeout=10) as resp:
            history = json.loads(resp.read().decode("utf-8"))
        if prompt_id in history:
            entry = history[prompt_id]
            status = entry.get("status", {})
            if status.get("completed", False):
                errors = status.get("errors", [])
                if errors:
                    return False, str(errors)
                return True, None
            return False, "Not completed"
        return False, "No history entry"
    except Exception as e:
        return False, str(e)


def move_output(prefix, dest_path):
    files = sorted([f for f in os.listdir(COMFYUI_OUTPUT) if f.startswith(prefix)])
    if not files:
        return None
    src = os.path.join(COMFYUI_OUTPUT, files[-1])
    shutil.move(src, dest_path)
    return dest_path


def generate_diagnostics(filename, detector, bboxes, W, H, img):
    """Generate the 6-panel diagnostic for a single image."""
    orig_path = os.path.join(ORIGINAL_ROOT, filename)
    corr_path = os.path.join(CORRECTED_ROOT, filename)

    orig = Image.open(orig_path).convert('RGB')
    corr = Image.open(corr_path).convert('RGB')

    # A. Original
    panel_orig = orig

    # B. Raw MediaPipe hand bounding box
    panel_bbox = draw_bboxes(orig, bboxes, W, H)

    # C. Final mask (original pipeline, large expansion)
    mask_orig = create_mask_original(bboxes, W, H, padding=0.5, morph_dilate=15, blur_radius=10)
    mask_pil_orig = Image.fromarray((mask_orig * 255).astype(np.uint8), mode='L')

    # D. Inpaint output (corrected image, masked only)
    # We approximate by showing the corrected image with non-mask areas grayed out
    corr_arr = np.array(corr).astype(np.float32)
    gray = np.zeros_like(corr_arr)
    gray[:, :, 0] = 128
    gray[:, :, 1] = 128
    gray[:, :, 2] = 128
    panel_inpaint = Image.fromarray(
        (corr_arr * mask_orig[:, :, None] + gray * (1 - mask_orig[:, :, None])).astype(np.uint8),
        mode='RGB'
    )

    # E. Final composited image
    panel_composite = corr

    # F. Difference image
    orig_arr = np.array(orig).astype(np.float32)
    diff = np.abs(corr_arr - orig_arr)
    diff_enhanced = np.clip(diff * 5, 0, 255).astype(np.uint8)
    panel_diff = Image.fromarray(diff_enhanced, mode='RGB')

    # Combine into 3x2 grid
    thumb = 256
    panel_orig_thumb = panel_orig.resize((thumb, thumb), Image.Resampling.LANCZOS)
    panel_bbox_thumb = panel_bbox.resize((thumb, thumb), Image.Resampling.LANCZOS)
    panel_inpaint_thumb = panel_inpaint.resize((thumb, thumb), Image.Resampling.LANCZOS)
    panel_composite_thumb = panel_composite.resize((thumb, thumb), Image.Resampling.LANCZOS)
    panel_diff_thumb = panel_diff.resize((thumb, thumb), Image.Resampling.LANCZOS)

    # Save individual mask
    mask_pil_orig.save(os.path.join(FIX_DIAGNOSTICS_DIR, f"diag_mask_{filename}"))

    # Create 3x2 contact sheet
    margin = 10
    label_h = 20
    sheet_w = 3 * thumb + 4 * margin
    sheet_h = 2 * thumb + 3 * margin + label_h
    sheet = Image.new('RGB', (sheet_w, sheet_h), (240, 240, 240))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 12)
    except:
        font = ImageFont.load_default()

    labels = ["A. Original", "B. BBox (green=raw)", "C. Mask (orig pipeline)",
              "D. Inpaint region", "E. Composited", "F. Diff (x5)"]
    panels = [panel_orig_thumb, panel_bbox_thumb, mask_pil_orig.resize((thumb, thumb)),
              panel_inpaint_thumb, panel_composite_thumb, panel_diff_thumb]

    for idx, (panel, label) in enumerate(zip(panels, labels)):
        col = idx % 3
        row = idx // 3
        x = col * (thumb + margin) + margin
        y = row * (thumb + margin) + margin + label_h
        sheet.paste(panel, (x, y))
        draw.text((x, y - 15), label, fill=(50, 50, 50), font=font)

    draw.text((margin, 3), f"DIAGNOSTIC: {filename}\nOriginal pipeline mask params",
              fill=(0, 0, 0), font=font)

    sheet.save(os.path.join(FIX_DIAGNOSTICS_DIR, f"diag_{filename}"))


def generate_fixed_diagnostics(filename, detector, bboxes, W, H, img, fixed_mask):
    """Generate diagnostic showing the FIXED mask vs original mask."""
    mask_pil_fixed = Image.fromarray((fixed_mask * 255).astype(np.uint8), mode='L')

    # Compare masks side by side
    thumb = 256
    mask_orig = create_mask_original(bboxes, W, H, padding=0.5, morph_dilate=15, blur_radius=10)

    orig_arr = (mask_orig * 255).astype(np.uint8)
    fixed_arr = (fixed_mask * 255).astype(np.uint8)

    panel_orig_mask = Image.fromarray(orig_arr, mode='L').resize((thumb, thumb), Image.Resampling.LANCZOS)
    panel_fixed_mask = Image.fromarray(fixed_arr, mode='L').resize((thumb, thumb), Image.Resampling.LANCZOS)

    # Overlay comparison on original
    orig_img = Image.open(os.path.join(ORIGINAL_ROOT, filename)).convert('RGB')

    def mask_to_overlay(mask_arr, base_img):
        overlay = base_img.convert('RGBA')
        colored = Image.new('RGBA', base_img.size, (255, 0, 0, 0))
        alpha = np.clip(mask_arr * 2, 0, 255).astype(np.uint8)
        colored.putalpha(Image.fromarray(alpha))
        return Image.alpha_composite(overlay, colored).convert('RGB')

    panel_orig_overlay = mask_to_overlay(mask_orig, orig_img).resize((thumb, thumb), Image.Resampling.LANCZOS)
    panel_fixed_overlay = mask_to_overlay(fixed_mask, orig_img).resize((thumb, thumb), Image.Resampling.LANCZOS)

    margin = 10
    label_h = 20
    sheet_w = 2 * thumb + 3 * margin
    sheet_h = 2 * thumb + 3 * margin + label_h
    sheet = Image.new('RGB', (sheet_w, sheet_h), (240, 240, 240))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 12)
    except:
        font = ImageFont.load_default()

    labels = ["Original mask overlay", "Fixed mask overlay"]
    panels = [panel_orig_overlay, panel_fixed_overlay]

    for idx, (panel, label) in enumerate(zip(panels, labels)):
        x = idx * (thumb + margin) + margin
        y = margin + label_h
        sheet.paste(panel, (x, y))
        draw.text((x, y - 15), label, fill=(50, 50, 50), font=font)

    draw.text((margin, 3), f"MASK COMPARISON: {filename}\nRed = original mask (larger) | Red = fixed mask (smaller)",
              fill=(0, 0, 0), font=font)

    sheet.save(os.path.join(FIX_DIAGNOSTICS_DIR, f"mask_compare_{filename}"))


def main():
    os.makedirs(FIX_OUTPUT_DIR, exist_ok=True)
    os.makedirs(FIX_MASKS_DIR, exist_ok=True)
    os.makedirs(FIX_DIAGNOSTICS_DIR, exist_ok=True)

    detector = HandDetector()

    fix_results = []

    for i, filename in enumerate(TEST_FILES):
        print(f"[{i+1}/{len(TEST_FILES)}] {filename}")
        orig_path = os.path.join(ORIGINAL_ROOT, filename)
        basename = os.path.splitext(filename)[0]

        # Detect hands
        bboxes, W, H, img = detector.detect(orig_path)
        print(f"  Hands detected: {len(bboxes)}")

        # Generate diagnostics for ORIGINAL pipeline
        print(f"  Generating diagnostics...")
        generate_diagnostics(filename, detector, bboxes, W, H, img)

        # Create masks
        mask_fixed = create_mask_fixed(bboxes, W, H,
                                        padding=FIXED_MASK_PADDING,
                                        morph_dilate=FIXED_MORPH_DILATE,
                                        blur_radius=FIXED_BLUR_RADIUS)

        mask_orig = create_mask_original(bboxes, W, H, padding=0.5, morph_dilate=15, blur_radius=10)

        # Mask stats
        orig_pct = (mask_orig > 0.5).sum() / (H * W) * 100
        fixed_pct = (mask_fixed > 0.5).sum() / (H * W) * 100
        print(f"  Mask area: original={orig_pct:.1f}%  fixed={fixed_pct:.1f}%  reduction={orig_pct-fixed_pct:.1f}pp")

        # Generate mask comparison diagnostics
        generate_fixed_diagnostics(filename, detector, bboxes, W, H, img, mask_fixed)

        # Save fixed mask
        mask_pil = Image.fromarray((mask_fixed * 255).astype(np.uint8), mode='L')
        mask_pil.save(os.path.join(FIX_MASKS_DIR, f"mask_{filename}"))

        # Save image + mask to ComfyUI input
        img_input_name = f"fix_{basename}.png"
        mask_input_name = f"fix_msk_{basename}.png"
        img.save(os.path.join(COMFYUI_INPUT, img_input_name))
        mask_pil.save(os.path.join(COMFYUI_INPUT, mask_input_name))

        # Submit workflow
        seed = hash(basename + "_fix") % (2**31)
        workflow = build_fixed_workflow(img_input_name, mask_input_name, seed)
        workflow["10"]["inputs"]["filename_prefix"] = f"fix_{basename}"

        print(f"  Submitting to ComfyUI (denoise={FIXED_DENOISE}, resize_source={FIXED_RESIZE_SOURCE})...")
        prompt_id = submit_workflow(workflow)

        completed = wait_for_prompt(prompt_id, timeout=600)
        if not completed:
            print(f"  TIMEOUT")
            fix_results.append({"filename": filename, "status": "timeout"})
            continue

        success, error = check_prompt_success(prompt_id)
        if not success:
            print(f"  ERROR: {error}")
            fix_results.append({"filename": filename, "status": "error", "error": error})
            continue

        # Move output
        dest = os.path.join(FIX_OUTPUT_DIR, filename)
        output_file = move_output(f"fix_{basename}", dest)
        if not output_file:
            print(f"  ERROR: No output")
            fix_results.append({"filename": filename, "status": "no_output"})
            continue

        # Pixel change analysis
        corrected = np.array(Image.open(dest).convert('RGB'))
        orig_arr = np.array(img.convert('RGB'))
        if corrected.shape == orig_arr.shape:
            diff = np.abs(corrected.astype(float) - orig_arr.astype(float))
            mask_changes = (diff[:, :, 0] > 10) * (mask_fixed > 0.5)
            outside_changes = (diff[:, :, 0] > 10) * (mask_fixed <= 0.5)
            pixel_change_pct = (diff > 10).mean(axis=2).mean() * 100
            mask_change_pct = mask_changes.mean() * 100
            outside_change_pct = outside_changes.mean() * 100
            print(f"  Done. Total change={pixel_change_pct:.1f}%, in-mask={mask_change_pct:.1f}%, outside-mask={outside_change_pct:.1f}%")
        else:
            print(f"  WARNING: Size mismatch {corrected.shape} vs {orig_arr.shape}")
            outside_change_pct = 0
            pixel_change_pct = 0

        # Clean up ComfyUI input files
        for f in [img_input_name, mask_input_name]:
            fpath = os.path.join(COMFYUI_INPUT, f)
            if os.path.exists(fpath):
                os.remove(fpath)

        fix_results.append({
            "filename": filename,
            "status": "corrected",
            "mask_area_pct_orig": round(orig_pct, 2),
            "mask_area_pct_fixed": round(fixed_pct, 2),
            "pixel_change_pct": round(pixel_change_pct, 2),
            "in_mask_change_pct": round(mask_change_pct, 2),
            "outside_mask_change_pct": round(outside_change_pct, 2),
        })

    detector.close()

    # Save results
    results_path = os.path.join(FIX_LOGS_DIR, "fixed_test_results.json")
    with open(results_path, 'w') as f:
        json.dump(fix_results, f, indent=2)
    print(f"\nResults saved: {results_path}")
    print(f"Fixed images: {FIX_OUTPUT_DIR}")
    print(f"Diagnostics: {FIX_DIAGNOSTICS_DIR}")

    # Print summary
    print(f"\n=== FIXED PIPELINE SUMMARY ===")
    print(f"Mask expansion: padding {0.5}->{FIXED_MASK_PADDING}, dilate {15}->{FIXED_MORPH_DILATE}, blur {10}->{FIXED_BLUR_RADIUS}, grow {8}->{FIXED_GROW_MASK_BY}")
    print(f"Denoise: {0.5}->{FIXED_DENOISE}")
    print(f"resize_source: True->{FIXED_RESIZE_SOURCE}")
    print()
    for r in fix_results:
        if r['status'] == 'corrected':
            print(f"  {r['filename']}: change={r['pixel_change_pct']:.1f}%, "
                  f"in-mask={r['in_mask_change_pct']:.1f}%, outside={r['outside_mask_change_pct']:.1f}%")


if __name__ == "__main__":
    main()

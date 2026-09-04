"""
Exile King — Local Hand Correction Pipeline
============================================
Detects AI-generated hand errors in Exile King card art and corrects them
using ComfyUI's masked inpainting workflow.

Architecture:
  INPUT IMAGE -> MediaPipe Hands (CPU) -> Problem-region mask ->
  ComfyUI VAEEncodeForInpaint + KSampler(denoise) + VAEDecode +
  ImageCompositeMasked -> OUTPUT IMAGE (corrected region only)

The original image remains the source of truth. Only masked regions are
modified. The entire pipeline runs locally — no cloud APIs.

Usage:
  python exile_king_hand_correction.py --mode test
  python exile_king_hand_correction.py --mode full
  python exile_king_hand_correction.py --mode retry
  python exile_king_hand_correction.py --mode contact-sheet
"""
import os
import sys
import json
import time
import shutil
import hashlib
import argparse
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

# ============================================================
# Configuration
# ============================================================

COMFYUI_DIR = r"D:\Jake\ComfyUI_windows_portable\ComfyUI"
COMFYUI_INPUT = os.path.join(COMFYUI_DIR, "input")
COMFYUI_OUTPUT = os.path.join(COMFYUI_DIR, "output")
COMFYUI_PYTHON = r"D:\Jake\ComfyUI_windows_portable\python_embeded\python.exe"
API_URL = "http://127.0.0.1:8188"

CHECKPOINT = "dreamshaperXL_sfwLightningDPMSDE.safetensors"
HAND_MODEL = os.path.join(COMFYUI_DIR, "models", "detection", "hand_landmarker.task")

# Art source
DEFAULT_INPUT_DIR = r"D:\the-exile-king\art\prototype"

# Output locations
BASE_OUTPUT_DIR = r"D:\the-exile-king\art\corrected"
CORRECTED_DIR = os.path.join(BASE_OUTPUT_DIR, "corrected")
MASKS_DIR = os.path.join(BASE_OUTPUT_DIR, "masks")
CONTACT_SHEETS_DIR = os.path.join(BASE_OUTPUT_DIR, "contact_sheets")
LOGS_DIR = os.path.join(BASE_OUTPUT_DIR, "logs")

# Inpainting settings
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
MASK_PADDING = 0.5  # expand bbox by 50% of its size in each direction
MORPH_DILATE = 15   # morphological dilation kernel size
BLUR_RADIUS = 10    # gaussian blur for feathering


# ============================================================
# Hand Detection (CPU via MediaPipe)
# ============================================================

class HandDetector:
    """Wrapper around MediaPipe HandLandmarker for CPU-based hand detection."""

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
        """Detect hands in an image file.
        Returns (list_of_bboxes, width, height, PIL_image)
        Each bbox: {x1, x2, y1, y2, score, label} in normalized coords.
        """
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


def create_mask_from_bboxes(bboxes, W, H, padding=0.5, morph_dilate=15, blur_radius=10):
    """Create a binary mask from hand bounding boxes.
    Mask value 1.0 = region to inpaint, 0.0 = region to preserve.
    """
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


def save_mask_visualization(mask, original_img, output_path, bbox_info=None):
    """Save a visualization showing the mask overlaid on the original image."""
    W, H = original_img.size
    mask_pil = Image.fromarray((mask * 255).astype(np.uint8), mode='L').resize((W, H))

    # Create overlay: original in RGB, mask boundary in red
    overlay = original_img.convert('RGBA')
    colored_mask = Image.new('RGBA', (W, H), (255, 0, 0, 0))
    mask_alpha = Image.new('L', (W, H), 0)
    mask_np = np.array(mask_pil)
    # Red overlay where mask > 0.5, fading at edges
    alpha = np.clip(mask_np.astype(np.float32) * 2, 0, 255).astype(np.uint8)
    mask_alpha = Image.fromarray(alpha)
    colored_mask.putalpha(mask_alpha)
    overlay = Image.alpha_composite(overlay, colored_mask).convert('RGB')

    # Draw bounding boxes
    draw = ImageDraw.Draw(overlay)
    if bbox_info:
        for info in bbox_info:
            x1 = int(info['x1'] * W)
            x2 = int(info['x2'] * W)
            y1 = int(info['y1'] * H)
            y2 = int(info['y2'] * H)
            draw.rectangle([x1, y1, x2, y2], outline=(255, 0, 0), width=2)
            draw.text((x1, y1), f"{info['label']} {info['score']:.2f}", fill=(255, 0, 0))

    overlay.save(output_path)


# ============================================================
# ComfyUI API Integration
# ============================================================

def submit_workflow(workflow):
    """Submit a ComfyUI workflow via API. Returns prompt_id."""
    payload = {"prompt": workflow}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{API_URL}/prompt",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        if "error" in result:
            raise RuntimeError(f"ComfyUI API error: {result['error']}")
        return result.get("prompt_id")


def wait_for_prompt(prompt_id, timeout=600):
    """Wait for a ComfyUI prompt to complete. Returns True if completed."""
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


def get_history(prompt_id):
    """Get execution history for a prompt from ComfyUI."""
    req = urllib.request.Request(f"{API_URL}/history?prompt_id={prompt_id}", method="GET")
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def check_prompt_success(prompt_id):
    """Check if a prompt completed successfully. Returns (success, error_msg)."""
    try:
        history = get_history(prompt_id)
        if prompt_id in history:
            entry = history[prompt_id]
            status = entry.get("status", {})
            if status.get("completed", False):
                errors = status.get("errors", [])
                if errors:
                    return False, str(errors)
                return True, None
            else:
                return False, "Not completed"
        return False, "No history entry"
    except Exception as e:
        return False, str(e)


def move_output(prefix, dest_path):
    """Find and move the output file from ComfyUI output dir."""
    files = sorted([f for f in os.listdir(COMFYUI_OUTPUT) if f.startswith(prefix)])
    if not files:
        return None
    src = os.path.join(COMFYUI_OUTPUT, files[-1])
    shutil.move(src, dest_path)
    return dest_path


def build_inpainting_workflow(img_filename, mask_filename, seed, steps, cfg, denoise):
    """Build the ComfyUI workflow JSON for hand correction inpainting."""
    return {
        "1": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": CHECKPOINT}
        },
        "2": {
            "class_type": "LoadImage",
            "inputs": {"image": img_filename}
        },
        "3": {
            "class_type": "LoadImageMask",
            "inputs": {"image": mask_filename, "channel": "red"}
        },
        "4": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": POSITIVE_PROMPT, "clip": ["1", 1]}
        },
        "5": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": NEGATIVE_PROMPT, "clip": ["1", 1]}
        },
        "6": {
            "class_type": "VAEEncodeForInpaint",
            "inputs": {
                "pixels": ["2", 0],
                "vae": ["1", 2],
                "mask": ["3", 0],
                "grow_mask_by": GROW_MASK_BY
            }
        },
        "7": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["1", 0],
                "seed": seed,
                "steps": steps,
                "cfg": cfg,
                "sampler_name": SAMPLER_NAME,
                "scheduler": SCHEDULER,
                "positive": ["4", 0],
                "negative": ["5", 0],
                "latent_image": ["6", 0],
                "denoise": denoise
            }
        },
        "8": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": ["7", 0],
                "vae": ["1", 2]
            }
        },
        "9": {
            "class_type": "ImageCompositeMasked",
            "inputs": {
                "destination": ["2", 0],
                "source": ["8", 0],
                "x": 0,
                "y": 0,
                "resize_source": True,
                "mask": ["3", 0]
            }
        },
        "10": {
            "class_type": "SaveImage",
            "inputs": {
                "images": ["9", 0],
                "filename_prefix": ""  # Set per-image
            }
        }
    }


# ============================================================
# Image Processing Pipeline
# ============================================================

def process_image(image_path, output_dir, mask_dir, detector,
                  steps=STEPS, cfg=CFG, denoise=DENOISE, seed_offset=0):
    """Process a single image through the full correction pipeline.

    Returns a dict with processing results and metadata.
    """
    filename = os.path.basename(image_path)
    basename = os.path.splitext(filename)[0]
    W_out = os.path.join(output_dir, filename)
    result = {
        'filename': filename,
        'path': image_path,
        'status': 'unknown',
        'hands_detected': 0,
        'bboxes': [],
        'mask_pixels_pct': 0.0,
        'output_path': None,
        'error': None,
        'processing_time': 0,
        'pixel_change_pct': 0.0,
    }

    start_time = time.time()

    try:
        # Step 1: Hand detection
        bboxes, W, H, img = detector.detect(image_path)
        result['hands_detected'] = len(bboxes)
        result['bboxes'] = [
            {**b, 'x1': round(b['x1'], 4), 'x2': round(b['x2'], 4),
             'y1': round(b['y1'], 4), 'y2': round(b['y2'], 4)}
            for b in bboxes
        ]

        if len(bboxes) == 0:
            result['status'] = 'no_hands'
            result['processing_time'] = time.time() - start_time
            # Copy original to output (no correction needed)
            shutil.copy2(image_path, W_out)
            result['output_path'] = W_out
            return result

        # Step 2: Create mask
        mask = create_mask_from_bboxes(
            bboxes, W, H,
            padding=MASK_PADDING,
            morph_dilate=MORPH_DILATE,
            blur_radius=BLUR_RADIUS,
        )
        mask_pct = (mask > 0.5).sum() / (H * W) * 100
        result['mask_pixels_pct'] = round(mask_pct, 2)

        # Save mask visualization
        mask_filename = f"mask_{basename}.png"
        overlay_filename = f"overlay_{basename}.png"
        mask_pil = Image.fromarray((mask * 255).astype(np.uint8), mode='L')
        mask_pil.save(os.path.join(mask_dir, mask_filename))
        save_mask_visualization(mask, img, os.path.join(mask_dir, overlay_filename), bboxes)

        # Step 3: Save image + mask to ComfyUI input
        img_input_name = f"in_{basename}.png"
        mask_input_name = f"msk_{basename}.png"
        img.save(os.path.join(COMFYUI_INPUT, img_input_name))
        mask_pil.save(os.path.join(COMFYUI_INPUT, mask_input_name))

        # Step 4: Build and submit workflow
        seed = hash(basename + str(seed_offset)) % (2**31)
        workflow = build_inpainting_workflow(
            img_input_name, mask_input_name, seed, steps, cfg, denoise
        )
        workflow["10"]["inputs"]["filename_prefix"] = f"corrected_{basename}"

        prompt_id = submit_workflow(workflow)

        # Step 5: Wait for completion
        completed = wait_for_prompt(prompt_id, timeout=600)
        if not completed:
            result['status'] = 'timeout'
            result['error'] = 'ComfyUI timed out'
            result['processing_time'] = time.time() - start_time
            # Fall back to original
            shutil.copy2(image_path, W_out)
            result['output_path'] = W_out
            return result

        success, error = check_prompt_success(prompt_id)
        if not success:
            result['status'] = 'failed'
            result['error'] = error
            result['processing_time'] = time.time() - start_time
            shutil.copy2(image_path, W_out)
            result['output_path'] = W_out
            return result

        # Step 6: Retrieve output
        output_file = move_output(f"corrected_{basename}", W_out)
        if not output_file:
            result['status'] = 'no_output'
            result['error'] = 'No output file found in ComfyUI output dir'
            result['processing_time'] = time.time() - start_time
            shutil.copy2(image_path, W_out)
            result['output_path'] = W_out
            return result

        # Step 7: Calculate pixel change
        corrected_img = np.array(Image.open(W_out).convert('RGB'))
        orig_img = np.array(img.convert('RGB'))
        if corrected_img.shape == orig_img.shape:
            diff = np.abs(corrected_img.astype(float) - orig_img.astype(float))
            result['pixel_change_pct'] = round((diff > 10).mean() * 100, 2)

        # Clean up ComfyUI input files
        for f in [img_input_name, mask_input_name]:
            fpath = os.path.join(COMFYUI_INPUT, f)
            if os.path.exists(fpath):
                os.remove(fpath)

        result['status'] = 'corrected'
        result['output_path'] = W_out
        result['processing_time'] = time.time() - start_time

    except Exception as e:
        result['status'] = 'error'
        result['error'] = str(e)
        result['processing_time'] = time.time() - start_time
        # Copy original as fallback
        try:
            shutil.copy2(image_path, W_out)
            result['output_path'] = W_out
        except Exception:
            pass

    return result


def scan_images(input_dir):
    """Scan input directory for all image files recursively."""
    supported_exts = {'.png', '.jpg', '.jpeg', '.webp', '.bmp'}
    images = []
    for root, dirs, files in os.walk(input_dir):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in supported_exts:
                images.append(os.path.join(root, f))
    return sorted(images)


# ============================================================
# Contact Sheet Generator
# ============================================================

def create_contact_sheet(image_groups, output_path, title="Before/After Comparison",
                         thumb_size=(256, 256), columns=4):
    """Create a contact sheet comparing original, mask, and corrected images.

    image_groups: list of dicts with keys: 'original_path', 'corrected_path',
                  'mask_path', 'overlay_path', 'label'
    """
    rows = len(image_groups)
    cols = columns  # original | mask overlay | corrected | (empty for notes)

    margin = 20
    label_height = 30
    sheet_w = cols * thumb_size[0] + (cols + 1) * margin
    sheet_h = rows * (thumb_size[1] + label_height + margin) + margin + label_height
    sheet = Image.new('RGB', (sheet_w, sheet_h), (240, 240, 240))
    draw = ImageDraw.Draw(sheet)

    try:
        font = ImageFont.truetype("arial.ttf", 14)
        title_font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
        title_font = font

    # Title
    draw.text((margin, 5), title, fill=(0, 0, 0), font=title_font)

    labels = ["Original", "Mask Overlay", "Corrected", "Diff"]

    for row_idx, group in enumerate(image_groups):
        y_base = margin + label_height + row_idx * (thumb_size[1] + label_height + margin)

        for col_idx in range(cols):
            x = col_idx * (thumb_size[0] + margin) + margin
            label = labels[col_idx] if col_idx < len(labels) else ""
            draw.text((x, y_base - label_height + 5), label, fill=(80, 80, 80), font=font)

            if col_idx == 0:
                # Original
                img = Image.open(group['original_path']).convert('RGB')
            elif col_idx == 1:
                # Mask overlay
                if group.get('overlay_path') and os.path.exists(group['overlay_path']):
                    img = Image.open(group['overlay_path']).convert('RGB')
                else:
                    img = Image.new('RGB', thumb_size, (200, 200, 200))
                    draw.text((x + 10, y_base + 100), "No mask", fill=(128, 128, 128), font=font)
            elif col_idx == 2:
                # Corrected
                img = Image.open(group['corrected_path']).convert('RGB')
            elif col_idx == 3:
                # Diff
                orig = np.array(Image.open(group['original_path']).convert('RGB')).astype(float)
                corr = np.array(Image.open(group['corrected_path']).convert('RGB')).astype(float)
                # Resize to match
                if orig.shape == corr.shape:
                    diff = np.abs(corr - orig).astype(np.uint8)
                else:
                    from PIL import Image as PI
                    corr_resized = PI.fromarray(np.zeros_like(orig, dtype=np.uint8)).convert('RGB')
                    diff = np.zeros_like(orig, dtype=np.uint8)
                img = Image.fromarray(diff)

            img.thumbnail(thumb_size, Image.Resampling.LANCZOS)
            # Paste with centering
            paste_x = x + (thumb_size[0] - img.size[0]) // 2
            paste_y = y_base + (thumb_size[1] - img.size[1]) // 2
            sheet.paste(img, (paste_x, paste_y))

        # Row label
        draw.text((margin, y_base + thumb_size[1] + 5),
                   f"{group['label']}", fill=(0, 0, 0), font=font)

    sheet.save(output_path, quality=90)
    print(f"Contact sheet saved: {output_path}")


# ============================================================
# Statistics
# ============================================================

def print_statistics(results, output_dir):
    """Print and save processing statistics."""
    stats = {
        'total_images': len(results),
        'successfully_processed': sum(1 for r in results if r['status'] == 'corrected'),
        'no_hands': sum(1 for r in results if r['status'] == 'no_hands'),
        'failed': sum(1 for r in results if r['status'] in ('failed', 'error', 'timeout', 'no_output')),
        'with_hands': sum(1 for r in results if r['hands_detected'] > 0),
        'total_hands_detected': sum(r['hands_detected'] for r in results),
        'avg_processing_time': round(np.mean([r['processing_time'] for r in results]), 1) if results else 0,
        'avg_pixel_change': round(np.mean([r['pixel_change_pct'] for r in results if r['pixel_change_pct'] > 0]), 2) if results else 0,
    }
    
    print(f"\n{'='*60}")
    print(f"PROCESSING STATISTICS")
    print(f"{'='*60}")
    print(f"Total images:          {stats['total_images']}")
    print(f"Successfully corrected: {stats['successfully_processed']}")
    print(f"No hands detected:     {stats['no_hands']}")
    print(f"Failed:                {stats['failed']}")
    print(f"Images with hands:     {stats['with_hands']}")
    print(f"Total hands detected:  {stats['total_hands_detected']}")
    print(f"Avg processing time:   {stats['avg_processing_time']}s")
    print(f"Avg pixel change:      {stats['avg_pixel_change']}%")
    print(f"{'='*60}")

    # Save stats
    stats_path = os.path.join(output_dir, 'statistics.json')
    with open(stats_path, 'w') as f:
        json.dump(stats, f, indent=2)
    print(f"Statistics saved: {stats_path}")
    
    return stats


# ============================================================
# Main Pipeline
# ============================================================

def ensure_dirs():
    """Create all required output directories."""
    for d in [CORRECTED_DIR, MASKS_DIR, CONTACT_SHEETS_DIR, LOGS_DIR,
              COMFYUI_INPUT, COMFYUI_OUTPUT]:
        os.makedirs(d, exist_ok=True)


def run_test(steps=STEPS, cfg=CFG, denoise=DENOISE, input_dir=DEFAULT_INPUT_DIR, limit=0):
    """Run the pipeline on a small test set (5-10 images with hands)."""
    print("=" * 60)
    print("PHASE 4-5: TEST RUN (5-10 images with hands)")
    print(f"Settings: steps={steps}, cfg={cfg}, denoise={denoise}")
    print("=" * 60)

    ensure_dirs()
    detector = HandDetector()
    
    # Select test images — ones we know have hands
    test_candidates = []
    all_images = scan_images(input_dir)
    for img_path in all_images:
        filename = os.path.basename(img_path)
        if os.path.getsize(img_path) > 300000:  # Skip tiny images
            test_candidates.append(img_path)
        if len(test_candidates) >= 15:
            break

    # Run detection to filter for images with hands
    test_images = []
    for img_path in test_candidates:
        try:
            bboxes, W, H, _ = detector.detect(img_path)
            if len(bboxes) > 0:
                test_images.append(img_path)
                print(f"  [DETECT] {os.path.basename(img_path)}: {len(bboxes)} hands")
            if len(test_images) >= 8:
                break
        except Exception as e:
            print(f"  [SKIP] {os.path.basename(img_path)}: {e}")

    if not test_images:
        print("WARNING: No images with hands found in test set. Using first 5 images anyway.")
        test_images = test_candidates[:5]

    print(f"\nSelected {len(test_images)} test images")
    print(f"Processing each image through the full pipeline...\n")

    results = []
    for i, img_path in enumerate(test_images):
        print(f"[{i+1}/{len(test_images)}] {os.path.basename(img_path)}")
        result = process_image(
            img_path, CORRECTED_DIR, MASKS_DIR, detector,
            steps=steps, cfg=cfg, denoise=denoise, seed_offset=i
        )
        results.append(result)
        print(f"  Status: {result['status']}, "
              f"hands: {result['hands_detected']}, "
              f"mask: {result['mask_pixels_pct']}%, "
              f"change: {result['pixel_change_pct']}%, "
              f"time: {result['processing_time']:.1f}s")
    
    # Generate contact sheet for test results
    groups = []
    for r in results:
        orig = r['path']
        corr = r['output_path'] or orig
        basename = os.path.splitext(r['filename'])[0]
        overlay = os.path.join(MASKS_DIR, f"overlay_{basename}.png")
        groups.append({
            'original_path': orig,
            'corrected_path': corr,
            'overlay_path': overlay if os.path.exists(overlay) else None,
            'label': r['filename']
        })
    
    sheet_path = os.path.join(CONTACT_SHEETS_DIR, "test_contact_sheet.png")
    create_contact_sheet(groups, sheet_path, title="Test Run: Original | Mask | Corrected | Diff")

    # Save test results
    log_path = os.path.join(LOGS_DIR, "test_results.json")
    with open(log_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print_statistics(results, LOGS_DIR)
    print(f"\nTest results saved: {log_path}")
    print(f"Contact sheet: {sheet_path}")
    print("\nReview the contact sheet and test results before proceeding to full batch.")
    return results


def run_full_batch(steps=STEPS, cfg=CFG, denoise=DENOISE, input_dir=DEFAULT_INPUT_DIR):
    """Run the pipeline on all images in the input directory."""
    print("=" * 60)
    print("PHASE 7: FULL BATCH RUN")
    print("=" * 60)

    ensure_dirs()
    detector = HandDetector()
    
    all_images = scan_images(input_dir)
    
    # Load existing log to skip completed images
    log_path = os.path.join(LOGS_DIR, "batch_results.json")
    processed_files = set()
    if os.path.exists(log_path):
        with open(log_path) as f:
            existing = json.load(f)
            processed_files = {r['filename'] for r in existing if r['status'] in ('corrected', 'no_hands')}
        print(f"Skipping {len(processed_files)} already processed files")

    # Load failures for retry
    if os.path.exists(log_path):
        failures = [r for r in existing if r['status'] in ('failed', 'error', 'timeout', 'no_output')]
        if failures and os.path.exists(os.path.join(LOGS_DIR, "failed_images.json")):
            with open(os.path.join(LOGS_DIR, "failed_images.json")) as f:
                failed_files = json.load(f)
                print(f"Found {len(failed_files)} failed images from previous run")

    results = []
    for i, img_path in enumerate(all_images):
        filename = os.path.basename(img_path)
        if filename in processed_files:
            print(f"[{i+1}/{len(all_images)}] {filename} - SKIPPED (already processed)")
            # Load existing result
            for r in existing:
                if r['filename'] == filename:
                    results.append(r)
            continue

        print(f"[{i+1}/{len(all_images)}] {filename}")
        result = process_image(
            img_path, CORRECTED_DIR, MASKS_DIR, detector,
            steps=steps, cfg=cfg, denoise=denoise, seed_offset=i
        )
        results.append(result)
        print(f"  Status: {result['status']}, "
              f"hands: {result['hands_detected']}, "
              f"mask: {result['mask_pixels_pct']}%, "
              f"time: {result['processing_time']:.1f}s")
        
        if result['error']:
            print(f"  Error: {result['error']}")

        # Save incremental results
        with open(log_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)

    detector.close()

    # Generate contact sheet for results with hands
    groups = []
    for r in results:
        if r['hands_detected'] > 0 or r['status'] in ('corrected', 'failed', 'error'):
            orig = r['path']
            corr = r['output_path'] or orig
            basename = os.path.splitext(r['filename'])[0]
            overlay = os.path.join(MASKS_DIR, f"overlay_{basename}.png")
            groups.append({
                'original_path': orig,
                'corrected_path': corr,
                'overlay_path': overlay if os.path.exists(overlay) else None,
                'label': r['filename']
            })

    sheet_path = os.path.join(CONTACT_SHEETS_DIR, "full_contact_sheet.png")
    create_contact_sheet(groups, sheet_path, title="Full Batch: Original | Mask | Corrected | Diff")
    
    print_statistics(results, LOGS_DIR)
    print(f"\nFull batch results saved: {log_path}")
    print(f"Contact sheet: {sheet_path}")


def run_retry(steps=STEPS, cfg=CFG, denoise=DENOISE):
    """Retry failed images from the previous batch run."""
    print("=" * 60)
    print("PHASE 7: RETRY FAILED IMAGES")
    print("=" * 60)

    ensure_dirs()
    
    log_path = os.path.join(LOGS_DIR, "batch_results.json")
    if not os.path.exists(log_path):
        print("No previous results found. Run full batch first.")
        return

    with open(log_path) as f:
        results = json.load(f)

    failed = [r for r in results if r['status'] in ('failed', 'error', 'timeout', 'no_output')]
    print(f"Found {len(failed)} failed images to retry")

    if not failed:
        print("No failed images to retry.")
        return

    detector = HandDetector()

    for i, r in enumerate(failed):
        img_path = r['path']
        if not os.path.exists(img_path):
            print(f"[{i+1}/{len(failed)}] {r['filename']} - SKIP (source not found)")
            continue
        print(f"[{i+1}/{len(failed)}] {r['filename']}")
        new_result = process_image(
            img_path, CORRECTED_DIR, MASKS_DIR, detector,
            steps=steps, cfg=cfg, denoise=denoise, seed_offset=i
        )
        print(f"  Status: {new_result['status']}")
        
        # Update results
        r.update(new_result)
        with open(log_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)

    detector.close()
    print_statistics(results, LOGS_DIR)


def run_contact_sheet():
    """Generate a contact sheet from existing results (no reprocessing)."""
    print("=" * 60)
    print("Generating contact sheet from existing results...")
    print("=" * 60)

    ensure_dirs()
    
    log_path = os.path.join(LOGS_DIR, "batch_results.json")
    if not os.path.exists(log_path):
        print("No results found. Run batch first.")
        return

    with open(log_path) as f:
        results = json.load(f)

    # Select representative images: hands, no hands, corrected, failed
    groups = []
    
    # Images with detected hands (first 10)
    hands_results = [r for r in results if r['hands_detected'] > 0][:10]
    # Images with no hands (first 5)
    no_hands = [r for r in results if r['hands_detected'] == 0][:5]
    # Failed images
    failed = [r for r in results if r['status'] in ('failed', 'error')]
    # Images with weapons (none — documented limitation)
    
    for r in hands_results:
        basename = os.path.splitext(r['filename'])[0]
        overlay = os.path.join(MASKS_DIR, f"overlay_{basename}.png")
        groups.append({
            'original_path': r['path'],
            'corrected_path': r.get('output_path') or r['path'],
            'overlay_path': overlay if os.path.exists(overlay) else None,
            'label': f"[HAND] {r['filename']}"
        })
    
    for r in no_hands[:5]:
        groups.append({
            'original_path': r['path'],
            'corrected_path': r.get('output_path') or r['path'],
            'overlay_path': None,
            'label': f"[NO HANDS] {r['filename']}"
        })
    
    for r in failed[:3]:
        groups.append({
            'original_path': r['path'],
            'corrected_path': r.get('output_path') or r['path'],
            'overlay_path': None,
            'label': f"[FAILED] {r['filename']}"
        })

    sheet_path = os.path.join(CONTACT_SHEETS_DIR, "comparison_contact_sheet.png")
    create_contact_sheet(
        groups, sheet_path,
        title="Exile King Hand Correction — Comparison Sheet\n"
              "Categories: HAND DETECTED | NO HANDS | FAILED\n"
              "Weapons: NOT IMPLEMENTED (see report)"
    )
    print(f"\nContact sheet saved: {sheet_path}")


def main():
    parser = argparse.ArgumentParser(description="Exile King Hand Correction Pipeline")
    parser.add_argument("--mode", choices=["test", "full", "retry", "contact-sheet"],
                        default="test", help="Pipeline mode")
    parser.add_argument("--steps", type=int, default=STEPS, help="Sampling steps")
    parser.add_argument("--cfg", type=float, default=CFG, help="CFG scale")
    parser.add_argument("--denoise", type=float, default=DENOISE, help="Denoise strength (0.0-1.0)")
    parser.add_argument("--input-dir", default=DEFAULT_INPUT_DIR, help="Input art directory")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of images (0 = no limit)")
    
    args = parser.parse_args()
    
    if args.mode == "test":
        run_test(steps=args.steps, cfg=args.cfg, denoise=args.denoise, input_dir=args.input_dir)
    elif args.mode == "full":
        run_full_batch(steps=args.steps, cfg=args.cfg, denoise=args.denoise, input_dir=args.input_dir)
    elif args.mode == "retry":
        run_retry(steps=args.steps, cfg=args.cfg, denoise=args.denoise)
    elif args.mode == "contact-sheet":
        run_contact_sheet()


if __name__ == "__main__":
    main()

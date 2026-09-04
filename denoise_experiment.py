#!/usr/bin/env python
"""
Experiment: Test different denoise values on the 3 problem images.
Keeping ALL other parameters at original pipeline values.
Changing ONLY: denoise (0.4, 0.6, 0.8, 1.0)

This isolates whether the hand-collapse is caused by an unsuitable denoise value
for the Lightning model's inpainting workflow.
"""
import os, sys, json, time, shutil
import numpy as np
from PIL import Image, ImageFilter

import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

import urllib.request
import urllib.error

COMFYUI_DIR = r"D:\Jake\ComfyUI_windows_portable\ComfyUI"
COMFYUI_INPUT = os.path.join(COMFYUI_DIR, "input")
COMFYUI_OUTPUT = os.path.join(COMFYUI_DIR, "output")
API_URL = "http://127.0.0.1:8188"

CHECKPOINT = "dreamshaperXL_sfwLightningDPMSDE.safetensors"
HAND_MODEL = os.path.join(COMFYUI_DIR, "models", "detection", "hand_landmarker.task")

ORIGINAL_ROOT = r"D:\the-exile-king\art\prototype\commander-cards"
EXP_OUTPUT_DIR = r"D:\the-exile-king\art\corrected\experiment"
EXP_MASKS_DIR = r"D:\the-exile-king\art\corrected\experiment_masks"
EXP_LOGS_DIR = r"D:\the-exile-king\art\corrected\logs"

# ORIGINAL pipeline parameters
ORIG_PADDING = 0.5
ORIG_MORPH_DILATE = 15
ORIG_BLUR_RADIUS = 10
ORIG_GROW_MASK_BY = 8
ORIG_STEPS = 8
ORIG_CFG = 5.0
ORIG_RESIZE_SOURCE = True

# Test denoise values
DENOISE_VALUES = [0.4, 0.6, 0.8, 1.0]

# Only the 3 problem images
PROBLEM_FILES = [
    "achish-02_00002_.png",
    "achish-03_00002_.png",
    "achish-03_00003_.png",
]

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


def detect_hands(image_path):
    base_options = mp_python.BaseOptions(
        model_asset_path=HAND_MODEL,
        delegate=mp_python.BaseOptions.Delegate.CPU)
    options = vision.HandLandmarkerOptions(
        base_options=base_options, running_mode=vision.RunningMode.IMAGE,
        num_hands=4, min_hand_detection_confidence=0.3,
        min_hand_presence_confidence=0.3, min_tracking_confidence=0.3)
    detector = vision.HandLandmarker.create_from_options(options)
    img = Image.open(image_path).convert('RGB')
    W, H = img.size
    img_np = np.array(img)
    mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_np)
    result = detector.detect(mp_img)
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
                'x1': min(xs), 'x2': max(xs), 'y1': min(ys), 'y2': max(ys),
                'score': float(score), 'label': handedness})
    detector.close()
    return bboxes, W, H, img


def create_mask(bboxes, W, H, padding=0.5, morph_dilate=15, blur_radius=10):
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
    return np.array(mask_pil, dtype=np.float32) / 255.0


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
                    for item in running)
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


def check_success(prompt_id):
    try:
        req = urllib.request.Request(f"{API_URL}/history?prompt_id={prompt_id}", method="GET")
        with urllib.request.urlopen(req, timeout=10) as resp:
            history = json.loads(resp.read().decode("utf-8"))
        if prompt_id in history:
            status = history[prompt_id].get("status", {})
            if status.get("completed", False):
                return True, status.get("errors", [])
            return False, "Not completed"
        return False, "No history"
    except Exception as e:
        return False, str(e)


def move_output(prefix, dest):
    files = sorted([f for f in os.listdir(COMFYUI_OUTPUT) if f.startswith(prefix)])
    if not files:
        return None
    shutil.move(os.path.join(COMFYUI_OUTPUT, files[-1]), dest)
    return dest


def build_workflow(img_name, mask_name, seed, denoise):
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": CHECKPOINT}},
        "2": {"class_type": "LoadImage", "inputs": {"image": img_name}},
        "3": {"class_type": "LoadImageMask", "inputs": {"image": mask_name, "channel": "red"}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {"text": POSITIVE_PROMPT, "clip": ["1", 1]}},
        "5": {"class_type": "CLIPTextEncode", "inputs": {"text": NEGATIVE_PROMPT, "clip": ["1", 1]}},
        "6": {"class_type": "VAEEncodeForInpaint",
              "inputs": {"pixels": ["2", 0], "vae": ["1", 2], "mask": ["3", 0], "grow_mask_by": ORIG_GROW_MASK_BY}},
        "7": {"class_type": "KSampler",
              "inputs": {"model": ["1", 0], "seed": seed, "steps": ORIG_STEPS, "cfg": ORIG_CFG,
                         "sampler_name": SAMPLER_NAME, "scheduler": SCHEDULER,
                         "positive": ["4", 0], "negative": ["5", 0],
                         "latent_image": ["6", 0], "denoise": denoise}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["7", 0], "vae": ["1", 2]}},
        "9": {"class_type": "ImageCompositeMasked",
              "inputs": {"destination": ["2", 0], "source": ["8", 0], "x": 0, "y": 0,
                         "resize_source": ORIG_RESIZE_SOURCE, "mask": ["3", 0]}},
        "10": {"class_type": "SaveImage", "inputs": {"images": ["9", 0], "filename_prefix": ""}},
    }


def analyze_hand_region(corrected_arr, orig_arr, bboxes, W, H):
    """Check if hands are still present (not flat gray) in corrected image."""
    results = []
    for i, bb in enumerate(bboxes):
        x1, x2 = int(bb['x1'] * W), int(bb['x2'] * W)
        y1, y2 = int(bb['y1'] * H), int(bb['y2'] * H)
        corr_region = corrected_arr[y1:y2, x1:x2]
        orig_region = orig_arr[y1:y2, x1:x2]

        std = corr_region.reshape(-1, 3).std(axis=0).mean()
        mean_rgb = corr_region.reshape(-1, 3).mean(axis=0)
        orig_mean = orig_region.reshape(-1, 3).mean(axis=0)
        color_diff = np.abs(mean_rgb - orig_mean).mean()

        results.append({
            "hand": i,
            "label": bb.get("label", "?"),
            "std_rgb": float(std),
            "mean_rgb": [int(x) for x in mean_rgb],
            "orig_mean_rgb": [int(x) for x in orig_mean],
            "color_diff": float(color_diff),
            "is_flat_gray": std < 10,  # std near 0 = flat color = hand collapsed
        })
    return results


def main():
    os.makedirs(EXP_OUTPUT_DIR, exist_ok=True)
    os.makedirs(EXP_MASKS_DIR, exist_ok=True)
    os.makedirs(EXP_LOGS_DIR, exist_ok=True)

    print("=== DENOISE EXPERIMENT ===")
    print("Testing denoise values: {} on {} problem images".format(DENOISE_VALUES, len(PROBLEM_FILES)))
    print("All other params at ORIGINAL pipeline values")
    print("=" * 60)

    all_results = {}

    for fname in PROBLEM_FILES:
        basename = os.path.splitext(fname)[0]
        orig_path = os.path.join(ORIGINAL_ROOT, fname)

        print("\n{} --".format(fname))

        # Detect hands and create mask
        bboxes, W, H, img = detect_hands(orig_path)
        mask = create_mask(bboxes, W, H,
                           padding=ORIG_PADDING, morph_dilate=ORIG_MORPH_DILATE,
                           blur_radius=ORIG_BLUR_RADIUS)
        mask_pil = Image.fromarray((mask * 255).astype(np.uint8), mode='L')

        # Save mask
        mask_pil.save(os.path.join(EXP_MASKS_DIR, "exp_mask_{}.png".format(fname)))

        # Save to ComfyUI input
        img_name = "exp_{}.png".format(basename)
        mask_name = "exp_{}_mask.png".format(basename)
        img.save(os.path.join(COMFYUI_INPUT, img_name))
        mask_pil.save(os.path.join(COMFYUI_INPUT, mask_name))

        orig_arr = np.array(img.convert('RGB')).astype(float)
        file_results = {"bboxes": bboxes, "denoise_tests": []}

        for dn in DENOISE_VALUES:
            seed = hash(basename + "_dn{}".format(dn)) % (2**31)
            workflow = build_workflow(img_name, mask_name, seed, dn)
            workflow["10"]["inputs"]["filename_prefix"] = "exp_{}_{}".format(basename, dn)

            print("  denoise={} ... ".format(dn), end="", flush=True)

            try:
                prompt_id = submit_workflow(workflow)
                if not wait_for_prompt(prompt_id, timeout=600):
                    print("TIMEOUT")
                    file_results["denoise_tests"].append({"denoise": dn, "status": "timeout"})
                    continue

                success, errors = check_success(prompt_id)
                if not success:
                    print("ERROR: {}".format(errors))
                    file_results["denoise_tests"].append({"denoise": dn, "status": "error"})
                    continue

                dest = os.path.join(EXP_OUTPUT_DIR, "exp_{}_{}.png".format(basename, dn))
                output_file = move_output("exp_{}_{}".format(basename, dn), dest)
                if not output_file:
                    print("NO OUTPUT")
                    file_results["denoise_tests"].append({"denoise": dn, "status": "no_output"})
                    continue

                corrected = np.array(Image.open(dest).convert('RGB')).astype(float)
                analysis = analyze_hand_region(corrected, orig_arr, bboxes, W, H)
                total_change = (np.abs(corrected - orig_arr) > 10).mean() * 100

                flat_count = sum(1 for a in analysis if a["is_flat_gray"])
                print("change={:.1f}% flat_hands={}/{}".format(total_change, flat_count, len(analysis)))

                file_results["denoise_tests"].append({
                    "denoise": dn,
                    "status": "success",
                    "pixel_change_pct": round(total_change, 2),
                    "hand_analysis": analysis,
                })

            except Exception as e:
                print("ERROR: {}".format(e))
                file_results["denoise_tests"].append({"denoise": dn, "status": "error", "error": str(e)})

        all_results[fname] = file_results

        # Clean up input files
        for f in [img_name, mask_name]:
            p = os.path.join(COMFYUI_INPUT, f)
            if os.path.exists(p):
                os.remove(p)

    # Print summary table
    print("\n" + "=" * 60)
    print("EXPERIMENT SUMMARY: Hand region integrity by denoise value")
    print("=" * 60)
    print("{:<25} {:>6} {:>6} {:>6} {:>6} {:>8} {:>8}".format(
        "File", "0.4", "0.6", "0.8", "1.0", "orig_std", "corr_std"))
    for fname in PROBLEM_FILES:
        tests = {t["denoise"]: t for t in all_results[fname]["denoise_tests"]}
        bboxes = all_results[fname]["bboxes"]

        vals = {}
        for dn in DENOISE_VALUES:
            t = tests.get(dn, {})
            if t.get("status") == "success":
                flat_count = sum(1 for a in t.get("hand_analysis", []) if a["is_flat_gray"])
                avg_std = np.mean([a["std_rgb"] for a in t.get("hand_analysis", [])])
                vals[dn] = "{}/{} flat".format(flat_count, len(bboxes)) if flat_count > 0 else "{:.0f}".format(avg_std)
            else:
                vals[dn] = "ERR"

        # Get original hand std
        orig_path = os.path.join(ORIGINAL_ROOT, fname)
        orig = np.array(Image.open(orig_path).convert('RGB')).astype(float)
        orig_stds = []
        for bb in bboxes:
            x1, x2 = int(bb['x1']*512), int(bb['x2']*512)
            y1, y2 = int(bb['y1']*768), int(bb['y2']*768)
            orig_stds.append(orig[y1:y2, x1:x2].reshape(-1,3).std(axis=0).mean())
        orig_avg_std = np.mean(orig_stds) if orig_stds else 0

        # Get original pipeline corrected std
        corr_path = os.path.join(r"D:\the-exile-king\art\corrected\corrected", fname)
        corr = np.array(Image.open(corr_path).convert('RGB')).astype(float)
        corr_stds = []
        for bb in bboxes:
            x1, x2 = int(bb['x1']*512), int(bb['x2']*512)
            y1, y2 = int(bb['y1']*768), int(bb['y2']*768)
            corr_stds.append(corr[y1:y2, x1:x2].reshape(-1,3).std(axis=0).mean())
        corr_avg_std = np.mean(corr_stds) if corr_stds else 0

        print("{:<25} {:>6} {:>6} {:>6} {:>6} {:>8} {:>8}".format(
            fname, vals[0.4], vals[0.6], vals[0.8], vals[1.0], "{:.0f}".format(orig_avg_std), "{:.0f}".format(corr_avg_std)))

    # Save experiment results
    log_path = os.path.join(EXP_LOGS_DIR, "denoise_experiment.json")
    with open(log_path, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\nDetailed results: {log_path}")


if __name__ == "__main__":
    main()

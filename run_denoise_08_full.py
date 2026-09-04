#!/usr/bin/env python
"""
Run full 8-image hand correction pipeline at denoise=0.8 to test if it meets ≤10% regression threshold.
Uses original pipeline parameters EXCEPT denoise=0.8.
"""
import os, sys, json, time, shutil
import numpy as np
from PIL import Image, ImageFilter
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision
import urllib.request

COMFYUI_DIR = r"D:\Jake\ComfyUI_windows_portable\ComfyUI"
COMFYUI_INPUT = os.path.join(COMFYUI_DIR, "input")
COMFYUI_OUTPUT = os.path.join(COMFYUI_DIR, "output")
API_URL = "http://127.0.0.1:8188"

CHECKPOINT = "dreamshaperXL_sfwLightningDPMSDE.safetensors"
HAND_MODEL = os.path.join(COMFYUI_DIR, "models", "detection", "hand_landmarker.task")

ORIGINAL_ROOT = r"D:\the-exile-king\art\prototype\commander-cards"
OUTPUT_DIR = r"D:\the-exile-king\art\corrected\denoise_0.8"
MASKS_DIR = r"D:\the-exile-king\art\corrected\denoise_0.8_masks"
LOGS_DIR = r"D:\the-exile-king\art\corrected\logs"

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
STEPS = 8
CFG = 5.0
DENOISE = 0.8
GROW_MASK_BY = 8
MASK_PADDING = 0.5
MORPH_DILATE = 15
BLUR_RADIUS = 10
RESIZE_SOURCE = True

TEST_FILES = [
    "achish-01_00001_.png", "achish-01_00002_.png",
    "achish-02_00001_.png", "achish-02_00002_.png",
    "achish-02_00003_.png", "achish-03_00002_.png",
    "achish-03_00003_.png", "achish-04_00003_.png",
]


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


def build_workflow(img_name, mask_name, seed):
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": CHECKPOINT}},
        "2": {"class_type": "LoadImage", "inputs": {"image": img_name}},
        "3": {"class_type": "LoadImageMask", "inputs": {"image": mask_name, "channel": "red"}},
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
                         "resize_source": RESIZE_SOURCE, "mask": ["3", 0]}},
        "10": {"class_type": "SaveImage", "inputs": {"images": ["9", 0], "filename_prefix": ""}},
    }


def analyze_hand_region(corrected_arr, orig_arr, bboxes, W, H):
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
            "is_flat_gray": std < 10,
        })
    return results


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(MASKS_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(COMFYUI_INPUT, exist_ok=True)
    os.makedirs(COMFYUI_OUTPUT, exist_ok=True)

    print("=== DENOISE 0.8 FULL PIPELINE RUN ===")
    print("Params: padding={}, dilate={}, blur={}, grow={}, steps={}, cfg={}, denoise={}, resize={}".format(
        MASK_PADDING, MORPH_DILATE, BLUR_RADIUS, GROW_MASK_BY, STEPS, CFG, DENOISE, RESIZE_SOURCE))
    print("Images: {}".format(len(TEST_FILES)))
    print("=" * 60)

    results = {"bboxes_map": {}, "image_results": []}

    for i, fname in enumerate(TEST_FILES):
        basename = os.path.splitext(fname)[0]
        orig_path = os.path.join(ORIGINAL_ROOT, fname)
        out_path = os.path.join(OUTPUT_DIR, fname)
        print("\n[{}/{}] {} ... ".format(i+1, len(TEST_FILES), fname), end="", flush=True)

        bboxes, W, H, img = detect_hands(orig_path)
        results["bboxes_map"][fname] = bboxes

        if not bboxes:
            print("NO HANDS")
            shutil.copy2(orig_path, out_path)
            continue

        mask = create_mask(bboxes, W, H,
                           padding=MASK_PADDING, morph_dilate=MORPH_DILATE,
                           blur_radius=BLUR_RADIUS)
        mask_pil = Image.fromarray((mask * 255).astype(np.uint8), mode='L')
        mask_pil.save(os.path.join(MASKS_DIR, "mask_{}.png".format(fname)))

        img_name = "dn8_{}.png".format(basename)
        mask_name = "dn8_{}_mask.png".format(basename)
        img.save(os.path.join(COMFYUI_INPUT, img_name))
        mask_pil.save(os.path.join(COMFYUI_INPUT, mask_name))

        orig_arr = np.array(img.convert('RGB')).astype(float)
        seed = hash(basename + "_dn0.8") % (2**31)
        workflow = build_workflow(img_name, mask_name, seed)
        workflow["10"]["inputs"]["filename_prefix"] = "dn8_{}".format(basename)

        try:
            prompt_id = submit_workflow(workflow)
            if not wait_for_prompt(prompt_id, timeout=600):
                print("TIMEOUT")
                shutil.copy2(orig_path, out_path)
                continue

            success, errors = check_success(prompt_id)
            if not success:
                print("ERROR: {}".format(errors))
                shutil.copy2(orig_path, out_path)
                continue

            if not move_output("dn8_{}".format(basename), out_path):
                print("NO OUTPUT")
                shutil.copy2(orig_path, out_path)
                continue

            corrected = np.array(Image.open(out_path).convert('RGB')).astype(float)
            analysis = analyze_hand_region(corrected, orig_arr, bboxes, W, H)
            total_change = (np.abs(corrected - orig_arr) > 10).mean() * 100
            flat_count = sum(1 for a in analysis if a["is_flat_gray"])
            avg_std = np.mean([a["std_rgb"] for a in analysis])
            print("OK | change={:.1f}% flat_hands={}/{} avg_std={:.0f}".format(
                total_change, flat_count, len(analysis), avg_std))

            results["image_results"].append({
                "filename": fname,
                "status": "corrected",
                "pixel_change_pct": round(total_change, 2),
                "hand_analysis": analysis,
                "std_min": float(min(a["std_rgb"] for a in analysis)),
            })

        except Exception as e:
            print("ERROR: {}".format(e))
            shutil.copy2(orig_path, out_path)

        for f in [img_name, mask_name]:
            p = os.path.join(COMFYUI_INPUT, f)
            if os.path.exists(p):
                os.remove(p)

    log_path = os.path.join(LOGS_DIR, "denoise_0.8_results.json")
    with open(log_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print("\nResults saved: {}".format(log_path))
    print("Outputs in: {}".format(OUTPUT_DIR))


if __name__ == "__main__":
    main()

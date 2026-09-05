"""
SDXL Localized Inpainting Pipeline for Commander Card Hand Generation

Pipeline:
1. Takes a commander card image (512x768 portrait)
2. Resizes with padding to 1024x1024 for SDXL inpainting
3. Uses MediaPipe HandLandmarker to detect hand regions
4. Creates precise segmentation masks from hand landmarks
5. Uses SDXL inpainting model (sdxl_inpainting_v2.safetensors) to generate the hand
6. Resizes back to original dimensions and composites the result

VRAM optimization: Uses async weight offloading, processes one image at a time
"""

import cv2
import numpy as np
import os
import json
import time
import urllib.request
from PIL import Image
import gc
import sys

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

MODEL_PATH = "D:/the-exile-king/models/hand_landmarker.task"
CHECKPOINT_NAME = "sdxl_inpainting_v2.safetensors"
INPUT_DIR = "D:/the-exile-king/art/prototype/commander-cards/"
OUTPUT_DIR = "D:/the-exile-king/art/output/"

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

def create_hand_mask(image, model_path=MODEL_PATH):
    h, w, _ = image.shape
    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        num_hands=2,
        min_hand_detection_confidence=0.3,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5
    )
    detector = vision.HandLandmarker.create_from_options(options)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
    results = detector.detect(mp_image)
    mask = np.zeros((h, w), dtype=np.uint8)
    
    if results.hand_landmarks:
        num_hands = len(results.hand_landmarks)
        print(f"  Detected {num_hands} hand(s)")
        for landmarks in results.hand_landmarks:
            points = []
            for lm in landmarks:
                x = int(lm.x * w)
                y = int(lm.y * h)
                points.append((x, y))
            points = np.array(points, dtype=np.int32)
            hull = cv2.convexHull(points)
            cv2.fillConvexPoly(mask, hull, 255)
            connections = vision.HandLandmarksConnections.HAND_CONNECTIONS
            for conn in connections:
                pt1 = points[conn.start]
                pt2 = points[conn.end]
                cv2.line(mask, pt1, pt2, 255, thickness=2)
            for pt in points:
                cv2.circle(mask, pt, 8, 255, -1)
        kernel = np.ones((20, 20), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=3)
    else:
        print("  No hands detected - using fallback region mask")
        mask_h_start = int(h * 0.45)
        mask_h_end = int(h * 0.85)
        mask_w_start = int(w * 0.15)
        mask_w_end = int(w * 0.85)
        mask[mask_h_start:mask_h_end, mask_w_start:mask_w_end] = 255
        kernel = np.ones((30, 30), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=2)
        mask = cv2.erode(mask, kernel, iterations=1)
    
    detector.close()
    return mask

def undo_padding(img_padded, offset, scale, original_size):
    target_w = int(original_size[0] * scale)
    target_h = int(original_size[1] * scale)
    crop_box = (offset[0], offset[1], offset[0] + target_w, offset[1] + target_h)
    cropped = img_padded.crop(crop_box)
    result = cropped.resize(original_size, Image.LANCZOS)
    return result

def get_vram_stats():
    try:
        url = "http://127.0.0.1:8188/system_stats"
        resp = urllib.request.urlopen(url)
        data = json.loads(resp.read())
        if data.get("devices") and len(data["devices"]) > 0:
            dev = data["devices"][0]
            vram_total = dev.get("vram_total", 0)
            vram_free = dev.get("vram_free", 0)
            torch_vram_free = dev.get("torch_vram_free", 0)
            return {
                "vram_total_mb": round(vram_total / (1024*1024), 1),
                "vram_free_mb": round(vram_free / (1024*1024), 1),
                "torch_vram_free_mb": round(torch_vram_free / (1024*1024), 1),
            }
    except Exception:
        pass
    return None

def submit_workflow(workflow):
    data = json.dumps({"prompt": workflow, "client_id": "inpaint_pipeline"}).encode()
    req = urllib.request.Request("http://127.0.0.1:8188/prompt", data=data, headers={"Content-Type": "application/json"})
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.read().decode()[:500]}"}
    except Exception as e:
        return {"error": str(e)}

def wait_prompt_done(prompt_id, timeout=600):
    start = time.time()
    while time.time() - start < timeout:
        try:
            url = f"http://127.0.0.1:8188/history/{prompt_id}"
            resp = urllib.request.urlopen(url)
            data = json.loads(resp.read())
            if prompt_id in data:
                status = data[prompt_id].get("status", {})
                if status.get("completed"):
                    return data[prompt_id]
        except:
            pass
        time.sleep(5)
    return {"error": "timeout"}

def save_temp_files(image_array, mask_array, prefix):
    temp_dir = "D:/Jake/ComfyUI_windows_portable/ComfyUI/input/"
    os.makedirs(temp_dir, exist_ok=True)
    img_path = os.path.join(temp_dir, f"{prefix}_image.png")
    mask_path = os.path.join(temp_dir, f"{prefix}_mask.png")
    cv2.imwrite(img_path, image_array)
    cv2.imwrite(mask_path, mask_array)
    return f"{prefix}_image.png", f"{prefix}_mask.png"

def run_inpainting_workflow(image_name, mask_name, positive_prompt, negative_prompt, steps=20, cfg=7.0, denoise=0.9, seed=42):
    workflow = {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": CHECKPOINT_NAME}},
        "2": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["1", 1], "text": positive_prompt}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["1", 1], "text": negative_prompt}},
        "4": {"class_type": "LoadImage", "inputs": {"image": image_name}},
        "5": {"class_type": "LoadImage", "inputs": {"image": mask_name}},
        "6": {"class_type": "VAEEncodeForInpaint", "inputs": {"pixels": ["4", 0], "vae": ["1", 2], "mask": ["5", 1], "grow_mask_by": 4}},
        "7": {"class_type": "InpaintModelConditioning", "inputs": {"positive": ["2", 0], "negative": ["3", 0], "vae": ["1", 2], "pixels": ["4", 0], "mask": ["5", 1], "noise_mask": True}},
        "8": {"class_type": "KSampler", "inputs": {"seed": seed, "steps": steps, "cfg": cfg, "sampler_name": "euler", "scheduler": "normal", "model": ["1", 0], "positive": ["7", 0], "negative": ["7", 1], "latent_image": ["7", 2], "denoise": denoise}},
        "9": {"class_type": "VAEDecode", "inputs": {"samples": ["8", 0], "vae": ["1", 2]}},
        "10": {"class_type": "SaveImage", "inputs": {"images": ["9", 0], "filename_prefix": "inpaint_temp"}}
    }
    
    vram_before = get_vram_stats()
    print(f"  VRAM before: {json.dumps(vram_before)}")
    
    result = submit_workflow(workflow)
    print(f"  Submit result: {json.dumps(result, indent=2)}")
    
    if "prompt_id" not in result:
        return None, result
    
    prompt_id = result["prompt_id"]
    done = wait_prompt_done(prompt_id, timeout=600)
    
    vram_after = get_vram_stats()
    print(f"  VRAM after: {json.dumps(vram_after)}")
    
    if done.get("status", {}).get("error"):
        error = done["status"]["error"]
        msgs = done.get("status", {}).get("messages", [])
        for msg in msgs:
            if isinstance(msg, list) and len(msg) > 1 and msg[0] == "execution_error":
                error_details = msg[1].get("exception_message", "")
                return None, {"error": f"{error}: {error_details}"}
        return None, {"error": error}
    
    if done.get("outputs"):
        output_info = done["outputs"].get("10", {}).get("images", [{}])[0]
        filename = output_info.get("filename", "")
        output_path = f"D:/Jake/ComfyUI_windows_portable/ComfyUI/output/{filename}"
        print(f"  Output saved: {output_path}")
        return output_path, None
    
    return None, {"error": "No outputs returned"}

def process_single_image(image_path, output_path):
    print(f"\nProcessing: {os.path.basename(image_path)}")
    img_orig = Image.open(image_path).convert("RGB")
    print(f"  Original size: {img_orig.size}")
    
    img_padded, offset, scale, orig_size = resize_to_square(img_orig, 1024)
    print(f"  Padded size: {img_padded.size}")
    
    img_cv = cv2.cvtColor(np.array(img_padded), cv2.COLOR_RGB2BGR)
    mask = create_hand_mask(img_cv)
    print(f"  Mask shape: {mask.shape}")
    
    prefix = "hand_inpaint_" + str(int(time.time()))
    img_name, mask_name = save_temp_files(img_cv, mask, prefix)
    
    positive_prompt = "a detailed realistic hand, anatomical, 3d render style, matching the card art style"
    negative_prompt = "deformed, blurry, bad anatomy, extra fingers, missing fingers, low quality, distorted, text, signature, watermark"
    
    print(f"  Running SDXL inpainting (20 steps, denoise=0.9)...")
    output_path_tmp, error = run_inpainting_workflow(img_name, mask_name, positive_prompt, negative_prompt)
    
    if error:
        print(f"  ERROR: {json.dumps(error)}")
        return False
    
    result_img = Image.open(output_path_tmp).convert("RGB")
    result_orig = undo_padding(result_img, offset, scale, orig_size)
    print(f"  Result size: {result_orig.size}")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    result_orig.save(output_path)
    print(f"  Saved to: {output_path}")
    
    mask_output = os.path.join(os.path.dirname(output_path), "masks", os.path.basename(output_path).replace(".png", "_mask.png"))
    os.makedirs(os.path.dirname(mask_output), exist_ok=True)
    cv2.imwrite(mask_output, mask)
    
    temp_dir = "D:/Jake/ComfyUI_windows_portable/ComfyUI/input/"
    for f in os.listdir(temp_dir):
        if f.startswith(prefix):
            os.remove(os.path.join(temp_dir, f))
    
    # Also clean up output temp files
    for f in os.listdir("D:/Jake/ComfyUI_windows_portable/ComfyUI/output/"):
        if f.startswith("inpaint_temp"):
            os.remove(os.path.join("D:/Jake/ComfyUI_windows_portable/ComfyUI/output/", f))
    
    return True

if __name__ == "__main__":
    print("SDXL Localized Inpainting Pipeline")
    print("=" * 60)
    
    import sys
    if len(sys.argv) > 1:
        # Process specific file(s)
        test_images = sys.argv[1:]
    else:
        # Process all commander cards
        test_images = sorted(os.listdir(INPUT_DIR))
        test_images = [f for f in test_images if f.endswith('.png')]
    
    print(f"Processing {len(test_images)} image(s)")
    
    success_count = 0
    fail_count = 0
    
    for img_name in test_images:
        img_path = os.path.join(INPUT_DIR, img_name)
        if os.path.exists(img_path):
            output_path = os.path.join(OUTPUT_DIR, img_name.replace(".png", "_inpaint.png"))
            try:
                success = process_single_image(img_path, output_path)
                if success:
                    success_count += 1
                    print(f"  SUCCESS: {output_path}")
                else:
                    fail_count += 1
                    print(f"  FAILED: {img_name}")
            except Exception as e:
                fail_count += 1
                print(f"  EXCEPTION: {img_name} - {e}")
        else:
            print(f"  NOT FOUND: {img_path}")
    
    print(f"\n{'='*60}")
    print(f"Results: {success_count} succeeded, {fail_count} failed")
    print(f"Total processed: {success_count + fail_count}")

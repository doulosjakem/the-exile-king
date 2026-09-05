import json
import time
import os
import base64
import urllib.request
from PIL import Image
import io
import sys

INPUT_DIR = "D:/the-exile-king/art/prototype/commander-cards/"
OUTPUT_DIR = "D:/the-exile-king/art/output/"
QA_CSV = "D:/the-exile-king/art/output/qa_results.csv"
QA_BATCH = "D:/the-exile-king/art/output/qa_batch_{}.json"

FALLBACK_LIST = set([
    "achish-03_00001_.png",
    "achish-04_00001_.png",
    "achish-04_00002_.png",
    "david-01_00002_.png",
    "david-01_00003_.png",
    "david-02_00001_.png",
    "david-02_00002_.png",
    "david-02_00003_.png",
    "david-04_00001_.png",
    "david-05_00002_.png",
    "david-05_00003_.png",
    "david-06_00001_.png",
    "david-06_00003_.png",
    "david-07_00002_.png",
    "david-07_00003_.png",
    "david-08_00001_.png",
    "david-08_00002_.png",
    "david-08_00003_.png",
    "david-09_00001_.png",
    "david-09_00002_.png",
    "david-09_00003_.png",
    "david-10_00002_.png",
    "jonathan-03_00002_.png",
    "jonathan-04_00003_.png",
    "jonathan-05_00003_.png",
    "jonathan-06_00002_.png",
    "jonathan-07_00001_.png",
    "jonathan-09_00001_.png",
    "jonathan-10_00001_.png",
    "jonathan-10_00003_.png",
    "philistine-lord-02_00001_.png",
    "philistine-lord-05_00002_.png",
    "philistine-lord-06_00001_.png",
    "philistine-lord-10_00002_.png",
])

def encode_image_b64(image_path, max_size=(256, 384)):
    img = Image.open(image_path)
    if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
        img.thumbnail(max_size, Image.LANCZOS)
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

def ask_ollama(images_b64, prompt_text):
    payload = {
        "model": "qwen2.5vl:7b",
        "messages": [
            {
                "role": "user",
                "content": prompt_text,
                "images": images_b64
            }
        ],
        "stream": False,
        "options": {
            "temperature": 0.1,
            "top_p": 0.9
        }
    }
    req = urllib.request.Request('http://localhost:11434/api/chat', data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    resp = urllib.request.urlopen(req, timeout=300)
    data = json.loads(resp.read())
    return data.get('message', {}).get('content', 'No response')

def process_image_pair(img_name, batch_num):
    original_path = os.path.join(INPUT_DIR, img_name)
    inpainted_path = os.path.join(OUTPUT_DIR, img_name.replace(".png", "_inpaint.png"))
    
    if not os.path.exists(original_path) or not os.path.exists(inpainted_path):
        print(f"  SKIP (missing): {img_name}")
        return None
    
    is_fallback = img_name in FALLBACK_LIST
    detection_type = "fallback" if is_fallback else "mediapipe"
    print(f"  QAd: {img_name} (detection={detection_type})")
    
    orig_b64 = encode_image_b64(original_path)
    inpa_b64 = encode_image_b64(inpainted_path)
    
    prompt = """Two images: ORIGINAL (left) and INPAINTED (right). Task was hand correction via localized inpainting.
Classify the result as: IMPROVED, UNCHANGED, WORSE, or UNCERTAIN

Check:
- Is the inpainted hand anatomically plausible (fingers distinct, correct count)?
- Is surrounding artwork preserved (no changes outside hand region)?
- Were weapons/tools preserved?
- Any rectangular artifacts, style mismatch, hand removal?
- Is the result genuinely better, or just different?

Output EXACTLY:
RESULT: [IMPROVED|UNCHANGED|WORSE|UNCERTAIN]
HAND_VISIBILITY: [hand_visible|hand_replaced|hand_removed|no_change]
AROUND_AREA_CHANGED: [yes|no]
ARTIFACTS: [yes|no]
REASONING: [one sentence]
"""
    
    response = ask_ollama([orig_b64, inpa_b64], prompt)
    print(f"    Response: {response[:300]}...")
    
    result_type = "UNCERTAIN"
    reasoning = ""
    hand_vis = ""
    around_changed = ""
    artifacts = ""
    
    for line in response.split('\n'):
        line = line.strip()
        if line.startswith("RESULT:"):
            result_type = line.split(":", 1)[1].strip().upper()
            if result_type not in ["IMPROVED", "UNCHANGED", "WORSE", "UNCERTAIN"]:
                result_type = "UNCERTAIN"
        elif line.startswith("HAND_VISIBILITY:"):
            hand_vis = line.split(":", 1)[1].strip()
        elif line.startswith("AROUND_AREA_CHANGED:"):
            around_changed = line.split(":", 1)[1].strip()
        elif line.startswith("ARTIFACTS:"):
            artifacts = line.split(":", 1)[1].strip()
        elif line.startswith("REASONING:"):
            reasoning = line.split(":", 1)[1].strip()
    
    return {
        "filename": img_name,
        "detection": detection_type,
        "result": result_type,
        "reasoning": reasoning,
        "hand_visibility": hand_vis,
        "area_changed": around_changed,
        "artifacts": artifacts,
        "batch": batch_num,
    }

if __name__ == "__main__":
    all_images = sorted([f for f in os.listdir(OUTPUT_DIR) if f.endswith("_inpaint.png")])
    original_names = [f.replace("_inpaint.png", ".png") for f in all_images]
    
    batch_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    batch_size = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    start_idx = (batch_num - 1) * batch_size
    end_idx = start_idx + batch_size
    batch_images = original_names[start_idx:end_idx]
    
    if not batch_images:
        print("No images to process in this batch")
        exit(0)
    
    print(f"QA Batch {batch_num}: {len(batch_images)} images (indices {start_idx}-{end_idx-1})")
    print("=" * 60)
    
    results = []
    for img_name in batch_images:
        result = process_image_pair(img_name, batch_num)
        if result:
            results.append(result)
        time.sleep(0.5)
    
    with open(QA_BATCH.format(batch_num), 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nBatch {batch_num} results:")
    for r in results:
        print(f"  {r['filename']}: {r['result']} | Hand: {r['hand_visibility']} | AreaChanged: {r['area_changed']} | Artifacts: {r['artifacts']}")
    
    all_results = []
    for i in range(1, batch_num + 1):
        batch_file = QA_BATCH.format(i)
        if os.path.exists(batch_file):
            with open(batch_file) as f:
                batch_data = json.load(f)
                all_results.extend(batch_data)
    
    if all_results:
        improved = sum(1 for r in all_results if r.get("result") == "IMPROVED")
        worse = sum(1 for r in all_results if r.get("result") == "WORSE")
        unchanged = sum(1 for r in all_results if r.get("result") == "UNCHANGED")
        uncertain = sum(1 for r in all_results if r.get("result") == "UNCERTAIN")
        print(f"\nRunning totals: IMPROVED={improved}, WORSE={worse}, UNCHANGED={unchanged}, UNCERTAIN={uncertain}")
        print(f"Total processed: {len(all_results)}/{len(original_names)}")
import requests
import json
import time
import os
import shutil

def submit_workflow(workflow):
    data = json.dumps({"prompt": workflow, "client_id": "gen_test_img"}).encode()
    req = requests.Request("POST", "http://127.0.0.1:8188/prompt", data=data, headers={"Content-Type": "application/json"})
    prepared = req.prepare()
    try:
        resp = requests.Session().send(prepared)
        return json.loads(resp.text)
    except Exception as e:
        return {"error": str(e)}

def wait_prompt_done(prompt_id, timeout=600):
    start = time.time()
    while time.time() - start < timeout:
        try:
            url = f"http://127.0.0.1:8188/history/{prompt_id}"
            resp = requests.get(url)
            data = json.loads(resp.text)
            if prompt_id in data:
                status = data[prompt_id].get("status", {})
                if status.get("completed"):
                    return data[prompt_id]
        except:
            pass
        time.sleep(3)
    return {"error": "timeout"}

print("Generating test image with hand...")
print("=" * 60)

# First, generate a full image with a hand using SDXL
# Image size: 1024x1024, prompt: "a person showing their hand"
workflow = {
    "1": {
        "class_type": "CheckpointLoaderSimple",
        "inputs": {
            "ckpt_name": "sdxl_inpainting_v2.safetensors"
        }
    },
    "2": {
        "class_type": "CLIPTextEncode",
        "inputs": {
            "clip": ["1", 1],
            "text": "a person showing their hand, detailed fingers, realistic, studio lighting"
        }
    },
    "3": {
        "class_type": "CLIPTextEncode",
        "inputs": {
            "clip": ["1", 1],
            "text": "deformed, blurry, bad anatomy, extra fingers, missing fingers, low quality"
        }
    },
    "4": {
        "class_type": "EmptyLatentImage",
        "inputs": {
            "width": 1024,
            "height": 1024,
            "batch_size": 1
        }
    },
    "5": {
        "class_type": "KSampler",
        "inputs": {
            "seed": 12345,
            "steps": 30,
            "cfg": 7.0,
            "sampler_name": "euler",
            "scheduler": "normal",
            "model": ["1", 0],
            "positive": ["2", 0],
            "negative": ["3", 0],
            "latent_image": ["4", 0],
            "denoise": 1.0
        }
    },
    "6": {
        "class_type": "VAEDecode",
        "inputs": {
            "samples": ["5", 0],
            "vae": ["1", 2]
        }
    },
    "7": {
        "class_type": "SaveImage",
        "inputs": {
            "images": ["6", 0],
            "filename_prefix": "test_hand_base"
        }
    }
}

result = submit_workflow(workflow)
print(f"Submit result: {json.dumps(result, indent=2)}")

if "prompt_id" in result:
    prompt_id = result["prompt_id"]
    print(f"Waiting for generation (prompt_id={prompt_id})...")
    
    done = wait_prompt_done(prompt_id, timeout=600)
    
    if done.get("status", {}).get("error"):
        print(f"Error: {done['status']['error']}")
    elif done.get("outputs"):
        print(f"Outputs: {json.dumps(done['outputs'], indent=2)}")
        # Find the saved image
        outputs = done["outputs"].get("7", {})
        if "images" in outputs and len(outputs["images"]) > 0:
            saved_image = outputs["images"][0]
            print(f"Generated image: {saved_image}")
            # Copy to test location
            src_path = f"D:/Jake/ComfyUI_windows_portable/ComfyUI/output/{saved_image}"
            dst_path = "D:/the-exile-king/art/test/test_hand_image.png"
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy2(src_path, dst_path)
            print(f"Copied to: {dst_path}")
    else:
        print(f"Unknown result: {json.dumps(done, indent=2)[:500]}")

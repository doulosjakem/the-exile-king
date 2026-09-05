import json
import time
import urllib.request

def submit_workflow(workflow):
    data = json.dumps({"prompt": workflow, "client_id": "test_sdxl_inpaint"}).encode()
    req = urllib.request.Request("http://127.0.0.1:8188/prompt", data=data, headers={"Content-Type": "application/json"})
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read())
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

def get_gpu_stats():
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
    except Exception as e:
        return {"error": str(e)}
    return None

print("PHASE 2: SDXL Inpainting test")
print("=" * 60)

gpu_before = get_gpu_stats()
print(f"GPU before: {json.dumps(gpu_before, indent=2)}")

# SDXL inpainting workflow
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
            "text": "a detailed anatomical hand, 3d render, realistic hands, intricate details"
        }
    },
    "3": {
        "class_type": "CLIPTextEncode",
        "inputs": {
            "clip": ["1", 1],
            "text": "deformed, blurry, bad anatomy, extra fingers, missing fingers, low quality, distorted"
        }
    },
    "4": {
        "class_type": "LoadImage",
        "inputs": {
            "image": "test_hand_image.png"
        }
    },
    "5": {
        "class_type": "LoadImage",
        "inputs": {
            "image": "test_hand_mask.png"
        }
    },
    "6": {
        "class_type": "VAEEncodeForInpaint",
        "inputs": {
            "pixels": ["4", 0],
            "vae": ["1", 2],
            "mask": ["5", 1],
            "grow_mask_by": 4
        }
    },
    "7": {
        "class_type": "InpaintModelConditioning",
        "inputs": {
            "positive": ["2", 0],
            "negative": ["3", 0],
            "vae": ["1", 2],
            "pixels": ["4", 0],
            "mask": ["5", 1],
            "noise_mask": True
        }
    },
    "8": {
        "class_type": "KSampler",
        "inputs": {
            "seed": 12345,
            "steps": 20,
            "cfg": 7.0,
            "sampler_name": "euler",
            "scheduler": "normal",
            "model": ["1", 0],
            "positive": ["7", 0],
            "negative": ["7", 1],
            "latent_image": ["7", 2],
            "denoise": 0.9
        }
    },
    "9": {
        "class_type": "VAEDecode",
        "inputs": {
            "samples": ["8", 0],
            "vae": ["1", 2]
        }
    },
    "10": {
        "class_type": "SaveImage",
        "inputs": {
            "images": ["9", 0],
            "filename_prefix": "sdxl_inpaint_result"
        }
    }
}

print("\nSubmitting inpainting workflow...")
result = submit_workflow(workflow)
print(f"Submit result: {json.dumps(result, indent=2)}")

if "prompt_id" in result:
    prompt_id = result["prompt_id"]
    print(f"\nWaiting for completion (prompt_id={prompt_id})...")
    
    done = wait_prompt_done(prompt_id, timeout=600)
    gpu_after = get_gpu_stats()
    print(f"\nGPU after: {json.dumps(gpu_after, indent=2)}")
    
    if done.get("status", {}).get("error"):
        print(f"\nError: {done['status']['error']}")
        msgs = done.get('status', {}).get('messages', [])
        for msg in msgs:
            if isinstance(msg, list) and len(msg) > 1:
                print(f"  {msg[0]}: {msg[1]}")
    elif done.get("outputs"):
        print(f"\nOutputs: {json.dumps(done['outputs'], indent=2)}")
        print("SUCCESS: Inpainting completed without errors!")
    else:
        print(f"\nResult: {json.dumps(done, indent=2)[:500]}")
elif "error" in result:
    print(f"\nWorkflow error: {result['error']}")

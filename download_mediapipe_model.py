import urllib.request
import os

model_url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
dest_dir = r"D:\Jake\ComfyUI_windows_portable\ComfyUI\models\detection"
dest_path = os.path.join(dest_dir, "hand_landmarker.task")

os.makedirs(dest_dir, exist_ok=True)

if os.path.exists(dest_path):
    print(f"Model already exists at {dest_path} ({os.path.getsize(dest_path)} bytes)")
else:
    print(f"Downloading from {model_url}...")
    try:
        urllib.request.urlretrieve(model_url, dest_path)
        print(f"Downloaded: {dest_path} ({os.path.getsize(dest_path)} bytes)")
    except Exception as e:
        print(f"Download failed: {e}")

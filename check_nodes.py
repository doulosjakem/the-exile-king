import urllib.request, json

# Get all available nodes
req = urllib.request.Request("http://127.0.0.1:8188/object_info", method="GET")
with urllib.request.urlopen(req, timeout=30) as resp:
    data = json.loads(resp.read().decode())

# Check for key nodes we need
key_nodes = ["LoadImage", "LoadImageMask", "VAEEncodeForInpaint", "KSampler",
             "VAEDecode", "ImageCompositeMasked", "ImageToMask", "SaveImage",
             "CheckpointLoaderSimple", "CLIPTextEncode", "DilateMask", "FeatherMask",
             "GrowMask", "MaskComposite", "MaskPreview", "VAEEncode", "LoadImageOutput"]

for name in key_nodes:
    if name in data:
        info = data[name]
        print(f"\n=== {name} ===")
        print(f"  Category: {info.get('category', 'N/A')}")
        input_types = info.get('input', {}).get('required', {})
        optional = info.get('input', {}).get('optional', {})
        outputs = info.get('output', [])
        print(f"  Required inputs: {list(input_types.keys())}")
        if optional:
            print(f"  Optional inputs: {list(optional.keys())}")
        print(f"  Outputs: {outputs}")
    else:
        print(f"\n=== {name} === NOT FOUND")

# Count total nodes
print(f"\n\nTotal nodes available: {len(data)}")
print(f"Total node names: {sorted(data.keys())[:50]}...")

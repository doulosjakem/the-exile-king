import os, cv2, numpy as np

mask_dir = r"D:\the-exile-king\art\output\masks"
orig_dir = r"D:\the-exile-king\art\prototype\commander-cards"

test_cases = [
    {"name": "achish-01_00001_.png", "type": "MediaPipe", "notes": "straightforward MediaPipe case"},
    {"name": "jonathan-08_00002_.png", "type": "MediaPipe-complex", "notes": "complex MediaPipe, large mask (56k px)"},
    {"name": "achish-03_00001_.png", "type": "Fallback", "notes": "fallback mask, skin tone 21%, dark area"},
    {"name": "david-09_00003_.png", "type": "Fallback", "notes": "fallback mask, high skin tone 69.3%"},
    {"name": "david-02_00002_.png", "type": "Fallback", "notes": "fallback with weapon+armor overlap"},
]

for tc in test_cases:
    fname = tc["name"]
    mask_name = fname.replace(".png", "_inpaint_mask.png")
    mask_path = os.path.join(mask_dir, mask_name)
    orig_path = os.path.join(orig_dir, fname)
    
    has_mask = os.path.exists(mask_path)
    has_orig = os.path.exists(orig_path)
    
    white = 0
    is_fallback = False
    if has_mask:
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        h, w = mask.shape
        white = int(np.count_nonzero(mask > 127))
        is_fallback = (white / (h*w) > 0.25 and white / (h*w) < 0.40)
    
    print(f"{fname}:")
    print(f"  type={tc['type']}, has_mask={has_mask}, has_orig={has_orig}")
    print(f"  mask_white_px={white}, is_fallback={is_fallback}")
    print(f"  notes={tc['notes']}")
    print()
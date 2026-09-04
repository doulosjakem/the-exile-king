from PIL import Image
import numpy as np
import os

orig_path = r"D:\the-exile-king\art\prototype\unit-cards\siege-engineer.png"
corrected_path = r"D:\the-exile-king\art\corrected\test\siege-engineer.png"
mask_path = r"D:\the-exile-king\art\corrected\test\masks\siege-engineer_mask.png"
overlay_path = r"D:\the-exile-king\art\corrected\test\masks\siege-engineer_overlay.png"

for label, path in [("Original", orig_path), ("Corrected", corrected_path), ("Mask", mask_path), ("Mask Overlay", overlay_path)]:
    if os.path.exists(path):
        img = Image.open(path)
        arr = np.array(img)
        print(f"{label}: size={img.size}, mode={img.mode}, shape={arr.shape}, "
              f"min={arr.min()}, max={arr.max()}, mean={arr.mean():.1f}")
    else:
        print(f"{label}: NOT FOUND at {path}")

# Check pixel difference between original and corrected
if os.path.exists(orig_path) and os.path.exists(corrected_path):
    orig = np.array(Image.open(orig_path).convert('RGB'))
    corr = np.array(Image.open(corrected_path).convert('RGB'))
    diff = np.abs(orig.astype(float) - corr.astype(float))
    changed_pixels_ratio = np.mean(diff > 10)
    max_diff = diff.max()
    mean_diff = diff.mean()
    print(f"\n--- Comparison ---")
    print(f"Pixels changed (>10): {changed_pixels_ratio * 100:.2f}%")
    print(f"Max diff: {max_diff:.1f}, Mean diff: {mean_diff:.1f}")

# Check mask stats
if os.path.exists(mask_path):
    mask = np.array(Image.open(mask_path).convert('L'))
    white_pixels = np.sum(mask > 127)
    total = mask.shape[0] * mask.shape[1]
    print(f"\n--- Mask Info ---")
    print(f"Size: {mask.shape}")
    print(f"White (inpaint) pixels: {white_pixels} ({white_pixels/total*100:.1f}%)")
    print(f"Non-zero (after blur) pixels: {np.sum(mask > 0)} ({np.sum(mask > 0)/total*100:.1f}%)")

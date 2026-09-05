"""
Pixel-level difference analysis between original and inpainted images.
Computes MSE, identifies change regions, and verifies no changes outside mask.
"""
import cv2
import numpy as np
import os
import csv

INPUT_DIR = "D:/the-exile-king/art/prototype/commander-cards/"
OUTPUT_DIR = "D:/the-exile-king/art/output/"
MASK_DIR = "D:/the-exile-king/art/output/masks/"
DIFF_CSV = "D:/the-exile-king/art/output/pixel_diff_analysis.csv"

def compute_diff_stats(original_path, inpainted_path, mask_path):
    """Compute pixel-level difference statistics."""
    orig = cv2.imread(original_path)
    inpa = cv2.imread(inpainted_path)
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    
    if orig is None or inpa is None or mask is None:
        return None
    
    # Ensure same size
    h, w = orig.shape[:2]
    inpa = cv2.resize(inpa, (w, h))
    mask = cv2.resize(mask, (w, h))
    
    # Compute per-channel differences
    diff = cv2.absdiff(orig, inpa)
    
    # Binary change mask (any pixel difference > 2 = changed)
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    changed = diff_gray > 2
    
    # Count pixels
    total_pixels = h * w
    changed_pixels = np.count_nonzero(changed)
    mask_pixels = np.count_nonzero(mask > 127)
    
    # Pixels changed inside mask
    changed_in_mask = np.count_nonzero(np.logical_and(changed, mask > 127))
    
    # Pixels changed outside mask
    changed_outside_mask = np.count_nonzero(np.logical_and(changed, mask <= 127))
    
    # MSE
    mse = np.mean((orig.astype(np.float32) - inpa.astype(np.float32)) ** 2)
    
    # RMSE
    rmse = np.sqrt(mse)
    
    # Change ratio
    change_ratio = changed_pixels / total_pixels
    outside_change_ratio = changed_outside_mask / total_pixels
    
    # Mean diff in masked vs unmasked regions
    mean_diff_masked = np.mean(diff_gray[mask > 127]) if mask_pixels > 0 else 0
    mean_diff_unmasked = np.mean(diff_gray[mask <= 127]) if (total_pixels - mask_pixels) > 0 else 0
    
    return {
        "total_pixels": total_pixels,
        "changed_pixels": changed_pixels,
        "mask_pixels": mask_pixels,
        "changed_in_mask": changed_in_mask,
        "changed_outside_mask": changed_outside_mask,
        "mse": round(mse, 2),
        "rmse": round(rmse, 2),
        "change_ratio": round(change_ratio * 100, 2),
        "outside_change_pct": round(outside_change_ratio * 100, 2),
        "mean_diff_masked": round(float(mean_diff_masked), 2),
        "mean_diff_unmasked": round(float(mean_diff_unmasked), 2),
    }

if __name__ == "__main__":
    print("Pixel-Level Difference Analysis")
    print("=" * 60)
    
    original_images = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith('.png')])
    
    all_stats = []
    for img_name in original_images:
        original_path = os.path.join(INPUT_DIR, img_name)
        inpainted_path = os.path.join(OUTPUT_DIR, img_name.replace(".png", "_inpaint.png"))
        mask_path = os.path.join(MASK_DIR, img_name.replace(".png", "_inpaint_mask.png"))
        
        stats = compute_diff_stats(original_path, inpainted_path, mask_path)
        if stats:
            stats["filename"] = img_name
            all_stats.append(stats)
            
            # Flag concerning cases
            flags = []
            if stats["outside_change_pct"] > 5:
                flags.append(f"HIGH_OUTSIDE_CHANGE({stats['outside_change_pct']}%)")
            if stats["change_ratio"] < 1:
                flags.append("NO_CHANGE")
            if stats["mse"] < 10:
                flags.append("LOW_MSE")
            
            if flags:
                print(f"  {img_name}: {', '.join(flags)} | MSE={stats['mse']} | outside={stats['outside_change_pct']}%")
    
    # Write CSV
    if all_stats:
        fieldnames = ["filename", "total_pixels", "changed_pixels", "mask_pixels", 
                      "changed_in_mask", "changed_outside_mask", "mse", "rmse",
                      "change_ratio", "outside_change_pct", "mean_diff_masked", "mean_diff_unmasked"]
        with open(DIFF_CSV, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for s in all_stats:
                row = {k: s.get(k, "") for k in fieldnames}
                writer.writerow(row)
        print(f"\nCSV saved to: {DIFF_CSV}")
    
    # Summary
    print(f"\n{'='*60}")
    print("DIFFERENCE SUMMARY")
    print("=" * 60)
    total_images = len(all_stats)
    
    no_change = sum(1 for s in all_stats if s["change_ratio"] < 1)
    low_mse = sum(1 for s in all_stats if s["mse"] < 10)
    high_outside = sum(1 for s in all_stats if s["outside_change_pct"] > 5)
    normal = sum(1 for s in all_stats if s["change_ratio"] >= 1 and s["mse"] >= 10 and s["outside_change_pct"] <= 5)
    
    print(f"Total images: {total_images}")
    print(f"No change (change_ratio < 1%): {no_change}")
    print(f"Low MSE (< 10): {low_mse}")
    print(f"High outside change (> 5%): {high_outside}")
    print(f"Normal change: {normal}")
    
    avg_mse = np.mean([s["mse"] for s in all_stats])
    avg_change = np.mean([s["change_ratio"] for s in all_stats])
    avg_outside = np.mean([s["outside_change_pct"] for s in all_stats])
    
    print(f"\nAverage MSE: {avg_mse:.2f}")
    print(f"Average change ratio: {avg_change:.2f}%")
    print(f"Average outside-mask change: {avg_outside:.2f}%")
    
    # List all images with their stats
    print(f"\n{'='*60}")
    print("PER-IMAGE STATS")
    print("=" * 60)
    print(f"{'Filename':<35} {'MSE':>8} {'Change%':>8} {'Outside%':>10} {'Flag':>10}")
    print("-" * 80)
    for s in sorted(all_stats, key=lambda x: x["outside_change_pct"], reverse=True)[:20]:
        flag = "!" if s["outside_change_pct"] > 5 or s["change_ratio"] < 1 else " "
        print(f"{s['filename'][:35]:<35} {s['mse']:>8.1f} {s['change_ratio']:>7.2f}% {s['outside_change_pct']:>9.2f}% {flag:>10}")

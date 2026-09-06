"""
EXPERIMENTS 2-4: Analysis of existing outputs, hard composite, and fallback masks.

Experiment 2: Original vs existing SDXL output
  - Using the already-generated 120 outputs, select 5 representative cases
  - Quantify: total image change, outside-mask change, inside-mask change

Experiment 3: Hard mask composite using existing outputs only
  - Construct: composite = original outside mask + generated image inside mask
  - Measure outside-mask change (should be ~0)
  - Visual assessment of hand integration, boundaries, halo, etc.

Experiment 4: Fallback mask risk analysis
  - Check fallback masks for overlap with hands, weapons, armor, etc.
"""
import os
import json
import csv
import numpy as np
import cv2
from PIL import Image, ImageDraw
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ORIGINAL_ROOT = r"D:\the-exile-king\art\prototype\commander-cards"
OUTPUT_DIR = r"D:\the-exile-king\art\output"
MASK_DIR = r"D:\the-exile-king\art\output\masks"
QA_DIR = r"D:\the-exile-king\art\corrected\experiment"
QA_LOGS_DIR = os.path.join(QA_DIR, "logs")

os.makedirs(QA_DIR, exist_ok=True)
os.makedirs(QA_LOGS_DIR, exist_ok=True)


def load_image(path, as_array=True):
    img = Image.open(path).convert("RGB")
    if as_array:
        return np.array(img)
    return img


def load_mask(path):
    mask = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if mask is None:
        mask = np.array(Image.open(path).convert("L"))
    return mask


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


def undo_padding(img_padded, offset, scale, original_size):
    target_w = int(original_size[0] * scale)
    target_h = int(original_size[1] * scale)
    crop_box = (offset[0], offset[1], offset[0] + target_w, offset[0] + target_h)
    cropped = img_padded.crop(crop_box)
    result = cropped.resize(original_size, Image.LANCZOS)
    return result


def compute_change_stats(orig, output, mask, threshold=2):
    """Compute change statistics between original and output, inside and outside mask."""
    orig_arr = orig.astype(np.float32)
    out_arr = output.astype(np.float32)

    h, w = orig_arr.shape[:2]
    mask = cv2.resize(mask, (w, h))
    mask_bin = mask > 127

    diff = np.abs(orig_arr - out_arr)
    changed = np.any(diff > threshold, axis=2)

    total_pixels = h * w
    mask_pixels = int(np.count_nonzero(mask_bin))
    outside_pixels = total_pixels - mask_pixels

    changed_in_mask = int(np.count_nonzero(np.logical_and(changed, mask_bin)))
    changed_outside_mask = int(np.count_nonzero(np.logical_and(changed, ~mask_bin)))

    mse = float(np.mean((orig_arr - out_arr) ** 2))
    total_change_pct = round(changed.sum() / total_pixels * 100, 2)
    inside_change_pct = round(changed_in_mask / max(mask_pixels, 1) * 100, 2)
    outside_change_pct = round(changed_outside_mask / max(outside_pixels, 1) * 100, 2)

    diff_gray = diff.mean(axis=2)
    mean_diff_masked = float(diff_gray[mask_bin].mean()) if mask_pixels > 0 else 0
    mean_diff_unmasked = float(diff_gray[~mask_bin].mean()) if outside_pixels > 0 else 0
    max_diff_masked = float(diff_gray[mask_bin].max()) if mask_pixels > 0 else 0
    max_diff_unmasked = float(diff_gray[~mask_bin].max()) if outside_pixels > 0 else 0

    return {
        "total_pixels": total_pixels,
        "mask_pixels": mask_pixels,
        "outside_pixels": outside_pixels,
        "changed_pixels": int(changed.sum()),
        "changed_in_mask": changed_in_mask,
        "changed_outside_mask": changed_outside_mask,
        "mse": round(mse, 2),
        "rmse": round(float(np.sqrt(mse)), 2),
        "total_change_pct": total_change_pct,
        "inside_change_pct": inside_change_pct,
        "outside_change_pct": outside_change_pct,
        "mean_diff_masked": round(mean_diff_masked, 2),
        "mean_diff_unmasked": round(mean_diff_unmasked, 2),
        "max_diff_masked": round(max_diff_masked, 2),
        "max_diff_unmasked": round(max_diff_unmasked, 2),
    }


def hard_composite(orig_arr, output_arr, mask, dilate_iter=0, blur_radius=0):
    """
    Create a hard composite: original outside mask, output inside mask.
    
    Args:
        orig_arr: original image array (HxWxC)
        output_arr: inpainted image array (HxWxC)
        mask: binary mask (HxW), values 0-255
        dilate_iter: number of dilation iterations
        blur_radius: gaussian blur radius for soft mask
    """
    h, w = orig_arr.shape[:2]
    mask_resized = cv2.resize(mask, (w, h)).astype(np.float32) / 255.0

    if dilate_iter > 0:
        kernel = np.ones((15, 15), np.uint8)
        mask_resized = cv2.dilate(mask_resized, kernel, iterations=dilate_iter)

    if blur_radius > 0:
        mask_resized = cv2.GaussianBlur(mask_resized, (0, 0), blur_radius)

    mask_expanded = mask_resized[:, :, np.newaxis]

    composite = orig_arr.astype(np.float64) * (1 - mask_expanded) + output_arr.astype(np.float64) * mask_expanded
    return composite.clip(0, 255).astype(np.uint8)


def is_fallback_mask(mask_arr):
    """Check if mask is the center-bottom fallback pattern (327494 px at 1024x1024)."""
    white_pixels = np.count_nonzero(mask_arr > 127)
    total = mask_arr.shape[0] * mask_arr.shape[1]
    if total == 1048576:  # 1024x1024
        return white_pixels == 327494
    elif total == 393216:  # 512x768
        return white_pixels == 123090
    # Check if it's approximately 31% of the image
    return white_pixels / total > 0.25 and white_pixels / total < 0.40


def analyze_mask_contents(mask_arr, img_shape):
    """Analyze where the mask falls in the original image based on position."""
    h, w = img_shape[:2]
    mask_resized = cv2.resize(mask_arr, (w, h))
    mask_bin = mask_resized > 127

    # Get mask bounding box
    ys, xs = np.where(mask_bin)
    if len(ys) == 0:
        return {"empty": True}

    y_min, y_max = ys.min(), ys.max()
    x_min, x_max = xs.min(), xs.max()

    # Divide image into quadrants and regions
    # For portrait images (512x768), hands are typically in the lower half
    regions = {
        "top_left": mask_bin[:h//2, :w//2].sum(),
        "top_right": mask_bin[:h//2, w//2:].sum(),
        "bottom_left": mask_bin[h//2:, :w//2].sum(),
        "bottom_right": mask_bin[h//2:, w//2:].sum(),
        "bottom_third": mask_bin[int(h*2/3):, :].sum(),
        "center": mask_bin[int(h*2/5):int(h*3/5), int(w*2/5):int(w*3/5)].sum(),
    }

    # For fallback masks, estimate hand position (hands are typically at bottom center)
    # Check if mask covers the hand/wrist area
    fallback_hand_area = mask_bin[int(h*0.45):int(h*0.85), int(w*0.15):int(w*0.85)].sum()
    total_white = mask_bin.sum()
    hand_area_pct = fallback_hand_area / max(total_white, 1) * 100

    return {
        "empty": False,
        "bbox": {"x_min": int(x_min), "y_min": int(y_min), "x_max": int(x_max), "y_max": int(y_max)},
        "regions": {k: int(v) for k, v in regions.items()},
        "total_white": int(total_white),
        "hand_area_coverage_pct": round(hand_area_pct, 2),
    }


def create_comparison_figure(orig, output, mask, composite, fname, out_path):
    """Create a 4-panel comparison figure."""
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))

    axes[0].imshow(orig)
    axes[0].set_title("Original")
    axes[0].axis('off')

    axes[1].imshow(output)
    axes[1].set_title("Existing SDXL Output")
    axes[1].axis('off')

    mask_viz = np.zeros_like(orig)
    mask_resized = cv2.resize(mask, (orig.shape[1], orig.shape[0]))
    mask_viz[:, :, 0] = mask_resized * 0.6
    overlay = cv2.addWeighted(orig, 0.7, mask_viz, 0.3, 0)
    axes[2].imshow(overlay)
    axes[2].set_title("Output + Mask Overlay")
    axes[2].axis('off')

    axes[3].imshow(composite)
    axes[3].set_title("Hard Composite")
    axes[3].axis('off')

    fig.suptitle(fname, fontsize=14)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()


def main():
    print("=" * 70)
    print("EXPERIMENTS 2-4: Existing Output Analysis, Hard Composite, Fallback Masks")
    print("=" * 70)

    # Read existing pixel diff analysis
    diff_csv = os.path.join(OUTPUT_DIR, "pixel_diff_analysis.csv")
    existing_stats = {}
    if os.path.exists(diff_csv):
        with open(diff_csv, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_stats[row["filename"]] = row
        print(f"Loaded existing pixel diff analysis for {len(existing_stats)} images")

    # Identify test images for Experiments 2-3
    # Select representative cases:
    # - 2 MediaPipe cases (one high outside change, one low)
    # - 2 fallback cases (one high, one moderate)
    # - 1 visually complex case

    test_cases = [
        {"name": "achish-01_00001_.png", "type": "MediaPipe", "notes": "MediaPipe detection"},
        {"name": "david-09_00003_.png", "type": "MediaPipe", "notes": "MediaPipe, lowest outside change (20.2%)"},
        {"name": "achish-03_00001_.png", "type": "Fallback", "notes": "Fallback mask, outside=26.65%"},
        {"name": "david-05_00002_.png", "type": "Fallback", "notes": "Fallback mask, outside=29.5%"},
        {"name": "jonathan-08_00002_.png", "type": "MediaPipe-complex", "notes": "MediaPipe, large mask (56k px)"},
    ]

    # ================================================================
    # EXPERIMENT 2: Original vs existing SDXL output
    # ================================================================
    print(f"\n{'='*70}")
    print("EXPERIMENT 2: ORIGINAL vs EXISTING SDXL OUTPUT")
    print("=" * 70)

    exp2_results = []
    for tc in test_cases:
        fname = tc["name"]
        orig_path = os.path.join(ORIGINAL_ROOT, fname)
        output_path = os.path.join(OUTPUT_DIR, fname.replace(".png", "_inpaint.png"))
        mask_path = os.path.join(MASK_DIR, fname.replace(".png", "_inpaint_mask.png"))

        if not all(os.path.exists(p) for p in [orig_path, output_path, mask_path]):
            print(f"  [{fname}] Missing files, skipping")
            continue

        orig_arr = load_image(orig_path)
        output_arr = load_image(output_path)
        mask_arr = load_mask(mask_path)

        # Resize output and mask to original dimensions (in case they're at different sizes)
        h, w = orig_arr.shape[:2]
        output_resized = cv2.resize(output_arr, (w, h))
        mask_resized = cv2.resize(mask_arr, (w, h))

        stats = compute_change_stats(orig_arr, output_resized, mask_resized)
        stats["filename"] = fname
        stats["mask_type"] = tc["type"]

        print(f"\n  [{fname}] ({tc['type']})")
        print(f"    MSE: {stats['mse']}")
        print(f"    Total change: {stats['total_change_pct']}%")
        print(f"    Outside-mask change: {stats['outside_change_pct']}%")
        print(f"    Inside-mask change: {stats['inside_change_pct']}%")
        print(f"    Mean diff (masked): {stats['mean_diff_masked']}")
        print(f"    Mean diff (unmasked): {stats['mean_diff_unmasked']}")

        exp2_results.append(stats)

    # ================================================================
    # EXPERIMENT 3: Hard mask composite using existing outputs
    # ================================================================
    print(f"\n{'='*70}")
    print("EXPERIMENT 3: HARD MASK COMPOSITE (existing outputs only)")
    print("=" * 70)

    exp3_results = []
    for tc in test_cases:
        fname = tc["name"]
        orig_path = os.path.join(ORIGINAL_ROOT, fname)
        output_path = os.path.join(OUTPUT_DIR, fname.replace(".png", "_inpaint.png"))
        mask_path = os.path.join(MASK_DIR, fname.replace(".png", "_inpaint_mask.png"))

        if not all(os.path.exists(p) for p in [orig_path, output_path, mask_path]):
            print(f"  [{fname}] Missing files, skipping")
            continue

        orig_arr = load_image(orig_path)
        output_arr = load_image(output_path)
        mask_arr = load_mask(mask_path)

        h, w = orig_arr.shape[:2]
        output_resized = cv2.resize(output_arr, (w, h))
        mask_resized = cv2.resize(mask_arr, (w, h))

        # Test with raw mask (no dilate, no blur)
        composite_raw = hard_composite(orig_arr, output_resized, mask_resized, dilate_iter=0, blur_radius=0)

        # Compute change stats for the composite vs original
        stats_raw = compute_change_stats(orig_arr, composite_raw, mask_resized)

        # Create comparison figure
        comp_fig_path = os.path.join(QA_DIR, f"comp_{fname.replace('.png', '.png')}")
        create_comparison_figure(orig_arr, output_resized, mask_resized, composite_raw, fname, comp_fig_path)

        # Visual assessment
        mad = stats_raw["mean_diff_unmasked"]
        pct = stats_raw["outside_change_pct"]

        if mad < 0.5 and pct < 0.5:
            boundary = "Clean - no visible boundary, seamless integration"
        elif mad < 2 and pct < 3:
            boundary = "Minor transition - slight softness at edges, acceptable"
        elif mad < 5 and pct < 10:
            boundary = "Noticeable boundary - visible edge artifacts"
        else:
            boundary = "Poor integration - harsh edge artifacts, visible seam"

        # Check hand coherence (inside mask, high change is expected for inpainted hand)
        hand_coherence = "Check if generated hand is anatomically correct and integrates with surrounding art"
        if stats_raw["inside_change_pct"] > 50:
            hand_coherence = "High change inside mask - hand was regenerated, assess quality"
        elif stats_raw["inside_change_pct"] < 10:
            hand_coherence = "Low change inside mask - minimal inpainting effect"

        print(f"\n  [{fname}] ({tc['type']})")
        print(f"    Composite outside-mask change: {stats_raw['outside_change_pct']}%")
        print(f"    Composite mean diff (unmasked): {stats_raw['mean_diff_unmasked']}")
        print(f"    Composite MSE: {stats_raw['mse']}")
        print(f"    Boundary: {boundary}")
        print(f"    Hand: {hand_coherence}")

        exp3_results.append({
            "filename": fname,
            "mask_type": tc["type"],
            "composite_stats": {
                "outside_change_pct": stats_raw["outside_change_pct"],
                "mean_diff_unmasked": stats_raw["mean_diff_unmasked"],
                "mse": stats_raw["mse"],
                "inside_change_pct": stats_raw["inside_change_pct"],
            },
            "boundary_assessment": boundary,
            "hand_assessment": hand_coherence,
        })

        # Save composite image
        Image.fromarray(composite_raw).save(os.path.join(QA_DIR, f"composite_{fname}"))

    # ================================================================
    # EXPERIMENT 4: Fallback mask risk analysis
    # ================================================================
    print(f"\n{'='*70}")
    print("EXPERIMENT 4: FALLBACK MASK RISK ANALYSIS")
    print("=" * 70)

    fallback_files = []
    mediapipe_files = []

    for fname in sorted(os.listdir(ORIGINAL_ROOT)):
        if not fname.endswith('.png'):
            continue
        mask_name = fname.replace(".png", "_inpaint_mask.png")
        mask_path = os.path.join(MASK_DIR, mask_name)
        if not os.path.exists(mask_path):
            continue
        mask_arr = load_mask(mask_path)
        if is_fallback_mask(mask_arr):
            fallback_files.append((fname, mask_arr))
        else:
            mediapipe_files.append((fname, mask_arr))

    print(f"\n  Total images: {len(fallback_files) + len(mediapipe_files)}")
    print(f"  Fallback masks: {len(fallback_files)}")
    print(f"  MediaPipe masks: {len(mediapipe_files)}")

    # Analyze fallback masks
    fallback_analysis = []
    hand_overlap_count = 0
    weapon_overlap_count = 0
    armor_overlap_count = 0
    background_overlap_count = 0
    multiple_overlap_count = 0

    # Fallback mask region: center-bottom roughly 45-85% height, 15-85% width
    for fname, mask_arr in fallback_files:
        orig_path = os.path.join(ORIGINAL_ROOT, fname)
        orig_arr = load_image(orig_path)

        h, w = orig_arr.shape[:2]
        mask_resized = cv2.resize(mask_arr, (w, h))
        mask_bin = mask_resized > 127

        # Define regions within the image
        # Hands are typically in the bottom half of the card
        hand_region = mask_bin[int(h * 0.45):int(h * 0.85), int(w * 0.15):int(w * 0.85)]

        # Weapon/equipment region (typically center-right or center-left, lower half)
        weapon_region_left = mask_bin[int(h * 0.3):int(h * 0.7), int(w * 0.1):int(w * 0.5)]
        weapon_region_right = mask_bin[int(h * 0.3):int(h * 0.7), int(w * 0.5):int(w * 0.9)]

        # Armor/clothing region
        armor_region = mask_bin[int(h * 0.2):int(h * 0.6):, :]

        # Background (top area)
        background_region = mask_bin[:int(h * 0.3), :]

        # Count overlaps
        hand_overlap = int(hand_region.sum())
        weapon_overlap = int((weapon_region_left.sum() + weapon_region_right.sum()))
        armor_overlap = int(armor_region.sum())
        background_overlap = int(background_region.sum())

        # Determine if mask plausibly targets a hand
        # A good hand mask should overlap with the bottom-center region
        total_white = int(mask_bin.sum())

        # Use HSV color analysis to estimate what's under the mask
        # Check for skin tone (hands), metal/weapon (shiny), fabric (armor)
        orig_hsv = cv2.cvtColor(orig_arr, cv2.COLOR_RGB2HSV)
        masked_hsv = orig_hsv[mask_bin]

        if len(masked_hsv) > 0:
            # Skin tone detection (HSV: H=0-30, S=30-120, V=50-255 for light skin)
            # Also H=330-360 for some skin tones
            skin_mask = ((masked_hsv[:, 0] < 30) | (masked_hsv[:, 0] > 330)) & \
                        (masked_hsv[:, 1] > 20) & (masked_hsv[:, 2] > 40)
            skin_pct = skin_mask.sum() / len(masked_hsv) * 100

            # Metal detection (high saturation, bright)
            metal_mask = (masked_hsv[:, 1] < 40) & (masked_hsv[:, 2] > 150)
            metal_pct = metal_mask.sum() / len(masked_hsv) * 100

            # Dark/dominant colors (likely armor or background)
            dark_pct = (masked_hsv[:, 2] < 80).sum() / len(masked_hsv) * 100
        else:
            skin_pct = 0
            metal_pct = 0
            dark_pct = 0

        # Categorize overlap
        overlaps_multi = []
        if hand_overlap > total_white * 0.3:
            overlaps_multi.append("hand_area")
        if weapon_overlap > total_white * 0.3:
            overlaps_multi.append("weapon_area")
        if armor_overlap > total_white * 0.2:
            overlaps_multi.append("armor_body")
        if background_overlap > total_white * 0.2:
            overlaps_multi.append("background")

        fallback_analysis.append({
            "filename": fname,
            "total_white": total_white,
            "hand_overlap_pct": round(hand_overlap / max(total_white, 1) * 100, 1),
            "weapon_overlap_pct": round(weapon_overlap / max(total_white, 1) * 100, 1),
            "armor_overlap_pct": round(armor_overlap / max(total_white, 1) * 100, 1),
            "background_overlap_pct": round(background_overlap / max(total_white, 1) * 100, 1),
            "skin_tone_pct": round(skin_pct, 1),
            "metal_pct": round(metal_pct, 1),
            "dark_pct": round(dark_pct, 1),
            "overlaps_categories": overlaps_multi,
            "multiple_categories": len(overlaps_multi) > 1,
        })

        if skin_pct > 15:
            hand_overlap_count += 1
        if metal_pct > 20:
            weapon_overlap_count += 1
        if armor_overlap > 0:
            armor_overlap_count += 1
        if background_overlap > 0:
            background_overlap_count += 1
        if len(overlaps_multi) > 1:
            multiple_overlap_count += 1

    print(f"\n  Fallback mask overlap analysis:")
    print(f"    Plausibly targeting hand (skin tone > 15%): {hand_overlap_count}/{len(fallback_files)} ({hand_overlap_count/len(fallback_files)*100:.1f}%)")
    print(f"    Overlapping weapon area (>30%): {weapon_overlap_count}/{len(fallback_files)} ({weapon_overlap_count/len(fallback_files)*100:.1f}%)")
    print(f"    Overlapping armor/body (>20%): {armor_overlap_count}/{len(fallback_files)} ({armor_overlap_count/len(fallback_files)*100:.1f}%)")
    print(f"    Overlapping background (>20%): {background_overlap_count}/{len(fallback_files)} ({background_overlap_count/len(fallback_files)*100:.1f}%)")
    print(f"    Overlapping multiple unrelated objects: {multiple_overlap_count}/{len(fallback_files)} ({multiple_overlap_count/len(fallback_files)*100:.1f}%)")

    # Show representative examples
    print(f"\n  Representative fallback mask examples:")
    for fa in sorted(fallback_analysis, key=lambda x: x["skin_tone_pct"], reverse=True)[:3]:
        print(f"    {fa['filename']}: skin={fa['skin_tone_pct']}%, metal={fa['metal_pct']}%, dark={fa['dark_pct']}%, overlaps={fa['overlaps_categories']}")
    print(f"    Worst cases (least likely hand):")
    for fa in sorted(fallback_analysis, key=lambda x: x["skin_tone_pct"])[:3]:
        print(f"    {fa['filename']}: skin={fa['skin_tone_pct']}%, metal={fa['metal_pct']}%, dark={fa['dark_pct']}%, overlaps={fa['overlaps_categories']}")

    # ================================================================
    # Save all results
    # ================================================================
    all_results = {
        "experiment2_existing_output": exp2_results,
        "experiment3_hard_composite": exp3_results,
        "experiment4_fallback_analysis": {
            "total_fallback_masks": len(fallback_files),
            "total_mediapipe_masks": len(mediapipe_files),
            "plausibly_targeting_hand": hand_overlap_count,
            "hand_percentage": round(hand_overlap_count / len(fallback_files) * 100, 1) if fallback_files else 0,
            "overlapping_weapon": weapon_overlap_count,
            "overlapping_armor": armor_overlap_count,
            "overlapping_background": background_overlap_count,
            "overlapping_multiple": multiple_overlap_count,
            "multiple_percentage": round(multiple_overlap_count / len(fallback_files) * 100, 1) if fallback_files else 0,
            "per_file_analysis": fallback_analysis,
        },
    }

    log_path = os.path.join(QA_LOGS_DIR, "experiments_2_3_4_results.json")
    with open(log_path, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\n{'='*70}")
    print(f"Results saved to: {log_path}")
    print(f"QA artifacts in: {QA_DIR}")


if __name__ == "__main__":
    main()

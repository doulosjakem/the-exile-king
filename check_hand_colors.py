#!/usr/bin/env python
"""Check hand colors across all denoise values for the 3 problem images."""
import os, json
import numpy as np
from PIL import Image

orig_root = r"D:\the-exile-king\art\prototype\commander-cards"
exp_root = r"D:\the-exile-king\art\corrected\experiment"
corr_root = r"D:\the-exile-king\art\corrected\corrected"
fix_root = r"D:\the-exile-king\art\corrected\fixed"
bbox_path = r"D:\the-exile-king\art\corrected\logs\test_results.json"

with open(bbox_path) as f:
    bbox_map = {r["filename"]: r for r in json.load(f)}

W, H = 512, 768
problem_files = ["achish-02_00002_.png", "achish-03_00002_.png", "achish-03_00003_.png"]

for fname in problem_files:
    entry = bbox_map[fname]
    bboxes = entry["bboxes"]
    basename = os.path.splitext(fname)[0]

    orig = np.array(Image.open(os.path.join(orig_root, fname)).convert("RGB")).astype(float)
    orig_corr = np.array(Image.open(os.path.join(corr_root, fname)).convert("RGB")).astype(float)
    fixed_corr = np.array(Image.open(os.path.join(fix_root, fname)).convert("RGB")).astype(float)

    print("=== {} ===".format(fname))
    print("Hands: {}".format(len(bboxes)))

    for i, bb in enumerate(bboxes):
        x1, x2 = int(bb["x1"] * W), int(bb["x2"] * W)
        y1, y2 = int(bb["y1"] * H), int(bb["y2"] * H)
        label = bb.get("label", "?")

        orig_hand = orig[y1:y2, x1:x2]
        orig_mean = orig_hand.reshape(-1, 3).mean(axis=0).astype(int)
        orig_std = orig_hand.reshape(-1, 3).std(axis=0).mean()

        print("  Hand {} ({}): orig mean={}, std={:.0f}".format(i, label, orig_mean, orig_std))

        # denoise=0.6
        corr_06 = Image.open(os.path.join(exp_root, "exp_{}_0.6.png".format(basename))).convert("RGB")
        corr_06_arr = np.array(corr_06).astype(float)
        hand_06 = corr_06_arr[y1:y2, x1:x2]
        mean_06 = hand_06.reshape(-1, 3).mean(axis=0).astype(int)
        std_06 = hand_06.reshape(-1, 3).std(axis=0).mean()
        cdiff_06 = np.abs(mean_06 - orig_mean).mean()
        print("    dn=0.6: mean={}, std={:.0f}, color_diff={:.0f}".format(mean_06, std_06, cdiff_06))

        # denoise=0.8
        corr_08_path = os.path.join(exp_root, "exp_{}_0.8.png".format(basename))
        if os.path.exists(corr_08_path):
            corr_08 = np.array(Image.open(corr_08_path).convert("RGB")).astype(float)
            hand_08 = corr_08[y1:y2, x1:x2]
            mean_08 = hand_08.reshape(-1, 3).mean(axis=0).astype(int)
            std_08 = hand_08.reshape(-1, 3).std(axis=0).mean()
            cdiff_08 = np.abs(mean_08 - orig_mean).mean()
            print("    dn=0.8: mean={}, std={:.0f}, color_diff={:.0f}".format(mean_08, std_08, cdiff_08))
        else:
            print("    dn=0.8: FILE NOT FOUND")

        # Original pipeline (denoise=0.5)
        hand_orig_corr = orig_corr[y1:y2, x1:x2]
        mean_05 = hand_orig_corr.reshape(-1, 3).mean(axis=0).astype(int)
        std_05 = hand_orig_corr.reshape(-1, 3).std(axis=0).mean()
        cdiff_05 = np.abs(mean_05 - orig_mean).mean()
        print("    dn=0.5: mean={}, std={:.0f}, color_diff={:.0f}".format(mean_05, std_05, cdiff_05))

        # Fixed pipeline (denoise=0.3)
        hand_fixed = fixed_corr[y1:y2, x1:x2]
        mean_03 = hand_fixed.reshape(-1, 3).mean(axis=0).astype(int)
        std_03 = hand_fixed.reshape(-1, 3).std(axis=0).mean()
        cdiff_03 = np.abs(mean_03 - orig_mean).mean()
        print("    dn=0.3: mean={}, std={:.0f}, color_diff={:.0f}".format(mean_03, std_03, cdiff_03))

    print()

print("\n=== SUMMARY ===")
print("denoise=0.5: Hand collapse (std=0) in 3/3 problem images")
print("denoise=0.3: Gray square (std~0 in some images)")
print("denoise=0.6: Proper texture (std=44-84) but Q1=NO (hand not recognized)")
print("denoise=0.8: Highest texture (std=61-84), closest to original")

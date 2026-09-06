import json
with open(r"D:\the-exile-king\art\corrected\experiment5\logs\experiment5_results.json") as f:
    results = json.load(f)
print(f"Number of results: {len(results)}")
for r in results:
    print(f"{r['filename']}: status={r['status']}")
    if r.get("stats_composite_1024"):
        s = r["stats_composite_1024"]
        print(f'  [1024] Composite: out={s["outside_change_pct"]}%, mad={s["mean_diff_unmasked"]}, mse={s["mse"]}, ring={s["outer_ring_mean_diff"]}')
    if r.get("stats_raw_1024"):
        s = r["stats_raw_1024"]
        print(f'  [1024] Raw: out={s["outside_change_pct"]}%, mad={s["mean_diff_unmasked"]}, mse={s["mse"]}')
    if r.get("stats_composite_512"):
        s = r["stats_composite_512"]
        print(f'  [512] Composite: out={s["outside_change_pct"]}%, mad={s["mean_diff_unmasked"]}, mse={s["mse"]}')
    if r.get("stats_existing"):
        s = r["stats_existing"]
        print(f'  [Existing] out={s["outside_change_pct"]}%, mad={s["mean_diff_unmasked"]}, mse={s["mse"]}')
    print()
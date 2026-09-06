import json

with open(r"D:\the-exile-king\art\corrected\experiment\logs\experiments_2_3_4_results.json") as f:
    data = json.load(f)

print("Experiment 2 (original vs existing output):")
for r in data["experiment2_existing_output"]:
    print(f'  {r["filename"]}: {r["mask_type"]}, outside_change={r["outside_change_pct"]}%, mse={r["mse"]}')

print()
print("Experiment 3 (hard composite):")
for r in data["experiment3_hard_composite"]:
    print(f'  {r["filename"]}: {r["mask_type"]}, outside_change={r["composite_stats"]["outside_change_pct"]}%, mse={r["composite_stats"]["mse"]}')
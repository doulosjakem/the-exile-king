# Handoff: Art Pipeline State

## Project
The Anointed Exile — board game with hand-painted bronze-age Levantine art style.
Model: DreamShaper XL Lightning in ComfyUI portable.
Review: Ollama minicpm-v:8b vision model.

## What's Done

### 1. Full Review Complete
- **788 unique images** reviewed across entire output folder
- **460 KEEP, 328 TRASH, 0 errors**
- Report: `D:\Jake\ComfyUI_windows_portable\ComfyUI\output\ComfyUI\annointed-exile\art_review_report.json`
- Review script: `D:\the-exile-king\review_art_ollama.py`

### 2. Generation Queue Ready
- **27 queue items** in `D:\the-exile-king\generation_queue.json`
- Covers: tiles (30), equipment (48), cards (72), UI (30), portraits (24)
- All items have `batch_size=1` (single images to avoid 6GB VRAM overflow)

### 3. Generation Script Ready
- `D:\the-exile-king\run_comfyui_generation.py` — standalone batch generator
- `D:\the-exile-king\run_item_cycle.py` — item-by-item generate+review cycle
- Both use portable ComfyUI Python: `D:\Jake\ComfyUI_windows_portable\python_embeded\python.exe`
- Checkpoint: `dreamshaperXL_sfwLightningDPMSDE.safetensors`

### 4. Prompt Fixes Applied
- Equipment prompts: removed "single person holding" → now "isolated single object centered on pure white background, clean cutout"
- Added negative prompts for equipment: `person, people, human, hands, fingers, body, figure, face, background, scenery, aged parchment, board game card art`
- Asset-type-aware positive/negative suffixes in generation script

## What's Left

### Generation Queue (27 items, ~162 images total)
Already generated in earlier runs:
- 10x grass tiles (hex_grass_00001-00010)
- 10x rock tiles (hex_rock_00001-00010)
- 10x sand tiles (hex_sand_00001-00010)
- 9x bronze-sword (00001-00009, last one with fixed prompt)
- 1x leather-shield, 1x spear, 1x sling, 1x bow, 1x camel
- Standees, portraits, cards, UI from earlier sessions

### Remaining to generate
Most equipment, all cards, all UI, all Amalekite portraits still need fresh generation with fixed prompts.

## Critical Constraint
**GTX 1060 6GB VRAM** — ComfyUI SDXL (~5GB) and Ollama vision (~5.5GB) CANNOT run simultaneously. Must alternate:
1. Start ComfyUI → generate batch → stop ComfyUI
2. Review with Ollama → fix prompts if needed
3. Repeat

## How to Continue

### Option A: Run item-by-item cycle
```powershell
python "D:\the-exile-king\run_item_cycle.py"
```
This auto-generates one queue item, stops ComfyUI, reviews all images, suggests prompt fixes, and moves to next item. Progress saved to `D:\the-exile-king\cycle_progress.json`.

### Option B: Manual batch control
```powershell
# 1. Start ComfyUI (visible window recommended for debugging)
D:\Jake\ComfyUI_windows_portable\python_embeded\python.exe -s ComfyUI\main.py --lowvram --windows-standalone-build -WorkingDirectory D:\Jake\ComfyUI_windows_portable

# 2. Generate a batch
python "D:\the-exile-king\run_comfyui_generation.py" --no-launch --items 3

# 3. Stop ComfyUI (close window or kill process)

# 4. Review specific batch
python "D:\the-exile-king\review_art_ollama.py" --output review.json
```

## Key Files
- `D:\the-exile-king\PROMPTS.md` — prompt reference
- `D:\the-exile-king\generation_queue.json` — what to generate
- `D:\the-exile-king\review_art_ollama.py` — review script with expected prompts
- `D:\the-exile-king\run_comfyui_generation.py` — generation runner
- `D:\the-exile-king\run_item_cycle.py` — full cycle
- `D:\the-exile-king\CYCLE_PROGRESS.md` — human-readable progress

## Known Issues
- Ollama times out when ComfyUI is loaded (VRAM conflict)
- Large batches (>1) can OOM on 6GB cards
- Some old outputs in root output/ need moving to proper subfolders
- `to_duplicates` folders got nested deeply from repeated dedupe runs

## Estimated Time Remaining
With batch_size=1, ~4 min per image (generation + startup/shutdown):
- ~120 images needing generation × 4 min = ~8 hours
- Plus review time after each batch

## User Preferences
- Wants asset-type-aware review (not just character art)
- Wants prompt comparison when possible
- Wants continuous automation, not manual steps
- Fine with it taking days
- Wants periodic status updates via CYCLE_PROGRESS.md

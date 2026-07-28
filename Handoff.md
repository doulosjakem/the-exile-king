# Handoff: Art Pipeline State

## Project
The Anointed Exile — printable board game prototype with hand-painted bronze-age Levantine art style.
Model: DreamShaper XL Lightning in ComfyUI portable.
Review: Ollama minicpm-v:8b vision model.

## Current Prototype Roster

### Commanders & Factions

| Commander | Faction | Color | Unit Types |
|---|---|---|---|
| David | David's Company | Purple | Swordsman, Spearman, Elite Slingers, Scouts, Shield Bearers |
| Jonathan | Jonathan's Followers | Blue | Loyal Guards, Elite Archers, Archers, Spearmen, Shield Bearers |
| Achish | Achish's Host (Lord of Gath) | Red | Giants, Swordsmen, Spearmen, Archers, Shield Bearers |
| Philistine Lord | Lord of Ekron's Host | Green | Chariots, Slingers, Swordsmen, Spearmen, Shield Bearers |

### Unit Discs Needed (2" diameter, colored border)

| Disc | Border Color | Notes |
|---|---|---|
| David | Purple | Commander portrait |
| Jonathan | Blue | Commander portrait |
| Achish | Red | Commander portrait |
| Philistine Lord | Green | Commander portrait |
| Swordsman | Purple/Blue/Red/Green | 4 faction variants |
| Spearman | Purple/Blue/Red/Green | 4 faction variants |
| Elite Slingers | Purple | David only |
| Slinger | Green | Ekron only |
| Scout | Purple | David only |
| Shield Bearer | Purple/Blue/Red/Green | 4 faction variants |
| Loyal Guard | Blue | Jonathan only |
| Elite Archer | Blue | Jonathan only |
| Archer | Blue/Red | 2 faction variants |
| Giant | Red | Achish only |
| Chariot | Green | Ekron only |

### Art Asset Counts

| Asset Type | Count | Status |
|---|---|---|
| Unit disc portraits | 25 unique designs | In queue |
| Commander card fronts | 40 unique (10 per commander) | In queue |
| Unit-type card fronts | 100 unique (5 types × 5 cards × 4 factions) | In queue |
| Card back | 1 shared design | In queue |
| Hex tiles | 30 (grass, rock, sand) | Mostly generated |
| Equipment icons | 48 | In queue |
| UI elements | 30 | In queue |

## What's Done

### 1. Prototype Roster Locked
- **GDD.md** updated: removed Amalekites/Saul's Kingdom from prototype scope; locked 4-commander roster.
- **Command cards** rewritten for 4 playable factions: David's Company, Jonathan's Followers, Achish's Host, Ekron's Host.
- **RULEBOOK.md** updated: 3 play modes (co-op, 1v1, 2v2), shared ruleset, prototype-specific deployment.
- **Command card files** updated: `command_cards/factions/*.md` and `command_cards/unit_types/*/*.md` aligned to prototype.

### 2. Art Generation Queue Rebuilt
- **216 queue items** in `D:\the-exile-king\generation_queue.json`
- **448 total images** to generate
- Covers: 25 unit discs, 40 commander cards, 100 unit cards, 1 card back, 30 hex tiles, 10 equipment, 4 UI elements
- Output subfolders: `prototype/unit-discs`, `prototype/commander-cards`, `prototype/unit-cards`, etc.

### 3. Prompt Pipeline Updated
- **56 new expected prompts** added to `review_art_ollama.py`
- `classify_asset_type` in `run_comfyui_generation.py` updated to recognize `card_front_*`, `card_back`, and new equipment/UI keys
- All prompt keys in the queue are resolved

### 4. Generation Scripts Ready
- `run_comfyui_generation.py` — standalone batch generator
- `review_art_ollama.py` — Ollama vision review
- Both use portable ComfyUI Python and DreamShaper XL Lightning checkpoint

## What's Left

### Art Generation
All prototype assets need generation. Total 448 images.

Already generated in earlier runs (old roster):
- 788 unique images reviewed, 460 KEEP / 328 TRASH
- These are in `box-art`, `player-units/amalekites`, etc. and are NOT part of the new prototype queue.

### Remaining to generate
- All unit discs (25 designs)
- All commander cards (40 designs)
- All unit-type cards (100 designs)
- Card back
- Hex tiles (30)
- Equipment (10)
- UI elements (4)

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

# 2. Generate a batch (limit to N items)
python "D:\the-exile-king\run_comfyui_generation.py" --no-launch --limit 5

# 3. Stop ComfyUI (close window or kill process)

# 4. Review specific batch
python "D:\the-exile-king\review_art_ollama.py" --output review.json
```

## Key Files
- `D:\the-exile-king\PROMPTS.md` — prompt reference
- `D:\the-exile-king\generation_queue.json` — 216 prototype queue items (448 images)
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
With batch_size=1, ~4 min per image:
- **448 prototype images × 4 min = ~30 hours of generation**
- Plus review time. At 5-10 items per session, expect ~10–20 sessions to complete.

## User Preferences
- Wants asset-type-aware review (not just character art)
- Wants prompt comparison when possible
- Wants continuous automation, not manual steps
- Fine with it taking days
- Wants periodic status updates via CYCLE_PROGRESS.md

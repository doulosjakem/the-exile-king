# Regeneration Round 2 Plan

## Goal
Regenerate all images scoring <= 3 from `full_review.json` with improved prompts, archive old low-scored outputs to a single folder, and prepare for a follow-up review round.

## Current State
- **2,213 images** reviewed by `review_art_ollama.py` (model: llava-phi3:3.8b)
- Score distribution:
  - **Score 1: 52** (TRASH) — mostly `modern object/text detected` + `not hand-painted`
  - **Score 2: 22** (TRASH) — `blurry/corrupted` or `prompt mismatch` paired with `not hand-painted`
  - **Score 3: 100** (99 KEEP, 1 TRASH) — `does not match expected prompt` only; hand-painted passes, no modern objects, no blur
  - **Score 4-5: 2,039** (KEEP)
- **Total regeneration candidates: 174 images**
- Outputs live under `D:\Jake\ComfyUI_windows_portable\ComfyUI\output\ComfyUI\annointed-exile`

## Key Finding
The 174 low-scored images break into two clusters:

| Cluster | Count | Prompt keys in review | Actual EXPECTED_PROMPTS keys | Folder |
|---|---|---|---|---|
| Box-art TRASH (scores 1-2) | ~74 | `null` | `box-art-board-of-war`, `box-art-covenant-at-the-cave` | `box-art\` |
| Box-art score-3 portraits | ~100 | `david`, `chieftain`, `abigail`, `asahel` | `box-art-round3-david-as-king`, `box-art-round3-david-at-adullam`, `box-art-round3-jonathan-and-david`, `box-art-round3-the-cave-of-engedi`, `box-art-round3-the-wounded-david`, `box-art-chieftains-challenge`, `box-art-abigail-intervenes`, `box-art-asahel-chases-abner`, plus variants | `box-art\` |

## Decisions
1. **Scope**: Regenerate ALL images with score <= 3 (174 images). Scores 4-5 remain untouched.
2. **Prompt fix strategy**:
   - **Box-art TRASH (1-2)**: Add them to the regen queue using their correct `EXPECTED_PROMPTS` keys. Strengthen negative prompt to explicitly block modern objects, text, 3D render, photograph, blur, and anime. Add positive reinforcement: `illuminated manuscript style, hand-painted historical illustration, aged parchment background, ink outlines with muted watercolor wash, muted earth tones`.
   - **Box-art score-3 portraits (david, chieftain, abigail, asahel)**: Simplify composition language to a single clear action. Add explicit NO lists for common failure modes (extra people, modern buildings, text/logo, fantasy elements). Keep 512x512, steps=4, cfg=3 unless batch fails.
3. **Prompt persistence**: Update `review_art_ollama.py` `EXPECTED_PROMPTS` dictionary in place. Do NOT create a separate overrides file.
4. **Queue structure**: Create `generation_queue_regen_round2.json` at repo root. Reuse existing queue entries where the prompt_key maps directly. Add new entries for the 8+ box-art scenes missing from `generation_queue.json`.
5. **Archive strategy**: Move all old low-scored files to a **single** archive folder:
   - `D:\Jake\ComfyUI_windows_portable\ComfyUI\output\ComfyUI\annointed-exile\_archive_regeneration_round2`
   - Preserve relative subfolder paths inside archive for traceability.
6. **Cleanup tool**: Create `archive_regeneration.py` to scan `full_review.json`, match output files by prefix, and move score <= 3 images to archive.
7. **ComfyUI execution**: Use existing `run_comfyui_generation.py` with `--fill-missing` so the script only generates enough new images to replace the archived ones.

## Execution Steps (for implementation agent)

### Step 1: Build regenerate list
- Parse `full_review.json` for all `score <= 3` images.
- Group by actual scene/prefix and output subfolder.
- Determine per-item `count` needed: = original count from manifest + number of archived bad images for that prefix, minus any existing good images still in place.

### Step 2: Improve prompts in `review_art_ollama.py`
- Edit the `EXPECTED_PROMPTS` dictionary.
- **Box-art keys**: tighten language and add explicit exclusions.
  Example for `box-art-abigail-intervenes`:
  > "game box art, painting in illuminated manuscript style, Abigail kneeling in dust before David, servant leading laden donkey behind her, David's men standing with weapons raised in background, her face lifted in supplication, his face softening, composition is low and dramatic, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine, NO modern clothing, NO modern buildings, NO text, NO logo, NO 3D render, NO photograph, NO anime, NO manga, NO cartoon, NO extra people, NO crowd"
- **Score-3 character portraits (abigail, asahel, chieftain, david)**: similar treatment, adding explicit DO/NOT lists.

### Step 3: Create `generation_queue_regen_round2.json`
- Include items for all 174 regenerations.
- For items already in `generation_queue.json`: keep same `output_subfolder` and `filename_prefix`, set `count` to fill missing.
- For box-art scenes missing from queue: add entries like:
  ```json
  {
    "id": "box-art-abigail-intervenes",
    "prompt_key": "box-art-abigail-intervenes",
    "count": 5,
    "steps": 4,
    "cfg": 3,
    "width": 512,
    "height": 512,
    "output_subfolder": "box-art",
    "filename_prefix": "abigail-intervenes"
  }
  ```

### Step 4: Archive old outputs (`archive_regeneration.py`)
- Script logic:
  1. Load `full_review.json` and collect all `{filename, score}` pairs where `score <= 3`.
  2. Scan `annointed-exile\<subfolder>` recursively for files matching those filenames.
  3. Move matched files to `_archive_regeneration_round2\<subfolder>\`.
  4. Also scan ComfyUI temp output `D:\Jake\ComfyUI_windows_portable\ComfyUI\output\` for matching prefixes and move those too.
  5. Print summary: total moved, per-scene counts.

### Step 5: Start ComfyUI and run generation
- If not already running:
  ```
  python run_comfyui_generation.py --queue generation_queue_regen_round2.json --manifest generation_manifest_regen_round2.json --no-shutdown
  ```
- If already running:
  ```
  python run_comfyui_generation.py --queue generation_queue_regen_round2.json --manifest generation_manifest_regen_round2.json --no-launch --no-shutdown
  ```

### Step 6: Follow-up review
- After batch completes, run:
  ```
  python review_art_ollama.py --base "D:\Jake\ComfyUI_windows_portable\ComfyUI\output\ComfyUI\annointed-exile" --output full_review_round2.json
  ```
- Target: 100% of regenerated images score >= 4. Iterate on prompt tweaks if any still score <= 3.

## Risks
- Box-art scenes may still score 3 if prompt is too complex for 4-step generation. Mitigation: if follow-up review shows batch failure, bump steps to 5-6 and cfg to 4 for those specific items and re-run.
- Archive script may miss manually renamed files. Mitigation: match by loose prefix patterns rather than exact filename.
- Some good (score 4-5) images share prefixes with bad ones. The archive script must only move the exact bad files, not the entire prefix folder.

## Files to Create / Modify
- **Modify**: `review_art_ollama.py` — improve ~15 EXPECTED_PROMPTS entries
- **Create**: `generation_queue_regen_round2.json`
- **Create**: `archive_regeneration.py`
- **Modify**: `CYCLE_PROGRESS.md` — reset state to generation batch

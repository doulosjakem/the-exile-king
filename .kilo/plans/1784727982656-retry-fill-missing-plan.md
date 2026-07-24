# Plan: Retry Logic + Fill-Missing-Images for Generation Pipeline

## Goal
Add error capturing (retry up to 3x per image) and a fill-missing-images mode to `run_comfyui_generation.py` so the pipeline reliably produces the expected number of images per queue item. Currently we regularly get only half the requested images per item due to timeouts and unhandled errors crashing the run.

## Current Failures
- `wait_for_prompt()` raises `RuntimeError` after 600s timeout — crashes the entire script
- No try/except around the per-image loop — one failure kills all remaining images for that item
- No tracking of which images succeeded vs failed within an item
- No ability to resume or fill in missing images after a crash

## Changes to `run_comfyui_generation.py`

### 1. Add `generate_one_image(item, seed, retries=3)` function (after `move_outputs`)
- Wraps `submit_workflow` + `wait_for_prompt` + `move_outputs` in try/except
- On failure, retries up to `retries` times (default 3) with a 3-second backoff
- Returns `moved_paths` list — empty on total failure
- Does not raise; errors are surfaced to the caller for reporting

### 2. Add `--retries` CLI argument (default 3, line ~301)
- Passes retry count to `generate_one_image`

### 3. Add `--fill-missing` CLI flag (line ~301)
- Scans each item's output directory for existing files matching the prefix
- For items with fewer files than `count`, generates the difference
- Uses fresh seeds for regenerated images
- Merges results into existing manifest (skips already-manifested item_ids)

### 4. Modify main loop (lines 337-350)
- Replace inline `submit_workflow` + `wait_for_prompt` + `move_outputs` with call to `generate_one_image`
- Track `failed_images` list per item for reporting
- Outer loop continues to next image on failure instead of crashing
- Prints per-item summary: success count, retry count, failures

### 5. Summary report at completion (after manifest write)
- Print total successes, failures, retries exhausted across all items
- On `--fill-missing`, report how many gaps were filled and what remains

## Verification
- Run `python run_comfyui_generation.py --help` to confirm new args appear
- Run with `--limit 3 --retries 1` against a small slice to sanity-check no crashes
- Manually verify `generate_one_image` catches `RuntimeError` from `wait_for_prompt`
- For `--fill-missing`, create a test shortfall and confirm it generates replacements without duplicating existing files
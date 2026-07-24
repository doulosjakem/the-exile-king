# Plan: Retry Logic + Fill-Missing-Images for Generation Pipeline

## Goal
Add error capturing (retry up to 3x per image) and a fill-missing-images mode to `run_comfyui_generation.py` so the pipeline reliably produces the expected number of images per queue item. Currently we regularly get only half the requested images per item due to timeouts and unhandled errors crashing the run.

## Current Failures
- `wait_for_prompt()` raises `RuntimeError` after 600s timeout — crashes the entire script
- No try/except around the per-image loop — one failure kills all remaining images for that item
- No tracking of which images succeeded vs failed within an item
- No ability to resume or fill in missing images after a crash

## Changes to `run_comfyui_generation.py`

### 1. Add `generate_one_image(item, seed, retries=3)` function
- Wraps `submit_workflow` + `wait_for_prompt` + `move_outputs` in try/except
- On failure, retries up to `retries` times (default 3) with a 3-second backoff
- Returns `(moved_paths, error)` tuple — empty `moved_paths` on total failure
- Does not crash the outer loop

### 2. Add `--retries` CLI argument (default 3)
- Passes retry count through to `generate_one_image`

### 3. Add `--fill-missing` CLI flag
- Scans each item's output directory for existing files matching the prefix
- For items with fewer files than `count`, generates the difference
- Uses fresh seeds for regenerated images
- Appends to the same manifest output file

### 4. Modify main loop
- Replace inline `submit_workflow` + `wait_for_prompt` + `move_outputs` with call to `generate_one_image`
- Track `failed_images` list per item for reporting
- Still processes all items even if individual images fail

### 5. Summary report at completion
- Print total successes, failures, and retries exhausted
- On `--fill-missing`, fill shortfalls and report what was fixed

## Verification
- Run `--help` to confirm new args appear
- Run with `--limit 3` against a small slice to verify retry logic works
- Check that the script no longer crashes on the first timeout
- Verify fill-missing correctly detects shortfalls and generates replacements
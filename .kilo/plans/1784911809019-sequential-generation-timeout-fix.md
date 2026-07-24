# Fix: Sequential Single-Image Generation (OOM + Timeout)

## Diagnosis

Two failure modes on GTX 1060 6GB:

1. **Timeout:** `run_cycle.py` `generation_phase()` (lines 463–474) submits all `count` workflows (e.g., 8 for one item) without waiting between submissions, then calls `wait_for_queue_empty()` for the entire batch. 8 images × ~94s each = ~752s, exceeding the 600s timeout → always fires.
2. **OOM root cause:** The queue flooding + timeout abort cycle causes ComfyUI to be stopped and restarted mid-batch, fragmenting VRAM. Also, `build_workflow()` currently reads `batch_size` from the item dict; if anyone passes `batch_size: 8`, ComfyUI tries to generate 8 images in one forward pass and OOMs immediately.

The user confirmed: **we CAN queue multiple workflows.** ComfyUI will process them one at a time. The hard constraint is: **no single workflow may have `batch_size > 1`.** Multiple sequential 1-image workflows are fine.

## Fix

### In `D:\the-exile-king\run_cycle.py` `generation_phase()` (lines 463–474):

- Import `wait_for_prompt` from `run_comfyui_generation`
- Replace the "submit all count workflows, then wait for queue empty" block with a per-image loop:
  `submit_workflow` → `wait_for_prompt(prompt_id)` → `move_outputs(batch_item)` → next image
- This removes the timeout cascade and eliminates queue flooding

### In `D:\the-exile-king\run_comfyui_generation.py` `build_workflow()` (line 139):

- Hardcode `"batch_size": 1` in the `EmptyLatentImage` dict — don't read it from the item
- Remove or ignore the `batch_size = item.get(...)` variable on line 107 so it can never leak in

### In `D:\the-exile-king\run_cycle.py` `build_workflow()` (line 123):

- `"batch_size": 1` is already hardcoded — leave it, but the OOM fix ensures this can never be overridden

### Invariant to enforce

Every workflow submitted to ComfyUI has `batch_size: 1` in its `EmptyLatentImage`. Multiple workflows may be queued, but each generates exactly 1 image.

## Steps

1. **Edit `D:\the-exile-king\run_cycle.py`**:
   - Add `wait_for_prompt` to the import from `run_comfyui_generation`
   - In `generation_phase()`, replace lines 463–474 with the per-image submit→wait→move loop

2. **Edit `D:\the-exile-king\run_comfyui_generation.py`**:
   - In `build_workflow()`, change `"batch_size": 1` to be a literal (not a variable), or leave line 107's variable unused and keep line 139 hardcoded
   - Remove `batch_size` from line 107 to prevent future misuse

3. **Verify**:
   - Run `python run_cycle.py --limit 1 --items 1` and confirm the first queue item (8 images) completes without timeout
   - Confirm no OOM by checking ComfyUI logs / nvidia-smi during the run

## Risk

- Low. Per-image wait is already proven in `run_comfyui_generation.py` (~94s/image, no timeout).
- Hardcoding `batch_size: 1` prevents future misconfiguration from reintroducing OOM.

## Open Decisions

- None. Ready to implement.

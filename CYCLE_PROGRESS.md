# Generation + Review Cycle Progress

**Started:** 2026-07-24 06:13
**Mode:** Generation-only batch, ComfyUI stays running entire time
**Current GPU:** GTX 1060 6GB
**ComfyUI flags:** `--disable-auto-launch --lowvram --reserve-vram 2.0 --windows-standalone-build`
**Batch size:** 1 image at a time, sequential
**Review:** deferred to separate pass after generation completes

## Approach Change

**Problem:** Starting/stopping ComfyUI for each of 152 items caused queue failures after the first image.
**Fix:** ComfyUI starts once at the beginning, stays running for all generation, stops once at the end.
**Why:** Eliminates repeated startup/shutdown overhead and VRAM/state thrashing.

## Current Status

**Cycle state:** Running generation-only batch
**Current item:** equipment-bronze-sword (skipped - 9 files exist)
**Current queue index:** 0 / 152
**ComfyUI server:** managed by cycle (single instance for entire batch)
**Ollama server:** DOWN
**Cycle process PID:** see background process

## Last updated

2026-07-24 06:13:00

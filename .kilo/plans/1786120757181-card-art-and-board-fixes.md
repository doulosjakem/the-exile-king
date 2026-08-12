# Plan: Fix Card Art and Board Rendering

## Problem
- `prototype/exile_king_printable_v2.pdf` looks awful: tiny centered square images with huge empty margins, ugly board, text separated from art.
- Root cause: art area is 742×300 px (ultra-wide) but source art is square → image gets centered with ~221 px empty space on each side.
- Board: hex radius is `hex_size * 0.5` but cell spacing is `hex_size`, making hexes half the cell size with massive gaps.
- Art duplication: non-commander cards get the same image on both halves.

## Goal
Cards look like actual game cards: art fills the space, text is readable, split layout is clean. Board looks like a map, not a checkerboard.

## Decisions

### Card Layout: KEEP split, but fix proportions
- Each half gets a **centered square-ish art box** (~500×280 px) instead of full-width ultra-wide box.
- Text overlays the **bottom 140 px of the art** with a semi-transparent dark background (alpha 190/255 ≈ 0.75).
- Gold initiative badge + "TOP/BOTTOM ACTION" label on the dark overlay.
- Faction label: small colored bar at very bottom of card.
- If top and bottom art are the same file (duplicate fallback), that's acceptable — it means the card only has one illustration.

### Board Rendering: Fix hex math, kill tile fallback
- If `playable_board` art exists: paste full-page, overlay hex outlines + coordinates.
- If no board art: render a **plain parchment board** with subtle hex grid lines and coordinate labels. NO grass/rock checkerboard tiles.
- Fix hex radius: use `hex_size * 1.0` so hexagons match their grid cells.

### Art Mapping: Stop blind duplication
- `map_cards_to_art()` should assign art intentionally:
  - Commander ability cards: commander portrait on top, ability illustration on bottom.
  - All other cards: same art on both halves is fine (only one illustration exists).
  - Remove the fallback loop that blindly copies `get_art(pk)` to both halves.

## Implementation Tasks

### Task 1: Fix `render_card()` art sizing
- Change art area from full-width 742×300 to centered ~500×280 per half.
- Compute `paste_x = art_x + (art_w - art.width) // 2` to center square art in the wider box.
- Keep the dark semi-transparent text overlay but position it over the bottom of the art area.

### Task 2: Fix `render_hex_board()` hex radius
- Change `hex_size * 0.5` to `hex_size * 1.0` in corner math.
- Remove tiled hex fallback entirely. If no `playable_board` art, draw plain parchment + hex outlines + labels.

### Task 3: Simplify `map_cards_to_art()`
- Remove the generic fallback loop.
- Commander ability cards: explicit top/bottom assignment.
- All other cards: single art source assigned to both halves.

### Task 4: Rebuild and verify
- Run `python build_printable_prototype.py --scope mvp --output prototype/exile_king_printable_v2.pdf`
- Check: 0 "ART PENDING", 17 pages, art fills space, board looks like a map.

## Out of Scope
- Double-sided PDF / card backs
- New art generation
- Changing card dimensions from poker size (2.5" × 3.5")

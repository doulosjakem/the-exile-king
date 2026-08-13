# Plan: Card Polish, Disc Masking, Rules Typography, and Playable Board

## Context
The printable prototype PDF is functional, but several visual/UX issues remain. The user also wants a real playable board map, not a schematic hex grid.

## Decisions
- **Single initiative location**: Top-left gold badge only. Remove initiative from A/B action bars.
- **Disc images**: Mask art to the unit disc circle so nothing bleeds outside the token.
- **Rules page**: Larger fonts and tighter vertical usage to fill the page better.
- **Playable board**: Replace the schematic hex-grid renderer with an actual composed map image that has terrain, labels, and grid overlay.

## Tasks

### Task 1: Remove duplicate initiative from A/B action bars
- **File**: `build_printable_prototype.py`
- **Change**: In `render_card()`, remove the initiative text drawn at the right side of both A and B action label bars. Keep the top-left initiative badge unchanged.
- **Validation**: Rebuild PDF and confirm A/B labels show only "A" / "B", with no initiative numbers in the bottom block.

### Task 2: Mask unit disc art inside the circle
- **File**: `build_printable_prototype.py`
- **Change**: In `render_unit_disc()`, after pasting art, apply a circular mask so image pixels outside the inner disc radius are transparent. Use the existing RGBA canvas.
- **Validation**: Rebuild PDF and verify disc images do not extend beyond the disc border.

### Task 3: Increase rules reference page font sizes
- **File**: `build_printable_prototype.py`
- **Change**: In `render_rules_reference()`, bump heading and body fonts and reduce excess spacing so content fills the page more densely.
  - Main title: larger
  - Section headers: larger bold
  - Body bullets: larger
- **Validation**: Rebuild PDF and confirm rules page uses larger text and remains readable.

### Task 4: Replace schematic board with a real playable hex map
- **File**: `build_printable_prototype.py`
- **Change**: Replace `render_hex_board()` with a composed 8×8 hex map renderer:
  1. Accept a `board_art` image or render a parchment background.
  2. Draw an 8×8 offset hex grid with consistent sizing.
  3. Overlay subtle terrain tints or tile textures per hex (if art exists), with hex outlines and coordinate labels.
  4. Remove the current tiled-checkerboard fallback.
- **Validation**: Rebuild PDF and confirm the board page reads as a tactical map rather than a schematic.

## Rollout Order
1. Task 1
2. Task 2
3. Task 3
4. Task 4

## Out of Scope
- Double-sided PDF / card backs
- New art generation
- Changing card dimensions

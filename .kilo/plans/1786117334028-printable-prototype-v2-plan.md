# Printable Prototype V2 Plan

## Current State
- `build_printable_prototype.py` builds a 17-page MVP PDF (81 cards, 25 unit discs) from card `.md` files + curated art in `art/prototype/`
- All 81 cards currently map to art (0 "ART PENDING" placeholders after last session's fixes)
- Card text is small: title 16px, body 11px, labels 10px (at 300dpi scale)
- Cards show both Top and Bottom actions, but there is no clear visual divider between them in the bottom text panel
- The 8×8 hex board renders as a flat alternating grass/rock checkerboard with coordinate labels — visually boring, not a "playable map"
- `art/prototype/` has 194 curated PNGs: commander cards (120 variants), unit cards (25), unit discs (25), hex tiles (30), UI (10), card backs (1), equipment (10)
- 9 commander ability cards currently reuse commander portrait art instead of having unique ability illustrations:
  - Battle Cry, Tactical Assessment, Last Resort, Flanking Maneuver, Siege Engineer
  - Shepherd's Call, Jonathan's Charge, Ekron's Decree, Philistine Might

## Goal
1. Make cards readable: larger text, clear top/bottom visual separation
2. Replace the flat hex checkerboard with a composed playable map image
3. Generate missing/improved art: unique ability card art + playable board

---

## Task 1: Card Rendering Improvements (build_printable_prototype.py)

### 1a. Increase text sizes
Current sizes at 300dpi:
- `font_title = 16px` → increase to `20px`
- `font_body = 11px` → increase to `14px`
- `font_label = 10px` → increase to `12px`
- `font_init = 18px` → keep as is (badges are fine)

### 1b. Add clear top/bottom divider
After rendering the "Top Action" text block, draw a horizontal rule (1px dark ink line with small margin) before the "Bottom Action" label. This visually splits the text panel into two halves.

### 1c. Adjust layout spacing
- Increase `body_y` offset so the larger title doesn't crowd the top of the text panel
- Verify bottom text doesn't overflow card bounds; if it does, reduce art area from 65% to 60% to give more room to text

### Validation
- Build PDF with `--scope mvp`
- Visually inspect: title readable at arm's length, body text legible, clear line between top and bottom actions
- Confirm 0 "ART PENDING" placeholders

---

## Task 2: Playable Board Art Generation

### Problem
The current `render_hex_board()` tiles individual flat hex tiles. This produces a sterile checkerboard, not a map you'd want to play on.

### Solution
Generate a **single composed playable board image** (8×8 hex grid rendered as a tactical map on aged parchment) and use it as the board background, then overlay hex coordinates/grid lines on top.

### Approach
1. **Add a new prompt key** `playable_board` to the generation pipeline
2. **Add a queue item** in `generation_queue.json` for the playable board:
   - `id`: `playable-board`
   - `prompt_key`: `playable_board`
   - `count`: 5 (generate 5 variants for review)
   - `width`: 2550, `height`: 3300 (US Letter at 300dpi, matching `PAGE_W`/`PAGE_H`)
   - `output_subfolder`: `prototype/board`
   - `filename_prefix`: `playable-board`

3. **Add the prompt** to `ART_GENERATION_GUIDE.md` and `PROMPTS.md`:
   ```
   top-down tactical battlefield map on aged parchment, 8x8 hex grid visible as subtle hexagon outlines, 
   bronze age Levantine terrain: dry grass plains, rocky outcrops, sandy patches, scattered boulders and 
   low shrubs, hand-painted illuminated manuscript style, ink outlines with muted watercolor wash in 
   ochre umber faded crimson and sage green, board game playable map, family friendly, 
   NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine
   ```

4. **Update `render_hex_board()`** in `build_printable_prototype.py`:
   - If `playable_board` art exists, paste it as the full-page background
   - Overlay subtle hex grid lines and coordinate labels on top
   - Fall back to current tiled hex rendering if no board art is available

### Alternative (if single-image generation fails)
Generate **terrain feature tiles** (rocks, bushes, ruins, paths) as PNGs with transparent backgrounds, then compose them onto the hex tiles during PDF build. This requires more queue items but gives more control.

### Validation
- Generate board art via ComfyUI
- Review variants, pick best KEEP
- Build PDF, verify board looks like a playable map, not a checkerboard

---

## Task 3: Missing Card Art Generation

### Current gaps
9 ability cards share commander portrait art instead of having unique tactical illustrations:
- `battle-cry`, `tactical-assessment`, `last-resort`, `flanking-maneuver`, `siege-engineer`
- `shepherds-call`, `jonathans-charge`, `ekrons-decree`, `philistine-might`

### Solution
Add these 9 prompt keys to the generation queue with unique tactical-scene prompts.

### Queue items to add
For each ability, add an entry to `generation_queue.json`:
- `id`: e.g., `ability-battle-cry`
- `prompt_key`: e.g., `battle-cry`
- `count`: 5
- `width`: 512, `height`: 768 (card art dimensions)
- `output_subfolder`: `prototype/unit-cards`
- `filename_prefix`: e.g., `battle-cry`

### Prompts to add (tactical manuscript style, NOT portraits)
| Prompt Key | Prompt Skeleton |
|---|---|
| `battle-cry` | `scene in illuminated manuscript style, bronze age Levantine warriors raising weapons and shouting, dust and motion, aged parchment background, ink outlines with muted watercolor wash in ochre and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European` |
| `tactical-assessment` | `scene in illuminated manuscript style, bronze age Levantine commander studying the battlefield from a rocky outcrop, hand raised in thought, warriors waiting below, aged parchment background, ink outlines with muted watercolor wash in umber and ochre, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European` |
| `last-resort` | `scene in illuminated manuscript style, bronze age Levantine warriors in desperate defensive position, shields locked, faces determined against overwhelming odds, aged parchment background, ink outlines with muted watercolor wash in faded crimson and umber, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European` |
| `flanking-maneuver` | `scene in illuminated manuscript style, bronze age Levantine soldiers moving through rocky terrain to outflank the enemy, motion lines, dust, aged parchment background, ink outlines with muted watercolor wash in ochre and faded indigo, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European` |
| `siege-engineer` | `scene in illuminated manuscript style, bronze age Levantine engineers constructing a siege ramp or battering ram, wooden beams, ropes, earthworks, aged parchment background, ink outlines with muted watercolor wash in umber and ochre, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European` |
| `shepherds-call` | `scene in illuminated manuscript style, young bronze age Levantine commander David standing on a hillside raising a shepherd's staff, small band of warriors gathering below, aged parchment background, ink outlines with muted watercolor wash in ochre and faded gold, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European` |
| `jonathans-charge` | `scene in illuminated manuscript style, bronze age Levantine warrior Jonathan leading a bold charge down a rocky slope, armor gleaming, spear raised, aged parchment background, ink outlines with muted watercolor wash in ochre and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European` |
| `ekrons-decree` | `scene in illuminated manuscript style, bronze age Levantine Philistine lord seated on a folding stool in a field tent, issuing commands to spearmen, warm lamplight, aged parchment background, ink outlines with muted watercolor wash in umber and amber, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European` |
| `philistine-might` | `scene in illuminated manuscript style, bronze age Levantine Philistine champion standing dominant among enemies, large figure, spear and shield, aged parchment background, ink outlines with muted watercolor wash in faded crimson and umber, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European` |

### Generation settings
- 512×768, steps 4, CFG 3, batch 5 per prompt
- Total: 9 prompts × 5 = 45 images
- Use `run_comfyui_generation.py` with updated queue

### Post-generation
- Run review pipeline (`review_art_ollama.py`) or manual review
- Curate best 1 per prompt key into `art/prototype/unit-cards/`
- Rebuild PDF and verify each ability card now shows unique art

---

## Task 4: Art Curation & Rebuild

After generation completes:
1. Run `review_art_ollama.py` on new images (or manual review if Ollama unavailable)
2. Copy KEEP images to `art/prototype/` preserving folder structure
3. Run `python build_printable_prototype.py --scope mvp --output prototype/exile_king_printable.pdf`
4. Verify:
   - 0 "ART PENDING" placeholders
   - All text is larger and readable
   - Cards have clear top/bottom separation
   - Board looks like a playable map

---

## Execution Order
1. **Task 1** (card rendering) — immediate, no art generation needed, just script edits
2. **Task 2** (playable board) — highest art priority, run ComfyUI generation
3. **Task 3** (missing card art) — second art priority, run after board generation
4. **Task 4** (curation + rebuild) — final step after all art is generated

## Risks
- ComfyUI generation is slow (~hours for 50+ images); may need to run overnight
- DreamShaper may drift from bronze-age style; era-lock prompts are critical
- Single composed board image may not tile well; fallback is better hex tiles or board background + grid overlay
- Card text increase may cause overflow on long ability texts; need to test and adjust art height or font size

## Out of Scope
- Full 6-faction prototype (this plan covers MVP 4 factions only)
- Unity implementation
- Mechanical balance changes

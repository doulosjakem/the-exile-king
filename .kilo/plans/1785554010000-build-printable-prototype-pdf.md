# Plan: Build Printable Prototype PDF Generator

## Objective
Create `build_printable_prototype.py` — a Python script that generates a print-and-play PDF
containing all physical game components for The Exile King: command cards, unit discs,
hex grid board, tokens, and a rules reference sheet.

## Key Facts

### Art Assets (source: `D:\Jake\ComfyUI_windows_portable\ComfyUI\output\ComfyUI\annointed-exile`)
| Type | Queue Items | Generated | Status |
|------|------------|-----------|--------|
| Commander cards | 40 (4 cmdrs × 10) | 1 | **Critical gap — 39 missing (queued for round 2)** |
| Unit cards | 100 | 56 | Partial (44 missing for round 2) |
| Unit discs | 25 | 93 (multi-variant) | Complete |
| Hex tiles | 30 | 29 | Near-complete |
| UI/tokens | 10 | 20 (multi-variant) | Complete |
| Card back | 1 | 2 | Complete |
| Equipment | 10 | 58 (multi-variant) | Complete |
| **Total** | 216 items | | **1,767 clean images** synced to Drive |

**Art review:** Currently running — 681/3,399 images reviewed as of last check. Ollama is now
operational (review is actively progressing, unlike the previous failed attempt).
Review report will be produced at completion: `art_review_report.json`

### Card Definitions
- 52 `.md` files in `command_cards/unit_types/**/*.md` across multiple factions
- Each file defines: card name, top/bottom actions, initiative, activations, unit stats
- `COMMAND_CARD_AUDIT.md` cross-references all card text (known issue: faction file drift)
- Card .md files include both formation cards (unique) and shared universal cards (Battle Cry, etc.)

### Art-to-Card Mapping
- `generation_queue.json` maps `id` → `prompt_key` → `filename_prefix` → `output_subfolder`
- Unit cards: queue ID like `unit-card-swordsmen-advance-01` maps directly to card text
- Commander cards: queue ID like `commander-card-david-01` (numbered, no card name) — needs order-based mapping to .md file
- Art filenames: `{filename_prefix}_{index:05d}_.png`

### Tech Stack Available
- Python 3.11.0, Pillow 12.3.0 (PIL), no reportlab/fpdf installed
- Ollama installed at `C:\Users\keath\AppData\Local\Programs\Ollama\ollama.exe`
- ComfyUI at `D:\Jake\ComfyUI_windows_portable\ComfyUI` (needs GPU for generation)
- Windows system fonts available (Arial, Times New Roman, etc.)

---

## Workflow (Parallel Execution)

The PDF generator can be built NOW while art review + generation continue in parallel.
Timeline:

1. **Phase 0 (current):** Art review running (681/3,399) — let it finish
2. **Phase 1 (can start now):** Build `build_printable_prototype.py` script — no art needed
   - Card text parser (reads .md files)
   - Layout engine (PIL card/disc/token/board renderers)
   - PDF assembly
   - CLI + options
   - Script runs offline — works with whatever images exist at execution time
3. **Phase 2 (next art gen round):** Queue + generate missing commander cards (39) + unit cards (44)
4. **Phase 3 (final):** Run `build_printable_prototype.py` with full reviewed art set
   - Review results (keep/trash) inform which images to use
   - All 90 target art pieces available
   - Single command produces final printable PDF

## Dependencies (before final PDF output)

### D1: Art Review (IN PROGRESS — 681/3,399)
**Why:** Need keep/trash classification to select approved images for the PDF.
**Status:** Ollama is running, review is actively processing. Will complete and produce
updated `art_review_report.json`.
**Action:** Wait for completion. Then parse report for "keep" classifications.
**Fallback:** Script accepts `--unreviewed-ok` to use all non-review-dir images.

### D2: Generate Missing Commander Card Art (Deferred to Round 2)
**Why:** Only 1 of 40 commander cards generated — PDF will look sparse without the rest.
**Status:** 39 commander cards + 44 unit cards will be queued for the next generation round.
**Action:** After review completes, update generation_queue.json with missing items,
then run `python run_comfyui_generation.py --fill-missing`.
**Fallback:** Generator script produces PDF with whatever art exists; missing cards
show placeholder "ART PENDING" instead of crashing.

### D3: Card Naming Drift (Non-blocking)
**Why:** COMMAND_CARD_AUDIT.md documents conflicts between `command_cards/unit_types/*.md` (card names like "Shepherd's Advance") and `command_cards/factions/*.md` (card names like "Swordsmen Advance").
**Decision:** Use `command_cards/unit_types/` as canonical source (more detailed). Note conflicts in output.
**Action:** Document known conflicts in the PDF generator output log. Address inconsistencies
incrementally — not a blocker for initial prototype build.

---

## Implementation Plan

### Step 1: Build Art Inventory + Card Mapping
Create a JSON mapping file (`prototype/card_art_mapping.json`) that maps:
- Each card (faction, unit type, card name) → art image file path
- Each unit disc (faction, unit name) → disc art image path
- Card back → card-back image path
- Tokens → UI image paths
- Review status: keep / trash / unreviewed (from `art_review_report.json` when available)

Generated by:
1. Parse `generation_queue.json` for `id` → `filename_prefix` → `prompt_key` mapping
2. Scan ComfyUI output `prototype/` directory for actual generated images
3. Cross-reference with card `.md` files for card names
4. For commander cards: map queue order (david-01 → 1st card in DAVID.md, david-02 → 2nd, etc.)
5. If `art_review_report.json` exists, filter to "keep" images only; if not, use all
6. Output: `card_art_mapping.json` with `{card_name: image_path}` for approved images

### Step 2: Card Template Module
Create `render_card(page, x, y, card_data, art_image, template)` function:
- Card size: 2.5" × 3.5" = 750 × 1050 px @ 300 DPI
- Layout:
  - **Art area**: top 65% of card (525 px), image fills this area
  - **Text panel**: bottom 35% (375 px), parchment-colored background
  - **Top-left corner**: Initiative number (small circle badge, 72px)
  - **Bottom-right corner**: Initiative number for bottom action
  - **Top of text panel**: Card name (bold, centered)
  - **Upper text panel**: Top action description
  - **Lower text panel**: Bottom action description
  - **Bottom edge**: Unit type + faction (small text)
- Font: Arial Bold for headers, Arial Regular for body
- Text wrapping for action descriptions

### Step 3: Unit Disc Sheet Module
Create function to render 2" diameter unit discs:
- Disc size: 2" = 600 px @ 300 DPI
- Colored border by faction:
  - David's Company: teal (#008080)
  - Jonathan's Followers: gold (#D4AF37)
  - Achish's Host: red (#DC143C)
  - Philistine Lord: red (#DC143C)
  - Saul's Kingdom: purple (#800080) [if included]
- Center: unit name + stats (Range/Attack/Defense/Health/Move)
- Multiple discs per page (6-8 per Letter page)
- Include cut lines (dotted) between discs

### Step 4: Hex Grid Board Module
Create an 8×8 hex grid board:
- Use hex tile art from `prototype/hex-tiles/` (30 tiles generated)
- Arrange in 8×8 grid
- Hex size: ~0.75" flat-to-flat (fits 8×8 on ~6"×6" area on Letter page)
- Include coordinate labels (A-H, 1-8)
- Print at actual size — may span 2 pages if too large

### Step 5: Token/Marker Sheet Module
Render circular tokens for:
- Activation tokens (used/not-used indicators)
- Commander aura markers
- Lost pile markers
- HP bar segments (from `prototype/ui/` art)
- Use UI art where available, fallback to simple geometric shapes
- 1" diameter tokens, 8-12 per page

### Step 6: Card Back Sheet Module
- Use `command-card-back` art image (reviewed keep only)
- Tile 6 copies per page (2.5" × 3.5" cards)
- All identical

### Step 7: Rules Reference Sheet
- Extract key rules from GDD.md + printable-co-op-prototype.md
- Sections: Setup, Turn Structure, Combat, Card Resolution, Deck Building, Victory/Defeat
- Compact layout with tables for unit stats
- Print on 1-2 pages

### Step 8: PDF Assembly
```python
# Each page is a PIL Image (2550×3300 px for US Letter @ 300 DPI)
pages = []
pages.append(make_cover_page())
pages.append(make_rules_page())
pages.extend(make_card_sheets(cards, mapping))  # ~6-8 cards per page
pages.extend(make_disc_sheets(units, mapping))  # ~6-8 discs per page
pages.extend(make_token_sheets(tokens))
pages.extend(make_hex_grid_board())
pages.append(make_card_back_sheet())
pages.append(make_reference_sheet())

# Combine into multi-page PDF
pages[0].save("printable_prototype.pdf", "PDF", save_all=True, append_images=pages[1:])
```

### Step 8: CLI + Options
```bash
python build_printable_prototype.py
  --output PATH              # output PDF path
  --art-dir PATH             # ComfyUI output directory
  --queue PATH               # generation_queue.json path
  --mapping PATH             # card_art_mapping.json path (auto-generate if missing)
  --review-report PATH       # art_review_report.json (use keep classifications)
  --dpi 300                  # output DPI
  --faction FACTION          # limit to specific faction(s)
  --scope mvp|full           # MVP = 4 factions, full = all factions
```

---

## MVP Scope (Print & Play Prototype)

### Cards (target: ~40 cards per page set)
1. **David** (commander) — Shepherd's Call, Wilderness Rally, Battle Cry, Tactical Assessment, Last Resort, Flanking Maneuver, Siege Engineer (7 cards)
2. **Swordsman** — Shepherd's Advance, Shepherd's Formation, Battle Cry, Tactical Assessment, Last Resort, Flanking Maneuver, Siege Engineer (7 cards)
3. **Spearman** — Shepherd's Wall, Shepherd's Screen, + 5 shared (7 cards)
4. **Slinger** — Shepherd's Strike, Stone Barrage, + 5 shared (7 cards)
5. **Archer** — Shepherd's Volley, Shepherd's Mark, + 5 shared (7 cards)
6. **Scout** — Wilderness Eye, Wilderness Ambush, + 5 shared (7 cards)
7. **Shield Bearer** — Shepherd's Shield, Wilderness Advance, + 5 shared (7 cards)
8. **Jonathan** (commander) — Jonathan's Charge, + 5 shared (6 cards)
9. **Loyal Guard** — Covenant Guard, + 5 shared (6 cards)
10. **Elite Archer** — Benjamin's Arrow, True Aim, + 5 shared (7 cards)
11. **Achish** (commander) — Philistine Might, + 5 shared (6 cards)
12. **Chariot** — Chariot Charge, Breakthrough, Hit and Run, + 5 shared (8 cards)

**Total:** ~78 card designs across MVP factions

### Unit Discs (~25 unique)
- 4 commanders + 11 unique unit types (Swordsman, Spearman, Slinger, Archer, Scout, Shield Bearer, Loyal Guard, Elite Archer, Heavy Infantry, Champion)
- Faction variants where applicable

### Board
- 8×8 hex grid (assembled from hex tiles)

### Tokens
- Activation markers (used/available)
- Commander aura markers (4 colors)
- Lost pile markers
- HP/shield tokens

---

## Build Order (Parallel-Friendly)

**Can build NOW (no art dependencies):**
1. Step 1: Card text parser — reads .md files, extracts card name/Top/Bottom/Initiative
2. Step 2: Card template renderer — PIL function to draw card frames + text
3. Step 3: Disc sheet module — PIL function for unit disc layout + colored borders
4. Step 5: Token/marker sheet module — uses simple geometric shapes (no art needed)
5. Step 7: Rules reference sheet — text-only, extracts from GDD.md
6. Step 8: PDF assembly — PIL multi-page save logic
7. CLI + options — `--unreviewed-ok` flag for using all images
8. Script tested with placeholder art (gray boxes) to verify layout correctness

**Depends on art review/generation completing:**
1. Step 1 uses `art_review_report.json` to filter keep/trash (falls back to `--unreviewed-ok`)
2. Step 3: Unit disc art from `prototype/unit-discs/` (already 93 images available)
3. Step 4: Hex grid board uses `prototype/hex-tiles/` (already 29 images available)
4. Step 6: Card back sheet uses `prototype/card-backs/` (already 2 images available)
5. Final PDF run with all approved art + missing cards generated in round 2

**Summary:** Script skeleton + layout engine built in parallel with art review. Final PDF
generated after review completes + missing commander/unit cards are generated in round 2.

---

## File Structure
```
build_printable_prototype.py       # Main script (create at workspace root)
prototype/
  card_art_mapping.json            # Auto-generated card→art mapping
  printable_prototype.pdf          # Output
  templates/                       # Generated card template reference
    card_template.png              # Reference template
    disc_template.png              # Reference template
```

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Ollama review running | ✅ In progress (681/3,399) — no action needed |
| Missing commander card art (39/40) | Queued for round 2 — generator handles gracefully with placeholders |
| PIL text rendering limitations | Pre-render card frames as template images, paste text as overlay |
| Font availability | Bundle a TTF font (e.g., Lora for serif headings) in project |
| Card naming conflicts between .md files | Use unit_types/ as canonical source, document conflicts |
| Hex grid too large for one page | Tile across 2 pages or print at 50% scale |
| Large PDF file size | Use JPEG compression for art images in PDF (PIL supports quality parameter) |
| reportlab/fpdf not installed | PIL supports multi-page PDFs natively — no extra deps needed |

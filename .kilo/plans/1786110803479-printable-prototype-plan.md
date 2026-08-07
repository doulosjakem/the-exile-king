# Printable Prototype Plan — The Exile King

## Current State Assessment

**What we have:**
- Complete card designs for 6 factions (4 MVP) in `command_cards/unit_types/**/*.md`
- `build_printable_prototype.py` — 1490-line PDF generator that renders cards, unit discs, hex board, tokens, card backs, and rules reference
- `RULEBOOK.md` — complete printable rulebook
- Art generation pipeline: `generation_queue.json`, `generation_manifest.json`, `full_review.json` (2,213 images reviewed)
- Prompt libraries in `ART_GENERATION_GUIDE.md` and `PROMPTS.md`
- Existing test PDFs: `prototype/test_prototype.pdf`, `prototype/test_printable.pdf`

**Critical gap — art assets are not on this machine:**
- `D:\Jake\ComfyUI\output\annointed-exile\prototype` does not exist
- `generation_manifest.json` references files in `prototype\commander-cards\`, `prototype\unit-cards\`, etc.
- The `build_printable_prototype.py` default art-dir points to `D:\Jake\ComfyUI_windows_portable\ComfyUI\output\ComfyUI\annointed-exile\prototype`

**Component inventory — what the PDF builder needs vs what exists:**

| Component | Needed For | Status |
|---|---|---|
| Game board (8×8 hex) | Play surface | Code ready, needs art tiles |
| Command cards (~40–50 unique) | Core gameplay | Card data complete, needs art |
| Unit discs (27 total) | Piece representation | Stats defined, needs art |
| Card backs (1 design) | Deck identity | Code ready, needs art |
| Tokens/markers (activation, lost pile, etc.) | Game state | Code ready, needs art |
| Rules reference | Playability | Code ready, text exists |

---

## Plan: 5 Phases to Printable Prototype

### Phase 1: Resolve Art Pipeline Location

**Goal:** Get art assets onto this machine in a location the PDF builder can find.

**Decision needed:** Where is ComfyUI installed on this machine, and where should art output go?

**If ComfyUI is available locally:**
1. Update `build_printable_prototype.py` default `--art-dir` to a local path (e.g., `D:\the-exile-king\art\prototype`)
2. Create the folder structure matching what `ArtInventory._scan_art()` expects:
   ```
   <art_dir>/
     commander-cards/
     unit-cards/
     hex-tiles/
     card-backs/
     ui/
   ```
3. Run `run_comfyui_generation.py` or manual ComfyUI batch to generate the ~175 queue items from `generation_queue.json`

**If ComfyUI is NOT on this machine:**
1. Copy `generation_queue.json` and `prep_regen_queue.json` to the machine with ComfyUI
2. Generate art there
3. Copy the output folder back to this machine
4. OR: Use `--no-art` mode to generate a placeholder PDF first, then manually paste in art later

**Art needed by category (from generation_queue.json):**

| Category | Items | Prompt Keys Needed |
|---|---|---|
| Commander cards | 40 (4 commanders × 10 variants each) | `card_front_david`, `card_front_jonathan`, `card_front_achish`, `card_front_philistine_lord` |
| Unit cards | ~100+ | `swordsmen-advance`, `swordsmen-formation`, `spear-wall`, `spearman-formation`, `spearman-screen`, `circle-and-strike`, `stone-volley`, `scout-recon`, `scout-formation`, `shield-wall`, `phalanx-advance`, `guard-formation`, `jonathans-mark`, `perfect-shot`, `archer-volley`, `archer-formation`, `giants-might`, `unstoppable`, `berserker-rage`, `chariot-charge`, `chariot-formation-1`, `chariot-formation-2`, `ekron-archer-command`, `ekron-archer-formation-1`, `ekron-archer-formation-2` |
| Card backs | 3 | `card_back` |
| Hex tiles | 30 (10 grass, 10 rock, 10 sand) | `hex_grass`, `hex_rock`, `hex_sand` |
| UI elements | ~8 | `command-card-back`, `activation-token`, `lost-pile-marker`, `card-frame-template`, `hp-bar-bg`, `hp-bar-fill`, `reward-panel`, `setup-sheet` |

**Prompt key mismatch risk:** The `generation_manifest.json` uses keys like `card_front_david` but `build_printable_prototype.py` maps card names to keys via `CARD_NAME_TO_PROMPT_KEY`. Verify all ~50 card names in the .md files have matching entries in that mapping table. Any gaps will render as "ART PENDING" placeholders.

### Phase 2: Art Curation

**Goal:** Select the best 1–2 images per prompt key from the generated variants.

**Steps:**
1. Run `review_art_ollama.py` on the newly generated art (or reuse `full_review.json` if art was previously reviewed)
2. For each prompt key, pick the highest-scoring KEEP image
3. Organize into a clean folder structure:
   ```
   art/
     curated/
       commander-cards/
         david.png
         jonathan.png
         achish.png
         philistine-lord.png
       unit-cards/
         swordsmen-advance.png
         ...
       hex-tiles/
         grass.png
         rock.png
         sand.png
       card-back.png
       tokens/
         activation.png
         ...
   ```
4. Update `build_printable_prototype.py` `--art-dir` to point to the curated folder

**Alternative (if no review pipeline available):** Manually inspect the generated images and copy the best one per prompt key to the curated folder with a clean filename.

### Phase 3: Card Data Validation

**Goal:** Ensure all card .md files are parseable and consistent before PDF generation.

**Known issues from COMMAND_CARD_AUDIT.md:**
1. Faction file drift — `command_cards/factions/*.md` may have different card text than unit type files
2. Card count inconsistency — some units have 2 cards, some have 3
3. Activation budget unverified
4. "Chariot Support" / "Chariot Lane" synergy abilities may need mechanical meaning
5. Ambush/Overwatch reaction abilities need rules support confirmation

**Steps:**
1. Run `check_dupes.py` and `check_missing.py` on card files
2. Cross-reference each unit type file against its faction file for name/effect consistency
3. Resolve any parse errors in `build_printable_prototype.py` (formation card parsing is fragile)
4. Verify `CARD_NAME_TO_PROMPT_KEY` covers every unique card name parsed from .md files

### Phase 4: Build the PDF

**Goal:** Generate a complete print-and-play PDF.

**Command:**
```bash
python build_printable_prototype.py \
  --art-dir "D:\the-exile-king\art\curated" \
  --output "D:\the-exile-king\prototype\exile_king_printable.pdf" \
  --scope mvp \
  --dpi 300
```

**Expected output sections:**
1. Cover page ("THE EXILE KING — Printable Prototype")
2. Rules reference (from RULEBOOK.md)
3. Command card sheets (3×3 grid per page, ~5–10 pages for ~50 cards)
4. Unit disc sheet (27 discs, 2" diameter)
5. Hex board (8×8 grid, one page)
6. Token sheet (activation, commander, lost pile, shield, HP markers)
7. Card back sheet (printable sheet of card backs)

**Validation:**
- Open the PDF, verify all card text is readable
- Verify art appears on every card (no "ART PENDING" placeholders)
- Verify unit disc stats are correct
- Print a test page and check physical sizing (2.5" × 3.5" cards, 2" discs)

### Phase 5: Physical Playtest Prep

**Goal:** Make the prototype actually playable on paper.

**Steps:**
1. **Print test:** Print one copy of each component type on cardstock:
   - Cards: 2.5" × 3.5" (use the 3×9 grid layout)
   - Unit discs: 2" diameter
   - Board: 8×8 hex grid, full page
   - Tokens: 1" diameter
2. **Laminate or sleeve:** Cards should be sleeved or laminated for durability
3. **Create token pool:** Cut out activation tokens, commander markers, lost pile marker
4. **Playtest checklist:**
   - Can you set up the co-op scenario in <5 minutes?
   - Can you resolve a full turn without referencing the rulebook?
   - Are card abilities clear and unambiguous?
   - Is the hex board readable?
   - Do unit disc stats match the rulebook?

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| ComfyUI not available on this machine | High | Blocks art generation | Copy art from other machine, or use `--no-art` placeholders |
| Prompt key mismatches between queue and PDF builder | Medium | Some cards get placeholders | Audit `CARD_NAME_TO_PROMPT_KEY` mapping table |
| Card .md parse errors (formation cards fragile) | Medium | Missing cards in PDF | Run parser validation before building |
| Review data (`full_review.json`) references files not on disk | Medium | ArtInventory can't find curated images | Use `--unreviewed-ok` flag or manual curation |
| Art style drift (medieval/fantasy instead of bronze age) | Medium | Aesthetic mismatch | Reject and regenerate with stronger era-lock prompts |
| Print sizing off | Low | Components don't fit | Verify DPI and dimensions in build script |

---

## Open Questions

1. **Where is ComfyUI installed?** Is it on this machine or only on "Jake's" machine? This determines whether art generation happens here or needs to be copied.
2. **Are the images in `generation_manifest.json` actually generated and available somewhere?** Or do they need to be regenerated from scratch?
3. **Do you want the full 6-faction prototype or just the 4 MVP factions?** The scope affects card count (~50 vs ~70 cards) and print length.

---

## Dependencies

- Pillow (PIL) — already used by `build_printable_prototype.py`
- ComfyUI + DreamShaper XL Lightning — for art generation
- Ollama — for art review (optional, can do manual review)

---

## Estimated Effort

- Phase 1 (art pipeline): 1–2 hours (or zero if art is already on disk)
- Phase 2 (art curation): 1–2 hours
- Phase 3 (card validation): 30–60 minutes
- Phase 4 (PDF build): 5–10 minutes
- Phase 5 (print + playtest): 2–4 hours including printing time

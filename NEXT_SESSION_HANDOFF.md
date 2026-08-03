# Prototype Handoff Context — The Exile King

## What's Done
- Biblical formation theming complete: all 40+ unit type files updated with faction-specific card names and removed anachronisms (committed as `48d1655`)
- Command card design finalized for 4 playable factions: David's Company, Jonathan's Followers, Achish's Host, Ekron's Host
- Art generation pipeline built: `generation_queue.json`, `review_art_ollama.py`, `run_comfyui_generation.py`
- Prompts defined in `PROMPTS.md`; prompt keys are stable (art assets can be generated without breaking references)
- **Full art review completed**: 2,213 images reviewed via Ollama (2,138 KEEP, 75 TRASH, 0 errors) — results in `full_review.json`
- **Low-scored images archived**: all 1,630 images scoring ≤3 moved to `_archive_regeneration_round2/`
- **`prep_regen_batch.py` created**: generates `prep_regen_queue.json` (175 items, ~388 images) with exact counts per prefix
- **`build_printable_prototype.py` completed**: generates print-and-play PDF from card `.md` files + ComfyUI art assets
- **`build_printable_prototype.py` bugs fixed**: `smart_title` apostrophe handling, Shield Advance mapping, formation card name overwrite

## What's NOT Done
- **Unity implementation has not started** (Sprint 3 is pending)
- **No C# changes yet** — no hex grid, no activation system, no card resolver
- **Printable prototype assets not fully generated** — `prep_regen_queue.json` is ready with 175 items / ~388 images; after the review round finishes and ComfyUI is launched, run the generation script
- **Mechanical balance is unvalidated** — card designs are on paper; nothing has been playtested or implemented

## Where Things Stand
- `command_cards/unit_types/**/*.md` — design complete, ready for implementation
- `command_cards/factions/*.md` — faction summaries and deck rules documented
- `command_cards/formations/*.md` — faction-wide formations defined
- `GDD.md` / `POST_MVP_GDD.md` — unit stats and roster rosters exist but may drift from the final card implementations
- `review_art_ollama.py` — prompt dictionary is populated and matches current card names

## Recommended Next Focus

### 1. Command Card Mechanical Validation
**Why:** The cards were just rethemed. Before Unity work starts, the abilities need a consistency pass:
- Verify every card's activation count, target count, and power budget matches the plan
- Check that renamed abilities haven't introduced mechanical ambiguity
- Resolve any conflicts between `command_cards/unit_types/*.md` and `command_cards/factions/*.md`

### 2. Unit Stat Alignment
**Why:** `GDD.md` has base stats, but the final command cards may imply different effective stats:
- Cross-reference unit stat blocks in GDD with what the cards actually let units do
- Adjust base stats or card effects so they match the intended power curve

### 3. Printable Prototype Build
**Why:** A physical print-and-play version can be built immediately while Unity is in development:
- Generate art assets using the existing ComfyUI pipeline
- Layout card templates and unit discs for printing
- Playtest with paper tokens to validate the core loop

### 4. Unity Sprint 3 Implementation
**Why:** This is the actual game engine work
- Hex grid, unit movement, activation resolution, card playing
- Follow the prototype plan's mechanical rules exactly

## Suggested First Topic for Next Session

**Start with Command Cards.** They are the heart of the game's tactical layer, they were just rethemed, and they need to be mechanically sound before any implementation begins. Once cards are validated, unit stats can be aligned, and then the printable prototype can be built for playtesting.

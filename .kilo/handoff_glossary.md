# Glossary Migration Handoff — Action Word Glossary Plan

## Source of Truth
`.kilo/plans/1785193363751-action-word-glossary.md` — all design decisions resolved there.

## What's Done
- All 27 design decisions in the plan are finalized and locked.
- Term retirement list is complete (Activate → Command, Defense → Shield tokens, commander auras removed, fatigue removed, Penalty removed).
- Formation card structure defined (3 subtypes: Regular, Persistent, Formation; 1 Formation + 4 Regular/Persistent per unit type; 10 per commander).
- Camp/Brainstorm mechanics fully specified.
- Forest LOS algorithm defined (unavoidable crossings, prefer non-Forest paths).
- Shield token timing locked (start of unit's next turn, not when damaged).
- **Phase 1 (terminology):** Complete. All "Activate" → "Command" and "Defense" → "Shield" replacements done across `command_cards/`, `CARDS.md`, `COMMAND_CARD_AUDIT.md`, `RULEBOOK.md`, `GDD.md`, `POST_MVP_GDD.md`, `PROMPTS.md`.
- **Phase 2 (card expansion):** ~55 new cards added across unit types and commanders to expand toward target counts.
- **Phase 4 (docs):** GDD.md, RULEBOOK.md, POST_MVP_GDD.md, PROMPTS.md, CARDS.md, COMMAND_CARD_AUDIT.md all updated.
- **Phase 5 (verification):** Zero remaining retired terms across the repo.

## What's NOT Done
- **Phase 3:** `command_cards/formations/*.md` (4 files) still separate from unit type files — not yet merged.
- **Card quality:** Phase 2 added structurally-appropriate cards but they need creative/design review for balance and flavor consistency.
- **Faction summaries** (`factions/*.md`) may need updates to reflect new card pools and merged Formation cards.

## Key Constraints
1. **Do NOT rename prompt keys** in `PROMPTS.md`, `generation_manifest.json`, `generation_queue.json`, or `review_art_ollama.py`. Only display names change.
2. **Do NOT implement fatigue** — rule is removed entirely.
3. **Brainstorm is a free action** — usable any time, even during your turn.
4. **Shield tokens are turn-based** — removed at start of next turn, not when damaged.
5. **No passive Spent recovery** — only Camp/Brainstorm recover Spent cards.
6. **Formation displacement** — new Formation replaces old one.

## Remaining Work
1. **Phase 3:** Merge `command_cards/formations/*.md` unit-specific Formation cards into corresponding `unit_types/` files. Retire faction-wide formations or integrate them into faction summary files.
2. **Creative review:** Phase 2 cards need design review for balance and flavor.
3. **Faction summaries:** Update `command_cards/factions/*.md` to reflect new card pools and merged formations.
4. **Unit stat alignment:** Cross-reference GDD base stats with new card effects to ensure power curve consistency.
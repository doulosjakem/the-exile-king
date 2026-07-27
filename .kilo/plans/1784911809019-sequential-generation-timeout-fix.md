# Plan: Build Printable Playable Prototype

## Goal

Produce a cut-out-and-play tabletop prototype printed on standard letter paper, plus a concise rule book.

## Current State

**We have:**
- Art assets generated/queued for portraits, standees, tokens, tiles, command cards, equipment, UI, box art
- GDD with full rules: turn structure, combat, command card system, AI priority, scenarios
- Unit stats defined for **David's Company** (7 units) and **Amalekites** (6 units)
- Command card design formula + activation framework docs
- 8×8 hex grid requirement

**We do NOT have:**
- Unit stats for most factions (Saul's Army, Jonathan's Followers, Philistines, Mighty Men, minor factions, neutrals)
- Rule book text (not written)
- Printable sheet layouts (no design for how tokens/tiles/cards are arranged on paper)
- Command card text (user is actively designing this elsewhere)

## Gaps to Close

### 1. Unit Stats (Critical)
Only **13 units** have stat blocks in the GDD. For a playable prototype we need at minimum the MVP factions:
- David's Company: 7 units (done)
- Amalekites: 6 units (done)
- Saul's Army: 6 units (missing)
- Jonathan's Followers: 4–8 units (missing)

That's ~10–14 missing stat blocks. Post-MVP factions (Philistines, Mighty Men, minor factions) can follow later.

### 2. Rule Book
Needs to cover, in 1–4 pages:
- Setup (army building, command deck)
- Turn structure (draw → fatigue → choose 2 cards → resolve → enemy turn)
- Activation rules (one activation per unit per turn)
- Combat (range, LoS, damage, armor)
- Commander mechanics (aura, death = loss)
- AI rules (for solo play)
- Victory conditions

Content exists in GDD but is not formatted for printing.

### 3. Component Layouts (Print-Ready)
Need designed pages for:
- **Unit token sheets** — cut-out tokens with portrait + stats on the same piece
- **Hex board** — 8×8 grid, either as 64 individual hex tiles or one full board
- **Command cards** — text + art layout (depends on what user designs elsewhere)
- **Activation/status tokens** — simple markers for activated units, HP tracking
- **Scenario cards** — objective, deployment, enemy list

### 4. Missing Art for Some Units
Not all unit portraits/tokens may be generated yet. Need to verify coverage for whatever stat blocks we define.

## Key Decision Needed

**Prototype scope:**

Option A: **MVP factions only** (David's Company + Amalekites + Saul's Army + Jonathan's Followers ≈ 20–25 units). Fastest path to playable.

Option B: **All 54 units** from the roster. More complete, but requires writing ~36 missing stat blocks and generating/curating art for all of them.

Option C: **Hybrid** — MVP factions get full stat blocks and print sheets. Everything else gets placeholder cards: "Coming soon / expansion unit."

## Recommendation

**Option A or C.** A playable prototype with 20–30 well-defined units is enough to validate the core loop. Once the game plays well, expanding to 54 units is just data entry and art assembly.

## Open Questions

1. **Which scope do you want?** A = MVP factions (~25 units), B = all 54, or C = MVP now, rest later?
2. **Token format:** standee style (portrait on top, stats on a base tab) or poker-card style (portrait front, stats back)?
3. **Hex board:** individual tiles you arrange, or one pre-laid-out 8×8 sheet?
4. **Rule book length:** quickstart (1 page) or full reference (4 pages)?

## Next Steps (after decisions)

1. Write missing unit stat blocks for chosen scope
2. Write concise rule book
3. Design printable page layouts (letter-size, cut lines, bleed)
4. Assemble art + text into print-ready sheets
5. Verify all required art exists; trigger generation for anything missing
6. Export as PDF

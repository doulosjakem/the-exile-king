# Handoff — MVP Sprint Progress

> **Auto-compacting active.** This file tracks what's built and what's next so a fresh context can resume seamlessly.

---

## 🚨 Design Pivot: Command Card System (Unit-Type Specific)

The battle system has been redesigned from the ground up. See `GDD.md` for the full spec and `ROADMAP.md` for the updated sprint plan.

**Old system:** 2 team actions per turn, unit state machines (Ready/Acted/Exhausted), Overwork mechanic, per-state action tables.

**New system:** Command Card deck built from army composition (unit-type specific cards + universal commands). Each unit can activate only once per turn. Fatigue causes random card loss. Casualties remove matching cards from deck.

**What this means for existing code:**
- `HexGrid.cs` — ✅ Still good, no changes needed
- `HexTileGenerator.cs` — ✅ Still good
- `UnitVisual.cs` — ✅ Still good
- `GameSetup.cs` — ⚠️ Updated (assigns UnitType, builds deck from army)
- `PlayerInputHandler.cs` — ⚠️ Updated (uses CanActivate, integrates with CardAbilityResolver)
- `AIDirector.cs` — ⚠️ Updated (uses new Unit activation API)
- `TurnManager.cs` — ⚠️ Updated (card phases, fatigue, activation reset)
- `DamagePopup.cs` — ✅ Still good, reuse as-is
- `GameUIController.cs` — ⚠️ Updated (hand display, fatigue notification, lost pile counter)
- `RunManager.cs` — ⚠️ Updated (casualty removal, recover lost card reward)
- `Unit.cs` — ⚠️ Refactored (removed state machine, added UnitType + activation tokens)
- `UnitData.cs` — ⚠️ Needs update for new UnitType-centric design
- `MobileInputHandler.cs` — ✅ Still good

**New files added:**
- `UnitType.cs` — UnitType enum
- `CommandCard.cs` — ScriptableObject with unit-type filters and casualty linkage
- `CardDeckManager.cs` — Deck/hand/spent/lost + fatigue + casualty removal
- `CardAbilityResolver.cs` — Execute card abilities with unit-type filtering and activation tokens

**Sprints 0-2 are fully done.** Sprints 3-7 have been rewritten for the new card system.

---

## Current State

**What's built and working:**
- Sprints 0–2 are committed and functional: hex grid, procedural tiles, unit visuals with shape-based tokens, selection/movement/attack input, basic AI, damage popups, mobile input, run manager
- The old turn system (2 actions/unit, Ready/Acted/Exhausted state machine, Overwork) was **replaced** by the Command Card deck system
- PROMPTS.md has been fully rewritten with era-locked prompts for 40 generation jobs across 7 batches
- ART_GENERATION_GUIDE.md has been updated with corrected negative prompt, output folder structure, and a complete rejection criteria section
- ComfyUI has been configured with `--lowvram` for GTX 1060 compatibility

**What's NOT built yet (needs implementation):**
- `UnitType.cs` — enum does not exist yet
- `CommandCard.cs` — ScriptableObject does not exist yet
- `CardDeckManager.cs` — deck/hand/spent/lost piles do not exist yet
- `CardAbilityResolver.cs` — card-to-unit action binding does not exist yet
- Command Card UI (hand display, card selection flow, fatigue notification, lost pile counter)
- TurnManager.cs refactor for card phases
- AIDirector.cs update for new activation API
- GameSetup.cs update for deck building from army composition
- RunManager.cs update for casualty removal and recover-lost-card reward
- Unit.cs refactor (remove state machine, add UnitType + activation tokens)
- UnitData.cs update for UnitType-centric design
- EncounterData.cs — encounter definitions do not exist yet

**The code in the repo is the PRE-PIVOT version.** The Command Card system is designed in GDD.md and PROMPTS.md but not yet implemented in code.

---

## Art Generation Status

**Prompt files:** ✅ Complete
- PROMPTS.md — 40 prompts across 7 batches, all era-locked
- ART_GENERATION_GUIDE.md — workflow, negative prompt, folder structure, rejection criteria

**ComfyUI setup:** ✅ Ready
- `D:\Jake\ComfyUI_windows_portable\run_nvidia_gpu.bat` updated with `--lowvram`
- Model: DreamShaper XL Lightning
- Output folder: `D:\Jake\ComfyUI_windows_portable\ComfyUI\output\exile_king_art\`

**Folder structure:** Ready to create
- PowerShell commands provided in ART_GENERATION_GUIDE.md
- Each prompt gets its own subfolder with `to_trash/` inside
- `_sorted/` and `_rejected/` folders for final organization

**Rejection criteria:** ✅ Locked in ART_GENERATION_GUIDE.md
- 3-tier check: Anatomy/era → Readability → Style match
- 21 AI generation error criteria
- 20 board game usability criteria
- 9 style consistency criteria
- 2 quality criteria + 3 FLAG criteria
- Review scoring system: 1–4 scale across 6 criteria, 24 total points

**Images generated so far:** None yet — waiting to start batch generation

---

## What To Do Next (Priority Order)

### 1. Art Generation (Do First)
See `ART_GENERATION_GUIDE.md` for full workflow. Quick start:
1. Create the `exile_king_art` folder structure using the PowerShell commands in the guide
2. Start with Batch 4: Unit Token Icons (most visible on the board)
3. Use `--lowvram` mode, batch size 1, sequential generation
4. Review using the rejection criteria in the guide
5. Move keepers to `_sorted/`, rejects to `to_trash/`

### 2. Command Card System Implementation (Code)
The design is finalized in `GDD.md`. Implementation order:
1. Create `UnitType.cs` enum
2. Create `CommandCard.cs` ScriptableObject
3. Create `CardDeckManager.cs`
4. Create `CardAbilityResolver.cs`
5. Refactor `Unit.cs` (remove state machine, add UnitType + activation)
6. Update `TurnManager.cs` for card phases
7. Update `AIDirector.cs` for new activation API
8. Update `GameSetup.cs` for deck building
9. Update `GameUIController.cs` for hand display
10. Update `RunManager.cs` for casualty removal
11. Create `EncounterData.cs`
12. Create `UnitData.cs` ScriptableObjects

### 3. Polish
- Balance card values and deck sizes
- Verify all card abilities resolve correctly
- Test fatigue system (lose random card each turn)
- Test casualty system (eliminate unit type → remove matching card)
- Verify AI turns work with new API
- Add remaining card art from PROMPTS.md

---

## Key Files Reference

| File | Status | Notes |
|---|---|---|
| `GDD.md` | ✅ Current | Command Card system spec |
| `ROADMAP.md` | ⚠️ Needs update | Sprint plan still shows old system |
| `Handoff.md` | ✅ This file | |
| `PROMPTS.md` | ✅ Current | 40 era-locked prompts |
| `ART_GENERATION_GUIDE.md` | ✅ Current | Full workflow + rejection criteria |
| `CARDS.md` | ⚠️ May need update | Card specs may have changed with pivot |
| `HexGrid.cs` | ✅ Working | 8×8 hex grid, BFS pathfinding |
| `HexTileGenerator.cs` | ✅ Working | Procedural hex mesh |
| `Unit.cs` | ⚠️ Needs refactor | Remove state machine, add UnitType |
| `UnitVisual.cs` | ✅ Working | Shape-based tokens |
| `PlayerInputHandler.cs` | ✅ Working | But needs CardAbilityResolver integration |
| `AIDirector.cs` | ✅ Working | But needs new activation API |
| `TurnManager.cs` | ⚠️ Needs refactor | Card phases, fatigue, activation reset |
| `GameUIController.cs` | ⚠️ Needs update | Hand display, fatigue notification |
| `GameSetup.cs` | ⚠️ Needs update | Deck building from army |
| `RunManager.cs` | ⚠️ Needs update | Casualty removal, recover lost |
| `DamagePopup.cs` | ✅ Working | Reuse as-is |
| `MobileInputHandler.cs` | ✅ Working | Reuse as-is |
| `UnitType.cs` | ❌ Does not exist | Create first |
| `CommandCard.cs` | ❌ Does not exist | ScriptableObject |
| `CardDeckManager.cs` | ❌ Does not exist | Deck/hand/spent/lost + fatigue |
| `CardAbilityResolver.cs` | ❌ Does not exist | Card-to-unit binding |
| `UnitData.cs` | ❌ Does not exist | ScriptableObject definitions |
| `EncounterData.cs` | ❌ Does not exist | Encounter definitions |

---

## ComfyUI Art Pipeline

**Model:** DreamShaper XL Lightning  
**Settings:** 512×512 or 1024×1536, steps 4–8, CFG 2.5–3, batch 1 (sequential due to lowvram)  
**Negative prompt:** Full era-lock list in ART_GENERATION_GUIDE.md  
**Output:** `D:\Jake\ComfyUI_windows_portable\ComfyUI\output\exile_king_art\`  
**Folder structure:** Per-prompt subfolders with `to_trash/`, `_sorted/`, `_rejected/`

**Generation order:**
1. Batch 4: Unit Token Icons (9 prompts) — most visible on board
2. Batch 5: Hex Tiles (3 prompts) — needed for board
3. Batch 6: UI Elements (4 prompts) — needed for gameplay
4. Batch 3: Unit Portraits (12 prompts) — for cards
5. Batch 1: Command Card Art (8 prompts) — for cards
6. Batch 2: Card Frame Template (1 prompt)
7. Batch 7: Cover Art (3 prompts)

**Review workflow:**
1. Generate batch size 1 per prompt
2. Review against rejection criteria (3-tier check)
3. Move passes to `_sorted/`, fails to `to_trash/`
4. Score keepers on 1–4 scale if choosing between variants
5. Delete `to_trash/` contents when done with prompt

---

## Important Context

- **Design pivot:** The game was redesigned from a 2-actions-per-turn system to a Command Card deck system. The code in the repo is the OLD system. The new system is designed but not yet implemented.
- **Art style:** Hand-painted historical illustration / illuminated manuscript / aged parchment. NOT photorealistic, NOT fantasy, NOT anime. Muted earth tones.
- **Era:** Bronze age Levantine (ancient Israel/Judea). NOT medieval, NOT European. Mediterranean features, dark hair, linen tunics, leather armor, wool cloaks, bronze weapons.
- **Platform:** Unity 6 LTS, targeting PC and mobile. Single GPU (GTX 1060 6GB) for art generation.
- **Current focus:** Art generation is the immediate priority. Code implementation of the Command Card system follows after art pipeline is flowing.

---

*Last updated: 2026-07-17*

# Handoff — The Anointed Exile

> **Status:** Art pipeline ready. Code is pre-pivot. Card system needs implementation.

---

## Current State

**Built (Sprints 0–2):** Hex grid, procedural tiles, unit visuals, selection/movement, basic AI, damage popups, mobile input, run manager. All committed.

**Built (Command Card system — Sprints 3–6):** `UnitType.cs`, `CommandCard.cs`, `CardDeckManager.cs`, `CardAbilityResolver.cs`, `CardTurnController.cs` (new — select 2 cards, resolve Top(A)+Bottom(B)), `GameBootstrap.cs` (new — runtime wiring so the game runs from the near-empty scene), `UnitData.cs`/`EncounterData.cs`. TurnManager/GameSetup/GameUIController/RunManager/AIDirector refactored for the card turn flow (Selection → Resolution → Done → Enemy). Player UI shows the hand, pick-2 + Reveal, per-half targeting, Deck/Spent/Lost counters, and reward panel wired to RunManager.

**Known MVP gaps (Sprint 7, not yet done):** card/deck state does not persist between battles in a run (`CardDeckManager.InitializeDeck` rebuilds each battle, so Lost cards from a prior battle are cleared); recruited units are not added to `currentPlayerRoster` so they don't carry to the next battle; ScriptableObject card *assets* in `Assets/Resources/CommandCards/` are not created (GameSetup builds them at runtime instead).

**IMPORTANT — project not yet opened in Unity:** there is no `Library/` and no `.cs.meta` files, and the scene only contains Camera/Light/Volume. `GameBootstrap` (via `[RuntimeInitializeOnLoadMethod]`) instantiates all managers and a runtime unit prefab on load, so the game is runnable once Unity imports the project. Open the project in Unity 6 before expecting a build.

---

## Art Pipeline (Post-Pivot Thread Work)

**PROMPTS.md** — 40 era-locked prompts across 7 batches:
- Batch 1: 8 command card art scenes
- Batch 2: 1 card frame template
- Batch 3: 12 unit portraits (player + Amalekite)
- Batch 4: 9 unit token icons
- Batch 5: 3 hex tiles
- Batch 6: 4 UI elements
- Batch 7: 3 cover art variants

All prompts include era-locking: "bronze age Levantine", "NOT medieval, NOT fantasy, NOT European", Mediterranean features, specific material details (hide shields, bronze-tipped spears, linen tunics, leather vests).

**ART_GENERATION_GUIDE.md** — updated with:
- Era-locked prompts for all 40 generation jobs
- Corrected universal negative prompt (adds chainmail, longbow, knight, crusader, etc.)
- ComfyUI setup with `--lowvram` for GTX 1060
- Output folder structure with per-prompt subfolders and `to_trash/` sorting
- Complete rejection criteria (3-tier check: Anatomy/era → Readability → Style match)
- Review scoring system: 1–4 scale across 6 criteria
- Folder mapping table for all 40 prompts

**ComfyUI:** `D:\Jake\ComfyUI_windows_portable\run_nvidia_gpu.bat` updated with `--lowvram`. Model: DreamShaper XL Lightning. Output: `D:\Jake\ComfyUI_windows_portable\ComfyUI\output\exile_king_art\`.

**Images generated:** None yet — ready to start batch generation.

---

## What To Do Next

### 1. Open the project in Unity 6 and verify the card flow runs (FIRST)
The card system is now implemented in code, but the project has **never been opened in Unity** (no `Library/`, no `.cs.meta`). `GameBootstrap` instantiates all managers + a runtime unit prefab on load, so it should run once Unity imports. Before any further work:
- Open in Unity 6 LTS, let it import/compile.
- Press Play → expect David + 2 Scouts vs Amalekites, hand of cards at the bottom, tap 2 → Reveal → resolve Top(A)+Bottom(B) → End Turn → AI acts.
- Fix any console errors (most likely candidates: URP shader/material references, or an ordering edge case).

### 2. Art Generation (parallel / independent thread)
Follow ART_GENERATION_GUIDE.md. Order: tokens → tiles → UI → portraits → card art → frame → cover. Batch size 1, lowvram mode. Review with rejection criteria. None generated yet.

### 3. Card System — remaining MVP gaps (Sprint 7)
The current build works for a single battle but does **not** yet persist run state:
- `CardDeckManager.InitializeDeck` rebuilds the deck every battle → Lost cards from a prior battle are cleared. Persist the deck Spent/Lost state across battles in a run.
- Recruited/upgraded units are not added to `RunManager.currentPlayerRoster` → they don't carry into the next battle. Wire recruit/upgrade rewards into the roster used by `GameSetup.SpawnBattle`.
- Create the `Assets/Resources/CommandCards/` ScriptableObject **assets** (per CARDS.md) instead of building cards at runtime in `GameSetup`, so art can be assigned and decks authored in-editor.
- Wire victory/defeat screens to RunManager flow (currently only the basic panel shows).

### 4. Card ability polish (post-basic)
- Attack cards currently auto-target the nearest enemy in range. Optionally let the player pick the specific target (resolver already exposes `GetValidAttackTargets`).
- Card art, ability icons, and "Lose" skull styling from CARDS.md are not yet shown.
- Grey-out / remove cards whose linked unit type was eliminated (casualty removal already moves them to Lost).

See GDD.md for card system spec. See CARDS.md for card list. See ROADMAP.md for the full sprint plan.

---

## Key Context

- **Era:** Bronze age Levantine. NOT medieval, NOT European. Mediterranean features, dark hair, linen/leather/wool, bronze weapons.
- **Style:** Hand-painted ink + watercolor on parchment. Muted earth tones.
- **Platform:** Unity 6 LTS, PC + mobile. GTX 1060 6GB for art.
- **Focus:** Art generation first, then card system implementation.

---

*Last updated: 2026-07-17*

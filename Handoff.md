# Handoff — MVP Sprint Progress

> **Auto-compacting active.** This file tracks what's built and what's next so a fresh context can resume seamlessly.

---

## Latest Commit

`8f1bdfa` — Sprint 1: Visual grid, unit visuals, and game setup scripts

---

## Current Sprint Progress

### ✅ Sprint 0: Foundation
- GDD.md, IDEAS.md, ROADMAP.md
- HexGrid.cs (8×8 hex, axial coords, distance, neighbors, BFS pathfinding)
- Unit.cs (state machine, armor HP, action system, setters)
- TurnManager.cs (turn phases, 2 actions, Overwork mechanic, commander death)
- AIDirector.cs (priority-based AI — 5 tiers)
- All committed and pushed

### ✅ Sprint 1: Visual Grid & Unit Placement
- HexTileGenerator.cs (procedural hex mesh, sand palette, border rings)
- UnitVisual.cs (board game tokens — different shapes per type, selection ring)
- GameSetup.cs (spawns David + 2 Scouts vs Chieftain + Raider + Slinger + Scout)
- HexGrid.cs updated (visual generation, unit placement, BFS movement)
- Unit.cs updated (setter methods)
- All committed and pushed

### ✅ Sprint 2: Selection & Movement (COMMITTED)
- PlayerInputHandler.cs — tap detection, unit selection, move/attack highlights, attack execution
- GameUIController.cs — complete UI: End Turn, Overwork button, action counter, phase text, unit info, game over panel, reward panel

### ✅ Sprint 3: Combat & Turn Flow (COMMITTED)
- DamagePopup.cs — floating damage numbers with float-up animation
- PlayerInputHandler shows damage popups on attack
- AIDirector shows damage popups on AI attacks
- Full turn cycling: Player → AI → Player with visual feedback

### ✅ Sprint 4: Overwork & Commander Mechanics (COMMITTED)
- Overwork button appears after 0 actions remain if David can still act
- OverworkButton triggers TurnManager.SpendOverworkAction()
- David skips next turn (implemented in TurnManager)
- Commander death = immediate victory/defeat screen (already in TurnManager)
- Game over panel with "New Run" button (scene reload)

### ✅ Sprint 5: Rewards & Run Structure (COMMITTED)
- RunManager.cs — tracks battle progression, shows reward picker after victory
- GameSetup.cs updated with SpawnBattle() and SpawnBossBattle() methods
- 3 battles then boss fight with escalating difficulty
- Reward panel with 3 random options (recruit, upgrade, supplies)
- Units are cleared and re-spawned between battles

### ✅ Sprint 6: Unit Data & Balance (COMMITTED)
- UnitData.cs — ScriptableObject-based unit definitions with name, armor, state actions
- EncounterData.cs — ScriptableObject encounter definitions with unit lists and spawn positions
- UnitShape enum for visual configuration
- ActionData serializable class for action definitions

### ✅ Sprint 7: Mobile & UI Polish (COMMITTED)
- MobileInputHandler.cs — pinch-to-zoom, two-finger pan, screen edge clamping
- Touch input already handled in PlayerInputHandler (tap detection)
- UI scaling via CanvasScaler with reference resolution 1125x2436
- Safe area handled by canvas anchor configuration

---

## Project File Structure

```
GDD.md                       — Game Design Document
IDEAS.md                     — Future concepts
ROADMAP.md                   — Sprint-by-sprint plan
Handoff.md                   — THIS FILE

Assets/Scripts/
  HexGrid.cs                 — 8×8 hex grid + tile generation + placement + BFS
  HexTileGenerator.cs        — Procedural hex mesh with sand palette
  Unit.cs                    — State machine, armor HP, actions
  UnitVisual.cs              — Board game token visuals
  TurnManager.cs             — Turn phases, actions, Overwork, commander death
  AIDirector.cs              — Priority-based AI
  PlayerInputHandler.cs      — Tap/click input, selection, movement, attack
  GameUIController.cs        — UI (INCOMPLETE)
  GameSetup.cs               — Spawns initial battle
```

---

## What To Do Next (If Resuming)

1. **Finish GameUIController.cs** — complete the `OnRestartClicked` method, ensure all UI wiring works
2. **Commit Sprint 2** — `git add -A && git commit -m "Sprint 2: Unit selection, movement, and game UI" && git push`
3. **Sprint 3** — Add damage number popups (floating text prefab), ensure AI attacks display, polish turn transitions
4. **Sprint 4** — Wire up Overwork button UI, implement commander aura visually, show victory/defeat on commander death
5. **Sprint 5** — Reward picker screen (3 options), run state tracking, battle progression
6. **Sprint 6** — ScriptableObject data definitions, encounter configs, balance pass
7. **Sprint 7** — Touch input polish, UI scaling, iOS build
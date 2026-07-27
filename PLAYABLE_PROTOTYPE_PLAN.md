# Playable Prototype Planning Handoff

Copy everything below this line into ChatGPT to plan the next sprint.

---

## Project Context

**Game:** The Anointed Exile — tactical grid + Command Card deck game inspired by *The Duke* and *Slay the Spire*.  
**Setting:** David's fugitive years (1 Samuel).  
**Engine:** Unity 6 LTS (URP), C#, iOS primary.  
**Status:** Sprints 0-2 complete. Hex grid, unit visuals, selection/movement working. Command Card system not yet built.

## Objective

Ship a **playable local co-op prototype** (hotseat, no networking) featuring:

- **Player 1:** David's Company (shared Command Card deck)
- **Player 2:** Jonathan's Followers (shared deck, same activation economy)
- **Enemy:** Philistines (AI-controlled), **two commanders**: Achish + Philistine Lord

**Goal:** Two humans vs AI on 8×8 hex grid. Fun and winnable in 15–20 minutes.

## Core Design Rule — Unit Identity vs Command Card Differentiation

### Two Layers

1. **Unit Profile** — what the soldier physically is, base stats, combat role
2. **Command Deck** — how the commander uses the unit, special tactics, faction identity

### Common Units (shared by multiple factions)

Same or very similar base stats. Faction personality comes from **Command Cards**.

| Unit | Range | Attack | Defense | Health | Move | Notes |
|---|---|---|---|---|---|---|
| Swordsman | 1 | 2 | 1 | 2 | 2 | Standard melee |
| Spearman | 2 (reach) | 2 | 1 | 2 | 2 | Anti-charge |
| Shield Bearer | 1 | 1 | 2 | 3 | 1 | Tank/defender |
| Heavy Infantry | 1 | 2 | 2 | 3 | 1 | Slow, hits hard |
| Scout | 2 | 1 | 1 | 1 | 3 | Fast recon |
| Refugee | 1 | 0 | 1 | 1 | 1 | Support/non-combat |

### Signature Units (unique stats + unique Command Cards)

These differentiate factions and feel distinct to play.

#### David's Slingers ⭐

| Stat | Value |
|---|---|
| Range | 3 |
| Attack | 1 |
| Defense | 1 |
| Health | 2 |
| Movement | 3 |

Theme: Mobile skirmishers, David's iconic weapon, wilderness fighters.  
Strengths: Long range, high mobility, harassment.  
Weaknesses: Low damage, poor melee.

David Command Cards:
- **Circle and Strike** — Slingers may move before attacking
- **Stone Volley** — Multiple Slingers combine attacks for bonus damage
- **Fade Into the Hills** — Slingers gain defensive bonus after moving

#### Jonathan's Elite Archers ⭐

Same base stats as standard Archer (Range 2, Attack 2, Defense 1, Health 2, Move 2).  
Theme: Elite precision troops, Saul's military tradition, highly trained personal followers.

Jonathan Command Cards:
- **Jonathan's Mark** — Target an enemy. Jonathan's Archer gains +1 attack, ignore 1 defense
- **Hold the Line** — Jonathan's Archers cannot be pushed/displaced this round
- **Perfect Shot** — If Archer has not moved, gain +1 range for this attack

#### Ekron Archers (Philistine)

Same base stats as standard Archer.  
Theme: Coastal Philistine battlefield support, coordinated volleys.

Ekron Command Cards:
- **Opening Volley** — Ekron Archers attack before movement
- **Covering Fire** — After an ally moves, an Ekron Archer may make a free attack
- **Break Formation** — Enemies hit by Ekron Archers lose movement next turn

#### Achish's Giants ⭐

Unique stats. Theme: Gath's giant warriors, fear and intimidation.

| Stat | Value |
|---|---|
| Range | 1 |
| Attack | 3 |
| Defense | 2 |
| Health | 4 |
| Movement | 1 |

Strengths: High health, high melee damage, hard to remove.  
Weaknesses: Slow, vulnerable to being surrounded.

Achish Command Cards:
- **Protect Giants** — Giants gain defense bonus when adjacent to Achish
- **Fear** — Enemies adjacent to Giant lose 1 move next turn
- **Heavy Swing** — Giant deals extra damage, pushes target 1 tile

#### Ekron War Chariots ⭐

Unique stats. Theme: Coastal plain warfare, Philistine military strength.

| Stat | Value |
|---|---|
| Range | 1 |
| Attack | 2 |
| Defense | 1 |
| Health | 2 |
| Movement | 3 |

Strengths: High movement, charge attacks, open terrain dominance.  
Weaknesses: Poor rough terrain, vulnerable if trapped.

Ekron Command Cards:
- **Charge** — Chariot moves then attacks, +1 damage if moved ≥2 tiles
- **Breakthrough** — Chariot pushes target 1 tile after attack
- **Reposition** — Chariot moves through friendly units without obstruction

## Co-op Scenario Design

### Forces

| Faction | Units | Commander |
|---|---|---|
| David's Company (P1) | David, 2 Swordsmen, 1 Spearman, 2 Slingers, 1 Archer, 1 Scout | David |
| Jonathan's Followers (P2) | Jonathan, 2 Loyal Guards, 2 Elite Archers, 1 Scout | Jonathan |
| Philistines (AI) | Achish, Philistine Lord, 3 Spearmen, 2 Heavy Infantry, 2 Archers, 1 Champion, 1 Chariot | Achish + Lord |

### Map Placement

- David's Company spawns left edge, centered (tiles 0x3–0x4)
- Jonathan's Followers spawn left edge, top/bottom (tiles 0x1, 0x6)
- Philistines spawn right edge, centered (tiles 7x3–7x4)
- Lord spawns right edge top (7x1), Achish right edge bottom (7x6)
- 1–2 terrain obstacles (rock clusters) placed mid-board for cover

### Victory Condition

- Eliminate **both** Philistine commanders = victory
- Lose **either** David OR Jonathan = defeat
- Battle ends immediately on commander death

---

## Turn Flow (Hotseat Co-op)

### Phase 1: Draw & Fatigue
1. Both players draw from shared deck until hand = 4 cards
2. Each player loses 1 random card to Fatigue (goes to Lost pile)
3. If deck empty, refresh from Spent pile (shuffle)

### Phase 2: Card Selection
1. P1 selects **2 cards** from hand (tap to highlight, tap again to confirm)
2. P2 selects **2 cards** from hand
3. Cards remain private until reveal

### Phase 3: Resolution
1. **Reveal** — both players' selected cards flip face-up simultaneously
2. **P1 resolves** — choose which card's **top** and which card's **bottom** to use, then assign each to a valid unit
3. **P2 resolves** — same
4. Each activated unit gets an activation token (cannot activate again this turn)

### Phase 4: Enemy Turn
1. AI activates each Philistine unit once
2. Priority:
   - Protect nearest commander if threatened
   - Attack isolated/low-HP player units
   - Advance toward nearest player unit/commander
   - Support allies (champion duels commanders, archers cover infantry)

### Phase 5: Cleanup
1. Remove activation tokens from all units
2. Discard played cards to Spent pile
3. Next turn → Phase 1

---

## Deck Construction Rules

### Shared Deck (P1 + P2 combined)

Built at scenario start from army composition:

- **1 copy per unit type** each player brings
- Up to **2 copies max** per card type
- Universal commands: March, Engage (always included)

**Example deck for this scenario:**

| Source | Cards | Count |
|---|---|---|
| David | David's Leadership | 1 |
| Swordsmen | Swordsmen Advance | 1 |
| Spearman | Spear Wall | 1 |
| Slingers ⭐ | Circle and Strike | 1 |
| Archers | Archer Volley | 1 |
| Scouts | Scout Recon | 1 |
| Jonathan | Jonathan's Leadership | 1 |
| Loyal Guards | Guard Formation | 1 |
| Elite Archers ⭐ | Jonathan's Mark | 1 |
| Universal | March | 2 |
| Universal | Engage | 2 |

**Total: ~13 cards** (shuffle together, shared between both players)

### Card Loss

- **Fatigue:** 1 random card from each player's hand → Lost pile each turn
- **Casualty:** When last unit of a type dies, remove 1 matching card from deck/hand/spent → Lost pile

---

## Philistine AI — Two Commander System

### Commander Abilities (passive, free each turn)

**Achish:** Adjacent Philistine allies gain -1 damage taken (damage reduction).

**Philistine Lord:** Adjacent allies gain +1 attack (offensive aura).

Achish and Lord should stay 3–4 tiles apart so their auras don't fully overlap — creates tactical spacing.

### AI Priority Order

1. If commander threatened (enemy within 2 tiles):
   - Move commander away from danger
   - Move adjacent ally to protect
   - Champion/Heavy Infantry intercept
2. Attack isolated player unit (no adjacent allies)
3. Attack lowest-HP player unit in range
4. Move toward nearest player commander
5. Support: Archers target concentrated player units, Heavy Infantry advance in formation
6. If no valid action, reposition toward center

### Chariot AI
- Prefer open terrain (avoid rock clusters)
- Use Charge equivalent: move ≥2 tiles toward target, then attack
- Do not enter melee with Spearmen if possible

---

## UI Requirements (Hotseat)

1. **Turn indicator** — "P1 (David) — Select Cards" / "P2 (Jonathan) — Select Cards" / "Enemy Turn"
2. **Hand display** — bottom of screen, 4 card slots, tap to select (highlight border)
3. **Selected indicator** — "1/2 cards selected" prompt
4. **Reveal button** — appears when both players have 2 cards selected
5. **Resolution prompt** — "Select unit for [Top/Bottom ability name]"
6. **Enemy turn** — auto-advance with "skip" button to speed through
7. **Pile counters** — Deck: X, Spent: X, Lost: X (top-right corner)

---

## Implementation Sprint Order

### Sprint 3: Card Data System
1. `UnitType.cs` enum
2. `CommandCard.cs` ScriptableObject (name, top/bottom abilities, unit filter, max activations, isLostOnUse)
3. `CardDeckManager.cs` (deck/hand/spent/lost, draw, fatigue, casualty, refresh)
4. Card data assets for all MVP units
5. Deck construction from army list at scenario start

### Sprint 4: Co-op Turn Flow
1. Refactor `TurnManager.cs` from 2-action to card-based phases
2. Hotseat player switching
3. Card selection state machine (select 2 → reveal → resolve)
4. Activation token system

### Sprint 5: Card Resolution
1. `CardAbilityResolver.cs`
2. Unit targeting UI (valid/invalid targets)
3. Execute move, attack, buff, multi-target
4. Discard to spent/lost after resolution

### Sprint 6: Philistine AI + Two Commanders
1. AI priority with commander protection
2. Commander aura passives
3. Chariot pathfinding preference

### Sprint 7: Polish + Playtest
1. Victory/defeat screens
2. Damage popups
3. Balance pass (unit counts, deck size, AI difficulty)
4. Build and test on device

---

## Balance Targets

- **Players combined:** ~10 units (David 7 + Jonathan 4 = 11, but Jonathan's units are slightly stronger)
- **Philistines:** 9 units but heavier (Heavy Infantry, Champion, Chariot, Giants if included)
- **Deck size:** 13–16 cards, shuffled shared pool
- **Hand size:** 4 per player
- **Cards per turn:** 2 per player
- **Fatigue:** 1 lost card per player per turn
- **Expected turn count:** 8–12 turns = 15–20 minutes

---

## Key Decisions Already Made

- **Hotseat co-op** (no networking, shared screen)
- **Shared Command Card deck** between P1 and P2 (both draw from same pool)
- **Two Philistine commanders:** Achish + Philistine Lord (not Goliath — save for boss)
- **Common unit stats shared across factions**, differentiated by Command Cards
- **Signature units have unique stats:** David's Slingers, Jonathan's Archers, Ekron Archers, Achish's Giants, Ekron Chariots
- **Victory:** eliminate both Philistine commanders
- **Defeat:** lose David OR Jonathan

---

## Relevant Files

- `GDD.md` — core rules, unit stats, card system, turn structure
- `POST_MVP_GDD.md` — Philistine faction, Jonathan commander ability, co-op notes
- `ROADMAP.md` — Sprint 3–7 tasks
- `command_cards/factions/DAVIDS_COMPANY.md` — deck construction
- `command_cards/factions/JONATHANS_FOLLOWERS.md` — ally rules
- `command_cards/factions/PHILISTINES.md` — faction rules
- `command_cards/unit_types/DAVIDS_COMPANY/david/DAVID.md` — David's card definitions
- `command_cards/unit_types/JONATHANS_FOLLOWERS/elite_archer/ELITE_ARCHER.md` — Jonathan archer cards
- `command_cards/unit_types/PHILISTINES/achish/ACHISH.md` — Achish card definitions
- `command_cards/formations/PHILISTINES.md` — Philistine formations

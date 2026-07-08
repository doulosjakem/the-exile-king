# The Anointed Exile — Development Roadmap

> **Goal:** Playable MVP (3 battles + boss, ~30 min run)
> **Engine:** Unity 6 LTS (URP)
> **Language:** C#
> **Target:** iOS (primary)

---

## Sprint 0: Foundation ✅ DONE

- [x] GDD.md — Full Game Design Document
- [x] IDEAS.md — Future concepts log
- [x] Assets/Scripts/HexGrid.cs — 8×8 hex grid with axial coordinates, distance, neighbors, LoS
- [x] Assets/Scripts/Unit.cs — State machine (Ready/Acted/Exhausted), armor HP, action system
- [x] Assets/Scripts/TurnManager.cs — Turn phases, 2 actions/turn, Overwork mechanic
- [x] Assets/Scripts/AIDirector.cs — Priority-based AI (5 tiers)
- [x] Committed and pushed to GitHub

---

## Sprint 1: Visual Grid & Unit Placement

**Goal:** See the board and pieces when pressing Play.

### Tasks

#### 1.1 Create HexTileGenerator.cs
- **File:** `Assets/Scripts/HexTileGenerator.cs`
- Procedurally generate flat-top hex meshes at runtime
- Color palette: warm sandy base, slightly darker raised borders
- Subtle color variation between tiles (not a flat carpet)
- Use URP Lit shader for lighting

#### 1.2 Create UnitVisual.cs
- **File:** `Assets/Scripts/UnitVisual.cs`
- Each unit gets a board-game-token look:
  - Small circular base/stand
  - Body shape made from stacked primitives (cylinder, sphere, cube)
  - Player units: warm blues/teals
  - Enemy units: dusty reds/browns
- David: recognizable commander shape (taller, cape-like shoulder pieces)
- Swordsman: blocky with small sword (thin box)
- Spearman: similar with longer spear piece
- Slinger: smaller, crouched shape
- Scout: small, slim shape
- Amalekite variants: same shapes but red/brown palette

#### 1.3 Create GameSetup.cs
- **File:** `Assets/Scripts/GameSetup.cs`
- Spawns initial battle on Start():
  - Player: David + 2 Scouts at one side of grid
  - Enemy: Amalekite Chieftain + 1 Raider + 1 Slinger + 1 Scout at opposite side
- Registers all units with TurnManager
- Positions units at valid hex coordinates

#### 1.4 Camera Setup
- Orthographic camera, top-down angled view (isometric-ish)
- Adjustable zoom for mobile (pinch-to-zoom later)
- Centers on the grid

#### 1.5 Wire into SampleScene
- Replace default scene content
- Add HexGrid, TurnManager, AIDirector, GameSetup to scene
- Press Play → see 8×8 hex grid with units positioned

### Acceptance Criteria
- [ ] 8×8 hex grid visible with colored tiles
- [ ] David + 2 Scouts visible on left side
- [ ] 4 Amalekites visible on right side
- [ ] Camera shows the full board
- [ ] No errors in console

---

## Sprint 2: Selection & Movement

**Goal:** Tap a unit, see valid moves, move it.

### Tasks

#### 2.1 Unit Selection
- Tap/click a friendly unit → highlight it (glow ring or outline)
- Deselect by tapping empty space or another friendly unit
- Show unit info (name, HP, current state) in a small UI panel

#### 2.2 Movement Visualization
- When a unit is selected, show valid movement hexes
- Movement range = highest Move value in unit's current state actions
- Valid hexes highlighted with translucent green overlay
- Hexes occupied by other units are blocked

#### 2.3 Movement Execution
- Tap a highlighted hex → unit moves there
- Movement consumes the unit's action (calls unit.Act())
- Update TurnManager action count
- If no actions remain, auto-end turn

#### 2.4 Pathfinding
- Simple A* or BFS pathfinding on hex grid
- Path follows valid hexes, avoids obstacles/units
- Animate unit sliding along path (lerp)

### Acceptance Criteria
- [ ] Tap friendly unit → selected with visual indicator
- [ ] Valid move hexes shown in green
- [ ] Tap valid hex → unit moves there
- [ ] Movement consumes action
- [ ] Cannot move through or onto occupied hexes

---

## Sprint 3: Combat & Turn Flow

**Goal:** Attack enemies and see turns cycle.

### Tasks

#### 3.1 Attack Targeting
- When a unit is selected, show valid attack targets
- Valid targets = enemies within range of any Ready-state action
- Highlight valid targets with red outline/overlay
- Tap valid target → show available actions (e.g., "Sword (dmg 2)", "Spear Thrust (dmg 2)")

#### 3.2 Attack Execution
- Select action → unit performs attack
- Show damage number popup (floating text)
- Update target's HP bar
- If target dies, remove from grid and unregister from TurnManager

#### 3.3 End Turn Button
- "End Turn" button in UI
- Ends player turn, triggers AI turn
- AI turn executes (AIDirector processes each enemy unit)
- After AI turn, player turn starts again

#### 3.4 Turn UI
- Show current turn phase (Player/AI)
- Show remaining actions counter
- Show which units have acted (greyed out or dimmed)

### Acceptance Criteria
- [ ] Select unit → valid attack targets highlighted
- [ ] Tap target → choose action → damage applied
- [ ] Dead units removed from grid
- [ ] End Turn button works
- [ ] AI takes its turn automatically
- [ ] Turns cycle correctly

---

## Sprint 4: Overwork & Commander Mechanics

**Goal:** David's special abilities work.

### Tasks

#### 4.1 Overwork Button
- After using both normal actions, if David hasn't acted, show "Overwork" button
- Clicking it activates David as a 3rd action
- David skips his entire next turn (no activation, no refresh)
- Visual indicator: David is greyed out next turn

#### 4.2 Commander Aura
- David provides adjacent allies +1 damage
- Show aura range visually (subtle ring around David)
- Damage bonus applied when attacking from adjacent tile
- Enemy Chieftain has same aura for Amalekites

#### 4.3 Commander Death
- If David dies → Defeat screen immediately
- If Chieftain dies → Victory screen immediately
- Game over screen with "Run Again" button

### Acceptance Criteria
- [ ] Overwork available after 2 actions if David hasn't acted
- [ ] David skips next turn after Overwork
- [ ] Adjacent allies get +1 damage indicator
- [ ] Commander death ends game immediately
- [ ] Victory/Defeat screen shown

---

## Sprint 5: Rewards & Run Structure

**Goal:** Chain battles into a full run.

### Tasks

#### 5.1 Victory Screen
- After winning a battle, show Victory screen
- Display: surviving units, any upgrades earned
- "Continue" button → reward selection

#### 5.2 Reward Picker
- Show 3 random options from reward pools:
  - Recruit new unit (random from available types)
  - Upgrade existing unit (random eligible unit gets +1 HP or new action)
  - Improve equipment (random unit gets weapon upgrade)
  - Gain supplies (heal all units by 1 HP)
- Player picks one
- Apply reward immediately

#### 5.3 Run State
- Track units, their HP, upgrades across battles
- Carry over surviving units to next battle
- Scale enemy difficulty per battle (more enemies, tougher types)

#### 5.4 Battle Progression
- Battle 1: Easy (3 enemies + chieftain)
- Battle 2: Medium (4 enemies + chieftain + 1 elite)
- Battle 3: Hard (5 enemies + chieftain + 2 elites)
- Boss: Unique scenario (e.g., "Survive 6 turns" or "Kill boss unit with 5 HP")

#### 5.5 Defeat Screen
- If David dies or all units wiped → Defeat screen
- Show stats (battles won, units recruited, enemies killed)
- "New Run" button → restart from Battle 1

### Acceptance Criteria
- [ ] Victory → reward picker with 3 options
- [ ] Reward applied correctly
- [ ] Units carry over to next battle with HP intact
- [ ] 3 battles + boss playable in sequence
- [ ] Defeat → restart option

---

## Sprint 6: Unit Data & Balance

**Goal:** All units exist as real data, game is balanced.

### Tasks

#### 6.1 ScriptableObject Unit Data
- **File:** `Assets/Scripts/UnitData.cs` (ScriptableObject)
- Each unit type defined as data asset:
  - Unit name, armor tier, state actions per state
  - Visual shape/color preferences
- Create assets for all 6 player types and 6 Amalekite types

#### 6.2 Encounter Definitions
- **File:** `Assets/Scripts/EncounterData.cs` (ScriptableObject)
- Define which enemies appear in each battle
- Define starting positions
- Define victory conditions (eliminate commander, survive, etc.)

#### 6.3 Balance Pass
- Tune damage numbers, move ranges, HP values
- Ensure battles are winnable but challenging
- Test all 6 player unit types feel useful
- Test all 6 Amalekite types feel distinct

### Acceptance Criteria
- [ ] All 12 unit types defined as ScriptableObjects
- [ ] Encounters configurable via data assets
- [ ] Game is playable and winnable
- [ ] No obviously broken unit or encounter

---

## Sprint 7: Mobile & UI Polish

**Goal:** Feels like a mobile game, build for iOS.

### Tasks

#### 7.1 Touch Input
- All interactions work with touch (tap, drag, pinch)
- No mouse-only dependencies
- Touch-friendly UI element sizes (min 44px tap targets)

#### 7.2 UI Scaling
- UI scales properly for phone screens (9:16 aspect ratio)
- Safe area handling for notches
- Font sizes readable on small screens

#### 7.3 UI Polish
- End Turn button, action counter, unit info panel
- HP bars on units (world-space or screen-space)
- Turn transition animation (fade or slide)
- Simple sound effects (optional, can add later)

#### 7.4 iOS Build
- Build for iOS TestFlight
- Test on device
- Fix any device-specific issues

### Acceptance Criteria
- [ ] Full touch input support
- [ ] UI works on phone-sized screens
- [ ] iOS build succeeds
- [ ] Game runs on device without crashes

---

## Post-MVP (Future Sprints)

These are captured in `IDEAS.md` and are not part of the MVP roadmap:

- Counter-attacks
- Terrain bonuses
- Fog of war
- Campaign map
- Story events
- Additional factions (Philistines, Saul's army)
- The Mighty Men (hero units)
- Equipment crafting
- Morale system
- Sound effects & music
- Leaderboards
- Android / Steam / Web ports

---

## Development Philosophy

> **Finish something fun before making it big.**

Every feature must answer:
> *"Does this make the tactical decisions more interesting?"*

If not, don't build it.
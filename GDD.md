# The Anointed Exile — Game Design Document

> **Working Title:** David (Project Codename)
> **Engine:** Unity 6 LTS (URP)
> **Language:** C#
> **Target Platform:** iOS (primary), Android, Steam, Web (future)

---

## Vision

A tactical strategy game inspired by **The Duke**, with the progression and replayability of **Slay the Spire**, set during David's years as a fugitive before becoming king.

### Core Pillars
- Easy to learn
- Deep tactical gameplay
- High replayability
- Historically grounded (not fantasy)
- Small enough for a solo developer

---

## Target Platform & Tech Stack

| | |
|---|---|
| **Primary** | iOS |
| **Future** | Android, Steam, Web |
| **Engine** | Unity 6 LTS (URP) |
| **Language** | C# |
| **AI Workflow** | VS Code, Cline, Ollama (Qwen2.5-Coder), GitHub |

---

## Theme

**Time Period:** David while fleeing Saul (c. 1 Samuel 18–31).

**Possible Locations:**
- Cave of Adullam
- Wilderness of Judah
- Ziklag
- Amalekite territory
- Philistine borderlands

---

## Factions & Scenario Participants

The game is built around a **skirmish-first** philosophy. Factions have distinct rosters and playstyles. A campaign layer is built on top later, using the same faction rosters.

### Core Player Faction: David's Company

David's warband of refugees, outcasts, and loyal fighters. Flexible underdog playstyle. The only faction with the Command Card deck system.

| Unit | Type | Notes |
|---|---|---|
| David | Commander | Unique — always available |
| Refugees | Support | Non-combatants, provide passive bonuses |
| Outcasts | Light Infantry | Desperate fighters, cheap |
| Swordsmen | Infantry | Standard melee |
| Spearmen | Infantry | Reach, anti-charge |
| Slingers | Skirmisher | Ranged, light |
| Archers | Ranged | Stationary damage |
| Scouts | Light | Fast, hit-and-run |
| Veterans | Elite | Upgraded base units (campaign) |
| Mighty Men | Hero | Unique named units (late campaign) |

### Primary Factions

#### Saul's Kingdom (Enemy → Neutral → Ally)
Relationship varies by scenario. Often pursuing David. Sometimes fights common enemies.

| Unit | Type | Notes |
|---|---|---|
| Abner | Commander | Saul's general |
| Royal Guard | Heavy Infantry | Iron armor, shield wall |
| Benjamite Spearmen | Elite Infantry | Better spearmen, loyal tribe |
| Israelite Archers | Ranged | Standard archers |
| Officers | Support | Buff adjacent units |
| Elite Bodyguards | Elite | Protect Saul/Abner |

#### Jonathan's Followers (Ally)
Small temporary allied force. Scenario-specific.

| Unit | Type | Notes |
|---|---|---|
| Loyal Guards | Infantry | Devoted to Jonathan |
| Elite Archers | Ranged | Crack shots |
| Scouts | Light | Fast, intel |

#### Philistines (Enemy OR Ally)
David serves Achish for a time. Later they become enemies again.

| Unit | Type | Notes |
|---|---|---|
| Achish | Commander | Philistine lord |
| Spearmen | Infantry | Standard |
| Heavy Infantry | Heavy | Slow, hit hard |
| Archers | Ranged | Standard |
| Chariots | Unique | Rare, devastating |
| Champions | Elite | Duelists |
| Lords of the Philistines | Commander variants | Scenario-specific |

#### Amalekites (Enemy)
Fast-moving desert raiders. Major campaign enemy. Raid Ziklag.

| Unit | Type | Notes |
|---|---|---|
| Chieftain | Commander | |
| Raiders | Infantry | Core melee |
| Slingers | Skirmisher | Ranged |
| Desert Scouts | Light | Fast skirmishers |
| Camel Riders | Unique | Mobile heavy |

### Minor Historical Peoples (Enemy — Expansion)

#### Girzites (Girzites/Gizzites)
Mentioned in 1 Samuel 27. David raids them while living among the Philistines. Very little historical information survives. Good opportunity for tasteful historical reconstruction.

#### Geshurites (Southern Geshurites)
Also mentioned in 1 Samuel 27. NOT the northern Kingdom of Geshur near Bashan. Likely desert or semi-desert tribal people.

#### Gezerites
Some Bible translations read "Gezrites." Textual tradition is debated. Could be treated as another small tribal group.

### Optional / Late Campaign

#### Judah Militia (Ally)
Local village defenders, shepherd militia, and levies.

| Unit | Type | Notes |
|---|---|---|
| Local Leader | Commander | |
| Village Defender | Infantry | Light armor, motivated |
| Shepherd | Skirmisher | Staff/sling, basic |

#### Keilah (Ally → Neutral)
David rescues Keilah. Later they are willing to hand him over to Saul. Could appear as a scenario-specific allied force or objective.

#### Nabal's Household (Neutral)
Could appear in diplomacy scenarios. Abigail eventually becomes David's wife.

#### Priests of Nob (Ally)
Supply/support scenarios. Historically significant for sheltering David.

### Scenario-Only Participants

These aren't full factions — they appear as objectives or environmental elements.

**Civilians:**
- Shepherds
- Farmers
- Families
- Merchants

**Wildlife:**
- Lions
- Bears
- Wolves (optional)

### Scenario Objectives

Beyond "eliminate commander," scenarios can have varied objectives:

- **Eliminate** — Defeat the enemy commander
- **Rescue captives** — Reach and free allied prisoners
- **Escort civilians** — Guide non-combatants to safety
- **Recover livestock** — Capture resources from enemy camp
- **Burn supplies** — Destroy enemy provisions
- **Defend position** — Survive for N turns
- **Escape pursuit** — Reach the opposite edge of the map
- **Ambush patrol** — Eliminate a moving enemy unit before it escapes
- **Breakthrough** — Get a specific unit to the opposite side

### MVP Recommendation

| Status | Factions |
|---|---|
| **Playable (MVP)** | David's Company, Saul's Army, Amalekites |
| **Scenario allies** | Jonathan's Men, Philistines (select scenarios) |
| **Expansion** | Girzites, Southern Geshurites, Judah Militia, Keilah |
| **Late campaign** | Nabal's Household, Priests of Nob, Philistines (full), Mighty Men |

---

## Recommended Loadouts (Skirmish Mode)

Pre-set team + card deck combinations for balanced pick-up games — inspired by **ROOT's** recommended setups. These are the quickest way to get playing.

| Loadout | Player Faction | Enemy Faction | Player Units | Objective | Difficulty |
|---|---|---|---|---|---|
| **First Blood** | David's Company | Amalekites | David + 2 Scouts + 2 Spearmen | Eliminate chieftain | Easy |
| **Desert Pursuit** | David's Company | Amalekites | David + Swordsman + Archer + Slinger | Eliminate chieftain | Medium |
| **Hold the Pass** | David's Company | Amalekites | David + 3 Spearmen + Archer | Defend (survive 6 turns) | Medium |
| **Rescue at Keilah** | David's Company | Saul's Army | David + Scout + 2 Swordsmen + Refugee | Escort civilians to safety | Hard |
| **Escape Pursuit** | David's Company | Saul's Army | David + Scout + Refugee | Reach the opposite map edge | Hard |
| **Ziklag Raid** | David's Company | Amalekites | David + 2 Veterans + Slinger + Refugee | Rescue captives | Hard |
| **The Anointed** | David's Company | Philistines | David + Swordsman + Spearman + Archer + Scout | Eliminate commander | Very Hard |

### Loadout Format
Each loadout defines:
- **Player faction** (always David's Company for MVP — other factions later)
- **Enemy faction** (Amalekites, Saul's Army, Philistines)
- **Player starting units** (which units + how many)
- **Starting deck** (which Command Cards — default is the full 10-card deck unless specified)
- **Scenario objective** (eliminate, rescue, escort, defend, escape, ambush)

---

## Inspirations

| | |
|---|---|
| **Combat** | The Duke (tactical grid, unit states) |
| **Campaign** | Slay the Spire (progression, replayability) |
| **Presentation** | Modern board game, 2.5D / Isometric |

---

## Core Gameplay Loop

```
Start Run
    ↓
Travel to encounter
    ↓
Fight tactical battle
    ↓
Receive reward
    ↓
Recruit / Upgrade / Deck Improvement
    ↓
Next encounter
    ↓
Boss
    ↓
Win or Lose
    ↓
Start another run
```

---

## Tactical Battles

- **Grid:** 8×8 hex grid
- **Player controls:** David + warband via Command Cards
- **Enemy controls:** AI commander + troops
- **Goal:** Defeat enemy commander OR complete scenario objective

### Turn Structure

```
Start Turn
    ↓
Draw until hand contains 4 Command Cards
(first turn: start with 2, draw 2)
LOSE one random card (Fatigue)
    ↓
Choose 2 Command Cards from hand
    ↓
Reveal both cards
    ↓
Resolve:
  • Top ability of one card
  • Bottom ability of the other card
  (Each ability activates ONE unit — activation token placed)
    ↓
Discard both cards to Spent pile
(or Lose pile if specified)
    ↓
Enemy Turn
```

### Unit Limitation Rule

Each unit can generally activate only **once per player turn**. When a unit activates, place an activation token on it. It cannot activate again until the next player turn.

This prevents:
- Moving the same powerful units repeatedly.
- Ignoring half the army.
- "Favorite three units" strategies.

---

## Battle Command System

### Design Philosophy

- **Units** answer: *"Who am I?"*
- **Cards** answer: *"What orders am I giving?"*

The interesting decisions come from:
- Which two commands to select from your hand
- Which half of each command to use (top or bottom)
- Which unit executes the command
- Whether a powerful command is worth losing forever

### Command Deck Setup

Before a scenario:
1. Choose your commander/faction.
2. Choose your army units.
3. Add command cards based on the units brought.

Example:
David + 3 Swordsmen + 2 Archers + 1 Scout

Command deck:
- David Leadership cards
- Swordsman command cards
- Archer command cards
- Scout command card

### Card Design

Each command card has:
- **TOP ACTION:** Primary command ability. Usually stronger or more specialized.
- **BOTTOM ACTION:** Secondary command ability. Usually movement, positioning, support, or weaker action.

### Universal Commands

Every army has access to basic commands:

- **March:** Activate up to 2 units of one type. Move them.
- **Engage:** Activate up to 2 units of one type. They attack.

Universal commands are weaker than specialized commands.

### Card States

```
Deck
  ↓
Hand
  ↓
Played
  ↓
Spent
  ↓
Refresh
  ↓
Deck
```

Some powerful abilities instead go:

```
Played
  ↓
Lost
```

Lost cards do not return until a battle recovery (or a special ability recovers them).

### Starting Hand

The player starts the game with **2 Command Cards** in hand. On the first turn, draw 2 more (hand of 4). Each subsequent turn, draw up to 2 to refill the hand back to 4.

### Fatigue / Command Loss

When refreshing your command hand:
- Draw back up according to your hand rules.
- Lose one random card.

Represents:
- Commander fatigue.
- Loss of communication.
- Soldiers becoming harder to coordinate.

### Casualty System

When a unit type is eliminated:
- Remove one matching command card from the deck.

Example:

All David archers are destroyed.

Remove:
"Archer Volley"

Effect:
- Your army loses tactical options as it suffers losses.

### Co-op / AI Possibility

Human-controlled faction:
- Draw cards.
- Choose best actions.

AI-controlled faction:
- Reveal command cards randomly.
- Execute the top action first.
- Follow simple priority rules.

Priority rules:
1. Attack if possible.
2. Move toward objective/enemy.
3. Support nearby allies.
4. If unable, reposition.

### Command Cards

Cards represent David's battlefield orders. Each card has a **Top** ability and a **Bottom** ability. When resolving a turn, the player picks one card's top ability and the other card's bottom ability.

Examples:

**Swordsmen Advance**
```
Top:
  Activate Swordsmen:
  - Up to 3 Swordsmen may move and attack.
  - Gain +1 attack if adjacent to another Swordsman.

Bottom:
  Move:
  - Move up to 2 Swordsmen.
```

**Archer Volley**
```
Top:
  Activate Archers:
  - Up to 2 Archers attack.
  - Must target enemies within range.

Bottom:
  Reposition:
  - Move up to 2 Archers.
```

---

## Units — Player Roster (MVP)

Units have fixed base stats. Actions are enhanced by Command Cards.

### David (Commander)
| Stat | Value |
|---|---|
| **HP** | 2 (Bronze) |
| **Move** | 2 |
| **Attack** | Melee dmg 2 |
| **Range** | 1 |
| **Passive** | Adjacent allies +1 damage (Commander Aura) |
| **Special** | Lose David = lose battle |

### Swordsman
| Stat | Value |
|---|---|
| **HP** | 2 (Bronze) |
| **Move** | 2 |
| **Attack** | Melee dmg 2 |
| **Range** | 1 |
| **Passive** | Shield Block (defend once per turn) |

### Spearman
| Stat | Value |
|---|---|
| **HP** | 2 (Bronze) |
| **Move** | 2 |
| **Attack** | Spear Thrust dmg 2 |
| **Range** | 2 |
| **Passive** | Brace (bonus dmg vs charging enemies) |

### Slinger
| Stat | Value |
|---|---|
| **HP** | 1 (Leather) |
| **Move** | 2 |
| **Attack** | Sling dmg 1 |
| **Range** | 3 |
| **Passive** | — |

### Archer
| Stat | Value |
|---|---|
| **HP** | 1 (Leather) |
| **Move** | 2 |
| **Attack** | Bow Shot dmg 2 |
| **Range** | 3 |
| **Passive** | Aim (next shot +1 dmg if stationary) |

### Scout
| Stat | Value |
|---|---|
| **HP** | 1 (Leather) |
| **Move** | 3 |
| **Attack** | Javelin dmg 1 |
| **Range** | 2 |
| **Passive** | Retreat (gain +1 Move when disengaging) |

---

## Units — Enemy Roster (Amalekites)

Historically nomadic raiders. Lightly armored, mobile. No heavy infantry.

### Amalekite Scout
| Stat | Value |
|---|---|
| **HP** | 1 (Leather) |
| **Move** | 3 |
| **Attack** | Javelin dmg 1 |
| **Range** | 2 |
| **Passive** | Retreat |

### Amalekite Raider (core melee)
| Stat | Value |
|---|---|
| **HP** | 2 (Bronze) |
| **Move** | 2 |
| **Attack** | Spear Thrust dmg 2 |
| **Range** | 2 |
| **Passive** | Shield Wall (defend) |

### Amalekite Slinger
| Stat | Value |
|---|---|
| **HP** | 1 (Leather) |
| **Move** | 2 |
| **Attack** | Sling dmg 1 |
| **Range** | 3 |
| **Passive** | — |

### Amalekite Archer (mounted)
| Stat | Value |
|---|---|
| **HP** | 2 (Bronze) |
| **Move** | 3 |
| **Attack** | Bow Shot dmg 2 |
| **Range** | 3 |
| **Passive** | Parthian Shot (move 1 + shoot, dmg 1) |

### Camel Rider (unique heavy)
| Stat | Value |
|---|---|
| **HP** | 3 (Iron) |
| **Move** | 3 |
| **Attack** | Spear dmg 2 / Trample dmg 2 (pushes target 1 tile) |
| **Range** | 2 |
| **Passive** | Trample |

### Amalekite Chieftain (commander)
| Stat | Value |
|---|---|
| **HP** | 2 (Bronze) |
| **Move** | 2 |
| **Attack** | Melee dmg 2 |
| **Range** | 1 |
| **Passive** | Command (rally adjacent exhausted ally → ready), War Cry (adjacent allies +1 dmg this turn) |
| **Special** | Lose Chieftain = lose battle |

---

## Combat System

### Health
Simple armor-based tiers:

| Armor | HP | Examples |
|---|---|---|
| Leather | 1 | Scouts, Slingers, Archers |
| Bronze | 2 | Swordsmen, Spearmen, Raiders |
| Iron | 3 | Camel Rider, Elite units |

No complex RPG stats.

### Damage
- Leather sword: Damage 1
- Bronze spear: Damage 2
- Iron sword: Damage 3
- Keep combat readable and predictable.

### Ranged Attacks
- Line-of-sight required
- Blocked by units and obstacles
- Uses Bresenham's line algorithm for LoS checking

### Melee Attacks
- Adjacent by default
- Spearmen have range 2 melee (reach)
### Counter-Attacks
- **NOT in MVP**
- Future consideration: specific units/equipment can have counter-attack as a perk

### Commander Mechanic
- David provides adjacent allies +1 damage (commander aura)
- Lose David = lose the battle (immediate defeat)
- Enemy Chieftain behaves identically

---

## Progression & Rewards

### After Each Battle
Choose **ONE** from a random pool:
1. Recruit new unit
2. Upgrade existing unit (e.g., Young Slinger → Veteran Slinger → Elite Slinger)
3. Improve equipment (Wood → Bronze → Iron)
4. Gain supplies (heal wounded units)
5. **Improve Command Deck** (add a new card, upgrade an existing card, or recover a Lost card)

No random loot explosion. Meaningful choices.

### Duplicates
Allowed — you can have multiple swordsmen, slingers, etc.

### Upgrade Path Example
```
Young Slinger
    ↓
Veteran Slinger (more HP, longer range)
    ↓
Elite Slinger (new actions, passive abilities)
```

---

## Run Structure (MVP)

| Encounter | Difficulty | Est. Time |
|---|---|---|
| Battle 1 | Easy — 3 enemies + chieftain | ~5 min |
| Battle 2 | Medium — 4 enemies + chieftain | ~7 min |
| Battle 3 | Hard — 5 enemies + chieftain + elite | ~10 min |
| Boss | Unique scenario | ~10 min |
| **Total** | | **~30 min** |

---

## AI Design

Priority-based evaluation each turn:

1. **Protect commander** — If commander is threatened (enemy within 2 tiles), move to protect or retreat commander
2. **Attack weak units** — Target isolated or low-HP player units
3. **Capture objectives** — If scenario has objectives, move toward them
4. **Focus isolated enemies** — Prioritize units with no nearby allies
5. **Retreat when appropriate** — If HP < 30% and no advantage, fall back toward commander

---

## Art Style

- **2.5D / Isometric** perspective
- **Parchment / illuminated manuscript aesthetic**
- Hand-painted historical illustration style
- Watercolor and ink outlines
- Muted earth tones
- NOT realistic. NOT fantasy.
- Inspired by ancient chronicles, illustrated manuscripts, and board game card art
- Readable over realistic
- Units rendered as small tokens on the battlefield
- Selecting a unit opens a command card (like a playing card)

---

## MVP Feature Checklist

- [x] Hex grid (8×8)
- [x] Click/tap movement
- [x] Unit selection
- [x] Enemy AI (priority-based)
- [x] Basic attacks (melee & ranged)
- [x] Health system (Leather/Bronze/Iron)
- [x] **Command Card deck & hand management**
- [ ] Card draw system (draw to 4 each turn)
- [ ] Card selection UI (pick 2 from hand)
- [ ] Top/bottom card resolution
- [ ] Spent & Lost card piles
- [x] Turn system (card-based player turn → enemy turn)
- [x] Victory conditions (eliminate commander)
- [x] Recruitment & upgrades (including deck improvement)
- [x] Run structure (3 battles + boss)

---

## NOT in MVP

- Kingdom management
- Crafting
- Diplomacy
- Base building
- Multiplayer
- Voice acting
- Cutscenes
- Large campaign map
- Complex economy
- Counter-attacks
- Terrain bonuses
- Fog of war

---

## Long-Term Ideas

- The Mighty Men (elite units)
- David vs Saul campaign
- Philistine campaign
- Amalekite campaign
- Story events
- Equipment crafting
- Morale system
- Terrain bonuses
- Fog of war
- Campaign map
- Boss encounters
- Counter-attack perks
- Unit-specific abilities

---

## Development Philosophy

> **Finish something fun before making it big.**

Every feature must answer:
> *"Does this make the tactical decisions more interesting?"*

If not, don't build it.

---

## Sprint Roadmap

See `ROADMAP.md` for the full development plan from Sprint 0 through MVP.

### Summary

| Sprint | Focus | Status |
|---|---|---|
| 0 | Foundation (GDD, core scripts) | ✅ Done |
| 1 | Visual grid & unit placement | ✅ Done |
| 2 | Selection & movement | ✅ Done |
| 3 | Command Card data system | ⬜ Not started |
| 4 | Command Card UI & selection | ⬜ Not started |
| 5 | Card resolution & unit linking | ⬜ Not started |
| 6 | Updated turn flow & enemy AI | ⬜ Not started |
| 7 | Campaign, deck rewards, & polish | ⬜ Not started |

---

# Open Design Questions

---

# Phase 1: Must Answer Before First Prototype

## 1. What is the basic unit structure?

Decide:

- Is a miniature always one warrior?
- Is a miniature a squad?
- Does a "Spearman Order" control one spearman or multiple?

Questions:

- Does 1 card = 1 unit?
- Does 1 card = a squad of similar units?
- How does a larger force gain advantage without creating bookkeeping?

---

## 2. What are the core unit stats?

Finalize the minimum stat line.

Possible:

- Health
- Movement
- Attack
- Defense
- Range
- Initiative
- Keywords

Avoid unnecessary stats.

---

## 3. How does activation work exactly?

When an Order says:

"Activate up to 2 Spearmen"

What happens?

Questions:

- Can the same unit activate twice?
- Can units split movement and attacks?
- Can activated units trigger reactions afterward?
- Do units have exhaustion states?

---

## 4. How does combat resolve?

Finalize:

- Attack sequence.
- Defense sequence.
- Retaliation.
- Damage.
- Critical hits.
- Misses.
- Attack Modifier Deck effects.

---

## 5. How much randomness is desired?

Current options:

A. Shared Attack Modifier Deck

B. Dice

C. Hybrid

Need to decide:

- How much should planning overcome luck?
- How swingy should combat feel?

---

## 6. What does a card actually contain?

Finalize Order card structure.

Example:

Initiative number

TOP:
- Action

BOTTOM:
- Action

Questions:

- Unit requirement?
- Range?
- Keywords?
- Persistent ability?
- Flavor text?

---

# Phase 2: Command System

## 7. Is drawing 2 Orders enough?

Test:

- Draw 2 every round.
- Hand limit 4.
- Extra draw effects.

Questions:

- Do players feel starved?
- Do players feel forced into repetition?
- Are extra draw abilities exciting?

---

## 8. How does Brainstorm trigger?

Current:

"When unable to draw enough Orders."

Need to define:

- Is it automatic?
- Can players choose it early?
- Can players intentionally discard to trigger it?

---

## 9. How does Regroup work?

Finalize:

- How much healing?
- Does every unit heal?
- Does it remove conditions?
- Can enemies interrupt it?

---

## 10. How are Lost Orders handled physically?

Need final elegant solution.

Options:

- Remove immediately.
- Flip card.
- Unit board slots.
- Separate casualty area.

Goal:

No deck searching.

---

# Phase 3: Army Building

## 11. How are armies created?

Need:

- Point system?
- Scenario lists?
- Campaign roster?
- Commander limits?

---

## 12. How is command value balanced?

Because command matters as much as units.

Need formula for:

Army strength =
- Unit value
- Commander value
- Order quantity
- Tactical flexibility

---

## 13. How many commanders can an army have?

Questions:

- One commander per faction?
- Captains?
- Mighty Men as secondary commanders?

---

# Phase 4: Enemy AI

## 14. How does solo/co-op enemy AI work?

Need:

- Behavior rules.
- Enemy Orders.
- Priority system.

Examples:

Philistines:
Advance and overwhelm.

Amalekites:
Strike isolated targets and retreat.

Saul:
Protect formation and pursue objectives.

---

## 15. Does AI use Orders?

Options:

A.
AI has its own Orders Deck.

B.
AI uses behavior cards.

C.
AI uses priority rules.

---

# Phase 5: Scenarios

## 16. What is the default victory condition?

Avoid every battle being:

"Kill everyone."

Need:

- Escape.
- Survival.
- Rescue.
- Ambush.
- Capture.
- Delay.

---

## 17. What makes scenarios replayable?

Need:

- Random events?
- Enemy deployment?
- Objectives?
- Terrain variation?

---

# Phase 6: Campaign

## 18. How does Influence work?

Define:

Gain Influence from:

- Victory.
- Objectives.
- Protecting allies.
- Low casualties.

Spend Influence on:

- Recruitment.
- New units.
- New Orders.
- Mighty Men.

---

## 19. How does progression work?

Avoid simple +1 bonuses.

Options:

- New Orders.
- New formations.
- New followers.
- New commanders.

---

## 20. How long is a campaign?

Need target:

- Short campaign?
- Full David exile campaign?
- Multiple books/expansions?

---

# Phase 7: Content

## 21. What is the first playable faction set?

Current:

- David
- Saul
- Philistines
- Amalekites

Need:

- Unit lists.
- Commanders.
- Orders.

---

## 22. What is the first scenario?

Need one "proof of concept" battle.

Ideal:

- Uses movement.
- Uses reactions.
- Uses terrain.
- Uses command decisions.

---

# Phase 8: Presentation

## 23. How much biblical flavor?

Need decide:

- Historical simulation?
- Biblical adventure?
- Tactical game inspired by Scripture?

---

## 24. How are faith elements handled?

Guiding principle:

Do not turn faith into a resource.

Need define:

- How miracles/events are represented.
- How providence is handled.
- What is thematic versus mechanical.

---

# 25. What is the game's unique hook?

Current candidate:

"The army is your command deck."

Need validate through playtesting.

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

**Time Period:** David while fleeing Saul.

**Possible Locations:**
- Cave of Adullam
- Wilderness of Judah
- Ziklag
- Amalekite territory
- Philistine borderlands

**Enemy Factions:**
- Amalekites (MVP faction)
- Philistines (future)
- Saul's soldiers (future)
- Bandits (future)

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
Recruit / Upgrade / Equipment
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
- **Player controls:** David + warband
- **Enemy controls:** AI commander + troops
- **Goal:** Defeat enemy commander OR complete scenario objective

### Turn Structure

1. **Player Turn** — 2 team actions
2. Each action = activate one unit (move + attack OR special)
3. A unit can only activate **once per turn** (regardless of state)
4. **Overwork (David only):** Spend a 3rd action with David. David skips his **entire next turn** (no activation, no refresh)
5. End turn
6. **AI Turn** — Same structure
7. **Refresh Phase** — All units advance one state toward Ready

### Unit State Machine

Units have 1–3 states (most common: 2). Flow:

```
READY
  ↓  (unit acts)
ACTED (optional, for 3-state units)
  ↓
EXHAUSTED
  ↓  (refresh)
READY
```

---

## Units — Player Roster (MVP)

### David (Commander)
| State | Actions |
|---|---|
| **Ready** | Move (2), Sword (dmg 2), Inspire (adjacent allies +1 dmg this turn) |
| **Acted** | Move (1), Sword (dmg 2) |
| **Exhausted** | Move (1), Weak Melee (dmg 1) |
| **HP:** 2 (Bronze) | **Special:** Lose David = lose battle |

### Swordsman
| State | Actions |
|---|---|
| **Ready** | Move (2), Sword (dmg 2), Shield Block (defend) |
| **Exhausted** | Move (1), Melee (dmg 1) |
| **HP:** 2 (Bronze) |

### Spearman
| State | Actions |
|---|---|
| **Ready** | Move (2), Spear Thrust (range 2, dmg 2), Brace (bonus dmg vs charging enemies) |
| **Exhausted** | Move (1), Melee (dmg 1) |
| **HP:** 2 (Bronze) |

### Slinger
| State | Actions |
|---|---|
| **Ready** | Move (2), Long Shot (range 3, dmg 1), Sling Volley (range 2, dmg 2, can't move same turn) |
| **Exhausted** | Move (1), Reload, Weak Melee (dmg 1) |
| **HP:** 1 (Leather) |

### Archer
| State | Actions |
|---|---|
| **Ready** | Move (2), Bow Shot (range 3, dmg 2), Aim (next shot +1 dmg) |
| **Exhausted** | Move (1), Weak Shot (range 2, dmg 1) |
| **HP:** 1 (Leather) |

### Scout
| State | Actions |
|---|---|
| **Ready** | Move (3), Javelin (range 2, dmg 1), Retreat (2) |
| **Exhausted** | Move (2), Weak Melee (dmg 1) |
| **HP:** 1 (Leather) |

---

## Units — Enemy Roster (Amalekites)

Historically nomadic raiders. Lightly armored, mobile. No heavy infantry.

### Amalekite Scout
| State | Actions |
|---|---|
| **Ready** | Move (3), Javelin (range 2, dmg 1), Retreat (2) |
| **Exhausted** | Move (2), Weak Melee (dmg 1) |
| **HP:** 1 (Leather) |

### Amalekite Raider (core melee)
| State | Actions |
|---|---|
| **Ready** | Move (2), Spear Thrust (range 2, dmg 2), Shield Wall (defend) |
| **Exhausted** | Move (1), Melee (dmg 1) |
| **HP:** 2 (Bronze) |

### Amalekite Slinger
| State | Actions |
|---|---|
| **Ready** | Move (2), Long Shot (range 3, dmg 1), Sling Volley (range 2, dmg 2) |
| **Exhausted** | Move (1), Reload, Weak Melee (dmg 1) |
| **HP:** 1 (Leather) |

### Amalekite Archer (mounted)
| State | Actions |
|---|---|
| **Ready** | Move (3), Bow Shot (range 3, dmg 2), Parthian Shot (move 1 + shoot, dmg 1) |
| **Exhausted** | Move (2), Weak Shot (range 2, dmg 1) |
| **HP:** 2 (Bronze) |

### Camel Rider (unique heavy)
| State | Actions |
|---|---|
| **Ready** | Move (3), Trample (dmg 2, pushes target 1 tile), Spear (range 2, dmg 2) |
| **Exhausted** | Move (2), Melee (dmg 1) |
| **HP:** 3 (Iron) |

### Amalekite Chieftain (commander)
| State | Actions |
|---|---|
| **Ready** | Move (2), Command (rally adjacent exhausted ally → ready), War Cry (adjacent allies +1 dmg this turn) |
| **Acted** | Move (1), Melee (dmg 2) |
| **Exhausted** | Move (1), Weak Melee (dmg 1) |
| **HP:** 2 (Bronze) |

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
- David provides adjacent allies +1 damage
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
5. Unlock ability

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
- **Modern board game aesthetic**
- Stylized low-poly or flat-shaded
- Simple but polished
- Readable over realistic

---

## MVP Feature Checklist

- [x] Hex grid (8×8)
- [x] Click/tap movement
- [x] Unit selection
- [x] Enemy AI (priority-based)
- [x] Basic attacks (melee & ranged)
- [x] Health system (Leather/Bronze/Iron)
- [x] Unit states (Ready → Exhausted)
- [x] Turn system (2 actions per side)
- [x] Victory conditions (eliminate commander)
- [x] Recruitment & upgrades
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
# Plan: Playable Co-op Prototype
## David + Jonathan vs Philistines (Local Hotseat / Head-to-Head)

---

## Prototype Scope

**Support multiple play modes with a single ruleset:**
- **Co-op:** 2 players vs AI Philistines
- **1v1 Head-to-Head:** 1 player vs 1 player
- **2v2 Head-to-Head:** 2 players vs 2 players

**Commanders:** David, Jonathan, Achish, Philistine Lord
**Format:** Printable board game with unit discs, command cards, hex grid
**Philosophy:** Same core ruleset scales across modes. Army building and deck construction are identical; only the number of human sides changes.

**This is a prototype scope expansion.** The game now supports any combination of commanders, not just the co-op scenario.

---

## Core Design Rule: Unit Identity vs Command Card Differentiation

The game has two layers:

1. **Unit Profile** — what the soldier physically is, base stats, combat role
2. **Command Deck** — how the commander uses the unit, special tactics, faction identity

**Common Units:** Same or very similar base stats across factions. Personality comes from **Command Cards**.

**Signature Units:** Unique stats + unique Command Cards. Differentiate factions and feel distinct to play.

### Shared Unit Stats (Common Units)

| Unit | Range | Attack | Defense | Health | Move | Notes |
|---|---|---|---|---|---|---|
| Swordsman | 1 | 2 | 1 | 2 | 2 | Standard melee |
| Spearman | 2 (reach) | 2 | 1 | 2 | 2 | Anti-charge |
| Shield Bearer | 1 | 1 | 2 | 3 | 1 | Tank/defender |
| Heavy Infantry | 1 | 2 | 2 | 3 | 1 | Slow, hits hard |
| Scout | 2 | 1 | 1 | 1 | 3 | Fast recon |
| Refugee | 1 | 0 | 1 | 1 | 1 | Support/non-combat |
| Archer | 2 | 2 | 1 | 2 | 2 | Standard ranged |
| Loyal Guard | 1 | 2 | 1 | 2 | 2 | Jonathan's infantry |

### Signature Units (Unique Stats + Unique Cards)

#### David's Slingers ⭐
| Range | Attack | Defense | Health | Move |
|---|---|---|---|---|
| 3 | 1 | 1 | 2 | 3 |

Mobile skirmishers, David's iconic weapon. Long range, high mobility, harassment. Low damage, poor melee.

#### Jonathan's Elite Archers ⭐
Same as standard Archer (Range 2, Attack 2, Defense 1, Health 2, Move 2).  
Elite precision troops with specialized command cards.

#### Ekron Archers (Philistine)
Same as standard Archer. Battlefield support with coordinated volley cards.

#### Achish's Giants ⭐
| Range | Attack | Defense | Health | Move |
|---|---|---|---|---|
| 1 | 3 | 2 | 4 | 1 |

Gath's giant warriors. High health/damage, slow, vulnerable to being surrounded.

#### Ekron War Chariots ⭐
| Range | Attack | Defense | Health | Move |
|---|---|---|---|---|
| 1 | 2 | 1 | 2 | 3 |

Coastal plain warfare. High movement, charge attacks, open terrain dominance. Poor in rough terrain.

---

## Play Modes

### 1. Co-op (2 players vs AI)
- Players 1 + 2 form a single team
- Shared command deck, shared activation economy
- Deploy exactly 6 units total (including both commanders)
- Battle vs Philistine AI (2 commanders, 8 units)

### 2. 1v1 Head-to-Head
- Each player fields exactly 1 commander + 5 units = 6 units total
- Each player has their own deck
- Battle: player 1 vs player 2

### 3. 2v2 Head-to-Head
- Each player fields exactly 1 commander + 3 units = 4 units per side, 8 units total on board
- Each team shares a deck
- Battle: Team A vs Team B

### Shared Constraints (all modes)
- Each side must include **at least 3 different unit types**
- Deployment zones depend on number of players
- Deck construction follows the same random + limited-choice formula

### Deployment by Mode

| Mode | Player 1 | Player 2 | AI / Team 2 |
|---|---|---|---|
| Co-op | Left-center | Left-flank | Right side |
| 1v1 | Left side | Right side | — |
| 2v2 | Left side | Left side | Right side |

### Victory Condition
- **Co-op:** Eliminate both Philistine commanders
- **Head-to-Head:** Eliminate opponent's commander(s). If both commanders fall simultaneously, the player with more surviving units wins. If tied, it's a draw.

### Defeat Condition
- **Co-op:** Lose either David or Jonathan
- **Head-to-Head:** Lose your commander

### Faction/Commander Pairing
- Commanders can be paired with other factions' units for testing, but themed decks are encouraged
- David's Company units: Swordsmen, Spearmen, Slingers, Scouts, Shield Bearers
- Jonathan's Followers units: Loyal Guards, Elite Archers, Archers, Spearmen, Shield Bearers
- Achish's Host units: Giants, Swordsmen, Spearmen, Archers, Shield Bearers
- Lord of Ekron's Host units: Chariots, Slingers, Swordsmen, Spearmen, Shield Bearers
- Cross-faction play allowed for balance testing

---

## Card System

Each card has:
- **Initiative:** 1–10 (higher acts first within a phase)
- **Top ability:** Primary command
- **Bottom ability:** Secondary command (usually movement, positioning, or weaker action)

Resolution: Player picks 2 cards from hand, reveals both, resolves top of one + bottom of the other.

### Card Construction Formula

```
CARD POTENTIAL = (Action Potential × Command Multiplier) + Flexibility Modifiers + Unit Tier Modifier
```

| Action | Points |
|--------|--------|
| Move | 2 |
| Attack | 2 |
| Defend | 2 |
| +1 Move | +1 |
| +1 Attack | +1 |
| +1 Defense | +1 |
| Push 1 | +1 |
| Ignore Counterattack | +1 |
| Ignore Terrain | +1 |
| Special Effect | +1 to +3 |
| Sequence bonus (3+ actions) | +1 to +3 |

| Squads | Multiplier |
|--------|-----------|
| 1 | ×1.0 |
| 2 | ×1.75 |
| 3 | ×2.5 |
| 4 | ×3.0 |
| 5+ | ×3.5 |

| Restriction | Modifier |
|-------------|----------|
| Specific unit type | -1 |
| Adjacent only | -1 |
| Must stay in formation | -1 |

| Flexibility | Modifier |
|-------------|----------|
| Any friendly squad | +1 |
| Any unit type | +2 |
| Can split actions | +1 |

### Card Level Targets

| Level | Low | High |
|-------|-----|------|
| 1 | 3–5 | 8–10 |
| 2 | 4–6 | 9–11 |
| 3+ | +1 per level | |

### Formations

At least **two formations per unit type**. Formations represent specialized battlefield formations.

When played:
- Choose top OR bottom action
- Place on Command Board
- Limited activations
- When final activation spent, card is Lost

---

## Army Size & Deck Scaling

**Choose one army size for the match (all sides must use the same):**

| Army Size | Units per Side | Deck Size | Cards per Unit |
|---|---|---|---|
| **Small** | 6 (commander + 5) | 10 | ~1.7 |
| **Medium** | 8 (commander + 7) | 13 | ~1.6 |
| **Large** | 10 (commander + 9) | 16 | ~1.6 |

All sides must field the same army size. Suggested starting point: **Small (6 units, 10 cards)**.

---

## Deck Construction Rules

### Army Selection

**Requirements (per side):**
- Select exactly **1 commander**
- Select additional units to reach chosen army size
- Must have **at least 3 different unit types** among total units
- Units drawn only from commander's own faction pool

### Deck Building Flow

Build a deck of exactly **10 / 13 / 16 cards** depending on army size. All draws are random. Cards are not revealed during setup.

| Step | Draw | Count | Source |
|---|---|---|---|
| 2a | Unit cards | 1 per squad type | Random from each unit type's pool |
| 2b | Commander cards | 1 | Random from commander's 10-card pool |
| 2c | Fill to target | Remainder | Player selects 2 source pools; draw random from those pools |

**Example (Small/10 cards):** David brings Swordsman, Swordsman, Spearman, Slinger, Scout
- Step 2a: 1 random Swordsman card, 1 random Spearman card, 1 random Slinger card, 1 random Scout card = 4 cards
- Step 2b: 1 random David card = 1 card
- Step 2c: 5 more cards. Player chooses 2 pools (e.g., "David cards" + "Swordsman cards"). Draw 5 random cards from combined pool.

### Starting Hands
- Shuffle deck
- Deal **4 cards** to each player
- Remaining deck face-down

---

## Card Loss

- **Fatigue:** 1 random card from your hand → Lost pile each turn
- **Casualty:** When last unit of a type dies, remove 1 matching card from deck/hand/spent → Lost pile

---

## Unit Roster for Prototype

### David's Company (Purple Discs)

| Unit | Copies Available | Base Stats |
|---|---|---|
| David | 1 | Range 1 / Atk 2 / Def 1 / HP 2 / Move 2 |
| Swordsman | 4 | Range 1 / Atk 2 / Def 1 / HP 2 / Move 2 |
| Spearman | 4 | Range 2 / Atk 2 / Def 1 / HP 2 / Move 2 |
| Slinger | 3 | Range 3 / Atk 1 / Def 1 / HP 2 / Move 3 |
| Scout | 4 | Range 2 / Atk 1 / Def 1 / HP 1 / Move 3 |
| Shield Bearer | 4 | Range 1 / Atk 1 / Def 2 / HP 3 / Move 1 |

### Jonathan's Followers (Blue Discs)

| Unit | Copies Available | Base Stats |
|---|---|---|
| Jonathan | 1 | Range 1 / Atk 2 / Def 1 / HP 2 / Move 2 |
| Loyal Guard | 4 | Range 1 / Atk 2 / Def 1 / HP 2 / Move 2 |
| Elite Archer | 3 | Range 2 / Atk 2 / Def 1 / HP 2 / Move 2 |
| Archer | 4 | Range 2 / Atk 2 / Def 1 / HP 2 / Move 2 |
| Spearman | 4 | Range 2 / Atk 2 / Def 1 / HP 2 / Move 2 |
| Shield Bearer | 4 | Range 1 / Atk 1 / Def 2 / HP 3 / Move 1 |

### Philistines

#### Achish's Host (Lord of Gath) (Red Discs)

| Unit | Copies Available | Base Stats |
|---|---|---|
| Achish | 1 | Range 1 / Atk 2 / Def 1 / HP 2 / Move 2 |
| Giant | 2 | Range 1 / Atk 3 / Def 2 / HP 4 / Move 1 |
| Swordsman | 4 | Range 1 / Atk 2 / Def 1 / HP 2 / Move 2 |
| Spearman | 4 | Range 2 / Atk 2 / Def 1 / HP 2 / Move 2 |
| Archer | 4 | Range 2 / Atk 2 / Def 1 / HP 2 / Move 2 |
| Shield Bearer | 4 | Range 1 / Atk 1 / Def 2 / HP 3 / Move 1 |

#### Lord of Ekron's Host (Green Discs)

| Unit | Copies Available | Base Stats |
|---|---|---|
| Philistine Lord | 1 | Range 1 / Atk 2 / Def 1 / HP 2 / Move 2 |
| Chariot | 2 | Range 1 / Atk 2 / Def 1 / HP 2 / Move 3 |
| Slinger | 3 | Range 3 / Atk 1 / Def 1 / HP 2 / Move 3 |
| Swordsman | 4 | Range 1 / Atk 2 / Def 1 / HP 2 / Move 2 |
| Spearman | 4 | Range 2 / Atk 2 / Def 1 / HP 2 / Move 2 |
| Shield Bearer | 4 | Range 1 / Atk 1 / Def 2 / HP 3 / Move 1 |

---

## Drafted Cards

*Drafted with the balancing formula. Initiative 1–10, Top/Bottom format. Two formations per unit type when applicable.*

### David's Leadership (David)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 7 | 3 |
| **Effect** | Activate David: move up to 2, then attack. Adjacent allies gain +1 attack this turn. | Activate David: grant one friendly unit within 2 tiles an extra activation this turn. |

### Swordsmen Advance (Swordsman)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 6 | 2 |
| **Effect** | Activate up to 3 Swordsmen: each may move and attack. Gain +1 attack if adjacent to another Swordsman. | Move up to 2 Swordsmen up to 2 tiles each. |

### Swordsmen Formation (Swordsman)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 4 | 5 |
| **Effect** | Shield Wall: adjacent Swordsmen gain +1 defense until next player turn. (2 activations) | Phalanx: Swordsmen may attack without penalty when adjacent to friendly Spearmen. (1 activation) |

### Spear Wall (Spearman)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 5 | 3 |
| **Effect** | Activate up to 2 Spearmen: attack with +1 damage vs charging enemies. | Activate up to 2 Spearmen: move up to 2 tiles, gain brace (+1 defense vs melee until next turn). |

### Spearman Formation 1 (Spearman)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 4 | 5 |
| **Effect** | Lock Shields: adjacent Spearmen gain +2 defense until next player turn. (2 activations) | Thrust Line: Spearmen attack with reach without penalty against charging enemies. (1 activation) |

### Spearman Formation 2 (Spearman)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 3 | 6 |
| **Effect** | Screen: adjacent friendly Heavy Infantry gain -1 damage taken. (2 activations) | Spear Wall: Spearmen may make free attack when enemy enters melee range. (1 activation) |

### Circle and Strike (Slinger)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 8 | 4 |
| **Effect** | Activate up to 2 Slingers: each may move then attack. If moved ≥2 tiles, attack gains +1 damage. | Activate up to 2 Slingers: move up to 3 tiles each. |

### Stone Volley (Slinger)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 9 | 2 |
| **Effect** | Activate all Slingers: combine fire on one target. Each Slinger adds +1 damage. | Activate 1 Slinger: attack. If another Slinger is within 2 tiles, this attack gains +1 damage. |

### Archer Volley (Archer)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 6 | 3 |
| **Effect** | Activate up to 2 Archers: each attacks. Must target enemies within range. | Activate up to 2 Archers: move and gain Aim (+1 dmg on next shot if stationary). |

### Archer Formation (Archer)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 5 | 5 |
| **Effect** | Overwatch: Archers may make free attack when enemy moves into range. (1 activation) | Marksman: one Archer ignores 1 defense this turn. (2 activations) |

### Scout Recon (Scout)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 7 | 5 |
| **Effect** | Activate 1 Scout: move up to 4 tiles (ignores terrain), then make a free attack. | Activate 1 Scout: move up to 3 tiles. If ends adjacent to enemy, retreat 1 tile after interaction. |

### Scout Formation (Scout)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 6 | 4 |
| **Effect** | Ambush: Scouts start hidden. First attack gains +2 damage and enemy cannot counter. (1 activation) | Screen: Scouts block LoS for enemies within 1 tile. (2 activations) |

### Jonathan's Leadership (Jonathan)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 7 | 3 |
| **Effect** | Activate Jonathan: move and attack. All Loyal Guards within 2 tiles gain +1 defense this turn. | Activate Jonathan: grant one Elite Archer within 2 tiles the ability to attack twice this turn. |

### Guard Formation (Loyal Guard)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 5 | 4 |
| **Effect** | Shield Wall: Loyal Guards gain +2 defense until next player turn if adjacent to Jonathan. (2 activations) | Protect Commander: move Loyal Guard adjacent to friendly commander; commander gains -1 damage taken. (1 activation) |

### Jonathan's Mark (Elite Archer)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 8 | 3 |
| **Effect** | Target one enemy with an Elite Archer. This Archer gains +1 attack and ignores 1 defense. | Activate Elite Archer: move up to 2 tiles, then attack with +1 range this turn. |

### Perfect Shot (Elite Archer)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 9 | 2 |
| **Effect** | If Elite Archer has not moved this turn: attack with +2 range and +1 damage. | Activate Elite Archer: attack. If stationary, gain +1 damage. |

### March (Universal)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 1 | — |
| **Effect** | Activate up to 2 units of one type: each moves up to its full movement. | — |

### Engage (Universal)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 2 | — |
| **Effect** | Activate up to 2 units of one type: each attacks once. | — |

### Achish's Strength (Achish)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 7 | 3 |
| **Effect** | Activate Achish: move up to 2, then attack. All adjacent Philistines gain Shielded (first damage prevented this turn). | Place on Command Board. Adjacent Giants and Heavy Infantry gain +1 defense. (2 activations) |

### Lord's Command (Philistine Lord)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 6 | 4 |
| **Effect** | Activate Philistine Lord: move up to 2, then attack. Adjacent allies gain +1 attack this turn. | Grant one Champion or Heavy Infantry within 2 tiles an extra activation. |

### Philistine Spearmen
| | Top | Bottom |
|---|---|---|
| **Initiative** | 5 | 3 |
| **Effect** | Activate up to 2 Spearmen: each moves up to 2 tiles and attacks with +1 damage vs charging enemies. | Activate up to 2 Spearmen: each gains brace (+1 defense vs melee until next turn). |

### Spearmen Formation 1 (Spearman)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 4 | 5 |
| **Effect** | Lock Shields: adjacent Spearmen gain +2 defense until next player turn. (2 activations) | Thrust Line: Spearmen attack with reach without penalty against charging enemies. (1 activation) |

### Spearmen Formation 2 (Spearman)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 3 | 6 |
| **Effect** | Screen: adjacent friendly Heavy Infantry gain -1 damage taken. (2 activations) | Spear Wall: Spearmen may make free attack when enemy enters melee range. (1 activation) |

### Heavy Infantry Command (Heavy Infantry)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 4 | 2 |
| **Effect** | Activate up to 2 Heavy Infantry: each moves 1 tile and attacks with +1 damage. | Activate up to 2 Heavy Infantry: each gains +2 defense until next player turn. |

### Heavy Infantry Formation 1 (Heavy Infantry)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 3 | 5 |
| **Effect** | Shield Wall: Heavy Infantry gain +1 defense and cannot be pushed if adjacent to another Heavy Infantry. (2 activations) | Battering Ram: Heavy Infantry may push target 1 tile after attack. (1 activation) |

### Heavy Infantry Formation 2 (Heavy Infantry)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 2 | 4 |
| **Effect** | Slow Advance: Heavy Infantry gain +1 move this turn but lose -1 defense. (2 activations) | Iron Wall: adjacent friendly Spearmen gain -1 damage taken. (1 activation) |

### Ekron Archer Command (Archer)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 6 | 3 |
| **Effect** | Activate up to 2 Ekron Archers: each attacks. Enemies hit lose 1 movement next turn. | Activate up to 2 Ekron Archers: move 1 tile each and gain +1 range this turn. |

### Ekron Archer Formation 1 (Archer)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 5 | 4 |
| **Effect** | Opening Volley: Ekron Archers attack before all movement this turn. (1 activation) | Covering Fire: after an ally moves, one Ekron Archer may make a free attack. (2 activations) |

### Ekron Archer Formation 2 (Archer)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 3 | 6 |
| **Effect** | Coordinated Volley: multiple Ekron Archers targeting same tile gain +1 damage each. (2 activations) | Break Formation: enemies hit by Ekron Archers cannot move next turn. (1 activation) |

### Champion's Duel (Champion)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 8 | 2 |
| **Effect** | Activate Champion: target enemy commander or Hero. This attack ignores 2 defense. | Activate Champion: move up to 2 tiles. Gain +1 attack and +1 defense until end of turn. |

### Champion's Formation 1 (Champion)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 7 | 3 |
| **Effect** | Champion's Challenge: target enemy commander must attack Champion this turn if able. (1 activation) | Champion gains +2 defense when adjacent to friendly commander. (2 activations) |

### Champion's Formation 2 (Champion)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 6 | 4 |
| **Effect** | If Champion has not attacked this turn: gain +2 damage on next attack. (1 activation) | Champion may push target 1 tile after attack. (2 activations) |

### Chariot Charge (Chariot)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 9 | 4 |
| **Effect** | Activate Chariot: move up to 3 tiles (must move ≥2), then attack with +1 damage. Push target 1 tile. | Activate Chariot: move up to 3 tiles through friendly units without obstruction. |

### Chariot Formation 1 (Chariot)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 8 | 5 |
| **Effect** | Breakthrough: Chariot attacks and pushes target 2 tiles instead of 1. (1 activation) | Chariot ignores rough terrain penalties this turn. (2 activations) |

### Chariot Formation 2 (Chariot)
| | Top | Bottom |
|---|---|---|
| **Initiative** | 7 | 3 |
| **Effect** | Hit and Run: Chariot may move after attacking (up to 1 tile). (2 activations) | Chariot gains +1 defense for each tile moved this activation. (1 activation) |

---

## Balance Targets

- **Deck size:** 20 cards per side
- **Hand size:** 4 cards
- **Cards per turn:** 2 selected, top of one + bottom of the other
- **Fatigue:** 1 lost card per player per turn
- **Expected turn count:** 8–12 turns = 15–20 minutes

---

## Art Requirements Summary

### Unit Discs (2" diameter, colored border by commander)

| Disc | Border Color |
|---|---|
| David | Teal |
| Jonathan | Gold |
| Achish | Red |
| Philistine Lord | Red |
| Swordsman | Varies by faction |
| Spearman | Varies by faction |
| Slinger | Teal (David only) |
| Archer | Varies by faction |
| Elite Archer | Gold (Jonathan only) |
| Scout | Varies by faction |
| Loyal Guard | Gold (Jonathan only) |
| Heavy Infantry | Red (Philistine only) |
| Champion | Red (Philistine only) |
| Chariot | Red (Philistine only) |

### Command Cards (2.5" × 3.5")

| Category | Count | Notes |
|---|---|---|
| Commander cards (David) | 10 | Unique designs |
| Commander cards (Jonathan) | 10 | Unique designs |
| Commander cards (Achish) | 10 | Unique designs |
| Commander cards (Philistine Lord) | 10 | Unique designs |
| Unit-type cards (each type) | 5 | 1 double-formation card per type |
| Card back | 1 | Shared design |

**Total card fronts needed:** 40 commander cards + 50 unit-type cards = 90 unique designs

### Physical Components

- 8×8 hex grid board
- Unit discs with colored borders
- Command cards
- Activation tokens
- Commander aura markers
- Lost Pile markers
- Setup/reference sheets

---

## Open Design Questions

1. **Faction restrictions:** Should commanders be limited to their own faction's units, or can David recruit Philistine Spearmen for testing?
2. **Deck size scaling:** Should deck size scale with army size, or stay fixed at 20?
3. **Commander card count:** 2 random commander cards per commander is the current proposal. Is this enough?
4. **Unit-type card draw:** 1 card per unit type (not per copy) is proposed. Does this create enough variety?

---

## Key Decisions

- **Flexible play modes:** Co-op, 1v1, and 2v2 all use the same core ruleset
- **Army size:** Exactly 6 units per side (including commander)
- **Unit type diversity:** At least 3 different unit types per side
- **Deck size:** Fixed at 20 cards per side
- **Deck construction:** Random draws + limited player choice
- **Unit discs:** 2" circles with colored borders by commander/faction
- **Command cards:** 5 per unit type, 10+ per commander

---

## Relevant Files

- `GDD.md` — core rules, unit stats, card system, turn structure
- `POST_MVP_GDD.md` — Philistine faction, Jonathan commander ability, co-op notes
- `ROADMAP.md` — Sprint 3–7 tasks
- `COMMAND_CARD_DESIGN.md` — card balancing formula and design grid
- `command_cards/factions/DAVIDS_COMPANY.md` — deck construction
- `command_cards/factions/JONATHANS_FOLLOWERS.md` — ally rules
- `command_cards/factions/PHILISTINES.md` — faction rules
- `command_cards/unit_types/DAVIDS_COMPANY/david/DAVID.md` — David's card definitions
- `command_cards/unit_types/JONATHANS_FOLLOWERS/elite_archer/ELITE_ARCHER.md` — Jonathan archer cards
- `command_cards/unit_types/PHILISTINES/achish/ACHISH.md` — Achish card definitions
- `command_cards/formations/PHILISTINES.md` — Philistine formations
- `RULEBOOK.md` — printable rulebook

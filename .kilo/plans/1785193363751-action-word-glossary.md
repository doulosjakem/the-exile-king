# Action Word Glossary & Mechanics — The Exile King

## Agreed Decisions
- Replace "Activate [unit]" with **Command [unit]** in all card text
- Keep **Attack** as the combat verb
- Replace "+1 Defense" buffs with rare **Shield tokens**
- Shield tokens last until **start of unit's next turn** (not until damaged)
- No Penalty mechanic
- Three card subtypes: **Regular**, **Persistent**, **Formation**
- Ranged attacks fire over allies/enemies
- Forest LOS: count unavoidable Forest crossings (excluding attacker's tile); each = -1 Range
- **Hand size:** 4 max, no overdrawing
- **Draw rate:** Draw up to 2 cards at the start of each turn (if you can)
- **Card recovery:** Two actions exist — **Camp** (spend your whole turn; heal 1 HP to all units; choose 1 Spent card to Lose; rest return to Command Deck; refill hand to 4) and **Brainstorm** (do not spend your turn; no healing; 1 random Spent card is Lost; rest return to Command Deck; refill hand to 4)
- **Commander auras:** Removed entirely
- **Card counts:** Each unit type has exactly **5 cards** in its pool (1 Formation card + 4 Regular/Persistent). Each commander has exactly **10 cards** in its pool.
- **Fatigue:** Removed entirely. No random card loss each turn.
- **Spent recovery timing:** Spent cards return to the Command Deck **only** via Camp or Brainstorm. No passive end-of-round recovery.
- **Formation timing:** Formation abilities can trigger on **other players' turns**, subject to their own trigger conditions. Only **one active Formation** at a time.

---

## Core Actions (card text + rules)

| Term | Definition | Usage |
|---|---|---|
| **Command** | Select X units and perform an action with them. | Card text, rules |
| **Move** | Change unit position by X tiles. | Card text, rules |
| **Attack** | Make a combat roll against an adjacent or in-range target. | Card text, rules, stat blocks |
| **Heal / Mend** | Restore HP to a unit. | Card text |

---

## Combat Stats

| Term | Definition | Usage |
|---|---|---|
| **Range** | How far a unit can Attack. 1 = melee, 2+ = ranged. | Stat block, card text |
| **Attack** | Base damage stat (1-3). | Stat block |
| **Health** | Damage a unit can take before elimination. | Stat block |
| **Move** | tiles per Move action. | Stat block |

**Removed stat:** **Defense** — replaced by Shield tokens for heavy units. Most units have no Defense stat.

---

## Shield Token Mechanic

| Term | Definition | Usage |
|---|---|---|
| **Shield** | Temporary token that absorbs 1 damage per token. Tokens are placed during the Command phase and removed at the start of the unit's next turn. | Card text, rules |
| **Shielded** | State description: "this unit has Shield tokens." | Card text |

**Persistence rule:** Shield tokens persist until the **start of the unit's next turn**, not until damage is taken. This means:
- A Shield Bearer gains 2 Shield tokens on your turn
- Enemy attacks next turn; tokens absorb damage
- At the start of your next turn, tokens are removed regardless of whether damage was taken

**Who gets Shield:** Rare. Only Shield Bearer, Royal Guard, and Veteran units have cards that generate Shield tokens. Most other units use avoidance (Screen, Cover, Ambush, Overwatch) for defense.

---

## Position / Movement Verbs

| Term | Definition | Usage |
|---|---|---|
| **Advance** | Move toward enemy, optionally with Attack. | Card text |
| **Retreat** / **Fall Back** | Move away from enemy, optionally with defensive bonus. | Card text |
| **Push** | Force enemy to move X tiles away from you. | Card text |
| **Rush** | Move quickly (3+ tiles), optionally with restrictions. | Card text |

---

## Defensive States (no Penalty mechanic)

| Term | Definition | Usage |
|---|---|---|
| **Cover** | Unit takes reduced damage from ranged attacks. **RARE.** | Card text |
| **Screen** | Unit blocks enemy Line-of-Sight for units behind it. | Card text |
| **Ambush** | Unit is hidden; first Attack gains bonus and enemy cannot counter. | Card text |
| **Overwatch** | Stationary unit may make a free Attack when an enemy moves into its Range. | Card text |

**Removed:** "Screen" as "+1 damage taken for adjacent" — this was vague and overlapping with Cover. Screen now means **Line-of-Sight blocking only**.

---

## Commander / Meta Verbs

| Term | Definition | Usage |
|---|---|---|
| **Rally** | Grant a unit an extra Command this turn. | Card text |
| **Shield** (verb) | Unit takes damage intended for another unit. Differs from Shield tokens. | Card text |
| **Command** (verb, meta) | Force an adjacent/allied unit to perform an action immediately. | Card text |
| **Decree** / **Boost** | Grant a passive bonus to a unit or group for a duration. | Card text |

---

## Formation Cards (the command deck)

All cards in your deck are **Command Cards**. Each unit type gets exactly **1 Formation card** (with Top and Bottom actions). When played, it either resolves immediately (Regular / Persistent) or moves to your **Formation** zone for ongoing effects (Formation type).

- "Shepherd's Advance", "Spear Wall", "Covenant Shield" — these are **Formation Cards** in your deck
- They are not a separate manual - they are the playable cards themselves

### Regular (in-card effect)
- Resolve immediately when played
- Card goes to **Spent** pile

### Persistent (in-card effect, lingering)
- Resolve immediately when played
- Bonus/effect continues until **end of round**
- All Persistent cards are moved to their discard piles at the end of the round
- Card goes to **Spent** pile

### Formation (active zone card)
- When played, card moves to the **Formation** zone on your player mat
- **Only 1 Formation card may be active at a time.** Playing a new Formation displaces/replaces the previous one.
- Has **n Activations** tracked on the card itself
- Provides a **passive rule** or **triggered reaction** while active
- Abilities may trigger on **your turn** or on **other players' turns**, depending on their trigger conditions
- Each time the ability applies/triggers, spend 1 Activation
- When all Activations are spent, the card is immediately **Lost**
- Persists across multiple turns

**Example:** "Shield Wall — While this Formation is active, all adjacent friendly Spearmen gain +1 Shield. (3 activations)"

---

## Deck Recovery: Camp vs Brainstorm

When you need to recover Spent cards (or when the game state requires it), you choose one:

### Camp
- Takes your **whole turn**
- Heal **1 HP to all units**
- Choose **1 Spent card** to **Lose**
- All other Spent cards return to your Command Deck
- Refill your hand to **4**

### Brainstorm
- Does **not** take your turn
- No healing
- **1 random Spent card** is **Lost**
- All other Spent cards return to your Command Deck
- Refill your hand to **4**

---

## Turn Structure (draft)

1. **Start of turn:** Draw up to 2 cards. Hand size cannot exceed 4.
2. **Play phase:** Play 1 Regular, Persistent, or Formation card from your Hand.
3. **Command phase:** Resolve the card's effect.
4. **End of turn:** If you played a Persistent card, its effect continues until end of round.

**Note:** Camp and Brainstorm are recovery actions that replace your normal play phase (Camp) or happen as a special action (Brainstorm).

---

## Deck Zones (player mat)

| Zone | Definition | Behavior |
|---|---|---|
| **Command Deck** | Face-down draw pile. | Draw up to 2 at start of turn. |
| **Hand** | Cards you can play this turn. | Max 4. Draw up to 2 at start of turn. |
| **Spent** | Cards played this turn (Regular/Persistent). | Recovered via Camp or Brainstorm. |
| **Lost** | Cards removed from play permanently. | Return only via special recovery abilities or between battles. |
| **Formation** | Active Formation-type cards placed here. | Persistent until Lost. Track activations on card. |

**Note:** Regular and Persistent cards never enter the Formation zone — they resolve and go straight to Spent. Only Formation-type cards (with activations and ongoing effects) go to the Formation zone.

---

## Term Retirement List

These terms are **removed** from all card text and rules:

| Retired Term | Replacement | Reason |
|---|---|---|
| Activate (imperative) | Command | Overloaded with game-state "activation" |
| Defense (stat/buff) | Shield (token) | Undefined mechanic; replaced with explicit tokens |
| Toughness | Shield | User preference; "Shield" is more intuitive |
| Penalty | (no replacement) | User rejected; use positional/state restrictions instead |
| Lock Shields | Brace / Shield Wall | Anachronistic; user already approved rename |
| Phalanx | Formation / Shield Line | Anachronistic; user already approved rename |
| Iron Wall (Israelite) | King's Wall / Royal Shield | Anachronistic; user already approved rename |
| Commander aura | (none) | Removed entirely |

---

## Terrain & Line-of-Sight (LOS)

### Agreed Principles
- **Ranged attacks can fire over allies and enemies** — units do not block LOS for ranged targeting
- **Terrain can block LOS and/or movement completely** (walls, cliffs)
- **Some terrain costs double movement** (difficult ground)
- **Forests limit LOS** — range reduction rule below

### Terrain Types (draft)

| Terrain | Move Cost | Blocks LOS? | Effect |
|---|---|---|---|
| **Open** | 1 | No | Default |
| **Difficult** | 2 | No | Rough ground, rocky slopes |
| **Forest** | 2 | See LOS rule below | Limits LOS; see exact rule |
| **Impassable** | ∞ | Yes | Cliffs, walls, water |
| **Road** | 1 | No | No effect |

### LOS Rules
- **Melee:** Adjacent only (Range 1). No LOS check needed.
- **Ranged:** Must have LOS to target. LOS is blocked by Impassable terrain and terrain edges.
- **Units do NOT block LOS** for ranged attacks (per user preference).
- **Forest LOS reduction:** When drawing LOS from attacker to target:
  - Count every **Forest** tile the line passes through, **excluding the attacker's own tile**
  - Each Forest tile crossed reduces effective Range by 1
  - If the LOS line can pass through **either** Forest or non-Forest tiles (hex-edge ambiguity), choose the non-Forest path — no penalty
  - This means firing **out of** a forest is unrestricted, but firing **into** a forest is penalized

**Example:** Archer in open terrain fires at target 3 tiles away, with 1 forest tile between them. Effective Range = 3 - 1 = 2. If the target was at Range 2, the shot is fine. If at Range 3, it cannot reach.

**Edge case:** Attacker on forest edge, target 2 tiles away through alternating forest/open hexes. If any alternative path exists through non-forest tiles, use it. Only unavoidable forest crossings count.

---

## Card Pool Targets

| Scope | Target | Current Approx | Gap |
|---|---|---|---|
| Unit types | 5 cards each | 1–3 cards each | ~2–4 new cards per unit type |
| Commanders | 10 cards each | 1–2 cards each | ~8–9 new cards per commander |

**Current catalogue:** `COMMAND_CARD_AUDIT.md` contains the existing card text extracted from `command_cards/unit_types/**/*.md` and `command_cards/factions/*.md`. Full card catalog exists but needs reconciliation between faction files and unit type files.

---

## Resolved Design Decisions

All major design decisions are resolved:

| # | Decision | Resolution |
|---|---|---|
| 1 | Shield timing | Until start of unit's next turn |
| 2 | Card recovery | Camp (full turn, heal 1 all, choose 1 Spent to Lose, refill to 4) vs Brainstorm (no turn, no heal, 1 random Spent Lost, refill to 4) |
| 3 | Hand size / draw | 4 max, draw up to 2 at start of turn |
| 4 | Commander auras | Removed entirely |
| 5 | Card subtypes | Regular, Persistent, Formation; 1 Formation card per unit type with Top + Bottom |
| 6 | Fatigue | Removed entirely |
| 7 | Spent recovery | Only via Camp/Brainstorm. No passive end-of-round recovery. |
| 8 | Formation timing | Abilities can trigger on other players' turns. Only 1 Formation active at a time. |
| 9 | Brainstorm timing | Always available at any time as a free action |
| 10 | Brainstorm hand refill | Yes, refill to 4 |
| 11 | LOS / ranged | Ranged attacks fire over allies/enemies. Forests cost extra range per unavoidable crossing. |

---

## Migration Scope

To fully implement this glossary, the following files need updates:

1. `command_cards/unit_types/**/*.md` — retire "Activate", "Defense"; add new cards to reach 5 per unit type
2. `command_cards/factions/*.md` — faction summaries, deck rules, new card pools
3. `command_cards/formations/*.md` — merge into unit type files or retire
4. `GDD.md` — stat blocks, remove commander auras, add Camp/Brainstorm/hand rules
5. `POST_MVP_GDD.md` — references to retired terms
6. `PROMPTS.md` — art prompts referencing retired terms
7. `RULEBOOK.md` — core rules text
8. `review_art_ollama.py` / `generation_*.json` — prompt keys if any reference retired terms

Estimated new cards needed: **~50+** new card entries to reach 5 per unit type and 10 per commander.
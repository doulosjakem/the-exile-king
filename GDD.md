# THE EXILE KING
## Master Game Design Document (GDD)
### Draft v0.7

---

# PURPOSE

This document is the current source of truth for The Exile King.

It contains:

- Current design decisions
- Guiding principles
- Mechanics
- Remaining design questions
- Prototype roadmap

Items in the **Open Questions** section are intentionally unresolved and should not be considered finalized.

---

# VISION

The Exile King is a tactical skirmish game inspired by the life of David during his exile.

Players command small companies rather than individual heroes.

The game emphasizes:

- Leadership
- Tactical positioning
- Difficult command decisions
- Battlefield endurance
- Efficient use of limited command bandwidth

The experience should feel somewhere between:

- Gloomhaven
- Root
- Historical skirmish games

while remaining mechanically distinct.

---

# DESIGN PILLARS

## Command over Heroics

Victory comes through leadership.

Not superheroes.

---

## Positioning over Arithmetic

Board position creates advantage.

Avoid stacking modifiers.

---

## Tactical Decisions

Hard choices.

Simple calculations.

---

## Elegance

Every rule should justify its existence.

Reduce bookkeeping whenever possible.

---

## Theme First

Mechanics reinforce the biblical narrative.

Faith is never represented as a numerical resource.

---

# CORE DESIGN PHILOSOPHY

Units provide capability.

Orders provide intent.

Commanders provide coordination.

The game's true resource is **command bandwidth**.

The player is constantly deciding:

"What deserves my commander's attention?"

---

# UNIT STRUCTURE

Units contain only inherent characteristics.

## Core Stats

Health

Movement

Attack

Counterattack

Attack Type

- Melee
- Ranged

Range (if ranged)

Keywords

---

## Intentionally Omitted

No Defense stat.

No Initiative stat.

Very few inherent special abilities.

Most interesting behavior comes from Orders.

---

# ORDERS

Orders represent commands issued by a commander.

They determine:

- Which units activate.
- What actions those units perform.
- Temporary tactical advantages.
- Persistent battlefield plans.

Units define what they CAN do.

Orders define what they DO.

---

# ORDERS DECK

Each company contributes Orders.

Example:

David

2 Orders

Spearmen ×3

3 Orders

Scout

1 Order

Archer

1 Order

Total:

7-card Orders Deck

The deck represents command capability—not stamina.

---

# HAND

Orders in Hand

Players normally:

Draw 2 Orders during Preparation.

Maximum hand size:

4 Orders.

---

# ISSUED ORDERS

Played Orders move here.

Recovered by:

- Brainstorm
- Regroup

---

# LOST ORDERS

Orders permanently removed.

Represent:

- Fallen soldiers
- Lost command opportunities
- Long-term exhaustion
- Campaign consequences

Persistent Orders also move directly here after completion.

---

# ROUND STRUCTURE

## 1. Preparation

Draw 2 Orders.

Choose:

- Initiative Order
- Support Order

---

## 2. Initiative

Reveal Initiative Orders.

Resolve from lowest initiative to highest.

---

## 3. Action Phase

Resolve:

Top of one Order.

Bottom of the other.

Orders determine:

- Activated units
- Sequence of actions
- Modifiers

---

## 4. End Phase

Resolve:

Persistent Orders.

Scenario effects.

Victory conditions.

Begin next Round.

---

# BRAINSTORM

Emergency battlefield adaptation.

Lose:

1 random Order.

Recover:

All Issued Orders.

Shuffle.

Continue normally.

---

# REGROUP

Deliberate recovery.

Skip your activation.

Recover:

All Issued Orders.

Lose:

1 chosen Order.

Heal your company.

(Current healing amount TBD.)

---

# COMBAT PHILOSOPHY

Combat comes from only three sources:

1. Unit Stats

2. Orders

3. Shared Attack Modifier Deck

Nearly every tactical decision should arise from:

- Positioning
- Timing
- Orders
- Persistent Orders
- Unit synergy

Not arithmetic.

---

# COMBAT (CURRENT DIRECTION)

General sequence:

1. Resolve Order.
2. Activate units.
3. Move / Attack according to the Order.
4. Apply Order bonuses.
5. Draw Attack Modifier.
6. Deal damage.
7. Resolve retaliation.
8. Resolve Persistent effects.

Exact timing remains under development.

---

# RETALIATION

Units normally retaliate during melee attacks.

Counterattack determines retaliation strength.

Some units may have:

Counterattack = 0

Orders may grant additional reaction attacks.

Examples:

- Spear Wall
- Covering Fire
- Ambush
- Shield Wall

These reactions are separate from normal retaliation.

---

# PERSISTENT ORDERS

Persistent Orders represent ongoing battlefield commands.

Examples:

- Spear Wall
- Covering Fire
- Hold the Line
- Shield Wall

Persistent Orders:

Require an activation.

Remain active.

Track a limited number of triggers.

Immediately become Lost after completion.

Persistent Orders intentionally trade long-term endurance for battlefield control.

---

# COMMAND SCALE

Players command companies.

Not individual warriors.

Typical Order:

Activate:

1 unit.

Sometimes:

Up to 2 units.

Rarely:

Entire formations with weaker effects.

General principle:

The broader the Order,

the weaker or less precise it becomes.

---

# ARMY COMPOSITION

Players are encouraged to build cohesive companies.

Example:

4 Spearmen

2 Slingers

rather than

1 Spearman

1 Archer

1 Scout

1 Swordsman

Mixed companies gain versatility.

Focused companies gain command efficiency.

This is an intentional strategic tradeoff.

---

# TERRAIN

Terrain primarily influences:

Movement

Visibility

Positioning

Space control

Avoid combat math whenever possible.

---

# ATTACK MODIFIER DECK

One shared deck.

Used by every player.

Represents:

Battlefield uncertainty.

Momentum.

Human error.

Providence.

Current direction:

Mostly:

0

+1 Attack

-1 Attack

+1 Counterattack

-1 Counterattack

Rare:

Miss

Counterattack fails

±2

Randomness should support tactics—not replace them.

---

# CAMPAIGN

Regular followers:

May permanently die.

Replacement followers recruited using Influence.

Named heroes:

Become Wounded instead of dying.

Unavailable until recovered.

David's death:

Lose the scenario.

Retry.

---

# INITIAL FACTIONS

David

Saul

Philistines

Amalekites

---

# VERTICAL SLICE

Target:

4 factions.

6–8 unit types.

20–30 Orders.

1 map.

3 scenarios.

Goal:

Determine whether commanding companies is genuinely fun.

---

# OPEN DESIGN QUESTIONS

## 1. Combat Resolution ⭐⭐⭐⭐⭐

Finalize:

- Exact damage formula.
- Counterattack timing.
- Ranged retaliation.
- Death timing.
- Multiple attackers.
- Order of operations.

---

## 2. Order Card Design ⭐⭐⭐⭐⭐

Design the standard Order template.

Need to determine:

- Typical Move values.
- Typical Attack values.
- Combined Move + Attack frequency.
- Persistent Order frequency.
- Commander Orders vs Unit Orders.
- Shared Orders.
- Typical activation counts.

---

## 3. Movement ⭐⭐⭐⭐☆

Need to finalize:

Can Orders allow:

- Move
- Attack
- Move → Attack
- Attack → Move
- Move → Attack → Move

Current leaning:

The Order defines the sequence.

---

## 4. Attack Modifier Deck ⭐⭐⭐⭐☆

Finalize:

Deck size.

Distribution.

Reshuffle timing.

Rare effects.

---

## 5. Keywords ⭐⭐⭐☆

Finalize reusable keyword system.

Examples:

Reach

Scout

Shield

Heavy

Volley

Mounted

---

## 6. Unit Costs ⭐⭐⭐☆

Develop point values.

Primarily solved through playtesting.

---

## 7. Orders Deck Construction ⭐⭐⭐☆

Determine:

Starting deck size.

Commander Order count.

Unit Order count.

Shared Order count.

---

## 8. Enemy AI ⭐⭐⭐☆

Need:

Solo system.

Co-op automation.

Faction personalities.

Behavior priorities.

---

## 9. Scenario Design ⭐⭐⭐☆

Objectives.

Replayability.

Scaling.

Randomization.

---

## 10. Campaign Progression ⭐⭐⭐☆

Finalize:

Influence.

Recruitment.

Unlock cadence.

Progression systems.

---

# PROTOTYPE ROADMAP

Prototype 0.1

□ Core combat

□ Basic movement

□ David

□ Saul

□ Spearmen

□ Swordsmen

□ Slingers

□ Archers

□ ~20 Orders

□ Shared Attack Modifier Deck

□ Printable cards

---

Prototype 0.2

□ Four factions

□ AI

□ Scenario objectives

□ Campaign skeleton

---

Prototype 0.3

Blind playtesting.

Balance.

Rulebook.

---

# PLAYTESTING PLAN

Stage 1

Designer solo testing.

Question:

"Does it function?"

---

Stage 2

Trusted friends.

Question:

"Is it fun?"

---

Stage 3

Experienced strategy gamers.

Question:

"Can they break it?"

---

Stage 4

Casual gamers.

Question:

"Can they learn it?"

---

Stage 5

Local game stores.

Board game clubs.

Question:

"Would people play this again?"

---

# AI'S ROLE

AI should help with:

- Probability analysis
- Unit costing
- Balance suggestions
- Edge-case discovery
- Simulated game states
- Rule consistency

Humans determine:

- Fun
- Clarity
- Excitement
- Emotional pacing
- Replayability

---

# NORTH STAR

Whenever adding a rule, ask:

"Does this improve the experience of commanding a company?"

If not,

it probably doesn't belong.

---

# Suggested Repository Structure (Future)

Once the GDD grows beyond ~20 pages, split it into focused documents:

docs/
├── 01 Vision.md
├── 02 Design Pillars.md
├── 03 Core Rules.md
├── 04 Combat.md
├── 05 Units.md
├── 06 Orders.md
├── 07 Campaign.md
├── 08 AI.md
├── 09 Scenarios.md
├── 10 Playtesting.md
├── Open Questions.md
└── Changelog.md

Keep this master GDD until the prototype is stable. Then, move each section into its own file and let your coding/design agent treat each Markdown file as a single source of truth for that subsystem. That makes it easier for the agent to modify Combat without accidentally changing Campaign, for example, and makes Git history much cleaner.

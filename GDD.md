# The Exile King
## Game Design Document (GDD)
### Draft v0.6

---

# Vision

The Exile King is a tactical skirmish game inspired by the life of David during his exile.

Players command small companies through carefully chosen Orders rather than overwhelming force.

The focus is on:

- Leadership
- Positioning
- Tactical timing
- Battlefield endurance
- Command bandwidth

The game should feel somewhere between Gloomhaven, Root, and a historical skirmish game while maintaining its own identity.

---

# Design Pillars

## Command Over Heroics

Players command companies, not superheroes.

Leadership wins battles.

---

## Positioning Over Arithmetic

Terrain and formations create tactical decisions.

Avoid stacking numerical modifiers.

---

## Tactical Difficulty

Interesting decisions.

Simple math.

---

## Elegance

Every rule should reduce bookkeeping whenever possible.

Prefer:

- Board state
- Player decisions
- Keywords

over exception rules.

---

## Theme First

Mechanics should reinforce Scripture and the historical setting.

Faith is never treated as a quantifiable resource.

---

# Core Philosophy

Units provide capability.

Orders provide intent.

Commanders provide coordination.

Victory comes from using limited command bandwidth wisely.

---

# Unit Structure

Every unit contains only its inherent capability.

## Stats

Health

Movement

Attack

Counterattack

Attack Type
(Melee / Ranged)

Range
(if ranged)

Keywords

No Defense stat.

No inherent initiative.

Very few inherent special abilities.

Most tactical behavior comes from Orders.

---

# Orders

Orders represent commands issued by the commander.

Players build an Orders Deck.

Orders come from:

- Commander
- Unit types
- Shared tactical Orders

---

# Orders Deck

The Orders Deck represents command capability.

Example:

David

2 Orders

Spearmen ×3

3 Orders

Archer ×1

1 Order

Scout ×1

1 Order

---

# Orders in Hand

Players normally:

Draw 2 Orders each Round.

Maximum hand size:

4 Orders.

---

# Issued Orders

After use:

Orders move here.

Recovered by:

- Brainstorm
- Regroup

---

# Lost Orders

Lost permanently.

Represent:

- Fallen units
- Lost command capability
- Campaign consequences

---

# Round Structure

## 1. Preparation

Draw 2 Orders.

Choose:

- Initiative Order
- Support Order

---

## 2. Initiative

Reveal Initiative.

Resolve:

Lowest to highest.

---

## 3. Action

Resolve:

Top of one Order

Bottom of the other.

Orders determine:

- Which units activate.
- What actions they perform.

---

## 4. End Phase

Resolve:

- Persistent Orders
- Scenario effects
- Victory

Repeat.

---

# Brainstorm

Emergency recovery.

Lose:

1 random Order.

Recover:

All Issued Orders.

Shuffle.

Continue.

---

# Regroup

Deliberate recovery.

Skip activation.

Recover:

All Issued Orders.

Lose:

1 chosen Order.

Heal.

(Current healing amount TBD.)

---

# Combat Philosophy

Combat comes from three things:

1. Unit stats.
2. Orders.
3. Attack Modifier Deck.

Most tactical depth comes from:

- Positioning.
- Timing.
- Formation.
- Persistent Orders.

Not arithmetic.

---

# Combat Sequence (Draft)

1. Resolve Order.
2. Activate unit(s).
3. Move / Attack according to Order.
4. Apply Order bonuses.
5. Draw Attack Modifier.
6. Deal damage.
7. Resolve retaliation.
8. Resolve Persistent effects.

Exact timing remains under development.

---

# Attack Modifier Deck

One shared deck.

Represents:

- Battlefield chaos.
- Fortune.
- Momentum.
- Human error.

Likely contents:

Many:

0

Some:

+1 Attack

-1 Attack

+1 Counterattack

-1 Counterattack

Rare:

Miss

Counterattack fails

±2

Keep randomness meaningful but not dominant.

---

# Retaliation

Units normally retaliate when attacked in melee.

Counterattack determines retaliation strength.

Orders may grant additional reactions beyond normal retaliation.

Examples:

- Spear Wall
- Covering Fire
- Ambush
- Shield Wall

---

# Persistent Orders

Persistent Orders represent standing battlefield commands.

Examples:

Spear Wall

Covering Fire

Shield Wall

Hold the Line

Characteristics:

Require an activation.

Remain active.

Limited trigger count.

Immediately become Lost after completion.

Persistent Orders trade endurance for battlefield control.

---

# Command Scale

Players command companies.

Not every individual action.

Typical Order:

Activate:

1 unit.

Occasionally:

Up to 2.

Rarely:

Entire formations with weaker effects.

General principle:

The broader an Order,

the weaker or less precise it becomes.

---

# Army Composition

Mixed companies provide flexibility.

Focused companies provide command efficiency.

Example:

4 Spearmen

2 Slingers

is easier to command than

1 Spearman

1 Archer

1 Scout

1 Swordsman

This is an intentional strategic tradeoff.

---

# Terrain

Terrain primarily affects:

- Movement
- Position
- Visibility
- Space control

Avoid combat math.

---

# Campaign

Regular units:

May die permanently.

Replacement followers recruited using Influence.

Named characters:

Become Wounded instead of dying.

David's death:

Scenario loss.

Retry scenario.

---

# Initial Factions

David

Saul

Philistines

Amalekites

---

# Vertical Slice Goal

Playable prototype:

4 factions.

6–8 unit types.

20–30 Orders.

1 map.

3 scenarios.

Enough to determine whether commanding companies is fun.

---

# Ultimate Design Goal

The player's greatest resource is not damage.

It is not health.

It is command.

Every interesting decision should ask:

"What is worthy of my commander's attention?"

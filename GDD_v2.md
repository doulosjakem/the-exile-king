# Player Command Board

Each player has a Command Board.

The Command Board centralizes nearly all bookkeeping, allowing the battlefield to remain clean and readable.

The board has two primary responsibilities:

## 1. Orders

The board manages the player's Orders.

Areas include:

- Orders Deck
- Orders in Hand
- Issued Orders
- Lost Orders

The board should make the state of a player's command resources immediately obvious.

---

## 2. Company Roster

The board also tracks every squad under the player's command.

Each squad occupies its own slot.

Each slot contains:

- Squad Card
- Health Tracker
- Current Squad Level
- Squad Keywords
- Base Statistics

The battlefield does not need to display this information.

---

# Squad Cards

Each squad is represented by a Squad Card inserted into the Command Board.

The Squad Card defines:

- Health
- Movement
- Attack
- Counterattack
- Range
- Keywords

The battlefield standee only identifies the squad's location.

---

# Squad Progression

Campaign progression upgrades existing squads.

Rather than replacing components, Squad Cards support multiple progression levels.

Current direction:

Each Squad Card contains multiple versions of the same squad.

Example:

Spearmen

Level I

↓

Level II

↓

Level III

↓

Level IV

The active version is selected during campaign setup before the scenario begins.

Squads never upgrade during a battle.

This keeps gameplay simple while allowing meaningful long-term progression.

(Current implementation—double-sided cards, rotational layouts, etc.—will be determined during component design.)

---

# Squad Identity

Each battlefield standee represents one squad.

Standees include:

- Squad artwork
- Squad number

Example:

Spearmen 1

Spearmen 2

Spearmen 3

Spearmen 4

The matching Squad Card on the player's Command Board uses the same identifier.

This allows players to quickly determine which squad corresponds to which battlefield standee.

---

# Health Tracking

Health is tracked on the Command Board rather than the battlefield.

Current direction:

Each Squad Card uses a simple health slider or cube moving along a printed track.

Avoid:

- Stacks of damage tokens.
- Recounting damage.
- Excessive bookkeeping.

The game tracks current state, not damage history.

---

# Battlefield Information

The battlefield intentionally contains very little bookkeeping.

Battlefield components communicate only:

- Position
- Facing (if applicable)
- Squad identity

All remaining information lives on the Command Board.

This reinforces one of the game's core design pillars:

Keep the battlefield focused on tactical decisions rather than administrative tasks.

---

# Color Coding

Each faction uses a consistent player color.

Examples:

- David — Purple
- Saul — Blue
- Philistines — Red
- Amalekites — Green

The following components share that color:

- Command Board
- Standees
- Health sliders
- Initiative markers
- (Potentially) Orders Deck backs

This allows players to identify ownership at a glance.

---

# Component Philosophy

The game should minimize unique components.

Where possible:

One standee represents a squad.

One Squad Card represents all progression levels of that squad.

Campaign progression changes the Squad Card configuration rather than requiring entirely new components.

This reduces production cost while increasing replayability.

---

# New Design Principle

Whenever possible:

Complexity belongs on the Command Board.

Simplicity belongs on the battlefield.

Players should spend their attention making tactical decisions—not managing components.

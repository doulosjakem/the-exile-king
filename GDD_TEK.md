# The Exile King
## Game Design Document (Draft v0.4)

---

# Design Pillars

## Command Over Individual Heroics

The player does not primarily control individual warriors.

The player commands a company.

Victory comes from:
- Choosing the right orders.
- Timing actions correctly.
- Positioning forces effectively.
- Maintaining command structure.

---

## Positioning Over Arithmetic

The game should reward:
- Formation.
- Terrain control.
- Timing.
- Tactical choices.

Avoid excessive modifiers and calculations.

---

## Small Disciplined Companies

A smaller, coordinated force should be capable of defeating a larger disorganized enemy.

Numbers matter, but leadership matters more.

---

## Tactical Difficulty, Mathematical Simplicity

Decisions should be difficult.

Resolution should be simple.

Avoid stacking:
- Terrain bonuses.
- Ability bonuses.
- Equipment bonuses.
- Multiple combat modifiers.

---

## Elegance

The battlefield should remain the focus.

Whenever possible:

- Track information through board state.
- Avoid searching through decks.
- Avoid unnecessary bookkeeping.
- Use simple terminology.
- Prefer decisions over administration.

---

# Orders System

Cards represent the commands available to a commander.

The player's army is represented through their Orders Deck.

---

# Orders Deck

Each company has an Orders Deck.

Cards come from:

- Commander Orders
- Unit Orders
- Shared Orders

Example: David's Company

| Source | Cards |
|---|---|
| David | 2 David Orders |
| Spearmen x3 | 3 Spearman Orders |
| Archer x1 | 1 Archer Order |
| Scout x1 | 1 Scout Order |

Total: 7 Orders

The Orders Deck represents command capability.

---

# Orders in Hand

Orders currently available to issue.

Players may hold a maximum of 4 Orders.

Players normally draw 2 Orders during preparation.

Additional Orders may be gained through:

- Commander abilities.
- Rally effects.
- Tactical actions.
- Scenario effects.

---

# Issued Orders

Orders that have already been given.

After use, cards move to the Issued Orders pile.

Issued Orders cannot normally be used again until recovered.

Recovered through:

- Brainstorm.
- Regroup.
- Other abilities.

---

# Lost Orders

Orders permanently removed from the campaign.

Lost Orders represent:

- Fallen units.
- Broken command structures.
- Loss of battlefield capability.

Lost Orders do not return.

---

# Round Structure

Each Round:

1. Preparation Phase
2. Initiative Phase
3. Action Phase
4. End Phase

---

# 1. Preparation Phase

All players simultaneously:

1. Draw 2 Orders.
2. Choose an Initiative Order.
3. Choose a Support Order.
4. Place both face down.

Players may use abilities before choosing cards if allowed.

---

# 2. Initiative Phase

Reveal Initiative Orders.

Players act from lowest initiative number to highest.

Tie breakers:

1. Lower Initiative on Support Order.
2. Player choice.

---

# 3. Action Phase

When a player's turn begins:

Resolve either:

- Top of Initiative Order + Bottom of Support Order

OR:

- Bottom of Initiative Order + Top of Support Order

The Initiative Order determines speed.

The Support Order provides additional command.

After resolving:

Both cards move to Issued Orders unless they are Lost, Persistent, or otherwise instructed.

---

# 4. End Phase

Resolve:

- Persistent effects.
- Scenario effects.
- Victory conditions.
- Defeat conditions.

Begin next Round.

---

# Brainstorm

Brainstorm represents making quick decisions during chaos.

A player must Brainstorm when:

- They cannot draw enough Orders to function.
- Their available Orders are critically depleted.

Brainstorm:

1. Lose 1 random Order permanently.
2. Recover all Issued Orders.
3. Shuffle recovered Orders into the Orders Deck.
4. Continue play.

Brainstorm allows continuation but damages long-term command capability.

---

# Regroup

Regroup represents deliberate reorganization.

The player sacrifices immediate action to restore their company.

Regroup:

- Skip activation.
- Recover all Issued Orders.
- Lose 1 Order of choice permanently.
- Heal a small amount of health.

Regroup is safer than Brainstorm but costs battlefield momentum.

---

# Unit Loss

Units contribute Orders.

However, casualties should avoid excessive bookkeeping.

Each unit has a corresponding Order card.

When a unit is defeated:

The unit's Order becomes Lost.

No searching through decks is required.

Recommended implementation:

Unit Order cards remain associated with their units.

When the unit falls:

- Flip the card.
- Mark it Lost.
- Remove when convenient.

---

# Replacement & Recruitment

Regular soldiers can be replaced.

Between scenarios:

Players may spend Influence to recruit replacements.

Example:

Three Spearmen are lost.

The player may spend Influence to recruit:

- Two new Spearmen.
- Or one Swordsman.

Recruitment represents attracting new followers and reorganizing the company.

---

# Named Heroes & Mighty Men

Mighty Men are not ordinary units.

When defeated:

They become Wounded.

A wounded Mighty Man:

- Cannot participate.
- Returns after recovery.
- May trigger campaign events.

Named characters are valuable because they cannot simply be replaced.

---

# David's Defeat

If David is defeated:

The scenario is lost.

David's survival is a campaign requirement.

However:

David should be powerful because of leadership, not because he is simply the strongest fighter.

---

# Commander System

Every commander has their own command capability.

A commander has:

- Their own Orders Deck.
- Their own Initiative.
- Their own abilities.

This allows multiplayer scaling.

Example:

Two players:

- David
- Jonathan

Enemy:

- Saul
- Abner

Each commander contributes command capability.

---

# Multiplayer Balance

Do not balance only by unit numbers.

A force's strength includes:

- Military strength.
- Number of commanders.
- Orders available.
- Tactical flexibility.

A larger army with poor command may lose to a smaller disciplined force.

---

# Persistent Orders

Some Orders remain active.

They stay active until:

- Triggered enough times.
- The unit is destroyed.
- The player chooses to end them.
- The card is lost.

---

# Example Persistent Order

## Spear Wall

Persistent.

Effect:

Spearmen gain defensive formation.

When an enemy moves away from adjacent Spearmen:

The Spearmen may immediately attack.

Maximum: 3 triggers.

After third trigger: Lose this Order.

---

# Reactions

Units may influence combat without being activated.

Examples:

- Swordsmen: Retaliate against melee attackers.
- Spearmen: Punish enemies entering formation.
- Shield Bearers: Protect nearby allies.
- Archers: Strong ranged control.
- Scouts: Mobility and ambush.

---

# Terrain Philosophy

Terrain creates tactical choices.

Terrain primarily affects:

- Movement.
- Visibility.
- Position.
- Control.

Avoid large combat modifiers.

Examples:

| Terrain | Effect |
|---|---|
| Forest | Reduced visibility. Difficult movement. |
| Hill | Improved visibility. |
| River | Difficult crossing. |
| Thorn Brush | Movement penalty or hazard. |

---

# Combat

Combat should remain simple.

Attack:

Unit Value + Order Effect + Attack Modifier = Result

---

# Shared Attack Modifier Deck

All factions use one shared Attack Modifier Deck.

It represents:

- Battlefield uncertainty.
- Momentum shifts.
- Unpredictable circumstances.

The deck is shared.

It is not upgraded during the campaign.

---

# Initiative

Every Order has an Initiative value.

Low initiative:

- Fast.
- Reactive.

High initiative:

- Slower.
- Often stronger.

Choosing initiative is a major tactical decision.

---

# Initial Factions

Version One:

## David's Company

Identity:

Flexible leadership and adaptation.

## Saul's Army

Identity:

Formation, discipline, and authority.

## Philistines

Identity:

Heavy pressure and direct force.

## Amalekites

Identity:

Mobility, raiding, and disruption.

---

# Campaign Goals

The campaign should create stories.

Not simply:

"Did you win?"

But:

- Who survived?
- What did you sacrifice?
- Who joined you?
- What command abilities did you lose?
- How did your company change?

---

# Overall Design Goal

The player's greatest resource is not damage.

It is not health.

It is not numbers.

It is **command**.

Victory comes from issuing the right orders, at the right moment, to the right people.

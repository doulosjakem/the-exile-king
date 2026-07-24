# Unit Command Card Design Guide

## Formula

```
CARD POTENTIAL = (Action Potential × Command Multiplier) + Flexibility Modifiers + Unit Tier Modifier
```

---

## 1. Action Potential

### Basic Actions

| Action | Points |
|--------|--------|
| Move | 2 |
| Attack | 2 |
| Defend | 2 |

### Action Bonuses

| Bonus | Points |
|-------|--------|
| +1 Move | +1 |
| +1 Attack | +1 |
| +1 Defense | +1 |
| Push 1 | +1 |
| Ignore Counterattack | +1 |
| Ignore Terrain | +1 |
| Special Effect | +1 to +3 |

### Sequence Bonuses

| Number of Actions | Bonus |
|-------------------|-------|
| 2 | +0 |
| 3 | +1 |
| 4 | +2 |
| 5+ | +3 |

### Example

Move → Attack → Move

- Move: 2
- Attack: 2
- Move: 2

Action subtotal: 6  
Sequence bonus (3 actions): +1

**Action Potential = 7**

---

## 2. Command Multiplier

How many squads receive the command?

| Squads | Multiplier |
|--------|-----------|
| 1 | ×1.0 |
| 2 | ×1.75 |
| 3 | ×2.5 |
| 4 | ×3.0 |
| 5+ | ×3.5 |

### Example

Move + Attack

Action Potential: 4  
Commanding 2 squads:

4 × 1.75 = **7 Command Potential**

---

## 3. Flexibility Modifiers

### Restrictions (reduce value)

| Restriction | Modifier |
|-------------|----------|
| Specific unit type | -1 |
| Specific squad | -2 |
| Adjacent only | -1 |
| Must stay in formation | -1 |
| Cannot repeat | -1 |

### Flexibility (increases value)

| Flexibility | Modifier |
|-------------|----------|
| Any friendly squad | +1 |
| Any unit type | +2 |
| Choose after initiative | +1 |
| Can split actions | +1 |

---

## 4. Unit Tier Modifier

| Level | Modifier |
|-------|----------|
| 1 | +0 |
| 2 | +1 |
| 3 | +2 |
| 4 | +3 |

**Maximum recommended:** +3

---

## 5. Card Design Targets

### Level 1 Units

| Command / Action | Low | High |
|------------------|-----|------|
| Low Command / Low Action | 3–5 | — |
| High Command / Low Action | 5–7 | — |
| Low Command / High Action | 6–8 | — |
| High Command / High Action | 8–10 | — |

### Level 2 Units

Add approximately **+1 Potential**

### Levels 3–4

Add **+1 Potential per level**

---

## 6. Design Grid

```
                 ACTION POWER
              LOW              HIGH

COMMAND    Army Order       Coordinated Assault
POWER      5–7             8–10
HIGH

            Utility          Elite Maneuver
LOW         3–5             6–8
```

### Design Rule

Do not balance every card to the same number. Balance the **role**.

- A high-command card wins through coordination.
- A high-action card wins through tactical impact.
- Both should be valuable.

---

## 7. Worked Example

**Card:** "Advance and Strike"  
**Effect:** Move 2 + Attack (targets any squad within range)  
**Tier:** Level 1

1. **Action Potential**
   - Move: 2
   - Attack: 2
   - Sequence: +0 (2 actions)
   - Subtotal: 4

2. **Command Multiplier**
   - Targets 1 squad: ×1.0
   - 4 × 1.0 = 4

3. **Flexibility Modifiers**
   - Any friendly squad: +1
   - Can split actions: +1
   - +2

4. **Unit Tier**
   - Level 1: +0

5. **Total:** 4 + 2 + 0 = **6**

This falls in the High Command / High Action range for Level 1 — an elite-style card.

# Command Cards — Master Catalog

> **Design Philosophy:** Cards answer *"What orders am I giving?"* Each card represents a tactical command David can issue to his warband. Your army composition determines which cards are available.

---

## Card Anatomy

Every Command Card has:

```
┌─────────────────┐
│   Card Title     │
├─────────────────┤
│                  │
│   Card Art       │
│   (illustration) │
│                  │
├─────────────────┤
│ TOP ABILITY      │
│ [name] — [desc]  │
├─────────────────┤
│ BOTTOM ABILITY   │
│ [name] — [desc]  │
├─────────────────┤
│ [Lose] tag (if   │
│  card is lost    │
│  after use)      │
└─────────────────┘
```

---

## Deck Building

Before a scenario, your command deck is built from your army composition:

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

**Rule:** 1 copy per unit type brought, up to a max of 2 copies per card type.

---

## Universal Commands

Every army has access to basic commands. These are always included regardless of army composition.

| Card | Top | Bottom | Lose? |
|---|---|---|---|
| **March** | — | Move up to 2 units of one type. | No |
| **Engage** | — | Up to 2 units of one type attack. | No |

Universal commands are weaker than specialized commands — they provide no bonuses.

---

## David's Company Command Cards

These cards are unlocked by bringing the corresponding unit type.

### David's Leadership
| | |
|---|---|
| **Unit Type** | David |
| **Top** | Command David + 1 ally: both may move and attack. Adjacent allies +1 damage this turn. |
| **Bottom** | Move David up to 3 spaces. |
| **Lose?** | No |

### Swordsmen Advance
| | |
|---|---|
| **Unit Type** | Swordsman |
| **Top** | Command Swordsmen: Up to 3 Swordsmen may move and attack. +1 attack if adjacent to another Swordsman. |
| **Bottom** | Move: Move up to 2 Swordsmen. |
| **Lose?** | No |

### Archer Volley
| | |
|---|---|
| **Unit Type** | Archer |
| **Top** | Command Archers: Up to 2 Archers attack. Must target enemies within range. |
| **Bottom** | Reposition: Move up to 2 Archers. |
| **Lose?** | No |

### Spear Wall
| | |
|---|---|
| **Unit Type** | Spearman |
| **Top** | Command Spearmen: Up to 2 Spearmen attack. Gain 1 Shield vs melee this turn. |
| **Bottom** | Move: Move up to 2 Spearmen. They may not be targeted by melee until next turn. |
| **Lose?** | No |

### Slinger Skirmish
| | |
|---|---|
| **Unit Type** | Slinger |
| **Top** | Command Slingers: Up to 2 Slingers attack. Ignore cover. |
| **Bottom** | Move: Move up to 2 Slingers. They gain +1 move this turn. |
| **Lose?** | No |

### Scout Recon
| | |
|---|---|
| **Unit Type** | Scout |
| **Top** | Command Scouts: Up to 2 Scouts move and attack. They cannot be targeted until next turn. |
| **Bottom** | Move: Move up to 3 Scouts. |
| **Lose?** | No |

### Refugee Aid
| | |
|---|---|
| **Unit Type** | Refugee |
| **Top** | Heal: Heal 1 HP on up to 2 units. |
| **Bottom** | Move: Move up to 2 Refugees to safety (away from enemies). |
| **Lose?** | No |

---

## Card Removal by Casualty

When the last unit of a type is eliminated, remove one matching command card from the deck.

| Unit Type Eliminated | Card Removed |
|---|---|
| Last Swordsman | Swordsmen Advance |
| Last Archer | Archer Volley |
| Last Spearman | Spear Wall |
| Last Slinger | Slinger Skirmish |
| Last Scout | Scout Recon |
| Last Refugee | Refugee Aid |
| David | David's Leadership |

**Priority:** Remove from Deck first, then Hand, then Spent pile. Card moves to Lost pile permanently.

---

## Deck Rules Summary

| Rule | Details |
|---|---|
| **Starting hand** | 2 cards |
| **Draw per turn** | Up to hand size (hand fills to 4) |
| **Recovery** | Camp or Brainstorm to return Spent cards |
| **Cards chosen per turn** | 2 |
| **Resolve** | Top of card A + Bottom of card B |
| **After resolve** | Both cards → Spent pile |
| **Lose on use** | Card → Lost pile (instead of Spent) |
| **Lost recovery** | Only via run reward or special ability |
| **Empty deck** | Auto-refresh from Spent pile |
| **Starting deck** | Built from army composition + universal commands |
| **Max hand size** | 4 cards |

---

## Card Ability Icons (Future)

For visual clarity, each ability type should have a small icon on the card:

| Ability | Icon Concept |
|---|---|
| Attack | Crossed swords |
| Move | Sandal footprint |
| Buff / Shield | Shield |
| Heal | Red crescent / drop |
| Multi-target | Two figures |
| Lose | Skull / broken seal |

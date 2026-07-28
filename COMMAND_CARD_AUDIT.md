# Command Card Audit Context — The Exile King

## Current State
All command card designs are in `command_cards/unit_types/**/*.md`. The text below is the **exact current ability wording** for every card. This is what needs mechanical validation.

---

## David's Company

### David (Commander)
| Card | Top | Bottom |
|---|---|---|
| Shepherd's Call | Activate David + 1 adjacent ally: both may move and attack. Adjacent allies gain +1 damage. | Move David up to 3. After moving, David may issue a command to 1 adjacent friendly unit: that unit may activate immediately. |
| **Activations:** | 3 | 2 |

### Swordsman
| Card | Top | Bottom |
|---|---|---|
| Shepherd's Advance | Activate up to 3 Swordsmen: each may move and attack. +1 attack if adjacent to another Swordsman. | Move up to 2 Swordsmen up to 2 tiles each. |
| Shepherd's Formation | Shield Wall: adjacent Swordsmen gain +1 defense until next player turn. (2 activations) | Covenant Support: Swordsmen may attack without penalty when adjacent to friendly Spearmen. (1 activation) |
| **Init:** | 6/2 | 4/5 |

### Spearman
| Card | Top | Bottom |
|---|---|---|
| Shepherd's Wall | Activate up to 2 Spearmen: each moves up to 2 tiles and attacks with +1 damage vs charging enemies. | Activate up to 2 Spearmen: each gains brace (+1 defense vs melee until next turn). |
| Shepherd's Screen | Screen: adjacent friendly units gain -1 damage taken. (2 activations) | Spear Wall: Spearmen may make free attack when enemy enters melee range. (1 activation) |
| **Init:** | 5/3 | 3/6 |

Note: There is a third card "Spearman Formation" in the faction file with text about Brace Shields. Need to check if this conflicts with the unit type file.

### Slinger
| Card | Top | Bottom |
|---|---|---|
| Shepherd's Strike | Activate up to 2 Slingers: each may move then attack. If moved ≥2 tiles, attack gains +1 damage. | Activate up to 2 Slingers: move up to 3 tiles each. |
| Stone Barrage | Activate all Slingers: combine fire on one target. Each Slinger adds +1 damage. | Activate 1 Slinger: attack. If another Slinger is within 2 tiles, this attack gains +1 damage. |
| **Init:** | 8/4 | 9/2 |

### Archer
| Card | Top | Bottom |
|---|---|---|
| Shepherd's Volley | Activate up to 2 Archers: each attacks. Must target enemies within range. | Activate up to 2 Archers: move and gain Aim (+1 dmg on next shot if stationary). |
| Shepherd's Mark | Overwatch: Archers may make free attack when enemy moves into range. (1 activation) | Marksman: one Archer ignores 1 defense this turn. (2 activations) |
| **Init:** | 6/3 | 5/5 |

### Scout
| Card | Top | Bottom |
|---|---|---|
| Wilderness Eye | Activate 1 Scout: move up to 4 tiles (ignores terrain), then make a free attack. | Activate 1 Scout: move up to 3 tiles. If ends adjacent to enemy, retreat 1 tile after interaction. |
| Wilderness Ambush | Ambush: Scouts start hidden. First attack gains +2 damage and enemy cannot counter. (1 activation) | Screen: Scouts block LoS for enemies within 1 tile. (2 activations) |
| **Init:** | 7/5 | 6/4 |

### Shield Bearer
| Card | Top | Bottom |
|---|---|---|
| Shepherd's Shield | Adjacent friendly units gain +1 defense until next player turn. (2 activations) | Bracing: Shield Bearer gains +1 defense this turn. |
| Wilderness Advance | Activate Shield Bearer: move 1 tile. Adjacent enemies cannot move through this tile. (1 activation) | Allies adjacent to Shield Bearer ignore hazardous terrain. (2 activations) |
| **Init:** | 4/5 | 3/6 |

### Refugee
| Card | Top | Bottom |
|---|---|---|
| Provision | Heal 1 HP on up to 2 friendly units. (3 activations) | Move up to 2 Refugees to safety (away from enemies). Refugees cannot be targeted by melee while moving. (2 activations) |
| **Init:** | N/A | N/A |

### Outcast
| Card | Top | Bottom |
|---|---|---|
| Fugitive's Charge | Outcasts may move up to 3 spaces and attack. Gain +1 Attack on this attack. | Move up to 2 Outcasts. Outcasts gain +2 Defense against ranged attacks this turn. |
| **Init:** | 2 | 3 |

### Veteran
| Card | Top | Bottom |
|---|---|---|
| Battle-Tested | Veterans attack with +1 Attack. If this attack defeats an enemy, Veterans may immediately attack an adjacent enemy. | Veterans gain +2 Defense this turn. Adjacent allied units gain +1 Defense until your next turn. |
| **Init:** | 3 | 2 |

### Mighty Men
| Card | Top | Bottom |
|---|---|---|
| Mighty Men's Charge | Gain +1 Attack. If the attack defeats an enemy, move 1 space. | When a nearby ally would take damage: Mighty Men may move adjacent and take 1 damage instead. |
| **Init:** | 3 | 2 |

---

## Jonathan's Followers

### Jonathan (Commander)
| Card | Top | Bottom |
|---|---|---|
| Jonathan's Charge | Activate Jonathan: move and attack. All Loyal Guards within 2 tiles gain +1 defense this turn. | Activate Jonathan: grant one Elite Archer within 2 tiles the ability to attack twice this turn. |
| **Init:** | 7 | 3 |

### Loyal Guard
| Card | Top | Bottom |
|---|---|---|
| Covenant Guard | Shield Wall: Loyal Guards gain +2 defense until next player turn if adjacent to Jonathan. (2 activations) | Protect Commander: move Loyal Guard adjacent to friendly commander; commander gains -1 damage taken. (1 activation) |
| **Init:** | 5 | 4 |

### Elite Archer
| Card | Top | Bottom |
|---|---|---|
| Benjamin's Arrow | Target one enemy with an Elite Archer. This Archer gains +1 attack and ignores 1 defense. | Activate Elite Archer: move up to 2 tiles, then attack with +1 range this turn. |
| True Aim | If Elite Archer has not moved this turn: attack with +2 range and +1 damage. | Activate Elite Archer: attack. If stationary, gain +1 damage. |
| **Init:** | 8/3 | 9/2 |

### Archer
| Card | Top | Bottom |
|---|---|---|
| Covenant Volley | Activate up to 2 Archers: each attacks. Must target enemies within range. Gain +1 attack if Jonathan is within 2 tiles. | Activate up to 2 Archers: move and gain Aim (+1 dmg on next shot if stationary). |
| Benjamin's Eye | Overwatch: Archers may make free attack when enemy moves into range. (1 activation) | Marksman: one Archer ignores 1 defense this turn. If stationary, gain +1 range this turn. (2 activations) |
| **Init:** | 6/3 | 5/5 |

### Spearman
| Card | Top | Bottom |
|---|---|---|
| Tribe's Wall | Activate up to 2 Spearmen: each moves up to 2 tiles and attacks with +1 damage vs charging enemies. | Activate up to 2 Spearmen: each gains brace (+1 defense vs melee until next turn). |
| Tribe's Screen | Screen: adjacent friendly units gain -1 damage taken. (2 activations) | Benjamite Thrust: Spearmen attack with reach with +1 damage. (1 activation) |
| **Init:** | 5/3 | 4/5 |

### Shield Bearer
| Card | Top | Bottom |
|---|---|---|
| Covenant Shield | Adjacent friendly units gain +1 defense until next player turn. (2 activations) | Bracing: Shield Bearer gains +1 defense this turn. |
| Commander's Advance | Activate Shield Bearer: move 1 tile. Adjacent enemies cannot move through this tile. (1 activation) | Allies adjacent to Shield Bearer ignore hazardous terrain. (2 activations). If Jonathan is adjacent, Shield Bearer gains +1 defense. |
| **Init:** | 4/5 | 3/6 |

---

## Saul's Kingdom

### Abner (Commander)
| Card | Top | Bottom |
|---|---|---|
| Abner's Command | Issue an order to all units of one type within 2 spaces of Abner: Those units may activate immediately this turn. | All Saul's Kingdom units within 2 spaces of Abner gain +1 Attack this turn. |
| **Init:** | 3 | 2 |

### Royal Guard
| Card | Top | Bottom |
|---|---|---|
| Royal Shield | When Royal Guard is attacked by melee, gain +3 Defense. After the attack, the attacker loses 1 Activation next turn. | Royal Guard may form a wall with another adjacent Royal Guard. Both gain +2 Defense until your next turn. |
| King's Wall | Activate Royal Guard: move 1 tile. Adjacent enemies cannot move through this tile. (1 activation) | Allies adjacent to Royal Guard ignore hazardous terrain. (2 activations). If Abner is adjacent, Royal Guard gains +1 defense. |
| **Init:** | 4/5 | 3/6 |

### Benjamite Spearman
| Card | Top | Bottom |
|---|---|---|
| Benjamite Charge | Benjamite Spearmen may move 2 spaces and attack. If the target is an Infantry unit, gain +2 Attack instead of +1. | Benjamite Spearmen gain +2 Defense. Adjacent friendly Infantry units also gain +1 Defense. |
| **Init:** | 3 | 2 |

### Israelite Archer
| Card | Top | Bottom |
|---|---|---|
| Israelite Volley | All Israelite Archers attack the same enemy. Gain +1 total Attack for each Archer in range. | Archers cannot be targeted by melee this turn. |
| **Init:** | 3 | 2 |

### Officer
| Card | Top | Bottom |
|---|---|---|
| Officer's Boost | Choose 1 adjacent allied unit. That unit gains +2 Attack and +1 Defense until your next turn. | Choose 1 adjacent allied unit. That unit may activate immediately this turn. |
| **Init:** | 3 | 2 |

### Elite Bodyguard
| Card | Top | Bottom |
|---|---|---|
| Guard | Elite Bodyguard may move adjacent to a Commander (Saul or Abner). Until your next turn, the Commander gains +2 Defense when Elite Bodyguards are adjacent. | When an adjacent enemy attacks the Commander, the Elite Bodyguard may intercept: take the damage instead. The Elite Bodyguard is eliminated after intercepting. |
| **Init:** | 2 | 3 |

---

## Philistines (Achish's Host)

### Achish (Commander)
| Card | Top | Bottom |
|---|---|---|
| Philistine Might | Activate Achish: move up to 2, then attack. All adjacent Philistines gain Shielded (first damage prevented this turn). | Place on Command Board. Adjacent Giants and Heavy Infantry gain +1 defense. (2 activations) |
| **Init:** | 7 | 3 |

### Swordsman
| Card | Top | Bottom |
|---|---|---|
| Philistine Advance | Activate up to 3 Swordsmen: each may move and attack. Gain +1 attack if moved ≥2 tiles. | Move up to 2 Swordsmen up to 2 tiles each. |
| Iron Resolve | Adjacent friendly Swordsmen gain +1 defense until next player turn. (2 activations) | Chariot Support: Swordsmen may attack without penalty when adjacent to friendly Chariots. (1 activation) |
| **Init:** | 6/2 | 4/5 |

### Spearman
| Card | Top | Bottom |
|---|---|---|
| Philistine Spearmen | Activate up to 2 Spearmen: each moves up to 2 tiles and attacks with +1 damage vs charging enemies. | Activate up to 2 Spearmen: each gains brace (+1 defense vs melee until next turn). |
| Ekron Screen | Screen: adjacent friendly units gain -1 damage taken. (2 activations) | Chariot Lane: Spearmen do not block friendly Chariot movement. (1 activation) |
| **Init:** | 5/3 | 3/6 |

### Archer
| Card | Top | Bottom |
|---|---|---|
| Ekron Volley | Activate up to 2 Archers: each attacks. Enemies hit lose 1 movement next turn. | Activate up to 2 Archers: move 1 tile each and gain +1 range this turn. |
| Ekron Aim | Opening Volley: Archers attack before all movement this turn. (1 activation) | Covering Fire: after an ally moves, one Archer may make a free attack. (2 activations) |
| **Init:** | 6/3 | 5/4 |

### Shield Bearer
| Card | Top | Bottom |
|---|---|---|
| Iron Bulwark | Adjacent friendly units gain +1 defense until next player turn. (2 activations) | Bracing: Shield Bearer gains +1 defense this turn. |
| Shield Advance | Activate Shield Bearer: move 1 tile. Adjacent enemies cannot move through this tile. (1 activation) | Allies adjacent to Shield Bearer ignore hazardous terrain. (2 activations) |
| **Init:** | 4/5 | 3/6 |

### Heavy Infantry
| Card | Top | Bottom |
|---|---|---|
| Iron Shield Wall | Gain +2 Defense this turn. Cannot be pushed or moved by enemy effects this turn. | Heavy Infantry attacks with +2 Attack. After the attack, may move 1 space. |
| **Init:** | 3 | 2 |

### Chariot
| Card | Top | Bottom |
|---|---|---|
| Chariot Charge | Activate Chariot: move up to 3 tiles (must move ≥2), then attack with +1 damage. Push target 1 tile. | Activate Chariot: move up to 3 tiles through friendly units without obstruction. |
| Coastal Charge | Breakthrough: Chariot attacks and pushes target 2 tiles instead of 1. (1 activation) | Chariot ignores rough terrain penalties this turn. (2 activations) |
| **Init:** | 9/4 | 8/5 |

### Champion
| Card | Top | Bottom |
|---|---|---|
| Champion's Duel | Choose 1 enemy unit. Champion attacks with +2 Attack. If this attack defeats an enemy champion or hero, Champion may attack again immediately. | Champion gains +3 Defense this turn. Champion cannot be targeted by non-champion or non-hero units. |
| **Init:** | 3 | 2 |

### Lords
| Card | Top | Bottom |
|---|---|---|
| Lord's Decree | Issue an order to all Philistine units within 3 spaces: those units may activate immediately this turn. | All Philistine units within 3 spaces gain +1 Attack and +1 Defense until your next turn. |
| **Init:** | 3 | 2 |

---

## Amalekites

### Chieftain (Commander)
| Card | Top | Bottom |
|---|---|---|
| Raid | Chieftain may move 2 spaces and attack. If the attack defeats an enemy, the Chieftain may move 1 additional space. | Chieftain attacks an adjacent enemy unit. Deal 1 damage and push the target 2 spaces. |
| **Init:** | 3 | 2 |

### Raider
| Card | Top | Bottom |
|---|---|---|
| Raid Charge | Raiders may move 3 spaces and attack. Gain +1 Attack if this attack targets a unit with lower HP than the Raider. | All Raiders may move 3 spaces. They cannot be targeted by melee until your next turn. They can still be targeted by ranged attacks. |
| **Init:** | 3 | 2 |

### Slinger
| Card | Top | Bottom |
|---|---|---|
| Desert Storm | All Amalekite Slingers attack the same enemy. Gain +1 total Attack for each Slinger in range. | Slingers may move 2 spaces and attack once. Movement does not trigger opportunity attacks this turn. After attacking, Slingers must move at least 1 space further or suffer 1 damage. |
| **Init:** | 3 | 2 |

### Desert Scout
| Card | Top | Bottom |
|---|---|---|
| Desert Flank | When an enemy enters line of sight of a Desert Scout, the Scout attacks immediately before normal initiative order. Deal 1 additional damage. | Choose an enemy unit. Reveal: Movement, Attack, HP. All Desert Scouts gain +1 Attack against that unit this turn. |
| **Init:** | 2 | 3 |

### Desert Mount
| Card | Top | Bottom |
|---|---|---|
| Desert Charge | Desert Mount may move 4 spaces and attack. Gain +2 Attack for this attack. If the attack defeats an enemy, may move 2 additional spaces. Ignores terrain penalties during this move. | Desert Mount may move 3 spaces. All enemy units within 1 space of the Desert Mount's path suffer 1 damage. Ignores terrain penalties during this move. |
| **Init:** | 3 | 2 |

---

## Ekron's Host

### Philistine Lord (Commander)
| Card | Top | Bottom |
|---|---|---|
| Ekron's Decree | Activate Philistine Lord: move up to 2, then attack. Adjacent allies gain +1 attack this turn. | Grant one Champion or Heavy Infantry within 2 tiles an extra activation. |
| **Init:** | 6 | 4 |

### Chariot
| Card | Top | Bottom |
|---|---|---|
| Coastal Charge | Activate Chariot: move up to 3 tiles (must move ≥2), then attack with +1 damage. Push target 1 tile. | Activate Chariot: move up to 3 tiles through friendly units without obstruction. |
| Plain Breaker | Breakthrough: Chariot attacks and pushes target 2 tiles instead of 1. (1 activation) | Chariot ignores rough terrain penalties this turn. (2 activations) |
| Hit and Run | Hit and Run: Chariot may move after attacking (up to 1 tile). (2 activations) | Chariot gains +1 defense for each tile moved this activation. (1 activation) |
| **Init:** | 9/4 | 8/5 |

### Slinger
| Card | Top | Bottom |
|---|---|---|
| Coastal Sling | Activate up to 2 Slingers: each may move then attack. If moved ≥2 tiles, attack gains +1 damage. | Activate up to 2 Slingers: move up to 3 tiles each. |
| Stone Storm | Activate all Slingers: combine fire on one target. Each Slinger adds +1 damage. Targets hit cannot move next turn. | Activate 1 Slinger: attack. If another Slinger is within 2 tiles, this attack gains +1 damage. Targets hit cannot move next turn. |
| **Init:** | 8/4 | 9/2 |

### Swordsman
| Card | Top | Bottom |
|---|---|---|
| Philistine Advance | Activate up to 3 Swordsmen: each may move and attack. Gain +1 attack if moved ≥2 tiles. | Move up to 2 Swordsmen up to 2 tiles each. |
| Iron Resolve | Adjacent friendly Swordsmen gain +1 defense until next player turn. (2 activations) | Chariot Support: Swordsmen may attack without penalty when adjacent to friendly Chariots. (1 activation) |
| **Init:** | 6/2 | 4/5 |

### Spearman
| Card | Top | Bottom |
|---|---|---|
| Ekron Hedge | Activate up to 2 Spearmen: each moves up to 2 tiles and attacks with +1 damage vs charging enemies. | Activate up to 2 Spearmen: each gains brace (+1 defense vs melee until next turn). |
| Ekron Line | Brace Shields: adjacent Spearmen gain +2 defense until next player turn. (2 activations) | Chariot Lane: Spearmen do not block friendly Chariot movement. (1 activation) |
| Ekron Screen | Screen: adjacent friendly units gain -1 damage taken. (2 activations) | Spear Support: Spearmen attack with reach without penalty against charging enemies. (1 activation) |
| **Init:** | 5/3 | 4/5 |

### Shield Bearer
| Card | Top | Bottom |
|---|---|---|
| Iron Bulwark | Adjacent friendly units gain +1 defense until next player turn. (2 activations) | Bracing: Shield Bearer gains +1 defense this turn. |
| Shield Advance | Activate Shield Bearer: move 1 tile. Adjacent enemies cannot move through this tile. (1 activation) | Allies adjacent to Shield Bearer ignore hazardous terrain. (2 activations) |
| **Init:** | 4/5 | 3/6 |

---

## Unit Stats (from GDD.md)

| Unit | Range | Attack | Defense | Health | Move | Notes |
|---|---|---|---|---|---|---|
| Swordsman | 1 | 2 | 1 | 2 | 2 | Standard melee |
| Spearman | 2 (reach) | 2 | 1 | 2 | 2 | Anti-charge |
| Shield Bearer | 1 | 1 | 2 | 3 | 1 | Tank/defender |
| Heavy Infantry | 1 | 2 | 2 | 3 | 1 | Slow, hits hard |
| Scout | 2 | 1 | 1 | 1 | 3 | Fast recon |
| Refugee | 1 | 0 | 1 | 1 | 1 | Support/non-combat |
| Archer | 2 | 2 | 1 | 2 | 2 | Standard ranged |
| Slinger | 3 | 1 | 1 | 2 | 3 | David's skirmisher |
| Loyal Guard | 1 | 2 | 1 | 2 | 2 | Jonathan's infantry |
| Elite Archer | 2 | 2 | 1 | 2 | 2 | Jonathan's ranged |
| Benjamite Spearman | 1 | 3 | 1 | 2 | 2 | Elite infantry |
| Israelite Archer | 3 | 1 | 1 | 1 | 0 | Stationary ranged |
| Officer | 1 | 1 | 1 | 2 | 2 | Support |
| Elite Bodyguard | 1 | 3 | 2 | 2 | 2 | Protect commander |
| Giant | 1 | 3 | 2 | 4 | 1 | Slow, devastating |
| Chariot | 1 | 2 | 1 | 2 | 3 | Fast assault |
| Champion | 1 | 3 | 1 | 3 | 2 | Duelist |
| Chieftain | 1 | 2 | 1 | 2 | 3 | Commander |
| Raider | 1 | 2 | 1 | 1 | 3 | Fast melee |
| Desert Scout | 1 | 1 | 1 | 1 | 4 | Fast skirmisher |
| Desert Mount | 1 | 3 | 1 | 3 | 4 | Mobile heavy |

---

## Known Issues to Resolve

1. **Faction file drift:** `command_cards/factions/*.md` may have different card text than `command_cards/unit_types/*/*.md` for the same unit. Need to harmonize.
2. **Card count consistency:** Some units have 2 cards, some have 3. Verify each faction's unit type has the intended number.
3. **Activation budget:** Verify that total activations across a unit's cards matches the intended power curve.
4. **"Chariot Support" / "Chariot Lane":** These are faction-specific synergy abilities. Need to confirm they have mechanical meaning in the ruleset.
5. **Ambush / Overwatch:** These are reaction-style abilities. Need to confirm the rules support "enemy moves into range" triggers.
6. **Formation cards:** `command_cards/formations/*.md` has faction-wide formations. These are lower priority but need review.

---

## Rules Reference (from printable-co-op-prototype.md)

- **Card Resolution:** Player picks 2 cards from hand, reveals both, resolves top of one + bottom of the other.
- **Initiative:** Higher acts first within a phase.
- **Army Size (Small):** 6 units (1 commander + 5), 10-card deck.
- **Starting Hand:** 4 cards.
- **Deck Building:** 1 random card per unit type brought + 1 random commander card + fill from 2 chosen pools.
- **Fatigue:** Lose 1 random card from hand → Lost pile after each turn.
- **Casualty:** When last unit of a type dies, remove 1 matching card from deck/hand/spent → Lost pile.

---

## Suggested Validation Order

1. **Cross-reference check:** For each unit, grep the faction file and unit type file and ensure card names and effects match exactly.
2. **Activation budget check:** Sum activations per unit and compare across factions for equivalent units.
3. **Ambiguity check:** Read each ability for rules-lawyering holes (undefined terms, missing triggers, etc.).
4. **Power curve check:** Compare common units across factions to ensure no faction's base unit is strictly better.

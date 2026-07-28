# Biblical Formation Theming — Implementation Plan

## Goal
Retheme all command card formations across all factions to use biblical/ancient Near Eastern terminology, remove anachronistic Greek terms, and give each faction's common units distinct identities.

## Scope

### In Scope
- All unit type markdown files under `command_cards/unit_types/**/*.md`
- Art prompt references in `PROMPTS.md`
- Generation manifests: `formation_cards_batch.json`, `generation_manifest.json`
- Prompt dictionaries: `existing_prompts.json`, `review_art_ollama.py`, `fix_review.py`, `add_all_prompts.py`
- Master reference: `COMMAND_CARDS.md`
- Faction-wide formation files under `command_cards/formations/*.md`

### Out of Scope
- GDD mechanical system changes (hex grid, activations, turn structure)
- Core combat math (damage values, HP tiers)
- Unity implementation files (no C# changes yet — Sprint 3 not started)

---

## Preserved Baseline

Everything below is held constant. Only card names and ability flavor text change.

- All unit stat blocks unchanged
- All activation counts unchanged
- All card counts per unit unchanged
- All target counts unchanged
- All initiative values unchanged
- All mechanical triggers (when X, then Y) preserved in function, reworded in flavor

---

## Prompt Key Strategy

Art prompt keys in `PROMPTS.md`, `existing_prompts.json`, `generation_manifest.json`, and `formation_cards_batch.json` remain **stable**. Display names on cards may diverge from prompt keys.

Example: the art prompt key `swordsmen-advance` stays the same even if the card display name changes from "Swordsmen Advance" to "Shepherd's Advance."

This avoids regenerating art manifests and preserves existing generated assets.

---

## Faction Naming Themes

| Faction | Theme | Naming Vocabulary |
|---|---|---|
| **David's Company** | Shepherd-warriors, wilderness, faith, underdog | Shepherd's, Wilderness, Bethlehem, Faith, David's, Fugitive |
| **Saul's Kingdom** | Royal army, organized, professional | Royal, King's, Benjamite, Saul's, Guard |
| **Jonathan's Followers** | Covenant, loyalty, elite, noble | Covenant, Jonathan's, Benjamite, Loyal, Bound |
| **Philistines / Ekron's Host** | Iron, chariots, sea-peoples, mercenary | Philistine, Iron, Ekron, Gittite, Coastal, Mercenary |
| **Amalekites** | Desert, raid, nomads, swift | Desert, Sand, Raid, Nomad, Swift, Scorched |

---

## Anachronism Fixes (Mandatory)

| Current Term | Replace With | Reason |
|---|---|---|
| Phalanx (any faction) | Shield Line, Spear Support, Formation | Greek hoplite phalanx is 7th century BC anachronism for c. 1000 BC Israel |
| Lock Shields | Brace Shields, Raise Shields | Interlocking shield walls are specifically Greek |
| Iron Wall (Israelite units) | Royal Wall, King's Shield | Israelites explicitly lacked iron (1 Sam 13:19-22); Philistines had iron |
| Camel Rider (unit type) | Desert Mount | Notes already acknowledge camels were not war mounts for Amalekites |
| Swordsmen Advance (generic) | Shepherd's Advance / Covenant Advance / Philistine Advance | Too generic, no faction identity |

---

## Unit Type Renames

| Current Path/Name | New Path/Name | Reason |
|---|---|---|
| `command_cards/unit_types/AMALEKITES/camel_rider/CAMEL_RIDER.md` | `command_cards/unit_types/AMALEKITES/desert_mount/DESERT_MOUNT.md` | Remove anachronistic "Camel Rider" unit type name |
| `Camel Rider` (display name in file) | `Desert Mount` | Same |
| All GDD.md references to Camel Rider | Desert Mount | Consistency |
| All POST_MVP_GDD.md references to Camel Rider | Desert Mount | Consistency |

---

## Common Unit Faction Identity

Currently identical cards are shared across David's Company, Jonathan's Followers, and Ekron's Host for: Swordsman, Spearman, Archer, Slinger, Shield Bearer, Scout.

Each faction's common unit cards will receive:
1. Unique card names reflecting faction theme
2. One faction-specific ability tweak (same activation count, same power level, different tactical expression)
3. Preserved mechanical baseline so cross-faction balance holds

### Swordsman (Standard Melee)

#### David's Company
**Card 1: Shepherd's Advance**
- Top: Activate up to 3 Swordsmen: each may move and attack. Gain +1 attack if adjacent to another Swordsman.
- Bottom: Move up to 2 Swordsmen up to 2 tiles each.

**Card 2: Shepherd's Resolve**
- Top: Adjacent friendly Swordsmen gain +1 defense until next player turn. (2 activations)
- Bottom: Shepherd's Support: Swordsmen may attack without penalty when adjacent to friendly Spearmen. (1 activation)

#### Jonathan's Followers
**Card 1: Covenant Advance**
- Top: Activate up to 2 Swordsmen: each may move and attack. Gain +1 attack if Jonathan is within 2 tiles.
- Bottom: Move up to 2 Swordsmen up to 2 tiles each.

**Card 2: Covenant Hold**
- Top: Adjacent friendly Swordsmen gain +1 defense until next player turn. (2 activations)
- Bottom: Jonathan's Aegis: if Jonathan is adjacent, Swordsmen gain +1 defense. (1 activation)

#### Ekron's Host
**Card 1: Philistine Advance**
- Top: Activate up to 3 Swordsmen: each may move and attack. Gain +1 attack if moved ≥2 tiles.
- Bottom: Move up to 2 Swordsmen up to 2 tiles each.

**Card 2: Iron Resolve**
- Top: Adjacent friendly Swordsmen gain +1 defense until next player turn. (2 activations)
- Bottom: Chariot Support: Swordsmen may attack without penalty when adjacent to friendly Chariots. (1 activation)

---

### Spearman (Reach Melee)

#### David's Company
**Card 1: Shepherd's Wall**
- Top: Activate up to 2 Spearmen: each moves up to 2 tiles and attacks with +1 damage vs charging enemies.
- Bottom: Activate up to 2 Spearmen: each gains brace (+1 defense vs melee until next turn).

**Card 2: Shepherd's Screen**
- Top: Screen: adjacent friendly units gain -1 damage taken. (2 activations)
- Bottom: Spear Wall: Spearmen may make free attack when enemy enters melee range. (1 activation)

#### Jonathan's Followers
**Card 1: Tribe's Wall**
- Top: Activate up to 2 Spearmen: each moves up to 2 tiles and attacks with +1 damage vs charging enemies.
- Bottom: Activate up to 2 Spearmen: each gains brace (+1 defense vs melee until next turn).

**Card 2: Tribe's Screen**
- Top: Screen: adjacent friendly units gain -1 damage taken. (2 activations)
- Bottom: Benjamite Thrust: Spearmen attack with reach with +1 damage. (1 activation)

#### Ekron's Host
**Card 1: Ekron Hedge**
- Top: Activate up to 2 Spearmen: each moves up to 2 tiles and attacks with +1 damage vs charging enemies.
- Bottom: Activate up to 2 Spearmen: each gains brace (+1 defense vs melee until next turn).

**Card 2: Ekron Screen**
- Top: Screen: adjacent friendly units gain -1 damage taken. (2 activations)
- Bottom: Chariot Lane: Spearmen do not block friendly Chariot movement. (1 activation)

---

### Archer (Ranged)

#### David's Company
**Card 1: Shepherd's Volley**
- Top: Activate up to 2 Archers: each attacks. Must target enemies within range.
- Bottom: Activate up to 2 Archers: move and gain Aim (+1 dmg on next shot if stationary).

**Card 2: Shepherd's Mark**
- Top: Overwatch: Archers may make free attack when enemy moves into range. (1 activation)
- Bottom: Marksman: one Archer ignores 1 defense this turn. (2 activations)

#### Jonathan's Followers
**Card 1: Covenant Volley**
- Top: Activate up to 2 Archers: each attacks. Must target enemies within range. Gain +1 attack if Jonathan is within 2 tiles.
- Bottom: Activate up to 2 Archers: move and gain Aim (+1 dmg on next shot if stationary).

**Card 2: Benjamin's Eye**
- Top: Overwatch: Archers may make free attack when enemy moves into range. (1 activation)
- Bottom: Marksman: one Archer ignores 1 defense this turn. If stationary, gain +1 range this turn. (2 activations)

#### Ekron's Host
**Card 1: Ekron Volley**
- Top: Activate up to 2 Archers: each attacks. Must target enemies within range. Enemies hit lose 1 movement next turn.
- Bottom: Activate up to 2 Archers: move 1 tile each and gain +1 range this turn.

**Card 2: Ekron Aim**
- Top: Opening Volley: Archers attack before all movement this turn. (1 activation)
- Bottom: Covering Fire: after an ally moves, one Archer may make a free attack. (2 activations)

---

### Slinger (Skirmisher)

#### David's Company
**Card 1: Shepherd's Strike**
- Top: Activate up to 2 Slingers: each may move then attack. If moved ≥2 tiles, attack gains +1 damage.
- Bottom: Activate up to 2 Slingers: move up to 3 tiles each.

**Card 2: Stone Barrage**
- Top: Activate all Slingers: combine fire on one target. Each Slinger adds +1 damage.
- Bottom: Activate 1 Slinger: attack. If another Slinger is within 2 tiles, this attack gains +1 damage.

#### Jonathan's Followers
**Card 1: Valley Shot**
- Top: Activate up to 2 Slingers: each may move then attack. If moved ≥2 tiles, attack gains +1 damage.
- Bottom: Activate up to 2 Slingers: move up to 3 tiles each.

**Card 2: Benjamite Volley**
- Top: Activate all Slingers: combine fire on one target. Each Slinger adds +1 damage.
- Bottom: Activate 1 Slinger: attack. If Jonathan is within 2 tiles, this attack gains +1 damage.

#### Ekron's Host
**Card 1: Coastal Sling**
- Top: Activate up to 2 Slingers: each may move then attack. If moved ≥2 tiles, attack gains +1 damage.
- Bottom: Activate up to 2 Slingers: move up to 3 tiles each.

**Card 2: Stone Storm**
- Top: Activate all Slingers: combine fire on one target. Each Slinger adds +1 damage. Targets hit cannot move next turn.
- Bottom: Activate 1 Slinger: attack. If another Slinger is within 2 tiles, this attack gains +1 damage. Targets hit cannot move next turn.

---

### Shield Bearer (Tank/Defender)

#### David's Company
**Card 1: Shepherd's Shield**
- Top: Adjacent friendly units gain +1 defense until next player turn. (2 activations)
- Bottom: Bracing: Shield Bearer gains +1 defense this turn.

**Card 2: Wilderness Advance**
- Top: Activate Shield Bearer: move 1 tile. Adjacent enemies cannot move through this tile. (1 activation)
- Bottom: Allies adjacent to Shield Bearer ignore hazardous terrain. (2 activations)

#### Jonathan's Followers
**Card 1: Covenant Shield**
- Top: Adjacent friendly units gain +1 defense until next player turn. (2 activations)
- Bottom: Bracing: Shield Bearer gains +1 defense this turn.

**Card 2: Commander's Advance**
- Top: Activate Shield Bearer: move 1 tile. Adjacent enemies cannot move through this tile. (1 activation)
- Bottom: Allies adjacent to Shield Bearer ignore hazardous terrain. (2 activations). If Jonathan is adjacent, Shield Bearer gains +1 defense.

#### Ekron's Host
**Card 1: Iron Bulwark**
- Top: Adjacent friendly units gain +1 defense until next player turn. (2 activations)
- Bottom: Bracing: Shield Bearer gains +1 defense this turn.

**Card 2: Shield Advance**
- Top: Activate Shield Bearer: move 1 tile. Adjacent enemies cannot move through this tile. (1 activation)
- Bottom: Allies adjacent to Shield Bearer ignore hazardous terrain. (2 activations)

---

### Scout (Light / Fast Recon)

#### David's Company
**Card 1: Wilderness Eye**
- Top: Activate 1 Scout: move up to 4 tiles (ignores terrain), then make a free attack.
- Bottom: Activate 1 Scout: move up to 3 tiles. If ends adjacent to enemy, retreat 1 tile after interaction.

**Card 2: Wilderness Ambush**
- Top: Ambush: Scouts start hidden. First attack gains +2 damage and enemy cannot counter. (1 activation)
- Bottom: Screen: Scouts block LoS for enemies within 1 tile. (2 activations)

#### Jonathan's Followers
**Card 1: Covenant Scout**
- Top: Activate 1 Scout: move up to 4 tiles (ignores terrain), then make a free attack.
- Bottom: Activate 1 Scout: move up to 3 tiles. If ends adjacent to enemy, retreat 1 tile after interaction.

**Card 2: Benjamin's Eye**
- Top: Ambush: Scouts start hidden. First attack gains +1 damage and enemy cannot counter. (1 activation)
- Bottom: Screen: Scouts block LoS for enemies within 1 tile. (2 activations)

#### Ekron's Host
**Card 1: Coast Raider**
- Top: Activate 1 Scout: move up to 4 tiles (ignores terrain), then make a free attack.
- Bottom: Activate 1 Scout: move up to 3 tiles. If ends adjacent to enemy, retreat 1 tile after interaction.

**Card 2: Raider's Eye**
- Top: Ambush: Scouts start hidden. First attack gains +1 damage and enemy cannot counter. (1 activation)
- Bottom: Screen: Scouts block LoS for enemies within 1 tile. (2 activations)

---

## Unique Unit Renames

| Unit | Faction | Current | Proposed |
|---|---|---|---|
| David | David's Company | Leadership / Rally | Shepherd's Call / Wilderness Rally |
| Refugee | David's Company | Aid / Evacuate | Provision / Flight |
| Outcast | David's Company | Desperate Charge / Fall Back | Fugitive's Charge / Scatter |
| Veteran | David's Company | Veteran Formation / Battle Hardened | Battle-Tested / Unbroken |
| Mighty Men | David's Company | David's Champions / Stand Together | Mighty Men's Charge / Covenant Bond |
| Abner | Saul's Kingdom | Command / Battle Cry | Abner's Command / Host's Cry |
| Officer | Saul's Kingdom | Buff / Rally Point | Officer's Boost / Rally Standard |
| Royal Guard | Saul's Kingdom | Ancient Shield / Iron Wall | Royal Shield / King's Wall |
| Benjamite Spearman | Saul's Kingdom | Tribe Charge / Hold Ranks | Benjamite Charge / Tribe's Stand |
| Israelite Archer | Saul's Kingdom | Ranked Volley / Hold the Range | Israelite Volley / Defender's Range |
| Elite Bodyguard | Saul's Kingdom | Protect / Intercept | Guard / Shield Brother |
| Jonathan | Jonathan's Followers | Jonathan's Leadership | Jonathan's Charge / Covenant Rally |
| Loyal Guard | Jonathan's Followers | Guard Formation | Covenant Guard / Shield Brother |
| Elite Archer | Jonathan's Followers | Jonathan's Mark / Perfect Shot | Benjamin's Arrow / True Aim |
| Achish | Philistines | Achish's Strength | Philistine Might / Lord's Command |
| Heavy Infantry | Philistines | Iron Wall / Power Strike | Iron Shield Wall / Heavy Strike |
| Chariot | Philistines | War Charge / Wheel of War | Chariot Charge / Scythed Wheel |
| Champion | Philistines | Duelist's Stance / Champion's Respite | Champion's Duel / Victor's Pause |
| Lords | Philistines | Command / Iron Edict | Lord's Decree / Iron Word |
| Chieftain | Amalekites | Raid / Desert Ambush | Raid / Desert Ambush (keep) |
| Raider | Amalekites | Raid Charge / Scatter | Raid Charge / Scatter (keep) |
| Slinger | Amalekites | Desert Storm / Stone Gallop | Desert Storm / Nomad Gallop |
| Desert Scout | Amalekites | Desert Flank / Eyes on the Target | Desert Flank / Desert Watch |
| Desert Mount | Amalekites | Raid Charge / Desert Dash | Desert Charge / Sand Dash |
| Philistine Lord | Ekron's Host | Lord's Command | Ekron's Decree / Coastal Command |
| Chariot | Ekron's Host | Chariot Charge / Formation 1 / Formation 2 | Coastal Charge / Plain Breaker / Hit and Run |

---

## Faction-Wide Formations

Files under `command_cards/formations/*.md` contain faction-wide formation cards. These also need biblical renaming.

| Faction File | Current Names | Action |
|---|---|---|
| `SAULS_KINGDOM.md` | KING'S DIVISION, RELENTLESS ADVANCE, BATTLE LINE | Rename to biblical Hebrew/Israelite terminology |
| `PHILISTINES.md` | PHILISTINE DOMINANCE, IRON SHIELD WALL, CHARIOT CHARGE LINE | Keep Philistine flavor; ensure no anachronisms |
| `JONATHANS_FOLLOWERS.md` | LOYAL BOND, SWIFT RETREAT, FAITHFUL STAND | Rename to covenant/loyalty terminology |
| `AMALEKITES.md` | DESERT RAID, STEPPES FLANK, HARASSMENT CAMPAIGN | Keep desert raid flavor |

These are lower priority than unit cards but are in scope for this pass.

---

## Ability Rework Principles

1. **Preserve activation counts and target counts** — same number of activations, same number of units targeted
2. **Preserve power budget** — if old ability gave +2 Attack, new ability gives equivalent combat value
3. **Biblical flavor over mechanics** — rename and reflavor, don't redesign core loop
4. **Faction distinction through minor variance** — e.g., David's swordsmen get +1 when adjacent (underdog pack tactics), Philistine swordsmen get +1 when charging (professional shock)

---

## Files to Update

### Unit Type Files (all formation card names and abilities)

```
command_cards/unit_types/DAVIDS_COMPANY/david/DAVID.md
command_cards/unit_types/DAVIDS_COMPANY/refugee/REFUGEE.md
command_cards/unit_types/DAVIDS_COMPANY/outcast/OUTCAST.md
command_cards/unit_types/DAVIDS_COMPANY/swordsman/SWORDSMAN.md
command_cards/unit_types/DAVIDS_COMPANY/spearman/SPEARMAN.md
command_cards/unit_types/DAVIDS_COMPANY/slinger/SLINGER.md
command_cards/unit_types/DAVIDS_COMPANY/archer/ARCHER.md
command_cards/unit_types/DAVIDS_COMPANY/scout/SCOUT.md
command_cards/unit_types/DAVIDS_COMPANY/veteran/VETERAN.md
command_cards/unit_types/DAVIDS_COMPANY/mighty_man/MIGHTY_MAN.md
command_cards/unit_types/DAVIDS_COMPANY/shield_bearer/SHIELD_BEARER.md
command_cards/unit_types/SAULS_KINGDOM/ABNER.md
command_cards/unit_types/SAULS_KINGDOM/OFFICER.md
command_cards/unit_types/SAULS_KINGDOM/royal_guard/ROYAL_GUARD.md
command_cards/unit_types/SAULS_KINGDOM/benjamite_spearman/BENJAMITE_SPEARMAN.md
command_cards/unit_types/SAULS_KINGDOM/israelite_archer/ISRAELITE_ARCHER.md
command_cards/unit_types/SAULS_KINGDOM/elite_bodyguard/ELITE_BODYGUARD.md
command_cards/unit_types/JONATHANS_FOLLOWERS/jonathan/JONATHAN.md
command_cards/unit_types/JONATHANS_FOLLOWERS/loyal_guard/LOYAL_GUARD.md
command_cards/unit_types/JONATHANS_FOLLOWERS/elite_archer/ELITE_ARCHER.md
command_cards/unit_types/JONATHANS_FOLLOWERS/spearman/SPEARMAN.md
command_cards/unit_types/JONATHANS_FOLLOWERS/archer/ARCHER.md
command_cards/unit_types/JONATHANS_FOLLOWERS/shield_bearer/SHIELD_BEARER.md
command_cards/unit_types/PHILISTINES/achish/ACHISH.md
command_cards/unit_types/PHILISTINES/spearman/SPEARMAN.md
command_cards/unit_types/PHILISTINES/archer/ARCHER.md
command_cards/unit_types/PHILISTINES/heavy_infantry/HEAVY_INFANTRY.md
command_cards/unit_types/PHILISTINES/chariot/CHARIOT.md
command_cards/unit_types/PHILISTINES/champion/CHAMPION.md
command_cards/unit_types/PHILISTINES/lords/LORDS.md
command_cards/unit_types/PHILISTINES/shield_bearer/SHIELD_BEARER.md
command_cards/unit_types/AMALEKITES/chieftain/CHIEFTAIN.md
command_cards/unit_types/AMALEKITES/raider/RAIDER.md
command_cards/unit_types/AMALEKITES/slinger/SLINGER.md
command_cards/unit_types/AMALEKITES/desert_scout/DESERT_SCOUT.md
command_cards/unit_types/AMALEKITES/desert_mount/DESERT_MOUNT.md
command_cards/unit_types/EKRONS_HOST/swordsman/SWORDSMAN.md
command_cards/unit_types/EKRONS_HOST/spearman/SPEARMAN.md
command_cards/unit_types/EKRONS_HOST/shield_bearer/SHIELD_BEARER.md
command_cards/unit_types/EKRONS_HOST/slinger/SLINGER.md
command_cards/unit_types/EKRONS_HOST/chariot/CHARIOT.md
command_cards/unit_types/EKRONS_HOST/philistine_lord/PHILISTINE_LORD.md
```

### Cross-Reference Files
```
PROMPTS.md — Update display names in card art prompt descriptions; keep prompt keys stable
formation_cards_batch.json — Update card display names if changed; keep prompt keys stable
generation_manifest.json — Update display names if changed; keep prompt keys stable
existing_prompts.json — Update prompt display strings if changed; keep keys stable
review_art_ollama.py — Update EXPECTED_PROMPTS display strings if changed; keep keys stable
fix_review.py — Update formation prompt display strings if changed; keep keys stable
add_all_prompts.py — Update if it references formation display names
COMMAND_CARDS.md — Update unit type index links if filenames change
command_cards/formations/*.md — Update faction-wide formation display names
GDD.md — Update Camel Rider references to Desert Mount
POST_MVP_GDD.md — Update Camel Rider references to Desert Mount
```

---

## Validation Checklist

1. **No anachronisms**: grep for "phalanx", "lock shields", "iron wall" (in Israelite files), "camel rider" — all must return zero results in unit type files
2. **Faction uniqueness**: Each common unit type in David's Company, Jonathan's Followers, and Ekron's Host has different card names
3. **Mechanical parity**: Each faction's common unit has same number of cards and activations as before
4. **Cross-references intact**: All prompt keys in generation_manifest.json match keys in PROMPTS.md and existing_prompts.json
5. **Art prompt names**: grep for old display names in PROMPTS.md — none should remain except as historical references
6. **Unit type index**: COMMAND_CARDS.md links still resolve to correct files
7. **PROMPTS.md clean**: grep PROMPTS.md for "phalanx" — must return zero
8. **Desert Mount consistency**: grep GDD.md and POST_MVP_GDD.md for "Camel Rider" — must return zero

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Balance shift from ability changes | Gameplay feels unbalanced | Keep activation counts and target counts identical; preserve power budget |
| Broken art generation pipeline | Art prompts no longer match card names | Keep prompt keys stable; only change display names |
| Cross-reference rot | Dead links in COMMAND_CARDS.md | Use grep to verify all internal links after changes |
| Scope creep into GDD mechanics | Unplanned system changes | Explicitly out of scope; only card data and naming changes |
| Folder rename breaks imports | Code or scripts referencing old path | Update all cross-reference files atomically with folder rename |

---

## Execution Order

Batch by faction to keep diffs reviewable and reduce merge conflict surface.

1. **David's Company** (11 files + 1 folder rename for desert_mount)
   - Rename `AMALEKITES/camel_rider/` → `AMALEKITES/desert_mount/` and `CAMEL_RIDER.md` → `DESERT_MOUNT.md`
   - Update all 11 David's Company unit type files
   - Update GDD.md and POST_MVP_GDD.md Camel Rider references

2. **Saul's Kingdom** (6 files)

3. **Jonathan's Followers** (6 files)
   - Common unit variants tested against David's pattern

4. **Philistines** (7 files)

5. **Amalekites** (4 files + use renamed desert_mount folder)

6. **Ekron's Host** (6 files)
   - Common unit variants tested against Jonathan's pattern

7. **Faction-wide formations** (4 files under `command_cards/formations/`)

8. **Cross-reference files**
   - PROMPTS.md
   - formation_cards_batch.json
   - generation_manifest.json
   - existing_prompts.json
   - review_art_ollama.py
   - fix_review.py
   - add_all_prompts.py
   - COMMAND_CARDS.md

9. **Validation**
   - Run all 8 grep checks from Validation Checklist
   - Verify faction-wide formation files for anachronisms
   - Spot-check 2-3 unit files per faction for correct full ability text

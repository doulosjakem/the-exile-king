# Asset Generation Prompts — SDXL Turbo (Refined)

> Art Direction: **Hand-painted historical illustration / illuminated manuscript / parchment aesthetic**
> NOT realistic. NOT fantasy. Watercolor and ink, muted earth tones, ancient chronicle style.
> Current tool: Draw Things on iPhone with SDXL Turbo.
> Try: SDXL v1 8-bit if Turbo keeps producing artifacts.

---

## Golden Prompt Template

Use this as your base prompt for all unit portraits. Adjust the description for each unit.

```
ONE PERSON ONLY, solo portrait, waist-up, [UNIT DESCRIPTION], hand-painted historical illustration, watercolor and ink, aged parchment, board game card art, centered composition, family friendly
```

**Standard Negative Prompt (add to every generation):**

```
two people, duplicate, twin, clone, double head, extra body, merged body, extra arms, extra hands, malformed weapon, blurry, watermark, text, photorealistic, anime, fantasy armor, modern clothing, gore, nsfw, ugly, deformed
```

---

## Technique Notes

- **Start prompt with "ONE PERSON ONLY"** — significantly reduces duplicate figures
- **Waist-up portraits** — avoids mangled legs/feet
- **Generate equipment separately** — weapons/shields as standalone images, composite in Unity
- **Use strong negative prompts** — copy the full negative list above every time
- **Multiple generations per unit** — pick the best one, don't settle for artifacts
- **SDXL Turbo limitation:** frequently produces extra heads, merged bodies, mangled hands. When this happens, either:
  - Regenerate with same seed but stronger negative prompt
  - Switch to SDXL v1 8-bit (slower but cleaner)

---

## Hex Tile Textures (512×512, tileable)

| Asset | Prompt |
|---|---|
| **Sand tile** | `top-down flat hex tile, sandy desert terrain, warm beige, parchment texture, subtle grain, watercolor wash, board game style, seamless, 512x512` |
| **Rock tile** | `top-down flat hex tile, rocky gravel, gray-brown, stone texture, watercolor wash, board game style, seamless, 512x512` |
| **Grass tile** | `top-down flat hex tile, dry savanna grass, warm green-brown, ink wash, board game style, seamless, 512x512` |

---

## Unit Portrait Prompts (256×256 or 512×512, transparent background)

Generate **waist-up portraits** and composite onto token bases in Unity. Start every prompt with:

> `ONE PERSON ONLY, solo portrait, waist-up,`

### Player Units

| Unit | Prompt Addition |
|---|---|
| **David** | `young David, bronze age Israelite shepherd-warrior, leather armor over linen tunic, brown cloak, determined expression, Judean wilderness` |
| **Swordsman** | `ancient Israelite swordsman, bronze sword, round shield, leather armor, blue tunic, battle-ready stance` |
| **Spearman** | `ancient Israelite spearman, long spear, leather armor, blue tunic, defensive stance` |
| **Slinger** | `ancient Israelite slinger, crouching, holding leather sling, pouch at belt, leather armor, blue tunic` |
| **Archer** | `ancient Israelite archer, drawing bow, leather armor, blue tunic, focused expression` |
| **Scout** | `ancient Israelite scout, slim build, javelin in hand, light leather armor, blue tunic, alert expression` |

### Enemy Units (Amalekites)

| Unit | Prompt Addition |
|---|---|
| **Raider** | `ancient Amalekite raider, nomadic desert warrior, red-brown cloak, spear, weathered face` |
| **Slinger** | `ancient Amalekite slinger, crouching, red-brown cloak, leather sling, desert warrior` |
| **Archer** | `ancient Amalekite mounted archer, drawing composite bow, red-brown cloak, on horseback` |
| **Scout** | `ancient Amalekite scout, red-brown cloak, javelin, lean build, desert warrior` |
| **Camel Rider** | `ancient Amalekite camel rider, spear, red-brown cloak, riding camel, desert warrior` |
| **Chieftain** | `ancient Amalekite chieftain, tall headdress, red-brown cloak, commanding presence, weathered and fierce` |

---

## Equipment & Weapon Prompts (transparent background)

| Asset | Prompt |
|---|---|
| **Bronze sword** | `bronze age short sword, single person holding, hand-painted illustration, watercolor, transparent background` |
| **Leather shield** | `round leather shield, bronze rim, hand-painted illustration, watercolor, transparent background` |
| **Spear** | `bronze-tipped wooden spear, hand-painted illustration, watercolor, transparent background` |
| **Sling** | `leather sling with pouch, hand-painted illustration, watercolor, transparent background` |
| **Bow** | `composite bow, hand-painted illustration, watercolor, transparent background` |
| **Camel** | `dromedary camel, side view, hand-painted illustration, watercolor, transparent background` |

---

## UI Elements (transparent background)

| Asset | Prompt |
|---|---|
| **End Turn button** | `rounded rectangle, aged parchment color, ink border, game UI, flat design, 200x60` |
| **Overwork button** | `rounded rectangle, faded red-earth color, ink border, game UI, flat design, 200x60` |
| **Command card back** | `blank aged parchment card, rectangular, ink border, hand-painted texture, 250x350` |
| **HP bar background** | `thin bar, dark brown ink wash, game UI, 100x10` |
| **HP bar fill** | `thin bar, faded crimson, game UI, 100x10` |
| **Action icon (move)** | `simple sandal footprint, ink drawing style, white on transparent, 32x32` |
| **Action icon (attack)** | `simple bronze sword, ink drawing style, white on transparent, 32x32` |
| **Reward panel** | `aged parchment panel, dark edges, ink border, rounded corners, 400x300` |

---

## Tips for Better Results

1. **"ONE PERSON ONLY" at the start** — this is the single most effective fix for duplicate figures
2. **Strong negative prompt every time** — don't skip it, paste the full list
3. **Generate 3-5 versions** of each unit, pick the cleanest
4. **Upscale in Draw Things** if available, then resize to 256×256 in Unity
5. **Output naming convention:**
   - `hex_sand.png`, `hex_rock.png`, `hex_grass.png`
   - `unit_david.png`, `unit_swordsman.png`, `unit_spearman.png`, `unit_slinger.png`, `unit_archer.png`, `unit_scout.png`
   - `enemy_raider.png`, `enemy_slinger.png`, `enemy_archer.png`, `enemy_scout.png`, `enemy_camel.png`, `enemy_chieftain.png`
   - `equip_sword.png`, `equip_shield.png`, `equip_spear.png`, `equip_sling.png`, `equip_bow.png`, `equip_camel.png`
   - `ui_endturn.png`, `ui_overwork.png`, `ui_card_back.png`
6. **Save a prompt log** — note which seed gave the best result for each unit so you can regenerate consistently

---

## Commercial Use

- **SDXL Turbo** is licensed under CreativeML Open RAIL-M — generated outputs are yours to use commercially
- **SDXL v1 8-bit** — same license, same commercial rights
- All code in this project is your property — use it freely
- Unity Personal license is fine until $200K annual revenue

---

## Development Priority

> Don't let perfect art delay gameplay.

1. Get functional art in place (even placeholder colors)
2. Make combat fun
3. Clean up UI
4. Improve art later

The game itself is valuable. The development process is equally valuable.
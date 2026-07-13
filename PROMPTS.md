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

Full prompt (unit name + description + suffix). Add negative prompt from the template above.

| Unit | Full Prompt |
|---|---|
| **David** | `ONE PERSON ONLY, young David as a bronze age Israelite fugitive commander, simple linen tunic with leather chest piece, brown wool cloak pinned at shoulder, bronze short sword at his hip, leather sling tucked in his belt, shepherd's staff in hand, determined and watchful expression, standing on a rocky Judean hillside under an overcast sky, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family-friendly` |
| **Swordsman** | `ONE PERSON ONLY, young Israelite swordsman, bronze age warrior, simple linen tunic with layered leather vest, worn brown cloak, bronze short sword in hand, small round hide-covered shield on his arm, leather wrapped grip, sturdy sandals, battle-ready stance, alert expression, standing on rocky Judean ground, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family-friendly` |
| **Spearman** | `ONE PERSON ONLY, young Israelite spearman, bronze age skirmisher, simple linen tunic with leather shoulder piece, brown cloak tied at neck, long bronze-tipped wooden spear held in both hands, small hide shield slung across his back, knife at his waist, sandals, defensive ready stance, focused expression, standing on a hillside overlooking wilderness valleys, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family-friendly` |
| **Slinger** | `ONE PERSON ONLY, young Israelite slinger, bronze age skirmisher, simple linen tunic with leather vest, worn brown cloak, leather sling in hand with pouch at his belt, pouch of smooth stones at his hip, small knife, crouched lightly on the balls of his feet, ready to pivot and throw, alert watchful expression, standing on a rocky slope, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family-friendly` |
| **Archer** | `ONE PERSON ONLY, young Israelite archer, bronze age wilderness hunter, simple linen tunic with leather vest, brown cloak, wooden composite bow in hand with arrow nocked, quiver of arrows slung across his back, knife at his waist, sandals, drawing the bow with focused precision, standing on a ridge overlooking the valleys, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family-friendly` |
| **Scout** | `ONE PERSON ONLY, young Israelite scout, bronze age wilderness tracker, lean shepherd-skirmisher, simple linen tunic with leather vest, worn brown cloak, sandals, sling at his belt, short spear, small round hide shield slung across his back, knife at his waist, alert watchful expression, standing lightly on rocky Judean hillside overlooking the valleys, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family-friendly` |

### Enemy Units (Amalekites)

| Unit | Full Prompt |
|---|---|
| **Raider** | `ONE PERSON ONLY, Amalekite raider, bronze age nomadic desert warrior, worn red-brown wool cloak wrapped around his body, leather tunic underneath, bronze-tipped spear in hand, curved knife at his belt, weathered and lean face, windblown hair, hardened squinting expression, standing on sandy desert ground with rocky outcrops, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family-friendly` |
| **Slinger** | `ONE PERSON ONLY, Amalekite slinger, bronze age nomadic skirmisher, dusty red-brown cloak wrapped loose, leather sling in hand with pouch of stones at his hip, simple leather tunic, barefoot or sandaled, crouched low in a mobile throwing stance, alert predatory expression, standing on sandy desert terrain, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family-friendly` |
| **Archer** | `ONE PERSON ONLY, Amalekite mounted archer, bronze age nomadic horseman, dusty red-brown cloak flowing, riding a small hardy desert horse, composite bow drawn with arrow aimed, quiver strapped to the horse's flank, weathered focused expression, horse mid-stride on open desert plain, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family-friendly` |
| **Scout** | `ONE PERSON ONLY, Amalekite scout, bronze age desert tracker, lean wind-hardened build, dusty red-brown cloak patched and worn, short javelin in hand, leather sling at his belt, small hide shield slung across his back, sandals, crouched and scanning the horizon, keen narrowed eyes, standing on a rocky desert ridge, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family-friendly` |
| **Camel Rider** | `ONE PERSON ONLY, Amalekite camel rider, bronze age desert warrior, dusty red-brown cloak and headwrap, bronze-tipped spear held upright, riding a tall dromedary camel, leather reins in hand, weathered stern expression, camel standing on sandy desert ground with distant mountains, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family-friendly` |
| **Chieftain** | `ONE PERSON ONLY, Amalekite chieftain, bronze age nomadic warlord, dark red-brown wool cloak trimmed with rough wool fringe, leather and bronze chest piece, weathered authoritative face, gray-streaked beard, bronze short sword at his hip, spear in hand, tall headdress wrapped in desert cloth, standing on a rocky outcrop overlooking his warriors, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family-friendly` |

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
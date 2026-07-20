# Asset Generation Prompts — The Exile King

> **Art Direction:** Hand-painted historical illustration / illuminated manuscript / aged parchment aesthetic.
> **NOT realistic photography. NOT fantasy. NOT anime.**
> Think: medieval manuscript marginalia, ancient chronicle illustrations, watercolor and ink line art.
> Muted earth tones — ochre, umber, faded ochre, parchment tan, faded crimson, charcoal ink.
> All figures wear historically accurate bronze age Levantine clothing: linen tunics, leather armor/vests, wool cloaks, sandals. Bronze weapons (short swords, spears with bronze tips, composite bows). No plate armor, no steel, no fantasy elements.
> **Era lock:** Every prompt includes "bronze age Levantine", "NOT medieval, NOT fantasy, NOT European" to prevent DreamShaper from drifting into medieval/anachronistic territory.
> **Recommended tool:** ComfyUI + DreamShaper XL Lightning (see ART_GENERATION_GUIDE.md)

---

## Universal Negative Prompt (all generations)

```
photorealistic, hyperrealistic, realistic skin texture, photograph, cinematic lighting, ray tracing, 3d render, octane render, unity engine, video game screenshot, modern clothing, plate armor, steel armor, chainmail, scale armor, fantasy armor, elaborate armor, longbow, long sword, greatsword, crossguard, medieval helmet, horned helmet, winged helmet, knight, crusader, viking, samurai, European castle, stone castle, heraldry, coat of arms, shield with cross, shield with lion, glowing, neon, bright colors, anime, manga, cartoon, digital art, illustration, signature, watermark, text, logo, ugly, deformed, blurry, low quality, worst quality, bad anatomy, extra limbs, merged body, duplicate, clone, two people, three people, group, crowd, nsfw, gore, blood
```

**Always use this negative prompt. Do not shorten it. This prevents photorealism, fantasy, medieval drift, and DreamShaper-specific artifacts.**

---

## Prompt Guidance

- **Command card art:** Do NOT prefix with "ONE PERSON ONLY" — these are tactical scenes with multiple figures
- **Unit standees:** full upright figure (head to toe) on a small circular base, transparent background, NOT a flat silhouette or medallion
- **Era lock:** Every character prompt includes "bronze age Levantine / Israelite", "NOT medieval, NOT fantasy, NOT European", and "Mediterranean complexion, dark hair, Semitic features" to prevent model drift
- **Don't skip the negative prompt** — paste the full list every time
- **Batch 5+ per prompt** — pick the best result
- **See ART_GENERATION_GUIDE.md** for full ComfyUI setup, workflow diagrams, and step-by-step instructions

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
| **David** | `ONE PERSON ONLY, solo portrait, waist-up, young bronze age Israelite commander, bronze age Levantine man, dark curly hair and trimmed beard, simple linen tunic with leather chest piece, brown wool cloak pinned at shoulder with bronze brooch, bronze short sword at hip, leather sling tucked in belt, shepherd's staff in hand, determined watchful expression, standing on rocky Judean hillside under overcast sky, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Swordsman** | `ONE PERSON ONLY, solo portrait, waist-up, young bronze age Israelite swordsman, bronze age Levantine warrior, dark hair and short beard, simple linen tunic with layered leather vest, worn brown wool cloak pinned at shoulder, bronze short sword with leaf-shaped blade in hand, small round hide-covered shield on arm, leather wrapped grip, sandals, alert expression, standing on rocky Judean ground, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European` |
| **Spearman** | `ONE PERSON ONLY, solo portrait, waist-up, young bronze age Israelite spearman, bronze age Levantine warrior, dark hair, linen tunic with leather shoulder piece, brown cloak tied at neck, long wooden spear with bronze tip held in both hands, small hide shield slung across back, knife at waist, sandals, focused expression, standing on hillside overlooking wilderness valleys, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European` |
| **Slinger** | `ONE PERSON ONLY, solo portrait, waist-up, young bronze age Israelite slinger, bronze age Levantine skirmisher, dark hair, simple linen tunic with leather vest, worn brown cloak, leather sling in hand with pouch at belt, pouch of smooth stones at hip, small knife, crouched lightly ready to pivot and throw, alert watchful expression, standing on rocky slope, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European` |
| **Archer** | `ONE PERSON ONLY, solo portrait, waist-up, young bronze age Israelite archer, bronze age Levantine hunter, dark hair, simple linen tunic with leather vest, brown cloak, short composite bow in hand with arrow nocked, quiver of arrows slung across back, knife at waist, sandals, drawing bow with focused precision, standing on ridge overlooking valleys, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European` |
| **Scout** | `ONE PERSON ONLY, solo portrait, waist-up, young bronze age Israelite scout, bronze age Levantine tracker, lean shepherd-skirmisher, dark hair, simple linen tunic with leather vest, worn brown cloak, sandals, sling at belt, short spear, small hide shield on back, knife at waist, alert watchful expression, standing lightly on rocky Judean hillside, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European` |

### Enemy Units (Amalekites)

| Unit | Full Prompt |
|---|---|
| **Raider** | `ONE PERSON ONLY, solo portrait, waist-up, Amalekite raider, bronze age Levantine nomadic desert warrior, dark windblown hair, weathered lean face, dusty red-brown wool cloak wrapped around body, leather tunic underneath, bronze-tipped spear in hand, curved knife at belt, hardened squinting expression, standing on sandy desert ground with rocky outcrops, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European` |
| **Slinger** | `ONE PERSON ONLY, solo portrait, waist-up, Amalekite slinger, bronze age Levantine nomadic skirmisher, dark hair, dusty red-brown cloak wrapped loose, leather sling in hand with pouch of stones at hip, simple leather tunic, sandals, crouched low in mobile throwing stance, alert predatory expression, standing on sandy desert terrain, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European` |
| **Archer** | `ONE PERSON ONLY, solo portrait, waist-up, Amalekite mounted archer, bronze age Levantine nomadic horseman, dark hair, dusty red-brown cloak flowing, riding small hardy desert horse, composite bow drawn with arrow aimed, quiver strapped to horse flank, weathered focused expression, horse mid-stride on open desert plain, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European` |
| **Scout** | `ONE PERSON ONLY, solo portrait, waist-up, Amalekite scout, bronze age Levantine desert tracker, lean wind-hardened build, dark hair, dusty red-brown cloak patched and worn, short javelin in hand, leather sling at belt, small hide shield on back, sandals, crouched and scanning horizon, keen narrowed eyes, standing on rocky desert ridge, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European` |
| **Camel Rider** | `ONE PERSON ONLY, solo portrait, waist-up, Amalekite camel rider, bronze age Levantine desert warrior, dark hair, dusty red-brown cloak and headwrap, bronze-tipped spear held upright, riding tall dromedary camel, leather reins in hand, weathered stern expression, camel standing on sandy desert ground with distant mountains, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European` |
| **Chieftain** | `ONE PERSON ONLY, solo portrait, waist-up, Amalekite chieftain, bronze age Levantine nomadic warlord, dark hair and gray-streaked beard, dark red-brown wool cloak trimmed with rough fringe, leather and simple bronze chest piece, weathered authoritative face, bronze short sword at hip, spear in hand, wrapped headdress, standing on rocky outcrop overlooking warriors, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European` |

---

## Equipment & Weapon Prompts (transparent background)

| Asset | Prompt |
|---|---|
| **Bronze sword** | `bronze age short sword, leaf-shaped blade, single person holding, hand-painted illustration, watercolor, transparent background, NOT medieval, NOT fantasy, NOT European` |
| **Leather shield** | `round leather shield, bronze rim, hand-painted illustration, watercolor, transparent background, NOT medieval, NOT fantasy, NOT European` |
| **Spear** | `bronze-tipped wooden spear, hand-painted illustration, watercolor, transparent background, NOT medieval, NOT fantasy, NOT European` |
| **Sling** | `leather sling with pouch, hand-painted illustration, watercolor, transparent background, NOT medieval, NOT fantasy, NOT European` |
| **Bow** | `short composite bow, hand-painted illustration, watercolor, transparent background, NOT medieval, NOT fantasy, NOT European` |
| **Camel** | `dromedary camel, side view, hand-painted illustration, watercolor, transparent background, NOT medieval, NOT fantasy, NOT European` |

---

## UI Elements (transparent background)

| Asset | Prompt |
|---|---|
| **End Turn button** | `rounded rectangle, aged parchment color, ink border, game UI, flat design, 200x60` |
| **Command card back** | `blank aged parchment card, rectangular, ink border, hand-painted texture, 250x350` |
| **HP bar background** | `thin bar, dark brown ink wash, game UI, 100x10` |
| **HP bar fill** | `thin bar, faded crimson, game UI, 100x10` |
| **Action icon (move)** | `simple sandal footprint, ink drawing style, white on transparent, 32x32` |
| **Action icon (attack)** | `simple bronze sword, ink drawing style, white on transparent, 32x32` |
| **Reward panel** | `aged parchment panel, dark edges, ink border, rounded corners, 400x300` |
| **Card frame template** | `blank rectangular card frame, aged parchment border, ink line art style, top half and bottom half separated by a thin decorative line, space for illustration, 250x350` |

---

## Command Card Art (250×350, ink & parchment)

Generate card art for the top half of each Command Card. Style matches the unit portrait aesthetic.

### Unit-Type Specific Cards

| Card | Prompt |
|---|---|
| **Swordsmen Advance** | `scene in illuminated manuscript style, two bronze age Levantine Israelite swordsmen advancing in formation, bronze short swords raised, hide shields overlapping, dust at their heels, linen tunics and leather vests, determined expressions, aged parchment background, ink outlines with muted watercolor wash in ochre and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Archer Volley** | `scene in illuminated manuscript style, two bronze age Levantine Israelite archers on ridge aiming forward, composite bows drawn, arrows ready to loose, linen tunics, leather arm bracers, quivers on backs, aged parchment background, ink outlines with muted watercolor wash in ochre and faded ochre, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European` |
| **Spear Wall** | `scene in illuminated manuscript style, three bronze age Levantine Israelite spearmen in tight formation, long wooden spears with bronze tips angled outward, shields locked, braced defensive stance, linen tunics, leather armor, grim expressions, aged parchment background, ink outlines with muted watercolor wash in umber and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European` |
| **Slinger Skirmish** | `scene in illuminated manuscript style, two bronze age Levantine Israelite slingers in skirmish formation, leather slings raised, stones in pouches, light armor, crouched mobile stances, alert expressions, aged parchment background, ink outlines with muted watercolor wash in ochre and umber, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European` |
| **Scout Recon** | `scene in illuminated manuscript style, two bronze age Levantine Israelite scouts moving swiftly through rocky terrain, light clothing, scanning horizon, short spears and slings, alert watchful expressions, aged parchment background, ink outlines with muted watercolor wash in ochre and faded ochre, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European` |
| **Refugee Aid** | `scene in illuminated manuscript style, bronze age Levantine civilians being tended to by a soldier, simple linen tunics, worn cloaks, one soldier offering water, lean-to shelter in background, compassionate expressions, aged parchment background, ink outlines with muted watercolor wash in ochre and brown, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European` |
| **David's Leadership** | `scene in illuminated manuscript style, bronze age Levantine Israelite commander on rocky outcrop with arm raised rallying men, soldiers gathered below looking up, simple cloth banner on wooden pole, linen tunics, leather armor, wool cloaks, aged parchment background, ink outlines with muted watercolor wash in ochre and brown, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European` |

### Universal Command Cards

| Card | Prompt |
|---|---|
| **March** | `scene in illuminated manuscript style, bronze age Levantine Israelite soldiers marching in organized column across dusty ground, spears and shields at sides, linen tunics and leather vests, brown wool cloaks, steady pace, aged parchment background, ink outlines with muted watercolor wash in ochre and umber, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European` |
| **Engage** | `scene in illuminated manuscript style, bronze age Levantine Israelite soldiers charging forward with weapons raised, bronze short swords and spears, shields forward, linen tunics, leather vests, dust and motion, aged parchment background, ink outlines with muted watercolor wash in ochre and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European` |

---

## Unit Standees (512×512, then downscale to 256×256 in Unity)

**Settings:** 512×512, steps 4, CFG 3, batch 5

**Note:** Generating at 512×512 then downscaling to 256×256 in Unity gives better results than generating directly at 256×256.

These are **board game standees** — a single full upright figure (head to toe) standing on a small circular base/disc, as if cut from a cardboard or wooden standee. The figure is a clean front-facing or 3/4 view, fully colored in the hand-painted illustration style, NOT a flat silhouette. Transparent background so it can be dropped onto the hex grid in Unity.

| # | File Prefix | Prompt |
|---|---|---|
| 1 | `token_david` | `board game standee, single full upright figure from head to toe standing on a small circular base disc, hand-painted ink and watercolor illustration, a young bronze age Levantine man, bronze age Israelite, dark curly hair and short beard, simple linen tunic with leather chest piece, brown wool cloak pinned at shoulder, bronze short sword at hip, leather sling in belt, no helmet, sandals, Mediterranean complexion, dark ink outlines, full color, transparent background, centered, NOT medieval, NOT fantasy, NOT European, family friendly` |
| 2 | `token_swordsman` | `board game standee, single full upright figure from head to toe standing on a small circular base disc, hand-painted ink and watercolor illustration, a bronze age Levantine infantryman, bronze age Israelite warrior, dark hair, short beard, simple linen tunic, leather vest, brown wool cloak, small round hide-covered shield on arm, bronze short sword with leaf-shaped blade, sandals, Mediterranean features, dark ink outlines, full color, transparent background, centered, NOT medieval, NOT fantasy, NOT European, family friendly` |
| 3 | `token_spearman` | `board game standee, single full upright figure from head to toe standing on a small circular base disc, hand-painted ink and watercolor illustration, a bronze age Levantine spearman, bronze age Israelite, dark hair, linen tunic with leather shoulder piece, long wooden spear with bronze tip held in both hands, small hide shield on back, knife at waist, sandals, Mediterranean features, dark ink outlines, full color, transparent background, centered, NOT medieval, NOT fantasy, NOT European, family friendly` |
| 4 | `token_slinger` | `board game standee, single full upright figure from head to toe standing on a small circular base disc, hand-painted ink and watercolor illustration, a bronze age Levantine skirmisher, bronze age Israelite slinger, dark hair, linen tunic with leather vest, leather sling raised overhead, pouch of stones at hip, small knife, light ready stance, sandals, alert expression, dark ink outlines, full color, transparent background, centered, NOT medieval, NOT fantasy, NOT European, family friendly` |
| 5 | `token_archer` | `board game standee, single full upright figure from head to toe standing on a small circular base disc, hand-painted ink and watercolor illustration, a bronze age Levantine archer, bronze age Israelite hunter, dark hair, linen tunic, leather vest, short composite bow drawn with arrow nocked, quiver on back, knife at waist, sandals, dark ink outlines, full color, transparent background, centered, NOT medieval, NOT fantasy, NOT European, family friendly` |
| 6 | `token_scout` | `board game standee, single full upright figure from head to toe standing on a small circular base disc, hand-painted ink and watercolor illustration, a lean bronze age Levantine scout, bronze age Israelite tracker, dark hair, light linen tunic, leather vest, worn brown cloak, sling at belt, short spear, small hide shield on back, knife, alert watchful expression, sandals, dark ink outlines, full color, transparent background, centered, NOT medieval, NOT fantasy, NOT European, family friendly` |
| 7 | `token_chieftain_amalekite` | `board game standee, single full upright figure from head to toe standing on a small circular base disc, hand-painted ink and watercolor illustration, a bronze age Levantine warlord, dark red-brown wrapped headdress, dark beard, leather and simple bronze chest piece, bronze short sword at hip, spear in hand, weathered authoritative face, dark ink outlines, full color, transparent background, centered, NOT medieval, NOT fantasy, NOT European, family friendly` |
| 8 | `token_raider_amalekite` | `board game standee, single full upright figure from head to toe standing on a small circular base disc, hand-painted ink and watercolor illustration, a bronze age Levantine desert raider, dark windblown hair, weathered lean face, dusty red-brown wool cloak wrapped around body, leather tunic, bronze-tipped spear, curved knife at belt, sandals, hardened expression, dark ink outlines, full color, transparent background, centered, NOT medieval, NOT fantasy, NOT European, family friendly` |
| 9 | `token_refugee` | `board game standee, single full upright figure from head to toe standing on a small circular base disc, hand-painted ink and watercolor illustration, a bronze age Levantine civilian, simple linen tunic, worn brown cloak, bundle on stick over shoulder, sandals, weary but hopeful expression, no weapons, dark ink outlines, full color, transparent background, centered, NOT medieval, NOT fantasy, NOT European, family friendly` |

**Total: 9 prompts × 5 samples = 45 images**

---

## Hex Tiles (512×512 tileable)

**Settings:** 512×512, steps 4, CFG 3.5, batch 3

| # | File Prefix | Prompt |
|---|---|---|
| 1 | `hex_sand` | `top-down view of a flat hexagonal tile, sandy desert terrain, warm beige and light brown, subtle parchment-like texture, very fine grain, watercolor wash with soft edges, tileable seamless pattern, board game style, hand-painted texture, no grid lines, 512x512` |
| 2 | `hex_roc` | `top-down view of a flat hexagonal tile, rocky gravel and small stones, gray-brown and warm umber tones, parchment texture overlay, watercolor wash, tileable seamless pattern, board game style, hand-painted texture, no grid lines, 512x512` |
| 3 | `hex_grass` | `top-down view of a flat hexagonal tile, dry savanna grass on hard earth, warm green-brown and ochre tones, dry grass textures, watercolor wash, tileable seamless pattern, board game style, hand-painted texture, no grid lines, 512x512` |

**Total: 3 prompts × 3 samples = 9 images**

---

## UI Elements (512×512, downscale in Unity)

**Settings:** 512×512, steps 4, CFG 3.5, batch 3

Generate at larger size then downscale to target in Unity for better quality.

| # | File Prefix | Prompt | Unity target size |
|---|---|---|---|
| 1 | `ui_endturn_button` | `rounded rectangle button shape, aged warm parchment color, dark ink border outline, flat medieval manuscript style, game UI element, hand-painted texture, isolated on transparent background, family friendly` | 200×60 |
| 2 | `ui_hp_bar_bg` | `thin horizontal bar shape, dark brown ink wash texture, rough hand-painted edges, game UI health bar background, isolated on transparent background, family friendly` | 128×16 |
| 3 | `ui_hp_bar_fill` | `thin horizontal bar shape, faded crimson red ink wash, rough hand-painted edges, game UI health bar fill, isolated on transparent background, family friendly` | 128×16 |
| 4 | `ui_reward_panel` | `large aged parchment panel texture, darker edges, vignette effect, ink border with corner ornaments, rounded rectangle shape, game UI panel, hand-painted texture, isolated on transparent background, family friendly` | 400×300 |

**Total: 4 prompts × 3 samples = 12 images**

---

## Card Frame Template (512×768)

**Settings:** 512×768, steps 4, CFG 3.5, batch 3

| # | File Prefix | Prompt |
|---|---|---|
| 1 | `card_frame_template` | `blank rectangular playing card, aged parchment background, ornate decorative ink border in dark brown, thin horizontal line dividing the card into top and bottom halves, corner ornaments, medieval manuscript border style, no text, hand-painted board game card, 512x768` |

**Total: 1 prompt × 3 samples = 3 images**

---

## Summary: Complete Generation Queue

| Batch | Description | Prompts | Samples Each | Total Images |
|---|---|---|---|---|
| 1 | Unit Standees | 9 | 5 | 45 |
| 2 | Unit Portraits | 12 | 5 | 60 |
| 3 | Command Card Art — Unit Specific | 9 | 5 | 45 |
| 4 | Card Frame Template | 1 | 3 | 3 |
| 5 | Hex Tiles | 3 | 3 | 9 |
| 6 | UI Elements | 4 | 3 | 12 |
| **Total** | | **38** | | **174 images** |

Estimated time: **~10–15 minutes total** on GTX 1060 with DreamShaper XL Lightning.

---

## Quick Reference: Final Assets List

After generating and picking the best, these are the final files needed in `Assets/Textures/`:

```
Tokens/ (unit standees, full upright figure on circular base, 256x256)
  token_david.png
  token_swordsman.png
  token_spearman.png
  token_slinger.png
  token_archer.png
  token_scout.png
  token_chieftain_amalekite.png
  token_raider_amalekite.png
  token_refugee.png

Cards/Portraits/ (unit portraits for card art)
  david.png
  swordsman.png
  spearman.png
  slinger.png
  archer.png
  scout.png
  chieftain_amalekite.png
  raider_amalekite.png
  slinger_amalekite.png
  archer_amalekite.png
  scout_amalekite.png
  camel_rider_amalekite.png

Cards/Art/ (command card art, 512x768)
  card_davids_leadership.png
  card_swordsmen_advance.png
  card_archer_volley.png
  card_spear_wall.png
  card_slinger_skirmish.png
  card_scout_recon.png
  card_refugee_aid.png
  card_march.png
  card_engage.png
  card_frame_template.png

Tiles/ (hex tile textures, 512x512)
  hex_sand.png
  hex_rock.png
  hex_grass.png

UI/ (UI elements)
  ui_endturn_button.png
  ui_hp_bar_bg.png
  ui_hp_bar_fill.png
  ui_reward_panel.png
```

Some of the old filenames from earlier drafts (like `unit_david.png`, `enemy_raider.png`, `equip_sword.png`, `ui_overwork.png`) are **deprecated** by the Command Card pivot. The new unit standee system replaces unit portraits for MVP.

---

## Tips for Best Results

1. **Every prompt has era-locking language** — "bronze age Levantine", "NOT medieval, NOT fantasy, NOT European" is baked in
2. **Always paste the full negative prompt** — the new additions (chainmail, longbow, knight, crusader, etc.) are tuned to DreamShaper's specific biases
3. **If images still drift medieval** — add "Canaanite clothing, Levantine dress, Near Eastern" to the positive prompt
4. **If faces look European** — strengthen "Mediterranean complexion, Semitic features, dark curly hair, dark eyes"
5. **If weapons look wrong** — add "NO crossguard, NO longblade, short bronze blade" to positive
6. **If shields look decorated** — add "plain hide shield, no symbols, no markings, no emblems"
7. **Generate 5 versions** of each, pick the cleanest
8. **Save seeds of good results** — the seed number appears in the image metadata
9. **Downscale standees in Unity** — generate at 512×512, set Pixels Per Unit to match the board scale
10. **Check the parchment style** — if results drift toward photorealism, add "watercolor, ink outlines, not realistic, not photograph" to the positive prompt

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

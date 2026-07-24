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

## Post-MVP Content

> **All portrait prompts, box art, and faction art for Jonathan's Followers, Philistines, Girzites, Geshurites, Gezerites, Mighty Men, Joab/Amasa/Asahel, and any expansion content are maintained in `POST_MVP_GDD.md`.**
>
> This file only contains MVP art prompts needed for Sprints 3–7.

---

## Development Priority

> Don't let perfect art delay gameplay.

1. Get functional art in place (even placeholder colors)
2. Make combat fun
3. Clean up UI
4. Improve art later

**Settings:** 1024×768, steps 4, CFG 3.5, batch 3–5 per concept

All box art concepts fit the illuminated manuscript / watercolor / aged parchment aesthetic. Each concept is a distinct mood and composition for selecting the final box cover.

### Box Art Concepts

| # | Concept Key | Prompt |
|---|---|---|
| 1 | `box-art-fugitives-path` | `game box art, painting in illuminated manuscript style, David silhouetted against a rocky Judean cliff face, cloak billowing, looking back toward a distant Philistine encampment on the horizon, three tiny enemy figures pursue along a winding mountain trail, parchment sky with copperpage sepia wash, focus on isolation and pursuit, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 2 | `box-art-adullams-cave` | `game box art, painting in illuminated manuscript style, interior view of a cave mouth at dusk, David and a ragged group of outcasts huddle inside, faces lit by a small fire, outside Saul's soldiers sprawl on rocks with spears, dramatic light contrast warm firelight vs cool blue dusk, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded indigo, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 3 | `box-art-anointed-stone` | `game box art, painting in illuminated manuscript style, close-up composition a simple shepherd's staff and a sling rest on rough stone, in the background faint golden light breaks through cloud over a hill, no people the objects carry the weight, manuscript border with vine motifs, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 4 | `box-art-before-the-king` | `game box art, painting in illuminated manuscript style, David leaning on his spear gazing at a ruined city skyline in the distance, he wears a simple tunic no crown no regalia, two loyal warriors stand nearby arms crossed, dawn light, title treatment sits above in illuminated capitals, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 5 | `box-art-wilderness-march` | `game box art, painting in illuminated manuscript style, wide panoramic composition a winding column of small figures moves through a rocky desert valley, dust rises, perspective from above but not a map more like a medieval chronicle illustration flattened into a single vertical plane, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 6 | `box-art-watcher-on-the-hill` | `game box art, painting in illuminated manuscript style, David standing alone on a rocky outcrop, shield at his feet, staff in hand, below in the valley a Philistine camp smolders, smoke in thin wispy lines, composition is vertical to fit box proportions, minimal figures one man one landscape, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 7 | `box-art-refugee-column` | `game box art, painting in illuminated manuscript style, from behind a moving column of civilians with bundles and children passes through a narrow pass, soldiers guard the flanks, the scene is intimate and human the company aspect of David's warband, parchment tones with faded indigo sky, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded indigo, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 8 | `box-art-shield-wall` | `game box art, painting in illuminated manuscript style, low-angle view from ground level three Israelite spearmen locked in shield wall facing impossibly numerous Amalekite raiders, dust motion lines tension, foreground shows the rear of the shields plain leather no heraldry, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 9 | `box-art-shepherd-king` | `game box art, painting in illuminated manuscript style, David seated on a natural stone throne in a cave listening to an elder, lighting from a single torch, around them men repair weapons and tend wounds, a sense of rest before the next journey, warm amber tones, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 10 | `box-art-chieftains-challenge` | `game box art, painting in illuminated manuscript style, face-off across a dusty clearing David and the Amalekite Chieftain mirror each other both armed both looking at a small object on the ground between them a shared water skin or bread, not a duel in motion but a moment of pause before violence, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 11 | `box-art-narrow-pass` | `game box art, painting in illuminated manuscript style, top-down flattened view of a mountain pass at night, small lights flicker along the winding path, the composition reads like a tactical map on parchment, figures are tiny, tension comes from the constricted space, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded indigo, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 12 | `box-art-warlords-tent` | `game box art, painting in illuminated manuscript style, interior of a Philistine commander's tent at dusk, Achish seated on a low couch flanked by two spearmen, he holds a goblet expression unreadable, David stands before him stripped of his armor bowing slightly a fugitive at the mercy of a foreign lord, warm lamplight, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 13 | `box-art-last-stand-at-ziklag` | `game box art, painting in illuminated manuscript style, before a burned and looted settlement David kneels among smoldering timbers head bowed, behind him his warriors grip weapons, below them in shadow raiders ride away into the desert, composition is low and crushing, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 14 | `box-art-board-of-war` | `game box art, painting in illuminated manuscript style, a stone between two boulders serves as a crude war table, on it a crude clay map, David leans in with three captains pointing, skin scrolls lean against the rocks, punchy ink strokes minimal color, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 15 | `box-art-hunter-hunted` | `game box art, painting in illuminated manuscript style, three-panel manuscript-page layout left panel shows David and a scout hidden behind rock watching center panel shows Saul's army marching unaware right panel shows a narrow path where David's band will ambush, used as if this were a medieval chronicle page, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 16 | `box-art-dry-place` | `game box art, painting in illuminated manuscript style, wide desert vista under a single palm, a tiny figure David sits beneath it sling at his side a single waterskin beside him, scale emphasizes solitude, horizon line is low, ochre umber and a single green palm frond, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 17 | `box-art-covenant-at-the-cave` | `game box art, painting in illuminated manuscript style, David's hand reaches toward Jonathan's within a shadowed cave interior, both wear simple cloaks, a single lit torch between them casts their faces gold, composition is tight and emotional friendship sworn in dangerous times, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 18 | `box-art-river-crossing` | `game box art, painting in illuminated manuscript style, figures fording a shallow stony river at dawn, an ox and a donkey precede a woman with a child, warriors lead the way and guard the rear, mist rises from the water, the scene is pastoral but tense everyone is fleeing, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded indigo, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 19 | `box-art-watchfire` | `game box art, painting in illuminated manuscript style, night camp on a ridge above a valley, a single watchfire burns, figures sleep wrapped in cloaks around it, one sentry stands at the edge of the light looking out, the sky is ink-black with a few stars, simple quiet tense, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded indigo, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 20 | `box-art-philistine-lord` | `game box art, painting in illuminated manuscript style, Achish seated on a folding stool in a field tent flanked by two spearmen, he holds a goblet expression unreadable, David stands before him stripped of his armor bowing slightly a fugitive at the mercy of a foreign lord, warm lamplight, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 21 | `box-art-surprise-attack` | `game box art, painting in illuminated manuscript style, dynamic motion composition three Israelite warriors burst through a low brush line at the edge of a camp weapons raised, the enemy camp sprawls behind them figures still sleeping, dust and motion, perspective is from the enemy camp looking toward the attackers, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 22 | `box-art-shepherds-flute` | `game box art, painting in illuminated manuscript style, David seated on a rocky outcrop at sunset resting between journeys, a simple shepherd's pipe is in his hand not a weapon, below a small flock of goats grazes, the image is serene almost pastoral, the tension is in the viewer knowing this peace will end, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 23 | `box-art-wounded-bear` | `game box art, painting in illuminated manuscript style, close-up of a hand gripping a spear shaft thrust into fur, a wounded bear rears, David's boot and the lower half of his tunic are visible, blood is implied through a single stroke of faded crimson, mythic and primal grounded in the historical David legend, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 24 | `box-art-desert-mirage` | `game box art, painting in illuminated manuscript style, single figure walking in shimmering heat across white desert ground, the horizon dissolves into heat haze, on the ground faint reflections show the faces of his men back at camp, surreal but controlled the disorientation of the fugitive, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 25 | `box-art-the-board-at-rest` | `game box art, painting in illuminated manuscript style, the actual game board the 8x8 hex grid rendered as aged parchment sits on a wooden table, two empty command card slots face a single commander token, a bronze sword rests diagonally across the corner of the board, everything still, the viewer is invited to sit down and play, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 26 | `box-art-david-fleeing-naioth` | `game box art, painting in illuminated manuscript style, David running through a dark stone corridor at Naioth, Samuel's hand raised behind him in benediction, torchlight flickering on rough walls, Saul's soldiers visible at the far end hesitating, composition is vertical and tense, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 27 | `box-art-covenant-at-mizpah` | `game box art, painting in illuminated manuscript style, Jonathan and David standing on a hilltop at Mizpah, a young lamb between them as a witness, both holding the shaft of a single spear pointing toward the ground, wind blowing their cloaks apart, golden light breaking through clouds behind them, composition is solemn and emotional, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 28 | `box-art-the-showbread-at-nob` | `game box art, painting in illuminated manuscript style, interior of a humble sanctuary at Nob, a priest in simple linen robes places bread on a golden table, David standing nearby with a sword at his hip, stone walls and hanging curtains, lamplight, composition is reverent and quiet, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 29 | `box-art-saul-at-the-javelin` | `game box art, painting in illuminated manuscript style, Saul seated on a high bench in his palace, a javelin in his right hand poised to throw at David who stands near the wall with a harp in hand, court attendants frozen in the background, dramatic tension in the still moment before violence, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 30 | `box-art-david-in-the-wilderness-of-ziph` | `game box art, painting in illuminated manuscript style, David and a small band crouched in a dark cave opening overlooking the wilderness of Ziph, Saul's army visible as a dust trail far below on the plateau, heat haze rising, composition is wide and claustrophobic, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 31 | `box-art-abigail-intervenes` | `game box art, painting in illuminated manuscript style, Abigail kneeling in the dust before David, a servant leading a laden donkey behind her, David's men standing with weapons raised in the background, her face lifted in supplication, his face softening, composition is low and dramatic, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 32 | `box-art-nabal-s-whetting` | `game box art, painting in illuminated manuscript style, Nabal at his rich table in Carmel, feasting with his sons, golden cups and roasted meat, a servant standing at the edge of the scene looking shocked, outside the window Abigail leads donkeys laden with gifts, contrast between opulence and the dust road beyond, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 33 | `box-art-david-among-the-philistines` | `game box art, painting in illuminated manuscript style, David standing in a Philistine camp at Ziklag, wearing Philistine-style dress, Achish pointing toward the battlefield in the distance, Israelite warriors looking on with mixed expressions, the moment of uneasy alliance, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded indigo, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 34 | `box-art-ziklag-burned` | `game box art, painting in illuminated manuscript style, the settlement of Ziklag smoldering at dawn, walls collapsed, smoke rising, David's warriors fall to their knees weeping, the Amalekite raiders visible as tiny dust specks on the horizon fleeing with captives, composition is low and crushing, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 35 | `box-art-the-egyptian-slave` | `game box art, painting in illuminated manuscript style, a wounded Egyptian slave sitting under a desert shrub, David kneeling beside him offering bread and water, the slave's face gaunt with exhaustion, a vast empty desert stretching behind them, composition is intimate and compassionate, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 36 | `box-art-the-pursuit-of-the-amalekites` | `game box art, painting in illuminated manuscript style, David's band riding hard across a dusty plain, a slave leading an Egyptian on a donkey ahead, an Amalekite camp visible in the distance spilling over a rocky ridge, composition is motion and dust, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 37 | `box-art-david-spares-saul-in-the-cave` | `game box art, painting in illuminated manuscript style, inside a dark cave at Ein Gedi, David crouching near Saul who is entering unaware, Saul's robe spread wide at the cave entrance, David's hand hovering near the hem, torchlight flickering, composition is tight and tense, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 38 | `box-art-saul-and-jonathan-slain` | `game box art, painting in illuminated manuscript style, on the heights of Gilboa, Saul leaning on his own sword and falling, Jonathan fallen across him, armor scattered, Philistine chariots visible in the valley, a single Israelite bow abandoned in the foreground, composition is tragic and still, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 39 | `box-art-the-amalekite-messenger` | `game box art, painting in illuminated manuscript style, an Amalekite runner stumbling into David's camp at Ziklag, clothes torn and dusty, holding up a crown and armlet, David's men drawing weapons to kill him, David's hand raised in horror and disbelief, composition is dramatic and tense, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 40 | `box-art-david-s-lament` | `game box art, painting in illuminated manuscript style, David seated on a rocky ledge, harp in hand but head bowed, ink and tears on parchment, the words "the beauty of Israel is slain upon thy high places" faintly visible as if written across the sky, no other figures, composition is grief, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 41 | `box-art-david-anointed-king-of-judah` | `game box art, painting in illuminated manuscript style, the elders of Israel standing in a circle around David at Hebron, a horn of oil in the hands of the high priest, olive trees and stone walls of Hebron in the background, golden autumn light, composition is coronation but simple, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 42 | `box-art-the-battle-at-gibeon` | `game box art, painting in illuminated manuscript style, two armies arrayed at the pool of Gibeon, Israelite spearmen on one side, Joab and Abner watching from opposite hills, Asahel running toward Abner with spear raised, dust and crowd, composition is tactical and tense, hand-painted historical illustration, aged parchment background, ink outlines with muted watercolor wash in ochre umber and faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 43 | `box-art-asahel-chases-abner` | `game box art, painting in illuminated manuscript style, Asahel running with incredible speed across open ground toward Abner who rides a horse backward, Abner turning with spear butt raised, other warriors frozen in shock on both sides, motion lines and dust, composition is the moment before death, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 44 | `box-art-david-mourns-abner` | `game box art, painting in illuminated manuscript style, David walking behind Abner's coffin at the gate of Hebron, weeping openly, his captains walking beside him with bowed heads, the people watching from the walls, a single torch casting long shadows, composition is public grief and dignity, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded indigo, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 45 | `box-art-ish-bosheth-assassinated` | `game box art, painting in illuminated manuscript style, two captains Baanah and Rechab entering Ishbosheth's bedroom at noon, daylight streaming through the window, Ishbosheth lying on his bed, the murderers lowering a spear, composition is calculated and cold, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded crimson, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 46 | `box-art-david-returns-the-ark` | `game box art, painting in illuminated manuscript style, the Ark of the Covenant carried on a new cart by oxen, David dancing before it in a linen ephod, the people of Israel cheering with trumpets, Jerusalem's walls visible in the background, celebration and worship, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 47 | `box-art-the-well-of-bethlehem` | `game box art, painting in illuminated manuscript style, three mighty men breaking through the Philistine line to reach the well by the gate of Bethlehem, water pouring into a cup, David looking on with gratitude and awe, the gate in the background with Philistine banners, composition is heroism and fellowship, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 48 | `box-art-david-counting-israel` | `game box art, painting in illuminated manuscript style, David standing on a raised platform with a scroll in hand, census counters moving through the camp below, a prophet in rough garments standing before him pointing heavenward in rebuke, dark clouds gathering, composition is judgment and regret, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded indigo, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 49 | `box-art-the-threshing-floor-of-araunah` | `game box art, painting in illuminated manuscript style, an angel of the Lord standing with a drawn sword on a threshing floor outside Jerusalem, David looking up from his knees in supplication, Araunah the Jebusite offering his threshing floor and oxen, smoke rising from a sacrifice already burning, composition is atonement and mercy, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 50 | `box-art-david-s-mighty-men-at-the-cave` | `game box art, painting in illuminated manuscript style, the Three Mighty Men standing in a cave mouth at Adullam, water dripping from the ceiling, their faces weathered and devoted, David looking at them with deep affection, weapons stacked against the wall, composition is loyalty and brotherhood, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |

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
| 7 | Formation Cards (MVP factions) | 57 | 8 | 456 |
| **Total** | | **95** | | **630 images** |

Estimated time: **~10–15 minutes total** on GTX 1060 with DreamShaper XL Lightning.

---
---

## Post-MVP Command Card Art

| Asset | Prompt |
|---|---|
| **Jonathan Precision** | `ONE PERSON ONLY, scene in illuminated manuscript style, Jonathan son of Saul drawing his composite bow, arrow aimed, two Israelite archers beside him, aged parchment background, ink outlines with muted watercolor wash in ochre and faded gold, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Joab Assault** | `ONE PERSON ONLY, scene in illuminated manuscript style, Joab son of Zeruiah leading a fierce charge, bronze spear raised, Israelite warriors behind him, aged parchment background, ink outlines with muted watercolor wash in ochre and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Amasa Rally** | `ONE PERSON ONLY, scene in illuminated manuscript style, Amasa son of Jether rallying troops with hand raised, bronze spear in other hand, soldiers gathering around, aged parchment background, ink outlines with muted watercolor wash in ochre and amber, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Asahel Flank** | `ONE PERSON ONLY, scene in illuminated manuscript style, Asahel son of Zeruiah running with incredible speed, short sword raised, dust rising at his feet, single runner outrunning formation, aged parchment background, ink outlines with muted watercolor wash in umber and faded gold, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Philistine Charge** | `ONE PERSON ONLY, scene in illuminated manuscript style, Philistine heavy infantry advancing in formation, large shields locked, spears angled forward, dust and determination, aged parchment background, ink outlines with muted watercolor wash in umber ochre and faded indigo, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Goliath Challenge** | `ONE PERSON ONLY, scene in illuminated manuscript style, Goliath the Gittite standing immense with spear like a weaver's beam, small figure of David opposite him, bronze shields, dust rising, aged parchment background, ink outlines with muted watercolor wash in umber and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Amalekite Raid** | `ONE PERSON ONLY, scene in illuminated manuscript style, Amalekite raiders on camel and foot sweeping through a settlement, spears raised, dust clouds, civilians fleeing, aged parchment background, ink outlines with muted watercolor wash in ochre umber and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |

---

## Formation Card Art (768×512, ink & parchment)

> **Batch 7 — MVP factions only:** David's Company, Saul's Kingdom, Jonathan's Followers, Amalekites.
> Each prompt is for the TOP action of the formation card. Bottom action shares the same card art.
> 57 formation cards × 8 samples = **456 images**.
> **Do NOT prefix with "ONE PERSON ONLY"** — these are tactical scenes with multiple figures.

| Card | Prompt |
|---|---|
| **Spear Wall** | `scene in illuminated manuscript style, bronze age Levantine Israelite spearmen in tight phalanx formation, long wooden spears with bronze tips angled outward, shields locked, first enemy advancing into spears, linen tunics and leather armor, determined expressions, aged parchment background, ink outlines with muted watercolor wash in umber and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Hold Line** | `scene in illuminated manuscript style, bronze age Levantine Israelite spearmen holding defensive line, shields locked, spears braced, taking impact from enemy attack, linen tunics visible beneath leather armor, grim determined expressions, aged parchment background, ink outlines with muted watercolor wash in umber and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Aggressive Push** | `scene in illuminated manuscript style, bronze age Levantine Israelite swordsmen pushing forward in aggressive advance, bronze short swords raised, dust at their heels, breaking through enemy line, linen tunics and leather vests, determined expressions, aged parchment background, ink outlines with muted watercolor wash in ochre and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Locked Shields** | `scene in illuminated manuscript style, bronze age Levantine Israelite swordsmen with shields locked in tight defensive cluster, overlapping hide shields, spears and swords ready, grim defensive stance, linen tunics and leather armor, standing shoulder to shoulder, aged parchment background, ink outlines with muted watercolor wash in ochre and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Focused Volley** | `scene in illuminated manuscript style, bronze age Levantine Israelite archers focusing volley on single enemy target, composite bows drawn and aimed, arrows pointed at same target, concentrated fire, linen tunics and leather vests, focused expressions, aged parchment background, ink outlines with muted watercolor wash in umber and faded gold, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Suppressing Fire** | `scene in illuminated manuscript style, bronze age Levantine Israelite archers laying down suppressing fire into enemy zone, arrows arcing through air, enemy unit pinned behind cover, dust and tension, linen tunics, alert focused expressions, aged parchment background, ink outlines with muted watercolor wash in umber and faded gold, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Skirmish Tactics** | `scene in illuminated manuscript style, bronze age Levantine Israelite slingers in hit-and-run skirmish, leather slings in motion, stones flying, light mobile stances, dust swirling around feet, linen tunics and leather vests, alert expressions, aged parchment background, ink outlines with muted watercolor wash in ochre and umber, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Stone Barrage** | `scene in illuminated manuscript style, bronze age Levantine Israelite slingers unleashing stone barrage on advancing enemy, slings in motion, stones arcing toward target, enemy recoiling from impact, linen tunics, alert predatory expressions, aged parchment background, ink outlines with muted watercolor wash in ochre and umber, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Ambush Position** | `scene in illuminated manuscript style, bronze age Levantine Israelite scout in ambush position, short spear ready, crouched behind rock, enemy unit unaware approaching, tense predatory expression, linen tunic and leather vest, dusty terrain, aged parchment background, ink outlines with muted watercolor wash in umber and faded gold, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Reconnaissance** | `scene in illuminated manuscript style, bronze age Levantine Israelite scout observing enemy from hidden position, short spear and small shield, keen eyes scanning enemy camp, linen tunic and worn cloak, alert intelligent expression, rocky hillside vantage point, aged parchment background, ink outlines with muted watercolor wash in umber and faded gold, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Davids Champions** | `scene in illuminated manuscript style, David's Mighty Men champions breaking through enemy line, bronze short swords raised, elite warriors in action, heavy cloaks flowing, linen tunics and leather armor, fierce determined expressions, aged parchment background, ink outlines with muted watercolor wash in ochre and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Stand Together** | `scene in illuminated manuscript style, David's Mighty Men standing together protecting weaker unit, shield wall formation, elite warriors absorbing blow for ally, bronze short swords ready, heavy cloaks, linen tunics and leather armor, protective grim expressions, aged parchment background, ink outlines with muted watercolor wash in ochre and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Leadership** | `scene in illuminated manuscript style, young David commander rallying troops, bronze short sword raised, inspiring nearby warriors, brown wool cloak pinned with bronze brooch, determined watchful expression, rocky Judean hillside, Mediterranean complexion, aged parchment background, ink outlines with muted watercolor wash in ochre and faded gold, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Rally** | `scene in illuminated manuscript style, David moving rapidly across battlefield to rally dormant unit, bronze short sword in hand, shepherd's staff, brown cloak flowing, dynamic movement pose, determined expression, rocky terrain with scattered warriors, aged parchment background, ink outlines with muted watercolor wash in ochre and faded gold, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Aid** | `scene in illuminated manuscript style, David's Company refugees tending to wounded warrior, simple linen tunics, gentle careful movements, bandages and basic healing, concerned compassionate expressions, camp setting with tents, aged parchment background, ink outlines with muted watercolor wash in ochre and umber, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Evacuate** | `scene in illuminated manuscript style, David's Company refugees being escorted to safety away from battle, simple linen tunics, moving quickly with guide, dust and distant fighting, concerned but determined expressions, rocky path, aged parchment background, ink outlines with muted watercolor wash in ochre and umber, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Desperate Charge** | `scene in illuminated manuscript style, David's Company outcasts launching desperate charge, bronze short swords raised, reckless fury in their eyes, dust and chaos, worn leather armor over linen tunics, fierce desperate expressions, aged parchment background, ink outlines with muted watercolor wash in ochre and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Outcast Fall Back** | `scene in illuminated manuscript style, David's Company outcasts falling back from ranged fire, shields raised, leather armor visible, moving quickly to safety, weariness and determination, dusty terrain, aged parchment background, ink outlines with muted watercolor wash in ochre and umber, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Veteran Assault** | `scene in illuminated manuscript style, David's Company veteran warriors in devastating assault, bronze short swords raised, chain killing enemy, elite disciplined formation, heavy leather armor with bronze elements, grim efficient expressions, aged parchment background, ink outlines with muted watercolor wash in ochre and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Battle Hardened** | `scene in illuminated manuscript style, David's Company veterans holding defensive line, shields locked, heavy armor gleaming, unbroken by enemy assault, bronze short swords ready, grim immovable expressions, aged parchment background, ink outlines with muted watercolor wash in umber and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Kings Division** | `scene in illuminated manuscript style, Saul's Kingdom army within Abner's command aura, disciplined infantry formation, shields locked, spears angled, professionalism and order, iron armor gleaming, grim disciplined expressions, aged parchment background, ink outlines with muted watercolor wash in umber and faded indigo, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Relentless Advance** | `scene in illuminated manuscript style, Saul's Kingdom heavy infantry pushing forward in relentless advance, shields locked, spears angled, dust at their heels, iron armor, disciplined determined expressions, aged parchment background, ink outlines with muted watercolor wash in umber and faded indigo, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Battle Line** | `scene in illuminated manuscript style, Saul's Kingdom army holding solid battle line, overlapping shields, spears and javelins ready, layered defense, iron and leather armor, grim professional expressions, aged parchment background, ink outlines with muted watercolor wash in umber and faded indigo, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Abner Command** | `scene in illuminated manuscript style, Abner commander issuing orders to Saul's Kingdom units, arm raised in command, nearby units activating, iron armor, leather cloak, authoritative expression, aged parchment background, ink outlines with muted watercolor wash in umber and faded indigo, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Abner Battle Cry** | `scene in illuminated manuscript style, Abner leading battle cry, sword raised, nearby Saul's Kingdom warriors boosted with attack bonus, iron armor gleaming, fierce determined expression, aged parchment background, ink outlines with muted watercolor wash in ochre and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Ancient Shield** | `scene in illuminated manuscript style, Saul's Royal Guard taking melee hit with iron shield phalanx, shields locked, iron armor gleaming, attacker's weapon bouncing off, retaliation in their eyes, heavy iron armor, disciplined expressions, aged parchment background, ink outlines with muted watercolor wash in umber and faded indigo, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Iron Wall** | `scene in illuminated manuscript style, two Saul's Royal Guards forming iron wall together, shields overlapping, unbreakable defensive position, iron armor gleaming, immovable stance, linen tunics visible beneath armor, grim expressions, aged parchment background, ink outlines with muted watercolor wash in umber and faded indigo, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Tribe Charge** | `scene in illuminated manuscript style, Benjamite spearmen of Benjamin tribe charging into enemy infantry, long spears angled forward, tribal fury in their eyes, dust and motion, leather armor with bronze elements, fierce expressions, aged parchment background, ink outlines with muted watercolor wash in ochre and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Hold Ranks** | `scene in illuminated manuscript style, Benjamite spearmen holding ranks in defensive formation, spears angled outward, adjacent infantry gaining protection, tight disciplined line, leather armor and shields, grim determined expressions, aged parchment background, ink outlines with muted watercolor wash in umber and faded indigo, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Ranged Barrage** | `scene in illuminated manuscript style, Israelite archers firing concentrated volley at single enemy target, composite bows drawn and aimed, coordinated fire, arrows flying toward target, linen tunics and leather vests, focused expressions, aged parchment background, ink outlines with muted watercolor wash in umber and faded gold, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Skirmish Line** | `scene in illuminated manuscript style, Israelite archers repositioning in skirmish line, moving quickly away from melee threat, bows still ready, light mobile stances, linen tunics and leather vests, alert expressions, aged parchment background, ink outlines with muted watercolor wash in umber and faded gold, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Officer Buff** | `scene in illuminated manuscript style, Saul's Kingdom officer enhancing allied unit with command, hand on warrior's shoulder, aura of +2 attack and +1 defense, leather armor and cloak, authoritative encouraging expression, aged parchment background, ink outlines with muted watercolor wash in ochre and faded gold, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Officer Reorganize** | `scene in illuminated manuscript style, Saul's Kingdom officer rallying dormant unit to immediate action, arm raised in command, nearby warriors springing to life, leather armor and cloak, energetic leadership expression, aged parchment background, ink outlines with muted watercolor wash in ochre and faded gold, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Bodyguard Protect** | `scene in illuminated manuscript style, Saul's Elite Bodyguard moving to shield commander, standing between commander and threat, iron armor gleaming, defensive stance, leather cloak, vigilant protective expression, aged parchment background, ink outlines with muted watercolor wash in umber and faded indigo, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Bodyguard Intercept** | `scene in illuminated manuscript style, Saul's Elite Bodyguard sacrificing himself to intercept blow aimed at commander, taking damage to protect commander, iron armor, dramatic sacrifice, grim determined expression, aged parchment background, ink outlines with muted watercolor wash in umber and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Loyal Bond** | `scene in illuminated manuscript style, Jonathan's Followers units in tight loyal bond formation, small army punching above weight, shields overlapping, spears and bows ready, mutual protection and +1 attack glow, linen tunics and leather armor, fanatically loyal expressions, aged parchment background, ink outlines with muted watercolor wash in ochre and faded gold, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Swift Retreat** | `scene in illuminated manuscript style, Jonathan's Followers units making swift tactical retreat, moving quickly away from overwhelming force, shields raised against melee, disciplined withdrawal, linen tunics and leather armor, alert disciplined expressions, aged parchment background, ink outlines with muted watercolor wash in umber and faded gold, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Faithful Stand** | `scene in illuminated manuscript style, Jonathan's Followers sharing damage in faithful stand formation, adjacent warriors absorbing blow for wounded comrade, shields locked, grim sacrifice, linen tunics and leather armor, loyal determined expressions, aged parchment background, ink outlines with muted watercolor wash in ochre and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Loyal Charge** | `scene in illuminated manuscript style, Jonathan's Loyal Guards launching fanatical charge, shields raised, spears angled forward, momentum building from first kill, leather armor gleaming, fanatical fierce expressions, aged parchment background, ink outlines with muted watercolor wash in ochre and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Guard Wall** | `scene in illuminated manuscript style, Jonathan's Loyal Guards forming guard wall, shields locked, defensive anchor protecting entire formation, leather armor, protective stance, grim loyal expressions, aged parchment background, ink outlines with muted watercolor wash in umber and faded gold, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Sniper Volley** | `scene in illuminated manuscript style, Jonathan's Elite Archers eliminating highest threat with precise volley, composite bows drawn and aimed at dangerous enemy unit, concentrated精准 fire, linen tunics and leather vests, focused expressions, aged parchment background, ink outlines with muted watercolor wash in umber and faded gold, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Covered Retreat** | `scene in illuminated manuscript style, Jonathan's Elite Archers retreating under covered fire, shields raised, moving away from melee threat, composite bows still ready, light mobile stances, linen tunics and leather vests, alert expressions, aged parchment background, ink outlines with muted watercolor wash in umber and faded gold, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Jonathan Ambush** | `scene in illuminated manuscript style, Jonathan's Followers scout launching devastating ambush, short spear raised, striking before enemy can react, 2 damage impact, crouched predator pose, linen tunic and leather vest, keen alert expression, rocky terrain with approaching enemy, aged parchment background, ink outlines with muted watercolor wash in umber and faded gold, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Jonathan Recon** | `scene in illuminated manuscript style, Jonathan's Followers scout gathering intelligence on enemy unit, short spear and small shield, keen eyes observing, revealing enemy stats to allies, linen tunic and worn cloak, alert intelligent expression, vantage point overlooking enemy camp, aged parchment background, ink outlines with muted watercolor wash in umber and faded gold, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Desert Raid** | `scene in illuminated manuscript style, Amalekite unit striking deep behind enemy lines, fast desert raiders on horseback, dromedary camels in background, surprise attack from desert, dusty red-brown cloaks, bronze weapons, fierce expressions, aged parchment background, ink outlines with muted watercolor wash in ochre and umber, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Steppes Flank** | `scene in illuminated manuscript style, Amalekite raiders using superior desert mobility to outflank enemy, fast donkeys and horses, ignoring terrain, dust and speed, dusty red-brown cloaks, bronze weapons, alert expressions, desert terrain with rocky outcrops, aged parchment background, ink outlines with muted watercolor wash in ochre and umber, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Harassment Campaign** | `scene in illuminated manuscript style, Amalekite forces concentrating harassment on single enemy target, multiple slingers and skirmishers focusing fire, coordinated attack on weakened unit, dusty red-brown cloaks, bronze weapons, focused expressions, aged parchment background, ink outlines with muted watercolor wash in ochre and umber, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Raid Command** | `scene in illuminated manuscript style, Amalekite chieftain leading raid from front, dark red-brown wool cloak, leather and bronze chest piece, bronze short sword raised, striking hard and repositioning, authoritative weathered face, rocky outcrop, aged parchment background, ink outlines with muted watercolor wash in ochre and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Desert Ambush** | `scene in illuminated manuscript style, Amalekite chieftain disrupting enemy formation at melee range, pushing enemy unit back with spear thrust, dark red-brown cloak, bronze spear, dust and chaos, weathered stern expression, aged parchment background, ink outlines with muted watercolor wash in ochre and umber, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Raid Charge** | `scene in illuminated manuscript style, Amalekite raiders charging into battle, bronze-tipped spears raised, fast infantry advance, dusty red-brown cloaks, dust at their heels, fierce expressions, aged parchment background, ink outlines with muted watercolor wash in ochre and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Scatter** | `scene in illuminated manuscript style, Amalekite raiders scattering across desert, fast melee units dispersing to avoid pinning, dust clouds, still vulnerable to ranged fire, dusty red-brown cloaks, alert expressions, desert terrain, aged parchment background, ink outlines with muted watercolor wash in ochre and umber, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Desert Storm** | `scene in illuminated manuscript style, Amalekite slingers unleashing concentrated storm of stones, multiple slingers in coordinated fire, stones arcing toward single target, dusty red-brown cloaks, leather slings in motion, focused expressions, aged parchment background, ink outlines with muted watercolor wash in ochre and umber, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine warfare` |
| **Stone Galop** | `scene in illuminated manuscript style, Amalekite slingers on the move, throwing stones while repositioning, fast mobile skirmishers, leather slings in motion, dust swirling, dusty red-brown cloaks, alert predatory expressions, aged parchment background, ink outlines with muted watercolor wash in ochre and umber, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Desert Flank** | `scene in illuminated manuscript style, Amalekite desert scout launching devastating flank ambush, short javelin raised, striking before enemy initiative, dust and surprise, dusty patched cloak, lean wind-hardened build, keen predatory expression, desert ridge, aged parchment background, ink outlines with muted watercolor wash in umber and faded gold, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Eyes Target** | `scene in illuminated manuscript style, Amalekite desert scout observing enemy unit to gather intelligence, short javelin and small shield, keen eyes scanning, revealing enemy capabilities to allies, dusty patched cloak, alert intelligent expression, rocky desert vantage point, aged parchment background, ink outlines with muted watercolor wash in umber and faded gold, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Desert Raider Charge** | `scene in illuminated manuscript style, Amalekite desert raider on fast desert mount launching devastating deep strike, bronze-tipped spear raised, ignoring desert terrain, speed and power, dusty red-brown cloak flowing, weathered stern expression, open desert plain with distant mountains, aged parchment background, ink outlines with muted watercolor wash in ochre and faded crimson, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Desert Dash** | `scene in illuminated manuscript style, Amalekite desert raider dashing across battlefield, fast mount carving path through enemy lines, all nearby enemies suffering damage, dusty red-brown cloak, leather reins, focused expression, desert terrain with scattered enemies, aged parchment background, ink outlines with muted watercolor wash in ochre and umber, hand-painted historical illustration, board game card art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |

---

## Post-MVP Portrait Prompts

### Additional Commanders & Allies

| Asset | Prompt |
|---|---|
| **Benjamin Spearman** | `ONE PERSON ONLY, solo portrait, waist-up, Benjamite spearman of Jonathan's guard, bronze age Levantine elite infantry, strong fierce build, dark hair, white linen tunic with leather shoulder guards, brown cloak wrapped and fastened, long wooden spear with bronze tip held upright, small hide shield at side, leather cord belt with knife, alert loyal expression, standing in disciplined formation, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Judah Militia** | `ONE PERSON ONLY, solo portrait, waist-up, Judah militia defender, bronze age Levantine village warrior, sturdy build, dark hair, simple linen tunic with leather vest, brown wool cloak, bronze short sword in hand, small round hide shield, leather sandals, determined local expression, leaning on spear in resting pose, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Abigail** | `ONE PERSON ONLY, solo portrait, waist-up, Abigail wife of Nabal, bronze age Levantine noblewoman, dark hair in woven braids, rich but practical woolen tunic in faded blue, leather belt, small knife at waist, face showing intelligence and caution, standing with a loaded donkey behind her, laden with gifts, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Nabal** | `ONE PERSON ONLY, solo portrait, waist-up, Nabal the Carmelite, bronze age Levantine wealthy landowner, heavyset build, dark hair and short beard, rich woolen tunic with woven border, bronze rings on fingers, bronze short sword at hip, expression of stubborn pride, seated on a low stool with a wine cup in hand, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| **Priest of Nob** | `ONE PERSON ONLY, solo portrait, waist-up, priest of Nob, bronze age Levantine priest, older man, white linen ephod over simple tunic, bronze plate on chest with Urim and Thummim, short beard, kind eyes, holding a loaf of showbread, standing before a stone altar, Mediterranean complexion, hand-painted historical illustration, watercolor and ink on aged parchment, board game card art, centered composition, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |

---

## Additional Box Art Concepts — Round 3

| # | Concept Key | Prompt |
|---|---|---|
| 51 | `box-art-david-at-adullam` | `game box art, painting in illuminated manuscript style, David seated at the entrance of a cave at Adullam, surrounded by a ragtag band of outcasts and warriors, one man sharpening a spear, another mending a cloak, warm firelight against dark rock, composition is intimate and raw, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 52 | `box-art-jonathan-and-david` | `game box art, painting in illuminated manuscript style, Jonathan and David standing on a hilltop at Mizpah, Jonathan taking off his robe and giving it to David along with his weapons, wind blowing the fabric between them, golden light, composition is tender and covenant-making, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 53 | `box-art-the-wounded-david` | `game box art, painting in illuminated manuscript style, David lying wounded and exhausted on a rocky hillside, his armor scattered, a single warrior kneeling beside him offering water, dark storm clouds above, composition is vulnerability and trust, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded indigo, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 54 | `box-art-the-cave-of-engedi` | `game box art, painting in illuminated manuscript style, inside the dark cave at Ein Gedi, David standing in the shadows near Saul who is sleeping, Saul's robe spread wide at the entrance, David's hand hovering near the hem deciding whether to strike, torchlight flickering, composition is the moment of mercy, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones umber ochre faded gold, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |
| 55 | `box-art-david-as-king` | `game box art, painting in illuminated manuscript style, David crowned at Hebron, elder standing before him with a horn of oil, olive trees and stone walls in background, autumn golden light, his captains behind him, composition is kingship earned through hardship, hand-painted historical illustration, aged parchment background with ink outlines, muted earth tones ochre umber amber, board game cover art, family friendly, NOT medieval, NOT fantasy, NOT European, historically accurate bronze age Levantine` |

---

## Additional Tile Textures

| Asset | Prompt |
|---|---|
| **Desert night tile** | `top-down flat hex tile, desert at night, cool blue-gray under moonlight, subtle stars, watercolor wash, board game style, seamless, 512x512` |
| **Stone path tile** | `top-down flat hex tile, ancient stone path and packed earth, gray-brown, ink wash texture, board game style, seamless, 512x512` |
| **Ruins tile** | `top-down flat hex tile, broken stone walls and rubble, weathered umber, watercolor and ink wash, board game style, seamless, 512x512` |

---

## Additional UI Elements

| Asset | Prompt |
|---|---|
| **Portrait frame** | `ornate rectangular frame for character portrait, aged parchment with dark ink border, corner ornaments, board game UI element, hand-painted illustration, transparent background, NOT medieval, NOT fantasy, NOT European` |
| **Card slot** | `empty card slot on table, aged parchment background, wooden card border, board game UI element, transparent background, hand-painted illustration, NOT medieval, NOT fantasy, NOT European` |
| **Commander aura** | `soft glowing circle on ground, commander presence area, warm golden light, board game UI element, transparent background, hand-painted illustration, NOT medieval, NOT fantasy, NOT European` |

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

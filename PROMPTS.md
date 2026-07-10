# Asset Generation Prompts — SDXL Turbo

> Generate art on your iPhone 16e using SDXL Turbo. All prompts designed for 512×512 output, transparent backgrounds where noted.

---

## Hex Tile Textures (512×512, tileable)

| Asset | Prompt |
|---|---|
| **Sand tile** | `top-down flat hex tile, sandy desert terrain, warm beige color, subtle grain texture, board game style, flat shaded, game asset, seamless, 512x512` |
| **Rock tile** | `top-down flat hex tile, rocky gravel terrain, gray-brown color, small stones visible, board game style, flat shaded, game asset, seamless, 512x512` |
| **Grass tile** | `top-down flat hex tile, dry savanna grass, warm green-brown, short grass texture, board game style, flat shaded, game asset, seamless, 512x512` |

---

## Unit Token Textures (256×256 or 512×512, transparent background)

### Player Units (Blue/Teal)

| Unit | Prompt |
|---|---|
| **David** | `small 3D character token, ancient Israelite commander, blue cloak, bronze helmet, holding sword, board game miniature style, isometric view, flat shaded, game asset, transparent background` |
| **Swordsman** | `small 3D character token, ancient Israelite soldier, blue tunic, round shield, bronze sword, board game miniature, isometric, flat shaded, transparent background` |
| **Spearman** | `small 3D character token, ancient Israelite spearman, blue tunic, long spear, board game miniature, isometric, flat shaded, transparent background` |
| **Slinger** | `small 3D character token, ancient slinger, blue tunic, crouching, holding sling, board game miniature, isometric, flat shaded, transparent background` |
| **Archer** | `small 3D character token, ancient archer, blue tunic, bow and arrow, board game miniature, isometric, flat shaded, transparent background` |
| **Scout** | `small 3D character token, ancient scout, blue tunic, slim build, javelin, board game miniature, isometric, flat shaded, transparent background` |

### Enemy Units (Red/Brown — Amalekites)

| Unit | Prompt |
|---|---|
| **Raider** | `small 3D character token, ancient nomadic raider, red-brown cloak, spear, desert warrior, board game miniature, isometric, flat shaded, transparent background` |
| **Slinger** | `small 3D character token, ancient nomadic slinger, red-brown cloak, crouching, board game miniature, isometric, flat shaded, transparent background` |
| **Archer** | `small 3D character token, ancient mounted archer, red-brown cloak, on horse, bow, board game miniature, isometric, flat shaded, transparent background` |
| **Scout** | `small 3D character token, ancient nomadic scout, red-brown cloak, slim, javelin, board game miniature, isometric, flat shaded, transparent background` |
| **Camel Rider** | `small 3D character token, ancient camel rider, red-brown cloak, riding camel, spear, board game miniature, isometric, flat shaded, transparent background` |
| **Chieftain** | `small 3D character token, ancient nomadic chieftain, red-brown cloak, tall headdress, commanding pose, board game miniature, isometric, flat shaded, transparent background` |

---

## UI Elements (transparent background)

| Asset | Prompt |
|---|---|
| **End Turn button** | `rounded rectangle button, blue color, game UI, flat design, 200x60, transparent background` |
| **Overwork button** | `rounded rectangle button, orange color, game UI, flat design, 200x60, transparent background` |
| **HP bar background** | `thin horizontal bar, dark gray, game UI, flat design, 100x10, transparent background` |
| **HP bar fill** | `thin horizontal bar, bright green, game UI, flat design, 100x10, transparent background` |
| **Action icon** | `simple boot icon, white on transparent, game UI icon, flat design, 32x32` |
| **Sword icon** | `simple sword icon, white on transparent, game UI icon, flat design, 32x32` |
| **Reward background** | `dark semi-transparent panel, rounded corners, game UI, 400x300, transparent background` |

---

## Tips

1. **Use the same seed** for all prompts in a batch to keep style consistent
2. **Negative prompt:** add `--no text, no watermark, no signature, no letters, no words`
3. **Generate in waves:** all hex tiles first, then all player units, then all enemies
4. **Keep a prompt log** so you can regenerate if needed
5. **Output naming convention:** `hex_sand.png`, `unit_david.png`, `unit_swordsman.png`, `ui_endturn.png`, etc.

---

## Commercial Use

- **SDXL Turbo** is licensed under CreativeML Open RAIL-M — generated outputs are yours to use commercially

# WorldPainter Import Guide: Ashenfall Continent of Vantyra
### *How to Import the Master 16-Bit Heightmap into WorldPainter*

---

## 🗺️ Master Deliverables
* **16-Bit Grayscale Heightmap:** `ASHENFALL_HEIGHTMAP_16BIT.png` (4096 x 4096, 16-bit uint16)
* **Satellite Visual Reference:** `ASHENFALL_TOPOGRAPHIC_RENDER.png`
* **Preview Heightmap:** `ASHENFALL_HEIGHTMAP_PREVIEW.png`

---

## 🛠️ Step-by-Step WorldPainter Import Instructions

1. **Launch WorldPainter**.
2. Click **`File` ➔ `Import` ➔ `Height map...`**
3. Browse and select: **`ASHENFALL_HEIGHTMAP_16BIT.png`**.
4. In the **Import Height Map** dialog, configure these **exact settings**:

### ⚙️ Exact Height Settings:
* **Mapping:**
  - **Scale:** `100%` (produces an exact $4{,}096 \times 4{,}096$ block world; or `200%` for full $8{,}000 \times 8{,}000$ blocks)
  - **Height:** Set **`Lower limit: -64`** and **`Upper limit: 320`** (Total 384 blocks).
* **Water:**
  - **Water level:** **`62`**
  - Check: **`Create water in areas lower than water level`**
* **Terrain:**
  - Surface material: **`Bare stone / grass`**
* **Border:**
  - Border type: **`Endless water`** (This naturally creates The Veil of Salt ocean surrounding your continent!)

5. Click **`OK`**.
   WorldPainter will sculpt the entire continent in seconds!

---

## 🎨 Recommended Biome & Layer Painting in WorldPainter:

1. **The Ashen Caldera (Center: `0, 0`):**
   - Paint **`Basalt Deltas`** or **`Nether Wastes`** inside the crater basin.
   - Use the **`Blackstone`** or **`Basalt`** terrain palette for the volcanic rim ($Y=145$).
2. **The Cogwork March (West: `-2100, 0`):**
   - Paint **`Windswept Gravelly Hills`** and **`Badlands`**.
   - Carve Create factory foundations along the brass river canyons.
3. **The Solitary Glacial Spine (North: `0, -2500`):**
   - Paint **`Frozen Peaks`** on the summits ($Y \ge 180$).
   - Paint **`Snowy Slopes`** and **`Grove`** down the mountainsides.
4. **The Gilded Dunes (East: `2300, 0`):**
   - Paint **`Desert`** on the rolling barchan dunes.
   - Paint **`Red Sand`** and **`Terracotta`** on the flat-topped mesas.
5. **The Forgotten Coast (South: `0, 2500`):**
   - Paint **`Plains`** and **`Meadow`** on the coastal bluffs.
   - Paint **`Stony Shore`** along the waterline.

---

## 🚀 Exporting to Minecraft 1.21.1:

1. Click **`File` ➔ `Export` ➔ `Export as Minecraft map...`**
2. In the Export dialog:
   - **Game version:** Select **`Minecraft 1.19 or later (Deepslate / 384 blocks)`**.
   - Check **`Allow Cheats`** and select **`Survival`**.
3. **The Populate Layer (Still Life Compatibility):**
   - If you want **Still Life** to generate all dense trees, fallen logs, and wildflowers: enable **`Populate`** on the land!
4. Click **`Export`** and choose your `.minecraft/saves/Ashenfall` directory!

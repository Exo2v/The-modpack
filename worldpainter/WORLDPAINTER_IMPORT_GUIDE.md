# WorldPainter Import Guide: Ashenfall Continent of Vantyra
### *How to Import the Master 16-Bit Heightmap & Pre-Populated Biomes into WorldPainter*

---

## 🗺️ Master Deliverables
* **16-Bit Grayscale Heightmap:** `ASHENFALL_HEIGHTMAP_16BIT.png` (4096 x 4096, 16-bit uint16 master)
* **Pre-Population Layer Mask:** `ASHENFALL_POPULATE_MASK.png` (4096 x 4096, 1:1 vegetation & town mask)
* **Numeric Biome Mask:** `ASHENFALL_BIOME_MASK.png` (4096 x 4096, Minecraft 1.21.1 Biome IDs)
* **Automated Setup Script:** `ashenfall_worldpainter_setup.js` (Turnkey 1-click script for WorldPainter)
* **Satellite Visual Reference:** `ASHENFALL_TOPOGRAPHIC_RENDER.png` (2048 x 2048 3D hillshaded atlas)
* **Preview Heightmap:** `ASHENFALL_HEIGHTMAP_PREVIEW.png` (8-bit grayscale for image viewers)

---

## ⚡ Method 1: Automated 1-Click Script (Fastest)

WorldPainter has a built-in JavaScript engine (`Tools` ➔ `Run script...`). You can create, populate, and configure the entire continent in 5 seconds:

1. Launch **WorldPainter**.
2. Click **`Tools` ➔ `Run Script...`** in the top menu bar.
3. Select **`ashenfall_worldpainter_setup.js`**.
4. WorldPainter will automatically:
   * Load `ASHENFALL_HEIGHTMAP_16BIT.png`.
   * Configure height range ($-64$ to $320$) and sea level ($62$).
   * Apply `ASHENFALL_POPULATE_MASK.png` across all habitable valleys, plains, and riverbanks.
   * Save the completed project as **`Ashenfall_Continent.world`**!
5. Open `Ashenfall_Continent.world`, inspect the 3D continent, and export directly!

---

## 🛠️ Method 2: Manual Heightmap & Mask Import (Visual GUI)

If you prefer using WorldPainter's standard visual menus:

### Step 1: Import the Heightmap
1. Click **`File` ➔ `Import` ➔ `Height map...`**
2. Browse and select: **`ASHENFALL_HEIGHTMAP_16BIT.png`**.
3. In the dialog, set:
   * **Scale:** `100%` (or `200%` for an exact 1:1 $8{,}000 \times 8{,}000$ block world).
   * **Height:** Set **`Lower limit: -64`** and **`Upper limit: 320`** (Total 384 blocks).
   * **Water level:** **`62`** (Check *"Create water in areas lower than water level"*).
   * **Terrain:** Surface material: **`Bare stone / grass`**.
   * **Border:** Select **`Endless water`**.
4. Click **`OK`**.

### Step 2: Apply the Pre-Population Mask
1. Click **`Edit` ➔ `Import` ➔ `Mask as layer...`**
2. Browse and select: **`ASHENFALL_POPULATE_MASK.png`**.
3. In the layer dropdown, select: **`Populate`**.
4. Set mapping: **`White (255)` ➔ `100% intensity`**.
5. Click **`OK`**.
   *All habitable valleys, forests, riverbanks, and plains are now instantly painted with the Populate layer!*
   *The volcanic crater of the Ashen Caldera and sheer rock walls remain clean and barren.*

### Step 3: Apply Biomes
1. Click **`Edit` ➔ `Import` ➔ `Mask as layer...`**
2. Browse and select: **`ASHENFALL_BIOME_MASK.png`**.
3. In the layer dropdown, select: **`Biomes`**.
4. Click **`OK`**.

---

## 🚀 Exporting to Minecraft 1.21.1:

1. Click **`File` ➔ `Export` ➔ `Export as Minecraft map...`**
2. In the Export dialog:
   - **Game version:** Select **`Minecraft 1.19 or later (Deepslate / 384 blocks)`**.
   - Ensure **`Populate`** is checked.
   - Check **`Allow Cheats`** and select **`Survival`**.
3. Click **`Export`** and choose your `.minecraft/saves/Ashenfall` directory!

When Minecraft loads:
* **Still Life** will dynamically populate every chunk with photorealistic branches, fallen logs, mossy boulders, and wildflower carpets.
* **Towns and Towers** will detect flat coastal shorelines and generate medieval fishing ports, taverns, and inns.
* **Explorify** and **YUNG's mods** will place dungeons, desert temples, and bridges across river canyons!

# Ashenfall Datapack: data2 (`datapacks/ashenfall_data2/`)

### *Unified Lithosphere Continuous Spline & Still Life Biome Engine*
*(Minecraft 1.21.1 NeoForge · Data Pack Format 48)*

---

## 🗺️ What This Datapack Solves

1. **Abrupt Biome Seams (Zero Straight-Line Cutoffs)**:
   - Added a dense, continuous transitional biome belt (`grove`, `taiga`, `old_growth_pine_taiga`, `windswept_forest`, `meadow`) between the Solitary Glacial Spine and temperate regions.
   - Smooth multi-noise Euclidean distance mapping eliminates sharp Voronoi boundaries.

2. **Stepped Contour Terraces**:
   - Integrated with Lithosphere's continuous spline density functions (`continents`, `erosion`, `ridges`, `offset`, `factor`).
   - Natural, smooth organic slopes without voxel stair-stepping.

3. **Dry-Land Ocean Shipwrecks (The Y=117 Mountain Wreck Bug)**:
   - Continentalness noise strictly bounds ocean biomes (`deep_ocean`, `cold_ocean`, `lukewarm_ocean`) to $C < -0.15$.
   - Land biomes strictly require $C > 0.05$.
   - Structures that target ocean biomes can **never** spawn on dry land!

4. **100% World Fullness Restored**:
   - Works fully through Minecraft's native worldgen chunk pipeline.
   - Still Life runs its complete `features` decorator pass on every chunk, populating dense oak/birch forests, fallen logs, mossy stone boulders, wild berry bushes, and wildflower meadows.

5. **Region Geography (The 9 Nations)**:
   - **The Cogwork March** at `(-2000, 0)`: Carved river canyons, windswept gravelly hills, wooded badlands, and stony canal banks.
   - **The Solitary Glacial Spine** at `(0, -2500)`: Frozen peaks, jagged crags, snowy slopes, and alpine cirques.
   - **The Ashen Caldera** at `(0, 0)`: Sunken volcanic crater with basalt deltas, blackstone, and scorched badlands.
   - **The Gilded Dunes** at `(2500, 0)`: Amber desert sand sea, terracotta mesas, and arid savannas.
   - **The Whispering Fen** at `(2000, 2000)`: Mangrove bayous, dark forests, and muddy deltas.
   - **The Forgotten Coast** at `(0, 2500)`: Cold coastal bluffs, lush wildflower meadows, and plains (Spawn).
   - **The Veil of Salt**: Outer ocean border surrounding the finite 8,000 × 8,000 continent.

---

## ⚡ How to Install

### Option A: Install into an Existing World Save
1. Copy `data2.zip` (or the `data2` folder) into:
   `.minecraft/saves/Ashenfall/datapacks/`
2. Launch Minecraft and load the world!

### Option B: Automatic Pack Override
This datapack is automatically pre-installed in `pack/overrides/datapacks/ashenfall_data2.zip` so all new worlds automatically include it!

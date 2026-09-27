# Ashenfall v1.2.0 — Handcrafted World Map 1 & Native Worldgen (Single Zip Release)

Welcome to the **single zip release** for **Ashenfall Map 1 (Iteration: `map1`)** on **Minecraft 1.21.1 NeoForge**!

This release completely resolves all previous terrain defects (stepped hillside terracing, knife-edge biome cut-offs, dry-land shipwrecks, and barren snowfields) by restoring **native Lithosphere continuous spline generation** and **Still Life biome fullness**.

---

## 📥 Direct Downloads

### 🌟 Single All-in-One Master ZIP (Recommended)
Download this single archive to get everything (the world save, 1-click installers, mod downloader, configs, KubeJS scripts, and high-res continent maps):
- [⬇️ **Download `ashenfall-map1-native-release.zip`**](https://github.com/Exo2v/The-modpack/raw/arena/01a0e180-the-modpack/downloads/ashenfall-map1-native-release.zip) *(834 KB)*
- *Mirror (in builds/map1/)*: [Download `ashenfall-map1-release.zip`](https://github.com/Exo2v/The-modpack/raw/arena/01a0e180-the-modpack/builds/map1/ashenfall-map1-release.zip)

---

### ⚡ Quick Standalone Files (If you prefer individual files)
- **1-Click World Installer (.bat)**: [Download `build_world.bat`](https://github.com/Exo2v/The-modpack/raw/arena/01a0e180-the-modpack/build_world.bat)
- **Standalone World Builder (.py)**: [Download `build_world.py`](https://github.com/Exo2v/The-modpack/raw/arena/01a0e180-the-modpack/build_world.py)
- **1-Click Mod Downloader (.bat)**: [Download `download_mods.bat`](https://github.com/Exo2v/The-modpack/raw/arena/01a0e180-the-modpack/download_mods.bat)
- **Mod Downloader Engine (.py)**: [Download `download_mods.py`](https://github.com/Exo2v/The-modpack/raw/arena/01a0e180-the-modpack/download_mods.py)
- **High-Res Topographic Continent Map (.png)**: [Download `ASHENFALL_LITHOSPHERE_MAP.png`](https://github.com/Exo2v/The-modpack/raw/arena/01a0e180-the-modpack/ASHENFALL_LITHOSPHERE_MAP.png)

---

## 🚀 How to Install & Play (1 Click)

### Option A: 1-Click Automatic Setup
1. Download and extract **`ashenfall-map1-native-release.zip`**.
2. Double-click **`build_world.bat`** (or `install_world.bat`).
   - Automatically detects your `.minecraft/saves` directory (including TLauncher isolated instances).
   - Purges any stale synthetic chunks.
   - Installs the clean world save with satellite menu icon in under 1 second.
3. If you haven't installed the mods yet, double-click **`download_mods.bat`**.
4. Launch Minecraft 1.21.1 NeoForge and select **"Ashenfall - The Broken Realm"** in Singleplayer!

### Option B: Drag & Drop (Zero Python Needed)
1. Extract `ashenfall-map1-native-release.zip`.
2. Copy the folder `saves/Ashenfall` directly into your `.minecraft/saves/` directory.
3. Launch Minecraft!

---

## 🗺️ The Continent of Vantyra (8,000 × 8,000 Finite World)

```
                            [ NORTH: Z = -4000 ]
                     ══════════════════════════════════
                            THE VEIL OF SALT (OCEAN)
                     ══════════════════════════════════
                                    │
                       [ THE SOLITARY GLACIAL SPINE ]
                      (Z = -1500 to -3500, X = -2000 to +2000)
                     Jagged Snow Peaks & Glacial Cirques (Y = 140 - 210)
                                    │
   [ WEST: X = -4000 ]              │              [ EAST: X = +4000 ]
 ══════════════════════             │             ══════════════════════
   THE SUNKEN REACH                 │               THE GILDED DUNES
 (Drowned Port Ostraka)             │              (Al-Qadira Sand Sea)
  Shallow Lagoons & Reefs           │              Rolling Dunes & Terracotta
  X = -2500, Z = +1500              │              X = +2500, Z = 0
            │                       │                       │
            ├─────────────── [ THE CALDERA ] ───────────────┤
            │                  (X = 0, Z = 0)               │
            │           Throne of Melted Obsidian           │
            │          Jagged Volcanic Ring: Y = 145        │
            │           Sunken Crater Floor: Y = 38         │
            │                       │                       │
   [ THE COGWORK MARCH ]            │             [ THE WHISPERING FEN ]
  (Brass Canyons & Terraces)        │             (Deep Bayou & Mangroves)
  Stepped Cliffs & River Gorges     │             Muddy Deltas (Y = 60 - 64)
  X = -2000, Z = 0                  │             X = +2000, Z = +2000
                                    │
                     [ THE FORGOTTEN COAST & SPAWN ]
                       (X = 0, Z = 2500 — Marked RED)
                     Cold Pebble Beaches & Rolling Bluffs
                                    │
                     ══════════════════════════════════
                            THE VEIL OF SALT (OCEAN)
                     ══════════════════════════════════
                            [ SOUTH: Z = +4000 ]
```

---

## 🛠️ Key Technical Upgrades in This Build
* **Native Lithosphere Spline Engine**: Continental elevation, ridge lines, and continuous river canyons interpolate naturally without artificial quantization or contour terracing.
* **Full Still Life Flora**: Native chunk decoration runs in full—dense forests, fallen birch and oak logs, mossy boulders, wild berry bushes, and colorful wildflower meadows populate every biome.
* **Proper Biome Interpolation**: Multi-noise 5D climate blending replaces hard Voronoi edges, eliminating straight-line seams between biomes.
* **Accurate Structure Spawning**: Ocean structures generate exclusively in genuine water bodies, and villages/dungeons adapt to natural valleys.
* **Survival & Combat Balance**:
  - **Health**: 20 Hearts base (40 Max HP) permanent.
  - **Combat**: 100% Pure Vanilla PvP (cooldown, sweep, crits, sprint hits).
  - **Dragons**: Rare endgame bosses with 2,500-block sanctuary buffer from spawn.

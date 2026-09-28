# ⚔️ ASHENFALL: The Broken Realm ⚔️
### *A Soulslike RPG Pilgrimage & Geological Continent Overhaul*
**Minecraft 1.21.1 · NeoForge · Pack Format: 48 · Map Canvas: 8,000 × 8,000 Blocks**

---

## ⚡ 1-Click Fast Start (Zero Setup Needed)

To automatically install the complete **Ashenfall Continent world save**, the **Still Life + Lithosphere datapack**, and the narrative **KubeJS scripts** directly into your Minecraft folder, paste this into **Windows PowerShell**:

```powershell
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object System.Net.WebClient).DownloadFile('https://raw.githubusercontent.com/Exo2v/The-modpack/arena/01a0e180-the-modpack/setup.ps1', "$env:TEMP\setup.ps1"); powershell -NoProfile -ExecutionPolicy Bypass -File "$env:TEMP\setup.ps1"
```
*(Or double-click `build_world.bat` in the repository root).*

---

## 🌐 Ashenfall WorldStudio (Unified GUI)

We built an integrated web software that unifies **WorldPainter**, **Lithosphere**, **Still Life**, and **Continents** into a single interactive dashboard:

```bash
python tools/world_studio/server.py
```
*Open `http://localhost:3000` to access the interactive map with real-time coordinate inspection, Still Life foliage overlays, and 1-click downloads.*

---

## 📁 Repository Directory Structure

The repository is organized into dedicated, logical modules:

```
The-modpack/
├── README.md                      # Master repository guide (this document)
├── setup.ps1                      # Native 1-click Windows installer (zero Python)
├── build_world.bat                # 1-click batch launcher
├── build_world.py                 # Standalone world builder script
│
├── datapacks/                     # Minecraft 1.21.1 Worldgen Datapacks
│   ├── sources/                   # Upstream reference packs provided for Ashenfall
│   │   ├── lithosphere-1.8.2.zip  # Jayzet's continuous cubic spline macro-geology
│   │   ├── still_life-0.1.1.zip   # Jayzet's 234-biome realistic foliage & slope pack
│   │   └── tectonic-3.0.25.zip    # Apollo's extreme vertical terrain overhaul
│   ├── ashenfall_data2/           # Unpacked Ashenfall custom continental datapack
│   └── ashenfall_data2.zip        # Ready-to-use zipped worldgen datapack
│
├── worldpainter/                  # High-Resolution Master WorldPainter Suite
│   ├── ASHENFALL_WORLDPAINTER_SUITE.zip   # All-in-one download bundle (9.9 MB)
│   ├── ASHENFALL_HEIGHTMAP_16BIT.png      # 16-bit uint16 heightmap (4096 x 4096)
│   ├── ASHENFALL_POPULATE_MASK.png        # 1:1 vegetation & town mask (4096 x 4096)
│   ├── ASHENFALL_BIOME_MASK.png           # 1:1 Minecraft numeric biome mask
│   ├── ASHENFALL_STILL_LIFE_POPULATE_VIEW.png # 3D composite map with foliage boundary
│   ├── ASHENFALL_TOPOGRAPHIC_RENDER.png   # 3D hillshaded satellite topographic atlas
│   ├── ASHENFALL_HEIGHTMAP_PREVIEW.png    # 8-bit visual grayscale preview
│   ├── ashenfall_worldpainter_setup.js    # Smart auto-locating script (Tools > Run Script)
│   └── WORLDPAINTER_IMPORT_GUIDE.md       # Detailed step-by-step import manual
│
├── tools/                         # Tooling & Generation Engines
│   ├── world_studio/              # Unified Web GUI (Server & SPA frontend)
│   │   ├── server.py              # Multi-threaded Python HTTP/API backend
│   │   └── public/index.html      # Modern Tailwind + Lucide single-page interface
│   ├── generate_detailed_heightmap.py # Procedural 16-bit geological synthesizer
│   └── simulate_lithosphere_engine.py # Python simulator for cubic spline terrain
│
├── docs/                          # Comprehensive Documentation
│   ├── lore/                      # Narrative, faction chronicles & Abode of Will
│   ├── design/                    # Architectural blueprints, handovers & PDFs
│   ├── phases/                    # Milestone gate criteria (M0 through M3b)
│   └── guides/                    # Modlists, install instructions & references
│
├── scripts/                       # Modular Windows batch & bash utility scripts
│   ├── download_mods.py / .bat    # Automated mod JAR downloader
│   ├── install_full_modpack.bat   # Modpack profile installer
│   ├── fix_everything.py / .bat   # Comprehensive dependency conflict resolver
│   └── build.bat / build.sh       # Packwiz manifest build pipelines
│
├── pack/                          # Packwiz Modpack Definition
│   ├── pack.toml                  # Packwiz index
│   ├── mods/                      # Tracked mod TOML references
│   └── overrides/                 # KubeJS scripts & configs
│
├── builds/                        # Build releases and packaged archives
└── downloads/                     # Release distribution bundles
```

---

## 🔬 Datapack Data Analysis & Comparison

We audited and reverse-engineered the three uploaded worldgen packs:

### 1. `lithosphere-1.8.2.zip` (by Jayzet)
* **Architecture:** 49 Density Functions, 17 Noise Settings / Dimensions, 0 Biomes.
* **Core Function:** Completely replaces vanilla Minecraft's piecewise linear splines with **Continuous Cubic Hermite Splines** ($S(t) = 3t^2 - 2t^3$).
* **Key Mechanics:**
  * Carves wide U-shaped and V-shaped glacial river valleys.
  * Replaces jagged "onion-ring" hills with sweeping, gradual mountain slopes.
  * Expands noise wavelengths to 2,000–4,000 blocks for monumental continental scales.

### 2. `still_life-0.1.1.zip` (by Jayzet)
* **Architecture:** 234 Custom Biomes, 294 Placed Features, 294 Configured Features, 149 Tags.
* **Core Function:** Overhauls Minecraft's surface rules, vegetation decorators, and biomes to sit on top of Lithosphere.
* **Key Mechanics:**
  * **Slope-Aware Texturing:** Slopes $< 35^\circ$ receive deep topsoil and wildflower meadows; slopes $> 45^\circ$ expose raw bedrock and stone scree.
  * **Multi-Tiered Forest Structure:** Spawns branched canopy trees, fallen mossy logs (`block_pile`), glacial erratics (mossy stone boulders), and low understory bushes.
  * **Thermal Buffering:** Separates freezing snow biomes from warm biomes by $\Delta T \ge 0.55$, preventing snow pocket glitches.
  * **Mod Integration:** Native tags and structure bindings for `towns_and_towers`, `lithosphere`, and `c:worldgen`.

### 3. `tectonic-3.0.25.zip` (by Apollo)
* **Architecture:** 164 Density Functions, 8 Dimension Settings, 23 Placed Features, 0 Biomes.
* **Core Function:** Alternative macro-terrain overhaul featuring extreme vertical scaling ($Y = 260{-}320+$), sharper crags, and subterranean rivers.
* **Compatibility Note:** Tectonic and Lithosphere both override `minecraft:dimension/overworld.json` and `minecraft:worldgen/noise_settings/overworld.json`. In Ashenfall, **Lithosphere + Still Life** is our designated primary engine because Still Life's 234 biomes are calibrated directly to Lithosphere's density splines.

---

## 🗺️ The 7 Landmarks of Vantyra

The $8{,}000 \times 8{,}000$ continent features 7 landmark factions:

| Landmark | Coordinates | Target Biome | Geological Character |
| :--- | :---: | :--- | :--- |
| **The Forgotten Coast (Spawn)** | `(0, 2500)` | Plains / Meadow | Gentle coastal bluffs ($Y=72$), pebble beaches, medieval fishing ports |
| **The Solitary Glacial Spine** | `(0, -2500)` | Frozen Peaks / Grove | Alpine cordillera rising to **$Y=279$**, arêtes, cirques, ancient pine taiga |
| **The Cogwork March** | `(-2100, 0)` | Badlands / Windswept Hills | 9-block quarry benches, brass river chasms, Create factory plateaus |
| **The Ashen Caldera** | `(0, 0)` | Basalt Deltas / Nether Wastes | Collapsed volcanic ring ($Y=146$), sunken crater basin ($Y=40$), Obsidian Throne |
| **The Gilded Dunes** | `(2300, 0)` | Desert / Eroded Badlands | $45^\circ$ transverse barchan dunes, flat-topped terracotta mesas |
| **The Whispering Fen** | `(2000, 2000)`| Swamp / Mangrove | Flat sunken bayou ($Y=63$), braided delta channels, witch huts |
| **The Sunken Reach** | `(-2400, 1600)`| Warm Ocean / Atoll | Drowned caldera shelf ($Y=54$), coral reefs, barrier sandbars |

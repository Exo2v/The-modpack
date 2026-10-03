# Ashenfall Worldgen Datapack Handover Specification
### *Engineering Blueprint for Autonomous Agent & Human Developer Continuation*
**Target Environment:** Minecraft 1.21.1 Java Edition · **Mod Loader:** NeoForge 1.21.1 · **Data Pack Format:** 48  
**Core Dependencies:** Lithosphere (v1.3+), Still Life (v0.1+), Create (6.0.9+)  
**Repository Branch:** `arena/01a0e180-the-modpack`

---

## 1. Executive Summary & Mission Objective

The goal of this task is to deliver a **production-grade world generation system** for the soulslike modpack **Ashenfall: The Broken Realm**.

The world of Ashenfall is **Vantyra**: a strictly finite $8{,}000 \times 8{,}000$ block continent birthed from the collapse of a 10-dimensional divine realm ("The Abode of Will"), bounded by an impassable outer ocean ("The Veil of Salt"), and scarred by the remnants of nine fallen factions.

### Primary Objectives:
1. **Preserve Complete Flora & Chunk Fullness:** Chunks must run Minecraft's native `FEATURES` decoration pass in full—generating Still Life's dense oak/birch canopies, fallen birch/oak logs, mossy stone boulders, wild berry shrubs, and wildflower pastures.
2. **Eliminate All Stepped Contour Terracing:** Terrain slopes must be continuous, gradual, and cinematic, driven by Lithosphere's non-quantized 3D spline density functions.
3. **Eliminate Climate Clashing & Snow Pockets:** Cold snowy biomes and warm green forests must **never** spawn adjacent to one another. Climate zones must be separated by wide, continuous buffer belts.
4. **Eliminate Mountaintop Shipwrecks:** Ocean biomes must **strictly** be bound to true submarine elevations ($Y \le 62, C < -0.15$). Ocean structures must never spawn on dry land.
5. **Realize the 9 Nations of Vantyra:** Establish the geographical landmarks of the continent at their designated coordinates (The Caldera at center $(0,0)$, Cogwork March at $(-2000, 0)$, Glacial Spine at $(0, -2500)$, Gilded Dunes at $(2500, 0)$, Forgotten Coast spawn at $(0, 2500)$).

---

## 2. Post-Mortem Analysis: Root Causes of Previous Failures

To avoid repeating previous mistakes, any agent continuing this work must understand why earlier iterations exhibited severe visual and structural defects:

```
                            THE WORLDGEN PIPELINE
┌────────────────────────┐      ┌────────────────────────┐      ┌────────────────────────┐
│     STRUCTURE_STARTS   │ ───> │         BIOMES         │ ───> │          NOISE         │
└────────────────────────┘      └────────────────────────┘      └────────────────────────┘
                                                                             │
┌────────────────────────┐      ┌────────────────────────┐      ┌────────────▼───────────┐
│     LIGHT & SPAWN      │ <─── │        FEATURES        │ <─── │        SURFACE         │
│   (Final Settlement)   │      │ (Trees, Logs, Flowers) │      │ (Grass, Sand, Topsoil) │
└────────────────────────┘      └────────────────────────┘      └────────────────────────┘
```

### Failure 1: The Barren World & Stepped Terraces (Synthetic MCA Voxel Injection)
* **What Happened:** An early script (`build_world.py`) generated raw `.mca` chunk files directly and wrote `Status: "minecraft:full"`.
* **Why It Failed:** 
  1. When chunk status is marked `full`, Minecraft considers the chunk finished and **skips the `FEATURES` pass entirely**. All trees, shrubs, fallen logs, boulders, and flowers were bypassed.
  2. The script quantized elevation to integer layers ($Y = \text{round}(h)$), carving stair-step voxel contours across every hillside.
* **The Rule:** **Never inject pre-baked `.mca` chunks with `Status: "minecraft:full"`.** Minecraft's internal decorator engine must execute natively.

### Failure 2: Dry-Land Shipwrecks on Mountain Peaks at $Y=117$
* **What Happened:** In-game screenshots showed a wooden shipwreck sitting on a dry snowy mountaintop at $Y=117$, with F3 reporting `minecraft:deep_ocean`.
* **Why It Failed:** In Minecraft, structure placement queries the underlying multi-noise continentalness. The custom datapack mapped `minecraft:deep_ocean` to a continentalness range that coincided with high elevation splines. The structure locator found `deep_ocean`, searched downward for the highest solid block, and rested the shipwreck atop the mountain.
* **The Rule:** Ocean biomes must be **strictly separated** from land biomes in multi-noise:
  - Deep Ocean / Ocean: $C \in [-1.2, -0.20]$ (Offset sinks terrain below sea level).
  - Coast / Shore: $C \in [-0.15, 0.05]$ (Beaches and stony bluffs).
  - Inland Continents: $C \in [0.05, 1.20]$ (Strictly land biomes; ocean structures can never generate).

### Failure 3: The Snow-Pocket Glitch (Cold and Warm Biomes Spawning Together)
* **What Happened:** Screenshots showed an isolated patch of `minecraft:grove` (snowy leaves and white ground) inside a temperate dark spruce forest (`taiga`), separated only by a river.
* **Why It Failed:** In `data2`, `grove` was placed at $\text{Temperature} = -0.60$ and `old_growth_spruce_taiga` was placed at $\text{Temperature} = -0.50$. The gap between them was only $0.10$. Because Minecraft's temperature noise naturally undulates across hills, a slight negative dip caused the 5D Voronoi distance calculation to flip from green taiga to freezing snow across a 30-block span.
* **The Rule:** Freezing snow biomes must be separated from temperate biomes by **at least $0.55$ units of temperature**, insulated by a broad non-snowy boreal taiga buffer belt.

### Failure 4: The Datapack Coordinate Limitation in 1.21.1
* **What Happened:** At $(-2000, 0)$, players saw a random snowy forest rather than the Cogwork March river canyon.
* **Why It Failed:** Datapack density functions in Minecraft 1.21.1 rely strictly on **procedural Perlin noise** (`shifted_noise`, `noise`). Perlin noise is periodic and pseudo-random; it has no concept of absolute coordinates $X$ and $Z$. *(Coordinate-aware density functions like `axis: x/z` gradients were only added by Mojang in 26.3 snapshots).*

---

## 3. The Continent of Vantyra: Target Coordinates & Specifications

The world border is fixed at **$8{,}000 \times 8{,}000$ blocks** centered at $(0, 0)$, enclosed by **The Veil of Salt** ocean.

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

### Landmark Coordinates Table:

| Key | Nation / Region | Center $(X, Y, Z)$ | Target Biomes | Key Visual & Mechanical Features |
| :---: | :--- | :---: | :--- | :--- |
| **`1`** | **The Forgotten Coast** *(Spawn)* | `(0, 68, 2500)` | `plains`, `meadow`, `forest`, `stony_shore` | Awakening beach, old lighthouse beacon, starter chest, rolling coastal bluffs. |
| **`2`** | **The Cogwork March** | `(-2000, 85, 0)` | `windswept_hills`, `river`, `wooded_badlands`, `windswept_gravelly_hills` | Deep carved river canyons, steam-powered canal boats, clunker automaton boss, Create factories. |
| **`3`** | **The Ashen Caldera** | `(0, 80, 0)` | `basalt_deltas`, `eroded_badlands`, `savanna_plateau` | Epicenter of the Fall; sunken volcanic crater ($Y=38$), basalt columns, blackstone ground. |
| **`4`** | **The Solitary Glacial Spine** | `(0, 160, -2500)` | `frozen_peaks`, `jagged_peaks`, `snowy_slopes`, `grove` | Massive northern alpine range ($Y=160{-}210$), permafrost cirques, glacial ice spikes. |
| **`5`** | **The Gilded Dunes** | `(2500, 75, 0)` | `desert`, `badlands`, `eroded_badlands`, `savanna` | Vast amber sand sea, terracotta canyon mesas, scorched nomadic steppes. |
| **`6`** | **The Whispering Fen** | `(2000, 64, 2000)` | `swamp`, `mangrove_swamp`, `dark_forest` | Murky mangrove bayous, giant mushroom canopies, witchbane inquisitor towers. |
| **`7`** | **The Sunken Reach** | `(-2500, 62, 1500)` | `warm_ocean`, `lukewarm_ocean`, `beach`, `stony_shore` | Drowned port archipelago, shallow coral lagoons, tidal sandbars. |
| **`8`** | **The Hermit's Reach** | `(-1800, 140, -1800)`| `jagged_peaks`, `stony_peaks` | Solitary granite needles, ascetic mountain shrines. |
| **`9`** | **The Byzantine Choir** | `(1800, 120, -1800)` | `cherry_grove`, `meadow`, `flower_forest` | Gilded resonant basilicas, pink cherry blossoms, harmonic ruins. |
| **`RIM`**| **The Veil of Salt** | $R > 3800$ | `deep_ocean`, `deep_cold_ocean` | Bounding ocean abyss enclosing the $8{,}000 \times 8{,}000$ realm. |

---

## 4. Multi-Noise Climate Engineering Specification

To completely eliminate the "cold biome next to warm biome" defect, the multi-noise parameter distribution must strictly obey the following **5-Tier Climate Banding**:

```
                       5-TIER CLIMATE SEPARATION
  T <= -0.75         -0.60 <= T <= -0.25         -0.15 <= T <= 0.40         T >= 0.65
┌──────────────┐     ┌──────────────────────┐     ┌────────────────────┐     ┌──────────────┐
│ TIER 0:      │     │ TIER 1:              │     │ TIER 2:            │     │ TIER 4:      │
│ FREEZING     │ ──> │ BOREAL BUFFER BELT   │ ──> │ TEMPERATE COAST    │ ──> │ ARID EXPENSE │
│ (Snow & Ice) │     │ (Green Taiga/Pines)  │     │ (Plains & Meadows) │     │ (Desert/Mesa)│
│ [Strictly    │     │ [Strictly Rain,      │     │ [Grasslands,       │     │ [No Rain,    │
│  Snow Only]  │     │  ZERO Snow]          │     │  Foliage Blending] │     │  Terracotta] │
└──────────────┘     └──────────────────────┘     └────────────────────┘     └──────────────┘
       ▲                        ▲                            ▲                      ▲
       └────────────────────────┴──────────┬─────────────────┴──────────────────────┘
                                           │
                             Separated by >= 0.20 Gaps
                            (Prevents Noise Flickering)
```

### Parameter Thresholds:

1. **Tier 0 — Freezing Glacial ($T \le -0.75$):**
   - Biomes: `minecraft:frozen_peaks`, `minecraft:jagged_peaks`, `minecraft:snowy_slopes`, `minecraft:grove`, `minecraft:snowy_plains`, `minecraft:ice_spikes`.
   - Precipitation: **Snow**.
   - Continentalness: $C \in [0.20, 0.90]$.

2. **Tier 1 — Boreal Insulation Buffer ($T \in [-0.60, -0.25]$):**
   - Biomes: `minecraft:taiga`, `minecraft:old_growth_pine_taiga`, `minecraft:old_growth_spruce_taiga`, `minecraft:windswept_forest`.
   - Precipitation: **Rain (NO SNOW)**.
   - Purpose: Acts as a geographical moat insulating Tier 0 freezing snow from Tier 2 temperate grass.

3. **Tier 2 — Temperate Heartland & Coast ($T \in [-0.15, 0.40]$):**
   - Biomes: `minecraft:plains`, `minecraft:meadow`, `minecraft:forest`, `minecraft:flower_forest`, `minecraft:birch_forest`.
   - Continentalness: $C \in [0.10, 0.65]$.

4. **Tier 3 — Humid Bayou & Fen ($T \in [0.25, 0.70], H \ge 0.45$):**
   - Biomes: `minecraft:swamp`, `minecraft:mangrove_swamp`, `minecraft:dark_forest`.
   - Erosion: $E \in [0.20, 0.90]$.

5. **Tier 4 — Scorched Desert & Mesas ($T \ge 0.65, H \le -0.30$):**
   - Biomes: `minecraft:desert`, `minecraft:badlands`, `minecraft:eroded_badlands`, `minecraft:savanna`.

6. **The Maritime Outer Moat ($C < -0.20$):**
   - Biomes: `minecraft:deep_ocean`, `minecraft:ocean`, `minecraft:deep_cold_ocean`, `minecraft:deep_lukewarm_ocean`.
   - Elevation offset: Strictly negative, guaranteeing deep water.

---

## 5. Architectural Approaches for Future Implementation

There are two viable architectural paths to realize the continent in Minecraft 1.21.1:

### Path A: The Native World Save Generator (Recommended for True Elden Ring Handcrafting)
Because Minecraft 1.21.1 density functions lack horizontal coordinate gradients ($X, Z$), the true way to guarantee that $(-2000, 0)$ is the Cogwork March and $(0, 0)$ is the Caldera is by generating the world save via Python with **partial chunk initialization**:
* **How to Implement:**
  1. The Python script generates the elevation and biome assignment for the $8{,}000 \times 8{,}000$ grid using mathematical radial/coordinate formulas.
  2. The script writes `.mca` files containing the surface heightmap and biome palettes, but sets:
     ```python
     'Status': String('minecraft:biomes') # or 'minecraft:noise'
     ```
  3. **Critical Step:** Do **NOT** set `Status: "minecraft:full"`.
  4. When the game loads the world, Minecraft detects that the chunks have not completed the `FEATURES` pass. It passes the chunks through Still Life's native decorator pipeline, placing all trees, fallen birch/oak logs, mossy boulders, and wildflowers directly on top of the custom terrain!

### Path B: Seed-Synchronized Procedural Datapack
If the user prefers a pure datapack:
* **How to Implement:**
  1. Calibrate density functions (`continents.json`, `temperature.json`, `vegetation.json`, `erosion.json`) with ultra-low frequency scaling (`xz_scale: 0.035 - 0.05`).
  2. Maintain the 5-Tier climate separation in `dimension/overworld.json` (1,489+ points).
  3. Curate the world seed in `level.dat` (`seed: 4815162342`) so that the macro Perlin wave peaks coincide with the cardinal coordinates.

---

## 6. In-Game Verification: The 5-Location Wayfinder Compass

The modpack includes an automated in-game verification tool:
* **File:** `pack/overrides/kubejs/server_scripts/wayfinder_compass.js`
* **Trigger:** Players spawn with the `🧭 Ashenfall Wayfinder Compass`. Right-clicking **any compass** in hand opens an interactive 5-destination chat GUI.

### Interactive Teleport Commands:
* `/wayfinder 1` ➔ Teleports to **The Forgotten Coast** `(0, 68, 2500)`
* `/wayfinder 2` ➔ Teleports to **The Cogwork March** `(-2000, 85, 0)`
* `/wayfinder 3` ➔ Teleports to **The Ashen Caldera** `(0, 80, 0)`
* `/wayfinder 4` ➔ Teleports to **The Solitary Glacial Spine** `(0, 160, -2500)`
* `/wayfinder 5` ➔ Teleports to **The Gilded Dunes** `(2500, 75, 0)`
* Datapack fallback: `/function ashenfall:wayfinder`

### Quality Assurance Checklist for Testing:
1. **At `(0, 160, -2500)` (Glacial Spine):**
   - Press **F3**. Biome must report `frozen_peaks`, `snowy_slopes`, or `grove`.
   - Elevation should reach $Y \ge 160$.
   - Fly south toward $(0, 0)$. Verify that snow smoothly transitions into green spruce taiga without knife-edge grass seams.
2. **At `(-2000, 85, 0)` (Cogwork March):**
   - Press **F3**. Biome should report `windswept_hills`, `river`, or `wooded_badlands`.
   - Must **not** be a featureless snowfield. Terrain should feature river gorges and canyon walls.
3. **At `(0, 80, 0)` (Caldera):**
   - Press **F3**. Biome should report volcanic/eroded biomes (`basalt_deltas`, `eroded_badlands`).
4. **At `(2500, 75, 0)` (Gilded Dunes):**
   - Press **F3**. Biome should report `desert` or `badlands`.
5. **Around All Water Bodies:**
   - Verify that shipwrecks and ocean monuments only generate submerged in genuine water, never atop mountains.

---

## 7. Deliverable File Structure

```
The-modpack/
├── ASHENFALL_WORLDGEN_DATAPACK_HANDOVER_SPECIFICATION.md  # This master document
├── builds/
│   ├── DATAPACK_HANDOVER_SPECIFICATION.md                # Builds reference copy
│   ├── data2/                                            # Unpacked production datapack
│   │   ├── pack.mcmeta                                   # Format 48 (MC 1.21.1)
│   │   ├── README.md                                     # Datapack overview
│   │   └── data/
│   │       ├── ashenfall/function/                       # Built-in wayfinder mcfunctions
│   │       │   ├── wayfinder.mcfunction
│   │       │   ├── tp_coast.mcfunction
│   │       │   ├── tp_cogwork.mcfunction
│   │       │   ├── tp_caldera.mcfunction
│   │       │   ├── tp_glacial.mcfunction
│   │       │   └── tp_gilded.mcfunction
│   │       └── minecraft/
│   │           ├── dimension/
│   │           │   └── overworld.json                    # 1,489 calibrated multi-noise points
│   │           └── worldgen/density_function/overworld/  # Lithosphere continuous splines
│   │               ├── continents.json
│   │               ├── erosion.json
│   │               ├── ridges.json
│   │               ├── temperature.json
│   │               └── vegetation.json
│   ├── data2.zip                                         # Packaged datapack archive
│   └── map1/                                             # Build iteration 1 artifacts
│       ├── build_world.py                                # Clean world save setup script
│       ├── build_world.bat                               # 1-Click Windows runner
│       ├── ashenfall-map1-release.zip                    # Master bundle zip
│       └── data2.zip                                     # Mirror of data2
├── pack/
│   └── overrides/
│       ├── datapacks/ashenfall_data2.zip                 # Auto-installed modpack datapack
│       └── kubejs/server_scripts/
│           ├── wayfinder_compass.js                      # 5-Destination compass teleport system
│           └── intro_awakening.js                        # Starter lighthouse & equipment
└── tools/
    └── build_data2.py                                    # Automated build & compilation engine
```

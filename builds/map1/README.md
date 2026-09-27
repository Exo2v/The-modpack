# Ashenfall Build Iteration: Map 1 (`builds/map1/`)

### *The Handcrafted 8,000 × 8,000 Elden Ring Finite Continent of Vantyra*
*(Powered by Native Lithosphere Continuous Spline Terrain & Still Life Biome Fullness)*

---

## 🗺️ About This Build (Iteration: `map1`)

This build represents the first full iteration of the **handcrafted continent of Vantyra**, built using the **Elden Ring method** (pure organic terrain, continuous mountain ranges, deep river canyons, sweeping badlands, and ocean cliffs with zero synthetic chunk corruption, ready for landmark and dungeon placement).

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

## ⚡ How to Install (Zero Other Steps)

### Method 1: Double-Click Batch (Windows)
Double-click `install_world.bat` or `build_world.bat`.
It will automatically locate your `.minecraft/saves` (including TLauncher isolated instances), clean any old broken synthetic chunks, write the pristine `level.dat`, and set up the world in under 1 second!

### Method 2: Run Python directly
```bash
python build_world.py
```

### Method 3: Manual Drag & Drop
Copy the `saves/Ashenfall` folder directly into your `.minecraft/saves/` directory.

---

## 📦 What's Inside This Release

| File | Description |
|---|---|
| **`build_world.bat` / `install_world.bat`** | 1-click Windows runner that executes the installer automatically. |
| **`build_world.py` / `install_world.py`** | Standalone Python worldbuilder that writes the clean NBT `level.dat` and cleans stale chunks. |
| **`saves/Ashenfall/`** | Pre-built world save folder with pre-configured `level.dat` and `icon.png`. |
| **`download_mods.bat` & `download_mods.py`** | 1-click automated downloader for all required mods (Lithosphere, Still Life, Create, Performance). |
| **`ASHENFALL_LITHOSPHERE_MAP.png`** | High-resolution topographic continent map showing all 9 faction regions and coordinates. |
| **`ASHENFALL_CONTINENT_MAP.png`** | Satellite geological elevation render of Vantyra. |

---

## 🎮 In-Game World Specs
* **World Name**: `Ashenfall - The Broken Realm`
* **World Seed**: `4815162342`
* **Spawn Point**: `X: 0, Y: 68, Z: 2500` (The Forgotten Coast)
* **World Border**: `8,000 × 8,000 blocks` (The Veil of Salt)
* **Max Health**: 20 Hearts (40 HP)
* **Combat**: 100% Pure Vanilla PvP (cooldowns, crits, sweep, sprint resets)
* **Compatible Version**: Minecraft 1.21.1 NeoForge

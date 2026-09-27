# Ashenfall Build Iteration: Map 1 (`builds/map1/`)

### *The Handcrafted 8,000 × 8,000 Elden Ring Finite Continent of Vantyra*

---

## 🗺️ About This Build (Iteration: `map1`)

This build represents the first full iteration of the **handcrafted continent of Vantyra**, built using the **Elden Ring method** (pure organic terrain, geological elevations, mountain ranges, canyons, desert dunes, and ocean cliffs with no structures, ready for landmark and dungeon placement).

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

### Method 1: Run Python directly
```bash
python build_world.py
```
*(Or run `python builds/map1/build_world.py`)*

### Method 2: Double-click Batch (Windows)
Double-click `install_world.bat` in this folder.

---

## 📦 What's Inside `builds/map1/`

| File | Description |
|---|---|
| **`build_world.py`** | Standalone Python script that builds and installs this world into your Minecraft saves folder automatically with zero pip dependencies. |
| **`Ashenfall.zip`** | The complete pre-built world archive (9.4 MB) containing `level.dat`, `icon.png`, and 20 Anvil region files (20,480 chunks). |
| **`level.dat`** | Pre-configured world data (DataVersion 3955, Spawn at `0, 68, 2500`, 8,000-block world border). |
| **`icon.png`** | Satellite topographic map icon shown in the Minecraft Singleplayer menu. |
| **`ASHENFALL_CONTINENT_MAP.png`** | High-resolution (1200x1200) topographic satellite render of the entire continent. |
| **`install_world.bat`** | 1-click Windows runner. |

---

## 🎮 In-Game Verification
* **World Name**: `Ashenfall - The Broken Realm`
* **Spawn Point**: `X: 0, Y: 68, Z: 2500` (The Forgotten Coast)
* **World Border**: `8,000 x 8,000 blocks` (The Veil of Salt)
* **Compatible Version**: Minecraft 1.21.1 NeoForge

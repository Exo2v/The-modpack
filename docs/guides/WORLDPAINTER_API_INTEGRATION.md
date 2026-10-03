# WorldPainter Scripting API Integration Guide

This guide documents the turnkey **WorldPainter JSR223 Scripting API integration** built into the repository. It enables automated, headless, and programmable synthesis of 3D Minecraft worlds, custom terrain stratification, populate masks, biome layers, and direct Anvil region exports.

---

## 🏗 Architecture Overview

WorldPainter exposes a Java JSR-223 Scripting API accessible via the `wpscript` CLI utility or through the GUI under **Tools > Run script...**.

Our repository integrates with WorldPainter at three distinct layers:

```
┌─────────────────────────────────────────────────────────────┐
│                 WorldStudio Web App (Port 3000)             │
│   • Interactive UI to configure dimensions, strata & masks  │
│   • Live syntax-highlighted JSR223 script generator         │
│   • REST API: /api/worldpainter/generate-script & /status   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│             Python SDK Bridge (tools/worldpainter_api.py)   │
│   • WorldPainterScriptBuilder: Parametric code synthesizer   │
│   • WorldPainterCLIBridge: Cross-platform wpscript detector │
│   • CLI: python tools/worldpainter_api.py {generate|run}    │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│              Headless JSR223 Script Runner Engine            │
│   • scripts/run_worldpainter_api.bat (Windows auto-runner)  │
│   • scripts/run_worldpainter_api.sh (Linux/macOS runner)    │
│   • wpscript worldpainter/ashenfall_worldpainter_setup.js   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│        Generated Minecraft World or .world Project File     │
│   • Y=-64 to Y=320 16-bit smooth terrain                    │
│   • 100% Still Life Pre-Populate chunk layer               │
│   • Altitude-based geological rock & snow stratification    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Execution Options

### Option 1: 1-Click Headless Windows Runner
Double-click:
```cmd
scripts\run_worldpainter_api.bat
```
The script will:
1. Automatically search for `wpscript.exe` in `PATH`, `C:\Program Files\WorldPainter`, and `%LOCALAPPDATA%\Programs\WorldPainter`.
2. Execute `worldpainter/ashenfall_worldpainter_setup.js` headlessly.
3. Save the resulting project file directly to `~/Downloads/Ashenfall_Continent.world`.

### Option 2: WorldPainter GUI (Manual / Interactive)
1. Open WorldPainter.
2. In the top menu bar, click **Tools** → **Run script...** (or press `Ctrl+R`).
3. Select `worldpainter/ashenfall_worldpainter_setup.js`.
4. WorldPainter will automatically locate `ASHENFALL_HEIGHTMAP_16BIT.png` and `ASHENFALL_POPULATE_MASK.png`, sculpt the $-64 \to 320$ continent, apply the Populate layer, and save the project.

### Option 3: Python CLI
Generate custom scripts with specific limits:
```bash
python tools/worldpainter_api.py generate \
    --world-name "Ashenfall_Custom" \
    --min-y -64 \
    --max-y 320 \
    --sea-level 62 \
    --export-mode world \
    --output worldpainter/my_custom_script.js
```

Detect installed WorldPainter CLI:
```bash
python tools/worldpainter_api.py detect
```

---

## 🧩 Core WorldPainter JSR-223 Scripting API Reference

### 1. Loading Heightmaps
```javascript
var heightMap = wp.getHeightMap()
    .fromFile("path/to/heightmap_16bit.png")
    .go();
```

### 2. Creating a 3D World
```javascript
var world = wp.createWorld()
    .fromHeightMap(heightMap)
    .scale(100)                     // 100% block scaling (1 pixel = 1 block)
    .shift(0, 0)                    // X, Z block offset
    .fromLevels(0, 65535)           // Input 16-bit grayscale range
    .toLevels(-64, 320)             // Target Minecraft vertical bounds
    .withWaterLevel(62)             // Sea level
    .withLowerBuildLimit(-64)       // 1.18+ Extended build limits
    .withUpperBuildLimit(320)
    .go();
```

### 3. Applying Geological Terrain Strata (Altitude Mapping)
```javascript
wp.applyHeightMap(heightMap)
    .toWorld(world)
    .applyToTerrain()
    .fromLevels(-64, 64).toTerrain(36)   // Beaches (ocean floor & shoreline)
    .fromLevels(65, 140).toTerrain(0)    // Grass (lowland plains & river basins)
    .fromLevels(141, 190).toTerrain(3)   // Permadirt (subalpine meadows)
    .fromLevels(191, 250).toTerrain(74)  // StoneMix (exposed mountain crags)
    .fromLevels(251, 320).toTerrain(40)  // DeepSnow (permafrost & glaciated peaks)
    .go();
```

### 4. Applying the "Populate" Layer Mask
The Populate layer instructs Minecraft's internal chunk generator (and mods like Still Life) to run structure, tree, flower, and cave decorators:
```javascript
var popMask = wp.getHeightMap().fromFile("path/to/populate_mask.png").go();
var populateLayer = wp.getLayer().withName("Populate").go();

wp.applyHeightMap(popMask)
    .toWorld(world)
    .applyToLayer(populateLayer)
    .fromLevels(128, 255).toLevel(1)    // White pixels = 100% populated
    .go();
```

### 5. Applying the High-Altitude Frost Layer
```javascript
var frostLayer = wp.getLayer().withName("Frost").go();

wp.applyHeightMap(heightMap)
    .toWorld(world)
    .applyToLayer(frostLayer)
    .fromLevels(0, 209).toLevel(0)
    .fromLevels(210, 320).toLevel(1)    // Frost above Y=210
    .go();
```

### 6. Saving or Exporting
Save as a `.world` file for further manual editing:
```javascript
wp.saveWorld(world).toFile("Ashenfall_Continent.world").go();
```
Or export directly into Minecraft save directory:
```javascript
wp.exportWorld(world, "C:/Users/<Username>/AppData/Roaming/.minecraft/saves/Ashenfall");
```

---

## 🎨 WorldPainter Terrain Type Indices

| Index | Name | Minecraft Block Representation |
|:-----:|:-----|:------------------------------|
| `0` | Grass | Minecraft Grass Block with biome tint |
| `1` | Bare Grass | Plain dirt/grass without tall grass foliage |
| `2` | Dirt | Standard Dirt |
| `3` | Permadirt | Rooted dirt / Coarse dirt blend |
| `4` | Podzol | Podzol pine litter |
| `5` | Sand | Standard Sand |
| `6` | Red Sand | Mesa Red Sand |
| `10` | Hardened Clay | Terracotta |
| `27` | Sandstone | Sandstone blocks |
| `28` | Stone | Smooth Stone |
| `29` | Rock | Natural Rock cliff mix |
| `30` | Cobblestone | Weathered Cobblestone |
| `31` | Mossy Cobblestone | Damp ruins / ravine bed |
| `32` | Obsidian | Hardened volcanic caldera glass |
| `34` | Gravel | Gravel riverbed / scree |
| `36` | Beaches | Sand and clay coastal mix |
| `37` | Water | Water source block |
| `38` | Lava | Lava source block |
| `39` | Stone Snow | Rock with snow dusting |
| `40` | Deep Snow | Full snow blocks / Powder snow |
| `70` | Red Sandstone | Badlands Red Sandstone |
| `74` | Stone Mix | Granite, Diorite, Andesite, and Stone blend |
| `100` | Magma | Magma block |

---

## 🖥 Web Studio API Integration

In **WorldStudio** (`http://localhost:3000`), the **WorldPainter API** tab provides:
* **Interactive Parameter Sliders**: Adjust water level, build limits, snow lines, and layer masks.
* **Live Script Code Generation**: Dynamically inspects your settings and outputs JSR223 JavaScript code in real time.
* **1-Click Download**: Generates and serves custom `.js` scripts directly to your browser.
* **Headless Status Checker**: Verifies whether `wpscript` is reachable on the local machine.

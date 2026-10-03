# Ashenfall: Master World Map & Geological Specification
### *Complete Technical Data: Heightmaps, Coordinates, Lithosphere Splines, Climate Gradients & Still Life Population*
**Target Engine:** Minecraft 1.21.1 Java Edition · **Data Pack Format:** 48 · **Canvas:** 8,000 × 8,000 Blocks  
**World:** Continent of Vantyra · **Dependencies:** Lithosphere (v1.3+), Still Life (v0.1+)

---

## 1. Heightmap Data & Elevation Mathematical Specification

The continent of Vantyra operates across Minecraft 1.21.1's extended world height ceiling:
* **Minimum World Height:** $Y = -64$
* **Maximum World Height:** $Y = 320$
* **Total Height Space:** $384$ blocks
* **Mean Sea Level (Water Surface):** $Y = 62$

### 16-Bit uint16 Linear Normalization Equation
Every pixel in the master heightfield maps directly to a discrete block elevation through linear scaling:

$$h_{\text{norm}} = \frac{Y - (-64.0)}{384.0} = \frac{Y + 64.0}{384.0}$$
$$V_{\text{uint16}} = \text{round}(h_{\text{norm}} \times 65535.0)$$
$$Y_{\text{block}} = -64.0 + \left(\frac{V_{\text{uint16}}}{65535.0}\right) \times 384.0$$

### Elevation Keypoints Table

| Geological Feature | Target Y Block | Normalized [0..1] | 16-Bit uint16 | Lithosphere Material / Layer |
| :--- | :---: | :---: | :---: | :--- |
| **Bedrock Floor** | $Y = -64.0$ | $0.0000$ | `0` | Solid Bedrock Floor |
| **Abyssal Trench (Veil of Salt)** | $Y = -32.0 \to 10.0$ | $0.0833 \to 0.1927$ | `5,461` $\to$ `12,629` | Deep Cold Ocean / Gravel |
| **Sunken Caldera Floor** | $Y = 38.0 \to 42.0$ | $0.2656 \to 0.2760$ | `17,406` $\to$ `18,088` | Basalt / Lava Basins / Obsidian |
| **Sunken Reach Drowned Shelf** | $Y = 52.0 \to 56.0$ | $0.3021 \to 0.3125$ | `19,798` $\to$ `20,480` | Warm Ocean Reefs / Sandbars |
| **Mean Sea Level (Water Line)** | **$Y = 62.0$** | **$0.3281$** | **`21,504`** | **Water Surface / Sea Surface** |
| **Forgotten Coast Shoreline** | $Y = 68.0 \to 74.0$ | $0.3438 \to 0.3594$ | `22,532` $\to$ `23,556` | Stony Shore / Cold Pebble Beaches |
| **Gilded Dunes Low Mesas** | $Y = 82.0 \to 96.0$ | $0.3802 \to 0.4167$ | `24,917` $\to$ `27,307` | Terracotta / Red Sandstone |
| **Cogwork March Quarry Benches** | $Y = 85.0 \to 110.0$ | $0.3880 \to 0.4531$ | `25,428` $\to$ `29,695` | Terraced Badlands (9m steps) |
| **Caldera Volcanic Rim** | $Y = 142.0 \to 156.0$ | $0.5365 \to 0.5729$ | `35,158` $\to$ `37,548` | Blackstone / Basalt Spines |
| **Subalpine Taiga Foothills** | $Y = 150.0 \to 190.0$ | $0.5573 \to 0.6615$ | `36,523` $\to$ `43,351` | Podzol / Coarse Dirt (Pine Limit) |
| **Glacial Spine Arêtes & Horns**| $Y = 220.0 \to 279.2$ | $0.7396 \to 0.8938$ | `48,471` $\to$ `58,575` | Frozen Peaks / Blue Glacier Ice |
| **World Build Limit Ceiling** | $Y = 320.0$ | $1.0000$ | `65,535` | Atmospheric Sky Ceiling |

### Continental Shelf Dropoff (Hermite S-Curve Formula)
Beyond the continental shelf radius of $R_{\text{inner}} = 3{,}300$ blocks, terrain descends monotonically into the abyss, reaching maximum ocean depth at $R_{\text{outer}} = 3{,}800$ blocks:

$$t = \text{clamp}\left(\frac{R - 3300.0}{3800.0 - 3300.0}, 0.0, 1.0\right)$$
$$S(t) = 3t^2 - 2t^3 \quad \text{(Continuous Cubic Hermite Spline)}$$
$$H_{\text{drop}}(R) = -600.0 \times S(t) \quad \text{(Plunging into the Veil of Salt)}$$

---

## 2. Landformations & Exact Coordinate Specifications

```
                            [ NORTH: Z = -4000 ]
                     ══════════════════════════════════
                            THE VEIL OF SALT (OCEAN)
                     ══════════════════════════════════
                                    │
                       [ THE SOLITARY GLACIAL SPINE ]
                      (Z = -1500 to -3500, X = -1800 to +1800)
                     Jagged Snow Peaks & Glacial Cirques (Y = 180 - 279)
                                    │
   [ WEST: X = -4000 ]              │              [ EAST: X = +4000 ]
 ══════════════════════             │             ══════════════════════
   THE SUNKEN REACH                 │               THE GILDED DUNES
 (Drowned Port Ostraka)             │              (Al-Qadira Sand Sea)
  Shallow Lagoons & Reefs           │              Rolling Dunes & Terracotta
  X = -2400, Z = +1600              │              X = +2300, Z = 0
            │                       │                       │
            ├─────────────── [ THE CALDERA ] ───────────────┤
            │                  (X = 0, Z = 0)               │
            │           Throne of Melted Obsidian           │
            │          Jagged Volcanic Ring: Y = 146        │
            │           Sunken Crater Floor: Y = 40         │
            │                       │                       │
   [ THE COGWORK MARCH ]            │             [ THE WHISPERING FEN ]
  (Brass Canyons & Terraces)        │             (Deep Bayou & Mangroves)
  Stepped Cliffs & River Gorges     │             Muddy Deltas (Y = 62 - 66)
  X = -2100, Z = 0                  │             X = +2000, Z = +2000
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

### Landmark Coordinates Table

| Landmark Name | Center Coord $(X, Y, Z)$ | Bounding Box $(X_1..X_2, Z_1..Z_2)$ | Target $Y$ | Geological Formation Rules |
| :--- | :---: | :---: | :---: | :--- |
| **1. Forgotten Coast (Spawn)** | `(0, 68, 2500)` | $X: [-600, 600], Z: [2000, 3200]$ | $68 - 74$ | Cold pebble bluffs, rolling wildflower bluffs, stone beacon pier. |
| **2. Cogwork March** | `(-2100, 85, 0)` | $X: [-2800, -1400], Z: [-700, 700]$ | $85 - 110$ | Concentric 9m quarry steps, brass river chasms, Create factory benches. |
| **3. The Ashen Caldera** | `(0, 80, 0)` | $X: [-750, 750], Z: [-750, 750]$ | $38 - 150$ | Volcanic ring wall ($Y=146$), sunken crater basin ($Y=40$), Obsidian Throne ($Y=92$). |
| **4. Solitary Glacial Spine** | `(0, 220, -2500)` | $X: [-1800, 1800], Z: [-3500, -1500]$ | $180 - 279$ | Alpine cordillera, Matterhorn arêtes, cirque tarns, flash-frozen pilgrim trails. |
| **5. The Gilded Dunes** | `(2300, 75, 0)` | $X: [1600, 3100], Z: [-800, 800]$ | $75 - 94$ | Vitrified black-glass dunes, $45^\circ$ barchan ridges, terracotta canyon mesas. |
| **6. The Whispering Fen** | `(2000, 63, 2000)` | $X: [1300, 2700], Z: [1300, 2700]$ | $62 - 66$ | Flat sunken bayous, braided delta channels, giant fungal heartwood trees. |
| **7. The Sunken Reach** | `(-2400, 54, 1600)` | $X: [-3200, -1700], Z: [1000, 2300]$ | $50 - 62$ | Drowned coastal caldera shelf (100 fathoms), coral atolls, barrier sandbars. |
| **8. The Hermit's Spire** | `(-1800, 140, -1800)`| $X: [-2300, -1300], Z: [-2300, -1300]$ | $140 - 185$ | Solitary granite needles, ascetic rope bridges, silent wind-scoured cloisters. |
| **9. The Byzantine Choir** | `(1800, 120, -1800)` | $X: [1300, 2300], Z: [-2300, -1300]$ | $110 - 145$ | Gilded resonant basilicas, pink cherry terraces, harmonic acoustic ruins. |
| **RIM: The Veil of Salt** | $R > 3550$ | Full perimeter to $[-4000, 4000]$ | $-32 - 62$ | Syrupy caustic brine abyss, white salt crusts; space dissolves beyond $4000$. |

---

## 3. Lithosphere Biomes & Density Function Architecture

Lithosphere eliminates stepped contour terracing through 3 continuous cubic spline functions:

1. **`continents.json` (Continentalness $C \in [-1.2, 1.2]$):**
   * $C < -0.20$: Submarine oceanic trenches (`deep_cold_ocean`, `deep_ocean`).
   * $-0.20 \le C \le 0.05$: Coastal bluffs and beaches.
   * $0.05 < C \le 0.60$: Inland fertile lowlands and valleys.
   * $C > 0.60$: High mountain cordilleras.
2. **`erosion.json` (Erosion Detail $E \in [-1.0, 1.0]$):**
   * $E < -0.45$: Low erosion produces jagged alpine arêtes and Matterhorn horns (Solitary Spine).
   * $-0.45 \le E \le 0.25$: Moderate erosion produces terraced plateaus (Cogwork March).
   * $E > 0.25$: High erosion produces flat bayous and floodplains (Whispering Fen).
3. **`ridges.json` (Ridge Lines $R \in [-1.0, 1.0]$):**
   * $R \approx 0$: Carves wide U-shaped glacial river valleys.
   * $|R| \approx 1$: Forms sharp knife-edge crests and arêtes.

---

## 4. Temperature Gradient, Altitude Lapse Rates & Biome Blending

### 5-Tier Climate Banding (Anti-Snow-Pocket Rule)
To eliminate snow pockets from generating in temperate forests, climate zones are separated by **at least $0.55$ temperature units**:

* **Tier 0: Glacial Arctic ($T \le -0.75$):** Glacial Spine summits ($Y > 180$). `frozen_peaks`, `jagged_peaks`, `snowy_slopes`.
* **Tier 1: Boreal Buffer Belt ($-0.60 \le T \le -0.25$):** Mandatory 600-block non-snowy pine taiga buffer.
* **Tier 2: Temperate Lowlands ($-0.15 \le T \le 0.40$):** Forgotten Coast, plains, meadows, oak/birch woodlands.
* **Tier 3: Subtropical Bayou ($0.35 \le T \le 0.60$):** Whispering Fen. Saturated peat, mangrove deltas, warm swamps.
* **Tier 4: Arid & Volcanic ($T \ge 0.70$):** Gilded Dunes and Ashen Caldera. Desert sand seas, terracotta badlands, basalt sinks.

### Atmospheric Altitude Lapse Rate Formula
Temperature decreases linearly with elevation above sea level:
$$T_{\text{eff}}(x, y, z) = T_{\text{base}}(x, z) - 0.0055 \times \max(0.0, y - 62.0)$$

### 5D Multi-Noise Voronoi Metric & Client Blending
Biome placement evaluates Euclidean distance in 5D multi-noise space $(T, H, C, E, W)$:
$$D(\mathbf{P}, \mathbf{B}_i) = \sqrt{(T - T_i)^2 + (H - H_i)^2 + (C - C_i)^2 + (E - E_i)^2 + (W - W_i)^2}$$
Client biome blend radius is set to `4` (9×9 chunk voxel smoothing), eliminating knife-edge biome borders.

---

## 5. Population Instructions: How to Force Still Life to Generate Where Desired

Still Life features (tall branched canopies, fallen birch/oak logs, mossy boulders, and wildflower carpets) are forced through three deterministic methods:

### Method 1: The WorldPainter 'Populate' Layer (100% Guaranteed Native Pass)
1. Generate the binary mask `ASHFALL_POPULATE_MASK.png` (white = fertile valleys, black = bare rock/caldera).
2. In WorldPainter's JSR-223 script:
   ```javascript
   var popMask = wp.getHeightMap().fromFile("worldpainter/ASHFALL_POPULATE_MASK.png").go();
   var popLayer = wp.getLayer().withName("Populate").go();
   wp.applyHeightMap(popMask).toWorld(world).applyToLayer(popLayer).fromLevels(128, 255).toLevel(1).go();
   ```
3. Export the world to `.minecraft/saves`. Chunks with the Populate flag natively trigger Minecraft's `FEATURES` pass, generating Still Life's full placed feature registry.

### Method 2: Still Life Biome Tag Injections (Datapack Level)
In `data/still_life/tags/worldgen/biome/`, add your target biome IDs:
* `has_canopy.json`: `["minecraft:plains", "minecraft:forest", "minecraft:meadow"]`
* `has_fallen_logs.json`: `["minecraft:forest", "minecraft:taiga", "minecraft:old_growth_pine_taiga"]`
* `has_boulders.json`: `["minecraft:windswept_hills", "minecraft:meadow", "minecraft:stony_shore"]`

### Method 3: The Still Life Slope-Aware Surface Rule
Still Life automatically inspects local slope angles $\theta = \arctan(\|\nabla H\|)$:
* **$0^\circ \le \theta < 25^\circ$:** 100% Deep Grass & Soil $\to$ 100% Full Canopy Trees, Fallen Logs, Wildflowers.
* **$25^\circ \le \theta \le 35^\circ$:** Coarse Dirt & Podzol $\to$ 40% Density (Pine taiga, berry bushes).
* **$35^\circ < \theta \le 45^\circ$:** Scree & Gravel $\to$ 5% Density (Mossy boulders only).
* **$\theta > 45^\circ$:** 100% Bare Bedrock & Basalt $\to$ **0% Population (No trees or logs can spawn).**
* **$Y > 225.0$:** Climatic Treeline Cutoff $\to$ **0% Population (Glacial frost and ice only).**
* **Caldera Rim:** Barrenness mask overrides all foliage $\to$ **0% Population.**

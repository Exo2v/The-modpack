# Ashenfall: Lore-Accurate Castles, Towns & Buildings Guide
### *Architectural Directory & Spawning Instructions for Minecraft 1.21.1 NBT Structure Schematics*
**Data Pack Namespace:** `ashenfall` · **Format:** Minecraft 1.21.1 Native NBT Structure (`.nbt`)  
**Download Bundle:** `downloads/ASHENFALL_LORE_SCHEMATICS_BUNDLE.zip` · **WorldPainter Directory:** `worldpainter/structures/`

---

## 1. Overview & Architecture

To populate the continent of Vantyra with lore-accurate landmarks, we have constructed eight genuine Minecraft 1.21.1 `.nbt` structure templates. These schematics can be deployed in three ways:

1. **In-Game Voxel Placement:** Using the native Minecraft `/structure load ashenfall:<name> ~ ~ ~` command.
2. **WorldPainter Custom Object Layers:** Loading the `.nbt` files into WorldPainter to paint or scatter them across designated biomes during continent export.
3. **Worldgen Datapack Integration:** Using Minecraft jigsaw pools to generate them dynamically in custom structures.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 THE SCHEMATIC SUITE                                    │
├─────────────────────────┬──────────────────────────────┬───────────────────────────────┤
│ Realm / Nation          │ Schematic File (.nbt)        │ Architectural Archetype       │
├─────────────────────────┼──────────────────────────────┼───────────────────────────────┤
│ 1. Forgotten Coast      │ grey_frontier_watchtower.nbt │ House Douglas Border Bastion  │
│ 1. Forgotten Coast      │ coastal_fishing_wharf.nbt    │ Stilt Pier & Angler Cottage   │
│ 2. The Sunken Reach     │ drowned_cathedral_spire.nbt  │ Submerged Basilica Belfry     │
│ 4. Solitary Spine       │ glacial_hermit_cloister.nbt  │ Mute Alpine Prayer Sanctuary  │
│ 5. Cogwork March        │ cogwork_steam_foundry.nbt    │ Steampunk Clunker Assembly Bay│
│ 6. Gilded Dunes         │ al_qadira_sunken_bazaar.nbt  │ Domed Sandstone & Slag Vault  │
│ 7. Whispering Fen       │ fen_witch_stilt_dwelling.nbt │ Mycelial Mangrove Stilt Hut   │
│ 9. Ashen Caldera        │ obsidian_imperial_dais.nbt   │ Crucible of Ash Imperial Dais │
└─────────────────────────┴──────────────────────────────┴───────────────────────────────┘
```

---

## 2. Comprehensive Structure Catalog

---

### 1. The Grey Frontier Watchtower (`grey_frontier_watchtower.nbt`)
* **Realm:** *The Forgotten Coast & Grey Frontier (House Douglas)*
* **Target Coordinates:** `(X = 0, Z = +2500)` along coastal roads and frontier trench passes.
* **Dimensions:** $9 \times 17 \times 9$ blocks (Width $\times$ Height $\times$ Length).
* **Lore:** The granite and cracked stone-brick watchtowers of General Douglas's border guard. The arrow slits face inward toward the capital roads to shoot fleeing deserters. Features crenellated battlements, arrow slits, iron-reinforced doors, weapon racks, and an elevated signal brazier.
* **Block Palette:** `minecraft:stone_bricks`, `minecraft:cracked_stone_bricks`, `minecraft:mossy_stone_bricks`, `minecraft:cobblestone`, `minecraft:dark_oak_planks`, `minecraft:iron_bars`, `minecraft:netherrack`, `minecraft:fire`, `minecraft:lantern`.
* **In-Game Command:**
  ```text
  /structure load ashenfall:grey_frontier_watchtower ~ ~ ~
  ```

---

### 2. Coastal Fishing Wharf & Cottage (`coastal_fishing_wharf.nbt`)
* **Realm:** *The Forgotten Coast (Player Awakening Shore)*
* **Target Coordinates:** `(X = 0, Z = +2500)` to `(X = -300, Z = +2800)` along pebble bluffs and waterlines.
* **Dimensions:** $11 \times 9 \times 13$ blocks.
* **Lore:** The weather-beaten stilt piers of the Forgotten Coast where the Tenth Scion awakens. A seaside fisherman's cottage with wooden pylons submerged in water, barrel racks, drying fish racks, cobblestone fireplace, smoking chimney, and spruce shingle roof.
* **Block Palette:** `minecraft:spruce_logs`, `minecraft:spruce_planks`, `minecraft:stripped_spruce_log`, `minecraft:cobblestone`, `minecraft:campfire`, `minecraft:barrel`, `minecraft:chest`, `minecraft:lantern`.
* **In-Game Command:**
  ```text
  /structure load ashenfall:coastal_fishing_wharf ~ ~ ~
  ```

---

### 3. Cogwork Steam Foundry (`cogwork_steam_foundry.nbt`)
* **Realm:** *The Cogwork March (House Vance)*
* **Target Coordinates:** `(X = -2100, Z = 0)` on the 9-block terraced quarry benches.
* **Dimensions:** $13 \times 15 \times 13$ blocks.
* **Lore:** An automated smelting and clunker assembly bay. Built from polished and cut copper, deepslate tiles, and brass pillars. Features a towering exhaust chimney venting steam, blast furnaces, anvil workstations, and grated catwalks where Otto Vance's engineers forged brass automatons.
* **Block Palette:** `minecraft:cut_copper`, `minecraft:deepslate_tiles`, `minecraft:polished_deepslate`, `minecraft:blast_furnace`, `minecraft:anvil`, `minecraft:smithing_table`, `minecraft:iron_bars`, `minecraft:campfire`, `minecraft:soul_lantern`.
* **In-Game Command:**
  ```text
  /structure load ashenfall:cogwork_steam_foundry ~ ~ ~
  ```

---

### 4. The Obsidian Imperial Dais (`obsidian_imperial_dais.nbt`)
* **Realm:** *The Ashen Caldera (The Crucible of Ash)*
* **Target Coordinates:** `(X = 0, Z = 0)` in the center of the volcanic crater.
* **Dimensions:** $13 \times 12 \times 13$ blocks.
* **Lore:** The seat of Emperor Valerius IX in the center of the collapsed volcanic crater. Colonnades of polished basalt and crying obsidian framing an elevated sacrificial dais with magma braziers, blackstone steps, and the throne of melted blades where the Ninth Sound was struck.
* **Block Palette:** `minecraft:polished_basalt`, `minecraft:blackstone`, `minecraft:polished_blackstone_bricks`, `minecraft:crying_obsidian`, `minecraft:obsidian`, `minecraft:magma_block`, `minecraft:soul_fire`, `minecraft:gilded_blackstone`.
* **In-Game Command:**
  ```text
  /structure load ashenfall:obsidian_imperial_dais ~ ~ ~
  ```

---

### 5. Glacial Hermit Cloister (`glacial_hermit_cloister.nbt`)
* **Realm:** *The Solitary Glacial Spine (House Vane)*
* **Target Coordinates:** `(X = 0, Z = -2500)` along razor-sharp alpine arêtes and summits ($Y \ge 200$).
* **Dimensions:** $11 \times 15 \times 11$ blocks.
* **Lore:** The high-altitude stone cells of the mute monks. Built from packed ice, calcite, and smooth basalt, perched on narrow alpine ridges. Contains the cell where initiates took the vow of total silence, a central ice-encased relic shrine, wind-deflecting buttresses, and an ice spire needle.
* **Block Palette:** `minecraft:calcite`, `minecraft:packed_ice`, `minecraft:blue_ice`, `minecraft:smooth_basalt`, `minecraft:diorite`, `minecraft:polished_diorite`, `minecraft:lectern`, `minecraft:soul_lantern`.
* **In-Game Command:**
  ```text
  /structure load ashenfall:glacial_hermit_cloister ~ ~ ~
  ```

---

### 6. Al-Qadira Sunken Bazaar (`al_qadira_sunken_bazaar.nbt`)
* **Realm:** *The Gilded Dunes (House Seljuk)*
* **Target Coordinates:** `(X = +2300, Z = 0)` jutting from the black glass desert dunes.
* **Dimensions:** $13 \times 12 \times 13$ blocks.
* **Lore:** A half-buried desert trading post and netherite slag vault jutting from the black glass sands. Domed sandstone roof, terracotta decorative banding, gold filigree accents, iron bar treasury cages, and market stalls.
* **Block Palette:** `minecraft:red_sandstone`, `minecraft:cut_red_sandstone`, `minecraft:orange_terracotta`, `minecraft:yellow_terracotta`, `minecraft:gold_block`, `minecraft:iron_bars`, `minecraft:barrel`, `minecraft:chest`.
* **In-Game Command:**
  ```text
  /structure load ashenfall:al_qadira_sunken_bazaar ~ ~ ~
  ```

---

### 7. Fen Witch Stilt Dwelling (`fen_witch_stilt_dwelling.nbt`)
* **Realm:** *The Whispering Fen (House Belen)*
* **Target Coordinates:** `(X = +2000, Z = +2000)` in murky mangrove bayous.
* **Dimensions:** $11 \times 12 \times 11$ blocks.
* **Lore:** The swamp dwellings of the Mycelial Covenant, raised six blocks above stagnant water on petrified mangrove stilts. Features thatched mushroom roofs, brewing cauldrons, mushroom compost beds, hanging botanical vines, and an access ladder.
* **Block Palette:** `minecraft:stripped_mangrove_wood`, `minecraft:mangrove_planks`, `minecraft:mud_bricks`, `minecraft:brown_mushroom_block`, `minecraft:red_mushroom_block`, `minecraft:cauldron`, `minecraft:brewing_stand`, `minecraft:vine`.
* **In-Game Command:**
  ```text
  /structure load ashenfall:fen_witch_stilt_dwelling ~ ~ ~
  ```

---

### 8. Drowned Cathedral Spire (`drowned_cathedral_spire.nbt`)
* **Realm:** *The Sunken Reach (Port Ostraka)*
* **Target Coordinates:** `(X = -2400, Z = +1600)` submerged in coastal waters.
* **Dimensions:** $11 \times 18 \times 11$ blocks.
* **Lore:** The submerged upper bell tower of the Grand Basilica of Port Ostraka projecting from shallow coastal waters. Weathered prismarine arches, waterlogged quartz belfry, the holy bronze bell, sea lanterns, and hanging kelp.
* **Block Palette:** `minecraft:prismarine_bricks`, `minecraft:dark_prismarine`, `minecraft:smooth_quartz`, `minecraft:bell`, `minecraft:gold_block`, `minecraft:sea_lantern`, `minecraft:water`.
* **In-Game Command:**
  ```text
  /structure load ashenfall:drowned_cathedral_spire ~ ~ ~
  ```

---

## 3. How to Import Schematics into WorldPainter (Custom Object Layers)

To scatter these buildings across your world automatically during WorldPainter generation:

1. **Locate the Schematics:**  
   The `.nbt` files are saved in `worldpainter/structures/` (or extract `downloads/ASHENFALL_LORE_SCHEMATICS_BUNDLE.zip`).
2. **Open WorldPainter:**  
   Open your `Ashfall_Continent.world` project.
3. **Create a Custom Object Layer:**  
   - In the **Layers** panel on the left, click the **`+`** icon ➔ select **`Add a custom object layer...`**
   - Click **`Add`** and browse to `worldpainter/structures/`.
   - Select the desired `.nbt` file (e.g., `grey_frontier_watchtower.nbt`).
4. **Configure Spawn Rules:**
   - **Density:** Set spawn frequency (e.g., `0.5%` to `2.0%` for watchtowers).
   - **Collision:** Check *"Extend downwards"* so foundations bury into slopes.
   - **Slope Filter:** Set slope limit to `0° to 25°` to prevent structures floating on vertical cliffs.
5. **Paint or Automate:**  
   Paint the layer over designated landmarks, or bind it directly in the automated JSR-223 script!

# ASHENFALL — Complete Mod Catalog

**Minecraft 1.21.1 · NeoForge 21.1.65**  
Single Source of Truth: `tools/modlist.toml`

---

## Mod Budget Audit
- **Content Mods**: 94 / 130 max (✅ PASS)
- **Performance / Utility**: 15 / 18 max (✅ PASS)
- **Core Libraries**: 10 / 20 max (✅ PASS)
- **Total Active Stack**: 119 mods

---

## 1. Performance & Engine (Phase M0)

| Mod | Slug | Provider | Side | Role |
| :--- | :--- | :--- | :--- | :--- |
| **Embeddium** | `embeddium` | Modrinth | Client | Core rendering optimization engine for NeoForge |
| **Embeddium Extra** | `embeddium-extra` | Modrinth | Client | Extended graphical toggles and options |
| **ModernFix** | `modernfix` | Modrinth | Both | Dynamic resource loading and memory leak fixes |
| **FerriteCore** | `ferrite-core` | Modrinth | Both | Memory reduction for blockstates and models |
| **ImmediatelyFast** | `immediatelyfast` | Modrinth | Client | HUD & GUI render batching engine |
| **Entity Culling** | `entityculling` | Modrinth | Client | Skips rendering entities obscured by walls |
| **Clumps** | `clumps` | Modrinth | Both | Consolidates XP orbs into single entities |
| **Alternate Current** | `alternate-current` | Modrinth | Both | High-performance redstone computation |
| **Enhanced Block Entities** | `enhanced-block-entities` | Modrinth | Client | Optimizes chest and sign rendering |
| **FastSuite** | `fastsuite` | Modrinth | Both | Speeds up recipe lookup queries |
| **More Culling** | `moreculling` | Modrinth | Client | Additional face culling for performance |
| **Structure Layout Optimizer** | `structure-layout-optimizer` | Modrinth | Both | Reduces structure generation CPU spikes |
| **Dynamic FPS** | `dynamic-fps` | Modrinth | Client | Reduces render rate when window is unfocused |
| **Acedium Sodiumized** | `acedium-sodiumized` | CurseForge | Client | NeoForge Nvidium port for NVIDIA mesh shaders |
| **Chunky** | `chunky` | Modrinth | Both | Pre-generates terrain to eliminate in-game lag |

---

## 2. Core Libraries (Phase M0)

| Mod | Slug | Provider | Side | Role |
| :--- | :--- | :--- | :--- | :--- |
| **Curios API** | `curios` | Modrinth | Both | Accessory and equipment slot framework |
| **Lionfish API** | `lionfish-api` | Modrinth | Both | Animation library for L_Ender's Cataclysm |
| **Citadel** | `citadel` | Modrinth | Both | Animation backend for Alex's Caves and Alex's Mobs |
| **Patchouli** | `patchouli` | Modrinth | Both | In-game guidebook engine for Pilgrim's Journal |
| **Architectury API** | `architectury-api` | Modrinth | Both | Cross-platform mod abstraction layer |
| **Kotlin for Forge** | `kotlin-for-forge` | Modrinth | Both | Kotlin language runtime |
| **TerraBlender** | `terrablender` | Modrinth | Both | Biome blending backend for Terralith |
| **Player Animator** | `playeranimator` | Modrinth | Client | Dynamic combat and parkour player animations |
| **YUNG's API** | `yungs-api` | Modrinth | Both | Structure generator for YUNG's Better series |
| **Sophisticated Core** | `sophisticated-core` | Modrinth | Both | Core storage backend for Sophisticated Backpacks |

---

## 3. Movement & Combat (Phase M1)

| Mod | Slug | Provider | Side | Role |
| :--- | :--- | :--- | :--- | :--- |
| **Backported Spears** | `backported-spears` | Modrinth | Both | Jab, speed-scaled charge damage, Lunge dash |
| **Combat Roll** | `combat-roll` | Modrinth | Both | Dodge roll with invulnerability frames |
| **ParCool** | `parcool` | Modrinth | Both | Parkour vaulting, wall-runs, ledge-grabs |
| **ParCool+ Compatibility++** | `parcool-compatibility-addon` | CurseForge | Client | Animation compatibility layer |
| **GhostSwap** | `ghostswap` | Custom | Both | In-house 1-tick weapon attribute swapping |
| **Simply Swords** | `simply-swords` | Modrinth | Both | Glaives, katanas, greathammers, twinblades |
| **Spartan Weaponry** | `spartan-weaponry` | CurseForge | Both | Polearms, throwing knives, heavy crossbows |

---

## 4. Soulslike & Difficulty (Phase M2)

| Mod | Slug | Provider | Side | Role |
| :--- | :--- | :--- | :--- | :--- |
| **Silent's Power Scale** | `power-scale` | Modrinth | Both | Distance/progression scaling for mobs and player |
| **GraveStone Mod** | `gravestone-mod` | Modrinth | Both | Death recovery run mechanic |

---

## 5. World Generation & Landmarks (Phase M3)

| Mod | Slug | Provider | Side | Role |
| :--- | :--- | :--- | :--- | :--- |
| **Terralith** | `terralith` | Modrinth | Both | Overworld landmark terrain and 95+ biomes |
| **Explorify** | `explorify` | Modrinth | Both | Ambient ruins, watchtowers, surface dungeons |
| **Dungeons and Taverns** | `dungeons-and-taverns` | Modrinth | Both | Roadside taverns and multi-level dungeons |
| **Towns and Towers** | `towns-and-towers` | Modrinth | Both | Fortified imperial towns, outposts, towers |
| **When Dungeons Arise** | `when-dungeons-arise` | Modrinth | Both | Colossal flying fortresses and temples |

---

## 6. World Fullness, Ecology & Water (Phase M3b)

| Mod | Slug | Provider | Side | Role |
| :--- | :--- | :--- | :--- | :--- |
| **FallingTree** | `falling-tree` | Modrinth | Both | Tree felling scaled by Woodcutting level |
| **Sophisticated Backpacks**| `sophisticated-backpacks`| Modrinth | Both | Progression-gated backpacks and upgrades |
| **Star Worm Equestrian** | `swem` | CurseForge | Both | Realistic horse breeds, gaits, mounted combat |
| **Guard Villagers** | `guard-villagers` | Modrinth | Both | Village defense patrols and raid events |
| **Farmer's Delight** | `farmers-delight` | Modrinth | Both | Cooking, culinary buffs, nutrition |
| **Supplementaries** | `supplementaries` | Modrinth | Both | Vanilla+ utility, urns, sconces, lanterns |
| **Comforts** | `comforts` | Modrinth | Both | Sleeping bags and bonfires to restore Flask |
| **Tool Belt** | `tool-belt` | Modrinth | Both | Radial hotbar tool swapper |
| **Dynamic Waters** | `dynamic-waters` | CurseForge | Both | Flowing river currents that guide travel |
| **Flowing Fluids** | `flowing-fluids` | CurseForge | Both | Downhill water pressure physics |
| **Boatload** | `boatload` | Modrinth | Both | Large cargo sailing craft |

---

## 7. Dungeons & Forbidden Magic (Phase M3c)

| Mod | Slug | Provider | Side | Role |
| :--- | :--- | :--- | :--- | :--- |
| **YUNG's Suite (×11)** | `yungs-better-*` | Modrinth | Both | Complete overhaul of vanilla dungeons/structures |
| **Repurposed Structures** | `repurposed-structures` | Modrinth | Both | Displacement scar biome variants |
| **Hopo Better Portals/Ruins**| `hopo-better-*` | Modrinth | Both | Atmospheric planar gateways and ruins |
| **The Graveyard** | `the-graveyard` | Modrinth | Both | Mausoleums, Lich Prison, Lich's Bargain |
| **Structory** | `structory` | Modrinth | Both | Settlements, cottages, and ruins |
| **Dimensional Dungeons** | `dimensional-dungeons` | CurseForge | Both | Procedural dungeon dimension |
| **Iron's Spells 'n Spellbooks** | `irons-spells-n-spellbooks` | Modrinth | Both | 9 spell schools, mana, Arcane Anvil weapon imbue |
| **Monsters & Spellbooks** | `monsters-and-spellbooks` | CurseForge | Both | 10th Necromancy school, curses, and dark summons |

---

## 8. Nations & Factions (Phase M4)

| Mod | Slug | Provider | Side | Role |
| :--- | :--- | :--- | :--- | :--- |
| **Millénaire** | `millenaire` | CurseForge | Both | 7 living cultures (Normans, Seljuks, etc.) |
| **Aviel's Dialogue Mod** | `aviels-dialogue-mod` | CurseForge | Both | Branching conversations with named NPCs |
| **FTB Quests** | `ftb-quests-forge` | CurseForge | Both | Chapters 0–8 narrative and quest chains |
| **FTB Teams** | `ftb-teams` | CurseForge | Both | Party and faction coordination |
| **FTB Chunks** | `ftb-chunks` | CurseForge | Both | Territory protection |
| **KubeJS** | `kubejs` | Modrinth | Both | Custom standing logic and Ember Flask script |

---

## 9. RPG Progression & Grinding (Phase M5)

| Mod | Slug | Provider | Side | Role |
| :--- | :--- | :--- | :--- | :--- |
| **Project MMO (+ Classes/Books/XP)** | `project-mmo*` | Modrinth | Both | Complete skill leveling, 5 pilgrim classes, loot |
| **Origins (+ Classes)** | `origins*` | Modrinth | Both | Heritage traits and vocational perks |
| **Mob Grinding Utils** | `mob-grinding-utils` | CurseForge | Both | Material grinding and mob farm automation |
| **Reforged** | `tiered` | Modrinth | Both | Gear affix modifiers and anvil rerolling |
| **Attribute Modify** | `attribute-modify` | Modrinth | Both | Datapack attribute scaling |
| **Mob Champions** | `mob-champions` | Modrinth | Both | 4 champion tiers with unique loot beams |
| **Loot Beams: Refork** | `loot-beams` | Modrinth | Client | Vertical rarity beams matching Reforged tiers |

---

## 10. Boss Spine & Sensory Feedback (Phase M6)

| Mod | Slug | Provider | Side | Role |
| :--- | :--- | :--- | :--- | :--- |
| **L_Ender's Cataclysm** | `cataclysm` | Modrinth | Both | The 8 core two-phase titans |
| **Bosses of Mass Destruction** | `bosses-of-mass-destruction` | CurseForge | Both | Multi-phase dungeon bosses |
| **The Twilight Forest** | `the-twilight-forest` | CurseForge | Both | Act II pilgrimage realm |
| **The Aether** | `aether` | Modrinth | Both | Sky realm & ancient Ember Forge source |
| **Deeper and Darker** | `deeperdarker` | CurseForge | Both | The Otherside void dimension |
| **Alex's Caves & Mobs** | `alexs-caves` / `alexs-mobs` | Modrinth | Both | Subterranean biomes and wildlife |
| **Mini-boss Boss Bars** | `mini-boss-boss-bars` | Modrinth | Client | Health bars for regional elites |
| **Configurable Boss Bars** | `configurable-boss-bars` | Modrinth | Client | Souls-style unified boss bars |
| **Boss Music Mod** | `boss-music-mod` | Modrinth | Client | Adaptive boss battle music |
| **Floating Damage Indicators** | `floating-damage-indicators`| Modrinth | Client | Color-coded damage numbers |
| **YUNG's Traveler's Titles** | `yungs-travelers-titles` | Modrinth | Client | Souls-style region banner titles |

---

## 11. Navigation & QoL (Phase M7)

| Mod | Slug | Provider | Side | Role |
| :--- | :--- | :--- | :--- | :--- |
| **Explorer's & Nature's Compass** | `explorers-compass` | CurseForge | Both | Biome and landmark navigation |
| **Lootr** | `lootr` | Modrinth | Both | Instanced per-player dungeon chests |
| **Artifacts** | `artifacts` | CurseForge | Both | ~20 unique curios trinkets |
| **Enigmatic Legacy+** | `enigmatic-legacy-plus` | Modrinth | Both | Endgame relics and cursed scrolls |
| **Waystones & Fast Travel** | `waystones` | Modrinth | Both | Highway waystone network |
| **JEI, Jade, AppleSkin** | `jei`, `jade`, `appleskin`| Modrinth | Client | Essential recipe & status inspectors |
| **Xaero's World Map & Minimap** | `xaeros-*` | Modrinth | Client | Detailed atlas of Vantyra |
| **Mouse Tweaks & Controlling** | `mouse-tweaks`, `controlling` | Modrinth | Client | Inventory & keybind management |

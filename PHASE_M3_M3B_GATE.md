# Ashenfall — Phase M3 & M3b Gate Documentation (World Generation & World Fullness)

**Milestones**: 
- **Phase M3**: World Generation & Landmarks (The World's Shape)
- **Phase M3b**: World Fullness, Ecology, Camps & Storage (Life & Utility)  
**Target Loader**: Minecraft 1.21.1 · NeoForge 21.1.x  

---

## 1. Overview & Cumulative Scope (47 Mods Total)

Phase M3 & M3b build upon the verified Phase M0 performance engine and Phase M1/M2 Vanilla PvP and soulslike combat foundation by overhauling the Overworld terrain, dungeons, villages, cooking, backpacks, and exploration mechanics.

### Phase M0 (Skeleton & Performance Engine — 24 Mods)
- Embeddium, Embeddium Extra, ModernFix, FerriteCore, ImmediatelyFast, Entity Culling, Clumps, Alternate Current, FastSuite, More Culling, Dynamic FPS, Chunky, Curios API, Citadel, Patchouli, Architectury API, Kotlin for Forge, TerraBlender, Player Animator, YUNG's API, Sophisticated Core, Lionfish API

### Phase M1 & M2 (Movement, Pure Vanilla PvP & Soulslike — 10 Mods)
- Combat Roll, Cloth Config API, ParCool, Simply Swords, Fzzy Config, Oracle Index, Backported Spears, Silent Lib, Silent's Power Scale, GraveStone Mod (No Better Combat; pure Vanilla PvP mechanics)

### Phase M3 (World Generation & Landmarks — 4 Mods)
- **Terralith** (`terralith`): 95+ realistic and fantasy biomes, natural landforms (canyons, volcanic peaks, jagged ridges, alpine meadows) using purely vanilla blocks.
- **Explorify** (`explorify`): Ambient vanilla-friendly structures, shrines, watchtowers, and underground ruins.
- **Dungeons and Taverns** (`dungeons-and-taverns`): Roadside inns/taverns, multi-level dungeon complexes, and frontier outposts.
- **Towns and Towers** (`towns-and-towers`): Fortified imperial villages, pillager garrisons, and coastal seafaring vessels.

### Phase M3b (World Fullness, Living World & Utility — 9 Mods)
- **FallingTree** (`fallingtree`): Timber physics allowing clean felling of whole trees by breaking the base block (sneak to disable).
- **Sophisticated Backpacks** (`sophisticated-backpacks`): Wearable backpacks with Curios integration, upgrade slots (smelting, auto-pickup, magnet, feeding), and color dyeing.
- **Guard Villagers** (`guard-villagers`): Village militia armed with swords and crossbows that defend settlements from illager raids and zombies.
- **Farmer's Delight** (`farmers-delight`): Culinary expansion with cooking pots, skillets, knives, new crops (cabbage, tomato, onion, rice), and nutrition meals.
- **Moonlight Lib** (`moonlight`): Companion library required by Supplementaries.
- **Supplementaries** (`supplementaries`): Sconces, lanterns, signposts, urns, hanging flower pots, rope, faucets, and decorative utility.
- **Comforts** (`comforts`): Sleeping bags (sleep anywhere in the wild to pass the night without resetting your world spawn) and hammocks.
- **Tool Belt** (`traveler-tool-belt`): Radial hotbar quick-swap tool belt worn in the Curios belt slot.
- **Boatload** (`boatload`): Large sailing boats, boats with chests, furnaces, and banners for seafaring exploration.

---

## 2. In-Game Controls & Features

| Action / Feature | Hotkey / Interaction | Mod Source | Notes |
| :--- | :--- | :--- | :--- |
| **Open Backpack** | `B` (configurable) | Sophisticated Backpacks | Opens worn backpack directly |
| **Tool Belt Radial** | `R` / Configurable key | Tool Belt | Quick-swaps hotbar tools |
| **Sleep in Wild** | Right-click Sleeping Bag | Comforts | Skips night without clearing bed spawn point |
| **Fell Whole Tree** | Mine lowest log block | FallingTree | Sneak (`Shift`) to mine only 1 log |
| **Cook Hearty Meal** | Cooking Pot over fire/heat | Farmer's Delight | Stews, roast chicken, pasta dishes |
| **Hire Guard Villager** | Shift + Right-click Guard | Guard Villagers | Equip armor/weapons to customize guards |
| **Dodge Roll** | `R` or `Left Alt` | Combat Roll | Invulnerability frames |
| **Parkour Vault / Climb** | `Space` while sprinting | ParCool | Vaults over 1-2 block walls |
| **Slide** | `Left Ctrl` while sprinting | ParCool | Slides under 1-block passages |
| **ParCool Settings** | `Alt + P` | ParCool | Parkour configuration menu |

---

## 3. In-Game Gate Verification Checklist

1. **Clean Boot**: NeoForge 1.21.1 launches with 0 crashes (`Mods: 48 loaded`).
2. **World Generation**: Creating a new singleplayer world generates Terralith terrain with custom biomes and structures.
3. **Villages & Guards**: Villages spawn with armored Guard Villagers patrolling the borders.
4. **Backpack Crafting**: Crafting a Leather Backpack and wearing it in the Curios slot opens with keybind `B`.
5. **Cooking System**: Cooking pot places above heat source and accepts ingredients into stew recipes.
6. **Sleeping Bag Rest**: Using a sleeping bag during nighttime advances to sunrise without changing respawn point.
7. **Timber Tree Cut**: Chopping an oak tree fells all connected logs into item drops.

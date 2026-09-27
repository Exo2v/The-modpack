# Ashenfall — Phase M1 & M2 Gate Documentation

**Milestones**: 
- **Phase M1**: Movement & Combat Layer
- **Phase M2**: Soulslike Difficulty & Recovery Layer  
**Target Loader**: Minecraft 1.21.1 · NeoForge 21.1.x  

---

## 1. Scope & Installed Mods (Cumulative M0 + M1 + M2)

### Phase M0 (Skeleton & Performance Engine — 24 Mods)
- **Performance Engine**: Embeddium, Embeddium Extra, ModernFix, FerriteCore, ImmediatelyFast, Entity Culling, Clumps, Alternate Current, FastSuite, More Culling, Dynamic FPS, Chunky
- **Core APIs & Libraries**: Curios API, Citadel, Patchouli, Architectury API, Kotlin for Forge, TerraBlender, Player Animator, YUNG's API, Sophisticated Core, Lionfish API

### Phase M1 (Movement & Combat Layer — 8 Mods)
- **Better Combat** (`better-combat`): Dynamic melee weapon attack animations, sweeping strike combos, dual-wielding, and weapon hitboxes.
- **Cloth Config API** (`cloth-config`): Configuration framework for Better Combat & Combat Roll.
- **Combat Roll** (`combat-roll`): Dedicated dodge roll mechanic with configurable invulnerability frames (i-frames) and stamina cost.
- **ParCool** (`parcool`): Complete parkour movement system (ledge grabs, wall-running, vaulting over obstacles, sliding, cat leaps, diving).
- **Simply Swords** (`simply-swords`): 14+ new weapon archetypes (Glaives, Katanas, Greathammers, Twinblades, Rapiers, Halberds, Spears).
- **Fzzy Config** (`fzzy-config`): Configuration and GUI framework required by Simply Swords.
- **Oracle Index** (`oracle-index`): In-game documentation and weapon mastery encyclopedia for Simply Swords.
- **Backported Spears** (`backported-spears`): Spear jab attacks, velocity-scaled charge damage, and lunge mechanics integrated with Better Combat.

### Phase M2 (Soulslike & Difficulty Scaling — 3 Mods)
- **Silent Lib** (`silent-lib`): Core backend library for Power Scale.
- **Silent's Power Scale** (`silents-power-scale`): Attribute-based mob and player difficulty scaling. Mobs scale in health, attack power, and speed as the player explores further from spawn and gains levels.
- **GraveStone Mod / Corpse** (`gravestone-mod`): Spawns a grave marker at the point of death holding the player's full inventory, enabling soulslike corpse run recovery.

---

## 2. In-Game Controls & Keybinds

| Action | Default Keybind | Mod Source | Notes |
| :--- | :--- | :--- | :--- |
| **Dodge Roll** | `R` or `Left Alt` | Combat Roll | Grants i-frames during mid-roll animation |
| **Parkour Vault / Climb** | `Space` while sprinting | ParCool | Automatically vaults over 1-2 block obstacles |
| **Slide** | `Left Control` while sprinting | ParCool | Slides under 1-block gaps |
| **Wall Run** | Run diagonally into wall | ParCool | Wall-runs along flat vertical surfaces |
| **ParCool Settings** | `Alt + P` | ParCool | Customize parkour moves, stamina, and keybinds |
| **Weapon Attack Combo** | `Left Click` | Better Combat | Triggers multi-hit animated weapon swings |
| **Spear Lunge** | `Sneak + Right Click` | Backported Spears | Thrusts forward with spear |
| **Weapon Mastery Guide** | Open Inventory / Oracle | Oracle Index | In-game guide for Simply Swords mechanics |

---

## 3. In-Game Verification Checklist

1. **Clean Boot**: NeoForge 1.21.1 launches to title screen with 0 crashes (`Mods: 35 loaded`).
2. **Combat Animations**: Holding a sword or spear produces dynamic animated swings and particle trails upon left-clicking.
3. **Dodge Roll**: Pressing `R` executes a roll animation with recovery cooldown.
4. **Parkour Mobility**: Sprinting toward an obstacle triggers fluid vaulting and ledge climbing.
5. **Simply Swords Loot/Crafting**: Glaives, rapiers, and katanas appear in creative tabs and recipes.
6. **Death Grave Recovery**: Dying spawns a grave marker that cleanly restores inventory on retrieval.
7. **Mob Difficulty Scaling**: Hostile mobs spawn with scaled HP and attributes corresponding to distance.

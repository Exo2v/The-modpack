# ASHENFALL — 1-Minute Installation Guide

**Minecraft Version**: `1.21.1`  
**Mod Loader**: `NeoForge 21.1.65`  
**Allocated RAM**: `6 GB` minimum, `8 GB` recommended  

---

## Option 1: Prism Launcher / ATLauncher (Recommended)

1. Open **Prism Launcher** (or ATLauncher).
2. Click **Add Instance** (top left).
3. Select **Import** on the left menu.
4. Drag and drop **`ashfall-0.1.0.mrpack`** into the window (or click Browse and select it).
5. Click **OK**.
6. Prism will automatically create the instance, configure Minecraft `1.21.1`, install `NeoForge 21.1.65`, download the verified mods, and apply all configs.
7. Click **Launch** and enjoy!

---

## Option 2: Modrinth App

1. Open the **Modrinth App**.
2. Click the **+** (Add Instance) button on the left sidebar.
3. Select **Import from file**.
4. Choose **`ashfall-0.1.0.mrpack`**.
5. The Modrinth App will build the profile and download all mods.
6. Click **Play**!

---

## Option 3: CurseForge App

1. Open the **CurseForge App**.
2. Go to the Minecraft tab.
3. Click the **Create Custom Profile** button (or the three dots menu next to it).
4. Select **Import a previously exported profile**.
5. Choose **`ashfall-0.1.0-curseforge.zip`**.
6. CurseForge will automatically install the modpack profile and dependencies.

---

## Performance & GPU Profiles

Inside the `profiles/` folder, three hardware profiles are configured:

1. **`performance.toml` (NVIDIA GTX 1600+ / RTX 20xx+)**:
   - Enables `Acedium Sodiumized` (mesh shaders) and aggressive occlusion culling.
   - Recommended for high render distance (12–24 chunks).

2. **`compat.toml` (AMD / Intel / Older GPUs)**:
   - Uses stock `Embeddium` without mesh shader requirements.

3. **`magic.toml` (Stability testing)**:
   - Disables the experimental `Monsters & Spellbooks` Necromancy addon if troubleshooting.

---

## Default Controls & Combat Keybinds

- **Dodge Roll**: `R` or `Alt` (Combat Roll with i-frames)
- **Parkour Movements**: Sprint + Jump for vaults; wall-running activated along flat surfaces (ParCool)
- **Spear Lunge**: Sneak + Right Click with spear
- **Spear Charge**: Mount horse or run at top speed; damage scales with velocity
- **Attribute Swap**: `G` (GhostSwap instant weapon attribute swap)
- **Rest & Refill Flask**: Sleep in a hammock/sleeping bag or rest near a Waystone bonfire

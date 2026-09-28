# PHASE M0: Skeleton & Performance Baseline

**Status**: Ready for Verification Gate  
**Target Engine**: Minecraft `1.21.1` · NeoForge `21.1.65`  
**Phase Objective**: Can the game boot clean and sustain 60+ FPS with zero content mods?

---

## 1. Phase M0 Deliverables

In accordance with `PHASES.pdf §M0`, **no content mods are present in this build**. Only the performance engine and core library prerequisites are loaded:

### Performance & Engine Stack (15 mods — Budget Cap $\le 18$)
1. **Embeddium**: Primary rendering optimization
2. **Embeddium Extra**: Additional graphical controls
3. **ModernFix**: Fast resource loading & memory leak mitigation
4. **FerriteCore**: Model & blockstate memory reduction
5. **ImmediatelyFast**: Screen & HUD batch rendering
6. **Entity Culling**: Frustum & occlusion entity culling
7. **Clumps**: Consolidates XP orbs into single entities
8. **Alternate Current**: Fast redstone computation
9. **Enhanced Block Entities**: Optimized chest & sign block entity rendering
10. **FastSuite**: Recipe lookup performance boost
11. **More Culling**: Block face culling optimization
12. **Structure Layout Optimizer**: Memory-efficient structure generation
13. **Dynamic FPS**: Idle render-rate throttling
14. **Acedium Sodiumized**: Mesh shader acceleration (NVIDIA) with Embeddium fallback
15. **Chunky**: Terrain pre-generation engine

### Core Libraries (10 mods — Budget Cap $\le 20$)
- `curios`, `lionfish-api`, `citadel`, `patchouli`, `architectury-api`, `kotlin-for-forge`, `terrablender`, `playeranimator`, `yungs-api`, `sophisticated-core`

---

## 2. Direct Downloads for Phase M0

| Package | Format | Direct Download Link |
| :--- | :--- | :--- |
| **M0 Modrinth Package** (Recommended) | `.mrpack` | [Download `ashfall-0.1.0-M0.mrpack`](https://github.com/Exo2v/The-modpack/raw/arena/01a0e180-the-modpack/downloads/ashfall-0.1.0-M0.mrpack) |
| **M0 CurseForge Package** | `.zip` | [Download `ashfall-0.1.0-M0-curseforge.zip`](https://github.com/Exo2v/The-modpack/raw/arena/01a0e180-the-modpack/downloads/ashfall-0.1.0-M0-curseforge.zip) |
| **M0 Complete Bundle** | `.zip` | [Download `ashfall-0.1.0-M0-complete-bundle.zip`](https://github.com/Exo2v/The-modpack/raw/arena/01a0e180-the-modpack/downloads/ashfall-0.1.0-M0-complete-bundle.zip) |

---

## 3. Phase M0 Gate Verification Checklist

Before advancing to **Phase M1 (Movement & Combat)**, each numbered gate test must be verified in-game:

- [ ] **Gate 1: Cold Boot**: Clean launch, no JVM crash, no mixin errors in `latest.log`.
- [ ] **Gate 2: Frame Rate Baseline**: Steady **60+ FPS** at render distance 10–12 in a vanilla test world.
- [ ] **Gate 3: GUI Batching**: Verify `ImmediatelyFast` screen batching does not glitch any container or JEI screen.
- [ ] **Gate 4: GPU Profile & Mesh Shaders**: 
  - NVIDIA users: verify `Acedium Sodiumized` activates in video settings.
  - Non-NVIDIA users: verify `profiles/compat.toml` loads stock Embeddium cleanly.
- [ ] **Gate 5: Memory Allocation**: Allocate 6 GB RAM; observe F3 debug screen for memory stabilization without GC freezes.

---

## 4. Next Step: Phase M1 (Movement & Combat)

Once you verify the M0 baseline, we unlock:
- **Backported Spears** (jab, charge damage scaling with speed, Lunge dash)
- **Combat Roll** (i-frame dodge roll)
- **ParCool** (vaulting, ledge grabbing, wall running)
- **GhostSwap** (1-tick attribute swapping on key `G`)
- **Simply Swords** & **Spartan Weaponry** (weapons catalog pass)

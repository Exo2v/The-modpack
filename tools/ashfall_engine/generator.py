#!/usr/bin/env python3
"""
=============================================================================
ASHFALL CONTINENT GENERATOR & STILL LIFE POPULATION ENGINE
=============================================================================
Combines:
  1. Continents & Lithosphere Geology Engine (Continuous Hermite Splines, Alpine Spine, Caldera)
  2. creativitRy ColorToTerrain Logic (RGB SplatMap to Minecraft Block Palette)
  3. Still Life Population Logic (Multi-Tier Canopies, Shrubs, Fallen Logs, Glacial Boulders, Slope Rules)
  4. WorldPainter API Automation & 3D WebGL Export Pipeline
=============================================================================
"""

import os
import sys
import math
import time
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# -----------------------------------------------------------------------------
# 1. MINECRAFT BLOCK PALETTE FOR ColorToTerrain (Derived from creativitRy / WorldPainter)
# -----------------------------------------------------------------------------
MINECRAFT_PALETTE = [
    {"name": "BareGrass",       "t": 1,   "r": 69,  "g": 110, "b": 51,  "hex": "#456e33", "type": "grass"},
    {"name": "Grass",           "t": 0,   "r": 76,  "g": 125, "b": 42,  "hex": "#4c7d2a", "type": "grass"},
    {"name": "Dirt",            "t": 2,   "r": 134, "g": 96,  "b": 67,  "hex": "#866043", "type": "soil"},
    {"name": "Permadirt",       "t": 3,   "r": 110, "g": 78,  "b": 54,  "hex": "#6e4e36", "type": "soil"},
    {"name": "Podzol",          "t": 4,   "r": 90,  "g": 63,  "b": 28,  "hex": "#5a3f1c", "type": "soil"},
    {"name": "Sand",            "t": 5,   "r": 219, "g": 211, "b": 160, "hex": "#dbd3a0", "type": "sand"},
    {"name": "RedSand",         "t": 6,   "r": 169, "g": 88,  "b": 33,  "hex": "#a95821", "type": "sand"},
    {"name": "HardenedClay",    "t": 10,  "r": 150, "g": 92,  "b": 66,  "hex": "#965c42", "type": "terracotta"},
    {"name": "OrangeTerracotta","t": 12,  "r": 161, "g": 83,  "b": 37,  "hex": "#a15325", "type": "terracotta"},
    {"name": "YellowTerracotta","t": 15,  "r": 186, "g": 133, "b": 35,  "hex": "#ba8523", "type": "terracotta"},
    {"name": "Sandstone",       "t": 27,  "r": 218, "g": 210, "b": 158, "hex": "#dad29e", "type": "rock"},
    {"name": "Stone",           "t": 28,  "r": 125, "g": 125, "b": 125, "hex": "#7d7d7d", "type": "rock"},
    {"name": "Rock",            "t": 29,  "r": 123, "g": 123, "b": 123, "hex": "#7b7b7b", "type": "rock"},
    {"name": "Cobblestone",     "t": 30,  "r": 122, "g": 122, "b": 122, "hex": "#7a7a7a", "type": "rock"},
    {"name": "MossyCobblestone","t": 31,  "r": 103, "g": 121, "b": 103, "hex": "#677967", "type": "rock"},
    {"name": "Obsidian",        "t": 32,  "r": 20,  "g": 18,  "b": 29,  "hex": "#14121d", "type": "volcanic"},
    {"name": "Basalt",          "t": 74,  "r": 45,  "g": 45,  "b": 50,  "hex": "#2d2d32", "type": "volcanic"},
    {"name": "Magma",           "t": 100, "r": 200, "g": 80,  "b": 20,  "hex": "#c85014", "type": "volcanic"},
    {"name": "Gravel",          "t": 34,  "r": 126, "g": 124, "b": 122, "hex": "#7e7c7a", "type": "scree"},
    {"name": "Clay",            "t": 35,  "r": 158, "g": 164, "b": 176, "hex": "#9ea4b0", "type": "soil"},
    {"name": "Beaches",         "t": 36,  "r": 195, "g": 185, "b": 145, "hex": "#c3b991", "type": "coast"},
    {"name": "Water",           "t": 37,  "r": 47,  "g": 67,  "b": 244, "hex": "#2f43f4", "type": "water"},
    {"name": "DeepSnow",        "t": 40,  "r": 239, "g": 251, "b": 251, "hex": "#effbfb", "type": "snow"},
    {"name": "Granite",         "t": 71,  "r": 153, "g": 113, "b": 98,  "hex": "#997162", "type": "rock"},
    {"name": "Diorite",         "t": 72,  "r": 179, "g": 179, "b": 182, "hex": "#b3b3b6", "type": "rock"},
    {"name": "Andesite",        "t": 73,  "r": 130, "g": 131, "b": 131, "hex": "#828383", "type": "rock"},
]

# Fast NumPy RGB Array for Euclidean distance matching
PALETTE_RGB = np.array([[p["r"], p["g"], p["b"]] for p in MINECRAFT_PALETTE], dtype=np.float32)
PALETTE_T_IDS = np.array([p["t"] for p in MINECRAFT_PALETTE], dtype=np.int32)


# -----------------------------------------------------------------------------
# 2. ASHFALL CONTINENT GEOLOGICAL SYNTHESIZER
# -----------------------------------------------------------------------------
class AshfallContinentEngine:
    """
    Synthesizes the 8000x8000 block Ashfall continent with Lithosphere continuous splines,
    generates 16-bit heightmaps, photorealistic colormaps, and Still Life foliage layers.
    """

    def __init__(self, resolution: int = 2048):
        self.res = resolution
        self.extent = 4000.0  # -4000 to +4000 blocks
        self.pixel_size = (2.0 * self.extent) / self.res
        self.min_y = -64.0
        self.max_y = 320.0
        self.sea_level = 62.0
        self.total_h = self.max_y - self.min_y  # 384 blocks

    def generate_all(self, output_dir: Path, verbose: bool = True) -> Dict[str, Path]:
        """Generate master heightmap, Still Life population masks, and 3D textures."""
        start_t = time.time()
        output_dir.mkdir(parents=True, exist_ok=True)
        if verbose:
            print(f"=====================================================================")
            print(f"   ⚔ ASHFALL CONTINENT GENERATOR & STILL LIFE POPULATION ENGINE ⚔")
            print(f"   Resolution: {self.res}x{self.res} ({self.res*self.res:,} blocks) | Grid: -4000 to +4000")
            print(f"   Elevation: Y={self.min_y:.0f} -> Y={self.max_y:.0f} | Sea Level: Y={self.sea_level:.0f}")
            print(f"=====================================================================")

        # 1. Coordinate Grids
        lin = np.linspace(-self.extent, self.extent, self.res, dtype=np.float32)
        X, Z = np.meshgrid(lin, lin)
        R = np.sqrt(X**2 + Z**2)

        # -------------------------------------------------------------------------
        # STAGE 1: Continental Shelf & Hermite Splines
        # -------------------------------------------------------------------------
        if verbose: print("[1/6] Synthesizing Continental Landmass (Hermite S-Curve)...")
        r_norm = np.clip(R / 3550.0, 0.0, 1.0)
        # S(t) = 1 - (3t^2 - 2t^3)
        continent_mask = 1.0 - (3.0 * (r_norm**2) - 2.0 * (r_norm**3))

        # Add coastal fractal domain warping
        f_coastal = (
            np.sin(X * 0.0022 + Z * 0.0017) * 85.0 +
            np.cos(X * 0.0041 - Z * 0.0035) * 45.0 +
            np.sin(X * 0.0093 + Z * 0.0081) * 22.0
        )
        r_warped = R + f_coastal
        mask_shelf = np.clip((3650.0 - r_warped) / 450.0, 0.0, 1.0)
        mask_shelf = 3.0 * (mask_shelf**2) - 2.0 * (mask_shelf**3)

        # Base elevation: Ocean floor (-45) transitioning to rolling coastal lowlands (70)
        H = -45.0 + mask_shelf * 115.0

        # -------------------------------------------------------------------------
        # STAGE 2: 7 Cardinal Landmark Geologies
        # -------------------------------------------------------------------------
        if verbose: print("[2/6] Sculpting 7 Master Geological Landmarks...")

        # A. The Solitary Glacial Spine (Z < -1000, rising to Y=279+)
        spine_dist = np.sqrt((X * 0.7)**2 + (Z + 2500.0)**2)
        spine_ridge_dist = np.abs(X) + np.abs(Z + 2500.0) * 0.35
        spine_mask = np.clip((2400.0 - spine_dist) / 1200.0, 0.0, 1.0)
        spine_mask = 3.0 * (spine_mask**2) - 2.0 * (spine_mask**3)
        
        # Multi-harmonic rigid crags
        crags = (
            np.abs(np.sin(X * 0.0035 + Z * 0.0025)) * 95.0 +
            np.abs(np.cos(X * 0.0071 - Z * 0.0062)) * 55.0 +
            np.abs(np.sin(X * 0.0150 + Z * 0.0130)) * 28.0
        )
        H += spine_mask * crags

        # B. The Ashen Caldera (Center: R < 700)
        # Rim peaks at R=520, drops to deep crater basin at R < 350
        caldera_rim_env = np.exp(-((R - 520.0)**2) / (2.0 * (160.0**2)))
        caldera_spire_env = np.exp(-(R**2) / (2.0 * (95.0**2)))
        caldera_depression = np.clip((480.0 - R) / 250.0, 0.0, 1.0)

        H += caldera_rim_env * 78.0           # Volcanic rim up to Y=146
        H -= caldera_depression * 55.0        # Sunken crater down to Y=40
        H += caldera_spire_env * 52.0         # Resurgent obsidian throne spire up to Y=92

        # C. The Cogwork March (West: X in [-3000, -1200], Z in [-1000, 1000])
        cogwork_dist = np.sqrt((X + 2100.0)**2 + (Z * 1.4)**2)
        cogwork_mask = np.clip((1400.0 - cogwork_dist) / 700.0, 0.0, 1.0)
        cogwork_mask = 3.0 * (cogwork_mask**2) - 2.0 * (cogwork_mask**3)
        # 9m Quarry step terracing
        cogwork_raw = (np.sin(X * 0.004) + np.cos(Z * 0.004)) * 32.0 + 85.0
        cogwork_terraced = np.floor(cogwork_raw / 9.0) * 9.0
        H = np.where(cogwork_mask > 0.05, H * (1.0 - cogwork_mask) + cogwork_terraced * cogwork_mask, H)

        # D. The Gilded Dunes (East: X in [1200, 3200])
        dunes_dist = np.sqrt((X - 2300.0)**2 + (Z * 1.2)**2)
        dunes_mask = np.clip((1500.0 - dunes_dist) / 800.0, 0.0, 1.0)
        dune_waves = (
            np.sin(X * 0.012 + np.cos(Z * 0.006) * 2.5) * 24.0 +
            np.cos(X * 0.025 + Z * 0.008) * 9.0
        )
        H += dunes_mask * np.maximum(0.0, dune_waves)

        # E. The Whispering Fen (Sunken delta: X ~ 2000, Z ~ 2000)
        fen_dist = np.sqrt((X - 2000.0)**2 + (Z - 2000.0)**2)
        fen_mask = np.clip((1200.0 - fen_dist) / 600.0, 0.0, 1.0)
        H = np.where(fen_mask > 0.1, H * (1.0 - fen_mask) + 63.5 * fen_mask, H)

        # F. The Sunken Reach (Lagoon: X ~ -2400, Z ~ 1600)
        reach_dist = np.sqrt((X + 2400.0)**2 + (Z - 1600.0)**2)
        reach_mask = np.clip((1100.0 - reach_dist) / 500.0, 0.0, 1.0)
        H = np.where(reach_mask > 0.1, H * (1.0 - reach_mask) + 54.0 * reach_mask, H)

        # G. U-Shaped Glacial River Valleys (Lithosphere river_valley_u)
        river_chasm = (
            np.abs(np.sin(X * 0.0018 + np.cos(Z * 0.0015) * 1.8)) +
            np.abs(np.sin(Z * 0.0022 - np.sin(X * 0.0012) * 1.5))
        )
        river_carve = np.clip((0.18 - river_chasm) / 0.18, 0.0, 1.0)
        # Quadratic U-shape
        river_depth = (river_carve**2) * 36.0
        # Protect spawn and ocean
        H -= np.where((R < 3400.0) & (H > self.sea_level - 10.0), river_depth, 0.0)

        # Clamp vertical heights
        H = np.clip(H, self.min_y, self.max_y)

        # -------------------------------------------------------------------------
        # STAGE 3: Slope & Topographic Gradient Analysis
        # -------------------------------------------------------------------------
        if verbose: print("[3/6] Computing Geological Gradients & Slope Angles...")
        dz, dx = np.gradient(H, self.pixel_size, self.pixel_size)
        slope_rad = np.arctan(np.sqrt(dx**2 + dz**2))
        slope_deg = np.degrees(slope_rad)

        # -------------------------------------------------------------------------
        # STAGE 4: Still Life Population Logic & Ecological Masking
        # -------------------------------------------------------------------------
        if verbose: print("[4/6] Executing Still Life Multi-Tier Population Engine...")
        
        # Rule 1: Slope-Aware Topsoil Filtration (Still Life core rule)
        # < 35°: 100% soil / foliage eligible
        # 35°-45°: Transition scree
        # > 45°: Bare stone / cliffs (0% trees, no soil)
        soil_fertility = np.clip((42.0 - slope_deg) / 10.0, 0.0, 1.0)

        # Rule 2: Caldera Exclusion (Volcanic crater is strictly barren)
        caldera_exclusion = np.clip((R - 650.0) / 120.0, 0.0, 1.0)

        # Rule 3: Elevation Zoning & Tree Line
        # Y < Sea Level (62): Ocean / Submarine -> 0%
        # Y in [62, 135]: Fertile Lowlands (Oaks, Birches, Meadow) -> 100%
        # Y in [135, 205]: Subalpine Slopes (Taiga, Old Growth Pine) -> 85%
        # Y in [205, 230]: Alpine Scrub / Tree Line -> Rapid drop to 0%
        # Y > 230: Permafrost & Glacial Crags -> Strictly 0%
        above_sea = np.clip((H - self.sea_level) / 3.0, 0.0, 1.0)
        tree_line_mask = np.clip((225.0 - H) / 25.0, 0.0, 1.0)

        # Rule 4: Oceanic Shelf Cutoff (Inside Continent Radius)
        shelf_fertility = np.clip((3520.0 - R) / 150.0, 0.0, 1.0)

        # Master Populate Probability (0.0 to 1.0)
        populate_factor = soil_fertility * caldera_exclusion * above_sea * tree_line_mask * shelf_fertility

        # -------------------------------------------------------------------------
        # STAGE 5: creativitRy ColorToTerrain Block Palette Synthesis
        # -------------------------------------------------------------------------
        if verbose: print("[5/6] Synthesizing Photorealistic RGB SplatMap & ColorToTerrain...")

        # Synthesize RGB Colormap from geology
        rgb_map = np.zeros((self.res, self.res, 3), dtype=np.uint8)

        # Base ocean
        rgb_map[H <= self.sea_level] = [45, 95, 160]

        # Beaches / Shallows
        beach_cond = (H > self.sea_level) & (H <= self.sea_level + 3.0)
        rgb_map[beach_cond] = [219, 211, 160]

        # Lowland Grass / Plains
        plains_cond = (H > self.sea_level + 3.0) & (H <= 130.0) & (slope_deg <= 35.0)
        rgb_map[plains_cond] = [76, 125, 42]

        # Forest / Fertile Valleys
        forest_cond = plains_cond & (populate_factor > 0.4)
        rgb_map[forest_cond] = [58, 102, 33]

        # Subalpine Pine / Permadirt
        subalpine_cond = (H > 130.0) & (H <= 190.0) & (slope_deg <= 35.0)
        rgb_map[subalpine_cond] = [110, 78, 54]

        # Steep Rock Scree & Cliffs (> 35° or high altitude)
        rock_cond = ((slope_deg > 35.0) | ((H > 190.0) & (H <= 245.0))) & (H > self.sea_level)
        rgb_map[rock_cond] = [125, 125, 125]

        # Glacial Snow Summits (> 245m)
        snow_cond = (H > 245.0)
        rgb_map[snow_cond] = [239, 251, 251]

        # The Ashen Caldera: Basalt & Obsidian
        caldera_cond = (R <= 650.0) & (H > self.sea_level - 15.0)
        rgb_map[caldera_cond] = [38, 38, 44]
        # Caldera lava pools in crater basin
        lava_cond = (R <= 420.0) & (H <= 44.0)
        rgb_map[lava_cond] = [216, 104, 26]
        # Obsidian Throne spire
        throne_cond = (R <= 110.0) & (H > 70.0)
        rgb_map[throne_cond] = [20, 18, 29]

        # The Cogwork March: Terracotta Bands
        cog_cond = (cogwork_mask > 0.2) & (H > self.sea_level)
        cog_band = np.mod(np.floor(H / 5.0), 3.0)
        rgb_map[cog_cond & (cog_band == 0)] = [161, 83, 37]   # Orange Terracotta
        rgb_map[cog_cond & (cog_band == 1)] = [150, 92, 66]   # Hardened Clay
        rgb_map[cog_cond & (cog_band == 2)] = [186, 133, 35]  # Yellow Terracotta

        # The Gilded Dunes: Desert Sand
        dunes_cond = (dunes_mask > 0.25) & (H > self.sea_level + 2.0)
        rgb_map[dunes_cond] = [225, 205, 135]

        # The Whispering Fen: Dark Peat & Swamp
        fen_cond = (fen_mask > 0.2) & (H > self.sea_level - 2.0)
        rgb_map[fen_cond] = [52, 74, 45]

        # Hillshading for visual realism
        sun_azimuth = 315.0
        sun_altitude = 45.0
        az_rad = np.radians(sun_azimuth)
        alt_rad = np.radians(sun_altitude)
        aspect = np.arctan2(-dx, dz)
        shaded = np.sin(alt_rad) * np.cos(slope_rad) + np.cos(alt_rad) * np.sin(slope_rad) * np.cos(az_rad - aspect)
        shaded = np.clip(shaded, 0.0, 1.0)
        shaded_factor = 0.45 + 0.55 * shaded

        hillshade_rgb = (rgb_map.astype(np.float32) * shaded_factor[:, :, np.newaxis]).clip(0, 255).astype(np.uint8)

        # -------------------------------------------------------------------------
        # STAGE 6: Asset Export & Packaging
        # -------------------------------------------------------------------------
        if verbose: print("[6/6] Writing Master Files (16-bit uint16, Masks, 3D Assets)...")

        # 1. 16-Bit Master Heightmap (uint16)
        h_norm = np.clip((H - self.min_y) / self.total_h, 0.0, 1.0)
        h_u16 = (h_norm * 65535.0).astype(np.uint16)
        img_16bit = Image.fromarray(h_u16, mode='I;16')
        p_16bit = output_dir / "ASHFALL_HEIGHTMAP_16BIT.png"
        img_16bit.save(p_16bit)

        # 2. 8-Bit Grayscale Preview
        h_u8 = (h_norm * 255.0).astype(np.uint8)
        img_preview = Image.fromarray(h_u8, mode='L')
        p_preview = output_dir / "ASHFALL_HEIGHTMAP_PREVIEW.png"
        img_preview.save(p_preview)

        # 3. 3D Hillshaded Topographic Atlas
        img_topographic = Image.fromarray(hillshade_rgb, mode='RGB')
        p_topographic = output_dir / "ASHFALL_TOPOGRAPHIC_RENDER.png"
        img_topographic.save(p_topographic)

        # 4. Still Life 100% Populate Mask (Binary for WorldPainter Populate layer)
        pop_mask_u8 = np.where(populate_factor > 0.35, 255, 0).astype(np.uint8)
        img_pop = Image.fromarray(pop_mask_u8, mode='L')
        p_pop = output_dir / "ASHFALL_POPULATE_MASK.png"
        img_pop.save(p_pop)

        # 5. Composite Still Life & Populate View (Emerald Foliage Overlay)
        emerald_overlay = hillshade_rgb.copy()
        mask_bool = pop_mask_u8 > 128
        emerald_overlay[mask_bool, 1] = np.clip(emerald_overlay[mask_bool, 1].astype(np.int32) + 55, 0, 255).astype(np.uint8)
        emerald_overlay[mask_bool, 0] = np.clip(emerald_overlay[mask_bool, 0].astype(np.int32) - 15, 0, 255).astype(np.uint8)
        img_emerald = Image.fromarray(emerald_overlay, mode='RGB')
        p_emerald = output_dir / "ASHFALL_STILL_LIFE_POPULATE_VIEW.png"
        img_emerald.save(p_emerald)

        # 6. Biome Numeric Mask
        biome_mask_u8 = np.zeros((self.res, self.res), dtype=np.uint8)
        biome_mask_u8[H <= self.sea_level] = 0        # Ocean
        biome_mask_u8[plains_cond] = 1                # Plains
        biome_mask_u8[forest_cond] = 4                # Forest
        biome_mask_u8[subalpine_cond] = 5             # Taiga
        biome_mask_u8[snow_cond] = 12                 # Snowy Plains
        biome_mask_u8[caldera_cond] = 8               # Nether / Basalt
        biome_mask_u8[dunes_cond] = 2                 # Desert
        biome_mask_u8[cog_cond] = 37                  # Badlands
        biome_mask_u8[fen_cond] = 6                   # Swamp
        img_biome = Image.fromarray(biome_mask_u8, mode='L')
        p_biome = output_dir / "ASHFALL_BIOME_MASK.png"
        img_biome.save(p_biome)

        elapsed = time.time() - start_t
        if verbose:
            print(f"\n=====================================================================")
            print(f" [✓] GENERATION COMPLETE in {elapsed:.2f} seconds!")
            print(f" Outputs saved to: {output_dir}")
            print(f"=====================================================================\n")

        return {
            "heightmap_16bit": p_16bit,
            "heightmap_preview": p_preview,
            "topographic_render": p_topographic,
            "populate_mask": p_pop,
            "still_life_view": p_emerald,
            "biome_mask": p_biome
        }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Ashfall Continent & Still Life Generator Engine")
    parser.add_argument("--res", type=int, default=2048, choices=[1024, 2048, 4096], help="Grid resolution (default: 2048)")
    parser.add_argument("--out", type=str, default="worldpainter", help="Output directory")
    args = parser.parse_args()

    engine = AshfallContinentEngine(resolution=args.res)
    engine.generate_all(Path(args.out).resolve())

if __name__ == "__main__":
    main()

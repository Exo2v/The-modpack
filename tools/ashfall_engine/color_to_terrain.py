#!/usr/bin/env python3
"""
=============================================================================
ASHFALL: Gaea Color-To-Terrain Converter (Python Engine)
Based on creativitRy's ColorToTerrain Algorithm (https://github.com/creativitRy/ColorToTerrain)
=============================================================================
Converts photorealistic Gaea SatMap/RGB Colormaps into native Minecraft blocks
using vectorized color distance matching and geological slope rules.
"""

import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any

import numpy as np
from PIL import Image

# creativitRy Official Default Minecraft Terrain Palette
COLOR_TO_TERRAIN_PALETTE = [
    {"name": "BareGrass",        "t": 1,   "r": 69,  "g": 110, "b": 51,  "mc_block": "minecraft:grass_block"},
    {"name": "Dirt",             "t": 2,   "r": 134, "g": 96,  "b": 67,  "mc_block": "minecraft:dirt"},
    {"name": "Permadirt",        "t": 3,   "r": 110, "g": 78,  "b": 54,  "mc_block": "minecraft:coarse_dirt"},
    {"name": "Podzol",           "t": 4,   "r": 90,  "g": 63,  "b": 28,  "mc_block": "minecraft:podzol"},
    {"name": "Sand",             "t": 5,   "r": 219, "g": 211, "b": 160, "mc_block": "minecraft:sand"},
    {"name": "RedSand",          "t": 6,   "r": 169, "g": 88,  "b": 33,  "mc_block": "minecraft:red_sand"},
    {"name": "HardenedClay",     "t": 10,  "r": 150, "g": 92,  "b": 66,  "mc_block": "minecraft:terracotta"},
    {"name": "WhiteClay",        "t": 11,  "r": 209, "g": 178, "b": 161, "mc_block": "minecraft:white_terracotta"},
    {"name": "OrangeClay",       "t": 12,  "r": 161, "g": 83,  "b": 37,  "mc_block": "minecraft:orange_terracotta"},
    {"name": "MagentaClay",      "t": 13,  "r": 149, "g": 88,  "b": 108, "mc_block": "minecraft:magenta_terracotta"},
    {"name": "LightBlueClay",    "t": 14,  "r": 113, "g": 108, "b": 137, "mc_block": "minecraft:light_blue_terracotta"},
    {"name": "YellowClay",       "t": 15,  "r": 186, "g": 133, "b": 35,  "mc_block": "minecraft:yellow_terracotta"},
    {"name": "LimeClay",         "t": 16,  "r": 103, "g": 117, "b": 52,  "mc_block": "minecraft:lime_terracotta"},
    {"name": "PinkClay",         "t": 17,  "r": 161, "g": 78,  "b": 78,  "mc_block": "minecraft:pink_terracotta"},
    {"name": "GreyClay",         "t": 18,  "r": 57,  "g": 42,  "b": 35,  "mc_block": "minecraft:gray_terracotta"},
    {"name": "LightGreyClay",    "t": 19,  "r": 135, "g": 106, "b": 97,  "mc_block": "minecraft:light_gray_terracotta"},
    {"name": "CyanClay",         "t": 20,  "r": 86,  "g": 91,  "b": 91,  "mc_block": "minecraft:cyan_terracotta"},
    {"name": "PurpleClay",       "t": 21,  "r": 118, "g": 70,  "b": 86,  "mc_block": "minecraft:purple_terracotta"},
    {"name": "BlueClay",         "t": 22,  "r": 74,  "g": 59,  "b": 91,  "mc_block": "minecraft:blue_terracotta"},
    {"name": "BrownClay",        "t": 23,  "r": 77,  "g": 51,  "b": 35,  "mc_block": "minecraft:brown_terracotta"},
    {"name": "GreenClay",        "t": 24,  "r": 76,  "g": 83,  "b": 42,  "mc_block": "minecraft:green_terracotta"},
    {"name": "RedClay",          "t": 25,  "r": 143, "g": 61,  "b": 46,  "mc_block": "minecraft:red_terracotta"},
    {"name": "BlackClay",        "t": 26,  "r": 37,  "g": 22,  "b": 16,  "mc_block": "minecraft:black_terracotta"},
    {"name": "Sandstone",        "t": 27,  "r": 218, "g": 210, "b": 158, "mc_block": "minecraft:sandstone"},
    {"name": "Stone",            "t": 28,  "r": 125, "g": 125, "b": 125, "mc_block": "minecraft:stone"},
    {"name": "Rock",             "t": 29,  "r": 123, "g": 123, "b": 123, "mc_block": "minecraft:stone"},
    {"name": "Cobblestone",      "t": 30,  "r": 122, "g": 122, "b": 122, "mc_block": "minecraft:cobblestone"},
    {"name": "MossyCobblestone", "t": 31,  "r": 103, "g": 121, "b": 103, "mc_block": "minecraft:mossy_cobblestone"},
    {"name": "Obsidian",         "t": 32,  "r": 20,  "g": 18,  "b": 29,  "mc_block": "minecraft:obsidian"},
    {"name": "Bedrock",          "t": 33,  "r": 83,  "g": 83,  "b": 83,  "mc_block": "minecraft:bedrock"},
    {"name": "Gravel",           "t": 34,  "r": 126, "g": 124, "b": 122, "mc_block": "minecraft:gravel"},
    {"name": "Clay",             "t": 35,  "r": 158, "g": 164, "b": 176, "mc_block": "minecraft:clay"},
    {"name": "Water",            "t": 37,  "r": 47,  "g": 67,  "b": 244, "mc_block": "minecraft:water"},
    {"name": "Lava",             "t": 38,  "r": 216, "g": 104, "b": 26,  "mc_block": "minecraft:lava"},
    {"name": "DeepSnow",         "t": 40,  "r": 239, "g": 251, "b": 251, "mc_block": "minecraft:snow_block"},
    {"name": "Netherrack",       "t": 41,  "r": 111, "g": 54,  "b": 52,  "mc_block": "minecraft:netherrack"},
    {"name": "SoulSand",         "t": 42,  "r": 84,  "g": 64,  "b": 51,  "mc_block": "minecraft:soul_sand"},
    {"name": "Granite",          "t": 71,  "r": 153, "g": 113, "b": 98,  "mc_block": "minecraft:granite"},
    {"name": "Diorite",          "t": 72,  "r": 179, "g": 179, "b": 182, "mc_block": "minecraft:diorite"},
    {"name": "Andesite",         "t": 73,  "r": 130, "g": 131, "b": 131, "mc_block": "minecraft:andesite"},
    {"name": "GrassPath",        "t": 99,  "r": 159, "g": 114, "b": 98,  "mc_block": "minecraft:dirt_path"},
    {"name": "Magma",            "t": 100, "r": 200, "g": 80,  "b": 20,  "mc_block": "minecraft:magma_block"}
]

PAL_RGB = np.array([[p["r"], p["g"], p["b"]] for p in COLOR_TO_TERRAIN_PALETTE], dtype=np.float32)
PAL_T = np.array([p["t"] for p in COLOR_TO_TERRAIN_PALETTE], dtype=np.int32)


class ColorToTerrainConverter:
    """Vectorized Python engine implementing creativitRy's ColorToTerrain matching."""

    @classmethod
    def convert_image(
        cls,
        rgb_image_path: Path,
        output_preview_path: Optional[Path] = None,
        output_indexed_path: Optional[Path] = None,
        slope_mask: Optional[np.ndarray] = None
    ) -> Dict[str, Any]:
        t0 = time.time()
        img = Image.open(rgb_image_path).convert("RGB")
        w, h = img.size
        rgb_arr = np.array(img, dtype=np.float32)

        # Vectorized Euclidean color distance matching:
        # Distance = (R - r)^2 + (G - g)^2 + (B - b)^2
        # rgb_arr shape: (H, W, 3)
        # PAL_RGB shape: (N, 3)
        # Compute squared differences across channels
        r = rgb_arr[:, :, 0, np.newaxis]
        g = rgb_arr[:, :, 1, np.newaxis]
        b = rgb_arr[:, :, 2, np.newaxis]

        pr = PAL_RGB[:, 0]
        pg = PAL_RGB[:, 1]
        pb = PAL_RGB[:, 2]

        # Broadcasted distance computation: (H, W, N)
        dist_sq = (r - pr)**2 + (g - pg)**2 + (b - pb)**2

        # Find closest palette index for each pixel: (H, W)
        best_indices = np.argmin(dist_sq, axis=2).astype(np.int32)

        # If slope mask provided (> 45° forced to Rock or Stone):
        if slope_mask is not None:
            rock_idx = next(i for i, p in enumerate(COLOR_TO_TERRAIN_PALETTE) if p["name"] == "Rock")
            best_indices[slope_mask > 45.0] = rock_idx

        # Generate Quantized Color Preview Image
        quantized_rgb = PAL_RGB[best_indices].astype(np.uint8)
        img_preview = Image.fromarray(quantized_rgb, mode="RGB")

        if output_preview_path:
            output_preview_path.parent.mkdir(parents=True, exist_ok=True)
            img_preview.save(output_preview_path)

        # Generate Indexed Palette Image (Pixel value = Terrain Index)
        indexed_terrain_ids = PAL_T[best_indices].astype(np.uint8)
        img_indexed = Image.fromarray(indexed_terrain_ids, mode="L")

        if output_indexed_path:
            output_indexed_path.parent.mkdir(parents=True, exist_ok=True)
            img_indexed.save(output_indexed_path)

        dt = time.time() - t0
        return {
            "width": w,
            "height": h,
            "pixels_processed": w * h,
            "time_seconds": dt,
            "used_palette_entries": int(len(np.unique(best_indices))),
            "preview_path": str(output_preview_path) if output_preview_path else None,
            "indexed_path": str(output_indexed_path) if output_indexed_path else None
        }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Gaea ColorToTerrain Python Converter")
    parser.add_argument("input", help="Input RGB splatmap / SatMap PNG")
    parser.add_argument("--out-preview", default="worldpainter/ASHFALL_COLOR_TO_TERRAIN_PREVIEW.png", help="Output preview PNG")
    parser.add_argument("--out-indexed", default="worldpainter/ASHFALL_TERRAIN_INDEXED.png", help="Output indexed terrain PNG")
    args = parser.parse_args()

    res = ColorToTerrainConverter.convert_image(
        Path(args.input),
        output_preview_path=Path(args.out_preview),
        output_indexed_path=Path(args.out_indexed)
    )
    print(f"[✓] ColorToTerrain completed: {res['pixels_processed']:,} pixels mapped in {res['time_seconds']:.2f}s ({res['used_palette_entries']} block types)")

if __name__ == "__main__":
    main()

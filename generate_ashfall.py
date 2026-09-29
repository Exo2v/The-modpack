#!/usr/bin/env python3
"""
=============================================================================
ASHFALL: Master Turnkey Continent & Population Generator Pipeline
=============================================================================
Integrates:
  1. Continents & Lithosphere Geology Engine (Y=-64 to Y=320, Sea Level: 62)
  2. Still Life Population Logic (Slope-Aware Trees, Shrubs, Boulders, Logs)
  3. creativitRy ColorToTerrain Logic (RGB SplatMap to Minecraft Block Palette)
  4. WorldPainter JSR223 Automation & 3D WebGL WebStudio Integration
=============================================================================
"""

import os
import sys
import time
import zipfile
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from tools.ashfall_engine.generator import AshfallContinentEngine
from tools.ashfall_engine.color_to_terrain import ColorToTerrainConverter
from tools.worldpainter_api import WorldPainterScriptBuilder

def run_pipeline(
    resolution: int = 2048,
    output_dir: Path = BASE_DIR / "worldpainter",
    gaea_heightmap: Optional[Path] = None,
    gaea_satmap: Optional[Path] = None
):
    print("=====================================================================")
    print("   ⚔ ASHFALL MASTER CONTINENT & POPULATION PIPELINE ⚔")
    print(f"   Resolution: {resolution}x{resolution} | Destination: {output_dir}")
    if gaea_heightmap:
        print(f"   Mode: Ingesting Gaea Export ({gaea_heightmap.name})")
    else:
        print("   Mode: Procedural Continental Geology (Lithosphere + Continents)")
    print("=====================================================================")

    # STAGE 1: Continent Heightmap & Still Life Population
    if gaea_heightmap and gaea_heightmap.exists():
        files = AshfallContinentEngine.ingest_gaea_map(
            heightmap_path=gaea_heightmap,
            satmap_path=gaea_satmap,
            output_dir=output_dir,
            target_res=resolution
        )
        source_color = gaea_satmap if gaea_satmap and gaea_satmap.exists() else files["topographic_render"]
    else:
        engine = AshfallContinentEngine(resolution=resolution)
        files = engine.generate_all(output_dir)
        source_color = files["topographic_render"]

    # STAGE 2: creativitRy ColorToTerrain Conversion
    print("[+] Executing creativitRy ColorToTerrain Quantization...")
    color_preview = output_dir / "ASHFALL_COLOR_TO_TERRAIN_PREVIEW.png"
    terrain_indexed = output_dir / "ASHFALL_TERRAIN_INDEXED.png"
    ColorToTerrainConverter.convert_image(
        source_color,
        output_preview_path=color_preview,
        output_indexed_path=terrain_indexed
    )

    # STAGE 3: Build WorldPainter API Script
    print("[+] Compiling WorldPainter JSR223 Setup Script...")
    builder = WorldPainterScriptBuilder(
        world_name="Ashfall_Continent",
        min_y=-64,
        max_y=320,
        sea_level=62,
        heightmap_path="worldpainter/ASHFALL_HEIGHTMAP_16BIT.png",
        populate_mask_path="worldpainter/ASHFALL_POPULATE_MASK.png",
        enable_stratification=True,
        enable_frost=True,
        frost_altitude=210,
        export_mode="world"
    )
    script_path = output_dir / "ashenfall_worldpainter_setup.js"
    builder.write_script_file(str(script_path))

    # STAGE 4: Re-bundle WorldPainter Master Suite Zip
    print("[+] Packaging ASHENFALL_WORLDPAINTER_SUITE.zip...")
    zip_path = output_dir / "ASHENFALL_WORLDPAINTER_SUITE.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in [
            files["heightmap_16bit"],
            files["populate_mask"],
            files["topographic_render"],
            files["heightmap_preview"],
            files["biome_mask"],
            color_preview,
            terrain_indexed,
            script_path
        ]:
            if f.exists():
                z.write(f, arcname=f.name)
    print(f"      [✓] Suite packaged ({zip_path.stat().st_size / (1024*1024):.1f} MB)")

    print("\n=====================================================================")
    print(" [✓] ASHFALL PIPELINE COMPLETE — READY FOR WORLDPAINTER & 3D PREVIEW!")
    print("=====================================================================\n")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Ashfall Continent & Population Generator (Supports QuadSpinner Gaea)")
    parser.add_argument("--res", type=int, default=2048, choices=[1024, 2048, 4096], help="Resolution (default: 2048)")
    parser.add_argument("--out", type=str, default="worldpainter", help="Output directory")
    parser.add_argument("--gaea-heightmap", type=str, default=None, help="Path to 1024x1024 Gaea heightmap (.png, .tiff)")
    parser.add_argument("--gaea-satmap", type=str, default=None, help="Path to 1024x1024 Gaea SatMap/RGB colormap (.png)")
    args = parser.parse_args()

    h_path = Path(args.gaea_heightmap).resolve() if args.gaea_heightmap else None
    s_path = Path(args.gaea_satmap).resolve() if args.gaea_satmap else None

    run_pipeline(
        resolution=args.res,
        output_dir=Path(args.out).resolve(),
        gaea_heightmap=h_path,
        gaea_satmap=s_path
    )

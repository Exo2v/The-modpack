#!/usr/bin/env python3
"""
WorldPainter Scripting API Integration Engine
==============================================
Provides high-level Python abstractions and turnkey code generators for
WorldPainter's JSR223 Java Scripting API (wpscript).

Features:
- Programmatic .world / Minecraft world generation from 16-bit heightmaps
- Automatic application of Populate, Biome, and Custom Material layers
- Multi-tier terrain stratification (Beaches -> Grass -> Stone -> Snow)
- Dynamic script generation with intelligent multi-directory path resolvers
- Headless execution engine (detects wpscript across Windows, Linux, and macOS)
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

# Standard WorldPainter Terrain Type Indices (org.pepsoft.worldpainter.Terrain)
TERRAIN_TYPES = {
    "Grass": 0,
    "BareGrass": 1,
    "Dirt": 2,
    "Permadirt": 3,
    "Podzol": 4,
    "Sand": 5,
    "RedSand": 6,
    "Desert": 7,
    "RedDesert": 8,
    "Mesa": 9,
    "HardenedClay": 10,
    "Sandstone": 27,
    "Stone": 28,
    "Rock": 29,
    "Cobblestone": 30,
    "MossyCobblestone": 31,
    "Obsidian": 32,
    "Bedrock": 33,
    "Gravel": 34,
    "Clay": 35,
    "Beaches": 36,
    "Water": 37,
    "Lava": 38,
    "StoneSnow": 39,
    "DeepSnow": 40,
    "RedSandstone": 70,
    "Granite": 71,
    "Diorite": 72,
    "Andesite": 73,
    "StoneMix": 74,
    "Magma": 100,
}

# Common Minecraft Biome Numeric IDs for WorldPainter Biome Layers
MINECRAFT_BIOME_IDS = {
    "Ocean": 0,
    "Plains": 1,
    "Desert": 2,
    "WindsweptHills": 3,
    "Forest": 4,
    "Taiga": 5,
    "Swamp": 6,
    "River": 7,
    "NetherWastes": 8,
    "TheEnd": 9,
    "FrozenOcean": 10,
    "FrozenRiver": 11,
    "SnowyPlains": 12,
    "SnowyTaiga": 30,
    "OldGrowthPineTaiga": 32,
    "WindsweptForest": 34,
    "Badlands": 37,
    "WarmOcean": 44,
    "DeepDark": 174,
    "MangroveSwamp": 175,
    "CherryGrove": 176,
}

class WorldPainterScriptBuilder:
    """Generates production-grade JSR223 JavaScript scripts for WorldPainter."""

    def __init__(
        self,
        world_name: str = "Ashenfall_Continent",
        min_y: int = -64,
        max_y: int = 320,
        sea_level: int = 62,
        heightmap_path: str = "ASHENFALL_HEIGHTMAP_16BIT.png",
        populate_mask_path: Optional[str] = "ASHENFALL_POPULATE_MASK.png",
        biome_mask_path: Optional[str] = "ASHENFALL_BIOME_MASK.png",
        enable_stratification: bool = True,
        enable_frost: bool = True,
        frost_altitude: int = 210,
        export_mode: str = "world",  # 'world' or 'save'
        export_target: Optional[str] = None
    ):
        self.world_name = world_name
        self.min_y = min_y
        self.max_y = max_y
        self.sea_level = sea_level
        self.heightmap_path = heightmap_path
        self.populate_mask_path = populate_mask_path
        self.biome_mask_path = biome_mask_path
        self.enable_stratification = enable_stratification
        self.enable_frost = enable_frost
        self.frost_altitude = frost_altitude
        self.export_mode = export_mode
        self.export_target = export_target or (
            f"~/Downloads/{world_name}.world" if export_mode == "world" else f"~/AppData/Roaming/.minecraft/saves/{world_name}"
        )
        
        # Default Geological Terrain Strata (Altitude mapped to Terrain Index)
        self.strata: List[Dict[str, Any]] = [
            {"from_h": min_y, "to_h": sea_level + 2, "terrain": TERRAIN_TYPES["Beaches"], "name": "Ocean Floor & Coast"},
            {"from_h": sea_level + 3, "to_h": 140, "terrain": TERRAIN_TYPES["Grass"], "name": "Fertile Lowlands & Valleys"},
            {"from_h": 141, "to_h": 190, "terrain": TERRAIN_TYPES["Permadirt"], "name": "Subalpine Heathlands"},
            {"from_h": 191, "to_h": 250, "terrain": TERRAIN_TYPES["StoneMix"], "name": "High Crags & Bare Rock"},
            {"from_h": 251, "to_h": max_y, "terrain": TERRAIN_TYPES["DeepSnow"], "name": "Glacial Summits & Permafrost"}
        ]

    def set_strata(self, strata: List[Dict[str, Any]]) -> "WorldPainterScriptBuilder":
        """Override the default terrain strata."""
        self.strata = strata
        return self

    def generate_javascript(self) -> str:
        """Produce the complete, syntactically clean JSR223 JavaScript script."""
        
        # Build Strata JS chained calls
        strata_js_lines = []
        if self.enable_stratification and self.strata:
            strata_js_lines.append("    wp.applyHeightMap(heightMap)")
            strata_js_lines.append("        .toWorld(world)")
            strata_js_lines.append("        .applyToTerrain()")
            for s in self.strata:
                strata_js_lines.append(
                    f"        .fromLevels({s['from_h']}, {s['to_h']}).toTerrain({s['terrain']}) // {s['name']}"
                )
            strata_js_lines.append("        .go();")
            strata_js_lines.append('    print(" [✓] Terrain stratification successfully applied.");')
        strata_code = "\n".join(strata_js_lines)

        # Build Populate Layer JS
        populate_code = ""
        if self.populate_mask_path:
            populate_code = f"""
// -----------------------------------------------------------------------------
// STEP 3: Apply Still Life Pre-Population Layer (Foliage, Towns, Caverns)
// -----------------------------------------------------------------------------
print("\\n[3/5] Applying Still Life Pre-Population Layer...");
try {{
    var popMaskFile = resolveFile("{self.populate_mask_path}");
    var popMask = wp.getHeightMap().fromFile(popMaskFile).go();
    var populateLayer = wp.getLayer().withName("Populate").go();

    wp.applyHeightMap(popMask)
        .toWorld(world)
        .applyToLayer(populateLayer)
        .fromLevels(128, 255).toLevel(1)
        .go();
    print(" [✓] Populate Layer applied across all valleys, forests, and settlements!");
}} catch (e) {{
    print(" [!] Note on Populate Layer: " + e);
}}
"""

        # Build Frost Layer JS
        frost_code = ""
        if self.enable_frost:
            frost_code = f"""
// -----------------------------------------------------------------------------
// STEP 4: Apply High-Altitude Glacial Frost Layer
// -----------------------------------------------------------------------------
print("\\n[4/5] Applying High-Altitude Glacial Frost Layer (Y >= {self.frost_altitude})...");
try {{
    var frostLayer = wp.getLayer().withName("Frost").go();
    wp.applyHeightMap(heightMap)
        .toWorld(world)
        .applyToLayer(frostLayer)
        .fromLevels(0, {self.frost_altitude - 1}).toLevel(0)
        .fromLevels({self.frost_altitude}, {self.max_y}).toLevel(1)
        .go();
    print(" [✓] Glacial Frost layer painted across high mountain peaks!");
}} catch (e) {{
    print(" [!] Note on Frost Layer: " + e);
}}
"""

        # Build Export JS
        if self.export_mode == "save":
            export_code = f"""
// -----------------------------------------------------------------------------
// STEP 5: Headless Export Directly to Minecraft Anvil Region Save
// -----------------------------------------------------------------------------
var exportDir = resolveTargetDirectory("{self.export_target}");
print("\\n[5/5] Exporting World directly to Minecraft save: " + exportDir + "...");
wp.exportWorld(world, exportDir);
print("\\n=====================================================================");
print(" [✓] SUCCESS! Ashenfall continent exported directly to Minecraft saves!");
print(" Directory: " + exportDir);
print("=====================================================================");
"""
        else:
            export_code = f"""
// -----------------------------------------------------------------------------
// STEP 5: Save WorldPainter Master Project File (.world)
// -----------------------------------------------------------------------------
var saveTarget = resolveTargetFilePath("{self.export_target}");
print("\\n[5/5] Saving WorldPainter Master Project: " + saveTarget + "...");
wp.saveWorld(world).toFile(saveTarget).go();
print("\\n=====================================================================");
print(" [✓] SUCCESS! Ashenfall continent project created and configured!");
print(" Saved to: " + saveTarget);
print("=====================================================================");
"""

        js_template = f"""// =============================================================================
// ASHENFALL: WorldPainter JSR223 API Automated Synthesis Script
// World: {self.world_name}
// Dimensions: Y={self.min_y} to Y={self.max_y} | Sea Level: Y={self.sea_level}
// Built with WorldPainter API Integration Engine v2.5
// =============================================================================

print("=====================================================================");
print("   ⚔ ASHENFALL — WorldPainter JSR223 API Synthesis ⚔");
print("   World: {self.world_name}");
print("   Elevation Range: [{self.min_y} -> {self.max_y}] | Sea Level: {self.sea_level}");
print("=====================================================================");

// -----------------------------------------------------------------------------
// Smart Path Resolver (Inspects relative dir, Downloads, Desktop, or prompts)
// -----------------------------------------------------------------------------
function resolveFile(filename) {{
    var f = new java.io.File(filename);
    if (f.exists()) {{
        print(" -> Located file: " + f.getAbsolutePath());
        return f.getAbsolutePath();
    }}

    var userHome = java.lang.System.getProperty("user.home");
    var searchPaths = [
        filename,
        "worldpainter/" + filename,
        "../worldpainter/" + filename,
        userHome + "/Downloads/" + filename,
        userHome + "/Downloads/ASHENFALL_WORLDPAINTER_SUITE/" + filename,
        userHome + "/Desktop/" + filename,
        userHome + "/Desktop/ASHENFALL_WORLDPAINTER_SUITE/" + filename,
        userHome + "/Documents/" + filename
    ];

    for (var i = 0; i < searchPaths.length; i++) {{
        var candidate = new java.io.File(searchPaths[i]);
        if (candidate.exists()) {{
            print(" -> Located file: " + candidate.getAbsolutePath());
            return candidate.getAbsolutePath();
        }}
    }}

    // Headless / GUI Fallback
    try {{
        if (!java.awt.GraphicsEnvironment.isHeadless()) {{
            print(" -> Prompting for file: " + filename);
            var chooser = new javax.swing.JFileChooser(userHome + "/Downloads");
            chooser.setDialogTitle("WorldPainter API: Please select " + filename);
            var result = chooser.showOpenDialog(null);
            if (result == javax.swing.JFileChooser.APPROVE_OPTION) {{
                return chooser.getSelectedFile().getAbsolutePath();
            }}
        }}
    }} catch (guiErr) {{
        // Headless execution mode
    }}

    throw new java.lang.RuntimeException("WorldPainter API Error: Could not locate " + filename);
}}

function resolveTargetFilePath(target) {{
    var userHome = java.lang.System.getProperty("user.home");
    var expanded = target.replace(/^~/, userHome);
    var targetFile = new java.io.File(expanded);
    if (targetFile.getParentFile() != null && !targetFile.getParentFile().exists()) {{
        targetFile.getParentFile().mkdirs();
    }}
    return targetFile.getAbsolutePath();
}}

function resolveTargetDirectory(target) {{
    var userHome = java.lang.System.getProperty("user.home");
    var expanded = target.replace(/^~/, userHome);
    var targetDir = new java.io.File(expanded);
    if (!targetDir.exists()) {{
        targetDir.mkdirs();
    }}
    return targetDir.getAbsolutePath();
}}

// -----------------------------------------------------------------------------
// STEP 1: Load 16-Bit Master Topographic Heightmap
// -----------------------------------------------------------------------------
print("\\n[1/5] Loading 16-bit Master Heightmap...");
var heightMapFile = resolveFile("{self.heightmap_path}");
var heightMap = wp.getHeightMap()
    .fromFile(heightMapFile)
    .go();

// -----------------------------------------------------------------------------
// STEP 2: Create 3D World (Y={self.min_y} to Y={self.max_y}, Water={self.sea_level})
// -----------------------------------------------------------------------------
print("\\n[2/5] Sculpting 3D Continent Dimensions...");
var world = wp.createWorld()
    .fromHeightMap(heightMap)
    .scale(100)
    .shift(0, 0)
    .fromLevels(0, 65535).toLevels({self.min_y}, {self.max_y})
    .withWaterLevel({self.sea_level})
    .withLowerBuildLimit({self.min_y})
    .withUpperBuildLimit({self.max_y})
    .go();
print(" [✓] 3D World geometry initialized.");

// Optional Terrain Stratification
{strata_code}

{populate_code}

{frost_code}

{export_code}
"""
        return js_template.strip()

    def write_script_file(self, output_path: str) -> Path:
        """Write the generated script to a file on disk."""
        target = Path(output_path).resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        content = self.generate_javascript()
        target.write_text(content, encoding="utf-8")
        return target


class WorldPainterCLIBridge:
    """Detects and invokes the WorldPainter headless scripting tool (wpscript)."""

    WINDOWS_SEARCH_PATHS = [
        Path(os.environ.get("ProgramFiles", "C:\\Program Files")) / "WorldPainter" / "wpscript.exe",
        Path(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")) / "WorldPainter" / "wpscript.exe",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "WorldPainter" / "wpscript.exe",
        Path(os.environ.get("USERPROFILE", "")) / "AppData" / "Local" / "Programs" / "WorldPainter" / "wpscript.exe",
    ]

    LINUX_SEARCH_PATHS = [
        Path("/usr/local/bin/wpscript"),
        Path("/usr/bin/wpscript"),
        Path("/opt/worldpainter/wpscript"),
        Path.home() / ".local/bin/wpscript",
    ]

    MACOS_SEARCH_PATHS = [
        Path("/Applications/WorldPainter.app/Contents/MacOS/wpscript"),
        Path.home() / "Applications/WorldPainter.app/Contents/MacOS/wpscript",
    ]

    @classmethod
    def find_wpscript(cls) -> Optional[Path]:
        """Search system PATH and standard installation paths for wpscript binary."""
        # 1. System PATH
        which_path = shutil.which("wpscript") or shutil.which("wpscript.exe")
        if which_path:
            return Path(which_path).resolve()

        # 2. Operating System candidates
        candidates = []
        if sys.platform.startswith("win"):
            candidates.extend(cls.WINDOWS_SEARCH_PATHS)
        elif sys.platform.startswith("darwin"):
            candidates.extend(cls.MACOS_SEARCH_PATHS)
        else:
            candidates.extend(cls.LINUX_SEARCH_PATHS)

        for candidate in candidates:
            if candidate and candidate.exists() and os.access(str(candidate), os.X_OK):
                return candidate.resolve()

        return None

    @classmethod
    def execute_script(
        cls,
        script_path: str,
        wpscript_path: Optional[str] = None,
        extra_args: Optional[List[str]] = None,
        timeout_sec: int = 600
    ) -> Dict[str, Any]:
        """Execute a WorldPainter script headlessly."""
        binary = Path(wpscript_path) if wpscript_path else cls.find_wpscript()
        if not binary or not binary.exists():
            return {
                "success": False,
                "error": "wpscript executable not found on host machine",
                "searched_paths": [str(p) for p in (cls.WINDOWS_SEARCH_PATHS if sys.platform.startswith("win") else cls.LINUX_SEARCH_PATHS)],
                "stdout": "",
                "stderr": "",
                "exit_code": -1
            }

        cmd = [str(binary), str(Path(script_path).resolve())]
        if extra_args:
            cmd.extend(extra_args)

        try:
            res = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout_sec,
                check=False
            )
            return {
                "success": res.returncode == 0,
                "wpscript": str(binary),
                "script": str(script_path),
                "stdout": res.stdout,
                "stderr": res.stderr,
                "exit_code": res.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Execution timed out after {timeout_sec} seconds",
                "exit_code": -2,
                "stdout": "",
                "stderr": ""
            }
        except Exception as ex:
            return {
                "success": False,
                "error": str(ex),
                "exit_code": -3,
                "stdout": "",
                "stderr": ""
            }


# -----------------------------------------------------------------------------
# CLI Entrypoint
# -----------------------------------------------------------------------------
def main():
    import argparse
    parser = argparse.ArgumentParser(description="WorldPainter JSR223 API Integration CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: generate
    gen_parser = subparsers.add_parser("generate", help="Generate JSR223 script for WorldPainter")
    gen_parser.add_argument("--world-name", default="Ashenfall_Continent", help="World name")
    gen_parser.add_argument("--heightmap", default="worldpainter/ASHENFALL_HEIGHTMAP_16BIT.png", help="Heightmap file")
    gen_parser.add_argument("--populate-mask", default="worldpainter/ASHENFALL_POPULATE_MASK.png", help="Populate mask")
    gen_parser.add_argument("--min-y", type=int, default=-64, help="Lower build limit (default -64)")
    gen_parser.add_argument("--max-y", type=int, default=320, help="Upper build limit (default 320)")
    gen_parser.add_argument("--sea-level", type=int, default=62, help="Sea level (default 62)")
    gen_parser.add_argument("--export-mode", choices=["world", "save"], default="world", help="Export target mode")
    gen_parser.add_argument("--export-target", default=None, help="Target file or directory path")
    gen_parser.add_argument("--output", default="worldpainter/ashenfall_worldpainter_setup.js", help="Output .js file path")

    # Subcommand: detect
    subparsers.add_parser("detect", help="Scan system for WorldPainter wpscript executable")

    # Subcommand: run
    run_parser = subparsers.add_parser("run", help="Run a WorldPainter script headlessly via wpscript")
    run_parser.add_argument("script", help="Path to .js script file")
    run_parser.add_argument("--wpscript", default=None, help="Explicit path to wpscript executable")

    args = parser.parse_args()

    if args.command == "detect":
        binary = WorldPainterCLIBridge.find_wpscript()
        if binary:
            print(f"[✓] Found wpscript: {binary}")
            sys.exit(0)
        else:
            print("[!] wpscript not found in standard system locations.")
            sys.exit(1)

    elif args.command == "generate":
        builder = WorldPainterScriptBuilder(
            world_name=args.world_name,
            min_y=args.min_y,
            max_y=args.max_y,
            sea_level=args.sea_level,
            heightmap_path=args.heightmap,
            populate_mask_path=args.populate_mask,
            export_mode=args.export_mode,
            export_target=args.export_target
        )
        out = builder.write_script_file(args.output)
        print(f"[✓] Generated WorldPainter API script: {out}")

    elif args.command == "run":
        result = WorldPainterCLIBridge.execute_script(args.script, wpscript_path=args.wpscript)
        print(json.dumps(result, indent=2))
        sys.exit(0 if result.get("success") else 1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Build the Ashenfall Worldgen Datapack for Minecraft 1.21.1 NeoForge.
Integrates with Lithosphere (smooth splines) and Still Life (realistic biomes).
Outputs:
  - pack/overrides/datapacks/ashenfall_worldgen/
  - pack/overrides/datapacks/ashenfall_worldgen.zip
  - pack/overrides/data/ (embedded fallback)
"""

import os
import json
import zipfile
import shutil

def build_datapack():
    base_dir = "/home/user/The-modpack"
    dp_dir = os.path.join(base_dir, "pack/overrides/datapacks/ashenfall_worldgen")
    data_dir = os.path.join(dp_dir, "data/minecraft/dimension")
    os.makedirs(data_dir, exist_ok=True)
    
    # 1. pack.mcmeta (Format 48 for Minecraft 1.21.1)
    pack_mcmeta = {
        "pack": {
            "pack_format": 48,
            "description": "Ashenfall: The Broken Realm — Lithosphere & Still Life Continental Engine"
        }
    }
    with open(os.path.join(dp_dir, "pack.mcmeta"), "w", encoding="utf-8") as f:
        json.dump(pack_mcmeta, f, indent=2)
        
    # 2. overworld.json multi-noise biome definition
    # Carefully tuned climate parameter points matching the 9 Ashenfall nations
    biomes_config = [
        # --- THE VEIL OF SALT (OUTER OCEAN RIM) ---
        {
            "biome": "minecraft:deep_ocean",
            "parameters": {
                "temperature": [-0.5, 0.5],
                "humidity": [-0.5, 0.5],
                "continentalness": [-1.2, -0.35],
                "erosion": [-1.0, 1.0],
                "weirdness": [-1.0, 1.0],
                "depth": 0,
                "offset": 0.0
            }
        },
        {
            "biome": "minecraft:deep_cold_ocean",
            "parameters": {
                "temperature": [-1.2, -0.5],
                "humidity": [-0.5, 0.5],
                "continentalness": [-1.2, -0.35],
                "erosion": [-1.0, 1.0],
                "weirdness": [-1.0, 1.0],
                "depth": 0,
                "offset": 0.0
            }
        },

        # --- REGION 1: THE ASHEN CALDERA (CENTER, VOLCANIC EPICENTER) ---
        {
            "biome": "minecraft:basalt_deltas",
            "parameters": {
                "temperature": [0.2, 0.8],
                "humidity": [-0.8, -0.2],
                "continentalness": [0.65, 1.2],
                "erosion": [-1.0, -0.35],
                "weirdness": [-1.0, -0.4],
                "depth": 0,
                "offset": 0.0
            }
        },
        {
            "biome": "minecraft:eroded_badlands",
            "parameters": {
                "temperature": [0.3, 0.9],
                "humidity": [-0.7, -0.1],
                "continentalness": [0.55, 1.0],
                "erosion": [-0.6, 0.0],
                "weirdness": [-0.6, 0.0],
                "depth": 0,
                "offset": 0.0
            }
        },

        # --- REGION 2: THE SOLITARY GLACIAL SPINE (NORTH ALPINE MOUNTAINS) ---
        {
            "biome": "minecraft:frozen_peaks",
            "parameters": {
                "temperature": [-1.2, -0.6],
                "humidity": [-0.4, 0.4],
                "continentalness": [0.35, 1.0],
                "erosion": [-1.0, -0.5],
                "weirdness": [0.3, 1.0],
                "depth": 0,
                "offset": 0.0
            }
        },
        {
            "biome": "minecraft:jagged_peaks",
            "parameters": {
                "temperature": [-0.6, -0.3],
                "humidity": [-0.4, 0.4],
                "continentalness": [0.3, 1.0],
                "erosion": [-1.0, -0.4],
                "weirdness": [0.2, 1.0],
                "depth": 0,
                "offset": 0.0
            }
        },
        {
            "biome": "minecraft:snowy_slopes",
            "parameters": {
                "temperature": [-1.0, -0.4],
                "humidity": [-0.3, 0.5],
                "continentalness": [0.2, 0.7],
                "erosion": [-0.5, 0.2],
                "weirdness": [-0.3, 0.4],
                "depth": 0,
                "offset": 0.0
            }
        },
        {
            "biome": "minecraft:grove",
            "parameters": {
                "temperature": [-0.7, -0.2],
                "humidity": [0.2, 0.8],
                "continentalness": [0.1, 0.6],
                "erosion": [-0.2, 0.4],
                "weirdness": [-0.4, 0.3],
                "depth": 0,
                "offset": 0.0
            }
        },

        # --- REGION 3: THE COGWORK MARCH (WEST CANYONS & TERRACES) ---
        {
            "biome": "minecraft:windswept_hills",
            "parameters": {
                "temperature": [-0.2, 0.35],
                "humidity": [-0.3, 0.4],
                "continentalness": [0.2, 0.7],
                "erosion": [0.25, 0.85],
                "weirdness": [-0.8, -0.1],
                "depth": 0,
                "offset": 0.0
            }
        },
        {
            "biome": "minecraft:windswept_gravelly_hills",
            "parameters": {
                "temperature": [-0.1, 0.4],
                "humidity": [-0.4, 0.3],
                "continentalness": [0.25, 0.75],
                "erosion": [0.4, 0.9],
                "weirdness": [0.1, 0.7],
                "depth": 0,
                "offset": 0.0
            }
        },
        {
            "biome": "minecraft:river",
            "parameters": {
                "temperature": [-0.2, 0.5],
                "humidity": [0.1, 0.7],
                "continentalness": [0.1, 0.5],
                "erosion": [0.5, 1.0],
                "weirdness": [-0.1, 0.1],
                "depth": 0,
                "offset": 0.0
            }
        },

        # --- REGION 4: THE GILDED DUNES (EAST DESERT & MESAS) ---
        {
            "biome": "minecraft:desert",
            "parameters": {
                "temperature": [0.65, 1.2],
                "humidity": [-1.2, -0.45],
                "continentalness": [0.2, 0.85],
                "erosion": [-0.2, 0.7],
                "weirdness": [-0.5, 0.6],
                "depth": 0,
                "offset": 0.0
            }
        },
        {
            "biome": "minecraft:badlands",
            "parameters": {
                "temperature": [0.6, 1.1],
                "humidity": [-0.7, -0.2],
                "continentalness": [0.3, 0.9],
                "erosion": [-0.6, 0.3],
                "weirdness": [0.2, 0.9],
                "depth": 0,
                "offset": 0.0
            }
        },

        # --- REGION 5: THE WHISPERING FEN (SOUTH-EAST MANGROVE BAYOU) ---
        {
            "biome": "minecraft:swamp",
            "parameters": {
                "temperature": [0.2, 0.75],
                "humidity": [0.45, 1.1],
                "continentalness": [0.1, 0.55],
                "erosion": [0.35, 0.9],
                "weirdness": [-0.5, 0.4],
                "depth": 0,
                "offset": 0.0
            }
        },
        {
            "biome": "minecraft:mangrove_swamp",
            "parameters": {
                "temperature": [0.6, 1.2],
                "humidity": [0.6, 1.2],
                "continentalness": [0.05, 0.45],
                "erosion": [0.4, 1.0],
                "weirdness": [-0.3, 0.5],
                "depth": 0,
                "offset": 0.0
            }
        },

        # --- REGION 6: THE SUNKEN REACH (SOUTH-WEST DROWNED ARCHIPELAGO) ---
        {
            "biome": "minecraft:ocean",
            "parameters": {
                "temperature": [-0.2, 0.5],
                "humidity": [0.0, 0.6],
                "continentalness": [-0.3, 0.08],
                "erosion": [-0.4, 0.6],
                "weirdness": [-0.6, 0.6],
                "depth": 0,
                "offset": 0.0
            }
        },
        {
            "biome": "minecraft:beach",
            "parameters": {
                "temperature": [-0.1, 0.5],
                "humidity": [-0.2, 0.4],
                "continentalness": [-0.08, 0.05],
                "erosion": [0.1, 0.8],
                "weirdness": [-0.5, 0.5],
                "depth": 0,
                "offset": 0.0
            }
        },
        {
            "biome": "minecraft:stony_shore",
            "parameters": {
                "temperature": [-0.4, 0.3],
                "humidity": [-0.3, 0.3],
                "continentalness": [-0.1, 0.1],
                "erosion": [-0.9, -0.1],
                "weirdness": [-0.7, 0.7],
                "depth": 0,
                "offset": 0.0
            }
        },

        # --- REGION 7: THE FORGOTTEN COAST & GREY FRONTIER (SOUTH SPAWN) ---
        {
            "biome": "minecraft:plains",
            "parameters": {
                "temperature": [0.05, 0.45],
                "humidity": [-0.2, 0.35],
                "continentalness": [0.08, 0.5],
                "erosion": [-0.3, 0.4],
                "weirdness": [-0.4, 0.4],
                "depth": 0,
                "offset": 0.0
            }
        },
        {
            "biome": "minecraft:meadow",
            "parameters": {
                "temperature": [-0.1, 0.3],
                "humidity": [0.1, 0.6],
                "continentalness": [0.15, 0.55],
                "erosion": [-0.6, -0.1],
                "weirdness": [-0.5, 0.3],
                "depth": 0,
                "offset": 0.0
            }
        },
        {
            "biome": "minecraft:forest",
            "parameters": {
                "temperature": [0.1, 0.5],
                "humidity": [0.2, 0.7],
                "continentalness": [0.1, 0.6],
                "erosion": [-0.2, 0.5],
                "weirdness": [0.1, 0.7],
                "depth": 0,
                "offset": 0.0
            }
        }
    ]

    overworld_json = {
        "type": "minecraft:overworld",
        "generator": {
            "type": "minecraft:noise",
            "settings": "minecraft:overworld",
            "biome_source": {
                "type": "minecraft:multi_noise",
                "biomes": biomes_config
            }
        }
    }

    overworld_path = os.path.join(data_dir, "overworld.json")
    with open(overworld_path, "w", encoding="utf-8") as f:
        json.dump(overworld_json, f, indent=2)
    print(f"Created {overworld_path} ({len(biomes_config)} multi-noise biomes configured)")

    # 3. Create zip distribution
    zip_path = os.path.join(base_dir, "pack/overrides/datapacks/ashenfall_worldgen.zip")
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(dp_dir):
            for file in files:
                p = os.path.join(root, file)
                rel = os.path.relpath(p, dp_dir)
                zf.write(p, rel)
    print(f"Created {zip_path} ({os.path.getsize(zip_path)} bytes)")

    # 4. Also copy overworld.json to pack/overrides/data/minecraft/dimension/overworld.json (embedded data)
    emb_dir = os.path.join(base_dir, "pack/overrides/data/minecraft/dimension")
    os.makedirs(emb_dir, exist_ok=True)
    shutil.copy2(overworld_path, os.path.join(emb_dir, "overworld.json"))
    print(f"Embedded into {emb_dir}/overworld.json for automatic new world application")

if __name__ == "__main__":
    build_datapack()

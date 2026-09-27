#!/usr/bin/env python3
"""
=============================================================================
ASHENFALL: Clean World Setup for Lithosphere & Still Life
=============================================================================
Sets up the pristine "Ashenfall - The Broken Realm" world save directly in
your Minecraft saves folder.

Eliminates all broken synthetic chunk files so Lithosphere and Still Life
generate the entire world natively with 100% fullness:
  - Dense forests, fallen logs, and wildflowers (Still Life)
  - Smooth mountain ranges & continuous carved river valleys (Lithosphere)
  - 8,000 x 8,000 finite continental world border (The Veil of Salt)
  - Spawn at (0, 68, 2500) on the Forgotten Coast
=============================================================================
"""

import os
import sys
import struct
import gzip
import io
import platform
import shutil
from pathlib import Path


# =============================================================================
# 1. MINECRAFT SAVES DIRECTORY DETECTION (TLauncher + Vanilla + Custom)
# =============================================================================

def get_minecraft_saves_directory():
    """Detect default Minecraft saves directory based on OS, including TLauncher profiles."""
    system = platform.system()
    cwd = Path.cwd()

    if (cwd / "saves").is_dir():
        return (cwd / "saves").resolve()
    if cwd.name in (".minecraft", "game"):
        return (cwd / "saves").resolve()

    if system == "Windows":
        appdata = os.environ.get("APPDATA")
        if appdata:
            appdata_path = Path(appdata)

            # 1. TLauncher / Legacy isolated version instances
            try:
                tlauncher_instances = list(appdata_path.glob(".tlauncher/legacy/Minecraft/game/home/*/saves"))
                if tlauncher_instances:
                    for p in tlauncher_instances:
                        if "neoforge" in p.parent.name.lower() or "1.21" in p.parent.name:
                            return p.resolve()
                    return tlauncher_instances[0].resolve()
            except Exception:
                pass

            # 2. General TLauncher legacy directory
            tlauncher_game = appdata_path / ".tlauncher" / "legacy" / "Minecraft" / "game" / "saves"
            if tlauncher_game.is_dir():
                return tlauncher_game.resolve()

            # 3. Standard vanilla .minecraft
            return (appdata_path / ".minecraft" / "saves").resolve()

    elif system == "Darwin":  # macOS
        return (Path.home() / "Library" / "Application Support" / "minecraft" / "saves").resolve()
    else:  # Linux
        return (Path.home() / ".minecraft" / "saves").resolve()

    return (cwd / "saves").resolve()


# =============================================================================
# 2. PURE-PYTHON NBT SERIALIZER
# =============================================================================

def write_nbt_tag(stream, tag_id, name, val):
    stream.write(bytes([tag_id]))
    name_bytes = name.encode("utf-8")
    stream.write(struct.pack(">H", len(name_bytes)) + name_bytes)
    write_nbt_payload(stream, tag_id, val)

def write_nbt_payload(stream, tag_id, val):
    if tag_id == 1:   stream.write(struct.pack(">b", val))
    elif tag_id == 2: stream.write(struct.pack(">h", val))
    elif tag_id == 3: stream.write(struct.pack(">i", val))
    elif tag_id == 4: stream.write(struct.pack(">q", val))
    elif tag_id == 5: stream.write(struct.pack(">f", val))
    elif tag_id == 6: stream.write(struct.pack(">d", val))
    elif tag_id == 8:
        b = val.encode("utf-8")
        stream.write(struct.pack(">H", len(b)) + b)
    elif tag_id == 9:
        sub_id, items = val
        stream.write(bytes([sub_id]))
        stream.write(struct.pack(">i", len(items)))
        for item in items:
            write_nbt_payload(stream, sub_id, item)
    elif tag_id == 10:
        for k, (t_id, v) in val.items():
            write_nbt_tag(stream, t_id, k, v)
        stream.write(b"\x00")


# =============================================================================
# 3. WORLD INITIALIZER
# =============================================================================

def setup_clean_world(world_dir):
    """Sets up a pristine level.dat without broken synthetic region files."""
    os.makedirs(world_dir, exist_ok=True)

    # Purge old broken synthetic region files if they exist
    region_dir = world_dir / "region"
    if region_dir.is_dir():
        print(" [!] Purging old synthetic chunk files to allow native Lithosphere + Still Life generation...")
        shutil.rmtree(region_dir)

    # Build clean level.dat
    level_dat_path = world_dir / "level.dat"
    level_compound = {
        "Data": (10, {
            "DataVersion": (3, 3955),
            "LevelName": (8, "Ashenfall - The Broken Realm"),
            "generatorName": (8, "default"),
            "generatorVersion": (3, 1),
            "SpawnX": (3, 0),
            "SpawnY": (3, 68),
            "SpawnZ": (3, 2500),
            "version": (3, 19133),
            "initialized": (1, 1),
            "allowCommands": (1, 1),
            "GameType": (3, 0), # Survival
            "Difficulty": (1, 2), # Normal
            "DifficultyLocked": (1, 0),
            "BorderCenterX": (6, 0.0),
            "BorderCenterZ": (6, 0.0),
            "BorderSize": (6, 8000.0),
            "BorderSafeZone": (6, 10.0),
            "BorderDamagePerBlock": (6, 2.0),
            "BorderWarningDistance": (6, 60.0),
            "BorderWarningTime": (6, 10.0),
            "DayTime": (4, 1000),
            "Time": (4, 1000),
            "clearWeatherTime": (3, 60000),
            "rainTime": (3, 0),
            "raining": (1, 0),
            "thunderTime": (3, 0),
            "thundering": (1, 0),
            "WorldGenSettings": (10, {
                "seed": (4, 4815162342),
                "generate_features": (1, 1),
                "bonus_chest": (1, 0)
            }),
            "GameRules": (10, {
                "keepInventory": (8, "false"),
                "doDaylightCycle": (8, "true"),
                "doMobSpawning": (8, "true"),
                "mobGriefing": (8, "true"),
                "doWeatherCycle": (8, "true")
            })
        })
    }

    buf = io.BytesIO()
    write_nbt_tag(buf, 10, "", level_compound)
    with open(level_dat_path, "wb") as f:
        f.write(gzip.compress(buf.getvalue(), compresslevel=9))

    print(f" [✓] Created clean level.dat (Seed: 4815162342, Border: 8000, Spawn: 0, 68, 2500)")

    # Copy world icon if available
    base_dir = Path(__file__).resolve().parent
    icon_src = base_dir / "ASHENFALL_LITHOSPHERE_MAP.png"
    if not icon_src.exists():
        icon_src = base_dir / "ASHENFALL_CONTINENT_MAP.png"
    if not icon_src.exists():
        icon_src = Path("ASHENFALL_LITHOSPHERE_MAP.png")

    if icon_src.exists():
        try:
            from PIL import Image
            img = Image.open(icon_src)
            img.resize((128, 128)).save(world_dir / "icon.png")
            print(f" [✓] Installed satellite map icon (icon.png)")
        except Exception:
            pass


def main():
    print("=" * 70)
    print("   ⚔ ASHENFALL — Native World Setup (Lithosphere + Still Life) ⚔")
    print("=" * 70)

    saves_dir = get_minecraft_saves_directory()
    print(f"\n[1/2] Target Minecraft saves directory:")
    print(f"      {saves_dir}")

    ashenfall_dir = saves_dir / "Ashenfall"
    setup_clean_world(ashenfall_dir)

    print("\n" + "=" * 70)
    print(" [✓] SETUP COMPLETE — NATIVE WORLDGEN RESTORED!")
    print("=" * 70)
    print(f" World Folder:   {ashenfall_dir}")
    print(f" Terrain Engine: Lithosphere (Smooth Splines & Continuous Valleys)")
    print(f" Flora Engine:   Still Life (Dense Trees, Fallen Logs & Wildflowers)")
    print(f" World Border:   8,000 x 8,000 blocks (The Veil of Salt)")
    print(f" Spawn Point:    X: 0, Y: 68, Z: 2500 (The Forgotten Coast)")
    print("-" * 70)
    print(" HOW TO PLAY:")
    print("  1. Open Minecraft 1.21.1 NeoForge.")
    print("  2. Click 'Singleplayer'.")
    print("  3. Select 'Ashenfall - The Broken Realm'.")
    print("  4. Minecraft will now generate all trees, foliage, and valleys natively!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()

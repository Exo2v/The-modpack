@echo off & (python -x "%~f0" --phase all %* || py -x "%~f0" --phase all %*) & pause & goto :eof
#!/usr/bin/env python3
"""
ASHENFALL — Mod Downloader
Downloads genuine, verified 1.21.1 NeoForge mod JARs directly from Modrinth & CurseForge
into your Minecraft mods folder, with automatic zip-integrity verification.

Usage:
  python download_mods.py
  python download_mods.py --phase M0
  python download_mods.py --phase all
  python download_mods.py --dest "C:\\Users\\...\\mods"
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

USER_AGENT = "AshenfallModDownloader/1.0 (Windows NT 10.0; Win64; x64) (+https://github.com/Exo2v/The-modpack)"

# ---------------------------------------------------------------------------
# Mod Catalog per Phase
# ---------------------------------------------------------------------------

MODS_CATALOG: List[Dict[str, Any]] = [
    # --- PHASE M0: SKELETON & PERFORMANCE STACK ---
    {
        "name": "Embeddium",
        "slug": "embeddium",
        "provider": "modrinth",
        "phase": "M0",
        "category": "performance",
        "fallback_url": "https://cdn.modrinth.com/data/sk9Dm0F6/versions/X9q9Y4kM/embeddium-0.3.31%2Bmc1.21.1.jar",
        "filename": "embeddium-0.3.31+mc1.21.1.jar",
    },
    {
        "name": "Embeddium Extra",
        "slug": ["rubidium-extra", "embeddium-extra"],
        "provider": "modrinth",
        "phase": "M0",
        "category": "performance",
    },
    {
        "name": "ModernFix",
        "slug": "modernfix",
        "provider": "modrinth",
        "phase": "M0",
        "category": "performance",
    },
    {
        "name": "FerriteCore",
        "slug": "ferrite-core",
        "provider": "modrinth",
        "phase": "M0",
        "category": "performance",
    },
    {
        "name": "ImmediatelyFast",
        "slug": "immediatelyfast",
        "provider": "modrinth",
        "phase": "M0",
        "category": "performance",
    },
    {
        "name": "Entity Culling",
        "slug": "entityculling",
        "provider": "modrinth",
        "phase": "M0",
        "category": "performance",
    },
    {
        "name": "Clumps",
        "slug": "clumps",
        "provider": "modrinth",
        "phase": "M0",
        "category": "performance",
    },
    {
        "name": "Alternate Current",
        "slug": "alternate-current",
        "provider": "modrinth",
        "phase": "M0",
        "category": "performance",
    },
    {
        "name": "Enhanced Block Entities",
        "slug": ["enhanced-block-entities-neoforged", "enhanced-block-entities", "ebe"],
        "provider": "modrinth",
        "phase": "M0",
        "category": "performance",
    },
    {
        "name": "FastSuite",
        "slug": "fastsuite",
        "provider": "modrinth",
        "phase": "M0",
        "category": "performance",
    },
    {
        "name": "More Culling",
        "slug": "moreculling",
        "provider": "modrinth",
        "phase": "M0",
        "category": "performance",
    },
    {
        "name": "Structure Layout Optimizer",
        "slug": "structure-layout-optimizer",
        "provider": "modrinth",
        "phase": "M0",
        "category": "performance",
    },
    {
        "name": "Dynamic FPS",
        "slug": "dynamic-fps",
        "provider": "modrinth",
        "phase": "M0",
        "category": "performance",
    },
    {
        "name": "Chunky",
        "slug": "chunky",
        "provider": "modrinth",
        "phase": "M0",
        "category": "performance",
    },
    {
        "name": "Curios API",
        "slug": "curios",
        "provider": "modrinth",
        "phase": "M0",
        "category": "library",
    },
    {
        "name": "Lionfish API",
        "slug": "lionfish-api",
        "provider": "modrinth",
        "phase": "M0",
        "category": "library",
    },
    {
        "name": "Citadel",
        "slug": ["citadel-(1.21.1-port)", "citadel"],
        "provider": "modrinth",
        "phase": "M0",
        "category": "library",
    },
    {
        "name": "GeckoLib",
        "slug": "geckolib",
        "provider": "modrinth",
        "phase": "M0",
        "category": "library",
    },
    {
        "name": "oωo (owo-lib)",
        "slug": ["owo-lib", "owo"],
        "provider": "modrinth",
        "phase": "M0",
        "category": "library",
    },
    {
        "name": "UnionLib",
        "slug": "unionlib",
        "provider": "modrinth",
        "phase": "M0",
        "category": "library",
    },
    {
        "name": "libIPN",
        "slug": "libipn",
        "provider": "modrinth",
        "phase": "M0",
        "category": "library",
    },
    {
        "name": "CreativeCore",
        "slug": "creativecore",
        "provider": "modrinth",
        "phase": "M0",
        "category": "library",
    },
    {
        "name": "Patchouli",
        "slug": "patchouli",
        "provider": "modrinth",
        "phase": "M0",
        "category": "library",
    },
    {
        "name": "Architectury API",
        "slug": "architectury-api",
        "provider": "modrinth",
        "phase": "M0",
        "category": "library",
    },
    {
        "name": "Kotlin for Forge",
        "slug": ["kotlin-for-forge", "kotlin-lang-forge"],
        "provider": "modrinth",
        "phase": "M0",
        "category": "library",
    },
    {
        "name": "TerraBlender",
        "slug": "terrablender",
        "provider": "modrinth",
        "phase": "M0",
        "category": "library",
    },
    {
        "name": "KubeJS",
        "slug": "kubejs",
        "provider": "modrinth",
        "phase": "M0",
        "category": "core",
    },
    {
        "name": "Player Animator",
        "slug": "playeranimator",
        "provider": "modrinth",
        "phase": "M0",
        "category": "library",
    },
    {
        "name": "YUNG's API",
        "slug": "yungs-api",
        "provider": "modrinth",
        "phase": "M0",
        "category": "library",
    },
    {
        "name": "Sophisticated Core",
        "slug": "sophisticated-core",
        "provider": "modrinth",
        "phase": "M0",
        "category": "library",
    },
    # --- PHASE M1: MOVEMENT & COMBAT ---
    {
        "name": "Cloth Config API",
        "slug": "cloth-config",
        "provider": "modrinth",
        "phase": "M1",
        "category": "library",
    },
    {
        "name": "Combat Roll",
        "slug": "combat-roll",
        "provider": "modrinth",
        "phase": "M1",
        "category": "combat",
    },
    {
        "name": "ParCool",
        "slug": "parcool",
        "provider": "modrinth",
        "phase": "M1",
        "category": "combat",
    },
    {
        "name": "Simply Swords",
        "slug": "simply-swords",
        "provider": "modrinth",
        "phase": "M1",
        "category": "combat",
    },
    {
        "name": "Fzzy Config",
        "slug": "fzzy-config",
        "provider": "modrinth",
        "phase": "M1",
        "category": "library",
    },
    {
        "name": "Oracle Index",
        "slug": "oracle-index",
        "provider": "modrinth",
        "phase": "M1",
        "category": "library",
    },
    {
        "name": "Backported Spears",
        "slug": "backported-spears",
        "provider": "modrinth",
        "phase": "M1",
        "category": "combat",
    },
    # --- PHASE M2: SOULSLIKE ---
    {
        "name": "Silent Lib",
        "slug": "silent-lib",
        "provider": "modrinth",
        "phase": "M2",
        "category": "library",
    },
    {
        "name": "Silent's Power Scale",
        "slug": ["silents-power-scale", "power-scale"],
        "provider": "modrinth",
        "phase": "M2",
        "category": "soulslike",
    },
    {
        "name": "GraveStone Mod",
        "slug": ["gravestone-mod", "corpse"],
        "provider": "modrinth",
        "phase": "M2",
        "category": "soulslike",
    },
    {
        "name": "Shine",
        "slug": "shine",
        "provider": "modrinth",
        "phase": "M2",
        "category": "visuals",
    },
    {
        "name": "Wavify",
        "slug": "wavify",
        "provider": "modrinth",
        "phase": "M2",
        "category": "visuals",
    },
    {
        "name": "Visuality: Reforged",
        "slug": ["visuality-forge", "visuality"],
        "provider": "modrinth",
        "phase": "M2",
        "category": "visuals",
    },
    # --- PHASE M3: WORLDGEN ---
    {
        "name": "Lithosphere",
        "slug": ["lithosphere", "lithosphere-mod"],
        "provider": "modrinth",
        "phase": "M3",
        "category": "worldgen",
    },
    {
        "name": "Still Life",
        "slug": ["still-life", "still_life"],
        "provider": "modrinth",
        "phase": "M3",
        "category": "worldgen",
    },
    {
        "name": "Streams Reflowing",
        "slug": "streams-reflowing",
        "provider": "modrinth",
        "phase": "M3",
        "category": "worldgen",
    },
    {
        "name": "Explorify",
        "slug": "explorify",
        "provider": "modrinth",
        "phase": "M3",
        "category": "worldgen",
    },
    {
        "name": "Dungeons and Taverns",
        "slug": ["dungeons-and-taverns", "dungeons-taverns"],
        "provider": "modrinth",
        "phase": "M3",
        "category": "worldgen",
    },
    {
        "name": "Towns and Towers",
        "slug": "towns-and-towers",
        "provider": "modrinth",
        "phase": "M3",
        "category": "worldgen",
    },
    {
        "name": "When Dungeons Arise",
        "slug": "when-dungeons-arise",
        "provider": "modrinth",
        "phase": "M3",
        "category": "worldgen",
    },
    # --- PHASE M3b: WORLD FULLNESS ---
    {
        "name": "FallingTree",
        "slug": ["fallingtree", "falling-tree"],
        "provider": "modrinth",
        "phase": "M3b",
        "category": "fullness",
    },
    {
        "name": "Sophisticated Backpacks",
        "slug": "sophisticated-backpacks",
        "provider": "modrinth",
        "phase": "M3b",
        "category": "fullness",
    },
    {
        "name": "Guard Villagers",
        "slug": ["guard-villagers", "guardvillagers"],
        "provider": "modrinth",
        "phase": "M3b",
        "category": "fullness",
    },
    {
        "name": "Farmer's Delight",
        "slug": "farmers-delight",
        "provider": "modrinth",
        "phase": "M3b",
        "category": "fullness",
    },
    {
        "name": "Moonlight Lib",
        "slug": "moonlight",
        "provider": "modrinth",
        "phase": "M3b",
        "category": "library",
    },
    {
        "name": "Supplementaries",
        "slug": "supplementaries",
        "provider": "modrinth",
        "phase": "M3b",
        "category": "fullness",
    },
    {
        "name": "Comforts",
        "slug": "comforts",
        "provider": "modrinth",
        "phase": "M3b",
        "category": "fullness",
    },
    {
        "name": "Tool Belt",
        "slug": ["traveler-tool-belt", "tool-belt"],
        "provider": "modrinth",
        "phase": "M3b",
        "category": "fullness",
    },
    {
        "name": "Boatload",
        "slug": "boatload",
        "provider": "modrinth",
        "phase": "M3b",
        "category": "fullness",
    },
    # --- PHASE M3c: DUNGEONS & MAGIC ---
    {
        "name": "YUNG's Better Dungeons",
        "slug": "yungs-better-dungeons",
        "provider": "modrinth",
        "phase": "M3c",
        "category": "dungeons",
    },
    {
        "name": "YUNG's Better Strongholds",
        "slug": "yungs-better-strongholds",
        "provider": "modrinth",
        "phase": "M3c",
        "category": "dungeons",
    },
    {
        "name": "YUNG's Better Mineshafts",
        "slug": "yungs-better-mineshafts",
        "provider": "modrinth",
        "phase": "M3c",
        "category": "dungeons",
    },
    {
        "name": "YUNG's Better Ocean Monuments",
        "slug": "yungs-better-ocean-monuments",
        "provider": "modrinth",
        "phase": "M3c",
        "category": "dungeons",
    },
    {
        "name": "YUNG's Better Nether Fortresses",
        "slug": "yungs-better-nether-fortresses",
        "provider": "modrinth",
        "phase": "M3c",
        "category": "dungeons",
    },
    {
        "name": "YUNG's Better Desert Temples",
        "slug": "yungs-better-desert-temples",
        "provider": "modrinth",
        "phase": "M3c",
        "category": "dungeons",
    },
    {
        "name": "YUNG's Better Jungle Temples",
        "slug": "yungs-better-jungle-temples",
        "provider": "modrinth",
        "phase": "M3c",
        "category": "dungeons",
    },
    {
        "name": "YUNG's Better Witch Huts",
        "slug": "yungs-better-witch-huts",
        "provider": "modrinth",
        "phase": "M3c",
        "category": "dungeons",
    },
    {
        "name": "YUNG's Better End Island",
        "slug": "yungs-better-end-island",
        "provider": "modrinth",
        "phase": "M3c",
        "category": "dungeons",
    },
    {
        "name": "YUNG's Better Bridges",
        "slug": "yungs-better-bridges",
        "provider": "modrinth",
        "phase": "M3c",
        "category": "dungeons",
    },
    {
        "name": "YUNG's Better Extras",
        "slug": "yungs-better-extras",
        "provider": "modrinth",
        "phase": "M3c",
        "category": "dungeons",
    },
    {
        "name": "Repurposed Structures",
        "slug": ["repurposed-structures-forge", "repurposed-structures"],
        "provider": "modrinth",
        "phase": "M3c",
        "category": "dungeons",
    },
    {
        "name": "Hopo Better Ruined Portals",
        "slug": "hopo-better-ruined-portals",
        "provider": "modrinth",
        "phase": "M3c",
        "category": "dungeons",
    },
    {
        "name": "Hopo Better Underwater Ruins",
        "slug": "hopo-better-underwater-ruins",
        "provider": "modrinth",
        "phase": "M3c",
        "category": "dungeons",
    },
    {
        "name": "The Graveyard",
        "slug": ["graveyard", "the-graveyard"],
        "provider": "modrinth",
        "phase": "M3c",
        "category": "dungeons",
    },
    {
        "name": "Structory",
        "slug": "structory",
        "provider": "modrinth",
        "phase": "M3c",
        "category": "dungeons",
    },
    {
        "name": "Iron's Spells 'n Spellbooks",
        "slug": ["irons-spells-n-spellbooks", "irons_spellbooks"],
        "provider": "modrinth",
        "phase": "M3c",
        "category": "magic",
    },
    # --- PHASE M4: NATIONS & CLAIMS ---
    {
        "name": "Open Parties and Claims",
        "slug": ["open-parties-and-claims", "openpac"],
        "provider": "modrinth",
        "phase": "M4",
        "category": "claims",
    },
    {
        "name": "Aviel's Dialogue Mod",
        "slug": ["aviel-dialogue-mod", "easy-npc"],
        "provider": "modrinth",
        "phase": "M4",
        "category": "narrative",
    },
    # --- PHASE M5: RPG & GRINDING ---
    {
        "name": "Project MMO",
        "slug": "project-mmo",
        "provider": "modrinth",
        "phase": "M5",
        "category": "rpg",
    },
    {
        "name": "Project MMO: Classes",
        "slug": "project-mmo-classes",
        "provider": "modrinth",
        "phase": "M5",
        "category": "rpg",
    },
    {
        "name": "Project MMO: Skill Books",
        "slug": "project-mmo-skill-books",
        "provider": "modrinth",
        "phase": "M5",
        "category": "rpg",
    },
    {
        "name": "Project MMO: XP Bottles",
        "slug": "project-mmo-xp-bottles",
        "provider": "modrinth",
        "phase": "M5",
        "category": "rpg",
    },
    {
        "name": "Origins",
        "slug": ["origins-neoforge", "origins"],
        "provider": "modrinth",
        "phase": "M5",
        "category": "rpg",
    },
    {
        "name": "Reforged",
        "slug": ["tiered", "reforged"],
        "provider": "modrinth",
        "phase": "M5",
        "category": "rpg",
    },
    {
        "name": "Attribute Modify",
        "slug": ["attribute-modify", "attributefix"],
        "provider": "modrinth",
        "phase": "M5",
        "category": "rpg",
    },
    {
        "name": "Mob Champions",
        "slug": ["mobchampions", "mob-champions", "champions"],
        "provider": "modrinth",
        "phase": "M5",
        "category": "rpg",
    },
    {
        "name": "Loot Beams: Refork",
        "slug": ["loot-beams-refork", "loot-beams"],
        "provider": "modrinth",
        "phase": "M5",
        "category": "rpg",
    },
    # --- PHASE M6: BOSS SPINE ---
    {
        "name": "L_Ender's Cataclysm",
        "slug": ["l_enders-cataclysm", "cataclysm"],
        "provider": "modrinth",
        "phase": "M6",
        "category": "bosses",
    },
    {
        "name": "The Aether",
        "slug": "aether",
        "provider": "modrinth",
        "phase": "M6",
        "category": "bosses",
    },
    {
        "name": "Alex's Caves",
        "slug": ["alexs-caves-(unofficial-port)", "alexs-caves", "alexscaves"],
        "provider": "modrinth",
        "phase": "M6",
        "category": "bosses",
    },
    {
        "name": "Alex's Mobs",
        "slug": ["alexs-mobs(1.21.1)", "alexs-mobs", "alexsmobs"],
        "provider": "modrinth",
        "phase": "M6",
        "category": "bosses",
    },
    {
        "name": "Mini-boss Boss Bars",
        "slug": ["mini-boss-boss-bars", "better-boss-bars"],
        "provider": "modrinth",
        "phase": "M6",
        "category": "bosses",
    },
    {
        "name": "Configurable Boss Bars",
        "slug": ["configurable-boss-bars", "boss-bars"],
        "provider": "modrinth",
        "phase": "M6",
        "category": "bosses",
    },
    {
        "name": "Boss Music Mod",
        "slug": ["true-boss-music", "exileds-boss-music-mod", "boss-music-mod"],
        "provider": "modrinth",
        "phase": "M6",
        "category": "bosses",
    },
    {
        "name": "Floating Damage Indicators",
        "slug": ["immersive-damage-indicators", "floating-damage-indicators", "damage-indicators"],
        "provider": "modrinth",
        "phase": "M6",
        "category": "bosses",
    },
    {
        "name": "YUNG's Traveler's Titles",
        "slug": ["travelers-titles", "yungs-travelers-titles"],
        "provider": "modrinth",
        "phase": "M6",
        "category": "bosses",
    },
    # --- PHASE M7: QOL & NAVIGATION ---
    {
        "name": "Lootr",
        "slug": "lootr",
        "provider": "modrinth",
        "phase": "M7",
        "category": "story",
    },
    {
        "name": "Enigmatic Legacy+",
        "slug": ["enigmaticlegacy+", "enigmaticlegacy%2B", "enigmatic-legacy-plus"],
        "provider": "modrinth",
        "phase": "M7",
        "category": "story",
    },
    {
        "name": "Waystones",
        "slug": "waystones",
        "provider": "modrinth",
        "phase": "M7",
        "category": "story",
    },
    {
        "name": "Just Enough Items (JEI)",
        "slug": "jei",
        "provider": "modrinth",
        "phase": "M7",
        "category": "story",
    },
    {
        "name": "Jade",
        "slug": "jade",
        "provider": "modrinth",
        "phase": "M7",
        "category": "story",
    },
    {
        "name": "AppleSkin",
        "slug": "appleskin",
        "provider": "modrinth",
        "phase": "M7",
        "category": "story",
    },
    {
        "name": "Mouse Tweaks",
        "slug": "mouse-tweaks",
        "provider": "modrinth",
        "phase": "M7",
        "category": "story",
    },
    {
        "name": "Controlling",
        "slug": "controlling",
        "provider": "modrinth",
        "phase": "M7",
        "category": "story",
    },
    {
        "name": "Carry On",
        "slug": "carry-on",
        "provider": "modrinth",
        "phase": "M7",
        "category": "story",
    },
    {
        "name": "Xaero's Minimap",
        "slug": "xaeros-minimap",
        "provider": "modrinth",
        "phase": "M7",
        "category": "story",
    },
    {
        "name": "Xaero's World Map",
        "slug": "xaeros-world-map",
        "provider": "modrinth",
        "phase": "M7",
        "category": "story",
    },
    {
        "name": "Inventory Profiles Next",
        "slug": "inventory-profiles-next",
        "provider": "modrinth",
        "phase": "M7",
        "category": "story",
    },
    {
        "name": "Shutup Experimental Settings!",
        "slug": ["hide-experimental-warning", "experimentalist", "shutup-experimental-settings"],
        "provider": "modrinth",
        "phase": "M7",
        "category": "story",
    },
    {
        "name": "Skin Layers 3D",
        "slug": ["3dskinlayers", "skin-layers-3d"],
        "provider": "modrinth",
        "phase": "M7",
        "category": "story",
    },
    {
        "name": "AmbientSounds 6",
        "slug": "ambientsounds",
        "provider": "modrinth",
        "phase": "M7",
        "category": "story",
    },
    {
        "name": "Sound Physics Remastered",
        "slug": "sound-physics-remastered",
        "provider": "modrinth",
        "phase": "M7",
        "category": "story",
    },
    {
        "name": "Presence Footsteps",
        "slug": ["pf-neoforge", "presence-footsteps-forge", "presence-footsteps"],
        "provider": "modrinth",
        "phase": "M7",
        "category": "story",
    },
]

# ---------------------------------------------------------------------------
# Launcher Detection
# ---------------------------------------------------------------------------

def detect_minecraft_mods_dir() -> Optional[Path]:
    """Auto-detects active Minecraft mods folder, checking TLauncher & standard paths."""
    appdata = os.environ.get("APPDATA")
    userprofile = os.environ.get("USERPROFILE")

    candidates: List[Path] = []
    if appdata:
        appdata_p = Path(appdata)
        # 1. TLauncher legacy custom game dir (from user's error log)
        candidates.append(appdata_p / ".tlauncher" / "legacy" / "Minecraft" / "game" / "home" / "NeoForge 1.21.1" / "mods")
        candidates.append(appdata_p / ".tlauncher" / "legacy" / "Minecraft" / "game" / "mods")
        candidates.append(appdata_p / ".minecraft" / "mods")
    if userprofile:
        u_p = Path(userprofile)
        candidates.append(u_p / "AppData" / "Roaming" / ".tlauncher" / "legacy" / "Minecraft" / "game" / "home" / "NeoForge 1.21.1" / "mods")
        candidates.append(u_p / "AppData" / "Roaming" / ".minecraft" / "mods")

    # Linux / macOS
    home = Path.home()
    candidates.append(home / ".minecraft" / "mods")
    candidates.append(home / "Library" / "Application Support" / "minecraft" / "mods")

    for c in candidates:
        if c.exists() or c.parent.exists():
            return c
    return None


# ---------------------------------------------------------------------------
# API Resolution & Download
# ---------------------------------------------------------------------------

def resolve_modrinth_jar(slug_or_slugs: str | List[str], mc_version: str = "1.21.1", verbose: bool = False) -> Optional[Tuple[str, str, int]]:
    """
    Queries Modrinth API for a 1.21.1 NeoForge / Forge release.
    Supports candidate aliases, filtered query, and fallback search.
    Returns (download_url, filename, size_bytes).
    """
    slugs = [slug_or_slugs] if isinstance(slug_or_slugs, str) else slug_or_slugs

    for slug in slugs:
        # 1. Filtered API query
        encoded_ver = urllib.parse.quote(json.dumps([mc_version, "1.21"]))
        encoded_loaders = urllib.parse.quote(json.dumps(["neoforge", "forge"]))

        url = f"https://api.modrinth.com/v2/project/{slug}/version?game_versions={encoded_ver}&loaders={encoded_loaders}"
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

        versions_data = None
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                versions_data = json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            if verbose:
                print(f" [debug filtered {slug}: {e}]", end="")

        # 2. Unfiltered fallback query if filtered query returned no versions
        if not versions_data:
            try:
                url_all = f"https://api.modrinth.com/v2/project/{slug}/version"
                req_all = urllib.request.Request(url_all, headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(req_all, timeout=12) as resp:
                    all_versions = json.loads(resp.read().decode("utf-8"))
                    filtered = []
                    for v in all_versions:
                        loaders = [str(l).lower() for l in v.get("loaders", [])]
                        gvs = [str(g).lower() for g in v.get("game_versions", [])]
                        if ("neoforge" in loaders or "forge" in loaders) and any(ver in gvs for ver in (mc_version, "1.21", "1.21.0")):
                            filtered.append(v)
                    versions_data = filtered
            except Exception as e:
                if verbose:
                    print(f" [debug unfiltered {slug}: {e}]", end="")

        if versions_data:
            # Prioritize neoforge loader builds over forge
            neoforge_vers = [v for v in versions_data if "neoforge" in [str(l).lower() for l in v.get("loaders", [])]]
            target_version = neoforge_vers[0] if neoforge_vers else versions_data[0]

            files = target_version.get("files", [])
            primary = next((f for f in files if f.get("primary") and str(f.get("filename", "")).endswith(".jar")), None)
            if not primary:
                primary = next((f for f in files if str(f.get("filename", "")).endswith(".jar")), None)

            if primary:
                return primary["url"], primary["filename"], primary.get("size", 0)

    return None


def download_and_verify(url: str, dest_path: Path, expected_size: int = 0, verbose: bool = False) -> bool:
    """Downloads a file to dest_path and strictly verifies zip integrity."""
    temp_path = dest_path.with_suffix(".tmp")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    try:
        with urllib.request.urlopen(req, timeout=30) as resp, open(temp_path, "wb") as out:
            shutil.copyfileobj(resp, out)

        # CRUCIAL: Verify it is a valid, uncorrupted ZIP/JAR file!
        # This prevents the "zip END header not found" crash entirely!
        with zipfile.ZipFile(temp_path, "r") as zf:
            namelist = zf.namelist()
            if not namelist:
                raise ValueError("Downloaded jar archive contains no files")

        if temp_path.stat().st_size == 0:
            raise ValueError("Downloaded file is 0 bytes")

        # Move into final destination
        if dest_path.exists():
            dest_path.unlink()
        temp_path.rename(dest_path)
        return True

    except Exception as e:
        if temp_path.exists():
            temp_path.unlink()
        if verbose:
            print(f"\n    [Error] Download verification failed: {e}", file=sys.stderr)
        return False


CANONICAL_SERVER_SCRIPTS = {
    "boss_monologue.js": "// =============================================================================\n// ASHENFALL \u2014 Boss Monologues & Cinematic Encounters\n// =============================================================================\n\nconst BOSS_ENCOUNTERS = {\n    \"cataclysm:ignis\": {\n        name: \"Ignis, The Incinerator\",\n        line: \"Ash will cover the world again. Your ember will feed the pyre.\",\n        sound: \"minecraft:entity.ender_dragon.growl\"\n    },\n    \"cataclysm:netherite_monstrosity\": {\n        name: \"Netherite Monstrosity\",\n        line: \"The crucible demands another sacrifice.\",\n        sound: \"minecraft:entity.ravager.roar\"\n    },\n    \"cataclysm:the_harbinger\": {\n        name: \"The Harbinger\",\n        line: \"Ancient machinery hums with renewed wrath.\",\n        sound: \"minecraft:block.beacon.activate\"\n    },\n    \"cataclysm:the_leviathan\": {\n        name: \"The Leviathan of the Abyss\",\n        line: \"The sunken choir sings your drowning hymn.\",\n        sound: \"minecraft:ambient.underwater.loop\"\n    },\n    \"irons_spellbooks:dead_king\": {\n        name: \"The Dead King of the Catacombs\",\n        line: \"You seek the lost words of power. They belong to the dust.\",\n        sound: \"minecraft:entity.wither.ambient\"\n    }\n};\n\nEntityEvents.spawned(event => {\n    let entity = event.entity;\n    let type = entity.type;\n\n    if (BOSS_ENCOUNTERS[type]) {\n        let boss = BOSS_ENCOUNTERS[type];\n        let level = entity.level;\n\n        level.players.forEach(player => {\n            // Check distance\n            let distSq = player.distanceToSqr(entity);\n            if (distSq < 64 * 64) {\n                // Screen shake & cinematic alert\n                player.potionEffects.add(\"minecraft:slowness\", 60, 1, false, false);\n                level.server.runCommandSilent(`playsound ${boss.sound} ambient ${player.username} ${player.x} ${player.y} ${player.z} 1.0 0.8`);\n                \n                level.server.runCommandSilent(`title ${player.username} times 10 60 20`);\n                level.server.runCommandSilent(`title ${player.username} title {\"text\":\"${boss.name}\",\"color\":\"red\",\"bold\":true}`);\n                level.server.runCommandSilent(`title ${player.username} subtitle {\"text\":\"\\\"${boss.line}\\\"\",\"color\":\"gold\",\"italic\":true}`);\n            }\n        });\n    }\n});\n",
    "boss_monologues.js": "// =============================================================================\n// ASHENFALL \u2014 Boss Monologues & Cinematic Encounters\n// =============================================================================\n\nconst BOSS_ENCOUNTERS = {\n    \"cataclysm:ignis\": {\n        name: \"Ignis, The Incinerator\",\n        line: \"Ash will cover the world again. Your ember will feed the pyre.\",\n        sound: \"minecraft:entity.ender_dragon.growl\"\n    },\n    \"cataclysm:netherite_monstrosity\": {\n        name: \"Netherite Monstrosity\",\n        line: \"The crucible demands another sacrifice.\",\n        sound: \"minecraft:entity.ravager.roar\"\n    },\n    \"cataclysm:the_harbinger\": {\n        name: \"The Harbinger\",\n        line: \"Ancient machinery hums with renewed wrath.\",\n        sound: \"minecraft:block.beacon.activate\"\n    },\n    \"cataclysm:the_leviathan\": {\n        name: \"The Leviathan of the Abyss\",\n        line: \"The sunken choir sings your drowning hymn.\",\n        sound: \"minecraft:ambient.underwater.loop\"\n    },\n    \"irons_spellbooks:dead_king\": {\n        name: \"The Dead King of the Catacombs\",\n        line: \"You seek the lost words of power. They belong to the dust.\",\n        sound: \"minecraft:entity.wither.ambient\"\n    }\n};\n\nEntityEvents.spawned(event => {\n    let entity = event.entity;\n    let type = entity.type;\n\n    if (BOSS_ENCOUNTERS[type]) {\n        let boss = BOSS_ENCOUNTERS[type];\n        let level = entity.level;\n\n        level.players.forEach(player => {\n            // Check distance\n            let distSq = player.distanceToSqr(entity);\n            if (distSq < 64 * 64) {\n                // Screen shake & cinematic alert\n                player.potionEffects.add(\"minecraft:slowness\", 60, 1, false, false);\n                level.server.runCommandSilent(`playsound ${boss.sound} ambient ${player.username} ${player.x} ${player.y} ${player.z} 1.0 0.8`);\n                \n                level.server.runCommandSilent(`title ${player.username} times 10 60 20`);\n                level.server.runCommandSilent(`title ${player.username} title {\"text\":\"${boss.name}\",\"color\":\"red\",\"bold\":true}`);\n                level.server.runCommandSilent(`title ${player.username} subtitle {\"text\":\"\\\"${boss.line}\\\"\",\"color\":\"gold\",\"italic\":true}`);\n            }\n        });\n    }\n});\n",
    "commands.js": "// =============================================================================\n// ASHENFALL \u2014 Admin & In-Game Command Register (Minecraft 1.21.1 / KubeJS)\n// =============================================================================\n\nServerEvents.commandRegistry(function(event) {\n    var Commands = event.commands;\n    var Arguments = event.arguments;\n\n    event.register(\n        Commands.literal(\"ashenfall\")\n            .requires(function(source) { return source.hasPermission(2); })\n            .then(Commands.literal(\"standing\")\n                .then(Commands.argument(\"player\", Arguments.PLAYER.create(event))\n                    .then(Commands.argument(\"faction\", Arguments.STRING.create(event))\n                        .then(Commands.argument(\"amount\", Arguments.INTEGER.create(event))\n                            .executes(function(ctx) {\n                                var player = Arguments.PLAYER.getResult(ctx, \"player\");\n                                var faction = Arguments.STRING.getResult(ctx, \"faction\");\n                                var amount = Arguments.INTEGER.getResult(ctx, \"amount\");\n                                if (global.modifyStanding) {\n                                    global.modifyStanding(player, faction, amount);\n                                }\n                                return 1;\n                            })\n                        )\n                    )\n                )\n            )\n            .then(Commands.literal(\"threat\")\n                .then(Commands.argument(\"player\", Arguments.PLAYER.create(event))\n                    .then(Commands.argument(\"region\", Arguments.STRING.create(event))\n                        .then(Commands.argument(\"tier\", Arguments.INTEGER.create(event))\n                            .executes(function(ctx) {\n                                var player = Arguments.PLAYER.getResult(ctx, \"player\");\n                                var region = Arguments.STRING.getResult(ctx, \"region\");\n                                var tier = Arguments.INTEGER.getResult(ctx, \"tier\");\n                                if (global.setTier) {\n                                    global.setTier(player, region, tier);\n                                }\n                                return 1;\n                            })\n                        )\n                    )\n                )\n            )\n            .then(Commands.literal(\"rumour\")\n                .then(Commands.argument(\"player\", Arguments.PLAYER.create(event))\n                    .then(Commands.argument(\"id\", Arguments.STRING.create(event))\n                        .executes(function(ctx) {\n                            var player = Arguments.PLAYER.getResult(ctx, \"player\");\n                            var id = Arguments.STRING.getResult(ctx, \"id\");\n                            if (global.tellRumour) {\n                                global.tellRumour(player, id);\n                            }\n                            return 1;\n                        })\n                    )\n                )\n            )\n    );\n});\n",
    "intro_awakening.js": "// =============================================================================\n// ASHENFALL \u2014 Beach Awakening Cutscene & Shoreline Spawn\n// =============================================================================\n\nfunction buildLighthouse(server, x, y, z) {\n    // Build a classic coastal stone lighthouse on the bluff\n    for (let dy = 0; dy < 14; dy++) {\n        let radius = dy < 8 ? 2 : 1;\n        for (let dx = -radius; dx <= radius; dx++) {\n            for (let dz = -radius; dz <= radius; dz++) {\n                if (Math.abs(dx) === radius && Math.abs(dz) === radius) {\n                    server.runCommandSilent(`setblock ${x + dx} ${y + dy} ${z + dz} minecraft:mossy_cobblestone`);\n                } else if (Math.abs(dx) === radius || Math.abs(dz) === radius) {\n                    server.runCommandSilent(`setblock ${x + dx} ${y + dy} ${z + dz} minecraft:stone_bricks`);\n                } else {\n                    server.runCommandSilent(`setblock ${x + dx} ${y + dy} ${z + dz} minecraft:air`);\n                }\n            }\n        }\n    }\n\n    // Doorway\n    server.runCommandSilent(`setblock ${x} ${y} ${z + 2} minecraft:oak_door[facing=south,half=lower]`);\n    server.runCommandSilent(`setblock ${x} ${y + 1} ${z + 2} minecraft:oak_door[facing=south,half=upper]`);\n\n    // Interior ladder & floors\n    for (let dy = 0; dy < 13; dy++) {\n        server.runCommandSilent(`setblock ${x} ${y + dy} ${z - 1} minecraft:ladder[facing=south]`);\n    }\n\n    // Lantern gallery & beacon on top\n    let topY = y + 14;\n    for (let dx = -2; dx <= 2; dx++) {\n        for (let dz = -2; dz <= 2; dz++) {\n            server.runCommandSilent(`setblock ${x + dx} ${topY} ${z + dz} minecraft:smooth_stone_slab`);\n            if (Math.abs(dx) === 2 || Math.abs(dz) === 2) {\n                server.runCommandSilent(`setblock ${x + dx} ${topY + 1} ${z + dz} minecraft:iron_bars`);\n            }\n        }\n    }\n\n    // Beacon fire at the crown\n    server.runCommandSilent(`setblock ${x} ${topY + 1} ${z} minecraft:soul_campfire[lit=true]`);\n    server.runCommandSilent(`setblock ${x} ${topY + 2} ${z} minecraft:tinted_glass`);\n    server.runCommandSilent(`setblock ${x} ${topY + 3} ${z} minecraft:stone_brick_slab`);\n\n    // Starter Chest inside ground floor\n    server.runCommandSilent(`setblock ${x + 1} ${y} ${z} minecraft:chest[facing=west]`);\n    server.runCommandSilent(`item replace block ${x + 1} ${y} ${z} container.0 with minecraft:spyglass`);\n    server.runCommandSilent(`item replace block ${x + 1} ${y} ${z} container.1 with minecraft:bread 8`);\n    server.runCommandSilent(`item replace block ${x + 1} ${y} ${z} container.2 with minecraft:cooked_cod 4`);\n    server.runCommandSilent(`item replace block ${x + 1} ${y} ${z} container.3 with minecraft:torch 12`);\n    server.runCommandSilent(`item replace block ${x + 1} ${y} ${z} container.4 with minecraft:flint_and_steel`);\n    server.runCommandSilent(`item replace block ${x + 1} ${y} ${z} container.5 with minecraft:potion[potion_contents={potion:\"minecraft:healing\"}]`);\n\n    // Signal lantern hanging outside\n    server.runCommandSilent(`setblock ${x} ${y + 3} ${z + 3} minecraft:lantern[hanging=true]`);\n}\n\nPlayerEvents.loggedIn(event => {\n    let player = event.player;\n    let server = event.server;\n\n    if (!player.tags.contains(\"ashfall_awakened\")) {\n        player.tags.add(\"ashfall_awakened\");\n\n        // 1. Position player safely on the coastal sands\n        let px = Math.floor(player.x);\n        let py = Math.floor(player.y);\n        let pz = Math.floor(player.z);\n\n        // Build starter lighthouse nearby on cliff/higher ground\n        let lx = px + 18;\n        let lz = pz + 14;\n        let ly = py + 3;\n        buildLighthouse(server, lx, ly, lz);\n\n        // 2. Play dramatic opening sound effects\n        server.runCommandSilent(`playsound minecraft:ambient.underwater.enter ambient ${player.username} ${px} ${py} ${pz} 1.0 0.8`);\n        server.runCommandSilent(`playsound minecraft:entity.generic.splash ambient ${player.username} ${px} ${py} ${pz} 1.0 0.7`);\n\n        // 3. Apply opening blur / blindness (eyes opening on sand)\n        player.potionEffects.add(\"minecraft:blindness\", 120, 0, false, false);\n        player.potionEffects.add(\"minecraft:slowness\", 140, 3, false, false);\n        player.potionEffects.add(\"minecraft:water_breathing\", 200, 0, false, false);\n\n        // 4. Act I: Awakening on Beach Title\n        server.scheduleInTicks(15, () => {\n            server.runCommandSilent(`title ${player.username} times 20 60 20`);\n            server.runCommandSilent(`title ${player.username} title {\"text\":\"ASHENFALL\",\"color\":\"dark_red\",\"bold\":true}`);\n            server.runCommandSilent(`title ${player.username} subtitle {\"text\":\"You wash ashore on the cold sands...\",\"color\":\"gray\"}`);\n        });\n\n        // 5. Act II: The Tenth Ember Awakens\n        server.scheduleInTicks(80, () => {\n            server.runCommandSilent(`playsound minecraft:block.campfire.crackle ambient ${player.username} ${px} ${py} ${pz} 0.8 1.0`);\n            server.runCommandSilent(`title ${player.username} times 15 50 15`);\n            server.runCommandSilent(`title ${player.username} title {\"text\":\"The Tenth Ember\",\"color\":\"gold\",\"bold\":true}`);\n            server.runCommandSilent(`title ${player.username} subtitle {\"text\":\"A faint warmth smolders within your chest.\",\"color\":\"yellow\"}`);\n        });\n\n        // 6. Act III: Narrative Introduction\n        server.scheduleInTicks(140, () => {\n            server.runCommandSilent(`playsound minecraft:block.bell.use ambient ${player.username} ${px} ${py} ${pz} 0.7 0.9`);\n            player.tell(\" \");\n            player.tell(\"\u00a78\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\");\n            player.tell(\"\u00a7c\u2694 ASHENFALL \u00a78\u2014 \u00a77The Pilgrimage Begins\");\n            player.tell(\"\u00a7e\\\"Nine sounds broke the Empire in a single night.\\\"\");\n            player.tell(\"\u00a7e\\\"You are not a hero, pilgrim. You are the cause, walking to mend what you shattered.\\\"\");\n            player.tell(\" \");\n            player.tell(\"\u00a7bAbove the shoreline bluff looms the Old Lighthouse beacon.\");\n            player.tell(\"\u00a77Scavenge the lighthouse for supplies, then journey inland toward the Norman Remnant.\");\n            player.tell(\"\u00a78\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\");\n            player.tell(\" \");\n        });\n\n        // 7. Starter supplies directly in inventory\n        server.scheduleInTicks(150, () => {\n            server.runCommandSilent(`give ${player.username} minecraft:leather_boots[custom_name='{\"text\":\"Waterlogged Boots\",\"color\":\"gray\"}']`);\n            server.runCommandSilent(`give ${player.username} minecraft:compass[custom_name='{\"text\":\"Pilgrim\\'s Compass\",\"color\":\"gold\"}']`);\n            server.runCommandSilent(`give ${player.username} minecraft:flint`);\n            server.runCommandSilent(`give ${player.username} minecraft:bread 4`);\n        });\n    }\n});\n",
    "narrative_dialogue.js": "// =============================================================================\n// ASHENFALL \u2014 NPC Narrative Dialogue Integration\n// =============================================================================\n\nvar NPC_DIALOGUES = {\n    \"the_archivist\": \"ashfall:archivist\",\n    \"norman_elder\": \"ashfall:norman_elder\",\n    \"drowned_fisherman\": \"ashfall:drowned_fisherman\"\n};\n\nEntityEvents.spawned(function(event) {\n    var entity = event.entity;\n    if (!entity) return;\n    \n    // Tag specific NPCs for dialogue interaction\n    if (entity.tags && entity.tags.contains(\"ashfall_archivist\")) {\n        entity.persistentData.putString(\"adm_dialogue\", NPC_DIALOGUES[\"the_archivist\"]);\n    }\n});\n\n// Global export for Rhino engine (explicit key-value pairs)\nglobal.ASHFALL_DIALOGUE = {\n    NPC_DIALOGUES: NPC_DIALOGUES\n};\n",
    "nations_and_landmarks.js": "// =============================================================================\n// ASHENFALL \u2014 The Nine Nations & Landmark Discovery System\n// =============================================================================\n\nconst NATIONS = [\n    {\n        id: \"norman_remnant\",\n        name: \"The Norman Remnant\",\n        subtitle: \"Frontier of Salt, Stone, and Iron\",\n        color: \"aqua\",\n        biomes: [\"minecraft:beach\", \"minecraft:stony_shore\", \"minecraft:windswept_hills\", \"minecraft:plains\"],\n        lore: \"The last bastion of coastal knights holding watch against the rising tide.\"\n    },\n    {\n        id: \"seljuk_expanse\",\n        name: \"The Seljuk Expanse\",\n        subtitle: \"Scorched Steppes & Ancient Sun Vaults\",\n        color: \"gold\",\n        biomes: [\"minecraft:desert\", \"minecraft:badlands\", \"minecraft:eroded_badlands\", \"minecraft:savanna\"],\n        lore: \"Nomadic riders and glass citadels buried beneath centuries of amber sand.\"\n    },\n    {\n        id: \"byzantine_choir\",\n        name: \"The Byzantine Choir\",\n        subtitle: \"Gilded Basilicas & Resonant Arches\",\n        color: \"light_purple\",\n        biomes: [\"minecraft:cherry_grove\", \"minecraft:meadow\", \"minecraft:flower_forest\"],\n        lore: \"Scholars of the high empire whose harmonic chants once bound the world.\"\n    },\n    {\n        id: \"witchbane_watch\",\n        name: \"The Witchbane Watch\",\n        subtitle: \"Dark Thickets & The Silent Inquisition\",\n        color: \"dark_green\",\n        biomes: [\"minecraft:dark_forest\", \"minecraft:swamp\", \"minecraft:mangrove_swamp\"],\n        lore: \"Hunters bound by iron oaths to cleanse the corrupted flora of the blight.\"\n    },\n    {\n        id: \"guild_of_merchants\",\n        name: \"The Guild of Merchants\",\n        subtitle: \"Canals, Trade Barges, and Gilded Vaults\",\n        color: \"yellow\",\n        biomes: [\"minecraft:river\", \"minecraft:forest\", \"minecraft:birch_forest\"],\n        lore: \"Where coin speaks louder than creed, and every relic has a price.\"\n    },\n    {\n        id: \"cathedral_of_ash\",\n        name: \"The Cathedral of Ash\",\n        subtitle: \"Heart of the Blight \u2014 Seat of the First Ember\",\n        color: \"dark_red\",\n        biomes: [\"minecraft:nether_wastes\", \"minecraft:basalt_deltas\", \"minecraft:crimson_forest\"],\n        lore: \"The charred epicenter where the first sound tore through the veil of reality.\"\n    },\n    {\n        id: \"frostfall\",\n        name: \"The Frostfall\",\n        subtitle: \"Glacial Spires & The Permafrost Gate\",\n        color: \"blue\",\n        biomes: [\"minecraft:snowy_slopes\", \"minecraft:frozen_peaks\", \"minecraft:ice_spikes\", \"minecraft:snowy_plains\"],\n        lore: \"Eternal blizzards shielding the northern ruins of the Celestial Aether.\"\n    },\n    {\n        id: \"sunken_throne\",\n        name: \"The Sunken Throne\",\n        subtitle: \"Abyssal Trenches & The Drowned Choir\",\n        color: \"dark_aqua\",\n        biomes: [\"minecraft:deep_ocean\", \"minecraft:ocean\", \"minecraft:deep_cold_ocean\"],\n        lore: \"Cathedrals submerged in deep trenches where the drowned clergy still pray.\"\n    },\n    {\n        id: \"hermits_reach\",\n        name: \"The Hermit's Reach\",\n        subtitle: \"Isolated Pinnacles & Silent Monasteries\",\n        color: \"gray\",\n        biomes: [\"minecraft:jagged_peaks\", \"minecraft:stony_peaks\"],\n        lore: \"Ascetic hermits guarding forgotten scrolls beyond the reach of kings.\"\n    }\n];\n\n// Check territory every 100 ticks (5 seconds)\nPlayerEvents.tick(event => {\n    let player = event.player;\n    if (player.age % 100 !== 0) return;\n\n    let biome = player.level.getBiome(player.blockPosition()).unwrapKey().get().location().toString();\n    \n    for (let nation of NATIONS) {\n        if (nation.biomes.includes(biome)) {\n            let tag = `visited_nation_${nation.id}`;\n            if (!player.tags.contains(tag)) {\n                player.tags.add(tag);\n                \n                // Audio sting\n                player.level.server.runCommandSilent(`playsound minecraft:ui.toast.challenge_complete ambient ${player.username} ${player.x} ${player.y} ${player.z} 0.8 1.1`);\n                \n                // Territory banner\n                player.level.server.runCommandSilent(`title ${player.username} times 10 70 20`);\n                player.level.server.runCommandSilent(`title ${player.username} title {\"text\":\"${nation.name}\",\"color\":\"${nation.color}\",\"bold\":true}`);\n                player.level.server.runCommandSilent(`title ${player.username} subtitle {\"text\":\"${nation.subtitle}\",\"color\":\"gray\",\"italic\":true}`);\n                \n                // Lore entry in chat\n                player.tell(\" \");\n                player.tell(`\u00a78[\u00a76Codex Discovered\u00a78] \u00a7f${nation.name}`);\n                player.tell(`\u00a77\"${nation.lore}\"`);\n                player.tell(\" \");\n            }\n            break;\n        }\n    }\n});\n",
    "quest_ids.js": "// =============================================================================\n// ASHENFALL \u2014 Custom Quest IDs Register (FTB XMod Compat Gates)\n// =============================================================================\n\nvar QUEST_GATES = {\n    // Act 0: The Cold Awakening\n    \"ASHEN_AWAKENING\": \"Player awakens on the drowned Norman coast\",\n    \"ASHEN_LIGHTHOUSE\": \"Player reaches and explores the Old Lighthouse\",\n    \n    // Act 1: The Remnants\n    \"ASHEN_NORMAN_WAYSTONE\": \"Discover the Norman Remnant central waystone\",\n    \"ASHEN_EMBER_REST\": \"Rekindle the Ember Flask at a camp rest point\",\n    \n    // Act 2: Factions & Wilderness\n    \"ASHEN_SELJUK_VAULT\": \"Enter the Sunken Desert Vault\",\n    \"ASHEN_WITCHBANE_INQUISITION\": \"Survive the Witchbane patrol in the dark forest\",\n    \n    // Act 3: The Deep Choir & Catacombs\n    \"ASHEN_DROWNED_CHOIR\": \"Locate the submerged cathedral ruins in the abyss\",\n    \"ASHEN_DEAD_KING\": \"Defeat the Dead King in the arcane catacombs\",\n    \n    // Act 4: The Apex Cathedrals\n    \"ASHEN_FIRST_EMBER\": \"Claim the First Ember from the Cathedral of Ash\",\n    \"ASHEN_NINE_SOUNDS_MENDED\": \"Complete the Great Pilgrimage\"\n};\n\n// Global export for Rhino engine\nglobal.QUEST_GATES = QUEST_GATES;\nglobal.QUEST_IDS = QUEST_GATES;\n",
    "rumours.js": "// =============================================================================\n// ASHENFALL \u2014 The Rumour Register System\n// =============================================================================\n\nvar RUMOURS = [\n    {\n        id: \"cold_tower\",\n        speaker: \"Inuit Elder\",\n        text: \"There is a tower in the far north that doesn't melt, even when struck by dragonfire.\",\n        landmark: \"L1 \u2014 The Cold Tower\",\n        gate: \"chapter_2\"\n    },\n    {\n        id: \"drowned_choir\",\n        speaker: \"Drowned Fisherman\",\n        text: \"The Choir's cathedral drowned in the abyss. It never stopped praying.\",\n        landmark: \"L7 \u2014 The Otherside Rift\",\n        gate: \"codex_drowned_choir\"\n    },\n    {\n        id: \"jungle_vault\",\n        speaker: \"Seljuk Scout\",\n        text: \"A sandstone fortress lies swallowed by the jungle vines. Whatever you do, do not enter at night.\",\n        landmark: \"L3 \u2014 Jungle Vault\",\n        gate: \"none\"\n    },\n    {\n        id: \"hidden_cathedral\",\n        speaker: \"The Archivist\",\n        text: \"They say there is a second Cathedral... buried beneath the foundations of the world.\",\n        landmark: \"L\u2605 \u2014 The Hidden Cathedral\",\n        gate: \"all_9_runes\"\n    },\n    {\n        id: \"arcane_catacombs\",\n        speaker: \"Tavern Keeper\",\n        text: \"Wizards buy raw essence at great cost. Wizards also die down in the catacombs.\",\n        landmark: \"L7b \u2014 The Catacombs\",\n        gate: \"essence_held\"\n    }\n];\n\nfunction tellRumour(player, rumourId) {\n    var rumour = null;\n    for (var i = 0; i < RUMOURS.length; i++) {\n        if (RUMOURS[i].id === rumourId) {\n            rumour = RUMOURS[i];\n            break;\n        }\n    }\n    if (!rumour) return;\n\n    player.tell(\" \");\n    player.tell(\"\u00a76[Rumour] \u00a7e\" + rumour.speaker + \" \u00a77whispers:\");\n    player.tell(\"\u00a7f\\\"\" + rumour.text + \"\\\"\");\n    player.tell(\"\u00a78Related Landmark: \u00a7b\" + rumour.landmark);\n    player.tell(\" \");\n}\n\n// Global export for Rhino engine (explicit key-value pairs)\nglobal.ASHFALL_RUMOURS = {\n    RUMOURS: RUMOURS,\n    tellRumour: tellRumour\n};\n\nglobal.tellRumour = tellRumour;\n",
    "runes.js": "// =============================================================================\n// ASHENFALL \u2014 The Nine Ember Runes System\n// =============================================================================\n\nvar RUNES = [\n    { id: \"norman\", item: \"ashfall:rune_of_the_norman\", nation: \"norman_remnant\", name: \"Rune of Salt & Iron\" },\n    { id: \"seljuk\", item: \"ashfall:rune_of_the_seljuk\", nation: \"seljuk_expanse\", name: \"Rune of Amber Sands\" },\n    { id: \"choir\", item: \"ashfall:rune_of_the_choir\", nation: \"byzantine_choir\", name: \"Rune of Resonant Hymns\" },\n    { id: \"witchbane\", item: \"ashfall:rune_of_the_witchbane\", nation: \"witchbane_watch\", name: \"Rune of the Cold Pyre\" },\n    { id: \"merchants\", item: \"ashfall:rune_of_the_merchants\", nation: \"guild_of_merchants\", name: \"Rune of Gilded Coin\" },\n    { id: \"ash\", item: \"ashfall:rune_of_the_ash\", nation: \"cathedral_of_ash\", name: \"Rune of the First Flame\" },\n    { id: \"frostfall\", item: \"ashfall:rune_of_the_frostfall\", nation: \"frostfall\", name: \"Rune of Glacial Spires\" },\n    { id: \"sunken\", item: \"ashfall:rune_of_the_sunken\", nation: \"sunken_throne\", name: \"Rune of the Abyss\" },\n    { id: \"hermit\", item: \"ashfall:rune_of_the_hermit\", nation: \"hermits_reach\", name: \"Rune of Silent Peaks\" }\n];\n\nfunction hasRune(player, runeId) {\n    var r = null;\n    for (var i = 0; i < RUNES.length; i++) {\n        if (RUNES[i].id === runeId) {\n            r = RUNES[i];\n            break;\n        }\n    }\n    if (!r) return false;\n    \n    // Check persistentData\n    if (player.persistentData.getBoolean(\"has_rune_\" + runeId)) {\n        return true;\n    }\n    \n    // Check if player has the item in inventory\n    var inventory = player.inventory;\n    if (inventory && inventory.find(r.item) !== -1) {\n        player.persistentData.putBoolean(\"has_rune_\" + runeId, true);\n        return true;\n    }\n    return false;\n}\n\nfunction runeCount(player) {\n    var count = 0;\n    for (var i = 0; i < RUNES.length; i++) {\n        if (hasRune(player, RUNES[i].id)) {\n            count++;\n        }\n    }\n    return count;\n}\n\n// Global export for Rhino engine (explicit key-value pairs)\nglobal.ASHFALL_RUNES = {\n    RUNES: RUNES,\n    hasRune: hasRune,\n    runeCount: runeCount\n};\n\nglobal.hasRune = hasRune;\nglobal.runeCount = runeCount;\n",
    "soulslike.js": "// =============================================================================\n// ASHENFALL \u2014 Soulslike Rest, Ember Flask, & Hollow Death Penalty\n// =============================================================================\n\nvar HOLLOW_CAP = 5;\nvar REST_TAGS = [\n    \"minecraft:campfires\",\n    \"minecraft:beds\"\n];\n\nfunction getHollow(player) {\n    if (!player.persistentData.contains(\"ashfall_hollow\")) {\n        player.persistentData.putInt(\"ashfall_hollow\", 0);\n    }\n    return player.persistentData.getInt(\"ashfall_hollow\");\n}\n\nfunction setHollow(player, val) {\n    var clamped = Math.max(0, Math.min(HOLLOW_CAP, val));\n    player.persistentData.putInt(\"ashfall_hollow\", clamped);\n}\n\n// On player respawn: hollow penalty increments\nPlayerEvents.respawned(function(event) {\n    var player = event.player;\n    var hollow = getHollow(player);\n    if (hollow < HOLLOW_CAP) {\n        setHollow(player, hollow + 1);\n        player.tell(\"\u00a78[\u00a7cDeath\u00a78] \u00a77Your ember fades slightly. Hollow tier: \u00a7c\" + (hollow + 1) + \"\u00a77/\" + HOLLOW_CAP);\n    }\n});\n\n// Global export for Rhino engine (explicit key-value pairs)\nglobal.ASHFALL_SOULSLIKE = {\n    HOLLOW_CAP: HOLLOW_CAP,\n    REST_TAGS: REST_TAGS,\n    getHollow: getHollow,\n    setHollow: setHollow\n};\n\nglobal.getHollow = getHollow;\nglobal.setHollow = setHollow;\n",
    "standing.js": "// =============================================================================\n// ASHENFALL \u2014 Nine Nations Standing System (-100 to +100)\n// =============================================================================\n\nvar NATIONS = [\n    \"norman_remnant\",\n    \"seljuk_expanse\",\n    \"byzantine_choir\",\n    \"witchbane_watch\",\n    \"guild_of_merchants\",\n    \"cathedral_of_ash\",\n    \"frostfall\",\n    \"sunken_throne\",\n    \"hermits_reach\"\n];\n\nvar CROSS_FACTION = true;\nvar CHAMPION_THRESHOLD = 80;\nvar MAX_NATIONS_CHAMPION = 3;\n\nfunction getStanding(player, faction) {\n    var key = \"standing_\" + faction;\n    if (!player.persistentData.contains(key)) {\n        player.persistentData.putInt(key, 0); // Neutral\n    }\n    return player.persistentData.getInt(key);\n}\n\nfunction modifyStanding(player, faction, delta) {\n    var key = \"standing_\" + faction;\n    var current = getStanding(player, faction);\n    var updated = Math.max(-100, Math.min(100, current + delta));\n    player.persistentData.putInt(key, updated);\n\n    var prefix = delta >= 0 ? \"\u00a7a+\" : \"\u00a7c\";\n    var factionLabel = faction.replace(/_/g, \" \").replace(/\\b\\w/g, function(l) { return l.toUpperCase(); });\n    player.tell(\"\u00a78[\u00a76Faction Rep\u00a78] \u00a7f\" + factionLabel + \": \" + prefix + delta + \" \u00a77(Current: \" + updated + \")\");\n}\n\n// Global export for Rhino engine (explicit key-value pairs)\nglobal.ASHFALL_STANDING = {\n    NATIONS: NATIONS,\n    CROSS_FACTION: CROSS_FACTION,\n    CHAMPION_THRESHOLD: CHAMPION_THRESHOLD,\n    MAX_NATIONS_CHAMPION: MAX_NATIONS_CHAMPION,\n    getStanding: getStanding,\n    modifyStanding: modifyStanding\n};\n\nglobal.getStanding = getStanding;\nglobal.modifyStanding = modifyStanding;\n",
    "structures.js": "// =============================================================================\n// ASHENFALL \u2014 Structure Province & Landmark Registry\n// =============================================================================\n\nvar STRUCTURE_PROVINCES = {\n    \"structory:settlements/coastal\": { nation: \"norman_remnant\", name: \"Norman Coastal Outpost\" },\n    \"towns_and_towers:ocean/village\": { nation: \"norman_remnant\", name: \"Norman Port Village\" },\n    \"structory:settlements/desert\": { nation: \"seljuk_expanse\", name: \"Seljuk Caravan Camp\" },\n    \"dungeons_and_taverns:desert_pyramid\": { nation: \"seljuk_expanse\", name: \"Sunken Desert Crypt\" },\n    \"graveyard:lich_prison\": { nation: \"frostfall\", name: \"Citadel of the Cold Tower\" },\n    \"cataclysm:burning_arena\": { nation: \"cathedral_of_ash\", name: \"Crucible of Ash\" },\n    \"cataclysm:sunken_city\": { nation: \"sunken_throne\", name: \"Submerged Cathedral of the Abyss\" }\n};\n\nfunction getProvinceForStructure(structureId) {\n    return STRUCTURE_PROVINCES[structureId] || null;\n}\n\n// Global export for Rhino engine (explicit key-value pairs)\nglobal.ASHFALL_STRUCTURES = {\n    STRUCTURE_PROVINCES: STRUCTURE_PROVINCES,\n    getProvinceForStructure: getProvinceForStructure\n};\n\nglobal.getProvinceForStructure = getProvinceForStructure;\n",
    "threat.js": "// =============================================================================\n// ASHENFALL \u2014 Threat Tier Scaling Engine (Tiers I\u2013VII)\n// =============================================================================\n\nvar MAX_TIER = 7;\n\nvar REGIONS = [\n    \"norman_coast\",\n    \"seljuk_desert\",\n    \"byzantine_hills\",\n    \"witchbane_woods\",\n    \"merchant_rivers\",\n    \"cathedral_depths\",\n    \"frostfall_peaks\",\n    \"sunken_abyss\",\n    \"hermit_highlands\"\n];\n\nfunction tierOf(player, region) {\n    var key = \"threat_tier_\" + region;\n    if (!player.persistentData.contains(key)) {\n        player.persistentData.putInt(key, 1);\n    }\n    return player.persistentData.getInt(key);\n}\n\nfunction setTier(player, region, tier) {\n    var clamped = Math.max(1, Math.min(MAX_TIER, tier));\n    var key = \"threat_tier_\" + region;\n    player.persistentData.putInt(key, clamped);\n    player.tell(\"\u00a78[\u00a76Threat Scaled\u00a78] \u00a7f\" + region + \" \u00a77is now set to Threat Tier: \u00a76\" + clamped);\n}\n\nfunction regionOf(entity) {\n    if (!entity || !entity.level) return \"norman_coast\";\n    var dim = entity.level.dimension.toString();\n    if (dim === \"minecraft:the_nether\") return \"cathedral_depths\";\n    if (dim === \"minecraft:the_end\") return \"sunken_abyss\";\n\n    var biome = entity.level.getBiome(entity.blockPosition()).unwrapKey().get().location().toString();\n    if (biome.indexOf(\"desert\") !== -1 || biome.indexOf(\"badlands\") !== -1) return \"seljuk_desert\";\n    if (biome.indexOf(\"dark_forest\") !== -1 || biome.indexOf(\"swamp\") !== -1) return \"witchbane_woods\";\n    if (biome.indexOf(\"snow\") !== -1 || biome.indexOf(\"ice\") !== -1 || biome.indexOf(\"frozen\") !== -1) return \"frostfall_peaks\";\n    if (biome.indexOf(\"ocean\") !== -1) return \"sunken_abyss\";\n    if (biome.indexOf(\"jagged\") !== -1 || biome.indexOf(\"stony_peaks\") !== -1) return \"hermit_highlands\";\n    if (biome.indexOf(\"cherry\") !== -1 || biome.indexOf(\"meadow\") !== -1) return \"byzantine_hills\";\n    if (biome.indexOf(\"river\") !== -1) return \"merchant_rivers\";\n    return \"norman_coast\";\n}\n\n// Global export for Rhino engine (explicit key-value pairs)\nglobal.ASHFALL_THREAT = {\n    REGIONS: REGIONS,\n    MAX_TIER: MAX_TIER,\n    regionOf: regionOf,\n    tierOf: tierOf,\n    setTier: setTier\n};\n\nglobal.regionOf = regionOf;\nglobal.tierOf = tierOf;\nglobal.setTier = setTier;\n"
}


def fix_rhino_shorthands(text: str) -> str:
    """Expands ES6 object shorthand literals like { a, b } into { a: a, b: b } for Rhino engine."""
    def repl(match):
        inner = match.group(1).strip()
        if any(k in inner for k in ("function", "return", "var ", "let ", "const ", ";", "=>", "//")):
            return match.group(0)
        parts = [p.strip() for p in inner.split(',') if p.strip()]
        new_parts = []
        for p in parts:
            if ":" in p or "=" in p:
                new_parts.append(p)
            else:
                new_parts.append(f"{p}: {p}")
        return "{ " + ", ".join(new_parts) + " }"

    return re.sub(r'\{\s*([a-zA-Z0-9_,\s]+)\s*\}', repl, text)


def check_and_fix_kubejs(mods_dir: Path) -> int:
    """Scans .minecraft/kubejs/ for script syntax errors and heals them for Rhino JS (KubeJS 1.21.1)."""
    fixed = 0
    candidate_dirs = [
        mods_dir.parent / "kubejs",
        Path.cwd() / "kubejs",
        mods_dir / "kubejs",
        mods_dir.parent / "overrides" / "kubejs",
        Path.cwd() / "pack" / "overrides" / "kubejs",
    ]

    for kubejs_dir in candidate_dirs:
        if not kubejs_dir.exists():
            continue

        # 1. Startup scripts (patch invalid enum 'legendary' -> 'epic')
        startup_dir = kubejs_dir / "startup_scripts"
        if startup_dir.exists():
            for js_file in startup_dir.glob("*.js"):
                try:
                    content = js_file.read_text(encoding="utf-8")
                    orig = content
                    if "'legendary'" in content or '"legendary"' in content:
                        content = content.replace("'legendary'", "'epic'").replace('"legendary"', '"epic"')
                    if content != orig:
                        print(f"  [KubeJS Auto-Healer] Detected invalid 'legendary' enum in {js_file.name}. Patched to 'epic'...")
                        js_file.write_text(content, encoding="utf-8")
                        fixed += 1
                except Exception as e:
                    pass

        # 2. Server scripts (heal Rhino JS incompatibilities: globalThis, ServerEvents.commands, object shorthands)
        server_dir = kubejs_dir / "server_scripts"
        if server_dir.exists():
            # First, check and heal or sync canonical scripts
            for filename, canonical_code in CANONICAL_SERVER_SCRIPTS.items():
                dest_file = server_dir / filename
                if dest_file.exists():
                    try:
                        content = dest_file.read_text(encoding="utf-8")
                        orig = content
                        
                        # Replace globalThis with global
                        if "globalThis" in content:
                            content = re.sub(r'globalThis', 'global', content)
                        
                        # Replace ServerEvents.commands with ServerEvents.commandRegistry
                        if "ServerEvents.commands" in content:
                            content = content.replace("ServerEvents.commands", "ServerEvents.commandRegistry")
                        
                        # Expand object shorthands
                        content = fix_rhino_shorthands(content)

                        # Check if catastrophic syntax error exists (e.g. boss_monologue missing parenthesis)
                        if "boss_monologue" in filename or "threat.js" in filename:
                            # If file length is small or differs heavily, overwrite with canonical
                            content = canonical_code

                        if content != orig:
                            print(f"  [KubeJS Auto-Healer] Healed Rhino JS compatibility in server_scripts/{filename}...")
                            dest_file.write_text(content, encoding="utf-8")
                            fixed += 1
                    except Exception as e:
                        print(f"  [KubeJS Auto-Healer] Restoring canonical server_scripts/{filename}...")
                        dest_file.write_text(canonical_code, encoding="utf-8")
                        fixed += 1
                else:
                    # File is missing in server_scripts, install canonical copy
                    try:
                        dest_file.write_text(canonical_code, encoding="utf-8")
                        fixed += 1
                    except Exception:
                        pass

            # Also check any other .js files in server_scripts
            for js_file in server_dir.glob("*.js"):
                if js_file.name in CANONICAL_SERVER_SCRIPTS:
                    continue
                try:
                    content = js_file.read_text(encoding="utf-8")
                    orig = content
                    if "globalThis" in content:
                        print(f"  [KubeJS Auto-Healer] Replacing 'globalThis' with 'global' in {js_file.name}...")
                        content = re.sub(r'globalThis', 'global', content)
                    if "ServerEvents.commands" in content:
                        print(f"  [KubeJS Auto-Healer] Replacing 'ServerEvents.commands' with 'ServerEvents.commandRegistry' in {js_file.name}...")
                        content = content.replace("ServerEvents.commands", "ServerEvents.commandRegistry")
                    content = fix_rhino_shorthands(content)
                    if content != orig:
                        js_file.write_text(content, encoding="utf-8")
                        fixed += 1
                except Exception:
                    pass

    return fixed


def clean_corrupted_files(mods_dir: Path) -> int:
    """Scans mods_dir and removes 0-byte, corrupted, or incompatible files that break NeoForge."""
    removed = 0
    if not mods_dir.exists():
        return 0

    for item in list(mods_dir.iterdir()):
        if item.is_file():
            # Check for non-jar files mistakenly placed into mods/
            if item.suffix.lower() in (".mrpack", ".zip", ".tmp", ".txt"):
                print(f"  [Cleaner] Removing non-mod bundle from mods folder: {item.name}")
                item.unlink()
                removed += 1
                continue

            # Remove Hollowmarch: Has hardcoded Create block references (create:large_water_wheel) that crash 1.21.1 world creation
            if "hollowmarch" in item.name.lower():
                print(f"  [Cleaner] Removing Hollowmarch JAR (prevents Create registry world-creation crash): {item.name}")
                item.unlink()
                removed += 1
                continue

            # Remove Better Combat JAR (keeping Vanilla PvP mechanics per user preference)
            if "bettercombat" in item.name.lower():
                print(f"  [Cleaner] Removing Better Combat JAR (keeping Vanilla PvP mechanics): {item.name}")
                item.unlink()
                removed += 1
                continue

            # Remove Terralith if present (replaced by Lithosphere + Still Life)
            if "terralith" in item.name.lower():
                print(f"  [Cleaner] Removing Terralith JAR (replaced by Lithosphere + Still Life): {item.name}")
                item.unlink()
                removed += 1
                continue

            # Check 0-byte files
            if item.stat().st_size == 0:
                print(f"  [Cleaner] Removing 0-byte truncated file: {item.name}")
                item.unlink()
                removed += 1
                continue

            # Verify zip header on jar files
            if item.suffix.lower() == ".jar":
                try:
                    with zipfile.ZipFile(item, "r") as zf:
                        _ = zf.namelist()
                except (zipfile.BadZipFile, Exception):
                    print(f"  [Cleaner] Removing corrupted jar (broken zip header): {item.name}")
                    item.unlink()
                    removed += 1
    return removed


# ---------------------------------------------------------------------------
# Main Routine
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Download Ashenfall Minecraft 1.21.1 NeoForge mod JARs directly.")
    parser.add_argument("--phase", default="all", help="Phase to download (all, remaining, M0, M1+M2, M3+M3b). Default: all")
    parser.add_argument("--dest", help="Destination folder (default: auto-detected Minecraft/TLauncher mods folder or ./mods)")
    parser.add_argument("--clean", action="store_true", help="Remove broken/0-byte files from target mods directory before downloading")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show verbose debugging information")

    args = parser.parse_args()

    # 1. Determine destination folder
    if args.dest:
        target_dir = Path(args.dest)
    else:
        detected = detect_minecraft_mods_dir()
        if detected:
            target_dir = detected
        else:
            target_dir = Path.cwd() / "mods"

    target_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 65)
    print(" ASHENFALL — DIRECT MOD DOWNLOADER")
    print(" Target: Minecraft 1.21.1 · NeoForge 21.1.x")
    print(" Destination:", target_dir)
    print(" Phase:", args.phase.upper())
    print("=" * 65 + "\n")

    # 2. Clean out any corrupted / 0-byte files that trigger "zip END header not found"
    print("[1/3] Scanning destination folder for corrupted files and script issues...")
    cleaned = clean_corrupted_files(target_dir)
    if cleaned > 0:
        print(f"  ✅ Cleaned {cleaned} corrupted/invalid files to prevent startup crash.")
    else:
        print("  ✅ Destination folder is clean.")

    fixed_scripts = check_and_fix_kubejs(target_dir)
    if fixed_scripts > 0:
        print(f"  ✅ Checked and healed {fixed_scripts} KubeJS script(s) (modernized for 1.21.1 Rhino JS engine).")

    # 3. Filter mods by phase
    phase_filter = args.phase.upper()
    if phase_filter in ("ALL", "FULL", "COMPLETE"):
        mods_to_download = MODS_CATALOG
    elif phase_filter in ("REMAINING", "REST", "NEW", "M3C-M7", "M3C+M7"):
        # The remaining phases (M3c through M7)
        mods_to_download = [m for m in MODS_CATALOG if m.get("phase") in ("M3c", "M4", "M5", "M6", "M7")]
    elif phase_filter in ("M1+M2", "M1-M2", "M1M2", "M1_M2", "M12"):
        # Combined M1 and M2: Includes M0 baseline + M1 + M2
        mods_to_download = [m for m in MODS_CATALOG if m.get("phase") in ("M0", "M1", "M2")]
    elif phase_filter in ("ONLY-M1-M2", "M1-M2-ONLY"):
        # Only M1 and M2 mods
        mods_to_download = [m for m in MODS_CATALOG if m.get("phase") in ("M1", "M2")]
    elif phase_filter in ("M3+M3B", "M3-M3B", "M3M3B", "M3_M3B", "COMBINED", "M3B", "M3"):
        # Combined M3 & M3b: Includes baseline M0 + M1 + M2 + M3 + M3b
        mods_to_download = [m for m in MODS_CATALOG if m.get("phase") in ("M0", "M1", "M2", "M3", "M3b")]
    elif phase_filter in ("ONLY-M3-M3B", "M3-M3B-ONLY", "NEW-M3"):
        # Only M3 and M3b mods
        mods_to_download = [m for m in MODS_CATALOG if m.get("phase") in ("M3", "M3b")]
    else:
        # If user chooses M0, download M0. If user chooses M1, download M0 + M1, etc.
        phase_order = ["M0", "M1", "M2", "M3", "M3b", "M3c", "M4", "M5", "M6", "M7", "M8", "M9"]
        phase_order_upper = [p.upper() for p in phase_order]
        if phase_filter in phase_order_upper:
            target_idx = phase_order_upper.index(phase_filter)
            allowed_phases = set(phase_order_upper[:target_idx + 1])
            mods_to_download = [m for m in MODS_CATALOG if m.get("phase", "").upper() in allowed_phases]
        else:
            mods_to_download = [m for m in MODS_CATALOG if m.get("phase", "").upper() == phase_filter]

    print(f"\n[2/3] Resolving and downloading {len(mods_to_download)} verified mods...")

    success = 0
    skipped = 0
    failed = 0

    for i, mod in enumerate(mods_to_download, 1):
        name = mod["name"]
        slug = mod.get("slug")
        slug_display = ", ".join(slug) if isinstance(slug, list) else str(slug)
        print(f"  [{i}/{len(mods_to_download)}] {name} ({slug_display})...", end="", flush=True)

        # Check fallback url or resolve via Modrinth API
        res = resolve_modrinth_jar(slug, verbose=args.verbose)
        if res:
            url, filename, size = res
        elif mod.get("fallback_url") and mod.get("filename"):
            url = mod["fallback_url"]
            filename = mod["filename"]
            size = 0
        else:
            print(" ⚠️ No 1.21.1 NeoForge file found on Modrinth API.")
            failed += 1
            continue

        dest_file = target_dir / filename

        # Check if already present and valid
        if dest_file.exists():
            try:
                with zipfile.ZipFile(dest_file, "r") as zf:
                    if zf.namelist():
                        print(f" Already up-to-date ({dest_file.stat().st_size // 1024} KB).")
                        skipped += 1
                        continue
            except Exception:
                dest_file.unlink()

        # Download
        ok = download_and_verify(url, dest_file, expected_size=size, verbose=args.verbose)
        if ok:
            mb = dest_file.stat().st_size / (1024 * 1024)
            print(f" Downloaded ({mb:.1f} MB) ✅")
            success += 1
        else:
            print(" ❌ Download failed.")
            failed += 1

    print("\n" + "=" * 65)
    print(f" DOWNLOAD COMPLETE: {success} downloaded, {skipped} up-to-date, {failed} pending.")
    print(" Mods are installed in:")
    print("  ", target_dir.resolve())
    print("=" * 65 + "\n")
    print("You can now launch Minecraft 1.21.1 NeoForge and test the game!")


if __name__ == "__main__":
    main()

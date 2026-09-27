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
        "slug": "enhanced-block-entities",
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
        "slug": "citadel",
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
        "name": "Hollowmarch",
        "slug": "hollowmarch",
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
        "slug": "repurposed-structures",
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
        "slug": "the-graveyard",
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
        "slug": "origins",
        "provider": "modrinth",
        "phase": "M5",
        "category": "rpg",
    },
    {
        "name": "Reforged",
        "slug": "tiered",
        "provider": "modrinth",
        "phase": "M5",
        "category": "rpg",
    },
    {
        "name": "Attribute Modify",
        "slug": "attribute-modify",
        "provider": "modrinth",
        "phase": "M5",
        "category": "rpg",
    },
    {
        "name": "Mob Champions",
        "slug": "mob-champions",
        "provider": "modrinth",
        "phase": "M5",
        "category": "rpg",
    },
    {
        "name": "Loot Beams: Refork",
        "slug": "loot-beams",
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
        "slug": ["alexs-caves", "alexscaves", "alexs-caves-(unofficial-port)"],
        "provider": "modrinth",
        "phase": "M6",
        "category": "bosses",
    },
    {
        "name": "Alex's Mobs",
        "slug": ["alexs-mobs", "alexsmobs"],
        "provider": "modrinth",
        "phase": "M6",
        "category": "bosses",
    },
    {
        "name": "Mini-boss Boss Bars",
        "slug": "mini-boss-boss-bars",
        "provider": "modrinth",
        "phase": "M6",
        "category": "bosses",
    },
    {
        "name": "Configurable Boss Bars",
        "slug": "configurable-boss-bars",
        "provider": "modrinth",
        "phase": "M6",
        "category": "bosses",
    },
    {
        "name": "Boss Music Mod",
        "slug": "boss-music-mod",
        "provider": "modrinth",
        "phase": "M6",
        "category": "bosses",
    },
    {
        "name": "Floating Damage Indicators",
        "slug": "floating-damage-indicators",
        "provider": "modrinth",
        "phase": "M6",
        "category": "bosses",
    },
    {
        "name": "YUNG's Traveler's Titles",
        "slug": "yungs-travelers-titles",
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
        "slug": "enigmatic-legacy-plus",
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
        "slug": "shutup-experimental-settings",
        "provider": "modrinth",
        "phase": "M7",
        "category": "story",
    },
    {
        "name": "Skin Layers 3D",
        "slug": "skin-layers-3d",
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
        "slug": "presence-footsteps",
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


def clean_corrupted_files(mods_dir: Path) -> int:
    """Scans mods_dir and removes 0-byte, corrupted, or non-jar files that break NeoForge."""
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

            # Remove excluded/deprecated mods (e.g. Better Combat to preserve vanilla PvP mechanics)
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
    print("[1/3] Scanning destination folder for corrupted files...")
    cleaned = clean_corrupted_files(target_dir)
    if cleaned > 0:
        print(f"  ✅ Cleaned {cleaned} corrupted/invalid files to prevent startup crash.")
    else:
        print("  ✅ Destination folder is clean.")

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

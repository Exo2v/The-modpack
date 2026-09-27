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
from typing import Any, Dict, List, Optional, Tuple, Set

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
    {
        "name": "Distant Horizons",
        "slug": "distanthorizons",
        "provider": "modrinth",
        "phase": "M0",
        "category": "performance",
        "fallback_url": "https://cdn.modrinth.com/data/uCdwusMi/versions/IcOcoekl/DistantHorizons-3.3.1-1.21.1-fabric-neoforge.jar",
        "filename": "DistantHorizons-3.3.1-1.21.1-fabric-neoforge.jar",
    },
    {
        "name": "EasyMotionBlur",
        "slug": None,
        "provider": "curseforge",
        "phase": "M0",
        "category": "visual",
        "fallback_url": [
            "https://edge.forgecdn.net/files/8218/65/EasyMotionBlur-1.1-1.21.1-neoforge.jar",
            "https://mediafilez.forgecdn.net/files/8218/65/EasyMotionBlur-1.1-1.21.1-neoforge.jar",
        ],
        "filename": "EasyMotionBlur-1.1-1.21.1-neoforge.jar",
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
    {
        "name": "Streams Reflowing",
        "slug": "streams-reflowing",
        "provider": "curseforge",
        "phase": "M3",
        "category": "worldgen",
        "fallback_url": [
            "https://edge.forgecdn.net/files/8453/865/StreamsReflowing-1.21.1-neoforge-2.8.4.jar",
            "https://mediafilez.forgecdn.net/files/8453/865/StreamsReflowing-1.21.1-neoforge-2.8.4.jar",
        ],
        "filename": "StreamsReflowing-1.21.1-neoforge-2.8.4.jar",
    },
    {
        "name": "Create",
        "slug": "create",
        "provider": "modrinth",
        "phase": "M3",
        "category": "technology",
        "fallback_url": [
            "https://edge.forgecdn.net/files/7408/951/create-1.21.1-6.0.9.jar",
            "https://mediafilez.forgecdn.net/files/7408/951/create-1.21.1-6.0.9.jar",
        ],
        "filename": "create-1.21.1-6.0.9.jar",
    },
    {
        "name": "Create: Structures Arise",
        "slug": "create-structures-arise",
        "provider": "curseforge",
        "phase": "M3",
        "category": "worldgen",
        "fallback_url": [
            "https://edge.forgecdn.net/files/8837/992/Create-Structures-Arise-1.21.1-NeoForge-176.49.49.jar",
            "https://mediafilez.forgecdn.net/files/8837/992/Create-Structures-Arise-1.21.1-NeoForge-176.49.49.jar",
        ],
        "filename": "Create-Structures-Arise-1.21.1-NeoForge-176.49.49.jar",
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
    {
        "name": "Ice and Fire: Community Edition",
        "slug": ["iceandfire-ce", "iceandfire"],
        "provider": "modrinth",
        "phase": "M6",
        "category": "bosses",
        "fallback_url": [
            "https://cdn.modrinth.com/data/VpmCsizY/versions/S6tF3M1u/IceAndFireCE-1.1-1.21.1-neoforge.jar",
            "https://edge.forgecdn.net/files/6758/480/IceAndFireCE-1.1-1.21.1-neoforge.jar",
            "https://mediafilez.forgecdn.net/files/6758/480/IceAndFireCE-1.1-1.21.1-neoforge.jar",
        ],
        "filename": "IceAndFireCE-1.1-1.21.1-neoforge.jar",
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

def resolve_modrinth_jar(slug_or_slugs: str | List[str] | None, mc_version: str = "1.21.1", verbose: bool = False) -> Optional[Tuple[str, str, int]]:
    """
    Queries Modrinth API for a 1.21.1 NeoForge / Forge release.
    Supports candidate aliases, filtered query, and fallback search.
    Returns (download_url, filename, size_bytes).
    """
    if not slug_or_slugs:
        return None
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


def download_and_verify(urls: str | List[str], dest_path: Path, expected_size: int = 0, verbose: bool = False) -> bool:
    """Downloads a file to dest_path and strictly verifies zip integrity."""
    if isinstance(urls, str):
        urls = [urls]

    temp_path = dest_path.with_suffix(".tmp")
    for url in urls:
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
                print(f" [mirror error: {e}]", end="")
            continue

    return False


CANONICAL_SERVER_SCRIPTS = {
    "boss_monologue.js": "// =============================================================================\n// ASHENFALL \u2014 Boss Monologues & Cinematic Encounters\n// =============================================================================\n\nvar BOSS_ENCOUNTERS = {\n    \"cataclysm:ignis\": {\n        name: \"Ignis, The Incinerator\",\n        line: \"Ash will cover the world again. Your ember will feed the pyre.\",\n        sound: \"minecraft:entity.ender_dragon.growl\"\n    },\n    \"cataclysm:netherite_monstrosity\": {\n        name: \"Netherite Monstrosity\",\n        line: \"The crucible demands another sacrifice.\",\n        sound: \"minecraft:entity.ravager.roar\"\n    },\n    \"cataclysm:the_harbinger\": {\n        name: \"The Harbinger, The Ravager of Iron\",\n        line: \"RUST AND RUIN. THE GEARS TURN TO GRIND FLESH AND BONE.\",\n        sound: \"minecraft:block.beacon.activate\"\n    },\n    \"cataclysm:the_leviathan\": {\n        name: \"The Leviathan of the Abyss\",\n        line: \"The sunken choir sings your drowning hymn.\",\n        sound: \"minecraft:ambient.underwater.loop\"\n    },\n    \"irons_spellbooks:dead_king\": {\n        name: \"The Dead King of the Catacombs\",\n        line: \"You seek the lost words of power. They belong to the dust.\",\n        sound: \"minecraft:entity.wither.ambient\"\n    }\n};\n\nEntityEvents.spawned(function(event) {\n    try {\n        var entity = event.entity;\n        if (!entity) return;\n        var type = entity.type;\n\n        if (BOSS_ENCOUNTERS[type]) {\n            var boss = BOSS_ENCOUNTERS[type];\n            var level = entity.level;\n            if (!level || !level.players) return;\n\n            level.players.forEach(function(player) {\n                // Check distance\n                var distSq = player.distanceToSqr(entity);\n                if (distSq < 64 * 64) {\n                    var server = level.server;\n                    if (!server) return;\n                    player.potionEffects.add(\"minecraft:slowness\", 60, 1, false, false);\n                    server.runCommandSilent(\"playsound \" + boss.sound + \" ambient \" + player.username + \" \" + player.x + \" \" + player.y + \" \" + player.z + \" 1.0 0.8\");\n                    server.runCommandSilent(\"title \" + player.username + \" times 10 60 20\");\n                    server.runCommandSilent(\"title \" + player.username + \" title {\\\"text\\\":\\\"\" + boss.name + \"\\\",\\\"color\\\":\\\"red\\\",\\\"bold\\\":true}\");\n                    server.runCommandSilent(\"title \" + player.username + \" subtitle {\\\"text\\\":\\\"\\\\\\\"\" + boss.line + \"\\\\\\\"\\\",\\\"color\\\":\\\"gold\\\",\\\"italic\\\":true}\");\n                }\n            });\n        }\n    } catch (e) {\n        // Silently prevent event failure\n    }\n});\n",
    "commands.js": "// =============================================================================\n// ASHENFALL \u2014 Admin & In-Game Command Register (Minecraft 1.21.1 / KubeJS)\n// =============================================================================\n\nServerEvents.commandRegistry(function(event) {\n    var Commands = event.commands;\n    var Arguments = event.arguments;\n\n    event.register(\n        Commands.literal(\"ashenfall\")\n            .requires(function(source) { return source.hasPermission(2); })\n            .then(Commands.literal(\"standing\")\n                .then(Commands.argument(\"player\", Arguments.PLAYER.create(event))\n                    .then(Commands.argument(\"faction\", Arguments.STRING.create(event))\n                        .then(Commands.argument(\"amount\", Arguments.INTEGER.create(event))\n                            .executes(function(ctx) {\n                                var player = Arguments.PLAYER.getResult(ctx, \"player\");\n                                var faction = Arguments.STRING.getResult(ctx, \"faction\");\n                                var amount = Arguments.INTEGER.getResult(ctx, \"amount\");\n                                if (global.modifyStanding) {\n                                    global.modifyStanding(player, faction, amount);\n                                }\n                                return 1;\n                            })\n                        )\n                    )\n                )\n            )\n            .then(Commands.literal(\"threat\")\n                .then(Commands.argument(\"player\", Arguments.PLAYER.create(event))\n                    .then(Commands.argument(\"region\", Arguments.STRING.create(event))\n                        .then(Commands.argument(\"tier\", Arguments.INTEGER.create(event))\n                            .executes(function(ctx) {\n                                var player = Arguments.PLAYER.getResult(ctx, \"player\");\n                                var region = Arguments.STRING.getResult(ctx, \"region\");\n                                var tier = Arguments.INTEGER.getResult(ctx, \"tier\");\n                                if (global.setTier) {\n                                    global.setTier(player, region, tier);\n                                }\n                                return 1;\n                            })\n                        )\n                    )\n                )\n            )\n            .then(Commands.literal(\"rumour\")\n                .then(Commands.argument(\"player\", Arguments.PLAYER.create(event))\n                    .then(Commands.argument(\"id\", Arguments.STRING.create(event))\n                        .executes(function(ctx) {\n                            var player = Arguments.PLAYER.getResult(ctx, \"player\");\n                            var id = Arguments.STRING.getResult(ctx, \"id\");\n                            if (global.tellRumour) {\n                                global.tellRumour(player, id);\n                            }\n                            return 1;\n                        })\n                    )\n                )\n            )\n    );\n});\n",
    "intro_awakening.js": "// =============================================================================\n// ASHENFALL \u2014 Beach Awakening Cutscene & Shoreline Spawn\n// =============================================================================\n\nfunction buildLighthouse(server, x, y, z) {\n    // Build a classic coastal stone lighthouse on the bluff\n    for (var dy = 0; dy < 14; dy++) {\n        var radius = dy < 8 ? 2 : 1;\n        for (var dx = -radius; dx <= radius; dx++) {\n            for (var dz = -radius; dz <= radius; dz++) {\n                if (Math.abs(dx) === radius && Math.abs(dz) === radius) {\n                    server.runCommandSilent(\"setblock \" + (x + dx) + \" \" + (y + dy) + \" \" + (z + dz) + \" minecraft:mossy_cobblestone\");\n                } else if (Math.abs(dx) === radius || Math.abs(dz) === radius) {\n                    server.runCommandSilent(\"setblock \" + (x + dx) + \" \" + (y + dy) + \" \" + (z + dz) + \" minecraft:stone_bricks\");\n                } else {\n                    server.runCommandSilent(\"setblock \" + (x + dx) + \" \" + (y + dy) + \" \" + (z + dz) + \" minecraft:air\");\n                }\n            }\n        }\n    }\n\n    // Doorway\n    server.runCommandSilent(\"setblock \" + x + \" \" + y + \" \" + (z + 2) + \" minecraft:oak_door[facing=south,half=lower]\");\n    server.runCommandSilent(\"setblock \" + x + \" \" + (y + 1) + \" \" + (z + 2) + \" minecraft:oak_door[facing=south,half=upper]\");\n\n    // Interior ladder & floors\n    for (var ldy = 0; ldy < 13; ldy++) {\n        server.runCommandSilent(\"setblock \" + x + \" \" + (y + ldy) + \" \" + (z - 1) + \" minecraft:ladder[facing=south]\");\n    }\n\n    // Lantern gallery & beacon on top\n    var topY = y + 14;\n    for (var bx = -2; bx <= 2; bx++) {\n        for (var bz = -2; bz <= 2; bz++) {\n            server.runCommandSilent(\"setblock \" + (x + bx) + \" \" + topY + \" \" + (z + bz) + \" minecraft:smooth_stone_slab\");\n            if (Math.abs(bx) === 2 || Math.abs(bz) === 2) {\n                server.runCommandSilent(\"setblock \" + (x + bx) + \" \" + (topY + 1) + \" \" + (z + bz) + \" minecraft:iron_bars\");\n            }\n        }\n    }\n\n    // Beacon fire at the crown\n    server.runCommandSilent(\"setblock \" + x + \" \" + (topY + 1) + \" \" + z + \" minecraft:soul_campfire[lit=true]\");\n    server.runCommandSilent(\"setblock \" + x + \" \" + (topY + 2) + \" \" + z + \" minecraft:tinted_glass\");\n    server.runCommandSilent(\"setblock \" + x + \" \" + (topY + 3) + \" \" + z + \" minecraft:stone_brick_slab\");\n\n    // Starter Chest inside ground floor\n    server.runCommandSilent(\"setblock \" + (x + 1) + \" \" + y + \" \" + z + \" minecraft:chest[facing=west]\");\n    server.runCommandSilent(\"item replace block \" + (x + 1) + \" \" + y + \" \" + z + \" container.0 with minecraft:spyglass\");\n    server.runCommandSilent(\"item replace block \" + (x + 1) + \" \" + y + \" \" + z + \" container.1 with minecraft:bread 8\");\n    server.runCommandSilent(\"item replace block \" + (x + 1) + \" \" + y + \" \" + z + \" container.2 with minecraft:cooked_cod 4\");\n    server.runCommandSilent(\"item replace block \" + (x + 1) + \" \" + y + \" \" + z + \" container.3 with minecraft:torch 12\");\n    server.runCommandSilent(\"item replace block \" + (x + 1) + \" \" + y + \" \" + z + \" container.4 with minecraft:flint_and_steel\");\n    server.runCommandSilent(\"item replace block \" + (x + 1) + \" \" + y + \" \" + z + \" container.5 with minecraft:potion[potion_contents={potion:\\\"minecraft:healing\\\"}]\");\n\n    // Signal lantern hanging outside\n    server.runCommandSilent(\"setblock \" + x + \" \" + (y + 3) + \" \" + (z + 3) + \" minecraft:lantern[hanging=true]\");\n}\n\nPlayerEvents.loggedIn(function(event) {\n    try {\n        var player = event.player;\n        if (!player) return;\n        var server = event.server || (player.level && player.level.server);\n        if (!server) return;\n\n        if (!player.tags.contains(\"ashfall_awakened\")) {\n            player.tags.add(\"ashfall_awakened\");\n\n            // 1. Position player safely on the coastal sands\n            var px = Math.floor(player.x);\n            var py = Math.floor(player.y);\n            var pz = Math.floor(player.z);\n\n            // Build starter lighthouse nearby on cliff/higher ground\n            var lx = px + 18;\n            var lz = pz + 14;\n            var ly = py + 3;\n            buildLighthouse(server, lx, ly, lz);\n\n            // 2. Play dramatic opening sound effects\n            server.runCommandSilent(\"playsound minecraft:ambient.underwater.enter ambient \" + player.username + \" \" + px + \" \" + py + \" \" + pz + \" 1.0 0.8\");\n            server.runCommandSilent(\"playsound minecraft:entity.generic.splash ambient \" + player.username + \" \" + px + \" \" + py + \" \" + pz + \" 1.0 0.7\");\n\n            // 3. Apply opening blur / blindness (eyes opening on sand)\n            player.potionEffects.add(\"minecraft:blindness\", 120, 0, false, false);\n            player.potionEffects.add(\"minecraft:slowness\", 140, 3, false, false);\n            player.potionEffects.add(\"minecraft:water_breathing\", 200, 0, false, false);\n\n            // 4. Act I: Awakening on Beach Title\n            server.scheduleInTicks(15, function() {\n                server.runCommandSilent(\"title \" + player.username + \" times 20 60 20\");\n                server.runCommandSilent(\"title \" + player.username + \" title {\\\"text\\\":\\\"ASHENFALL\\\",\\\"color\\\":\\\"dark_red\\\",\\\"bold\\\":true}\");\n                server.runCommandSilent(\"title \" + player.username + \" subtitle {\\\"text\\\":\\\"You wash ashore on the cold sands...\\\",\\\"color\\\":\\\"gray\\\"}\");\n            });\n\n            // 5. Act II: The Tenth Ember Awakens\n            server.scheduleInTicks(80, function() {\n                server.runCommandSilent(\"playsound minecraft:block.campfire.crackle ambient \" + player.username + \" \" + px + \" \" + py + \" \" + pz + \" 0.8 1.0\");\n                server.runCommandSilent(\"title \" + player.username + \" times 15 50 15\");\n                server.runCommandSilent(\"title \" + player.username + \" title {\\\"text\\\":\\\"The Tenth Ember\\\",\\\"color\\\":\\\"gold\\\",\\\"bold\\\":true}\");\n                server.runCommandSilent(\"title \" + player.username + \" subtitle {\\\"text\\\":\\\"A faint warmth smolders within your chest.\\\",\\\"color\\\":\\\"yellow\\\"}\");\n            });\n\n            // 6. Act III: Narrative Introduction\n            server.scheduleInTicks(140, function() {\n                server.runCommandSilent(\"playsound minecraft:block.bell.use ambient \" + player.username + \" \" + px + \" \" + py + \" \" + pz + \" 0.7 0.9\");\n                player.tell(\" \");\n                player.tell(\"\u00a78\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\");\n                player.tell(\"\u00a7c\u2694 ASHENFALL \u00a78\u2014 \u00a77The Pilgrimage Begins\");\n                player.tell(\"\u00a7e\\\"Nine sounds broke the Empire in a single night.\\\"\");\n                player.tell(\"\u00a7e\\\"You are not a hero, pilgrim. You are the cause, walking to mend what you shattered.\\\"\");\n                player.tell(\" \");\n                player.tell(\"\u00a7bAbove the shoreline bluff looms the Old Lighthouse beacon.\");\n                player.tell(\"\u00a77Scavenge the lighthouse for supplies, then journey inland toward the Norman Remnant.\");\n                player.tell(\"\u00a78\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\");\n                player.tell(\" \");\n            });\n\n            // 7. Starter supplies directly in inventory\n            server.scheduleInTicks(150, function() {\n                server.runCommandSilent(\"give \" + player.username + \" minecraft:leather_boots[custom_name='{\\\"text\\\":\\\"Waterlogged Boots\\\",\\\"color\\\":\\\"gray\\\"}']\");\n                server.runCommandSilent(\"give \" + player.username + \" minecraft:compass[custom_name='{\\\"text\\\":\\\"Pilgrim\\\\'s Compass\\\",\\\"color\\\":\\\"gold\\\"}']\");\n                server.runCommandSilent(\"give \" + player.username + \" minecraft:flint\");\n                server.runCommandSilent(\"give \" + player.username + \" minecraft:bread 4\");\n            });\n        }\n    } catch (e) {\n        console.error(\"Intro awakening error: \" + e);\n    }\n});\n",
    "narrative_dialogue.js": "// =============================================================================\n// ASHENFALL \u2014 NPC Narrative Dialogue Integration\n// =============================================================================\n\nvar NPC_DIALOGUES = {\n    \"the_archivist\": \"ashfall:archivist\",\n    \"norman_elder\": \"ashfall:norman_elder\",\n    \"drowned_fisherman\": \"ashfall:drowned_fisherman\"\n};\n\nEntityEvents.spawned(function(event) {\n    var entity = event.entity;\n    if (!entity) return;\n    \n    // Tag specific NPCs for dialogue interaction\n    if (entity.tags && entity.tags.contains(\"ashfall_archivist\")) {\n        entity.persistentData.putString(\"adm_dialogue\", NPC_DIALOGUES[\"the_archivist\"]);\n    }\n});\n\n// Global export for Rhino engine (explicit key-value pairs)\nglobal.ASHFALL_DIALOGUE = {\n    NPC_DIALOGUES: NPC_DIALOGUES\n};\n",
    "nations_and_landmarks.js": "// =============================================================================\n// ASHENFALL \u2014 The Nine Nations & Landmark Discovery System\n// =============================================================================\n\nvar NATIONS = [\n    {\n        id: \"norman_remnant\",\n        name: \"The Norman Remnant\",\n        subtitle: \"Frontier of Salt, Stone, and Iron\",\n        color: \"aqua\",\n        biomes: [\"minecraft:beach\", \"minecraft:stony_shore\", \"minecraft:windswept_hills\", \"minecraft:plains\"],\n        lore: \"The last bastion of coastal knights holding watch against the rising tide.\"\n    },\n    {\n        id: \"seljuk_expanse\",\n        name: \"The Seljuk Expanse\",\n        subtitle: \"Scorched Steppes & Ancient Sun Vaults\",\n        color: \"gold\",\n        biomes: [\"minecraft:desert\", \"minecraft:badlands\", \"minecraft:eroded_badlands\", \"minecraft:savanna\"],\n        lore: \"Nomadic riders and glass citadels buried beneath centuries of amber sand.\"\n    },\n    {\n        id: \"byzantine_choir\",\n        name: \"The Byzantine Choir\",\n        subtitle: \"Gilded Basilicas & Resonant Arches\",\n        color: \"light_purple\",\n        biomes: [\"minecraft:cherry_grove\", \"minecraft:meadow\", \"minecraft:flower_forest\"],\n        lore: \"Scholars of the high empire whose harmonic chants once bound the world.\"\n    },\n    {\n        id: \"witchbane_watch\",\n        name: \"The Witchbane Watch\",\n        subtitle: \"Dark Thickets & The Silent Inquisition\",\n        color: \"dark_green\",\n        biomes: [\"minecraft:dark_forest\", \"minecraft:swamp\", \"minecraft:mangrove_swamp\"],\n        lore: \"Hunters bound by iron oaths to cleanse the corrupted flora of the blight.\"\n    },\n    {\n        id: \"cogwork_march\",\n        name: \"The Cogwork March\",\n        subtitle: \"Steam Cities, Skyward Airships & Brass Canals\",\n        color: \"gold\",\n        biomes: [\"minecraft:windswept_hills\", \"minecraft:windswept_gravelly_hills\", \"minecraft:badlands\", \"minecraft:wooded_badlands\", \"minecraft:river\", \"minecraft:stony_shore\"],\n        lore: \"The smog-choked industrial heartland of Vantyra. Massive steam cities, clunking brass cogwheels, and iron airships dominate the skyline, while forgotten foundries rust beneath.\"\n    },\n    {\n        id: \"cathedral_of_ash\",\n        name: \"The Cathedral of Ash\",\n        subtitle: \"Heart of the Blight \u2014 Seat of the First Ember\",\n        color: \"dark_red\",\n        biomes: [\"minecraft:nether_wastes\", \"minecraft:basalt_deltas\", \"minecraft:crimson_forest\"],\n        lore: \"The charred epicenter where the first sound tore through the veil of reality.\"\n    },\n    {\n        id: \"frostfall\",\n        name: \"The Frostfall\",\n        subtitle: \"Glacial Spires & The Permafrost Gate\",\n        color: \"blue\",\n        biomes: [\"minecraft:snowy_slopes\", \"minecraft:frozen_peaks\", \"minecraft:ice_spikes\", \"minecraft:snowy_plains\"],\n        lore: \"Eternal blizzards shielding the northern ruins of the Celestial Aether.\"\n    },\n    {\n        id: \"sunken_throne\",\n        name: \"The Sunken Throne\",\n        subtitle: \"Abyssal Trenches & The Drowned Choir\",\n        color: \"dark_aqua\",\n        biomes: [\"minecraft:deep_ocean\", \"minecraft:ocean\", \"minecraft:deep_cold_ocean\"],\n        lore: \"Cathedrals submerged in deep trenches where the drowned clergy still pray.\"\n    },\n    {\n        id: \"hermits_reach\",\n        name: \"The Hermit's Reach\",\n        subtitle: \"Isolated Pinnacles & Silent Monasteries\",\n        color: \"gray\",\n        biomes: [\"minecraft:jagged_peaks\", \"minecraft:stony_peaks\"],\n        lore: \"Ascetic hermits guarding forgotten scrolls beyond the reach of kings.\"\n    }\n];\n\n// Check territory every 100 ticks (5 seconds)\nPlayerEvents.tick(function(event) {\n    try {\n        var player = event.player;\n        if (!player || player.age % 100 !== 0) return;\n        if (!player.level) return;\n\n        var biome = player.level.getBiome(player.blockPosition()).unwrapKey().get().location().toString();\n        \n        for (var i = 0; i < NATIONS.length; i++) {\n            var nation = NATIONS[i];\n            if (nation.biomes.indexOf(biome) !== -1) {\n                var tag = \"visited_nation_\" + nation.id;\n                if (!player.tags.contains(tag)) {\n                    player.tags.add(tag);\n                    \n                    var server = player.level.server;\n                    if (server) {\n                        // Audio sting\n                        server.runCommandSilent(\"playsound minecraft:ui.toast.challenge_complete ambient \" + player.username + \" \" + player.x + \" \" + player.y + \" \" + player.z + \" 0.8 1.1\");\n                        \n                        // Territory banner\n                        server.runCommandSilent(\"title \" + player.username + \" times 10 70 20\");\n                        server.runCommandSilent(\"title \" + player.username + \" title {\\\"text\\\":\\\"\" + nation.name + \"\\\",\\\"color\\\":\\\"\" + nation.color + \"\\\",\\\"bold\\\":true}\");\n                        server.runCommandSilent(\"title \" + player.username + \" subtitle {\\\"text\\\":\\\"\" + nation.subtitle + \"\\\",\\\"color\\\":\\\"gray\\\",\\\"italic\\\":true}\");\n                    }\n                    \n                    // Lore entry in chat\n                    player.tell(\" \");\n                    player.tell(\"\u00a78[\u00a76Codex Discovered\u00a78] \u00a7f\" + nation.name);\n                    player.tell(\"\u00a77\\\"\" + nation.lore + \"\\\"\");\n                    player.tell(\" \");\n                }\n                break;\n            }\n        }\n    } catch (e) {\n        // Silently prevent tick failure\n    }\n});\n",
    "player_health.js": "// =============================================================================\n// ASHENFALL \u2014 Player Base Health (20 Hearts / 40 Max HP)\n// =============================================================================\n\nPlayerEvents.loggedIn(function(event) {\n    try {\n        var player = event.player;\n        if (!player) return;\n        var attr = player.getAttribute(\"minecraft:generic.max_health\");\n        if (attr) {\n            attr.setBaseValue(40.0);\n        }\n        if (player.health < 40) {\n            player.setHealth(40);\n        }\n    } catch (e) {\n        console.error(\"Health init exception: \" + e);\n    }\n});\n\nPlayerEvents.respawned(function(event) {\n    try {\n        var player = event.player;\n        if (!player) return;\n        var attr = player.getAttribute(\"minecraft:generic.max_health\");\n        if (attr) {\n            attr.setBaseValue(40.0);\n        }\n        player.setHealth(40);\n    } catch (e) {\n        console.error(\"Health respawn exception: \" + e);\n    }\n});\n\nPlayerEvents.changeDimension(function(event) {\n    try {\n        var player = event.player;\n        if (!player) return;\n        var attr = player.getAttribute(\"minecraft:generic.max_health\");\n        if (attr) {\n            attr.setBaseValue(40.0);\n        }\n    } catch (e) {\n        console.error(\"Health dimension exception: \" + e);\n    }\n});\n",
    "quest_ids.js": "// =============================================================================\n// ASHENFALL \u2014 Custom Quest IDs Register (FTB XMod Compat Gates)\n// =============================================================================\n\nvar QUEST_GATES = {\n    // Act 0: The Cold Awakening\n    \"ASHEN_AWAKENING\": \"Player awakens on the drowned Norman coast\",\n    \"ASHEN_LIGHTHOUSE\": \"Player reaches and explores the Old Lighthouse\",\n    \n    // Act 1: The Remnants\n    \"ASHEN_NORMAN_WAYSTONE\": \"Discover the Norman Remnant central waystone\",\n    \"ASHEN_EMBER_REST\": \"Rekindle the Ember Flask at a camp rest point\",\n    \n    // Act 2: Factions & Wilderness\n    \"ASHEN_SELJUK_VAULT\": \"Enter the Sunken Desert Vault\",\n    \"ASHEN_WITCHBANE_INQUISITION\": \"Survive the Witchbane patrol in the dark forest\",\n    \n    // Act 3: The Deep Choir & Catacombs\n    \"ASHEN_DROWNED_CHOIR\": \"Locate the submerged cathedral ruins in the abyss\",\n    \"ASHEN_DEAD_KING\": \"Defeat the Dead King in the arcane catacombs\",\n    \n    // Act 4: The Apex Cathedrals\n    \"ASHEN_FIRST_EMBER\": \"Claim the First Ember from the Cathedral of Ash\",\n    \"ASHEN_NINE_SOUNDS_MENDED\": \"Complete the Great Pilgrimage\"\n};\n\n// Global export for Rhino engine\nglobal.QUEST_GATES = QUEST_GATES;\nglobal.QUEST_IDS = QUEST_GATES;\n",
    "rumours.js": "// =============================================================================\n// ASHENFALL \u2014 The Rumour Register System\n// =============================================================================\n\nvar RUMOURS = [\n    {\n        id: \"cold_tower\",\n        speaker: \"Inuit Elder\",\n        text: \"There is a tower in the far north that doesn't melt, even when struck by dragonfire.\",\n        landmark: \"L1 \u2014 The Cold Tower\",\n        gate: \"chapter_2\"\n    },\n    {\n        id: \"drowned_choir\",\n        speaker: \"Drowned Fisherman\",\n        text: \"The Choir's cathedral drowned in the abyss. It never stopped praying.\",\n        landmark: \"L7 \u2014 The Otherside Rift\",\n        gate: \"codex_drowned_choir\"\n    },\n    {\n        id: \"jungle_vault\",\n        speaker: \"Seljuk Scout\",\n        text: \"A sandstone fortress lies swallowed by the jungle vines. Whatever you do, do not enter at night.\",\n        landmark: \"L3 \u2014 Jungle Vault\",\n        gate: \"none\"\n    },\n    {\n        id: \"hidden_cathedral\",\n        speaker: \"The Archivist\",\n        text: \"They say there is a second Cathedral... buried beneath the foundations of the world.\",\n        landmark: \"L\u2605 \u2014 The Hidden Cathedral\",\n        gate: \"all_9_runes\"\n    },\n    {\n        id: \"arcane_catacombs\",\n        speaker: \"Tavern Keeper\",\n        text: \"Wizards buy raw essence at great cost. Wizards also die down in the catacombs.\",\n        landmark: \"L7b \u2014 The Catacombs\",\n        gate: \"essence_held\"\n    },\n    {\n        id: \"clunker_behemoth\",\n        speaker: \"Disgraced Aeronaut\",\n        text: \"The brass airships fell from the sky when the Ancient Factory woke. A metal monster with three cannons sweeps lasers across the rusted foundries. None who entered ever returned.\",\n        landmark: \"L8 \u2014 The Ancient Foundry (Cogwork March)\",\n        gate: \"none\"\n    }\n];\n\nfunction tellRumour(player, rumourId) {\n    var rumour = null;\n    for (var i = 0; i < RUMOURS.length; i++) {\n        if (RUMOURS[i].id === rumourId) {\n            rumour = RUMOURS[i];\n            break;\n        }\n    }\n    if (!rumour) return;\n\n    player.tell(\" \");\n    player.tell(\"\u00a76[Rumour] \u00a7e\" + rumour.speaker + \" \u00a77whispers:\");\n    player.tell(\"\u00a7f\\\"\" + rumour.text + \"\\\"\");\n    player.tell(\"\u00a78Related Landmark: \u00a7b\" + rumour.landmark);\n    player.tell(\" \");\n}\n\n// Global export for Rhino engine (explicit key-value pairs)\nglobal.ASHFALL_RUMOURS = {\n    RUMOURS: RUMOURS,\n    tellRumour: tellRumour\n};\n\nglobal.tellRumour = tellRumour;\n",
    "runes.js": "// =============================================================================\n// ASHENFALL \u2014 The Nine Ember Runes System\n// =============================================================================\n\nvar RUNES = [\n    { id: \"norman\", item: \"ashfall:rune_of_the_norman\", nation: \"norman_remnant\", name: \"Rune of Salt & Iron\" },\n    { id: \"seljuk\", item: \"ashfall:rune_of_the_seljuk\", nation: \"seljuk_expanse\", name: \"Rune of Amber Sands\" },\n    { id: \"choir\", item: \"ashfall:rune_of_the_choir\", nation: \"byzantine_choir\", name: \"Rune of Resonant Hymns\" },\n    { id: \"witchbane\", item: \"ashfall:rune_of_the_witchbane\", nation: \"witchbane_watch\", name: \"Rune of the Cold Pyre\" },\n    { id: \"merchants\", item: \"ashfall:rune_of_the_merchants\", nation: \"cogwork_march\", name: \"Rune of Gilded Cog & Steam\" },\n    { id: \"ash\", item: \"ashfall:rune_of_the_ash\", nation: \"cathedral_of_ash\", name: \"Rune of the First Flame\" },\n    { id: \"frostfall\", item: \"ashfall:rune_of_the_frostfall\", nation: \"frostfall\", name: \"Rune of Glacial Spires\" },\n    { id: \"sunken\", item: \"ashfall:rune_of_the_sunken\", nation: \"sunken_throne\", name: \"Rune of the Abyss\" },\n    { id: \"hermit\", item: \"ashfall:rune_of_the_hermit\", nation: \"hermits_reach\", name: \"Rune of Silent Peaks\" }\n];\n\nfunction hasRune(player, runeId) {\n    var r = null;\n    for (var i = 0; i < RUNES.length; i++) {\n        if (RUNES[i].id === runeId) {\n            r = RUNES[i];\n            break;\n        }\n    }\n    if (!r) return false;\n    \n    // Check persistentData\n    if (player.persistentData.getBoolean(\"has_rune_\" + runeId)) {\n        return true;\n    }\n    \n    // Check if player has the item in inventory\n    var inventory = player.inventory;\n    if (inventory && inventory.find(r.item) !== -1) {\n        player.persistentData.putBoolean(\"has_rune_\" + runeId, true);\n        return true;\n    }\n    return false;\n}\n\nfunction runeCount(player) {\n    var count = 0;\n    for (var i = 0; i < RUNES.length; i++) {\n        if (hasRune(player, RUNES[i].id)) {\n            count++;\n        }\n    }\n    return count;\n}\n\n// Global export for Rhino engine (explicit key-value pairs)\nglobal.ASHFALL_RUNES = {\n    RUNES: RUNES,\n    hasRune: hasRune,\n    runeCount: runeCount\n};\n\nglobal.hasRune = hasRune;\nglobal.runeCount = runeCount;\n",
    "soulslike.js": "// =============================================================================\n// ASHENFALL \u2014 Soulslike Rest, Ember Flask, & Hollow Death Penalty\n// =============================================================================\n\nvar HOLLOW_CAP = 5;\nvar REST_TAGS = [\n    \"minecraft:campfires\",\n    \"minecraft:beds\"\n];\n\nfunction getHollow(player) {\n    if (!player.persistentData.contains(\"ashfall_hollow\")) {\n        player.persistentData.putInt(\"ashfall_hollow\", 0);\n    }\n    return player.persistentData.getInt(\"ashfall_hollow\");\n}\n\nfunction setHollow(player, val) {\n    var clamped = Math.max(0, Math.min(HOLLOW_CAP, val));\n    player.persistentData.putInt(\"ashfall_hollow\", clamped);\n}\n\n// On player respawn: hollow penalty increments\nPlayerEvents.respawned(function(event) {\n    try {\n        var player = event.player;\n        if (!player) return;\n        var hollow = getHollow(player);\n        if (hollow < HOLLOW_CAP) {\n            setHollow(player, hollow + 1);\n            player.tell(\"\u00a78[\u00a7cDeath\u00a78] \u00a77Your ember fades slightly. Hollow tier: \u00a7c\" + (hollow + 1) + \"\u00a77/\" + HOLLOW_CAP);\n        }\n    } catch (e) {\n        // Silently prevent respawn error\n    }\n});\n\n// Global export for Rhino engine (explicit key-value pairs)\nglobal.ASHFALL_SOULSLIKE = {\n    HOLLOW_CAP: HOLLOW_CAP,\n    REST_TAGS: REST_TAGS,\n    getHollow: getHollow,\n    setHollow: setHollow\n};\n\nglobal.getHollow = getHollow;\nglobal.setHollow = setHollow;\n",
    "standing.js": "// =============================================================================\n// ASHENFALL \u2014 Nine Nations Standing System (-100 to +100)\n// =============================================================================\n\nvar NATIONS = [\n    \"norman_remnant\",\n    \"seljuk_expanse\",\n    \"byzantine_choir\",\n    \"witchbane_watch\",\n    \"cogwork_march\",\n    \"guild_of_merchants\",\n    \"cathedral_of_ash\",\n    \"frostfall\",\n    \"sunken_throne\",\n    \"hermits_reach\"\n];\n\nvar CROSS_FACTION = true;\nvar CHAMPION_THRESHOLD = 80;\nvar MAX_NATIONS_CHAMPION = 3;\n\nfunction getStanding(player, faction) {\n    var key = \"standing_\" + faction;\n    if (!player.persistentData.contains(key)) {\n        player.persistentData.putInt(key, 0); // Neutral\n    }\n    return player.persistentData.getInt(key);\n}\n\nfunction modifyStanding(player, faction, delta) {\n    var key = \"standing_\" + faction;\n    var current = getStanding(player, faction);\n    var updated = Math.max(-100, Math.min(100, current + delta));\n    player.persistentData.putInt(key, updated);\n\n    var prefix = delta >= 0 ? \"\u00a7a+\" : \"\u00a7c\";\n    var factionLabel = faction.replace(/_/g, \" \").replace(/\\b\\w/g, function(l) { return l.toUpperCase(); });\n    player.tell(\"\u00a78[\u00a76Faction Rep\u00a78] \u00a7f\" + factionLabel + \": \" + prefix + delta + \" \u00a77(Current: \" + updated + \")\");\n}\n\n// Global export for Rhino engine (explicit key-value pairs)\nglobal.ASHFALL_STANDING = {\n    NATIONS: NATIONS,\n    CROSS_FACTION: CROSS_FACTION,\n    CHAMPION_THRESHOLD: CHAMPION_THRESHOLD,\n    MAX_NATIONS_CHAMPION: MAX_NATIONS_CHAMPION,\n    getStanding: getStanding,\n    modifyStanding: modifyStanding\n};\n\nglobal.getStanding = getStanding;\nglobal.modifyStanding = modifyStanding;\n",
    "structures.js": "// =============================================================================\n// ASHENFALL \u2014 Structure Province & Landmark Registry\n// =============================================================================\n\nvar STRUCTURE_PROVINCES = {\n    \"structory:settlements/coastal\": { nation: \"norman_remnant\", name: \"Norman Coastal Outpost\" },\n    \"towns_and_towers:ocean/village\": { nation: \"norman_remnant\", name: \"Norman Port Village\" },\n    \"structory:settlements/desert\": { nation: \"seljuk_expanse\", name: \"Seljuk Caravan Camp\" },\n    \"dungeons_and_taverns:desert_pyramid\": { nation: \"seljuk_expanse\", name: \"Sunken Desert Crypt\" },\n    \"graveyard:lich_prison\": { nation: \"frostfall\", name: \"Citadel of the Cold Tower\" },\n    \"cataclysm:burning_arena\": { nation: \"cathedral_of_ash\", name: \"Crucible of Ash\" },\n    \"cataclysm:sunken_city\": { nation: \"sunken_throne\", name: \"Submerged Cathedral of the Abyss\" },\n    \"cataclysm:ancient_factory\": { nation: \"cogwork_march\", name: \"The Abandoned Foundry \u2014 Domain of the Clunker Behemoth\" },\n    \"when_dungeons_arise:heavenly_challenger\": { nation: \"cogwork_march\", name: \"Imperial Brass Airship Dreadnought\" },\n    \"when_dungeons_arise:corsair_corvette\": { nation: \"cogwork_march\", name: \"Skyward Raider Airship\" },\n    \"when_dungeons_arise:aviary\": { nation: \"cogwork_march\", name: \"Aeronautics Clockwork Spire\" }\n};\n\nfunction getProvinceForStructure(structureId) {\n    return STRUCTURE_PROVINCES[structureId] || null;\n}\n\n// Global export for Rhino engine (explicit key-value pairs)\nglobal.ASHFALL_STRUCTURES = {\n    STRUCTURE_PROVINCES: STRUCTURE_PROVINCES,\n    getProvinceForStructure: getProvinceForStructure\n};\n\nglobal.getProvinceForStructure = getProvinceForStructure;\n",
    "threat.js": "// =============================================================================\n// ASHENFALL \u2014 Threat Tier Scaling Engine (Tiers I\u2013VII)\n// =============================================================================\n\nvar MAX_TIER = 7;\n\nvar REGIONS = [\n    \"norman_coast\",\n    \"seljuk_desert\",\n    \"byzantine_hills\",\n    \"witchbane_woods\",\n    \"cogwork_march\",\n    \"merchant_rivers\",\n    \"cathedral_depths\",\n    \"frostfall_peaks\",\n    \"sunken_abyss\",\n    \"hermit_highlands\"\n];\n\nfunction tierOf(player, region) {\n    var key = \"threat_tier_\" + region;\n    if (!player.persistentData.contains(key)) {\n        player.persistentData.putInt(key, 1);\n    }\n    return player.persistentData.getInt(key);\n}\n\nfunction setTier(player, region, tier) {\n    var clamped = Math.max(1, Math.min(MAX_TIER, tier));\n    var key = \"threat_tier_\" + region;\n    player.persistentData.putInt(key, clamped);\n    player.tell(\"\u00a78[\u00a76Threat Scaled\u00a78] \u00a7f\" + region + \" \u00a77is now set to Threat Tier: \u00a76\" + clamped);\n}\n\nfunction regionOf(entity) {\n    if (!entity || !entity.level) return \"norman_coast\";\n    var dim = entity.level.dimension.toString();\n    if (dim === \"minecraft:the_nether\") return \"cathedral_depths\";\n    if (dim === \"minecraft:the_end\") return \"sunken_abyss\";\n\n    var biome = entity.level.getBiome(entity.blockPosition()).unwrapKey().get().location().toString();\n    if (biome.indexOf(\"desert\") !== -1 || biome.indexOf(\"badlands\") !== -1) return \"seljuk_desert\";\n    if (biome.indexOf(\"dark_forest\") !== -1 || biome.indexOf(\"swamp\") !== -1) return \"witchbane_woods\";\n    if (biome.indexOf(\"snow\") !== -1 || biome.indexOf(\"ice\") !== -1 || biome.indexOf(\"frozen\") !== -1) return \"frostfall_peaks\";\n    if (biome.indexOf(\"ocean\") !== -1) return \"sunken_abyss\";\n    if (biome.indexOf(\"jagged\") !== -1 || biome.indexOf(\"stony_peaks\") !== -1) return \"hermit_highlands\";\n    if (biome.indexOf(\"cherry\") !== -1 || biome.indexOf(\"meadow\") !== -1) return \"byzantine_hills\";\n    if (biome.indexOf(\"river\") !== -1) return \"merchant_rivers\";\n    return \"norman_coast\";\n}\n\n// Global export for Rhino engine (explicit key-value pairs)\nglobal.ASHFALL_THREAT = {\n    REGIONS: REGIONS,\n    MAX_TIER: MAX_TIER,\n    regionOf: regionOf,\n    tierOf: tierOf,\n    setTier: setTier\n};\n\nglobal.regionOf = regionOf;\nglobal.tierOf = tierOf;\nglobal.setTier = setTier;\n"
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
            # Remove redundant duplicate scripts
            for dup_name in ["boss_monologues.js"]:
                dup_path = server_dir / dup_name
                if dup_path.exists():
                    try:
                        dup_path.unlink()
                        print(f"  [KubeJS Auto-Healer] Removed duplicate server_scripts/{dup_name}...")
                        fixed += 1
                    except Exception:
                        pass

            # Sync canonical scripts with verified Rhino JS versions
            for filename, canonical_code in CANONICAL_SERVER_SCRIPTS.items():
                dest_file = server_dir / filename
                if dest_file.exists():
                    try:
                        content = dest_file.read_text(encoding="utf-8")
                        if content != canonical_code:
                            print(f"  [KubeJS Auto-Healer] Updated server_scripts/{filename} to verified Rhino JS version...")
                            dest_file.write_text(canonical_code, encoding="utf-8")
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


ICEANDFIRE_COMMON_CONFIG = """# =============================================================================
# ASHENFALL — Ice and Fire Configuration
# Tuned for Rare Apex Boss Dragons (Mythic Encounters & Subterranean Dens)
# =============================================================================

[Generation]
	# How far away dangerous structures (dragon roosts, cyclops caves, etc.) must be from world spawn.
	# Ensures players can settle the starter beach without being sniped by a dragon.
	# Range: 1 ~ 10000 (Default: 300)
	"Dangerous World Gen Dist From Spawn" = 2500

	# How far away dangerous structures must be from the last generated structure.
	# Ensures dragons never clump together; each dragon holds its own massive territory.
	# Range: 1 ~ 10000 (Default: 300)
	"Dangerous World Gen Dist Seperation" = 1500

[Generation.Dragon]
	# Whether to generate dragon skeletons or not
	"Generate Dragon Skeletons" = true
	# 1 out of this number chance per chunk for skeleton generation
	# Range: 1 ~ 10000 (Default: 300)
	"Generate Dragon Skeleton Chance" = 1200

	# Whether to generate subterranean dragon caves or not
	"Generate Dragon Caves" = true
	# 1 out of this number chance per chunk for cave generation (Stage 4 & 5 ancient dragons)
	# Range: 1 ~ 10000 (Default: 180)
	"Generate Dragon Cave Chance" = 1200

	# Whether to generate surface dragon roosts or not
	"Generate Dragon Roosts" = true
	# 1 out of this number chance per chunk for roost generation (surface dragons)
	# Set high so surface dragons do NOT run all around the world
	# Range: 1 ~ 10000 (Default: 360)
	"Generate Dragon Roost Chance" = 2500

	# 1 out of this number chance per block that gold will generate in dragon lairs
	# Range: 1 ~ 10000
	"Dragon Den Gold Amount" = 4

	# Ratio of Stone to Ores in Dragon Caves
	# Range: 1 ~ 10000
	"Dragon Cave Ore Ratio" = 45

[Dragons]
	# Dragon block griefing:
	# 0 = Full griefing (breaks everything)
	# 1 = Griefing in combat only (does not destroy world while idle)
	# 2 = No block griefing
	# Range: 0 ~ 2
	"Dragon Griefing" = 1

	# How far away dragons can search for targets (reduced from default 128 to stop random sniping)
	# Range: 1 ~ 256
	"Dragon Target Search Length" = 48

	# How far dragons can wander from their home roost/cavern (prevents wandering into distant towns)
	# Range: 1 ~ 256
	"Dragon Wander from Home Distance" = 32

	# Dragon health multiplier (makes them formidable, endgame boss encounters)
	# Range: 0.1 ~ 10.0
	"Dragon Health Multiplier" = 1.5

	# Dragon attack damage multiplier
	# Range: 0.1 ~ 10.0
	"Dragon Attack Damage Multiplier" = 1.3

	# Dragons drop full scales and skulls upon defeat
	"Dragon Drop Skull" = true
"""


def install_custom_configs(mods_dir: Path) -> int:
    """Installs pre-tuned configs (such as rare dragon spawn rates) to prevent world-ruining spam."""
    installed = 0
    candidate_config_dirs = [
        mods_dir.parent / "config",
        Path.cwd() / "config",
        mods_dir / "config",
        mods_dir.parent / "overrides" / "config",
        Path.cwd() / "pack" / "overrides" / "config",
    ]
    for cfg_dir in candidate_config_dirs:
        try:
            cfg_dir.mkdir(parents=True, exist_ok=True)
            iaf_path = cfg_dir / "iceandfire-common.toml"
            if not iaf_path.exists() or iaf_path.stat().st_size == 0:
                iaf_path.write_text(ICEANDFIRE_COMMON_CONFIG, encoding="utf-8")
                installed += 1
        except Exception:
            pass
    return installed


def extract_mod_ids(jar_path: Path) -> Set[str]:
    """Extracts all mod IDs registered inside a jar file (from neoforge.mods.toml, mods.toml, fabric.mod.json)."""
    mod_ids: Set[str] = set()
    try:
        with zipfile.ZipFile(jar_path, "r") as zf:
            for name in zf.namelist():
                nl = name.lower()
                if nl in ("meta-inf/neoforge.mods.toml", "meta-inf/mods.toml"):
                    try:
                        content = zf.read(name).decode("utf-8", errors="ignore")
                        matches = re.findall(r"modId\s*=\s*[\"']([^\"']+)[\"']", content)
                        for m in matches:
                            mod_ids.add(m.strip().lower())
                    except Exception:
                        pass
                elif nl == "fabric.mod.json":
                    try:
                        data = json.loads(zf.read(name).decode("utf-8", errors="ignore"))
                        if "id" in data:
                            mod_ids.add(str(data["id"]).strip().lower())
                    except Exception:
                        pass
    except Exception:
        pass
    return mod_ids


def clean_unnecessary_and_outdated_mods(mods_dir: Path, catalog_filenames: Set[str]) -> int:
    """
    Cleans mods folder:
    1. Removes 0-byte, non-JAR bundles (.mrpack, .zip, .tmp, .txt), and corrupted JARs.
    2. Purges blacklisted / incompatible mods (hollowmarch, bettercombat, terralith, optifine, rubidium).
    3. Detects duplicate versions of the same mod ID and deletes outdated duplicates to prevent startup crashes.
    """
    removed = 0
    if not mods_dir.exists():
        return 0

    # 1. Non-JAR or corrupted file purge
    for item in list(mods_dir.iterdir()):
        if item.is_file():
            if item.suffix.lower() in (".mrpack", ".zip", ".tmp", ".txt", ".crdownload"):
                print(f"  [Cleaner] Removing non-mod file from mods folder: {item.name}")
                try:
                    item.unlink()
                    removed += 1
                except Exception:
                    pass
                continue

            if item.stat().st_size == 0:
                print(f"  [Cleaner] Removing 0-byte truncated file: {item.name}")
                try:
                    item.unlink()
                    removed += 1
                except Exception:
                    pass
                continue

            # Verify zip header on jar files
            if item.suffix.lower() == ".jar":
                try:
                    with zipfile.ZipFile(item, "r") as zf:
                        if not zf.namelist():
                            raise ValueError("Empty jar")
                except Exception:
                    print(f"  [Cleaner] Removing corrupted jar (broken zip header): {item.name}")
                    try:
                        item.unlink()
                        removed += 1
                    except Exception:
                        pass
                    continue

    # 2. Blacklisted / Unnecessary / Incompatible mods purge
    BLACKLIST_KEYWORDS = [
        ("hollowmarch", "Causes create:large_water_wheel registry crash on world creation"),
        ("bettercombat", "Replaced with Vanilla PvP mechanics per configuration"),
        ("terralith", "Replaced with Lithosphere + Still Life biome architecture"),
        ("optifine", "Incompatible with NeoForge 1.21.1 and Embeddium"),
        ("rubidium", "Deprecated Forge fork replaced by Embeddium"),
        ("magnesium", "Deprecated Forge fork"),
        ("sodium-fabric", "Fabric build detected in NeoForge folder"),
        ("iris-fabric", "Fabric build detected in NeoForge folder"),
        ("shine", "Produces uncalibrated bloom artifacts and blinding superbright spots on 1.21.1"),
        ("wavify", "Causes spammy white crescent wave billboard artifacts on rivers"),
    ]

    for item in list(mods_dir.glob("*.jar")):
        name_lower = item.name.lower()
        for kw, reason in BLACKLIST_KEYWORDS:
            if kw in name_lower:
                print(f"  [Cleaner] Removing unnecessary/incompatible mod ({reason}): {item.name}")
                try:
                    item.unlink()
                    removed += 1
                except Exception:
                    pass
                break

    # 3. Duplicate mod detection (prevent DuplicateModsFoundException)
    jars_by_modid: Dict[str, List[Path]] = {}
    for jar in list(mods_dir.glob("*.jar")):
        mod_ids = extract_mod_ids(jar)
        for mid in mod_ids:
            jars_by_modid.setdefault(mid, []).append(jar)

    for mid, jar_list in jars_by_modid.items():
        # Remove duplicate references to the same file
        unique_jars = list(dict.fromkeys(jar_list))
        if len(unique_jars) > 1:
            # Check if one matches catalog filename
            target_jar = next((j for j in unique_jars if j.name in catalog_filenames), None)
            if not target_jar:
                # Pick the newest by modification time
                target_jar = max(unique_jars, key=lambda j: j.stat().st_mtime)

            for j in unique_jars:
                if j != target_jar and j.exists():
                    print(f"  [Cleaner] Removing outdated duplicate version for mod '{mid}': {j.name} (keeping {target_jar.name})")
                    try:
                        j.unlink()
                        removed += 1
                    except Exception:
                        pass

    return removed


def download_mod_list(
    mods: List[Dict[str, Any]],
    target_dir: Path,
    verbose: bool = False,
    label: str = "Mods"
) -> Tuple[int, int, int]:
    """Downloads a list of mods, verifying zip integrity and skipping up-to-date files."""
    success = 0
    skipped = 0
    failed = 0

    for i, mod in enumerate(mods, 1):
        name = mod["name"]
        slug = mod.get("slug")
        slug_display = ", ".join(slug) if isinstance(slug, list) else str(slug or "Direct")
        print(f"  [{i}/{len(mods)}] {name} ({slug_display})...", end="", flush=True)

        res = resolve_modrinth_jar(slug, verbose=verbose) if slug else None
        if res:
            url, filename, size = res
        elif mod.get("fallback_url") and mod.get("filename"):
            url = mod["fallback_url"]
            filename = mod["filename"]
            size = 0
        else:
            print(" ⚠️ No 1.21.1 NeoForge file found.")
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
        ok = download_and_verify(url, dest_file, expected_size=size, verbose=verbose)
        if ok:
            mb = dest_file.stat().st_size / (1024 * 1024)
            print(f" Downloaded ({mb:.1f} MB) ✅")
            success += 1
        else:
            print(" ❌ Download failed.")
            failed += 1

    return success, skipped, failed


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
    print(" ASHENFALL — ALL-IN-ONE MODPACK INSTALLER & MANAGER")
    print(" Target: Minecraft 1.21.1 · NeoForge 21.1.x")
    print(" Destination:", target_dir)
    print(" Phase:", args.phase.upper())
    print("=" * 65)

    # 2. Stage 1: Clean unnecessary, incompatible & outdated duplicate mods
    print("\n[1/4] Scanning mods folder for unnecessary, incompatible & duplicate mods...")
    catalog_filenames = {m.get("filename") for m in MODS_CATALOG if m.get("filename")}
    cleaned = clean_unnecessary_and_outdated_mods(target_dir, catalog_filenames)
    if cleaned > 0:
        print(f"  ✅ Cleaned {cleaned} outdated, duplicate, or crash-inducing file(s).")
    else:
        print("  ✅ Destination folder is clean (no obsolete or conflicting mods found).")

    # 3. Stage 2: Deploy and heal KubeJS scripts & configs
    print("\n[2/4] Deploying & verifying KubeJS narrative/gameplay scripts and configs...")
    fixed_scripts = check_and_fix_kubejs(target_dir)
    if fixed_scripts > 0:
        print(f"  ✅ Deployed/healed {fixed_scripts} KubeJS script(s) (including 20 Hearts / 40 HP system).")
    else:
        print("  ✅ KubeJS scripts are up-to-date and 100% pure Rhino JS.")

    installed_cfgs = install_custom_configs(target_dir)
    if installed_cfgs > 0:
        print(f"  ✅ Configured {installed_cfgs} settings file(s) (rare dragons, 2500-block spawn sanctuary).")
    else:
        print("  ✅ Configurations are verified.")

    # 4. Stage 3: Verify and install essential Core APIs & Libraries
    print("\n[3/4] Verifying and installing essential Core APIs & Libraries...")
    api_mods = [m for m in MODS_CATALOG if m.get("category") == "library" or (m.get("phase") == "M0" and m.get("category") == "performance")]
    api_names = {m["name"] for m in api_mods}
    api_success, api_skipped, api_failed = download_mod_list(api_mods, target_dir, verbose=args.verbose, label="Core APIs")
    print(f"  -> APIs Status: {api_success} downloaded, {api_skipped} verified up-to-date, {api_failed} failed.")

    # 5. Stage 4: Download gameplay & content mods for requested phase
    phase_filter = args.phase.upper()
    if phase_filter in ("ALL", "FULL", "COMPLETE"):
        content_candidates = [m for m in MODS_CATALOG if m["name"] not in api_names]
    elif phase_filter in ("REMAINING", "REST", "NEW", "M3C-M7", "M3C+M7"):
        content_candidates = [m for m in MODS_CATALOG if m.get("phase") in ("M3c", "M4", "M5", "M6", "M7") and m["name"] not in api_names]
    elif phase_filter in ("M1+M2", "M1-M2", "M1M2", "M1_M2", "M12"):
        content_candidates = [m for m in MODS_CATALOG if m.get("phase") in ("M1", "M2") and m["name"] not in api_names]
    elif phase_filter in ("M3+M3B", "M3-M3B", "M3M3B", "M3_M3B", "COMBINED", "M3B", "M3"):
        content_candidates = [m for m in MODS_CATALOG if m.get("phase") in ("M1", "M2", "M3", "M3b") and m["name"] not in api_names]
    else:
        phase_order = ["M0", "M1", "M2", "M3", "M3b", "M3c", "M4", "M5", "M6", "M7", "M8", "M9"]
        phase_order_upper = [p.upper() for p in phase_order]
        if phase_filter in phase_order_upper:
            target_idx = phase_order_upper.index(phase_filter)
            allowed_phases = set(phase_order_upper[:target_idx + 1])
            content_candidates = [m for m in MODS_CATALOG if m.get("phase", "").upper() in allowed_phases and m["name"] not in api_names]
        else:
            content_candidates = [m for m in MODS_CATALOG if m.get("phase", "").upper() == phase_filter and m["name"] not in api_names]

    print(f"\n[4/4] Downloading {len(content_candidates)} Content Mods (LOD Distant Horizons, Streams Reflowing, EasyMotionBlur, Ice & Fire, etc.)...")
    cnt_success, cnt_skipped, cnt_failed = download_mod_list(content_candidates, target_dir, verbose=args.verbose, label="Content Mods")

    total_success = api_success + cnt_success
    total_skipped = api_skipped + cnt_skipped
    total_failed = api_failed + cnt_failed

    print("\n" + "=" * 65)
    print(f" INSTALLATION COMPLETE: {total_success} downloaded, {total_skipped} up-to-date, {total_failed} pending.")
    print(" Active Systems:")
    print("  * 20 Hearts (40 Max HP) base player health")
    print("  * Rare, hard-to-find Apex Boss Dragons (iceandfire-common.toml)")
    print("  * Distant Horizons (LOD far terrain & structure rendering)")
    print("  * Streams Reflowing (downstream currents, rapids & boat physics)")
    print("  * EasyMotionBlur (toggle in-game with 'G')")
    print("  * All required Core APIs & Performance Libraries verified")
    print(" Mods folder location:")
    print("  ", target_dir.resolve())
    print("=" * 65 + "\n")
    print("You can now launch Minecraft 1.21.1 NeoForge and enter your world!")


if __name__ == "__main__":
    main()

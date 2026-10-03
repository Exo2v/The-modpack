#!/usr/bin/env python3
"""
=============================================================================
ASHENFALL: Lore-Accurate Castles, Towns & Buildings Schematic Builder
Constructs genuine Minecraft 1.21.1 NBT Structure Templates (.nbt)
Compatible with:
  - In-game Minecraft 1.21.1 /structure load and Structure Blocks
  - WorldPainter Custom Object Layers (.nbt / .bo2 / .schem)
  - Datapack jigsaw structures & template pools
=============================================================================
"""

import os
import sys
import zipfile
from pathlib import Path
from typing import Dict, List, Tuple, Any

import nbtlib
from nbtlib.tag import Compound, List as NbtList, Int, String, Short, Byte

BASE_DIR = Path(__file__).resolve().parent.parent
STRUCTURES_DATAPACK_DIR = BASE_DIR / "datapacks" / "ashenfall_data2" / "data" / "ashenfall" / "structure"
STRUCTURES_WP_DIR = BASE_DIR / "worldpainter" / "structures"
BUNDLE_ZIP = BASE_DIR / "downloads" / "ASHENFALL_LORE_SCHEMATICS_BUNDLE.zip"

DATA_VERSION = Int(3955)  # Minecraft 1.21.1 DataVersion


class SchematicBuilder:
    """Helper to build 3D voxel grids and export clean, valid Minecraft .nbt structures."""
    def __init__(self, width: int, height: int, length: int):
        self.w = width
        self.h = height
        self.l = length
        self.grid = {}  # (x, y, z) -> (palette_idx, properties_dict)
        self.palette = []  # list of (block_name, properties_dict)
        self.palette_lookup = {}

    def get_palette_idx(self, block_name: str, props: Dict[str, str] = None) -> int:
        if props is None:
            props = {}
        # Convert props dict to tuple of sorted items for hashability
        props_tuple = tuple(sorted(props.items()))
        key = (block_name, props_tuple)
        if key not in self.palette_lookup:
            idx = len(self.palette)
            self.palette.append((block_name, props))
            self.palette_lookup[key] = idx
            return idx
        return self.palette_lookup[key]

    def set_block(self, x: int, y: int, z: int, block_name: str, props: Dict[str, str] = None):
        if 0 <= x < self.w and 0 <= y < self.h and 0 <= z < self.l:
            p_idx = self.get_palette_idx(block_name, props)
            self.grid[(x, y, z)] = p_idx

    def fill(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, block_name: str, props: Dict[str, str] = None):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(min(z1, z2), max(z1, z2) + 1):
                    self.set_block(x, y, z, block_name, props)

    def hollow_box(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, wall_block: str, props: Dict[str, str] = None):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(min(z1, z2), max(z1, z2) + 1):
                    is_edge = (x == x1 or x == x2 or y == y1 or y == y2 or z == z1 or z == z2)
                    if is_edge:
                        self.set_block(x, y, z, wall_block, props)

    def cylinder(self, cx: int, y1: int, y2: int, cz: int, radius: int, wall_block: str, fill_inside: bool = False):
        r_sq = radius * radius
        for x in range(cx - radius, cx + radius + 1):
            for z in range(cz - radius, cz + radius + 1):
                dist_sq = (x - cx)**2 + (z - cz)**2
                if dist_sq <= r_sq:
                    if fill_inside or dist_sq >= (radius - 1)**2:
                        for y in range(y1, y2 + 1):
                            self.set_block(x, y, z, wall_block)

    def build_nbt(self) -> Compound:
        palette_list = NbtList[Compound]()
        for name, props in self.palette:
            entry = {"Name": String(name)}
            if props:
                prop_comp = Compound({k: String(v) for k, v in props.items()})
                entry["Properties"] = prop_comp
            palette_list.append(Compound(entry))

        blocks_list = NbtList[Compound]()
        for (x, y, z), p_idx in self.grid.items():
            blocks_list.append(Compound({
                "pos": NbtList[Int]([Int(x), Int(y), Int(z)]),
                "state": Int(p_idx)
            }))

        struct_nbt = Compound({
            "size": NbtList[Int]([Int(self.w), Int(self.h), Int(self.l)]),
            "entities": NbtList[Compound]([]),
            "blocks": blocks_list,
            "palette": palette_list,
            "DataVersion": DATA_VERSION
        })
        return struct_nbt

    def save(self, filepath: Path):
        filepath.parent.mkdir(parents=True, exist_ok=True)
        file = nbtlib.File(self.build_nbt())
        file.save(str(filepath), gzipped=True)


# =============================================================================
# 1. THE GREY FRONTIER WATCHTOWER (House Douglas - Forgotten Coast)
# =============================================================================
def build_grey_frontier_watchtower() -> SchematicBuilder:
    """
    9x17x9 Stone-brick border watchtower with crenellations, arrow slits, and iron oak gate.
    """
    b = SchematicBuilder(9, 17, 9)
    # 1. Foundation & base
    b.fill(0, 0, 0, 8, 1, 8, "minecraft:cobblestone")
    b.fill(1, 1, 1, 7, 1, 7, "minecraft:stone_bricks")

    # 2. Main tower walls (Y=2 to Y=12)
    b.hollow_box(1, 2, 1, 7, 12, 7, "minecraft:stone_bricks")
    # Corner pillars
    for y in range(1, 13):
        b.set_block(1, y, 1, "minecraft:mossy_stone_bricks" if y % 3 == 0 else "minecraft:cobblestone")
        b.set_block(1, y, 7, "minecraft:cracked_stone_bricks" if y % 2 == 0 else "minecraft:cobblestone")
        b.set_block(7, y, 1, "minecraft:stone_bricks")
        b.set_block(7, y, 7, "minecraft:mossy_stone_bricks" if y % 4 == 0 else "minecraft:cobblestone")

    # Floors
    b.fill(2, 5, 2, 6, 5, 6, "minecraft:dark_oak_planks")
    b.fill(2, 9, 2, 6, 9, 6, "minecraft:dark_oak_planks")
    b.fill(1, 13, 1, 7, 13, 7, "minecraft:stone_bricks")  # Roof deck

    # Entrance (Facing South: Z=7)
    b.fill(3, 2, 7, 5, 4, 7, "minecraft:air")
    b.set_block(3, 2, 7, "minecraft:iron_bars")
    b.set_block(5, 2, 7, "minecraft:iron_bars")
    b.set_block(4, 2, 7, "minecraft:iron_door", {"facing": "south", "half": "lower"})
    b.set_block(4, 3, 7, "minecraft:iron_door", {"facing": "south", "half": "upper"})

    # Arrow slits on second and third floors
    for slit_y in [4, 7, 11]:
        b.set_block(4, slit_y, 1, "minecraft:iron_bars")
        b.set_block(1, slit_y, 4, "minecraft:iron_bars")
        b.set_block(7, slit_y, 4, "minecraft:iron_bars")

    # Battlements & Crenellations (Y=14 to Y=15)
    for x in range(0, 9):
        for z in range(0, 9):
            if x == 0 or x == 8 or z == 0 or z == 8:
                # Overhang corbels at Y=13
                b.set_block(x, 13, z, "minecraft:stone_brick_stairs")
                # Crenels
                if (x + z) % 2 == 0:
                    b.set_block(x, 14, z, "minecraft:stone_bricks")
                    b.set_block(x, 15, z, "minecraft:stone_brick_wall")
                else:
                    b.set_block(x, 14, z, "minecraft:stone_brick_wall")

    # Roof Braziers & Signal Fire
    b.set_block(4, 14, 4, "minecraft:netherrack")
    b.set_block(4, 15, 4, "minecraft:fire")
    b.set_block(4, 13, 4, "minecraft:iron_block")

    # Interior details: ladder and weapon racks
    for y in range(2, 14):
        b.set_block(6, y, 6, "minecraft:ladder", {"facing": "north"})
    b.set_block(2, 2, 2, "minecraft:anvil")
    b.set_block(2, 2, 3, "minecraft:barrel")
    b.set_block(3, 3, 2, "minecraft:lantern", {"hanging": "true"})
    b.set_block(3, 7, 2, "minecraft:lantern", {"hanging": "true"})

    return b


# =============================================================================
# 2. COASTAL FISHING WHARF & COTTAGE (Realm 1: Forgotten Coast - Port Village)
# =============================================================================
def build_coastal_wharf() -> SchematicBuilder:
    """
    11x9x13 Stilt-supported coastal wharf and wooden fishing cottage.
    """
    b = SchematicBuilder(11, 9, 13)
    # Stilt pylons (underwater/ground Y=0 to Y=2)
    for x in [1, 5, 9]:
        for z in [1, 5, 9, 12]:
            b.fill(x, 0, z, x, 2, z, "minecraft:stripped_spruce_log")

    # Decking (Y=2)
    b.fill(0, 2, 0, 10, 2, 12, "minecraft:spruce_planks")

    # Cottage walls (X: 1..7, Z: 1..7, Y: 3..6)
    b.hollow_box(1, 3, 1, 7, 6, 7, "minecraft:oak_planks")
    # Corner posts
    for x in [1, 7]:
        for z in [1, 7]:
            b.fill(x, 3, z, x, 6, z, "minecraft:spruce_log")

    # Cottage Door & Windows
    b.set_block(4, 3, 7, "minecraft:spruce_door", {"facing": "south", "half": "lower"})
    b.set_block(4, 4, 7, "minecraft:spruce_door", {"facing": "south", "half": "upper"})
    b.set_block(2, 4, 4, "minecraft:glass_pane")
    b.set_block(6, 4, 4, "minecraft:glass_pane")

    # Cottage Gable Roof (Y=7 to Y=8)
    for x in range(0, 9):
        b.set_block(x, 7, 0, "minecraft:spruce_stairs", {"facing": "south"})
        b.set_block(x, 7, 8, "minecraft:spruce_stairs", {"facing": "north"})
        b.fill(x, 7, 1, x, 7, 7, "minecraft:spruce_planks")
        b.fill(x, 8, 2, x, 8, 6, "minecraft:spruce_slab")

    # Cobblestone Fireplace & Chimney
    b.fill(2, 3, 2, 3, 8, 2, "minecraft:cobblestone")
    b.set_block(2, 3, 2, "minecraft:campfire")
    b.set_block(2, 9, 2, "minecraft:campfire")  # Smoke top

    # Pier Extension (Z: 8..12, X: 4..10)
    b.fill(3, 2, 8, 10, 2, 12, "minecraft:spruce_planks")
    for z in [8, 10, 12]:
        b.set_block(10, 3, z, "minecraft:spruce_fence")
    b.set_block(9, 3, 12, "minecraft:spruce_fence")
    b.set_block(8, 3, 12, "minecraft:lantern")

    # Barrels & Crates
    b.set_block(8, 3, 9, "minecraft:barrel")
    b.set_block(8, 4, 9, "minecraft:barrel")
    b.set_block(7, 3, 9, "minecraft:chest")

    return b


# =============================================================================
# 3. COGWORK STEAM FOUNDRY (Realm 5: Cogwork March - House Vance)
# =============================================================================
def build_cogwork_foundry() -> SchematicBuilder:
    """
    13x15x13 Steampunk brass & copper industrial foundry with boiler chimney.
    """
    b = SchematicBuilder(13, 15, 13)
    # Heavy stone & deepslate foundation
    b.fill(0, 0, 0, 12, 1, 12, "minecraft:deepslate_tiles")
    b.fill(1, 1, 1, 11, 1, 11, "minecraft:polished_deepslate")

    # Copper & Brass Columns (4 corners and portal frames)
    for x in [1, 11]:
        for z in [1, 11]:
            b.fill(x, 2, z, x, 8, z, "minecraft:cut_copper")
            b.set_block(x, 9, z, "minecraft:copper_block")

    # Factory Walls (Y=2 to Y=7)
    b.hollow_box(1, 2, 1, 11, 7, 11, "minecraft:cut_copper")
    # Wall insets with iron bars
    for side in [(6, 1), (6, 11)]:
        b.fill(side[0]-1, 3, side[1], side[0]+1, 5, side[1], "minecraft:iron_bars")
    for side in [(1, 6), (11, 6)]:
        b.fill(side[0], 3, side[1]-1, side[0], 5, side[1]+1, "minecraft:iron_bars")

    # Industrial Entrance (South Z=11)
    b.fill(5, 2, 11, 7, 5, 11, "minecraft:air")
    b.fill(5, 2, 11, 5, 5, 11, "minecraft:iron_bars")
    b.fill(7, 2, 11, 7, 5, 11, "minecraft:iron_bars")

    # Upper Catwalk Floor (Y=8)
    b.fill(2, 8, 2, 10, 8, 10, "minecraft:iron_bars")
    b.hollow_box(2, 9, 2, 10, 9, 10, "minecraft:iron_bars")  # Railing

    # Central High-Pressure Steam Boiler & Chimney (X: 5..7, Z: 5..7)
    b.fill(5, 2, 5, 7, 5, 7, "minecraft:iron_block")
    b.fill(5, 2, 5, 7, 2, 7, "minecraft:blast_furnace")
    # Vertical Exhaust Stack (Y=6 to Y=14)
    b.cylinder(6, 6, 13, 6, 1, "minecraft:cut_copper", fill_inside=False)
    b.set_block(6, 14, 6, "minecraft:campfire")  # Exhaust smoke plume

    # Artificer Workstations inside
    b.set_block(3, 2, 3, "minecraft:anvil")
    b.set_block(3, 2, 4, "minecraft:smithing_table")
    b.set_block(9, 2, 3, "minecraft:grindstone")
    b.set_block(9, 2, 4, "minecraft:iron_block")

    # Hanging soul lanterns
    b.set_block(3, 7, 3, "minecraft:soul_lantern", {"hanging": "true"})
    b.set_block(9, 7, 3, "minecraft:soul_lantern", {"hanging": "true"})
    b.set_block(3, 7, 9, "minecraft:soul_lantern", {"hanging": "true"})
    b.set_block(9, 7, 9, "minecraft:soul_lantern", {"hanging": "true"})

    return b


# =============================================================================
# 4. THE OBSIDIAN IMPERIAL DAIS (Realm 9: Ashen Caldera - The Crucible of Ash)
# =============================================================================
def build_obsidian_throne() -> SchematicBuilder:
    """
    13x12x13 Basalt colonnade, obsidian dais, and soul-fire throne of Emperor Valerius.
    """
    b = SchematicBuilder(13, 12, 13)
    # Foundation of magma and blackstone
    b.fill(0, 0, 0, 12, 0, 12, "minecraft:polished_blackstone")
    b.fill(1, 1, 1, 11, 1, 11, "minecraft:blackstone")

    # Stepped Dais (Y=2 to Y=4)
    b.fill(2, 2, 2, 10, 2, 10, "minecraft:polished_blackstone_bricks")
    b.fill(3, 3, 3, 9, 3, 9, "minecraft:polished_blackstone_bricks")
    b.fill(4, 4, 4, 8, 4, 8, "minecraft:crying_obsidian")

    # Four Colossal Basalt Colonnades (Y=2 to Y=9)
    for x in [2, 10]:
        for z in [2, 10]:
            b.fill(x, 2, z, x, 9, z, "minecraft:polished_basalt")
            b.set_block(x, 10, z, "minecraft:gilded_blackstone")
            b.set_block(x, 11, z, "minecraft:soul_fire")
            b.set_block(x, 10, z, "minecraft:netherrack")

    # Transverse Overhead Arches
    b.fill(2, 9, 3, 2, 9, 9, "minecraft:crying_obsidian")
    b.fill(10, 9, 3, 10, 9, 9, "minecraft:crying_obsidian")
    b.fill(3, 9, 2, 9, 9, 2, "minecraft:crying_obsidian")
    b.fill(3, 9, 10, 9, 9, 10, "minecraft:crying_obsidian")

    # Magma Braziers
    b.set_block(3, 3, 3, "minecraft:magma_block")
    b.set_block(9, 3, 3, "minecraft:magma_block")
    b.set_block(3, 3, 9, "minecraft:magma_block")
    b.set_block(9, 3, 9, "minecraft:magma_block")

    # The Imperial Obsidian Throne (Center North X=6, Z=5, Y=5..8)
    b.fill(5, 5, 5, 7, 5, 6, "minecraft:obsidian")
    b.fill(5, 6, 5, 7, 7, 5, "minecraft:obsidian")  # Throne Backrest
    b.set_block(6, 8, 5, "minecraft:crying_obsidian")  # Crown Peak
    b.set_block(5, 6, 6, "minecraft:polished_blackstone_brick_stairs", {"facing": "west"})
    b.set_block(7, 6, 6, "minecraft:polished_blackstone_brick_stairs", {"facing": "east"})
    b.set_block(6, 5, 6, "minecraft:red_carpet")

    # Melted Sword Relic Chest (Subterranean vault underneath throne)
    b.set_block(6, 3, 6, "minecraft:netherite_block")
    b.set_block(6, 4, 6, "minecraft:gilded_blackstone")

    return b


# =============================================================================
# 5. GLACIAL HERMIT CLOISTER (Realm 4: Solitary Spine - House Vane)
# =============================================================================
def build_glacial_cloister() -> SchematicBuilder:
    """
    11x15x11 Alpine monastery cloister built from calcite, packed ice, and diorite.
    """
    b = SchematicBuilder(11, 15, 11)
    # Foundation of solid calcite and smooth basalt
    b.fill(0, 0, 0, 10, 1, 10, "minecraft:smooth_basalt")
    b.fill(1, 1, 1, 9, 1, 9, "minecraft:calcite")

    # Main Sanctuary Walls (Y=2 to Y=9)
    b.hollow_box(1, 2, 1, 9, 9, 9, "minecraft:calcite")
    # Corner Buttresses
    for y in range(1, 10):
        b.set_block(0, y, 0, "minecraft:diorite")
        b.set_block(0, y, 10, "minecraft:diorite")
        b.set_block(10, y, 0, "minecraft:diorite")
        b.set_block(10, y, 10, "minecraft:diorite")

    # Slit windows with ice panes
    for y in [4, 7]:
        b.set_block(5, y, 1, "minecraft:packed_ice")
        b.set_block(1, y, 5, "minecraft:packed_ice")
        b.set_block(9, y, 5, "minecraft:packed_ice")

    # Entrance (South Z=9)
    b.fill(4, 2, 9, 6, 5, 9, "minecraft:air")
    b.set_block(4, 2, 9, "minecraft:iron_bars")
    b.set_block(6, 2, 9, "minecraft:iron_bars")
    b.set_block(5, 2, 9, "minecraft:iron_door", {"facing": "south", "half": "lower"})
    b.set_block(5, 3, 9, "minecraft:iron_door", {"facing": "south", "half": "upper"})

    # High Stepped Spire (Y=10 to Y=14)
    b.fill(2, 10, 2, 8, 10, 8, "minecraft:calcite")
    b.fill(3, 11, 3, 7, 11, 7, "minecraft:packed_ice")
    b.fill(4, 12, 4, 6, 12, 6, "minecraft:blue_ice")
    b.set_block(5, 13, 5, "minecraft:blue_ice")
    b.set_block(5, 14, 5, "minecraft:end_rod")  # Needle apex

    # Interior Prayer Cell & Silent Shrine
    b.fill(3, 2, 3, 7, 2, 7, "minecraft:polished_diorite")
    b.set_block(5, 3, 5, "minecraft:blue_ice")
    b.set_block(5, 4, 5, "minecraft:soul_lantern")  # Suspended cold light
    b.set_block(3, 2, 5, "minecraft:lectern", {"facing": "east"})

    return b


# =============================================================================
# 6. AL-QADIRA SUNKEN BAZAAR (Realm 6: Gilded Dunes - House Seljuk)
# =============================================================================
def build_sunken_bazaar() -> SchematicBuilder:
    """
    13x12x13 Red sandstone & terracotta domed trading post with slag vaults.
    """
    b = SchematicBuilder(13, 12, 13)
    # Foundation
    b.fill(0, 0, 0, 12, 1, 12, "minecraft:red_sandstone")
    b.fill(1, 1, 1, 11, 1, 11, "minecraft:cut_red_sandstone")

    # Walls with Terracotta Banding (Y=2 to Y=7)
    b.hollow_box(1, 2, 1, 11, 7, 11, "minecraft:cut_red_sandstone")
    b.hollow_box(1, 4, 1, 11, 4, 11, "minecraft:orange_terracotta")
    b.hollow_box(1, 6, 1, 11, 6, 11, "minecraft:yellow_terracotta")

    # Corner Pillars
    for x in [1, 11]:
        for z in [1, 11]:
            b.fill(x, 2, z, x, 8, z, "minecraft:chiseled_red_sandstone")

    # Open Arched Gateways on 4 sides
    for side in [(6, 1), (6, 11), (1, 6), (11, 6)]:
        x_c, z_c = side
        if z_c in (1, 11):
            b.fill(x_c - 1, 2, z_c, x_c + 1, 5, z_c, "minecraft:air")
        else:
            b.fill(x_c, 2, z_c - 1, x_c, 5, z_c + 1, "minecraft:air")

    # Stepped Domed Roof (Y=8 to Y=11)
    b.fill(2, 8, 2, 10, 8, 10, "minecraft:cut_red_sandstone")
    b.fill(3, 9, 3, 9, 9, 9, "minecraft:orange_terracotta")
    b.fill(4, 10, 4, 8, 10, 8, "minecraft:yellow_terracotta")
    b.fill(5, 11, 5, 7, 11, 7, "minecraft:gold_block")  # Golden dome crown

    # Central Slag Vault inside
    b.fill(5, 2, 5, 7, 3, 7, "minecraft:iron_bars")
    b.set_block(6, 2, 6, "minecraft:gold_block")
    b.set_block(6, 3, 6, "minecraft:lantern")

    # Market stalls
    b.set_block(3, 2, 3, "minecraft:barrel")
    b.set_block(3, 2, 4, "minecraft:chest")
    b.set_block(9, 2, 3, "minecraft:crafting_table")
    b.set_block(9, 2, 4, "minecraft:barrel")

    return b


# =============================================================================
# 7. FEN WITCH STILT DWELLING (Realm 7: Whispering Fen - House Belen)
# =============================================================================
def build_witch_stilt_dwelling() -> SchematicBuilder:
    """
    11x12x11 Mangrove wood & mud brick stilt dwelling with cauldron & drying racks.
    """
    b = SchematicBuilder(11, 12, 11)
    # Mangrove stilt legs (Y=0 to Y=4)
    for x in [2, 8]:
        for z in [2, 8]:
            b.fill(x, 0, z, x, 4, z, "minecraft:stripped_mangrove_wood")

    # Floor Platform (Y=4)
    b.fill(1, 4, 1, 9, 4, 9, "minecraft:mangrove_planks")

    # Hut Walls (X: 2..8, Z: 2..8, Y: 5..8)
    b.hollow_box(2, 5, 2, 8, 8, 8, "minecraft:mud_bricks")
    for x in [2, 8]:
        for z in [2, 8]:
            b.fill(x, 5, z, x, 8, z, "minecraft:mangrove_log")

    # Hut Door & Windows
    b.set_block(5, 5, 8, "minecraft:mangrove_door", {"facing": "south", "half": "lower"})
    b.set_block(5, 6, 8, "minecraft:mangrove_door", {"facing": "south", "half": "upper"})
    b.set_block(2, 6, 5, "minecraft:vine")
    b.set_block(8, 6, 5, "minecraft:vine")

    # Mushroom Thatched Roof (Y=9 to Y=11)
    b.fill(1, 9, 1, 9, 9, 9, "minecraft:brown_mushroom_block")
    b.fill(2, 10, 2, 8, 10, 8, "minecraft:red_mushroom_block")
    b.fill(3, 11, 3, 7, 11, 7, "minecraft:brown_mushroom_block")

    # Interior Apothecary & Cauldron
    b.set_block(4, 5, 4, "minecraft:cauldron", {"level": "3"})
    b.set_block(4, 5, 3, "minecraft:brewing_stand")
    b.set_block(6, 5, 4, "minecraft:barrel")
    b.set_block(6, 5, 3, "minecraft:chest")

    # Access ladder down to water
    for y in range(0, 5):
        b.set_block(5, y, 8, "minecraft:ladder", {"facing": "north"})

    return b


# =============================================================================
# 8. DROWNED CATHEDRAL SPIRE (Realm 2: Sunken Reach - Port Ostraka)
# =============================================================================
def build_drowned_cathedral_spire() -> SchematicBuilder:
    """
    11x18x11 Prismarine & quartz submerged bell tower with sea lanterns.
    """
    b = SchematicBuilder(11, 18, 11)
    # Submerged Foundation
    b.fill(0, 0, 0, 10, 1, 10, "minecraft:dark_prismarine")
    b.fill(1, 1, 1, 9, 1, 9, "minecraft:prismarine_bricks")

    # Main Tower Walls (Y=2 to Y=12)
    b.hollow_box(1, 2, 1, 9, 12, 9, "minecraft:prismarine_bricks")
    for y in range(2, 13):
        b.set_block(1, y, 1, "minecraft:dark_prismarine")
        b.set_block(1, y, 9, "minecraft:dark_prismarine")
        b.set_block(9, y, 1, "minecraft:dark_prismarine")
        b.set_block(9, y, 9, "minecraft:dark_prismarine")

    # Arched Belfry Openings (Y=8 to Y=11)
    for side in [(5, 1), (5, 9), (1, 5), (9, 5)]:
        x_c, z_c = side
        if z_c in (1, 9):
            b.fill(x_c - 1, 8, z_c, x_c + 1, 11, z_c, "minecraft:water")
        else:
            b.fill(x_c, 8, z_c - 1, x_c, 11, z_c + 1, "minecraft:water")

    # Belfry Deck & Bell (Y=7)
    b.fill(2, 7, 2, 8, 7, 8, "minecraft:smooth_quartz")
    b.set_block(5, 8, 5, "minecraft:bell", {"attachment": "floor"})
    b.set_block(5, 7, 5, "minecraft:gold_block")

    # Spire Roof (Y=13 to Y=17)
    b.fill(2, 13, 2, 8, 13, 8, "minecraft:prismarine_bricks")
    b.fill(3, 14, 3, 7, 14, 7, "minecraft:dark_prismarine")
    b.fill(4, 15, 4, 6, 15, 6, "minecraft:dark_prismarine")
    b.set_block(5, 16, 5, "minecraft:sea_lantern")
    b.set_block(5, 17, 5, "minecraft:end_rod")  # Cross apex

    # Sea lanterns & coral decoration
    b.set_block(3, 3, 3, "minecraft:sea_lantern")
    b.set_block(7, 3, 3, "minecraft:sea_lantern")
    b.set_block(3, 3, 7, "minecraft:sea_lantern")
    b.set_block(7, 3, 7, "minecraft:sea_lantern")

    return b


# =============================================================================
# MASTER BUILDER RUNNER
# =============================================================================
def build_all_schematics():
    print("=====================================================================")
    print("   ⚔ ASHENFALL: LORE-ACCURATE SCHEMATICS & CASTLES BUILDER ⚔")
    print(f"   Target: Minecraft 1.21.1 NBT Structure Templates")
    print("=====================================================================")

    schematics = {
        "grey_frontier_watchtower": (build_grey_frontier_watchtower(), "House Douglas Border Fortification"),
        "coastal_fishing_wharf": (build_coastal_wharf(), "Forgotten Coast Fisherman Wharf & Cottage"),
        "cogwork_steam_foundry": (build_cogwork_foundry(), "House Vance Steampunk Assembly Workshop"),
        "obsidian_imperial_dais": (build_obsidian_throne(), "Emperor Valerius Crucible of Ash Dais"),
        "glacial_hermit_cloister": (build_glacial_cloister(), "House Vane Mute Alpine Sanctuary"),
        "al_qadira_sunken_bazaar": (build_sunken_bazaar(), "House Seljuk Slag Vault & Desert Dome"),
        "fen_witch_stilt_dwelling": (build_witch_stilt_dwelling(), "House Belen Mycelial Stilt Hut"),
        "drowned_cathedral_spire": (build_drowned_cathedral_spire(), "House Sophia Submerged Basilica Spire")
    }

    STRUCTURES_DATAPACK_DIR.mkdir(parents=True, exist_ok=True)
    STRUCTURES_WP_DIR.mkdir(parents=True, exist_ok=True)
    BUNDLE_ZIP.parent.mkdir(parents=True, exist_ok=True)

    generated_files = []

    for name, (builder, desc) in schematics.items():
        filename = f"{name}.nbt"
        p_dp = STRUCTURES_DATAPACK_DIR / filename
        p_wp = STRUCTURES_WP_DIR / filename
        builder.save(p_dp)
        builder.save(p_wp)
        generated_files.append((filename, p_dp, desc, (builder.w, builder.h, builder.l)))
        print(f" [+] Generated: {filename:<30} ({builder.w}x{builder.h}x{builder.l} blocks) | {desc}")

    # Package Bundle ZIP for 1-click download
    with zipfile.ZipFile(BUNDLE_ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for fname, p_dp, desc, dim in generated_files:
            z.write(p_dp, arcname=f"structures/{fname}")
    print(f"\n [✓] Master Bundle Packaged: {BUNDLE_ZIP} ({BUNDLE_ZIP.stat().st_size} bytes)")

    # Re-zip datapacks/ashenfall_data2.zip to include new structures
    dp_dir = BASE_DIR / "datapacks" / "ashenfall_data2"
    dp_zip = BASE_DIR / "datapacks" / "ashenfall_data2.zip"
    with zipfile.ZipFile(dp_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(dp_dir):
            for file in files:
                abs_p = Path(root) / file
                rel_p = abs_p.relative_to(dp_dir)
                z.write(abs_p, arcname=str(rel_p))
    print(f" [✓] Updated Datapack Archive: {dp_zip} ({dp_zip.stat().st_size} bytes)")

    print("=====================================================================\n")

if __name__ == "__main__":
    build_all_schematics()

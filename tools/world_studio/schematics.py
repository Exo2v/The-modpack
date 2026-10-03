"""
=============================================================================
ASHENFALL WORLDSTUDIO: Lore-Accurate Schematics Engine
Pure-Python NBT structure loader, voxel geometry compiler, and metadata catalog.
=============================================================================
"""

import gzip
import struct
from pathlib import Path
from typing import Dict, List, Any, Optional

COLOR_PALETTE = {
    "cobblestone": "#7b7b7b",
    "mossy_cobblestone": "#647253",
    "stone_bricks": "#808080",
    "cracked_stone_bricks": "#6e6e6e",
    "mossy_stone_bricks": "#68755c",
    "stone": "#868686",
    "smooth_stone": "#9c9c9c",
    "deepslate": "#3f3f44",
    "deepslate_bricks": "#333338",
    "deepslate_tiles": "#29292d",
    "polished_deepslate": "#434347",
    "blackstone": "#272227",
    "polished_blackstone": "#2c282e",
    "polished_blackstone_bricks": "#231f24",
    "chiseled_polished_blackstone": "#2d282e",
    "gilded_blackstone": "#3d3225",
    "obsidian": "#110c1c",
    "crying_obsidian": "#23123b",
    "spruce_planks": "#674c2e",
    "spruce_log": "#3e2e1c",
    "stripped_spruce_log": "#6c5332",
    "spruce_stairs": "#674c2e",
    "spruce_slab": "#674c2e",
    "spruce_fence": "#674c2e",
    "oak_planks": "#997d4b",
    "oak_log": "#604d2e",
    "stripped_oak_log": "#947b4b",
    "oak_stairs": "#997d4b",
    "oak_slab": "#997d4b",
    "oak_fence": "#997d4b",
    "dark_oak_planks": "#3c2713",
    "dark_oak_log": "#2a1c0d",
    "mangrove_planks": "#6d332d",
    "mangrove_roots": "#4a3222",
    "mangrove_log": "#542e29",
    "mud_bricks": "#81664e",
    "packed_mud": "#87694f",
    "brown_mushroom_block": "#8a6d4e",
    "red_mushroom_block": "#b82a2a",
    "copper_block": "#b3634a",
    "cut_copper": "#aa5e47",
    "cut_copper_stairs": "#aa5e47",
    "cut_copper_slab": "#aa5e47",
    "exposed_cut_copper": "#916957",
    "weathered_cut_copper": "#56846b",
    "copper_grate": "#965541",
    "iron_block": "#d0d0d0",
    "iron_bars": "#909090",
    "heavy_core": "#545b63",
    "anvil": "#444444",
    "smithing_table": "#362a26",
    "blast_furnace": "#4a4a4a",
    "chain": "#333740",
    "calcite": "#d6d2c4",
    "diorite": "#b2b2b2",
    "polished_diorite": "#c4c4c4",
    "smooth_basalt": "#494b50",
    "packed_ice": "#82b0ed",
    "blue_ice": "#6898ed",
    "snow_block": "#eef4f4",
    "glowstone": "#ecab3d",
    "sea_lantern": "#acd0cb",
    "prismarine_bricks": "#54968d",
    "dark_prismarine": "#2c544a",
    "prismarine": "#5c9288",
    "smooth_quartz": "#e8e5dc",
    "bell": "#f4c430",
    "smooth_sandstone": "#d0c393",
    "sandstone": "#cbbb8e",
    "sandstone_stairs": "#d0c393",
    "sandstone_slab": "#d0c393",
    "cut_sandstone": "#c9bc8c",
    "chiseled_sandstone": "#beaf81",
    "red_sandstone": "#b55a1d",
    "cut_red_sandstone": "#a65219",
    "chiseled_red_sandstone": "#9f4c17",
    "terracotta": "#91583e",
    "yellow_terracotta": "#b27c1d",
    "orange_terracotta": "#9b4d1f",
    "red_terracotta": "#873928",
    "red_carpet": "#a62828",
    "white_wool": "#dedede",
    "red_wool": "#992121",
    "yellow_wool": "#e5b324",
    "water": "#2a59a8",
    "magma_block": "#8c3613",
    "lantern": "#d69f33",
    "soul_lantern": "#3eaeb2",
    "soul_fire": "#34c1b9",
    "fire": "#e25c1d",
    "netherrack": "#6d1d1d",
    "netherite_block": "#31292a",
    "end_rod": "#fbf4e2",
    "cauldron": "#434242",
    "barrel": "#7b5b37",
    "crafting_table": "#755332",
    "chest": "#88612f",
    "bookshelf": "#6b4f30",
    "lectern": "#8a6c42",
    "glass": "#b8dfe3",
    "glass_pane": "#b8dfe3",
    "tinted_glass": "#34293c",
    "respawn_anchor": "#3e124f",
    "gold_block": "#eabb2b",
    "amethyst_block": "#7d57ab",
    "ladder": "#84653b",
    "vine": "#335e22",
    "torch": "#e0a538",
    "wall_torch": "#e0a538",
    "campfire": "#e2782b",
    "brewing_stand": "#8a755d",
    "grindstone": "#6b6a69",
    "iron_door": "#cbcbcb",
    "spruce_door": "#674c2e",
    "mangrove_door": "#6d332d",
    "polished_basalt": "#504d53",
    "stone_brick_stairs": "#808080",
    "stone_brick_wall": "#808080",
    "polished_blackstone_brick_stairs": "#231f24",
    "stripped_mangrove_wood": "#66322b"
}

def resolve_block_color(name: str) -> str:
    clean = name.replace("minecraft:", "").lower()
    if clean in COLOR_PALETTE:
        return COLOR_PALETTE[clean]
    for key, color in COLOR_PALETTE.items():
        if key in clean:
            return color
    return "#7a828e"

def humanize_name(name: str) -> str:
    clean = name.replace("minecraft:", "")
    parts = clean.replace("_", " ").split()
    return " ".join(p.capitalize() for p in parts)

def parse_nbt(data: bytes, offset: int = 0) -> Dict[str, Any]:
    def read_string(off: int):
        length, = struct.unpack_from(">H", data, off)
        off += 2
        s = data[off:off+length].decode("utf-8", "replace")
        return s, off + length

    def parse_payload(tag_type: int, off: int):
        if tag_type == 1:
            return data[off], off + 1
        elif tag_type == 2:
            val, = struct.unpack_from(">h", data, off)
            return val, off + 2
        elif tag_type == 3:
            val, = struct.unpack_from(">i", data, off)
            return val, off + 4
        elif tag_type == 4:
            val, = struct.unpack_from(">q", data, off)
            return val, off + 8
        elif tag_type == 5:
            val, = struct.unpack_from(">f", data, off)
            return val, off + 4
        elif tag_type == 6:
            val, = struct.unpack_from(">d", data, off)
            return val, off + 8
        elif tag_type == 7:
            length, = struct.unpack_from(">i", data, off)
            off += 4
            return list(data[off:off+length]), off + length
        elif tag_type == 8:
            return read_string(off)
        elif tag_type == 9:
            elem_type = data[off]
            length, = struct.unpack_from(">i", data, off + 1)
            off += 5
            items = []
            for _ in range(length):
                item, off = parse_payload(elem_type, off)
                items.append(item)
            return items, off
        elif tag_type == 10:
            res = {}
            while off < len(data):
                t_type = data[off]
                off += 1
                if t_type == 0:
                    break
                name, off = read_string(off)
                val, off = parse_payload(t_type, off)
                res[name] = val
            return res, off
        elif tag_type == 11:
            length, = struct.unpack_from(">i", data, off)
            off += 4
            vals = list(struct.unpack_from(f">{length}i", data, off))
            return vals, off + length * 4
        elif tag_type == 12:
            length, = struct.unpack_from(">i", data, off)
            off += 4
            vals = list(struct.unpack_from(f">{length}q", data, off))
            return vals, off + length * 8
        return None, off

    tag_type = data[offset]
    offset += 1
    if tag_type != 10:
        raise ValueError("Root tag is not compound (10)")
    _, offset = read_string(offset)
    res, _ = parse_payload(10, offset)
    return res


SCHEMATIC_METADATA = {
    "grey_frontier_watchtower": {
        "title": "Grey Frontier Watchtower",
        "realm": "The Grey Frontier",
        "faction": "House Douglas Border Guard",
        "icon": "shield",
        "accent_color": "#94a3b8",
        "concept_art": "/art/wide_castle_grey_frontier_complete.png",
        "target_coords": {"x": 120, "y": 72, "z": 2380},
        "biome": "Plains / Windswept Hills / Frontier Passes",
        "lore": (
            "The granite and cracked stone-brick watchtowers of General Douglas's border guard. "
            "Erected during the early stages of the Great Sundering, these monolithic sentry posts "
            "monitored both outer barbarian incursions and internal capital roads. The crenellated battlements "
            "feature machicolations, arrow slits, iron-reinforced portcullis doors, and an elevated eternal "
            "netherrack brazier beacon visible across the southern plains."
        ),
        "architecture": (
            "Triple-tier square bastion (9x17x9). Ground floor contains heavy weapons racks, ammunition chests, "
            "and secure iron gates. Mid-level features archer firing slits and stone-brick buttressing. "
            "Top level provides a covered timber parapet surrounding an open signal flame."
        ),
        "survival_tips": (
            "Provides an ideal high-vantage early-game fortification. The netherrack brazier provides infinite light, "
            "preventing mob spawns on the parapet. Place at elevated ridge saddles to maximize render distance visibility."
        )
    },
    "coastal_fishing_wharf": {
        "title": "Coastal Fishing Wharf & Anchorage",
        "realm": "The Forgotten Coast",
        "faction": "Pebble Bluffs Fisherfolk",
        "icon": "anchor",
        "accent_color": "#38bdf8",
        "concept_art": "/art/wide_town_grey_frontier_harbor.png",
        "target_coords": {"x": -350, "y": 62, "z": 2600},
        "biome": "Warm Ocean / Pebble Bluffs / Shoreline",
        "lore": (
            "The weather-beaten stilt piers of the Forgotten Coast where the Tenth Scion awakens. "
            "A seaside fisherman's cottage with wooden pylons submerged in water, barrel racks, drying fish racks, "
            "a cobblestone fireplace with smoking chimney, and an elevated spruce shingle roof built to weather salt spray."
        ),
        "architecture": (
            "Deep submerged spruce logs anchor the wharf into sea beds (11x9x13). Features an open-air processing dock "
            "with drying frames, barrels for salting fish, an enclosed tackle shanty, and a working stone smokehouse."
        ),
        "survival_tips": (
            "Spawns directly at sea level (Y=62). Place half-submerged in water for maximum atmospheric realism. "
            "Contains multiple storage barrels and a warm hearth for the initial player awakening stage."
        )
    },
    "cogwork_steam_foundry": {
        "title": "Cogwork Steam Foundry",
        "realm": "The Cogwork March",
        "faction": "House Vance Mechanists",
        "icon": "cog",
        "accent_color": "#f97316",
        "concept_art": "/art/wide_town_cogwork_industrial.png",
        "target_coords": {"x": -2100, "y": 95, "z": 40},
        "biome": "Badlands / Canyons / Terraced Quarries",
        "lore": (
            "An automated smelting and clunker assembly bay. Built from cut copper, deepslate tiles, and polished basalt. "
            "Features a towering exhaust chimney venting geothermal steam, twin blast furnaces, heavy anvil workstations, "
            "and grated catwalks where Otto Vance's engineers forged brass automatons and clockwork limbs."
        ),
        "architecture": (
            "Heavy industrial architecture (13x15x13). High-temperature blast core encased in deepslate tiles. "
            "Ventilation chimney with active soul-fire steam smoke, copper ducting, catwalk railings, and iron grating."
        ),
        "survival_tips": (
            "Complete with dual blast furnaces, anvil, and smithing station. Position on the 9-meter terraced steps "
            "of the Cogwork canyon rim to simulate geothermal tapping."
        )
    },
    "obsidian_imperial_dais": {
        "title": "Obsidian Imperial Dais",
        "realm": "The Ashen Caldera",
        "faction": "The Cinder Conclave & Valerius IX",
        "icon": "flame",
        "accent_color": "#ef4444",
        "concept_art": "/art/wide_castle_ashen_imperium_complete.png",
        "target_coords": {"x": 0, "y": 146, "z": 0},
        "biome": "Basalt Deltas / Magma Rim / Nether Wastes",
        "lore": (
            "The seat of Emperor Valerius IX in the center of the collapsed volcanic crater. "
            "Colonnades of polished basalt and crying obsidian framing an elevated sacrificial dais with magma braziers, "
            "blackstone steps, and the throne of melted blades where the Ninth Sound was struck that fractured the continent."
        ),
        "architecture": (
            "Sacrificial amphitheater (13x12x13). Stepped blackstone pyramid ringed by crying obsidian pillars that pulse with "
            "amethyst light. Central dais houses molten magma channels, soul fire fonts, and gilded blackstone pediments."
        ),
        "survival_tips": (
            "Dangerous terrain fixture. Crying obsidian and magma blocks generate hazardous heat. "
            "Ideal for boss arena focal points or custom ritual summoning structures in the dead center of the continent."
        )
    },
    "glacial_hermit_cloister": {
        "title": "Glacial Hermit Cloister",
        "realm": "The Solitary Glacial Spine",
        "faction": "House Vane & The Silent Order",
        "icon": "snowflake",
        "accent_color": "#67e8f9",
        "concept_art": "/art/wide_castle_glacial_citadel_complete.png",
        "target_coords": {"x": 15, "y": 265, "z": -2480},
        "biome": "Frozen Peaks / Jagged Arêtes / Jagged Spires",
        "lore": (
            "The high-altitude stone cells of the mute monks. Built from packed ice, blue ice, calcite, and smooth basalt, "
            "perched precariously on narrow alpine ridges. Contains the cell where initiates took the vow of total silence, "
            "a central ice-encased relic shrine, wind-deflecting buttresses, and an ice needle spire."
        ),
        "architecture": (
            "Wind-sculpted spire (11x15x11). Engineered to endure 100-knot blizzards. Outer walls of reinforced calcite "
            "and blue ice. Features an insulated prayer alcove with soul lanterns, lectern scripture, and high glazed observation ports."
        ),
        "survival_tips": (
            "Spawns at extreme summit altitudes (Y >= 200). Blue ice will not melt under soul lantern light. "
            "Excellent mountain retreat, glider launching platform, or silent observation shrine."
        )
    },
    "al_qadira_sunken_bazaar": {
        "title": "Al-Qadira Sunken Bazaar",
        "realm": "The Gilded Dunes",
        "faction": "House Seljuk & Desert Caravans",
        "icon": "gem",
        "accent_color": "#eab308",
        "concept_art": "/art/wide_city_al_qadira_oasis.png",
        "target_coords": {"x": 2310, "y": 84, "z": -20},
        "biome": "Desert / Eroded Badlands / Red Sand Canyons",
        "lore": (
            "A half-buried desert trading post and netherite slag vault jutting from the black glass sands. "
            "Domed sandstone roof, terracotta decorative banding, gold filigree accents, iron bar treasury cages, "
            "and cooling water fountain alcoves insulated against the blistering daytime desert heat."
        ),
        "architecture": (
            "Subterranean hypostyle hall (13x12x13). Sunken courtyard with central marble fountain, cut sandstone colonnades, "
            "shaded trading alcoves with dyed wool awnings, and an armored gold-reinforced lockbox chamber."
        ),
        "survival_tips": (
            "Offers full shelter against desert heat and hostile night mobs. Central water spring provides infinite water source. "
            "Place submerged by 3-4 blocks into sand drifts to create a realistic excavated archaeological appearance."
        )
    },
    "fen_witch_stilt_dwelling": {
        "title": "Fen Witch Stilt Dwelling",
        "realm": "The Whispering Fen",
        "faction": "The Mycelial Covenant & House Belen",
        "icon": "skull",
        "accent_color": "#a855f7",
        "concept_art": "/art/wide_town_whispering_fen_stilt.png",
        "target_coords": {"x": 1980, "y": 63, "z": 2020},
        "biome": "Swamp / Mangrove Bayous / Murky Deltas",
        "lore": (
            "The swamp dwellings of the Mycelial Covenant, raised six blocks above stagnant water on petrified mangrove stilts. "
            "Features thatched red mushroom roofs, bubbling alchemy cauldrons, mushroom compost beds, hanging botanical vines, "
            "and an access ladder to keep swamp ghouls at bay."
        ),
        "architecture": (
            "Elevated mangrove hut (11x12x11). Deep mangrove root pilings cross-braced over murky water. "
            "Living mushroom canopy roof, outdoor alchemy potion balcony, mud-brick hearth, and drying herb racks."
        ),
        "survival_tips": (
            "Built specifically for water or bog placement. The high stilt floor prevents zombies and spiders from entering. "
            "Equipped with brewing stand, cauldron, and compost shelves for apothecary and potion crafting."
        )
    },
    "drowned_cathedral_spire": {
        "title": "Drowned Cathedral Spire",
        "realm": "The Sunken Reach",
        "faction": "Cataclysm Ruins & Port Ostraka",
        "icon": "landmark",
        "accent_color": "#2dd4bf",
        "concept_art": "/art/wide_ruins_sunken_atlantis_complete.png",
        "target_coords": {"x": -2380, "y": 38, "z": 1590},
        "biome": "Warm Ocean / Coral Reef Atoll / Seabed Trench",
        "lore": (
            "The submerged upper bell tower of the Grand Basilica of Port Ostraka projecting from shallow coastal waters. "
            "Weathered prismarine arches, waterlogged quartz belfry, the holy bronze bell, glowing sea lanterns, "
            "and hanging kelp tendrils swaying in the ocean currents."
        ),
        "architecture": (
            "Sunken gothic campanile (11x18x11). Prismarine brick buttressing supporting an open belfry. "
            "Houses the consecrated golden bell, sea lantern navigational beacons, and dark prismarine ribbed vaulting."
        ),
        "survival_tips": (
            "Spawns partially or completely submerged in water. Sea lanterns provide underwater illumination and air pockets "
            "near the ceiling arches. Ideal dive-site landmark and aquatic navigation beacon."
        )
    }
}


class SchematicsEngine:
    """Manages parsing, caching, and serving Minecraft NBT structures."""

    def __init__(self, structures_dir: Path):
        self.structures_dir = structures_dir
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._summary_cache: Optional[List[Dict[str, Any]]] = None

    def get_all_summaries(self) -> List[Dict[str, Any]]:
        if self._summary_cache is not None:
            return self._summary_cache

        summaries = []
        for file_path in sorted(self.structures_dir.glob("*.nbt")):
            s_id = file_path.stem
            detail = self.get_schematic(s_id)
            if not detail:
                continue
            meta = detail["metadata"]
            summaries.append({
                "id": s_id,
                "title": meta.get("title", humanize_name(s_id)),
                "realm": meta.get("realm", "Vantyra"),
                "faction": meta.get("faction", "Unknown"),
                "icon": meta.get("icon", "box"),
                "accent_color": meta.get("accent_color", "#38bdf8"),
                "concept_art": meta.get("concept_art", None),
                "target_coords": meta.get("target_coords", {"x": 0, "y": 64, "z": 0}),
                "biome": meta.get("biome", "Plains"),
                "size": detail["size"],
                "total_blocks": detail["total_blocks"],
                "palette_count": len(detail["palette"]),
                "file_size": file_path.stat().st_size,
                "tp_command": f"/tp @s {meta['target_coords']['x']} {meta['target_coords']['y']} {meta['target_coords']['z']}",
                "load_command": f"/structure load ashenfall:{s_id} ~ ~ ~",
                "download_url": f"/downloads/schematics/{s_id}.nbt"
            })

        self._summary_cache = summaries
        return summaries

    def get_schematic(self, schematic_id: str) -> Optional[Dict[str, Any]]:
        if schematic_id in self._cache:
            return self._cache[schematic_id]

        file_path = self.structures_dir / f"{schematic_id}.nbt"
        if not file_path.exists():
            return None

        with gzip.open(file_path, "rb") as f:
            raw_data = f.read()

        nbt = parse_nbt(raw_data)
        raw_palette = nbt.get("palette", [])
        raw_blocks = nbt.get("blocks", [])
        size = nbt.get("size", [0, 0, 0])

        counts = {}
        layer_counts = {}
        processed_blocks = []

        for b in raw_blocks:
            st = int(b.get("state", 0))
            pos = b.get("pos", [0, 0, 0])
            x, y, z = int(pos[0]), int(pos[1]), int(pos[2])
            counts[st] = counts.get(st, 0) + 1
            layer_counts[y] = layer_counts.get(y, 0) + 1
            processed_blocks.append([x, y, z, st])

        total_blocks = len(processed_blocks)

        palette = []
        for idx, item in enumerate(raw_palette):
            name = item.get("Name", "minecraft:air")
            c = counts.get(idx, 0)
            pct = round((c / total_blocks) * 100, 1) if total_blocks > 0 else 0.0
            palette.append({
                "index": idx,
                "name": name,
                "display_name": humanize_name(name),
                "count": c,
                "percent": pct,
                "color": resolve_block_color(name)
            })

        # Sort palette by count descending for cleaner presentation
        meta = SCHEMATIC_METADATA.get(schematic_id, {
            "title": humanize_name(schematic_id),
            "realm": "Ashenfall",
            "faction": "Lore Builders",
            "icon": "box",
            "accent_color": "#38bdf8",
            "target_coords": {"x": 0, "y": 64, "z": 0},
            "biome": "Plains",
            "lore": "Canonical structure of Vantyra.",
            "architecture": "Voxel masonry.",
            "survival_tips": "Spawns with standard orientation."
        })

        result = {
            "id": schematic_id,
            "size": size,
            "total_blocks": total_blocks,
            "palette": palette,
            "blocks": processed_blocks,
            "layer_stats": {str(k): v for k, v in sorted(layer_counts.items())},
            "metadata": meta,
            "in_game": {
                "tp": f"/tp @s {meta['target_coords']['x']} {meta['target_coords']['y']} {meta['target_coords']['z']}",
                "load": f"/structure load ashenfall:{schematic_id} ~ ~ ~"
            },
            "download_url": f"/downloads/schematics/{schematic_id}.nbt"
        }

        self._cache[schematic_id] = result
        return result

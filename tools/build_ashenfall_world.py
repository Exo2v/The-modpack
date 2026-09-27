#!/usr/bin/env python3
"""
Ashenfall Handcrafted World Generator (The Elden Ring Method).
Builds saves/Ashenfall with level.dat, icon.png, and core continental MCA regions.
"""

import os
import sys
import time
import struct
import zlib
import io
import numpy as np
from PIL import Image
import nbtlib
from nbtlib import File, Compound, List, String, Int, Byte, Long, Double, LongArray

# Import the organic elevation and biome generator
import sys
sys.path.insert(0, '/home/user/The-modpack/tools')
sys.path.insert(0, '/home/user/The-modpack')

from generate_continent_map import get_natural_continent

BIOME_MAP = {
    0: 'minecraft:deep_ocean',
    1: 'minecraft:basalt_deltas',
    2: 'minecraft:frozen_peaks',
    3: 'minecraft:windswept_hills',
    4: 'minecraft:desert',
    5: 'minecraft:swamp',
    6: 'minecraft:ocean',
    7: 'minecraft:plains'
}

SURFACE_BLOCKS = {
    0: ('minecraft:gravel', 'minecraft:sand'),
    1: ('minecraft:blackstone', 'minecraft:basalt'),
    2: ('minecraft:snow_block', 'minecraft:packed_ice'),
    3: ('minecraft:stone', 'minecraft:cobblestone'),
    4: ('minecraft:sand', 'minecraft:sandstone'),
    5: ('minecraft:mud', 'minecraft:coarse_dirt'),
    6: ('minecraft:sand', 'minecraft:gravel'),
    7: ('minecraft:grass_block', 'minecraft:dirt')
}

def pack_section(block_indices, b=4):
    entries_per_long = 64 // b
    num_longs = (4096 + entries_per_long - 1) // entries_per_long
    longs = []
    for i in range(num_longs):
        val = 0
        for j in range(entries_per_long):
            idx = i * entries_per_long + j
            if idx < 4096:
                val |= (block_indices[idx] & ((1 << b) - 1)) << (j * b)
        if val >= (1 << 63):
            val -= (1 << 64)
        longs.append(val)
    return longs

def create_level_dat(save_dir):
    data = Compound({
        'DataVersion': Int(3955),
        'LevelName': String('Ashenfall - The Broken Realm'),
        'generatorName': String('default'),
        'generatorVersion': Int(1),
        'SpawnX': Int(0),
        'SpawnY': Int(68),
        'SpawnZ': Int(2500),
        'version': Int(19133),
        'initialized': Byte(1),
        'allowCommands': Byte(1),
        'GameType': Int(0), # Survival
        'Difficulty': Byte(2), # Normal
        'DifficultyLocked': Byte(0),
        'BorderCenterX': Double(0.0),
        'BorderCenterZ': Double(0.0),
        'BorderSize': Double(8000.0),
        'BorderSafeZone': Double(10.0),
        'BorderDamagePerBlock': Double(2.0),
        'BorderWarningDistance': Double(60.0),
        'BorderWarningTime': Double(10.0),
        'DayTime': Long(1000),
        'Time': Long(1000),
        'clearWeatherTime': Int(60000),
        'rainTime': Int(0),
        'raining': Byte(0),
        'thunderTime': Int(0),
        'thundering': Byte(0),
        'GameRules': Compound({
            'keepInventory': String('false'),
            'doDaylightCycle': String('true'),
            'doMobSpawning': String('true'),
            'mobGriefing': String('true'),
            'doWeatherCycle': String('true')
        })
    })
    
    root = File({'Data': data}, gzipped=True)
    out_path = os.path.join(save_dir, 'level.dat')
    root.save(out_path)
    print(f"Created {out_path} (DataVersion: 3955, Spawn: 0, 68, 2500, Border: 8000)")

def create_icon_png(save_dir):
    map_path = "/home/user/The-modpack/ASHENFALL_CONTINENT_MAP.png"
    if os.path.exists(map_path):
        img = Image.open(map_path)
        icon = img.resize((128, 128), Image.Resampling.LANCZOS)
        out_path = os.path.join(save_dir, "icon.png")
        icon.save(out_path)
        print(f"Created world icon {out_path} (128x128)")

def generate_region_file(rx, rz, region_dir):
    t0 = time.time()
    bx = rx * 512
    bz = rz * 512
    xs = np.arange(bx, bx + 512)
    zs = np.arange(bz, bz + 512)
    X, Z = np.meshgrid(xs, zs)
    
    elev, biomes, water = get_natural_continent(X, Z)
    elev_int = np.clip(np.round(elev), -60, 310).astype(np.int32)
    
    locations = bytearray(4096)
    timestamps = bytearray(4096)
    sectors = bytearray()
    current_sector = 2
    now = int(time.time())
    
    for cz in range(32):
        for cx in range(32):
            chunk_x = rx * 32 + cx
            chunk_z = rz * 32 + cz
            
            c_elev = elev_int[cz*16 : (cz+1)*16, cx*16 : (cx+1)*16]
            c_bio = biomes[cz*16 : (cz+1)*16, cx*16 : (cx+1)*16]
            
            min_h = int(c_elev.min())
            max_h = int(c_elev.max())
            rep_bio = int(np.bincount(c_bio.flatten()).argmax())
            bio_str = BIOME_MAP.get(rep_bio, 'minecraft:plains')
            surf_top, surf_sub = SURFACE_BLOCKS.get(rep_bio, ('minecraft:grass_block', 'minecraft:dirt'))
            
            sections = []
            for sy in range(-4, 20):
                sec_base_y = sy * 16
                sec_top_y = sec_base_y + 15
                
                if sec_top_y < min_h:
                    if sy < 0:
                        blk = 'minecraft:deepslate'
                    elif sy == -4:
                        blk = 'minecraft:bedrock'
                    else:
                        blk = 'minecraft:stone'
                    sections.append(Compound({
                        'Y': Byte(sy),
                        'block_states': Compound({
                            'palette': List[Compound]([Compound({'Name': String(blk)})])
                        }),
                        'biomes': Compound({
                            'palette': List[String]([String(bio_str)])
                        })
                    }))
                elif sec_base_y > max_h:
                    if sec_top_y <= 62:
                        blk = 'minecraft:water'
                    else:
                        blk = 'minecraft:air'
                    sections.append(Compound({
                        'Y': Byte(sy),
                        'block_states': Compound({
                            'palette': List[Compound]([Compound({'Name': String(blk)})])
                        }),
                        'biomes': Compound({
                            'palette': List[String]([String(bio_str)])
                        })
                    }))
                else:
                    palette_names = ['minecraft:air', 'minecraft:stone', surf_sub, surf_top, 'minecraft:water']
                    palette_comp = List[Compound]([Compound({'Name': String(n)}) for n in palette_names])
                    
                    indices = [0] * 4096
                    for ly in range(16):
                        wy = sec_base_y + ly
                        for lz in range(16):
                            for lx in range(16):
                                h = c_elev[lz, lx]
                                if wy < -60:
                                    b_idx = 1
                                elif wy < h - 3:
                                    b_idx = 1
                                elif wy < h:
                                    b_idx = 2
                                elif wy == h:
                                    b_idx = 3
                                elif wy <= 62:
                                    b_idx = 4
                                else:
                                    b_idx = 0
                                indices[(ly * 16 + lz) * 16 + lx] = b_idx
                                
                    packed_data = pack_section(indices, b=4)
                    sections.append(Compound({
                        'Y': Byte(sy),
                        'block_states': Compound({
                            'palette': palette_comp,
                            'data': LongArray(packed_data)
                        }),
                        'biomes': Compound({
                            'palette': List[String]([String(bio_str)])
                        })
                    }))
                    
            chunk_nbt = File({
                'DataVersion': Int(3955),
                'xPos': Int(chunk_x),
                'yPos': Int(-4),
                'zPos': Int(chunk_z),
                'Status': String('minecraft:full'),
                'sections': List[Compound](sections)
            })
            
            buf = io.BytesIO()
            chunk_nbt.write(buf)
            compressed = zlib.compress(buf.getvalue(), level=1)
            
            payload = struct.pack('>IB', len(compressed) + 1, 2) + compressed
            pad_len = (4096 - (len(payload) % 4096)) % 4096
            sector_data = payload + (b'\x00' * pad_len)
            sector_count = len(sector_data) // 4096
            
            loc_idx = (cx + cz * 32) * 4
            struct.pack_into('>I', locations, loc_idx, (current_sector << 8) | sector_count)
            struct.pack_into('>I', timestamps, loc_idx, now)
            
            sectors.extend(sector_data)
            current_sector += sector_count
            
    mca_bytes = bytes(locations) + bytes(timestamps) + bytes(sectors)
    out_path = os.path.join(region_dir, f"r.{rx}.{rz}.mca")
    with open(out_path, "wb") as f:
        f.write(mca_bytes)
        
    elapsed = time.time() - t0
    print(f"  [✓] r.{rx}.{rz}.mca ({len(mca_bytes)/1024:.1f} KB, 1024 chunks in {elapsed:.2f}s)")

def build_world():
    save_dir = "/home/user/The-modpack/saves/Ashenfall"
    region_dir = os.path.join(save_dir, "region")
    os.makedirs(region_dir, exist_ok=True)
    
    print("=" * 60)
    print("ASHENFALL: Building Handcrafted Elden Ring Continent Save")
    print("=" * 60)
    
    # 1. Level.dat & Icon
    create_level_dat(save_dir)
    create_icon_png(save_dir)
    
    # 2. Key Continental Regions to Pre-Generate
    # These cover all 9 national landmarks and the spawn
    regions_to_generate = [
        # Spawn & Forgotten Coast
        (0, 4),   # Spawn at (0, 2500)
        (-1, 4),  # Coast West
        (0, 5),   # Coast South (ocean overlook)
        
        # The Ashen Caldera (Center)
        (0, 0),   # Center East
        (-1, 0),  # Center West
        (0, -1),  # Center North-East
        (-1, -1), # Center North-West
        
        # The Solitary Glacial Spine (North Alpine)
        (0, -3),  # Glacial Ridge East
        (-1, -3), # Glacial Ridge West
        (0, -4),  # High Glacial Summit
        
        # The Cogwork March (West Canyons & Terraces)
        (-2, 0),  # Industrial Gorge East
        (-3, 0),  # Industrial Gorge West
        (-3, 1),  # Canal Junction
        
        # The Gilded Dunes (East Desert & Mesas)
        (2, 0),   # Dunes West
        (3, 0),   # Dunes East
        (2, 1),   # Sandstone Mesas
        
        # The Whispering Fen (South-East Swamp)
        (2, 2),   # Fen Heartwood
        (3, 2),   # Deep Bayou
        
        # The Sunken Reach (South-West Lagoons)
        (-2, 2),  # Drowned Shore
        (-3, 2)   # Flooded Archipelago
    ]
    
    print(f"\nPre-generating {len(regions_to_generate)} key continental regions (20,480 chunks)...")
    t_start = time.time()
    
    for rx, rz in regions_to_generate:
        generate_region_file(rx, rz, region_dir)
        
    total_elapsed = time.time() - t_start
    print(f"\nAll {len(regions_to_generate)} regions generated successfully in {total_elapsed:.1f}s!")
    print(f"World save ready at: {save_dir}")
    print("=" * 60)

if __name__ == "__main__":
    build_world()

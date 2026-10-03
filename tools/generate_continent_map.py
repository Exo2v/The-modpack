#!/usr/bin/env python3
"""
Organic Elden-Ring Style Continent Generator for Ashenfall (Vantyra).
Generates organic, fractal terrain with natural coastlines, mountain spurs, and rivers.
"""

import numpy as np
from PIL import Image

def fractal_noise(x, z, octaves=5, lacunarity=2.0, gain=0.5, scale=400.0, seed=1337):
    rng = np.random.default_rng(seed)
    total = np.zeros_like(x, dtype=np.float32)
    freq = 1.0 / scale
    amp = 1.0
    
    for o in range(octaves):
        # 2D sinusoidal pseudo-random lattice
        ox = rng.uniform(0, 1000)
        oz = rng.uniform(0, 1000)
        nx = np.sin((x + ox) * freq) * np.cos((z + oz) * freq)
        nx += np.sin((x + z + ox) * freq * 0.7) * 0.5
        total += nx * amp
        freq *= lacunarity
        amp *= gain
        
    return total

def get_natural_continent(x, z):
    # Domain warping for natural fractal shapes
    warp_x = fractal_noise(x, z, octaves=3, scale=800.0, seed=101) * 350.0
    warp_z = fractal_noise(z, x, octaves=3, scale=800.0, seed=202) * 350.0
    
    wx = x + warp_x
    wz = z + warp_z
    
    dist = np.sqrt(wx**2 + wz**2)
    raw_dist = np.sqrt(x**2 + z**2)
    angle = np.arctan2(wz, wx) # -pi to pi
    
    # 1. Continental Boundary & The Veil of Salt
    # Radius fluctuates naturally between 3200 and 3600
    coast_radius = 3400.0 + fractal_noise(x, z, octaves=4, scale=600.0, seed=303) * 300.0
    
    # Continental mask (1 on land, 0 in deep ocean)
    t_coast = (coast_radius - raw_dist) / 300.0
    continental_factor = np.clip(t_coast, 0.0, 1.0)
    # Smooth step
    continental_factor = continental_factor * continental_factor * (3 - 2 * continental_factor)
    
    # Base terrain height
    elevation = np.full_like(x, 30.0, dtype=np.float32) # Ocean floor
    
    # Rolling land height
    macro_hills = fractal_noise(x, z, octaves=4, scale=300.0, seed=404) * 12.0
    land_base = 65.0 + macro_hills
    
    # 2. Regional Influences (Smooth Angle & Distance Weighting)
    # North: angle ~ -pi/2 (-1.57) -> Glacial Spine
    # West: angle ~ pi or -pi -> Cogwork March
    # East: angle ~ 0 -> Gilded Dunes
    # South-East: angle ~ pi/4 (0.78) -> Whispering Fen
    # South-West: angle ~ 3pi/4 (2.35) -> Sunken Reach
    # South: angle ~ pi/2 (1.57) -> Forgotten Coast (Spawn)
    
    w_north = np.clip(np.cos(angle + np.pi/2), 0.0, 1.0) ** 1.5 * np.clip((raw_dist - 500) / 1000.0, 0.0, 1.0)
    w_east  = np.clip(np.cos(angle), 0.0, 1.0) ** 1.5 * np.clip((raw_dist - 500) / 1000.0, 0.0, 1.0)
    w_west  = np.clip(-np.cos(angle), 0.0, 1.0) ** 1.5 * np.clip((raw_dist - 500) / 1000.0, 0.0, 1.0)
    w_south = np.clip(np.sin(angle), 0.0, 1.0) ** 1.5 * np.clip((raw_dist - 500) / 1000.0, 0.0, 1.0)
    
    # Refine South quadrants
    w_fen = w_south * np.clip(wx / 1000.0, 0.0, 1.0)
    w_sunken = w_south * np.clip(-wx / 1000.0, 0.0, 1.0)
    w_coast = w_south * np.clip(1.0 - (np.abs(wx) / 1200.0), 0.0, 1.0)
    
    # 3. Features:
    # A. The Caldera (Center, raw_dist < 700)
    caldera_rim_dist = np.abs(raw_dist - 420.0)
    caldera_rim = np.exp(-(caldera_rim_dist ** 2) / (2 * (80.0 ** 2))) * 75.0
    caldera_floor = np.where(raw_dist < 340.0, -22.0 * (1.0 - raw_dist / 340.0), 0.0)
    
    # B. Solitary Glacial Spine Mountains (North)
    mountain_ridges = np.abs(fractal_noise(wx * 2, wz, octaves=4, scale=250.0, seed=505)) * 95.0
    spine_height = (mountain_ridges + 45.0) * w_north
    
    # C. Cogwork March (West Canyons & Terraces)
    cog_terraces = (np.floor((land_base + 10.0) / 14.0) * 14.0 - land_base) * w_west
    # Winding Grand River flowing from Caldera to West Ocean
    river_path = np.sin(wx * 0.003) * 350.0 + (fractal_noise(x, z, octaves=2, scale=400.0, seed=606) * 150.0)
    river_dist = np.abs(wz - river_path)
    river_canyon = np.where((river_dist < 180.0) & (wx < 200), -20.0 * (1.0 - river_dist / 180.0) * w_west, 0.0)
    
    # D. Gilded Dunes (East Wind Ripples & Mesas)
    dune_ripples = (np.sin(wx * 0.012 + np.cos(wz * 0.004) * 4.0) * 12.0 + 8.0) * w_east
    
    # E. Whispering Fen (Low waterlogged delta)
    fen_depress = -8.0 * w_fen
    
    # F. Sunken Reach (Flooded coastal archipelago)
    sunken_depress = -14.0 * w_sunken
    
    # Combine Land Elevation
    total_land_elev = land_base + caldera_rim + caldera_floor + spine_height + cog_terraces + river_canyon + dune_ripples + fen_depress + sunken_depress
    
    # Apply Continental Shelf Falloff
    elevation = 32.0 + (total_land_elev - 32.0) * continental_factor
    
    # 4. Biome Determination
    # 0: Deep Ocean
    # 1: Caldera (Basalt / Obsidian)
    # 2: Glacial Spine (Snow / Ice)
    # 3: Cogwork March (Terraces / Canyons)
    # 4: Gilded Dunes (Desert / Badlands)
    # 5: Whispering Fen (Swamp / Bayou)
    # 6: Sunken Reach (Drowned Lagoon)
    # 7: Forgotten Coast (Plains / Bluffs)
    biome_id = np.zeros_like(x, dtype=np.int32)
    
    # Assign on land
    on_land = continental_factor > 0.3
    
    # Scores for each biome
    scores = np.stack([
        np.zeros_like(raw_dist),                       # 0: Ocean
        np.exp(-((raw_dist / 480.0)**4)) * 3.0,         # 1: Caldera
        w_north * 2.2,                                 # 2: Glacial
        w_west * 1.8,                                  # 3: Cogwork
        w_east * 1.8,                                  # 4: Dunes
        w_fen * 1.9,                                   # 5: Fen
        w_sunken * 1.9,                                # 6: Sunken
        w_coast * 1.7                                  # 7: Coast
    ], axis=0)
    
    chosen_biome = np.argmax(scores, axis=0)
    biome_id = np.where(on_land, chosen_biome, 0)
    
    # Water mask: where elevation < 62 and not in the heart of caldera
    water_mask = (elevation < 62.0) & ~((raw_dist < 400.0) & (elevation > 45.0))
    
    return elevation, biome_id, water_mask

def render_organic_map():
    width = 1200
    height = 1200
    xs = np.linspace(-4000, 4000, width, dtype=np.float32)
    zs = np.linspace(-4000, 4000, height, dtype=np.float32)
    X, Z = np.meshgrid(xs, zs)
    
    elevation, biomes, water_mask = get_natural_continent(X, Z)
    
    img = np.zeros((height, width, 3), dtype=np.uint8)
    elev_norm = np.clip((elevation - 30.0) / 190.0, 0.0, 1.0)
    
    ocean_deep = np.array([12, 24, 48], dtype=np.float32)
    ocean_shallow = np.array([28, 75, 115], dtype=np.float32)
    
    for y in range(height):
        for x in range(width):
            b = biomes[y, x]
            el = elevation[y, x]
            is_water = water_mask[y, x]
            
            if is_water:
                depth = np.clip((62.0 - el) / 32.0, 0.0, 1.0)
                col = (1.0 - depth) * ocean_shallow + depth * ocean_deep
            elif b == 1: # Caldera
                if el < 48:
                    col = np.array([210, 60, 15], dtype=np.float32) # Lava
                elif el > 105:
                    col = np.array([38, 35, 40], dtype=np.float32) # Obsidian ring
                else:
                    col = np.array([68, 62, 65], dtype=np.float32) # Basalt floor
            elif b == 2: # Glacial Spine
                if el > 130:
                    col = np.array([245, 250, 255], dtype=np.float32) # Snow peaks
                elif el > 95:
                    col = np.array([180, 210, 235], dtype=np.float32) # Glacial ice
                else:
                    col = np.array([120, 150, 175], dtype=np.float32) # Mountain stone
            elif b == 3: # Cogwork
                if el > 85:
                    col = np.array([145, 120, 85], dtype=np.float32) # Plateau
                else:
                    col = np.array([115, 95, 70], dtype=np.float32) # Gorge rock
            elif b == 4: # Gilded Dunes
                if el > 90:
                    col = np.array([195, 115, 65], dtype=np.float32) # Badlands mesa
                else:
                    col = np.array([225, 185, 100], dtype=np.float32) # Sand dunes
            elif b == 5: # Fen
                col = np.array([55, 75, 48], dtype=np.float32) # Dark bayou
            elif b == 6: # Sunken Reach
                col = np.array([75, 145, 135], dtype=np.float32) # Drowned shelf
            elif b == 7: # Forgotten Coast
                if el < 66:
                    col = np.array([190, 180, 145], dtype=np.float32) # Beach sand
                else:
                    col = np.array([90, 140, 70], dtype=np.float32) # Green hills
            else:
                col = np.array([80, 125, 65], dtype=np.float32)
                
            # Hillshade lighting (diffuse sunlight from North-West)
            shade = 0.8 + (elev_norm[y, x] * 0.35)
            final_col = np.clip(col * shade, 0, 255).astype(np.uint8)
            img[y, x] = final_col
            
    # Mark spawn point at X: 0, Z: 2500 -> pixel in 1200x1200
    spawn_px = int((0 + 4000) / 8000 * width)
    spawn_pz = int((2500 + 4000) / 8000 * height)
    # Bright red dot on spawn
    for dx in range(-4, 5):
        for dz in range(-4, 5):
            if dx*dx + dz*dz <= 16:
                img[spawn_pz + dz, spawn_px + dx] = [255, 30, 30]
                
    # Mark Caldera center at (0, 0)
    c_px = int(width / 2)
    c_pz = int(height / 2)
    for dx in range(-4, 5):
        for dz in range(-4, 5):
            if dx*dx + dz*dz <= 16:
                img[c_pz + dz, c_px + dx] = [255, 215, 0]

    out_file = "/home/user/The-modpack/ASHENFALL_CONTINENT_MAP.png"
    Image.fromarray(img).save(out_file)
    print(f"Organic continent rendered to {out_file} (1200x1200).")

if __name__ == "__main__":
    render_organic_map()

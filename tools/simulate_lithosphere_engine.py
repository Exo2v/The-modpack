#!/usr/bin/env python3
"""
Refined Lithosphere + Still Life + Ashenfall Worldgen Simulator.
Eliminates any modular artifacts and generates a 100% natural, seamless, painterly continent.
"""

import numpy as np
from PIL import Image

def smooth_spline(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)

def fractal_noise_2d(x, z, octaves=4, scale=600.0, seed=777):
    rng = np.random.default_rng(seed)
    total = np.zeros_like(x, dtype=np.float32)
    freq = 1.0 / scale
    amp = 1.0
    for _ in range(octaves):
        ox = rng.uniform(0, 5000)
        oz = rng.uniform(0, 5000)
        n = np.sin((x + ox) * freq) * np.cos((z + oz) * freq)
        n += np.cos((x - z + ox) * freq * 0.7) * 0.5
        total += n * amp
        freq *= 2.0
        amp *= 0.5
    return total

def get_refined_lithosphere_terrain(x, z):
    # Domain warping for natural fractal landforms
    wx = x + fractal_noise_2d(x, z, octaves=3, scale=800.0, seed=123) * 250.0
    wz = z + fractal_noise_2d(z, x, octaves=3, scale=800.0, seed=456) * 250.0
    
    raw_dist = np.sqrt(x**2 + z**2)
    warp_dist = np.sqrt(wx**2 + wz**2)
    angle = np.arctan2(wz, wx) # -pi to pi
    
    # 1. Continental Boundary & The Veil of Salt
    coast_radius = 3450.0 + fractal_noise_2d(x, z, octaves=3, scale=500.0, seed=999) * 250.0
    coast_shelf = smooth_spline((coast_radius - raw_dist) / 350.0) # 1 on land, 0 in ocean
    
    # 2. Lithosphere Smooth Spline Land Elevation
    broad_swell = fractal_noise_2d(wx, wz, octaves=4, scale=400.0, seed=111) * 14.0
    rolling_base = 66.0 + broad_swell
    
    # Regional directional weights (Smooth polar blending)
    # North (Glacial): angle ~ -pi/2
    w_north = np.clip(np.sin(-angle), 0.0, 1.0) ** 1.4 * np.clip((raw_dist - 400.0) / 900.0, 0.0, 1.0)
    # West (Cogwork): angle ~ pi or -pi (negative x)
    w_west  = np.clip(-np.cos(angle), 0.0, 1.0) ** 1.4 * np.clip((raw_dist - 400.0) / 900.0, 0.0, 1.0)
    # East (Dunes): angle ~ 0 (positive x)
    w_east  = np.clip(np.cos(angle), 0.0, 1.0) ** 1.4 * np.clip((raw_dist - 400.0) / 900.0, 0.0, 1.0)
    # South (Coast, Fen, Sunken): angle ~ pi/2 (positive z)
    w_south = np.clip(np.sin(angle), 0.0, 1.0) ** 1.4 * np.clip((raw_dist - 400.0) / 900.0, 0.0, 1.0)
    
    # South sub-regions
    w_fen = w_south * smooth_spline(wx / 1100.0) # South-East
    w_sunken = w_south * smooth_spline(-wx / 1100.0) # South-West
    w_coast = w_south * np.clip(1.0 - (np.abs(wx) / 1000.0), 0.0, 1.0) # South Center
    
    # 3. Terrain Features
    # A. Ashen Caldera (Center)
    caldera_mask = raw_dist <= 620.0
    caldera_rim_t = np.exp(-((raw_dist - 420.0)**2) / (2 * (80.0**2)))
    caldera_rim = caldera_rim_t * 80.0 # Peak Y=146
    caldera_sink = np.where(raw_dist < 340.0, -26.0 * (1.0 - raw_dist / 340.0), 0.0)
    caldera_elev = 66.0 + caldera_rim + caldera_sink
    
    # B. Solitary Glacial Spine (North Alpine Ridge)
    mountain_ridges = np.abs(fractal_noise_2d(wx * 1.5, wz, octaves=4, scale=300.0, seed=222)) * 105.0
    spine_elev = 68.0 + (mountain_ridges + 35.0) * w_north
    
    # C. Cogwork March (West Terraced Plateaus & Canyons)
    river_path = np.sin(wx * 0.0025) * 300.0 + fractal_noise_2d(x, z, octaves=2, scale=400.0, seed=333) * 120.0
    river_dist = np.abs(wz - river_path)
    u_canyon = smooth_spline(river_dist / 150.0) # U-shaped carved valley
    cogwork_elev = 52.0 + (rolling_base + 12.0 - 52.0) * u_canyon
    
    # D. Gilded Dunes (East Sand Waves)
    dune_waves = (np.sin(wx * 0.009 + np.cos(wz * 0.003) * 3.0) * 12.0 + 8.0) * w_east
    dunes_elev = 72.0 + dune_waves
    
    # E. Whispering Fen (South-East Organic Bayou)
    fen_noise = fractal_noise_2d(wx, wz, octaves=3, scale=300.0, seed=444) * 4.0
    fen_elev = 62.0 + fen_noise
    
    # F. Sunken Reach (South-West Drowned Shelf)
    sunken_noise = fractal_noise_2d(wx, wz, octaves=3, scale=350.0, seed=555) * 5.0
    sunken_elev = 56.5 + sunken_noise
    
    # G. Forgotten Coast (South Plains - Spawn)
    coast_elev = 68.0 + broad_swell * 0.6
    
    # Combine Land Elevation
    land_height = rolling_base
    land_height = np.where(w_north > 0.1, np.maximum(land_height, spine_elev), land_height)
    land_height = np.where(w_west > 0.2, (1.0 - w_west) * land_height + w_west * cogwork_elev, land_height)
    land_height = np.where(w_east > 0.2, (1.0 - w_east) * land_height + w_east * dunes_elev, land_height)
    land_height = np.where(w_fen > 0.2, (1.0 - w_fen) * land_height + w_fen * fen_elev, land_height)
    land_height = np.where(w_sunken > 0.2, (1.0 - w_sunken) * land_height + w_sunken * sunken_elev, land_height)
    land_height = np.where(w_coast > 0.2, (1.0 - w_coast) * land_height + w_coast * coast_elev, land_height)
    land_height = np.where(caldera_mask, caldera_elev, land_height)
    
    # Continental Shelf Falloff
    elevation = 32.0 + (land_height - 32.0) * coast_shelf
    
    # 4. Biomes
    scores = np.stack([
        np.zeros_like(raw_dist),          # 0: Deep Ocean
        np.where(caldera_mask, 6.0, 0.0), # 1: Caldera
        w_north * 2.6,                    # 2: Glacial Spine
        w_west * 2.2,                     # 3: Cogwork
        w_east * 2.2,                     # 4: Dunes
        w_fen * 2.3,                      # 5: Fen
        w_sunken * 2.3,                   # 6: Sunken
        w_coast * 2.2                     # 7: Coast
    ], axis=0)
    
    on_land = coast_shelf > 0.25
    chosen = np.argmax(scores, axis=0)
    biomes = np.where(on_land, chosen, 0)
    
    water_mask = (elevation < 62.0) & ~((caldera_mask) & (elevation > 45.0))
    return elevation, biomes, water_mask

def render():
    width = 1200
    height = 1200
    xs = np.linspace(-4000, 4000, width, dtype=np.float32)
    zs = np.linspace(-4000, 4000, height, dtype=np.float32)
    X, Z = np.meshgrid(xs, zs)
    
    elevation, biomes, water_mask = get_refined_lithosphere_terrain(X, Z)
    
    img = np.zeros((height, width, 3), dtype=np.uint8)
    elev_norm = np.clip((elevation - 30.0) / 190.0, 0.0, 1.0)
    
    ocean_abyssal = np.array([14, 26, 48], dtype=np.float32)
    ocean_coastal = np.array([36, 82, 118], dtype=np.float32)
    
    for y in range(height):
        for x in range(width):
            b = biomes[y, x]
            el = elevation[y, x]
            is_water = water_mask[y, x]
            
            if is_water:
                depth = np.clip((62.0 - el) / 30.0, 0.0, 1.0)
                col = (1.0 - depth) * ocean_coastal + depth * ocean_abyssal
            elif b == 1: # Caldera
                if el < 45: col = np.array([215, 65, 20], dtype=np.float32) # Magma
                elif el > 115: col = np.array([42, 40, 45], dtype=np.float32) # Obsidian ring
                else: col = np.array([72, 68, 70], dtype=np.float32) # Basalt
            elif b == 2: # Glacial Spine
                if el > 135: col = np.array([242, 246, 252], dtype=np.float32) # Snow
                elif el > 100: col = np.array([175, 205, 230], dtype=np.float32) # Ice
                else: col = np.array([115, 135, 150], dtype=np.float32) # Slate rock
            elif b == 3: # Cogwork March
                if el > 85: col = np.array([140, 125, 95], dtype=np.float32) # Terraces
                else: col = np.array([110, 120, 85], dtype=np.float32) # Canyon
            elif b == 4: # Gilded Dunes
                if el > 85: col = np.array([190, 120, 75], dtype=np.float32) # Mesas
                else: col = np.array([218, 182, 115], dtype=np.float32) # Sand
            elif b == 5: # Whispering Fen (Still Life Mangrove)
                col = np.array([58, 74, 52], dtype=np.float32) # Swamp
            elif b == 6: # Sunken Reach
                col = np.array([75, 140, 140], dtype=np.float32) # Reefs
            elif b == 7: # Forgotten Coast
                if el < 66: col = np.array([185, 175, 145], dtype=np.float32) # Beach
                else: col = np.array([95, 135, 78], dtype=np.float32) # Meadow
            else:
                col = np.array([85, 125, 70], dtype=np.float32)
                
            shade = 0.82 + (elev_norm[y, x] * 0.32)
            img[y, x] = np.clip(col * shade, 0, 255).astype(np.uint8)
            
    # Mark spawn point at X: 0, Z: 2500 (Red Dot)
    spawn_px = int((0 + 4000) / 8000 * width)
    spawn_pz = int((2500 + 4000) / 8000 * height)
    for dx in range(-4, 5):
        for dz in range(-4, 5):
            if dx*dx + dz*dz <= 16:
                img[spawn_pz + dz, spawn_px + dx] = [255, 30, 30]
                
    # Mark Caldera center at (0, 0) (Gold Ring)
    c_px = int(width / 2)
    c_pz = int(height / 2)
    for dx in range(-4, 5):
        for dz in range(-4, 5):
            if dx*dx + dz*dz <= 16:
                img[c_pz + dz, c_px + dx] = [255, 215, 0]

    out_file = "/home/user/The-modpack/ASHENFALL_LITHOSPHERE_MAP.png"
    Image.fromarray(img).save(out_file)
    print(f"Generated {out_file} successfully.")

if __name__ == "__main__":
    render()

#!/usr/bin/env python3
"""
=============================================================================
ASHENFALL: Master High-Resolution Geological Heightmap Synthesizer (v2.0)
=============================================================================
Generates a breathtaking, geologically authentic 16-bit grayscale heightmap
(4096 x 4096) and visual assets for WorldPainter & Minecraft 1.21.1:

  1. ASHENFALL_HEIGHTMAP_16BIT.png  (16-bit uint16 master for WorldPainter)
  2. ASHENFALL_HEIGHTMAP_PREVIEW.png (8-bit grayscale for image viewers)
  3. ASHENFALL_TOPOGRAPHIC_RENDER.png (Full-color 3D hillshaded satellite atlas)
  4. WORLDPAINTER_IMPORT_GUIDE.md   (Exact step-by-step import parameters)
=============================================================================
"""

import os
import sys
import math
import time
import shutil
import gc
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
BUILDS_MAP1_DIR = BASE_DIR / "builds" / "map1"
BUILDS_MAP1_DIR.mkdir(parents=True, exist_ok=True)

# Map Configuration
RES = 4096           # 4096 x 4096 grid
EXTENT = 4000.0      # -4000 to +4000 blocks in Minecraft coordinates
PIXEL_SIZE = (2.0 * EXTENT) / RES  # ~1.953 blocks per pixel

# Minecraft 1.21.1 Elevation Bounds (-64 to +320)
MIN_Y = -64.0
MAX_Y = 320.0
TOTAL_HEIGHT = MAX_Y - MIN_Y  # 384 blocks
SEA_LEVEL = 62.0

print("=" * 72)
print("   ⚔ ASHENFALL — Synthesizing Master Geological Heightmap (4096x4096) ⚔")
print("=" * 72)
start_time = time.time()

# ---------------------------------------------------------------------------
# 1. Procedural Noise & Geological Math Utilities (Memory-Optimized float32)
# ---------------------------------------------------------------------------
print(" [1/5] Initializing coordinate grid (-4000 to +4000 blocks)...")
xs = np.linspace(-EXTENT, EXTENT, RES, dtype=np.float32)
zs = np.linspace(-EXTENT, EXTENT, RES, dtype=np.float32)
X, Z = np.meshgrid(xs, zs)
del xs, zs
gc.collect()

def fbm(x, y, octaves=5, lacunarity=2.02, gain=0.5, freq=0.001, seed=0):
    """Memory-efficient vectorized harmonic fractal noise."""
    val = np.zeros_like(x, dtype=np.float32)
    amp = 1.0
    f = freq
    for i in range(octaves):
        ang = float(i) * 0.785398 + seed
        ca = math.cos(ang)
        sa = math.sin(ang)
        rx = (ca * x - sa * y) * f
        ry = (sa * x + ca * y) * f
        val += (np.sin(rx + np.cos(ry * 1.3)) * np.cos(ry - np.sin(rx * 1.1))) * amp
        f *= lacunarity
        amp *= gain
    return val

def ridged_fbm(x, y, octaves=5, lacunarity=2.05, gain=0.52, freq=0.0012, seed=0):
    """Vectorized sharp ridge noise for alpine crests, arêtes and crags."""
    val = np.zeros_like(x, dtype=np.float32)
    amp = 1.0
    f = freq
    weight = 1.0
    for i in range(octaves):
        ang = float(i) * 0.628318 + seed
        ca = math.cos(ang)
        sa = math.sin(ang)
        rx = (ca * x - sa * y) * f
        ry = (sa * x + ca * y) * f
        sig = 1.0 - np.abs(np.sin(rx + np.cos(ry * 1.25)) * np.cos(ry - np.sin(rx * 1.05)))
        sig = sig * sig * weight
        val += sig * amp
        weight = np.clip(sig * 1.8, 0.15, 1.0)
        f *= lacunarity
        amp *= gain
    return val

# ---------------------------------------------------------------------------
# 2. Macro Geology & Continental Landmass Sculpting
# ---------------------------------------------------------------------------
print(" [2/5] Sculpting tectonic landmass, domain warping & continental shelf...")

# Domain Warping for organic, sweeping plate tectonics
warp_x = fbm(X, Z, octaves=3, freq=0.0006, seed=11) * 380.0
warp_z = fbm(X + 800.0, Z - 800.0, octaves=3, freq=0.0006, seed=29) * 380.0
X_w = X + warp_x
Z_w = Z + warp_z
del warp_x, warp_z
gc.collect()

# Distance from continent center (warped)
R_w = np.sqrt(X_w**2 + Z_w**2)
R_raw = np.sqrt(X**2 + Z**2)

# Coastline falloff: The Veil of Salt (Outer Ocean)
# Main continent radius ~3200-3600 blocks with jagged coastal capes and fjords
coast_noise = fbm(X_w, Z_w, octaves=4, freq=0.0015, seed=107) * 420.0
coast_dist = R_w + coast_noise

# Continental Shelf mask: 1.0 = inner land, 0.0 = deep ocean
land_mask = np.clip((3550.0 - coast_dist) / 600.0, 0.0, 1.0)
land_factor = 0.5 - 0.5 * np.cos(land_mask * math.pi) # Hermite S-curve
del coast_dist
gc.collect()

# Base Ocean Trench (Y=24 to Y=48) & Lowland Plains (Y=66 to Y=74)
elevation = 28.0 + land_factor * 42.0

# Rolling lowland topography & hills
lowland_hills = fbm(X_w, Z_w, octaves=5, freq=0.0009, seed=223) * 16.0
elevation += lowland_hills * land_factor
del lowland_hills
gc.collect()

# ---------------------------------------------------------------------------
# 3. Iconic Macro Geological Features
# ---------------------------------------------------------------------------
print(" [3/5] Sculpting The Glacial Spine, Ashen Caldera, Cogwork March & Dunes...")

# --- A. THE SOLITARY GLACIAL SPINE (NORTH: Z ~ -2500, X ~ -2800 to +2800) ---
dist_spine_z = np.abs(Z_w - (-2500.0))
dist_spine_x = np.abs(X_w)
spine_envelope = np.exp(-(dist_spine_z / 650.0)**2) * np.exp(-(dist_spine_x / 2200.0)**2) * land_factor
del dist_spine_z, dist_spine_x
gc.collect()

spine_peaks = ridged_fbm(X_w, Z_w, octaves=6, freq=0.0014, seed=901)
# Tallest summits reach up to Y=235 (imposing alpine cordillera)
elevation += spine_peaks * (spine_envelope * 145.0)
del spine_peaks, spine_envelope
gc.collect()

# Glacial cirques & hanging valleys in northern mountains
cirques = np.clip(np.sin(X_w * 0.0035) * np.cos(Z_w * 0.0035), 0.0, 1.0)
cirque_mask = np.clip((-1600.0 - Z_w) / 400.0, 0.0, 1.0) * np.clip((elevation - 120.0) / 40.0, 0.0, 1.0)
elevation -= cirques * 22.0 * cirque_mask
del cirques, cirque_mask
gc.collect()

# --- B. THE ASHEN CALDERA (CENTER: X=0, Z=0) ---
# Massive collapsed supervolcano caldera
dist_caldera = R_raw # Use unwarped center for true central focal point
caldera_rim_radius = 560.0
caldera_rim_sigma = 160.0
rim_gaussian = np.exp(-((dist_caldera - caldera_rim_radius) / caldera_rim_sigma)**2)

# Radial volcanic fluting / lava runnels
angle = np.arctan2(Z, X)
fluting = np.sin(angle * 14.0 + fbm(X, Z, octaves=3, freq=0.003, seed=55) * 3.0)
volcanic_crags = ridged_fbm(X, Z, octaves=5, freq=0.003, seed=333) * 55.0
elevation += (30.0 + volcanic_crags + fluting * 12.0) * rim_gaussian

# Breach Canyon (Southwest breach at angle ~ -2.35 rad where ancient lava flowed into sea)
breach_angle_diff = np.abs(angle - (-2.35))
breach_radial = np.exp(-((dist_caldera - 520.0) / 220.0)**2)
breach_mask = np.exp(-(breach_angle_diff / 0.28)**2) * breach_radial
elevation -= breach_mask * 45.0

# Inner crater floor subsidence (drop to sunken volcanic lake / caldera basin at Y=42)
crater_drop = np.clip((caldera_rim_radius - dist_caldera) / 220.0, 0.0, 1.0)
crater_drop = 0.5 - 0.5 * np.cos(crater_drop * math.pi)
elevation = elevation * (1.0 - crater_drop) + (40.0 + fbm(X, Z, octaves=4, freq=0.004, seed=444) * 5.0) * crater_drop

# Central Resurgent Dome: The Molten Obsidian Spire (center R < 140)
central_plug = np.exp(-(dist_caldera / 120.0)**2)
elevation += central_plug * 52.0  # Rises back to Y=92
del rim_gaussian, volcanic_crags, fluting, crater_drop, central_plug, angle, breach_radial, breach_mask
gc.collect()

# --- C. THE COGWORK MARCH & BRASS GORGES (WEST: X ~ -2100, Z ~ 0) ---
dist_cog = np.sqrt((X_w - (-2100.0))**2 + (Z_w - 0.0)**2)
cog_envelope = np.exp(-(dist_cog / 1050.0)**2) * land_factor
del dist_cog
gc.collect()

# Stepped geological terraces (sedimentary strata / industrial quarry benches)
cog_undulation = fbm(X_w, Z_w, octaves=4, freq=0.0018, seed=611) * 32.0
terrace_base = elevation + cog_undulation
terrace_step = 9.0  # 9-block quarry / mesa steps
terraced_surface = np.round(terrace_base / terrace_step) * terrace_step
# Soften step edges slightly
terraced_smooth = terraced_surface + np.sin((terrace_base / terrace_step) * 2.0 * math.pi) * 0.9
elevation = elevation * (1.0 - cog_envelope) + terraced_smooth * cog_envelope
del cog_envelope, cog_undulation, terrace_base, terraced_surface, terraced_smooth
gc.collect()

# Carved River Canyons in Cogwork March
canyon_path1 = np.abs(X_w - (-1800.0 + np.sin(Z_w * 0.0018) * 350.0 + fbm(X_w, Z_w, octaves=3, freq=0.002, seed=71) * 120.0))
canyon_carve1 = np.clip((140.0 - canyon_path1) / 140.0, 0.0, 1.0)
canyon_env = np.clip((-1000.0 - X_w) / 300.0, 0.0, 1.0) * np.clip((1800.0 - np.abs(Z_w)) / 300.0, 0.0, 1.0)
elevation -= canyon_carve1 * 34.0 * canyon_env
del canyon_path1, canyon_carve1, canyon_env
gc.collect()

# --- D. THE GILDED DUNES (EAST: X ~ +2300, Z ~ 0) ---
dist_dunes = np.sqrt((X_w - 2300.0)**2 + (Z_w - 0.0)**2)
dune_envelope = np.exp(-(dist_dunes / 1150.0)**2) * land_factor
del dist_dunes
gc.collect()

# Wind-swept transverse barchan dunes (wave orientation ~ 45 degrees)
dune_coord = (X_w * 0.707 + Z_w * 0.707) * 0.012
# Smooth asymmetric dune profile without invalid negative roots
dune_wave = np.sin(dune_coord + fbm(X_w, Z_w, octaves=3, freq=0.002, seed=88) * 1.5)
dune_profile = np.sign(dune_wave) * (np.abs(dune_wave) ** 0.85)
elevation += (dune_profile * 22.0 + 14.0) * dune_envelope

# Desert Mesas / Buttes within Gilded Dunes
mesa_noise = ridged_fbm(X_w, Z_w, octaves=4, freq=0.0016, seed=512)
mesa_mask = (mesa_noise > 0.65) * dune_envelope
elevation += mesa_mask * 48.0
del dune_envelope, dune_coord, dune_wave, dune_profile, mesa_noise, mesa_mask
gc.collect()

# --- E. THE WHISPERING FEN (SOUTHEAST: X ~ +2000, Z ~ +2000) ---
dist_fen = np.sqrt((X_w - 2000.0)**2 + (Z_w - 2000.0)**2)
fen_envelope = np.exp(-(dist_fen / 950.0)**2) * land_factor
# Depress terrain down to water level (Y=62 to 64) with sunken braided bayous
elevation = elevation * (1.0 - fen_envelope) + (63.0 + fbm(X_w, Z_w, octaves=4, freq=0.003, seed=707) * 3.5) * fen_envelope
del dist_fen, fen_envelope
gc.collect()

# --- F. THE SUNKEN REACH & ATOLL BAY (SOUTHWEST: X ~ -2400, Z ~ +1600) ---
dist_reach = np.sqrt((X_w - (-2400.0))**2 + (Z_w - 1600.0)**2)
reach_envelope = np.exp(-(dist_reach / 850.0)**2) * land_factor
# Drown land into shallow bay and barrier islands
elevation = elevation * (1.0 - reach_envelope) + (54.0 + fbm(X_w, Z_w, octaves=5, freq=0.0025, seed=404) * 14.0) * reach_envelope
del dist_reach, reach_envelope
gc.collect()

# --- G. DENDRITIC CONTINENTAL RIVER ARTERIES ---
# Northern melt river flowing from mountains to sea
river_melt_x = np.abs(X_w - (np.sin(Z_w * 0.0012) * 550.0 + fbm(X_w, Z_w, octaves=3, freq=0.0015, seed=17) * 180.0))
river_melt_mask = np.clip((110.0 - river_melt_x) / 110.0, 0.0, 1.0)
river_z_env = np.clip((Z_w - (-2400.0)) / 300.0, 0.0, 1.0) * np.clip((1400.0 - Z_w) / 300.0, 0.0, 1.0)
elevation -= river_melt_mask * 18.0 * river_z_env * (elevation > 63.0)
del river_melt_x, river_melt_mask, river_z_env
gc.collect()

# Clamp final elevations strictly within valid Minecraft limits
elevation = np.clip(elevation, -64.0, 318.0)
min_elev = float(np.min(elevation))
max_elev = float(np.max(elevation))
print(f" -> Geological Elevation Range: Min Y={min_elev:.1f}, Max Y={max_elev:.1f}")
print(f" -> Sea Level: Y={SEA_LEVEL:.1f} (Waterline threshold)")

# ---------------------------------------------------------------------------
# 4. Export 16-Bit uint16 Heightmap for WorldPainter
# ---------------------------------------------------------------------------
print("\n [4/5] Exporting 16-bit uint16 heightmap for WorldPainter...")
# Linear transform: Y=-64..320 -> 0..65535 uint16
norm_16 = (elevation - MIN_Y) / TOTAL_HEIGHT
uint16_data = np.clip(norm_16 * 65535.0, 0.0, 65535.0).astype(np.uint16)
del norm_16
gc.collect()

heightmap_16_path = BASE_DIR / "ASHENFALL_HEIGHTMAP_16BIT.png"
img_16 = Image.fromarray(uint16_data)
img_16.save(heightmap_16_path)
print(f" [✓] Created 16-bit Heightmap: {heightmap_16_path} ({heightmap_16_path.stat().st_size:,} bytes)")
shutil.copy2(heightmap_16_path, BUILDS_MAP1_DIR / "ASHENFALL_HEIGHTMAP_16BIT.png")

# Export 8-bit preview heightmap
print(" [✓] Exporting 8-bit preview heightmap...")
uint8_data = (uint16_data >> 8).astype(np.uint8)
heightmap_8_path = BASE_DIR / "ASHENFALL_HEIGHTMAP_PREVIEW.png"
img_8 = Image.fromarray(uint8_data, mode="L")
img_8.save(heightmap_8_path)
print(f" [✓] Created 8-bit Preview: {heightmap_8_path}")
shutil.copy2(heightmap_8_path, BUILDS_MAP1_DIR / "ASHENFALL_HEIGHTMAP_PREVIEW.png")

del uint16_data, uint8_data
gc.collect()

# ---------------------------------------------------------------------------
# 5. Export Full-Color 3D Hillshaded Satellite Topographic Map
# ---------------------------------------------------------------------------
print("\n [5/5] Rendering 3D hillshaded full-color satellite topographic atlas...")

# Downsample by 2 for ultra-fast, memory-efficient hillshading (2048 x 2048)
sub = 2
elev_sub = elevation[::sub, ::sub]
x_sub = X[::sub, ::sub]
z_sub = Z[::sub, ::sub]
r_sub = np.sqrt(x_sub**2 + z_sub**2)
h_sub, w_sub = elev_sub.shape
del elevation, X, Z, X_w, Z_w, R_w, R_raw, land_factor, land_mask
gc.collect()

# Compute gradients for 3D hillshade
dy, dx = np.gradient(elev_sub, PIXEL_SIZE * sub, PIXEL_SIZE * sub)
slope = math.pi / 2.0 - np.arctan(np.sqrt(dx**2 + dy**2))
aspect = np.arctan2(-dy, -dx)
del dy, dx
gc.collect()

# Northwest lighting (Azimuth 315 deg, Altitude 45 deg)
azimuth = 315.0 * math.pi / 180.0
altitude = 45.0 * math.pi / 180.0
shaded = np.sin(altitude) * np.sin(slope) + np.cos(altitude) * np.cos(slope) * np.cos(azimuth - aspect)
shaded = np.clip(shaded, 0.0, 1.0)
del slope, aspect
gc.collect()

# Continuous Natural Hypsometric Color Ramp
rgb = np.zeros((h_sub, w_sub, 3), dtype=np.uint8)

# Deep Trench (Y < 48)
m_deep = elev_sub < 48.0
rgb[m_deep] = [16, 34, 68]

# Coastal Shelf & Water (48 <= Y < 62)
m_shallow = (elev_sub >= 48.0) & (elev_sub < 62.0)
t_w = np.clip((elev_sub - 48.0) / 14.0, 0.0, 1.0)
rgb[m_shallow, 0] = (22.0 + t_w[m_shallow] * 24.0).astype(np.uint8)
rgb[m_shallow, 1] = (52.0 + t_w[m_shallow] * 68.0).astype(np.uint8)
rgb[m_shallow, 2] = (108.0 + t_w[m_shallow] * 62.0).astype(np.uint8)

# Shore / Beach (62 <= Y < 66)
m_beach = (elev_sub >= 62.0) & (elev_sub < 66.0)
rgb[m_beach] = [218, 206, 154]

# Lowlands & Rolling Plains (66 <= Y < 95)
m_low = (elev_sub >= 66.0) & (elev_sub < 95.0)
t_low = np.clip((elev_sub - 66.0) / 29.0, 0.0, 1.0)
rgb[m_low, 0] = (68.0 + t_low[m_low] * 28.0).astype(np.uint8)
rgb[m_low, 1] = (126.0 - t_low[m_low] * 12.0).astype(np.uint8)
rgb[m_low, 2] = (54.0 - t_low[m_low] * 10.0).astype(np.uint8)

# Highlands & Foothills (95 <= Y < 140)
m_high = (elev_sub >= 95.0) & (elev_sub < 140.0)
t_high = np.clip((elev_sub - 95.0) / 45.0, 0.0, 1.0)
rgb[m_high, 0] = (108.0 + t_high[m_high] * 24.0).astype(np.uint8)
rgb[m_high, 1] = (120.0 - t_high[m_high] * 18.0).astype(np.uint8)
rgb[m_high, 2] = (62.0 + t_high[m_high] * 18.0).astype(np.uint8)

# Alpine Rocky Slopes & Scree (140 <= Y < 180)
m_rock = (elev_sub >= 140.0) & (elev_sub < 180.0)
rgb[m_rock] = [124, 122, 126]

# High Alpine Glacial Summits & Snow (Y >= 180)
m_snow = elev_sub >= 180.0
rgb[m_snow] = [242, 246, 252]

# --- Smooth Organic Regional Overlays (No Hard Square Boxes!) ---
# 1. Gilded Dunes (East): Amber, Ochre & Terracotta Mesas
dist_dunes_center = np.sqrt((x_sub - 2300.0)**2 + z_sub**2)
dunes_weight = np.clip((1400.0 - dist_dunes_center) / 600.0, 0.0, 1.0) * (elev_sub >= 62.0)
if np.any(dunes_weight > 0):
    dune_col = np.array([222, 162, 82], dtype=np.float32)
    mesa_col = np.array([178, 88, 52], dtype=np.float32)
    # Blend mesa color at higher elevation
    elev_t = np.clip((elev_sub - 90.0) / 40.0, 0.0, 1.0)[:, :, np.newaxis]
    target_dune_col = dune_col * (1.0 - elev_t) + mesa_col * elev_t
    w = (dunes_weight[:, :, np.newaxis] * 0.82)
    rgb[:] = (rgb.astype(np.float32) * (1.0 - w) + target_dune_col * w).astype(np.uint8)

# 2. Cogwork March (West): Steely Bronzed Quarry Terraces
dist_cog_center = np.sqrt((x_sub - (-2100.0))**2 + z_sub**2)
cog_weight = np.clip((1350.0 - dist_cog_center) / 600.0, 0.0, 1.0) * (elev_sub >= 62.0)
if np.any(cog_weight > 0):
    cog_col = np.array([138, 122, 94], dtype=np.float32)
    w = (cog_weight[:, :, np.newaxis] * 0.78)
    rgb[:] = (rgb.astype(np.float32) * (1.0 - w) + cog_col * w).astype(np.uint8)

# 3. Ashen Caldera (Center): Scorched Basalt, Blackstone & Crater Floor
caldera_rim_weight = np.exp(-((r_sub - 560.0) / 180.0)**2)
if np.any(caldera_rim_weight > 0.05):
    basalt_col = np.array([44, 42, 46], dtype=np.float32)
    w = (caldera_rim_weight[:, :, np.newaxis] * 0.88)
    rgb[:] = (rgb.astype(np.float32) * (1.0 - w) + basalt_col * w).astype(np.uint8)

# Inner Sunken Crater Floor
m_inner_crater = (r_sub < 420.0) & (elev_sub < 50.0)
rgb[m_inner_crater] = [24, 22, 26]

# Central Molten Obsidian Throne Spire
m_spire = (r_sub < 110.0) & (elev_sub >= 50.0)
rgb[m_spire] = [58, 48, 56]

# Apply 3D Hillshade Lighting
rgb_shaded = (rgb.astype(np.float32) * (shaded[:, :, np.newaxis] * 0.72 + 0.28)).clip(0, 255).astype(np.uint8)

topo_img = Image.fromarray(rgb_shaded, mode="RGB")
draw = ImageDraw.Draw(topo_img)

def to_pixel(x, z):
    px = int((x + EXTENT) / (2.0 * EXTENT) * (w_sub - 1))
    pz = int((z + EXTENT) / (2.0 * EXTENT) * (h_sub - 1))
    return px, pz

landmarks = [
    ("SPAWN: The Forgotten Coast (0, 2500)", (0, 2500), (255, 70, 70), (0, 30)),
    ("The Solitary Glacial Spine (0, -2500)", (0, -2500), (120, 220, 255), (0, -35)),
    ("The Cogwork March (-2100, 0)", (-2100, 0), (255, 205, 60), (-320, 0)),
    ("The Ashen Caldera (0, 0)", (0, 0), (255, 120, 120), (30, -30)),
    ("The Gilded Dunes (+2300, 0)", (2300, 0), (255, 215, 100), (30, 0)),
    ("The Whispering Fen (+2000, +2000)", (2000, 2000), (90, 230, 140), (30, 20)),
    ("The Sunken Reach (-2400, +1600)", (-2400, 1600), (80, 190, 255), (-310, 20)),
    ("The Veil of Salt (Outer Ocean)", (0, -3700), (150, 190, 255), (0, -25))
]

for text, (lx, lz), col, (ox, oy) in landmarks:
    px, pz = to_pixel(lx, lz)
    r_pt = 8
    draw.ellipse([px - r_pt, pz - r_pt, px + r_pt, pz + r_pt], fill=col, outline=(0, 0, 0), width=2)
    # Background badge
    tx = px + ox
    ty = pz + oy
    text_len = len(text) * 7 + 16
    draw.rectangle([tx, ty, tx + text_len, ty + 24], fill=(15, 18, 22), outline=col, width=2)
    draw.text((tx + 8, ty + 5), text, fill=(245, 248, 255))

topo_path = BASE_DIR / "ASHENFALL_TOPOGRAPHIC_RENDER.png"
topo_img.save(topo_path, quality=95)
print(f" [✓] Created Topographic Render: {topo_path} ({topo_path.stat().st_size:,} bytes)")
shutil.copy2(topo_path, BUILDS_MAP1_DIR / "ASHENFALL_TOPOGRAPHIC_RENDER.png")

# ---------------------------------------------------------------------------
# 6. Generate Updated WorldPainter Import Guide
# ---------------------------------------------------------------------------
print("\n [6/6] Updating WorldPainter Import Guide...")
guide_path = BASE_DIR / "WORLDPAINTER_IMPORT_GUIDE.md"
with open(guide_path, "w", encoding="utf-8") as f:
    f.write("""# WorldPainter Import Guide: Ashenfall Continent of Vantyra
### *How to Import the Master 16-Bit Heightmap into WorldPainter*

---

## 🗺️ Master Deliverables
* **16-Bit Grayscale Heightmap:** `ASHENFALL_HEIGHTMAP_16BIT.png` (4096 x 4096, 16-bit uint16)
* **Satellite Visual Reference:** `ASHENFALL_TOPOGRAPHIC_RENDER.png`
* **Preview Heightmap:** `ASHENFALL_HEIGHTMAP_PREVIEW.png`

---

## 🛠️ Step-by-Step WorldPainter Import Instructions

1. **Launch WorldPainter**.
2. Click **`File` ➔ `Import` ➔ `Height map...`**
3. Browse and select: **`ASHENFALL_HEIGHTMAP_16BIT.png`**.
4. In the **Import Height Map** dialog, configure these **exact settings**:

### ⚙️ Exact Height Settings:
* **Mapping:**
  - **Scale:** `100%` (produces an exact $4{,}096 \\times 4{,}096$ block world; or `200%` for full $8{,}000 \\times 8{,}000$ blocks)
  - **Height:** Set **`Lower limit: -64`** and **`Upper limit: 320`** (Total 384 blocks).
* **Water:**
  - **Water level:** **`62`**
  - Check: **`Create water in areas lower than water level`**
* **Terrain:**
  - Surface material: **`Bare stone / grass`**
* **Border:**
  - Border type: **`Endless water`** (This naturally creates The Veil of Salt ocean surrounding your continent!)

5. Click **`OK`**.
   WorldPainter will sculpt the entire continent in seconds!

---

## 🎨 Recommended Biome & Layer Painting in WorldPainter:

1. **The Ashen Caldera (Center: `0, 0`):**
   - Paint **`Basalt Deltas`** or **`Nether Wastes`** inside the crater basin.
   - Use the **`Blackstone`** or **`Basalt`** terrain palette for the volcanic rim ($Y=145$).
2. **The Cogwork March (West: `-2100, 0`):**
   - Paint **`Windswept Gravelly Hills`** and **`Badlands`**.
   - Carve Create factory foundations along the brass river canyons.
3. **The Solitary Glacial Spine (North: `0, -2500`):**
   - Paint **`Frozen Peaks`** on the summits ($Y \\ge 180$).
   - Paint **`Snowy Slopes`** and **`Grove`** down the mountainsides.
4. **The Gilded Dunes (East: `2300, 0`):**
   - Paint **`Desert`** on the rolling barchan dunes.
   - Paint **`Red Sand`** and **`Terracotta`** on the flat-topped mesas.
5. **The Forgotten Coast (South: `0, 2500`):**
   - Paint **`Plains`** and **`Meadow`** on the coastal bluffs.
   - Paint **`Stony Shore`** along the waterline.

---

## 🚀 Exporting to Minecraft 1.21.1:

1. Click **`File` ➔ `Export` ➔ `Export as Minecraft map...`**
2. In the Export dialog:
   - **Game version:** Select **`Minecraft 1.19 or later (Deepslate / 384 blocks)`**.
   - Check **`Allow Cheats`** and select **`Survival`**.
3. **The Populate Layer (Still Life Compatibility):**
   - If you want **Still Life** to generate all dense trees, fallen logs, and wildflowers: enable **`Populate`** on the land!
4. Click **`Export`** and choose your `.minecraft/saves/Ashenfall` directory!
""")

shutil.copy2(guide_path, BUILDS_MAP1_DIR / "WORLDPAINTER_IMPORT_GUIDE.md")

elapsed = time.time() - start_time
print("=" * 72)
print(f" [✓] MASTER GEOLOGICAL SYNTHESIS COMPLETE in {elapsed:.1f}s!")
print("=" * 72)

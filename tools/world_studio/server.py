#!/usr/bin/env python3
"""
=============================================================================
ASHENFALL WORLDSTUDIO: Unified WorldEngine Server
Unifies WorldPainter, Lithosphere, Still Life, and Continents into 1 Interface
=============================================================================
"""

import os
import sys
import json
import math
import mimetypes
import urllib.parse
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
STUDIO_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = STUDIO_DIR / "public"

PORT = 3000

class WorldStudioHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC_DIR), **kwargs)

    def end_headers(self):
        # Enable CORS and disable aggressive caching for live preview updates
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # 1. API: Get Current World Status & Engine Specs
        if path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            status_data = {
                "name": "Ashenfall: Continent of Vantyra",
                "version": "2.4.0-UnifiedEngine",
                "world_size": {"width_blocks": 8000, "height_blocks": 8000, "res_px": 4096},
                "elevation": {"min_y": -64, "max_y": 320, "sea_level": 62, "peak_y": 279.2},
                "engines": {
                    "continents": {
                        "name": "Continents (Starmute Logic)",
                        "status": "Active",
                        "continent_radius": 3550,
                        "ocean_name": "The Veil of Salt",
                        "shelf_dropoff": "Hermite S-Curve (-600 blocks)"
                    },
                    "lithosphere": {
                        "name": "Lithosphere (J4yzet Logic)",
                        "status": "Active",
                        "spline_interpolation": "Continuous Cubic Hermite",
                        "alpine_fractal": "6-Octave Multi-Rigid Domain Warped",
                        "canyon_carver": "Quadratic U-Shaped River Valleys",
                        "terracing": "Harmonic Strata Quantization (9m steps)"
                    },
                    "still_life": {
                        "name": "Still Life (J4yzet Logic)",
                        "status": "Active",
                        "slope_rules": "Topsoil < 35°, Exposed Rock > 45°",
                        "forest_layer": "Multi-tier canopies, fallen logs, mossy boulders",
                        "populate_coverage": "Habitable valleys & plains (excludes volcanic caldera)"
                    },
                    "worldpainter": {
                        "name": "WorldPainter (Captain Chaos)",
                        "status": "Integrated",
                        "formats": ["16-bit uint16 master", "Populate mask", "Biome mask", "1-click JS script"]
                    }
                },
                "landmarks": [
                    {"id": "spawn", "name": "The Forgotten Coast (Spawn)", "x": 0, "z": 2500, "y": 72, "biome": "Plains / Meadow"},
                    {"id": "spine", "name": "The Solitary Glacial Spine", "x": 0, "z": -2500, "y": 279, "biome": "Frozen Peaks / Grove"},
                    {"id": "cogwork", "name": "The Cogwork March", "x": -2100, "z": 0, "y": 95, "biome": "Badlands / Windswept Hills"},
                    {"id": "caldera", "name": "The Ashen Caldera", "x": 0, "z": 0, "y": 146, "biome": "Basalt Deltas / Nether Wastes"},
                    {"id": "dunes", "name": "The Gilded Dunes", "x": 2300, "z": 0, "y": 94, "biome": "Desert / Eroded Badlands"},
                    {"id": "fen", "name": "The Whispering Fen", "x": 2000, "z": 2000, "y": 63, "biome": "Swamp / Mangrove"},
                    {"id": "reach", "name": "The Sunken Reach", "x": -2400, "z": 1600, "y": 54, "biome": "Warm Ocean / Atolls"}
                ]
            }
            self.wfile.write(json.dumps(status_data, indent=2).encode("utf-8"))
            return

        # 2. File Downloads & Asset Proxies
        asset_map = {
            "/assets/topographic.png": BASE_DIR / "ASHENFALL_TOPOGRAPHIC_RENDER.png",
            "/assets/heightmap_preview.png": BASE_DIR / "ASHENFALL_HEIGHTMAP_PREVIEW.png",
            "/assets/populate_mask.png": BASE_DIR / "ASHENFALL_POPULATE_MASK.png",
            "/assets/biome_mask.png": BASE_DIR / "ASHENFALL_BIOME_MASK.png",
            "/downloads/heightmap_16bit.png": BASE_DIR / "ASHENFALL_HEIGHTMAP_16BIT.png",
            "/downloads/worldpainter_suite.zip": BASE_DIR / "ASHENFALL_WORLDPAINTER_SUITE.zip",
            "/downloads/datapack.zip": BASE_DIR / "builds" / "data2.zip",
            "/downloads/setup.ps1": BASE_DIR / "setup.ps1",
            "/downloads/script.js": BASE_DIR / "ashenfall_worldpainter_setup.js"
        }

        if path in asset_map:
            target_file = asset_map[path]
            if target_file.exists():
                mime, _ = mimetypes.guess_type(str(target_file))
                self.send_response(200)
                self.send_header("Content-Type", mime or "application/octet-stream")
                self.send_header("Content-Length", str(target_file.stat().st_size))
                if "/downloads/" in path:
                    self.send_header("Content-Disposition", f'attachment; filename="{target_file.name}"')
                self.end_headers()
                with open(target_file, "rb") as f:
                    while chunk := f.read(65536):
                        self.wfile.write(chunk)
                return
            else:
                self.send_error(404, f"File {target_file.name} not found")
                return

        # 3. Fallback to standard static file serving from public/
        return super().do_GET()

def run_server():
    server_address = ("0.0.0.0", PORT)
    httpd = ThreadingHTTPServer(server_address, WorldStudioHandler)
    print(f"=====================================================================")
    print(f"   ⚔ ASHENFALL WORLDSTUDIO — The United WorldEngine ⚔")
    print(f"   Unified Interface: WorldPainter + Lithosphere + Still Life + Continents")
    print(f"   Server listening on: http://0.0.0.0:{PORT}")
    print(f"=====================================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping WorldStudio server...")
        httpd.server_close()

if __name__ == "__main__":
    run_server()

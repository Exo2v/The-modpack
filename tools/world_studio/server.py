#!/usr/bin/env python3
"""
=============================================================================
ASHENFALL WORLDSTUDIO: Unified WorldEngine Server
Unifies WorldPainter, Lithosphere, Still Life, and Continents into 1 Interface
Includes WorldPainter JSR223 Scripting API Integration Backend
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

# Add repo root to sys.path so tools.worldpainter_api can be imported
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from tools.worldpainter_api import WorldPainterScriptBuilder, WorldPainterCLIBridge, TERRAIN_TYPES, MINECRAFT_BIOME_IDS

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
        self.handle_request(send_body=False)

    def do_GET(self):
        self.handle_request(send_body=True)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len) if content_len > 0 else b"{}"

        try:
            req_data = json.loads(body.decode("utf-8")) if body else {}
        except Exception:
            req_data = {}

        # 1. API: Generate WorldPainter JSR223 Script
        if path == "/api/worldpainter/generate-script":
            world_name = req_data.get("world_name", "Ashenfall_Continent")
            min_y = int(req_data.get("min_y", -64))
            max_y = int(req_data.get("max_y", 320))
            sea_level = int(req_data.get("sea_level", 62))
            enable_stratification = bool(req_data.get("enable_stratification", True))
            enable_frost = bool(req_data.get("enable_frost", True))
            frost_altitude = int(req_data.get("frost_altitude", 210))
            export_mode = req_data.get("export_mode", "world")
            export_target = req_data.get("export_target", None)

            builder = WorldPainterScriptBuilder(
                world_name=world_name,
                min_y=min_y,
                max_y=max_y,
                sea_level=sea_level,
                heightmap_path="worldpainter/ASHENFALL_HEIGHTMAP_16BIT.png",
                populate_mask_path="worldpainter/ASHENFALL_POPULATE_MASK.png" if req_data.get("enable_populate", True) else None,
                biome_mask_path="worldpainter/ASHENFALL_BIOME_MASK.png" if req_data.get("enable_biome_mask", False) else None,
                enable_stratification=enable_stratification,
                enable_frost=enable_frost,
                frost_altitude=frost_altitude,
                export_mode=export_mode,
                export_target=export_target
            )
            script_code = builder.generate_javascript()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            resp = {
                "success": True,
                "world_name": world_name,
                "script": script_code,
                "dimensions": {"min_y": min_y, "max_y": max_y, "sea_level": sea_level}
            }
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        # 2. API: Execute Headless WorldPainter Script
        elif path == "/api/worldpainter/run":
            script_path = req_data.get("script_path", "worldpainter/ashenfall_worldpainter_setup.js")
            result = WorldPainterCLIBridge.execute_script(script_path)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode("utf-8"))
            return

        else:
            self.send_error(404, "API endpoint not found")
            return

    def handle_request(self, send_body=True):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # 1. API: Get Current World Status & Engine Specs
        if path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            status_data = {
                "name": "Ashenfall: Continent of Vantyra",
                "version": "2.5.0-UnifiedEngine",
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
                        "name": "WorldPainter Scripting API",
                        "status": "Integrated (JSR223 & wpscript)",
                        "formats": ["16-bit uint16 master", "Populate mask", "Biome mask", "JSR223 JS Engine", "CLI Runner"]
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
            if send_body:
                self.wfile.write(json.dumps(status_data, indent=2).encode("utf-8"))
            return

        # 2. API: WorldPainter System Status & Detection
        if path == "/api/worldpainter/status":
            wpscript_path = WorldPainterCLIBridge.find_wpscript()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            resp = {
                "installed": wpscript_path is not None,
                "wpscript_path": str(wpscript_path) if wpscript_path else None,
                "supported_api_version": "JSR-223 ECMAScript / Rhino / GraalJS",
                "default_dimensions": {"min_y": -64, "max_y": 320, "sea_level": 62},
                "terrain_types": TERRAIN_TYPES,
                "biome_ids": MINECRAFT_BIOME_IDS
            }
            if send_body:
                self.wfile.write(json.dumps(resp, indent=2).encode("utf-8"))
            return

        # 3. File Downloads & Asset Proxies
        asset_map = {
            "/assets/still_life_populate.png": BASE_DIR / "worldpainter" / "ASHENFALL_STILL_LIFE_POPULATE_VIEW.png",
            "/assets/topographic.png": BASE_DIR / "worldpainter" / "ASHENFALL_TOPOGRAPHIC_RENDER.png",
            "/assets/heightmap_preview.png": BASE_DIR / "worldpainter" / "ASHENFALL_HEIGHTMAP_PREVIEW.png",
            "/assets/populate_mask.png": BASE_DIR / "worldpainter" / "ASHENFALL_POPULATE_MASK.png",
            "/assets/biome_mask.png": BASE_DIR / "worldpainter" / "ASHENFALL_BIOME_MASK.png",
            "/downloads/heightmap_16bit.png": BASE_DIR / "worldpainter" / "ASHENFALL_HEIGHTMAP_16BIT.png",
            "/downloads/worldpainter_suite.zip": BASE_DIR / "worldpainter" / "ASHENFALL_WORLDPAINTER_SUITE.zip",
            "/downloads/datapack.zip": BASE_DIR / "datapacks" / "ashenfall_data2.zip",
            "/downloads/setup.ps1": BASE_DIR / "setup.ps1",
            "/downloads/script.js": BASE_DIR / "worldpainter" / "ashenfall_worldpainter_setup.js",
            "/downloads/run_worldpainter_api.bat": BASE_DIR / "scripts" / "run_worldpainter_api.bat",
            "/downloads/run_worldpainter_api.sh": BASE_DIR / "scripts" / "run_worldpainter_api.sh",
            "/downloads/worldpainter_api.py": BASE_DIR / "tools" / "worldpainter_api.py",
            "/downloads/lithosphere.zip": BASE_DIR / "datapacks" / "sources" / "lithosphere-1.8.2.zip",
            "/downloads/still_life.zip": BASE_DIR / "datapacks" / "sources" / "still_life-0.1.1.zip",
            "/downloads/tectonic.zip": BASE_DIR / "datapacks" / "sources" / "tectonic-3.0.25.zip"
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
                if send_body:
                    with open(target_file, "rb") as f:
                        while chunk := f.read(65536):
                            self.wfile.write(chunk)
                return
            else:
                self.send_error(404, f"File {target_file.name} not found")
                return

        # 4. Fallback to standard static file serving from public/
        if send_body:
            return super().do_GET()
        else:
            return super().do_HEAD()

def run_server():
    server_address = ("0.0.0.0", PORT)
    httpd = ThreadingHTTPServer(server_address, WorldStudioHandler)
    print(f"=====================================================================")
    print(f"   ⚔ ASHENFALL WORLDSTUDIO — The United WorldEngine ⚔")
    print(f"   Unified Interface: WorldPainter API + Lithosphere + Still Life + Continents")
    print(f"   Server listening on: http://0.0.0.0:{PORT}")
    print(f"=====================================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping WorldStudio server...")
        httpd.server_close()

if __name__ == "__main__":
    run_server()

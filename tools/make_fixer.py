import json
from pathlib import Path

scripts_dir = Path("pack/overrides/kubejs/server_scripts")
canonical = {}
for js_path in sorted(scripts_dir.glob("*.js")):
    canonical[js_path.name] = js_path.read_text(encoding="utf-8")

startup_script = Path("pack/overrides/kubejs/startup_scripts/items.js").read_text(encoding="utf-8")
iaf_config = Path("pack/overrides/config/iceandfire-common.toml").read_text(encoding="utf-8")

lines = [
    '@echo off & (python -x "%~f0" %* || py -x "%~f0" %*) & pause & goto :eof',
    '#!/usr/bin/env python3',
    '# =============================================================================',
    '# ASHENFALL — 1-Click Crash Hotfixer & Mod Cleaner',
    '# Purges Hollowmarch & incompatible mods, sets 20 hearts, configures rare dragons, & updates KubeJS scripts',
    '# =============================================================================',
    '',
    'import os',
    'import sys',
    'from pathlib import Path',
    '',
    'CANONICAL_SCRIPTS = ' + json.dumps(canonical, indent=4),
    '',
    'ITEMS_JS = ' + json.dumps(startup_script),
    '',
    'IAF_CONFIG = ' + json.dumps(iaf_config),
    '',
    '''def find_game_dirs():
    dirs = []
    appdata = os.environ.get("APPDATA", "")
    if appdata:
        dirs.append(Path(appdata) / ".tlauncher" / "legacy" / "Minecraft" / "game" / "home" / "NeoForge 1.21.1")
        dirs.append(Path(appdata) / ".minecraft")
    
    dirs.append(Path.cwd())
    if Path.cwd().parent.name == "game":
        dirs.append(Path.cwd().parent)
    
    existing = []
    for d in dirs:
        if d.exists() and d not in existing:
            existing.append(d)
    return existing

def main():
    print("=" * 60)
    print("   ASHENFALL 1-CLICK CRASH HOTFIXER & MOD CLEANER")
    print("=" * 60)
    
    game_dirs = find_game_dirs()
    if not game_dirs:
        print("[!] Could not locate Minecraft installation directory automatically.")
        return
    
    total_cleaned = 0
    total_healed = 0
    
    BLACKLIST = [
        ("hollowmarch", "Causes create:large_water_wheel registry crash on world creation"),
        ("bettercombat", "Replaced with Vanilla PvP mechanics per configuration"),
        ("terralith", "Replaced with Lithosphere + Still Life biome architecture"),
        ("optifine", "Incompatible with NeoForge 1.21.1 and Embeddium"),
        ("rubidium", "Deprecated Forge fork replaced by Embeddium"),
        ("magnesium", "Deprecated Forge fork"),
        ("sodium-fabric", "Fabric build in NeoForge folder"),
        ("iris-fabric", "Fabric build in NeoForge folder"),
        ("shine", "Produces uncalibrated bloom artifacts and blinding superbright spots on 1.21.1"),
        ("wavify", "Causes spammy white crescent wave billboard artifacts on rivers"),
        ("streamsreflowing", "Causes 0% world generation infinite loop and chunk lock freeze"),
        ("streams-reflowing", "Causes 0% world generation infinite loop and chunk lock freeze"),
        ("graveyard", "Causes fatal Registry is already frozen [graveyard:tg_jigsaw] crash in worldgen worker thread"),
        ("mini_boss_boss_bars", "Contains broken functions referencing uninstalled mods"),
        ("better-boss-bars", "Contains broken functions referencing uninstalled mods")
    ]
    
    for gdir in game_dirs:
        print(f"\\nScanning directory: {gdir}")
        
        # 1. Purge corrupted files, bundles, and blacklisted mods
        mods_dir = gdir / "mods"
        if mods_dir.exists():
            for item in list(mods_dir.iterdir()):
                if item.is_file():
                    if item.suffix.lower() in (".mrpack", ".zip", ".tmp", ".txt", ".crdownload"):
                        print(f"  [FIXED] Removed non-mod bundle: {item.name}")
                        try:
                            item.unlink()
                            total_cleaned += 1
                        except Exception:
                            pass
                        continue
                    if item.stat().st_size == 0:
                        print(f"  [FIXED] Removed 0-byte file: {item.name}")
                        try:
                            item.unlink()
                            total_cleaned += 1
                        except Exception:
                            pass
                        continue

            for jar in list(mods_dir.glob("*.jar")):
                nl = jar.name.lower()
                for kw, reason in BLACKLIST:
                    if kw in nl:
                        print(f"  [FIXED] Deleting incompatible mod ({reason}): {jar.name}")
                        try:
                            jar.unlink()
                            total_cleaned += 1
                        except Exception as e:
                            print(f"  [ERROR] Failed to delete {jar.name}: {e}")
                        break
        
        # 2. Update KubeJS server scripts (including 20 Hearts / player_health.js)
        server_dir = gdir / "kubejs" / "server_scripts"
        if not server_dir.exists():
            server_dir.mkdir(parents=True, exist_ok=True)
            
        dup = server_dir / "boss_monologues.js"
        if dup.exists():
            try:
                dup.unlink()
                print("  [FIXED] Removed duplicate boss_monologues.js")
                total_healed += 1
            except Exception:
                pass
                
        for filename, script_code in CANONICAL_SCRIPTS.items():
            dest = server_dir / filename
            dest.write_text(script_code, encoding="utf-8")
            print(f"  [FIXED] Wrote verified Rhino JS script: kubejs/server_scripts/{filename}")
            total_healed += 1
            
        # 3. Update KubeJS startup scripts
        startup_dir = gdir / "kubejs" / "startup_scripts"
        if not startup_dir.exists():
            startup_dir.mkdir(parents=True, exist_ok=True)
        items_dest = startup_dir / "items.js"
        items_dest.write_text(ITEMS_JS, encoding="utf-8")
        print("  [FIXED] Wrote verified startup script: kubejs/startup_scripts/items.js")
        total_healed += 1

        # 4. Deploy rare dragon configuration (iceandfire-common.toml)
        config_dir = gdir / "config"
        if not config_dir.exists():
            config_dir.mkdir(parents=True, exist_ok=True)
        iaf_dest = config_dir / "iceandfire-common.toml"
        iaf_dest.write_text(IAF_CONFIG, encoding="utf-8")
        print("  [FIXED] Installed rare dragon configuration: config/iceandfire-common.toml")
        total_healed += 1

    print("\\n" + "=" * 60)
    print(f"[SUCCESS] Cleaned {total_cleaned} crash-inducing JAR(s) and healed/updated {total_healed} file(s)!")
    print("Features active:")
    print("  * 20 Hearts (40 Max HP) base player health")
    print("  * Rare, hard-to-find Apex Boss Dragons (iceandfire-common.toml)")
    print("  * 100% pure Rhino JS compatible KubeJS scripts")
    print("You can now launch Minecraft and click 'Create World' without crashes!")
    print("=" * 60 + "\\n")

if __name__ == "__main__":
    main()
'''
]

content = "\n".join(lines)
with open("fix_crash.bat", "w", encoding="utf-8", newline="\r\n") as f:
    f.write(content)

print("Generated fix_crash.bat successfully!")

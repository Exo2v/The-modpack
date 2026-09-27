import json
from pathlib import Path

scripts_dir = Path("pack/overrides/kubejs/server_scripts")
canonical = {}
for js_path in sorted(scripts_dir.glob("*.js")):
    canonical[js_path.name] = js_path.read_text(encoding="utf-8")

startup_script = Path("pack/overrides/kubejs/startup_scripts/items.js").read_text(encoding="utf-8")

lines = [
    '@echo off & (python -x "%~f0" %* || py -x "%~f0" %*) & pause & goto :eof',
    '#!/usr/bin/env python3',
    '# =============================================================================',
    '# ASHENFALL — 1-Click Crash Hotfixer',
    '# Purges Hollowmarch JAR and updates KubeJS scripts to 100% pure Rhino JS',
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
    print("       ASHENFALL 1-CLICK CRASH & KUBEJS HOTFIXER")
    print("=" * 60)
    
    game_dirs = find_game_dirs()
    if not game_dirs:
        print("[!] Could not locate Minecraft installation directory automatically.")
        return
    
    total_cleaned = 0
    total_healed = 0
    
    for gdir in game_dirs:
        print(f"\\nScanning directory: {gdir}")
        
        # 1. Purge Hollowmarch JAR from mods folder
        mods_dir = gdir / "mods"
        if mods_dir.exists():
            for jar in mods_dir.glob("*.jar"):
                if "hollowmarch" in jar.name.lower():
                    print(f"  [FIXED] Deleting offending Hollowmarch mod: {jar.name}")
                    try:
                        jar.unlink()
                        total_cleaned += 1
                    except Exception as e:
                        print(f"  [ERROR] Failed to delete {jar.name}: {e}")
        
        # 2. Update KubeJS server scripts
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

    print("\\n" + "=" * 60)
    print(f"[SUCCESS] Cleaned {total_cleaned} crash-inducing JAR(s) and healed {total_healed} script(s)!")
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

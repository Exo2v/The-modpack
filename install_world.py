#!/usr/bin/env python3
"""
=============================================================================
ASHENFALL — Handcrafted World Installer & GitHub Downloader
=============================================================================
Pulls the complete 8,000x8,000 Elden Ring continent world save from GitHub
and installs it directly into your Minecraft saves folder.

Usage:
    python install_world.py
    python install_world.py --path "C:\\custom\\path\\saves"
    python install_world.py --force
=============================================================================
"""

import os
import sys
import time
import argparse
import platform
import zipfile
import shutil
import urllib.request
import urllib.error
from pathlib import Path

# GitHub Repository & Branch
GITHUB_REPO = "Exo2v/The-modpack"
GITHUB_BRANCH = "arena/01a0e180-the-modpack"

PRIMARY_DOWNLOAD_URL = (
    f"https://github.com/{GITHUB_REPO}/raw/{GITHUB_BRANCH}/saves/Ashenfall.zip"
)
FALLBACK_DOWNLOAD_URL = (
    f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/saves/Ashenfall.zip"
)


def get_default_minecraft_saves():
    """Detect default Minecraft saves directory based on OS."""
    system = platform.system()
    cwd = Path.cwd()

    # Check if run from within a .minecraft folder or repo containing saves
    if (cwd / "saves").is_dir() and cwd.name == ".minecraft":
        return (cwd / "saves").resolve()

    if system == "Windows":
        appdata = os.environ.get("APPDATA")
        if appdata:
            win_path = Path(appdata) / ".minecraft" / "saves"
            if win_path.exists():
                return win_path.resolve()
            return win_path  # Return even if not created yet
    elif system == "Darwin":  # macOS
        mac_path = Path.home() / "Library" / "Application Support" / "minecraft" / "saves"
        if mac_path.exists():
            return mac_path.resolve()
        return mac_path
    else:  # Linux
        linux_path = Path.home() / ".minecraft" / "saves"
        if linux_path.exists():
            return linux_path.resolve()
        return linux_path

    # Fallback to current directory's saves
    return (cwd / "saves").resolve()


def download_with_progress(url, dest_path):
    """Download a file with a live terminal progress bar."""
    print(f" Connecting to GitHub: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AshenfallWorldInstaller/1.0"
    }
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            total_size = resp.headers.get("Content-Length")
            total_bytes = int(total_size) if total_size else 0

            downloaded = 0
            block_size = 65536
            t0 = time.time()

            with open(dest_path, "wb") as out_file:
                while True:
                    chunk = resp.read(block_size)
                    if not chunk:
                        break
                    out_file.write(chunk)
                    downloaded += len(chunk)

                    if total_bytes > 0:
                        pct = (downloaded / total_bytes) * 100
                        elapsed = time.time() - t0
                        speed = (downloaded / (1024 * 1024)) / max(elapsed, 0.001)
                        mb_down = downloaded / (1024 * 1024)
                        mb_tot = total_bytes / (1024 * 1024)
                        bar = "#" * int(pct / 4) + "-" * (25 - int(pct / 4))
                        sys.stdout.write(
                            f"\r [{bar}] {pct:5.1f}% ({mb_down:5.1f}/{mb_tot:5.1f} MB) - {speed:.1f} MB/s"
                        )
                        sys.stdout.flush()
                    else:
                        mb_down = downloaded / (1024 * 1024)
                        sys.stdout.write(f"\r Downloaded: {mb_down:.1f} MB...")
                        sys.stdout.flush()

            sys.stdout.write("\n")
            return True
    except Exception as e:
        print(f"\n [!] Download error: {e}")
        if os.path.exists(dest_path):
            os.remove(dest_path)
        return False


def extract_world_zip(zip_path, target_dir):
    """Extract world zip into target saves directory."""
    print(f" Extracting world files into: {target_dir}")
    os.makedirs(target_dir, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zf:
        members = zf.infolist()
        total = len(members)
        for i, member in enumerate(members):
            zf.extract(member, target_dir)
            if (i + 1) % 5 == 0 or (i + 1) == total:
                pct = ((i + 1) / total) * 100
                sys.stdout.write(f"\r Extracting: {pct:5.1f}% ({i+1}/{total} files)")
                sys.stdout.flush()
        sys.stdout.write("\n")


def generate_world_locally(target_dir):
    """Fallback generator if network is completely unreachable."""
    print("\n [!] Network download unavailable. Running built-in procedural terrain generator...")
    try:
        from tools.build_ashenfall_world import build_world
        # Temporary switch saves directory if needed
        build_world()
        return True
    except Exception as e:
        print(f" Local generator error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Install the Ashenfall Handcrafted Elden-Ring World Save from GitHub."
    )
    parser.add_argument(
        "--path",
        "-p",
        type=str,
        default=None,
        help="Custom Minecraft saves directory path (e.g. C:\\Users\\Name\\AppData\\Roaming\\.minecraft\\saves)",
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Overwrite existing Ashenfall save folder without asking.",
    )
    args = parser.parse_args()

    print("=" * 70)
    print("      ⚔ ASHENFALL — Handcrafted World Save Installer ⚔")
    print("       The 8,000x8,000 Elden Ring Finite Continent of Vantyra")
    print("=" * 70)

    # 1. Resolve saves directory
    if args.path:
        saves_dir = Path(args.path).resolve()
    else:
        saves_dir = get_default_minecraft_saves()

    print(f"\n[1/3] Target Minecraft saves directory:")
    print(f"      {saves_dir}")

    ashenfall_world_dir = saves_dir / "Ashenfall"

    # Check existing world
    if ashenfall_world_dir.exists() and not args.force:
        print(f"\n [i] Notice: 'Ashenfall' world folder already exists at:")
        print(f"     {ashenfall_world_dir}")
        user_choice = input("     Do you want to overwrite and update it? [Y/n]: ").strip().lower()
        if user_choice in ("n", "no"):
            print(" Installation aborted by user.")
            return

    # 2. Acquire Ashenfall.zip
    print(f"\n[2/3] Acquiring world archive (Ashenfall.zip)...")
    temp_zip = Path("Ashenfall_temp.zip")
    zip_source = None

    # Check local repository or current working directory first
    local_candidates = [
        Path("saves/Ashenfall.zip"),
        Path("Ashenfall.zip"),
        Path("../saves/Ashenfall.zip"),
    ]
    for cand in local_candidates:
        if cand.is_file() and cand.stat().st_size > 1000000:
            print(f" [✓] Found local world archive: {cand.resolve()} ({cand.stat().st_size / (1024*1024):.1f} MB)")
            zip_source = cand
            break

    # If no local copy, download from GitHub
    if not zip_source:
        print(" Downloading latest world build from GitHub repository...")
        success = download_with_progress(PRIMARY_DOWNLOAD_URL, temp_zip)
        if not success:
            print(" Retrying with secondary GitHub CDN endpoint...")
            success = download_with_progress(FALLBACK_DOWNLOAD_URL, temp_zip)

        if success and temp_zip.is_file() and temp_zip.stat().st_size > 1000000:
            zip_source = temp_zip
        else:
            print("\n [!] Could not download world archive from GitHub.")
            print("     Attempting fallback procedural generation...")
            if generate_world_locally(ashenfall_world_dir):
                print(" [✓] Procedural generation complete!")
                finish_install(ashenfall_world_dir)
                return
            else:
                print(" [✗] Installation failed. Please check your internet connection or download manually from:")
                print(f"     https://github.com/{GITHUB_REPO}/releases")
                return

    # 3. Extract into Minecraft saves
    print(f"\n[3/3] Installing into Minecraft...")
    try:
        extract_world_zip(zip_source, ashenfall_world_dir)
    finally:
        # Clean up temporary download file if created
        if temp_zip.exists():
            try:
                temp_zip.unlink()
            except Exception:
                pass

    finish_install(ashenfall_world_dir)


def finish_install(world_dir):
    """Verify installation and display instructions."""
    level_dat = world_dir / "level.dat"
    icon_png = world_dir / "icon.png"
    region_dir = world_dir / "region"

    valid = level_dat.is_file() and region_dir.is_dir()

    print("\n" + "=" * 70)
    if valid:
        region_count = len(list(region_dir.glob("*.mca")))
        print(" [✓] INSTALLATION SUCCESSFUL!")
        print("=" * 70)
        print(f" World Name:     Ashenfall - The Broken Realm")
        print(f" World Folder:   {world_dir}")
        print(f" Region Files:   {region_count} regions verified (~{region_count * 1024} chunks)")
        print(f" Spawn Location: X: 0, Y: 68, Z: 2500 (The Forgotten Coast)")
        print(f" World Border:   8,000 x 8,000 blocks (The Veil of Salt)")
        print(f" World Icon:     {'Verified (Satellite Map)' if icon_png.is_file() else 'Default'}")
        print("-" * 70)
        print(" HOW TO PLAY:")
        print("  1. Launch Minecraft 1.21.1 NeoForge.")
        print("  2. Click 'Singleplayer'.")
        print("  3. Select 'Ashenfall - The Broken Realm'.")
        print("  4. Wake upon the Forgotten Coast and begin your pilgrimage!")
    else:
        print(" [!] Installation finished with warnings. Please verify the saves folder:")
        print(f"     {world_dir}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()

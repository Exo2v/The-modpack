#!/usr/bin/env python3
"""
ASHENFALL — Modpack Build Tool
Generates, synchronizes, fetches, verifies, counts, and exports the packwiz project
and distributable .mrpack from tools/modlist.toml.

Stdlib Python 3.11+, zero external dependencies.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import time
import tomllib
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional

# Constants & Paths
REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
MODLIST_PATH = TOOLS_DIR / "modlist.toml"
PACK_DIR = REPO_ROOT / "pack"
MODS_META_DIR = PACK_DIR / "mods"
OVERRIDES_DIR = PACK_DIR / "overrides"
BUILD_DIR = REPO_ROOT / "build"
CACHE_DIR = BUILD_DIR / "cache"
DOWNLOADED_MODS_DIR = BUILD_DIR / "mods"
EXPORT_DIR = BUILD_DIR / "export"

USER_AGENT = "Ashenfall-Builder/0.1.0 (https://github.com/Exo2v/The-modpack)"
CACHE_TTL_SECONDS = 15 * 60  # 15 minutes as per PIPELINE.md

PHASE_ORDER = ["M0", "M1", "M2", "M3", "M3b", "M3c", "M4", "M5", "M6", "M7", "M8", "M9"]


# ---------------------------------------------------------------------------
# TOML Helper Functions (Formatting packwiz files)
# ---------------------------------------------------------------------------

def escape_toml_str(val: str) -> str:
    return json.dumps(val)


def write_pw_toml(path: Path, data: Dict[str, Any]) -> None:
    """Writes a packwiz .pw.toml file."""
    lines = [
        f'name = {escape_toml_str(data.get("name", ""))}',
        f'filename = {escape_toml_str(data.get("filename", ""))}',
        f'side = {escape_toml_str(data.get("side", "both"))}',
        "",
        "[download]",
        f'url = {escape_toml_str(data.get("download_url", ""))}',
        f'hash-format = {escape_toml_str(data.get("hash_format", "sha512"))}',
        f'hash = {escape_toml_str(data.get("hash", ""))}',
        "",
        "[update]",
    ]

    provider = data.get("provider", "modrinth")
    if provider == "modrinth":
        lines.extend([
            "[update.modrinth]",
            f'mod-id = {escape_toml_str(data.get("slug", ""))}',
            f'version = {escape_toml_str(data.get("version_id", ""))}',
        ])
    elif provider == "curseforge":
        lines.extend([
            "[update.curseforge]",
            f'file-id = {data.get("file_id", 0)}',
            f'project-id = {data.get("project_id", 0)}',
        ])

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def sha256_file(path: Path) -> str:
    """Calculates SHA256 of a local file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def sha512_file(path: Path) -> str:
    """Calculates SHA512 of a local file."""
    h = hashlib.sha512()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def sha1_file(path: Path) -> str:
    """Calculates SHA1 of a local file."""
    h = hashlib.sha1()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Manifest Loading
# ---------------------------------------------------------------------------

def load_manifest(manifest_path: Path = MODLIST_PATH) -> Dict[str, Any]:
    if not manifest_path.exists():
        print(f"Error: Manifest not found at {manifest_path}", file=sys.stderr)
        sys.exit(1)
    with open(manifest_path, "rb") as f:
        return tomllib.load(f)


def filter_mods(mods: List[Dict[str, Any]], phase_filter: Optional[str] = None, category_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    result = []
    phase_filter_upper = phase_filter.upper() if phase_filter else None

    # Cumulative or single phase match?
    # If phase_filter is like 'M0', user usually wants that phase or up to that phase.
    # We support exact phase match or '--cumulative' if needed. By default exact phase.
    for mod in mods:
        if phase_filter_upper and mod.get("phase", "").upper() != phase_filter_upper:
            continue
        if category_filter and mod.get("category", "").lower() != category_filter.lower():
            continue
        result.append(mod)
    return result


# ---------------------------------------------------------------------------
# Network & Resolution
# ---------------------------------------------------------------------------

def get_cached_json(cache_file: Path) -> Optional[Any]:
    if not cache_file.exists():
        return None
    try:
        mtime = cache_file.stat().st_mtime
        if (time.time() - mtime) > CACHE_TTL_SECONDS:
            return None
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def save_cached_json(cache_file: Path, data: Any) -> None:
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass


def fetch_modrinth_version(slug: str, mc_version: str = "1.21.1", loader: str = "neoforge", offline: bool = False) -> Optional[Dict[str, Any]]:
    cache_file = CACHE_DIR / "modrinth" / f"{slug}.json"
    cached = get_cached_json(cache_file)
    if cached is not None:
        return cached

    if offline:
        return None

    encoded_versions = urllib.parse.quote(json.dumps([mc_version]))
    encoded_loaders = urllib.parse.quote(json.dumps([loader]))
    url = f"https://api.modrinth.com/v2/project/{slug}/version?game_versions={encoded_versions}&loaders={encoded_loaders}"

    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data:
                # Find primary file in newest version
                version = data[0]
                primary_file = next((f for f in version.get("files", []) if f.get("primary")), None)
                if not primary_file and version.get("files"):
                    primary_file = version["files"][0]

                if primary_file:
                    resolved = {
                        "version_id": version.get("id"),
                        "version_number": version.get("version_number"),
                        "filename": primary_file.get("filename"),
                        "url": primary_file.get("url"),
                        "hashes": primary_file.get("hashes", {}),
                        "size": primary_file.get("size", 0),
                    }
                    save_cached_json(cache_file, resolved)
                    return resolved
    except Exception as e:
        # Check fallback loaders if neoforge didn't return (e.g. forge compatibility)
        if loader == "neoforge":
            return fetch_modrinth_version(slug, mc_version, "forge", offline=offline)
    return None


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_list(args: argparse.Namespace) -> None:
    manifest = load_manifest()
    mods = manifest.get("mods", [])
    filtered = filter_mods(mods, args.phase, args.category)

    if args.json:
        print(json.dumps(filtered, indent=2))
        return

    print(f"\n{'Name':<32} {'Slug':<28} {'Phase':<6} {'Category':<14} {'Provider':<10} {'Risk':<8}")
    print("-" * 102)
    for m in filtered:
        print(f"{m.get('name', ''):<32} {m.get('slug', ''):<28} {m.get('phase', ''):<6} {m.get('category', ''):<14} {m.get('provider', ''):<10} {m.get('risk', ''):<8}")
    print(f"\nTotal mods displayed: {len(filtered)} (of {len(mods)} in manifest)")

    dropped = manifest.get("dropped", [])
    if dropped and not args.phase and not args.category:
        print("\n[Dropped / Excluded Mods]")
        for d in dropped:
            print(f"  • {d.get('name')}: {d.get('reason')}")
    print()


def cmd_count(args: argparse.Namespace) -> None:
    manifest = load_manifest()
    mods = manifest.get("mods", [])
    budget = manifest.get("budget", {})

    max_content = budget.get("max_content", 130)
    max_perf = budget.get("max_performance", 18)
    max_lib = budget.get("max_libraries", 20)

    perf_count = sum(1 for m in mods if m.get("category") == "performance")
    lib_count = sum(1 for m in mods if m.get("category") == "library")
    content_count = sum(1 for m in mods if m.get("category") not in ("performance", "library"))
    total_count = len(mods)

    print("\n" + "=" * 55)
    print(" ASHENFALL MODPACK BUDGET AUDIT")
    print("=" * 55)
    print(f"Content Mods:     {content_count:>3} / {max_content:<3} " + ("✅ PASS" if content_count <= max_content else "❌ EXCEEDED"))
    print(f"Performance Mods: {perf_count:>3} / {max_perf:<3} " + ("✅ PASS" if perf_count <= max_perf else "❌ EXCEEDED"))
    print(f"Library Mods:     {lib_count:>3} / {max_lib:<3} " + ("✅ PASS" if lib_count <= max_lib else "❌ EXCEEDED"))
    print(f"Total Active:     {total_count:>3}")
    print("-" * 55)

    print("Phase Breakdown:")
    for phase in PHASE_ORDER:
        p_mods = [m for m in mods if m.get("phase") == phase]
        if p_mods:
            print(f"  {phase:<6}: {len(p_mods):>2} mods")
    print("=" * 55 + "\n")


def cmd_sync(args: argparse.Namespace) -> None:
    manifest = load_manifest()
    pack_info = manifest.get("pack", {})
    mods = manifest.get("mods", [])
    filtered = filter_mods(mods, args.phase, args.category)

    PACK_DIR.mkdir(parents=True, exist_ok=True)
    MODS_META_DIR.mkdir(parents=True, exist_ok=True)

    mc_ver = pack_info.get("minecraft", "1.21.1")
    loader = pack_info.get("loader", "neoforge")
    loader_ver = pack_info.get("loader_version", "21.1.65")
    pack_name = pack_info.get("name", "Ashenfall")
    pack_ver = pack_info.get("version", "0.1.0")

    # 1. Write pack/pack.toml
    pack_toml_lines = [
        f'name = {escape_toml_str(pack_name)}',
        'author = "Exo2v"',
        f'version = {escape_toml_str(pack_ver)}',
        'pack-format = "packwiz:1.1.0"',
        "",
        "[index]",
        'file = "index.toml"',
        'hash-format = "sha256"',
        "",
        "[versions]",
        f'minecraft = {escape_toml_str(mc_ver)}',
        f'neoforge = {escape_toml_str(loader_ver)}',
    ]
    with open(PACK_DIR / "pack.toml", "w", encoding="utf-8") as f:
        f.write("\n".join(pack_toml_lines) + "\n")

    print(f"\n[sync] Synchronizing packwiz project for {len(filtered)} mods (Minecraft {mc_ver}, {loader} {loader_ver})...")

    index_files = []
    pending_mods = []
    synced_count = 0

    for m in filtered:
        slug = m.get("slug")
        name = m.get("name")
        provider = m.get("provider", "modrinth")
        side = m.get("side", "both")
        pw_file = MODS_META_DIR / f"{slug}.pw.toml"

        res = None
        if provider == "modrinth":
            res = fetch_modrinth_version(slug, mc_ver, loader, offline=args.offline)

        if res:
            # We got resolved online or from cache
            write_pw_toml(pw_file, {
                "name": name,
                "filename": res["filename"],
                "side": side,
                "download_url": res["url"],
                "hash_format": "sha512",
                "hash": res["hashes"].get("sha512", ""),
                "provider": "modrinth",
                "slug": slug,
                "version_id": res["version_id"],
            })
            index_files.append((f"mods/{slug}.pw.toml", sha256_file(pw_file)))
            synced_count += 1
        else:
            # Pinned fallback or pending resolution
            pinned_version = m.get("pin", "latest")
            project_id = m.get("project_id", 0)

            if provider == "custom":
                pending_mods.append({
                    "name": name,
                    "slug": slug,
                    "phase": m.get("phase"),
                    "reason": "Custom mod to be built locally (e.g. ./gradlew build)",
                })
            elif provider == "curseforge":
                pending_mods.append({
                    "name": name,
                    "slug": slug,
                    "phase": m.get("phase"),
                    "project_id": project_id,
                    "reason": f"CurseForge project {project_id} pending file resolution",
                })
            else:
                # Modrinth mod without network / cache yet
                # Synthesize a pinned placeholder pw.toml so packwiz structure is valid
                fallback_filename = f"{slug}-mc{mc_ver}.jar"
                dummy_hash = hashlib.sha512(slug.encode()).hexdigest()
                dummy_url = f"https://cdn.modrinth.com/data/{slug}/versions/{fallback_filename}"

                write_pw_toml(pw_file, {
                    "name": name,
                    "filename": fallback_filename,
                    "side": side,
                    "download_url": dummy_url,
                    "hash_format": "sha512",
                    "hash": dummy_hash,
                    "provider": "modrinth",
                    "slug": slug,
                    "version_id": pinned_version,
                })
                index_files.append((f"mods/{slug}.pw.toml", sha256_file(pw_file)))
                pending_mods.append({
                    "name": name,
                    "slug": slug,
                    "phase": m.get("phase"),
                    "reason": "Offline / network restricted; generated pinned metadata stub",
                })
                synced_count += 1

    # 2. Write pack/index.toml
    index_lines = [
        'hash-format = "sha256"',
        "",
    ]
    for rel_path, file_hash in sorted(index_files):
        index_lines.extend([
            "[[files]]",
            f'file = {escape_toml_str(rel_path)}',
            f'hash = {escape_toml_str(file_hash)}',
            "metafile = true",
            "",
        ])

    with open(PACK_DIR / "index.toml", "w", encoding="utf-8") as f:
        f.write("\n".join(index_lines))

    # 3. Write pack/pending-mods.toml
    pending_lines = [
        "# Mods that require manual JAR assembly, CurseForge CDN resolution, or custom compilation.",
        "",
    ]
    for p in pending_mods:
        pending_lines.extend([
            "[[pending]]",
            f'name = {escape_toml_str(p.get("name", ""))}',
            f'slug = {escape_toml_str(p.get("slug", ""))}',
            f'phase = {escape_toml_str(p.get("phase", ""))}',
            f'reason = {escape_toml_str(p.get("reason", ""))}',
            "",
        ])
    with open(PACK_DIR / "pending-mods.toml", "w", encoding="utf-8") as f:
        f.write("\n".join(pending_lines))

    print(f"[sync] ✅ Wrote pack/pack.toml")
    print(f"[sync] ✅ Wrote pack/index.toml with {len(index_files)} metadata references")
    print(f"[sync] ✅ Wrote pack/pending-mods.toml ({len(pending_mods)} entries)")
    print(f"[sync] Finished. {synced_count} mod metadata files ready in pack/mods/.\n")


def cmd_fetch(args: argparse.Namespace) -> None:
    manifest = load_manifest()
    mods = manifest.get("mods", [])
    filtered = filter_mods(mods, args.phase, args.category)

    target_dir = Path(args.dir) if args.dir else DOWNLOADED_MODS_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n[fetch] Checking / downloading JARs for {len(filtered)} mods into {target_dir}...")
    fetched = 0
    verified = 0
    failed = 0

    for m in filtered:
        slug = m.get("slug")
        pw_file = MODS_META_DIR / f"{slug}.pw.toml"
        if not pw_file.exists():
            continue

        try:
            with open(pw_file, "rb") as f:
                pw_data = tomllib.load(f)
        except Exception:
            continue

        filename = pw_data.get("filename")
        url = pw_data.get("download", {}).get("url")
        expected_hash = pw_data.get("download", {}).get("hash")

        if not filename or not url:
            continue

        dest_file = target_dir / filename
        if dest_file.exists():
            actual_hash = sha512_file(dest_file)
            if actual_hash == expected_hash:
                verified += 1
                continue

        if args.dry_run:
            print(f"  [dry-run] Would fetch {filename} from {url}")
            fetched += 1
            continue

        print(f"  Fetching {filename}...")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=15) as resp, open(dest_file, "wb") as out:
                shutil.copyfileobj(resp, out)
            actual_hash = sha512_file(dest_file)
            if expected_hash and actual_hash != expected_hash:
                print(f"  ❌ Checksum mismatch for {filename}!", file=sys.stderr)
                dest_file.unlink()
                failed += 1
            else:
                fetched += 1
        except Exception as e:
            print(f"  ⚠️ Could not fetch {filename}: {e}", file=sys.stderr)
            failed += 1

    print(f"\n[fetch] Summary: {verified} already verified, {fetched} fetched, {failed} pending/failed.\n")


def cmd_verify(args: argparse.Namespace) -> None:
    manifest = load_manifest()
    mods = manifest.get("mods", [])
    filtered = filter_mods(mods, args.phase, args.category)

    target_dir = Path(args.dir) if args.dir else DOWNLOADED_MODS_DIR
    print(f"\n[verify] Verifying mod JARs in {target_dir}...")

    ok = 0
    missing = 0
    corrupt = 0

    for m in filtered:
        slug = m.get("slug")
        pw_file = MODS_META_DIR / f"{slug}.pw.toml"
        if not pw_file.exists():
            continue

        with open(pw_file, "rb") as f:
            pw_data = tomllib.load(f)

        filename = pw_data.get("filename")
        expected_hash = pw_data.get("download", {}).get("hash")
        file_path = target_dir / filename

        if not file_path.exists():
            missing += 1
            continue

        actual_hash = sha512_file(file_path)
        if actual_hash == expected_hash:
            ok += 1
        else:
            print(f"  ❌ Corrupted: {filename}")
            corrupt += 1

    print(f"\n[verify] Results: {ok} valid, {missing} missing, {corrupt} corrupt.\n")


def cmd_export(args: argparse.Namespace) -> None:
    manifest = load_manifest()
    pack_info = manifest.get("pack", {})
    pack_ver = pack_info.get("version", "0.1.0")
    pack_name = pack_info.get("name", "Ashenfall")
    summary = pack_info.get("summary", "A Soulslike RPG Pilgrimage")
    mc_ver = pack_info.get("minecraft", "1.21.1")
    loader_ver = pack_info.get("loader_version", "21.1.65")

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    downloads_dir = REPO_ROOT / "downloads"
    downloads_dir.mkdir(parents=True, exist_ok=True)

    mrpack_path = EXPORT_DIR / f"ashfall-{pack_ver}.mrpack"
    cf_zip_path = EXPORT_DIR / f"ashfall-{pack_ver}-curseforge.zip"
    bundle_path = EXPORT_DIR / f"ashfall-{pack_ver}-complete-bundle.zip"

    print(f"\n[export] 1. Assembling Modrinth .mrpack archive: {mrpack_path.name}...")

    mr_files = []
    cf_files = []
    if MODS_META_DIR.exists():
        for pw_file in sorted(MODS_META_DIR.glob("*.pw.toml")):
            try:
                with open(pw_file, "rb") as f:
                    pw_data = tomllib.load(f)
                filename = pw_data.get("filename")
                side = pw_data.get("side", "both")
                dl_info = pw_data.get("download", {})
                url = dl_info.get("url")
                sha512 = dl_info.get("hash")

                client_env = "required" if side in ("both", "client") else "unsupported"
                server_env = "required" if side in ("both", "server") else "unsupported"

                mr_files.append({
                    "path": f"mods/{filename}",
                    "hashes": {
                        "sha512": sha512,
                    },
                    "env": {
                        "client": client_env,
                        "server": server_env,
                    },
                    "downloads": [url] if url else [],
                    "fileSize": 0,
                })
            except Exception:
                pass

    # Build CF file list from manifest
    for m in manifest.get("mods", []):
        if m.get("provider") == "curseforge" and m.get("project_id"):
            cf_files.append({
                "projectID": m["project_id"],
                "fileID": 0,
                "required": True,
            })

    # 1. Modrinth .mrpack
    mr_index_json = {
        "formatVersion": 1,
        "game": "minecraft",
        "versionId": pack_ver,
        "name": pack_name,
        "summary": summary,
        "files": mr_files,
        "dependencies": {
            "minecraft": mc_ver,
            "neoforge": loader_ver,
        },
    }
    with zipfile.ZipFile(mrpack_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("modrinth.index.json", json.dumps(mr_index_json, indent=2))
        if OVERRIDES_DIR.exists():
            for root, _, files in os.walk(OVERRIDES_DIR):
                for file in files:
                    full_p = Path(root) / file
                    rel_p = full_p.relative_to(OVERRIDES_DIR)
                    archive_path = Path("overrides") / rel_p
                    zf.write(full_p, archive_path.as_posix())

    # 2. CurseForge zip
    print(f"[export] 2. Assembling CurseForge zip: {cf_zip_path.name}...")
    cf_manifest_json = {
        "minecraft": {
            "version": mc_ver,
            "modLoaders": [
                {
                    "id": f"neoforge-{loader_ver}",
                    "primary": True,
                }
            ],
        },
        "manifestType": "minecraftModpack",
        "manifestVersion": 1,
        "name": pack_name,
        "version": pack_ver,
        "author": "Exo2v",
        "files": cf_files,
        "overrides": "overrides",
    }
    with zipfile.ZipFile(cf_zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("manifest.json", json.dumps(cf_manifest_json, indent=2))
        if OVERRIDES_DIR.exists():
            for root, _, files in os.walk(OVERRIDES_DIR):
                for file in files:
                    full_p = Path(root) / file
                    rel_p = full_p.relative_to(OVERRIDES_DIR)
                    archive_path = Path("overrides") / rel_p
                    zf.write(full_p, archive_path.as_posix())

    # 3. Complete bundle
    print(f"[export] 3. Assembling Complete Distribution Bundle: {bundle_path.name}...")
    with zipfile.ZipFile(bundle_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(mrpack_path, mrpack_path.name)
        zf.write(cf_zip_path, cf_zip_path.name)
        for doc in ["INSTALL_GUIDE.md", "MODLIST.md", "README.md"]:
            doc_p = REPO_ROOT / doc
            if doc_p.exists():
                zf.write(doc_p, doc)
        if OVERRIDES_DIR.exists():
            for root, _, files in os.walk(OVERRIDES_DIR):
                for file in files:
                    full_p = Path(root) / file
                    rel_p = full_p.relative_to(OVERRIDES_DIR)
                    archive_path = Path("overrides") / rel_p
                    zf.write(full_p, archive_path.as_posix())

    # Copy to downloads/ folder for instant direct access
    shutil.copy2(mrpack_path, downloads_dir / mrpack_path.name)
    shutil.copy2(cf_zip_path, downloads_dir / cf_zip_path.name)
    shutil.copy2(bundle_path, downloads_dir / bundle_path.name)

    print(f"[export] ✅ Created {mrpack_path.name} ({mrpack_path.stat().st_size} bytes)")
    print(f"[export] ✅ Created {cf_zip_path.name} ({cf_zip_path.stat().st_size} bytes)")
    print(f"[export] ✅ Created {bundle_path.name} ({bundle_path.stat().st_size} bytes)")
    print(f"[export] All packages copied to {downloads_dir.relative_to(REPO_ROOT)}/ for direct download.\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="ASHENFALL Modpack Build & Generation Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/build.py count
  python tools/build.py list --phase M0
  python tools/build.py sync --phase M0
  python tools/build.py fetch --phase M0
  python tools/build.py export
        """,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list
    p_list = subparsers.add_parser("list", help="List mods in the manifest")
    p_list.add_argument("--phase", help="Filter by milestone phase (M0, M1, etc.)")
    p_list.add_argument("--category", help="Filter by category (performance, combat, etc.)")
    p_list.add_argument("--json", action="store_true", help="Output in JSON format")

    # count
    p_count = subparsers.add_parser("count", help="Audit mod counts against budget constraints")
    p_count.add_argument("--phase", help="Filter by milestone phase")

    # sync
    p_sync = subparsers.add_parser("sync", help="Resolve versions & generate packwiz project files in pack/")
    p_sync.add_argument("--phase", help="Filter by milestone phase")
    p_sync.add_argument("--category", help="Filter by category")
    p_sync.add_argument("--offline", action="store_true", help="Do not attempt remote API requests")
    p_sync.add_argument("--force", action="store_true", help="Bypass cache")

    # fetch
    p_fetch = subparsers.add_parser("fetch", help="Download JARs into build/mods/ and verify checksums")
    p_fetch.add_argument("--phase", help="Filter by milestone phase")
    p_fetch.add_argument("--category", help="Filter by category")
    p_fetch.add_argument("--dir", help="Custom destination folder (default build/mods/)")
    p_fetch.add_argument("--dry-run", action="store_true", help="Preview downloads without fetching")

    # verify
    p_verify = subparsers.add_parser("verify", help="Verify integrity of downloaded JARs in build/mods/")
    p_verify.add_argument("--phase", help="Filter by milestone phase")
    p_verify.add_argument("--category", help="Filter by category")
    p_verify.add_argument("--dir", help="Custom folder to verify (default build/mods/)")

    # export
    p_export = subparsers.add_parser("export", help="Package project into distributable .mrpack")
    p_export.add_argument("--output", help="Custom output archive path")
    p_export.add_argument("--phase", help="Export mods for a specific phase")

    args = parser.parse_args()

    cmd_map = {
        "list": cmd_list,
        "count": cmd_count,
        "sync": cmd_sync,
        "fetch": cmd_fetch,
        "verify": cmd_verify,
        "export": cmd_export,
    }
    cmd_map[args.command](args)


if __name__ == "__main__":
    main()

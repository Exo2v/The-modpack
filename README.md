# ASHENFALL — A Soulslike RPG Pilgrimage

**Minecraft 1.21.1 · NeoForge · Solo · Soulslike Difficulty · Vanilla Combat Instincts Preserved**

---

## 1. Overview

**Ashenfall** is a landmark-driven, narrative-rich RPG modpack set across the shattered ruins of the Vantyric Empire. It features an infinite world anchored by discovery, 9 living cultural nations (Millénaire + custom standing), a parallel magic curriculum (Iron's Spells + Necromancy), and a 21-boss progression staircase.

### Mod Budget Enforcement (`PIPELINE.pdf §1.3`)
- **Content Mods**: $\le 130$ (Current: **94**)
- **Performance / Utility Mods**: $\le 18$ (Current: **15**)
- **Core Libraries**: $\le 20$ (Current: **10**)
- **Total Mod Count**: **119** (Well within overall budget)

---

## 2. Workspace & Space Model (`PIPELINE.pdf §0.1`)

The repository separates durable text definitions from disposable heavy binaries:

| Path | Contents | Size | In Git / Snapshot? |
| :--- | :--- | :--- | :--- |
| `tools/` | `build.py`, `modlist.toml` (Single Source of Truth) | < 100 KB | **Yes** |
| `pack/` | `pack.toml`, `index.toml`, `mods/*.pw.toml`, `overrides/` | ~1 MB | **Yes (The Pack)** |
| `profiles/` | `performance.toml`, `compat.toml`, `magic.toml` | < 10 KB | **Yes** |
| `build/mods/` | Downloaded JAR files | ~400–600 MB | **No (Disposable)** |
| `build/cache/` | API responses (15-min TTL) | ~1 MB | **No (Disposable)** |
| `build/export/` | Distributable `.mrpack` archive | ~450 MB | **No (Disposable)** |

---

## 3. How to Use the Builder

The pack is generated via `tools/build.py` (stdlib Python 3.11+, zero dependencies), wrapped by `./build.sh` (Linux/macOS) and `build.bat` (Windows).

### Common Commands

```bash
# 1. Audit mod counts against budget constraints
./build.sh count

# 2. List mods in the manifest (with optional phase filter)
./build.sh list
./build.sh list --phase M0

# 3. Synchronize packwiz project files (pack.toml, index.toml, mods/*.pw.toml)
./build.sh sync
./build.sh sync --phase M0

# 4. Fetch / download mod JARs and verify sha512 checksums
./build.sh fetch --phase M0

# 5. Verify integrity of downloaded JARs in build/mods/
./build.sh verify --phase M0

# 6. Export the distributable Modrinth .mrpack archive
./build.sh export
```

---

## 4. Documentation References

The complete design specifications live in the repository PDFs:
- **`DESIGN.pdf`**: Master design bible, combat mechanics, class systems, and mod audit.
- **`LORE.pdf`**: The 1,800-year history of Vantyra, Ember Seals, Annals, and Endings.
- **`NARRATIVE-SYSTEMS.pdf`**: Dialogue trees, directional rumours, and Patchouli codex.
- **`PHASES.pdf`**: Milestone checklist (M0–M9) and verification gates.
- **`PIPELINE.pdf`**: Architecture pipeline, ordering rules, and tooling specification.
- **`PROGRESSION.pdf`**: Chapters 0–8 critical path and landmark discovery gates.

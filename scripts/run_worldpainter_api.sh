#!/usr/bin/env bash
set -e

echo "==============================================================================="
echo "       ASHENFALL - WorldPainter JSR223 API Headless Runner"
echo "==============================================================================="
echo

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SCRIPT_PATH="$REPO_ROOT/worldpainter/ashenfall_worldpainter_setup.js"

WPSCRIPT_BIN="$(which wpscript 2>/dev/null || true)"

if [ -z "$WPSCRIPT_BIN" ]; then
    for candidate in \
        "/opt/worldpainter/wpscript" \
        "/usr/local/bin/wpscript" \
        "$HOME/.local/bin/wpscript" \
        "/Applications/WorldPainter.app/Contents/MacOS/wpscript" \
        "$HOME/Applications/WorldPainter.app/Contents/MacOS/wpscript"; do
        if [ -x "$candidate" ]; then
            WPSCRIPT_BIN="$candidate"
            break
        fi
    done
fi

if [ -z "$WPSCRIPT_BIN" ]; then
    echo "[!] Could not locate wpscript executable on this system."
    echo
    echo "To run this script in WorldPainter GUI:"
    echo "  1. Open WorldPainter"
    echo "  2. Go to: Tools -> Run script..."
    echo "  3. Select: $SCRIPT_PATH"
    echo
    echo "Or install WorldPainter and ensure wpscript is in your PATH."
    exit 1
fi

echo "[✓] Found WorldPainter Engine: $WPSCRIPT_BIN"
echo "[✓] Executing script: $SCRIPT_PATH"
echo "-------------------------------------------------------------------------------"

"$WPSCRIPT_BIN" "$SCRIPT_PATH"

echo "-------------------------------------------------------------------------------"
echo "[✓] Done! Output saved."

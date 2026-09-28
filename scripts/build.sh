#!/usr/bin/env bash
set -e

# ASHENFALL build runner wrapper
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON:-python3}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    echo "Error: Python 3.11+ is required to build Ashenfall." >&2
    exit 1
fi

exec "$PYTHON_BIN" "$SCRIPT_DIR/tools/build.py" "$@"

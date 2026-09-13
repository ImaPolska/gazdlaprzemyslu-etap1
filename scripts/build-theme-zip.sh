#!/usr/bin/env bash
# Buduje theme.json i dist/gdp-child-{A|B|C}.zip (wrapper na scripts/build-theme.py).
# Użycie: scripts/build-theme-zip.sh [A|B|C|all]
set -euo pipefail
cd "$(dirname "$0")/.."
D="${1:-all}"
if [ "$D" = "all" ]; then for d in A B C; do python3 scripts/build-theme.py "$d"; done; else python3 scripts/build-theme.py "$D"; fi

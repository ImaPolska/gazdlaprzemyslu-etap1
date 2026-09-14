#!/usr/bin/env bash
# Buduje wszystko: theme.json + ZIP motywu (A/B/C), WXR, theme mods, blueprinty (produkcyjne i dev).
# Użycie: scripts/build-all.sh [BASE_URL]
#   BASE_URL – prefiks URL z {d} zamiast litery kierunku, np.
#   https://raw.githubusercontent.com/ORG/REPO/etap1-{d}/  (domyślnie z pliku config/base-url.txt)
set -euo pipefail
cd "$(dirname "$0")/.."
BASE="${1:-$(cat config/base-url.txt 2>/dev/null || echo 'http://127.0.0.1:8777/')}"
for d in A B C; do python3 scripts/build-theme.py "$d"; done
python3 scripts/build-pages.py
python3 scripts/build-wxr.py
python3 scripts/build-theme-mods.py
python3 scripts/build-blueprints.py --base "$BASE" --out 'blueprints/{d}.json'
python3 scripts/build-blueprints.py --base 'http://127.0.0.1:8777/' --out 'blueprints/dev/{d}.json' --debug
python3 scripts/verify-blocks.py

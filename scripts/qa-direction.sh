#!/usr/bin/env bash
# Pełna kontrola jednego kierunku (A|B|C) na lokalnym Playground:
# start serwera z blueprintem testowym, HTTP 200 dla mapy serwisu + debug.log, zrzuty do docs/screens/.
set -euo pipefail
cd "$(dirname "$0")/.."
D="${1:-A}"
scripts/dev-files.sh >/dev/null
scripts/dev-server.sh "$D"
python3 scripts/verify-http.py --dir "$D" --debug-log tmp/out/debug.log --json "docs/verify/http-$D.json" | tail -3
python3 scripts/screenshot.py --dir "$D" --out docs/screens | tail -1

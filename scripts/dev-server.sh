#!/usr/bin/env bash
# Uruchamia lokalny Playground CLI z blueprintem testowym kierunku A|B|C na porcie 9400.
# Wymaga działającego serwera plików repo: scripts/dev-files.sh (port 8777).
# debug.log trafia do tmp/out/debug.log (montowany katalog /gdp-out).
set -euo pipefail
cd "$(dirname "$0")/.."
D="${1:-A}"; PORT="${2:-9400}"
mkdir -p tmp/out; rm -f tmp/out/debug.log
pid=$(ss -ltnp 2>/dev/null | grep ":$PORT" | grep -o 'pid=[0-9]*' | head -1 | cut -d= -f2 || true)
[ -n "${pid:-}" ] && kill "$pid" && sleep 2
setsid nohup npx --yes @wp-playground/cli@latest server --blueprint="blueprints/dev/$D.json" --port="$PORT" \
  --mount="$PWD/tmp/out:/gdp-out" > "tmp/pg-$D.log" 2>&1 < /dev/null & disown
for i in $(seq 1 60); do grep -q "Ready!" "tmp/pg-$D.log" 2>/dev/null && break; sleep 2; done
tail -1 "tmp/pg-$D.log"

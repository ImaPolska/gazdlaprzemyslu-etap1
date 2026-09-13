#!/usr/bin/env bash
# Serwuje repozytorium po HTTP (port 8777) jako źródło ZIP/WXR/JSON dla blueprintów testowych.
set -euo pipefail
cd "$(dirname "$0")/.."
ss -ltnp 2>/dev/null | grep -q ':8777' && { echo "8777 już działa"; exit 0; }
setsid nohup python3 -m http.server 8777 --bind 127.0.0.1 > tmp/files.log 2>&1 < /dev/null & disown
sleep 1; echo "pliki: http://127.0.0.1:8777/"

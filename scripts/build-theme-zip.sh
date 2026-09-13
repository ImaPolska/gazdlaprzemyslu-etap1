#!/usr/bin/env bash
# Buduje dist/gdp-child-A.zip, -B.zip, -C.zip (oraz dist/gdp-child.zip = kopia wybranego kierunku, domyślnie A).
# Każdy ZIP zawiera katalog gdp-child/ z theme.json i assets/css/variant.css danego kierunku.
# Użycie: scripts/build-theme-zip.sh [A|B|C ...]   (bez argumentów: wszystkie trzy)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/theme/gdp-child"
DIST="$ROOT/dist"
TMP="$ROOT/.tmp-build"
DEFAULT_VARIANT="${DEFAULT_VARIANT:-A}"
VARIANTS=("$@")
[ ${#VARIANTS[@]} -eq 0 ] && VARIANTS=(A B C)

command -v zip >/dev/null || { echo "brak polecenia zip" >&2; exit 1; }
python3 "$ROOT/scripts/build-theme-json.py"

mkdir -p "$DIST"
for V in "${VARIANTS[@]}"; do
  [ -f "$ROOT/theme/variants/$V/theme.json" ] || { echo "brak theme/variants/$V/theme.json" >&2; exit 1; }
  rm -rf "$TMP"; mkdir -p "$TMP"
  cp -R "$SRC" "$TMP/gdp-child"
  cp "$ROOT/theme/variants/$V/theme.json" "$TMP/gdp-child/theme.json"
  mkdir -p "$TMP/gdp-child/assets/css"
  cp "$ROOT/theme/variants/$V/variant.css" "$TMP/gdp-child/assets/css/variant.css"
  # znacznik kierunku w nagłówku style.css (widoczny w Wygląd → Motywy)
  sed -i "s/^Theme Name:.*/Theme Name:   Gaz dla Przemysłu (gdp-child) – kierunek $V/" "$TMP/gdp-child/style.css"
  find "$TMP/gdp-child" -name '.DS_Store' -delete
  rm -f "$DIST/gdp-child-$V.zip"
  (cd "$TMP" && zip -qr -X "$DIST/gdp-child-$V.zip" gdp-child)
  echo "[ok] dist/gdp-child-$V.zip ($(du -h "$DIST/gdp-child-$V.zip" | cut -f1))"
done
cp "$DIST/gdp-child-$DEFAULT_VARIANT.zip" "$DIST/gdp-child.zip"
echo "[ok] dist/gdp-child.zip = kierunek $DEFAULT_VARIANT"
rm -rf "$TMP"

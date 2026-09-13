#!/usr/bin/env bash
# Odtworzenie prototypu na docelowym hostingu (etap 2) przy użyciu WP-CLI.
#
# Założenia:
#  - WordPress jest już zainstalowany (wp core install wykonane), WP-CLI działa w katalogu instalacji,
#  - repozytorium gazdlaprzemyslu jest dostępne lokalnie na serwerze (ścieżka w REPO),
#  - kierunek wizualny wybrany po etapie 1 podajesz w VARIANT (A, B lub C).
#
# Użycie:
#   REPO=/sciezka/do/gazdlaprzemyslu VARIANT=A WP_PATH=/var/www/html bash scripts/restore-on-host.sh
#
# Skrypt jest idempotentny w rozsądnym zakresie: ponowne uruchomienie nadpisze theme_mods i opcje,
# ale import WXR może zduplikować treść — przed powtórnym importem opróżnij witrynę (wp site empty --yes).
set -euo pipefail

REPO="${REPO:-$(cd "$(dirname "$0")/.." && pwd)}"
VARIANT="${VARIANT:-A}"
WP_PATH="${WP_PATH:-.}"
REDAKTOR_PASS="${REDAKTOR_PASS:-Redaktor-Etap1-2026}"
WP="wp --path=$WP_PATH"

case "$VARIANT" in A|B|C) ;; *) echo "VARIANT musi być A, B lub C"; exit 1;; esac
[ -f "$REPO/dist/gdp-child-$VARIANT.zip" ] || { echo "Brak $REPO/dist/gdp-child-$VARIANT.zip — uruchom scripts/build-theme-zip.sh"; exit 1; }
[ -f "$REPO/content/site.wxr" ] || { echo "Brak $REPO/content/site.wxr — uruchom python3 scripts/build-wxr.py"; exit 1; }

echo "[1/7] język i motywy"
$WP language core install pl_PL --activate || true
$WP theme install blocksy --force
$WP theme install "$REPO/dist/gdp-child-$VARIANT.zip" --force --activate

echo "[2/7] importer WXR (wtyczka wordpress-importer jest potrzebna tylko na czas importu)"
$WP plugin install wordpress-importer --activate
$WP import "$REPO/content/site.wxr" --authors=create
$WP plugin deactivate wordpress-importer && $WP plugin delete wordpress-importer

echo "[3/7] konfiguracja Blocksy, menu, strona główna, widgety stopki"
GDP_BASE="$REPO" GDP_VARIANT="$VARIANT" $WP eval-file "$REPO/scripts/playground-setup.php"

echo "[4/7] opcje witryny"
$WP option update blogname "Gaz dla Przemysłu"
$WP option update blogdescription "PBM Sp. z o.o., Grupa IMA Polska"
$WP option update timezone_string "Europe/Warsaw"
$WP option update date_format "j.m.Y"
$WP option update time_format "H:i"
$WP option update default_comment_status "closed"
$WP option update default_ping_status "closed"
$WP option update blog_public 0   # prototyp: nie indeksuj; przed startem produkcyjnym ustaw 1
$WP option update category_base "wiedza/kategoria"
$WP rewrite structure "/wiedza/%postname%/" --hard
$WP rewrite flush --hard

echo "[5/7] użytkownik redaktor"
if ! $WP user get redaktor >/dev/null 2>&1; then
  $WP user create redaktor "redaktor@example.invalid" --role=editor --display_name="Redaktor" --user_pass="$REDAKTOR_PASS"
  echo "    hasło redaktora: $REDAKTOR_PASS (zmień po pierwszym logowaniu)"
fi

echo "[6/7] kontrola"
$WP theme status gdp-child
$WP post list --post_type=page --fields=ID,post_title,post_name --format=table
$WP post list --post_type=wp_block --fields=ID,post_title,post_name --format=table
$WP menu list --format=table

echo "[7/7] gotowe. Otwórz stronę główną i wykonaj test edycji z docs/test-edycji.md."

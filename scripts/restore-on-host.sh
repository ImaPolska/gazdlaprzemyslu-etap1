#!/usr/bin/env bash
# ETAP 2 (staging zleceniodawcy) – odtworzenie serwisu z repozytorium przez WP-CLI.
# Nie uruchamiaj w etapie 1: skrypt wymaga dostępu SSH/WP-CLI do stagingu, którego agent nie ma i o który nie prosi.
# Założenia: czysta instalacja WordPress (pl_PL), WP-CLI w PATH, katalog repo obok. Bez wtyczek (poza ewentualnym
# tymczasowym wordpress-importer do `wp import`, usuwanym na końcu – decyzja do potwierdzenia w P1.4).
#
# Użycie: scripts/restore-on-host.sh <kierunek A|B|C|main> <ścieżka WP> <URL serwisu>
set -euo pipefail
cd "$(dirname "$0")/.."
D="${1:?kierunek}"; WP="${2:?ścieżka do WordPress}"; URL="${3:?URL serwisu}"
wp() { command wp --path="$WP" "$@"; }

wp core language install pl_PL --activate
wp theme install blocksy --version="$(cat config/blocksy-version.txt 2>/dev/null || echo latest)"
python3 scripts/build-theme.py "$D"
wp theme install "dist/gdp-child-$D.zip" --force --activate
wp option update blogname 'Gaz dla Przemysłu'
wp option update blogdescription 'PBM Sp. z o.o., Grupa IMA Polska'
wp option update timezone_string 'Europe/Warsaw'
wp option update permalink_structure '/%postname%/'
wp option update blog_public 0            # staging: bez indeksowania; produkcja: 1 po akceptacji
wp user create redaktor "[[e-mail redaktora]]" --role=editor --user_pass="$(openssl rand -base64 18)"
wp post delete 1 2 3 --force || true
mkdir -p "$WP/gdp-config"
cp config/theme_mods_"$D".json "$WP/gdp-config/theme_mods.json"
cp config/menus.json config/footer.json scripts/apply-theme-mods.php scripts/apply-config.php "$WP/gdp-config/"
wp eval-file "$WP/gdp-config/apply-theme-mods.php"
wp plugin install wordpress-importer --activate   # tymczasowo, tylko do importu
wp import "content/site.$D.wxr" --authors=create
wp plugin uninstall wordpress-importer --deactivate
wp eval-file "$WP/gdp-config/apply-config.php"
wp rewrite flush --hard
rm -rf "$WP/gdp-config"
echo "Gotowe: $URL – sprawdź scripts/verify-http.py --base $URL"

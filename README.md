# Gaz dla Przemysłu – prototyp WordPress (etap 1)

Serwis PBM Sp. z o.o. (Grupa IMA Polska) budowany jako kod: motyw potomny Blocksy (`gdp-child`), bloki core, treść jako markup bloków, konfiguracja jako JSON. Podgląd wyłącznie przez WordPress Playground z blueprintem. Bez wtyczek.

## Struktura

```
blueprints/        A.json, B.json, C.json (produkcyjne, czytają artefakty z tagu w GitHub); dev/ – lokalne (ignorowane w git)
theme/gdp-child/   style.css, functions.php, theme.base.json + variants/{A,B,C}/tokens.json → theme.json, patterns/, assets/
content/           pages.json (manifest), src/*.py (źródła treści), pages/*.html, posts/*.html, blocks/*.html (wp_block), site.{A,B,C}.wxr (generowane)
config/            menus.json, footer.json, theme_mods_{A,B,C}.json (generowane), base-url.txt, blocksy-version.txt
scripts/           budowa, zastosowanie konfiguracji, weryfikacja (sekcja 13), zrzuty
docs/              decisions.md, changelog.md, open-items.md, verify/, screens/
dist/              gdp-child-{A,B,C}.zip (budowane, wersjonowane per tag)
```

## Wymagania

Node ≥ 20 (Playground CLI przez `npx`), Python ≥ 3.11 (`pip install jsonschema playwright pillow` + `playwright install chromium`). PHP nie jest potrzebne – wszystko PHP wykonuje Playground.

## Budowa

```bash
scripts/build-all.sh                         # theme.json + ZIP ×3, WXR ×3, theme mods ×3, blueprinty prod (z config/base-url.txt) i dev, verify-blocks
scripts/build-all.sh 'https://raw.githubusercontent.com/ImaPolska/gazdlaprzemyslu-etap1/<tag>/'   # blueprinty prod na konkretny tag
scripts/build-theme-zip.sh A                 # tylko ZIP jednego kierunku
```

Tokeny zmieniasz w `theme/gdp-child/variants/X/tokens.json` (paleta, fonty, promienie, tryb nagłówka, pasek górny). Treść stron w `content/pages/*.html`, wzorce zsynchronizowane w `content/blocks/*.html`, menu i stopka w `config/`. Po zmianie zawsze `scripts/build-all.sh`.

## Podgląd lokalny

```bash
scripts/dev-files.sh        # serwer plików repo (127.0.0.1:8777) – źródło dla blueprintów dev
scripts/dev-server.sh A     # Playground CLI z blueprints/dev/A.json na 127.0.0.1:9400 (debug.log → tmp/out/debug.log)
scripts/qa-direction.sh A   # start + HTTP 200 dla całej mapy + debug.log + 4 zrzuty do docs/screens/
```

Logowanie: Playground loguje automatycznie jako `admin`; konto redakcyjne `redaktor` (rola Redaktor) – hasło w raporcie punktu kontrolnego.

## Podgląd publiczny (Playground)

Aktualny podgląd (kierunek A, pełna treść stron i artykułów, tag `etap1-v0.1-rc1`):

**https://playground.wordpress.net/?blueprint-url=https://raw.githubusercontent.com/ImaPolska/gazdlaprzemyslu-etap1/etap1-v0.1-rc1/blueprints/A.json**

Ładowanie trwa 1–2 minuty (Playground pobiera WordPress, Blocksy i importuje treść). Playground loguje automatycznie jako `admin`; konto redakcyjne do testu edycji: `redaktor`, hasło w raporcie punktu kontrolnego.

Kierunki z P1.1 (tylko strona główna i `/oferta/cena-stala/`):

- A – https://playground.wordpress.net/?blueprint-url=https://raw.githubusercontent.com/ImaPolska/gazdlaprzemyslu-etap1/etap1-A/blueprints/A.json
- B – https://playground.wordpress.net/?blueprint-url=https://raw.githubusercontent.com/ImaPolska/gazdlaprzemyslu-etap1/etap1-B/blueprints/B.json
- C – https://playground.wordpress.net/?blueprint-url=https://raw.githubusercontent.com/ImaPolska/gazdlaprzemyslu-etap1/etap1-C/blueprints/C.json

Schemat ogólny: blueprint musi leżeć pod publicznym URL z CORS, więc każdy podgląd to osobny tag w GitHub (`https://playground.wordpress.net/?blueprint-url=https://raw.githubusercontent.com/ImaPolska/gazdlaprzemyslu-etap1/<tag>/blueprints/<kierunek>.json`); adres bazowy tagu jest w `config/base-url.txt`, blueprinty przebudowuje `scripts/build-all.sh`. Tagi nie są przesuwane (D26).

Blueprint instaluje Blocksy z wordpress.org, ZIP motywu potomnego z `dist/`, ustawia język pl_PL, opcje i strukturę adresów (`/wiedza/%postname%/`), użytkownika `redaktor`, theme mods (Customizer) z `config/`, importuje WXR, odtwarza menu i stopkę, ustawia stronę główną (`start`) i autora wpisów (`autor`).

## Weryfikacja (sekcja 13)

```bash
python3 scripts/verify-blocks.py --json docs/verify/blocks.json               # 13.1 bloki, h1, templateLock
python3 scripts/verify-blueprint.py blueprints/A.json blueprints/B.json blueprints/C.json   # 13.2 schemat
python3 scripts/verify-http.py --dir A --debug-log tmp/out/debug.log          # 13.2 HTTP 200 + debug.log (na działającym dev-server)
python3 scripts/verify-editor.py --ids 1001,1004                             # ostrzeżenia o nieprawidłowych blokach w edytorze
python3 scripts/open-items.py                                                # 13.6 lista [[ ]] + zakazane frazy → docs/open-items.md
```

## Odtworzenie na hostingu (etap 2)

`scripts/restore-on-host.sh <A|B|C|main> <ścieżka WP> <URL>` – procedura WP-CLI (instalacja Blocksy w wersji z `config/blocksy-version.txt`, ZIP motywu potomnego, opcje, theme mods, import WXR, menu/stopka). Do przeglądu w P1.4; nie uruchamiać w etapie 1.

## Zasady

Nic nie istnieje wyłącznie w instancji Playground. Zmiany w Customizerze eksportujesz `scripts/export-theme-mods.php` do `config/` i odtwarzasz z repo przed wysłaniem linku. Miejsca wymagające danych zleceniodawcy: `[[ ]]` → `docs/open-items.md`.

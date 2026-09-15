# Gaz dla Przemysłu — prototyp WordPress, etap 1

Repozytorium prototypu serwisu gazdlaprzemyslu.pl (PBM Sp. z o.o., Grupa IMA Polska).
Zakres etapu 1: WordPress Playground, motyw Blocksy (free) z motywem potomnym `gdp-child`,
wyłącznie bloki `core/*`, zero wtyczek. Stan: **P1.2** (pełny prototyp wszystkich stron z mapy 8.1, kierunek B jako bazowy; tag `etap1-v0.1`).

Zasada nadrzędna: żadna informacja nie istnieje wyłącznie w instancji Playground — wszystko,
co widać na stronie, jest odtwarzalne z tego repozytorium.

## Linki Playground (kierunki wizualne)

Repozytorium: `https://github.com/ImaPolska/gazdlaprzemyslu-etap1` (gałąź `etap1-p1.2-b`). Adres bazowy plików dla blueprintów (tag `etap1-v0.1`): `https://raw.githubusercontent.com/ImaPolska/gazdlaprzemyslu-etap1/etap1-v0.1`

| Kierunek | Tag | Link uruchomieniowy |
|---|---|---|
| **Główny (P1.2) — pełny prototyp, kierunek B** | `etap1-v0.1` | https://playground.wordpress.net/?blueprint-url=https://raw.githubusercontent.com/ImaPolska/gazdlaprzemyslu-etap1/etap1-v0.1/blueprints/main.json |
| A — Przemysłowy (ostre krawędzie, ceglasty akcent, monospace w liczbach) | `etap1-A` | https://playground.wordpress.net/?blueprint-url=https://raw.githubusercontent.com/ImaPolska/gazdlaprzemyslu-etap1/etap1-v0.1/blueprints/A.json |
| B — Nowoczesny (zaokrąglenia 12 px, ciemne hero, turkusowy akcent) | `etap1-B` | https://playground.wordpress.net/?blueprint-url=https://raw.githubusercontent.com/ImaPolska/gazdlaprzemyslu-etap1/etap1-v0.1/blueprints/B.json |
| C — Ekspercki (serif w nagłówkach, cienkie linie, zielony akcent) | `etap1-C` | https://playground.wordpress.net/?blueprint-url=https://raw.githubusercontent.com/ImaPolska/gazdlaprzemyslu-etap1/etap1-v0.1/blueprints/C.json |

Uwaga: wszystkie cztery blueprinty pobierają pliki (ZIP motywu, WXR, skrypt PHP, theme_mods) z tego samego tagu `etap1-v0.1`; tagi `etap1-A/B/C` z P1.1 pozostają punktami kontrolnymi w historii lokalnej.

Uruchomienie trwa ok. 1–2 minuty (pobranie WordPressa, Blocksy, motywu potomnego, import treści).
Instancja Playground działa w przeglądarce; po zamknięciu karty znika. Link działa tak długo,
jak dostępny jest serwer statyczny z repozytorium.

Logowanie (`/wp-admin/` w tej samej karcie):

| Rola | Login | Hasło |
|---|---|---|
| Administrator | `admin` | `password` (domyślne konto Playground) |
| Redaktor (test edycji, sekcja 14 instrukcji) | `redaktor` | `Redaktor-Etap1-2026` |

## Struktura repozytorium

```
blueprints/            main.json (P1.2, = kierunek B), A.json, B.json, C.json — blueprinty Playground (ten sam zestaw kroków, inny ZIP motywu i theme_mods)
theme/gdp-child/       motyw potomny: style.css, functions.php, 404.php, theme.json (= kierunek A; ZIP-y per kierunek), patterns/*.php, assets/
theme/variants/{A,B,C} theme.json + variant.css per kierunek (generowane skryptem)
content/pages/*.html   treść stron (markup bloków core) z metadanymi w komentarzu nagłówkowym
content/posts/*.html   artykuły Wiedzy (nagłówek: Tytuł, Kategoria, Skrót) i komentarze rynkowe
content/blocks/*.html  wzorce zsynchronizowane (wp_block) i widgety stopki
content/site.wxr       eksport WXR generowany z content/ (strony, wpisy, wp_block, menu)
config/tokens.json     tokeny projektowe (kolory, typografia, odstępy) — źródło dla theme.json i theme_mods
config/theme_mods_*.json  ustawienia Customizera Blocksy per kierunek (generowane)
config/menus.json, footer_structure.json, widgets.json  menu, struktura stopki, widgety
scripts/               budowanie i weryfikacja (opis niżej)
docs/                  decyzje, changelog, otwarte pozycje, test edycji
dist/                  ZIP-y motywu potomnego (gdp-child-A/B/C.zip; gdp-child.zip = B)
```

## Budowanie i weryfikacja

Wymagania: Python 3.10+, `zip`. PHP nie jest potrzebne do budowania.

```bash
python3 scripts/build-theme-json.py     # tokens.json → theme/variants/*/theme.json + config/theme_mods_*.json
python3 scripts/build-wxr.py            # content/ → content/site.wxr
bash    scripts/build-theme-zip.sh      # theme/ → dist/gdp-child-{A,B,C}.zip
python3 scripts/verify-blocks.py        # kontrola bloków (sekcja 13.1) + docs/open-items.generated.md
python3 scripts/validate-blueprints.py  # kontrola strukturalna blueprintów (sekcja 13.2, część statyczna)
```

Kolejność ma znaczenie: po zmianie `config/tokens.json` uruchom kolejno build-theme-json, build-theme-zip;
po zmianie treści w `content/` uruchom build-wxr i verify-blocks.

Skrypt `scripts/playground-setup.php` uruchamia się wewnątrz WordPressa (krok `runPHP` blueprintu
lub `wp eval-file` w etapie 2): ustawia theme_mods Blocksy, lokalizacje menu, stronę główną,
widgety stopki, permalinki (`/wiedza/%postname%/`, baza kategorii `wiedza/kategoria`) i mapuje ID kategorii (21–26 z WXR) w pętlach zapytań.

## Edycja treści

- Treść stron: `content/pages/<slug>.html`. Pierwszy komentarz HTML zawiera `Tytuł:`, `slug:`, `rodzic:`.
- Treść artykułów: `content/posts/<slug>.html`; nagłówek zawiera `Tytuł:`, `Kategoria:` (slug z listy w `build-wxr.py`), `Skrót:`.
  Odwołania do wzorców zsynchronizowanych: `{{ref:slug-wzorca}}`; do kategorii: `{{term:komentarz-rynkowy}}`.
- Wzorce zsynchronizowane: `content/blocks/<slug>.html` (jedno źródło prawdy dla CTA, slotów, zastrzeżenia cen, FAQ).
- Sloty modułów (upload faktury, tabela cen, kalkulator, analiza umowy, formularz doradcy) mają docelowe
  wymiary i klasę `gdp-slot`; etap 4 podmieni je 1:1 na bloki dynamiczne `pbm/*`.
- Placeholdery `[[ ]]` zostają w treści dosłownie do czasu uzupełnienia przez zleceniodawcę (`docs/open-items.md`).

## Procedura etapu 2 (staging przez WP-CLI)

1. Zainstaluj WordPress na stagingu (`wp core install`), włącz `noindex` i HTTP auth.
2. Sklonuj repozytorium na serwer i zbuduj artefakty (sekcja „Budowanie”).
3. Uruchom `REPO=/sciezka/repo VARIANT=<A|B|C> WP_PATH=/sciezka/wp bash scripts/restore-on-host.sh`.
   Skrypt instaluje Blocksy i `gdp-child`, importuje `content/site.wxr` (tymczasowo przez wordpress-importer,
   który po imporcie usuwa), stosuje `playground-setup.php`, ustawia opcje witryny i tworzy konto `redaktor`.
4. Wykonaj test edycji (`docs/test-edycji.md`).
5. Po ręcznych zmianach w Customizerze wyeksportuj je do repozytorium:
   `wp eval-file scripts/export-theme-mods.php > config/theme_mods_<X>.json` i zatwierdź w git.
6. Wtyczki z listy licencyjnej instaluje się dopiero w etapie 2 po decyzji zleceniodawcy; prototyp ich nie wymaga.

## Tagi

- `etap1-A`, `etap1-B`, `etap1-C` — punkt kontrolny P1.1 (trzy kierunki wizualne, ten sam commit).
- `etap1-v0.1` — P1.2, pełny prototyp (blueprint `main.json`).
- Kolejne: `etap1-v0.x` (iteracje), `etap1-final` (P1.4).

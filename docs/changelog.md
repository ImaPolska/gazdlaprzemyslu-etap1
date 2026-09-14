# Changelog

## etap1-A / etap1-B / etap1-C – 2026-09-13 (P1.1 Kierunki)

Dodano
- Motyw potomny `gdp-child` (Template: blocksy): `theme.base.json` + trzy warianty tokenów (`variants/A|B|C/tokens.json`) → generowany `theme.json`; `style.css` (komponenty: hero, karty, etykiety, kroki, tabele, FAQ, atrapy formularzy, stopka, nagłówek sticky/shrink), `functions.php` (enqueue, kategoria wzorców `gdp`, blokady dla roli Editor, lista dozwolonych bloków `core/*`, wyłączenie Google Fonts, polskie etykiety Blocksy), `assets/js/header.js`, fonty WOFF2 self-hosted.
- 8 wzorców niezsynchronizowanych (`patterns/*.php`): hero produktu, jak to działa, dla kogo, ryzyka i ograniczenia, przykład liczbowy, tabela porównawcza, nagłówek artykułu, źródła.
- 10 wzorców zsynchronizowanych (`wp_block`): CTA wgraj fakturę, sloty (upload faktury, kalkulator wypowiedzenia, analiza umowy, formularz doradcy), segmenty, pasek zaufania, FAQ produktu, tabela cen, zastrzeżenie cen.
- Treść: strona główna (3 warianty hero), `/oferta/cena-stala/`, 21 stron zastępczych dla pozostałych URL mapy serwisu, 6 kategorii, 2 wpisy-szablony komentarza rynkowego; manifest `content/pages.json`.
- Konfiguracja: `config/menus.json` (menu główne z rozwijanymi Oferta/Narzędzia, menu prawne), `config/footer.json` (4 kolumny + wiersz danych podmiotu z zastrzeżeniem), `config/theme_mods_A|B|C.json` (generowane).
- Blueprinty `blueprints/A|B|C.json` (produkcyjne, `--base` na tag) i `blueprints/dev/*.json` (lokalne, z `WP_DEBUG_LOG`).
- Skrypty: `build-all.sh`, `build-theme.py`/`build-theme-zip.sh`, `build-wxr.py`, `build-theme-mods.py`, `build-blueprints.py`, `apply-theme-mods.php`, `apply-config.php`, `export-theme-mods.php`, `restore-on-host.sh` (szkic etapu 2), `verify-blocks.py` (13.1), `verify-blueprint.py` (13.2 schemat), `verify-http.py` (13.2 HTTP + debug.log), `verify-editor.py` (ostrzeżenia edytora), `open-items.py` (13.6), `screenshot.py`, `dev-files.sh`, `dev-server.sh`, `qa-direction.sh`.
- Dokumentacja: `docs/decisions.md`, `docs/open-items.md`, `docs/verify/*.json`, `docs/screens/*.png` (12 zrzutów).

Założenia (szczegóły w `docs/decisions.md`)
- D1–D18, w tym: theme.json jako źródło tokenów, brak Companion, jeden motyw z trzema wariantami, treść wspólna poza hero, menu/stopka odtwarzane z JSON, h1 w treści, stuby dla całej mapy, `/komentarz-rynkowy/` jako strona z Query Loop, pl_PL przez `setSiteLanguage`.

Naprawiono w trakcie QA
- Niewidoczne theme mods po `runPHP` – Blocksy trzyma wygenerowany CSS w transientcie `blocksy_dynamic_styles_descriptor`; usuwany po zapisie.
- Tło stopki – opcje poziomu stopki muszą leżeć w `footer_placements.sections[0].settings`.
- Nagłówki i etykiety w sekcjach ciemnych i w stopce dziedziczą jasny kolor; linki w białych kartach na ciemnym tle w kolorze akcentu.
- Tabele: bez `has-fixed-layout`, przewijanie poziome na mobile, mono tylko w kolumnach liczbowych.
- `/wiedza/` bez h1 – włączony hero Blocksy tylko dla archiwum bloga.
- Zdublowany pasek liczb w hero A – usunięty (zostaje synchronizowany „Pasek zaufania”).
- Pasek górny (C): link do komentarza dziedziczy jasny kolor tekstu; hover w kolorze secondary.
- Język instalacji pl_PL (`setSiteLanguage`) + polskie etykiety Blocksy filtrem `gettext_blocksy`.
- Test publicznych linków Playground dla A/B/C: `docs/verify/public-links.md`.

## 2026-09-14 – P1.2 w toku: pełna treść stron i artykuły (kierunek A)
Dodano
- Pełna treść 21 stron dotąd zastępczych (oferta ×6, ceny orientacyjne, wgraj fakturę, kalkulator, analiza umowy, dla kogo / przemysł / MŚP, dla doradców, dla agentów AI, wiedza, komentarz rynkowy, o nas, dokumenty, kontakt, polityka prywatności, regulamin) – każda jako sekwencja sekcji `core/group` (`metadata.name` po polsku, `templateLock: contentOnly`), z leadem-odpowiedzią ≤ 60 słów, tabelami z `<thead>`, FAQ (`core/details`), źródłami i CTA.
- 5 artykułów bazy wiedzy (`/wiedza/<slug>/`): jak zmienić sprzedawcę gazu w firmie; okres wypowiedzenia i klauzula prolongacyjna; sprzedaż rezerwowa gazu; cena stała czy indeksowana do TGE; art. 4j ust. 3b PE dla MŚP – każdy z leadem ≤ 60 słów, spisem treści z kotwicami, tabelami, sekcją „Źródła”, datą aktualizacji `[[data]]`, autorem `[[ ]]`, CTA. 2 szablony komentarza rynkowego przebudowane (tabela notowań, decyzje, „Co to znaczy dla Twojej umowy”, zastrzeżenie cen).
- Biblioteka `scripts/gdp_blocks.py`, źródła `content/src/*.py`, generator `scripts/build-pages.py` (w `build-all.sh` przed WXR); `screenshot.py` czyta adresy z manifestu; `verify-http.py` sprawdza wpisy pod `/wiedza/`.
- Użytkownik `autor` z nazwą `[[Imię i nazwisko autora]]` jako autor wpisów (D25).
Zmieniono
- `permalink_structure = /wiedza/%postname%/`, `/wiedza/` zwykłą stroną, `category_base = category` (D21).
- `.gdp-karta`: pełna wysokość tylko dla kart-kolumn (D23); tabele 4+ kolumn `alignwide`.
Naprawiono
- Przyklejony nagłówek nie działał (Blocksy `#header { position: relative }` wygrywało ze `.ct-header { position: sticky }`), a przy pasku admina reguła `top: 32px` przesuwała nagłówek na treść – podniesiona specyficzność (`#header.ct-header`).
- Wpisy: odstęp nad tytułem w hero Blocksy; `scroll-margin-top` dla kotwic spisu treści pod przyklejonym nagłówkiem.
- `verify-editor.py`: czeka na `domcontentloaded` zamiast `networkidle` (edytor cyklicznie odpytuje REST, więc test nigdy nie kończył się).
- Decyzje D21–D25; `docs/open-items.md` przegenerowane (118 unikalnych placeholderów).

## 2026-09-14 – publikacja
- Repozytorium publiczne `ImaPolska/gazdlaprzemyslu-etap1`; blueprinty A/B/C przebudowane na adresy `raw.githubusercontent.com` tagów `etap1-A/B/C`.
- Decyzja zleceniodawcy: kierunek A (D19).

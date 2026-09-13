# Decyzje projektowe (etap 1)

Każda decyzja przyjęta bez pytania zleceniodawcy. Format: data, decyzja, uzasadnienie, jak odwrócić.

## 2026-09-13 — P1.0

### D-01 Podział ustawień: theme.json vs Customizer Blocksy
Decyzja: typografia, paleta i odstępy edytora trafiają do `theme.json` motywu potomnego (tokeny z `config/tokens.json`);
układ nagłówka/stopki, menu, przycisk CTA w nagłówku, kolory nagłówka i stopki — do `theme_mods` Blocksy
(`config/theme_mods_<X>.json`, stosowane przez `scripts/playground-setup.php`).
Uzasadnienie: Blocksy free steruje nagłówkiem i stopką wyłącznie przez Customizer; edytor bloków czyta wyłącznie `theme.json`.
Jedno źródło tokenów (`tokens.json`) generuje oba pliki, więc kolory nie rozjeżdżają się.
Odwrócenie: zmiana tokenów i ponowne `build-theme-json.py`.

### D-02 Fonty systemowe, bez Google Fonts
Decyzja: stosy systemowe (`system-ui`, `Georgia` w kierunku C, `ui-monospace` dla liczb w A). `assets/fonts/fonts.css` zawiera tylko komentarz.
Uzasadnienie: kryterium 13.5 (brak hostów zewnętrznych) i brak decyzji zleceniodawcy o kroju firmowym (open-items #1).
Odwrócenie: dodanie plików WOFF2 do `assets/fonts/` i deklaracji `@font-face`; zmiana `fontFamilies` w tokenach.

### D-03 Bez Blocksy Companion
Decyzja: prototyp nie instaluje Blocksy Companion ani żadnej wtyczki.
Uzasadnienie: wymóg „zero wtyczek”; wszystkie potrzebne funkcje (nagłówek, stopka, menu, przycisk) są w motywie Blocksy free.
Skutek: widgety stopki to widgety blokowe WordPressa zapisane w opcjach (`config/widgets.json`), nie elementy Companion.

### D-04 Repozytorium: lokalny git serwowany statycznie zamiast GitHub
Decyzja: repozytorium git jest udostępnione jako katalog statyczny pod adresem
`https://160b0be17-8080.na112.preview.abacusai.app`; blueprinty pobierają z niego ZIP-y motywu, WXR i skrypt PHP.
Uzasadnienie: brak potwierdzenia, czy zleceniodawca ma konto GitHub (open-items #6). Struktura repo nie zależy od hostingu;
przeniesienie na GitHub wymaga tylko zmiany adresu bazowego w `blueprints/*.json` (raw.githubusercontent.com na tagu).

### D-05 Korekty kontrastu palet roboczych
Decyzja: kolory akcentów dobrano tak, aby tekst na przyciskach i linki spełniały WCAG AA (≥ 4,5:1):
- A: akcent ceglasty `#bf4600` na białym — 5,13:1 (biały tekst na akcencie — 5,13:1);
- B: turkusowy akcent jest jasny, dlatego tekst przycisków jest ciemny `#0d1b2a` na turkusie — 7,43:1; linki w treści `#0d47a1`;
- C: zielony `#1b5e20` na białym — 7,87:1.
Odwrócenie: po otrzymaniu kolorów firmowych (open-items #1) podmiana w `tokens.json` i ponowny pomiar kontrastu.

### D-06 Stałe ID w WXR
Decyzja: strony (101–104), wpisy (201–202) i wzorce (9001–9010) mają stałe ID w `content/site.wxr`; odwołania `core/block ref` wskazują te ID.
Uzasadnienie: importer WordPressa zachowuje `post_id` z WXR, jeśli jest wolne (po `wp site empty` zawsze jest). ID terminów importer
nadaje na nowo, więc kategoria „Komentarz rynkowy” w bloku Query Loop jest poprawiana po imporcie w `playground-setup.php`.

### D-07 Menu w Blocksy przez `blocksy_location`
Decyzja: elementy menu w nagłówku, menu mobilnym i stopce mają wartość `menu: blocksy_location`; przypisanie konkretnego menu
odbywa się przez `nav_menu_locations` (menu_1, menu_mobile, footer) po slugu menu (`glowne`, `prawne`).
Uzasadnienie: ID menu różni się między instalacjami; slug jest stabilny.

### D-08 Blueprint: `wp site empty` przed importem
Decyzja: blueprint usuwa domyślną treść WordPressa („Witaj, świecie”, „Przykładowa strona”) przed importem WXR.
Uzasadnienie: czysty zestaw stron; ID 101+ na pewno wolne.

### D-09 Prototyp bez indeksowania
Decyzja: `blog_public = 0`, komentarze wyłączone.
Uzasadnienie: Playground i staging nie mają być indeksowane; produkcja włączy indeksowanie w etapie 3.

### D-10 Autor wpisów
Decyzja: wpisy podpisane placeholderem „Zespół analiz PBM” (autor `admin`, display name).
Uzasadnienie: open-items #3; zmiana nazwy wyświetlanej nie wymaga zmiany treści.

### D-11 Walidacja blueprintów
Decyzja: zamiast pełnej walidacji JSON Schema wykonywana jest kontrola strukturalna (`scripts/validate-blueprints.py`:
nazwy kroków, wymagane pola, istnienie plików, do których odwołują się URL-e).
Uzasadnienie: oficjalny schemat Playground nie przechodzi kontroli metaschematem Draft 2020-12 w bibliotece python-jsonschema
(błąd w definicjach V2 schematu, nie w blueprintach). Test uruchomieniowy (headless, HTTP 200 dla mapy URL, `debug.log`)
pozostaje do wykonania w P1.2 — w środowisku budowania nie ma PHP ani przeglądarki headless.

### D-12 Zakres treści w P1.1
Decyzja: w P1.1 istnieją strony `/` (start), `/oferta/`, `/oferta/cena-stala/`, `/wiedza/` oraz dwa komentarze rynkowe;
pozostałe strony z tabeli 8.1 (ceny orientacyjne, kalkulator, analiza umowy, o nas, kontakt, wgraj fakturę, strony prawne)
powstają w P1.2. Linki do nich w menu i stopce są już obecne (struktura URL jest ustalona).
Uzasadnienie: P1.1 służy wyborowi kierunku wizualnego; pełna treść to P1.2.

### D-13 Szablon 404.php w motywie potomnym
Decyzja: motyw potomny zawiera `404.php` (nadpisanie szablonu Blocksy) — krótki tekst i dwa przyciski (start, oferta), bez stylów inline.
Uzasadnienie: Blocksy free jest motywem klasycznym, więc strona błędu nie jest edytowalna blokami; jeden plik PHP z markupem bloków
jest mniejszym odstępstwem niż wtyczka lub strona „404” podpięta filtrem. Treść jest statyczna i nie podlega edycji redaktora (odnotowane w open-items).

### D-14 Struktura adresów treści Wiedzy
Decyzja: permalinki wpisów `/wiedza/%postname%/`, baza kategorii `wiedza/kategoria` (archiwum `/wiedza/kategoria/<slug>/`).
`/wiedza/` jest zwykłą stroną z Query Loop (nie `page_for_posts`), `/komentarz-rynkowy/` jest stroną (ID 123) z Query Loop
ograniczonym do kategorii i slotem subskrypcji; właściwe archiwum kategorii to `/wiedza/kategoria/komentarz-rynkowy/`.
Uzasadnienie: mapa 8.1 wymaga adresów `/wiedza/<slug>/` i osobnego `/komentarz-rynkowy/`; strona zamiast archiwum daje redaktorowi
edytowalny wstęp i slot formularza bez szablonu PHP.

### D-15 Stałe identyfikatory w WXR i mapowanie kategorii
Decyzja: strony mają ID 101–123, wpisy 201–207, kategorie 21–26 w pliku WXR (`scripts/build-wxr.py`). Importer WordPressa nadaje
kategoriom własne ID, dlatego `playground-setup.php` (krok 5) przepisuje `"taxQuery":{"category":[21..26]}` w blokach Query Loop
na realne ID po imporcie.
Uzasadnienie: stałe ID pozwalają odwoływać się do stron i kategorii w treści (menu, Query Loop) bez zależności od kolejności importu.

### D-16 Kierunek B jako bazowy blueprint `main.json`
Decyzja: `blueprints/main.json` powstaje z `B.json` (kierunek „Energetyczny”), `dist/gdp-child.zip` = wariant B; blueprinty A/C
pozostają dostępne do porównania.
Uzasadnienie: wskazanie zleceniodawcy dla P1.2; zmiana kierunku to podmiana jednego ZIP-a i `theme_mods`, bez zmian w treści.

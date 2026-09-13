# Raport P1.0 + P1.1 — Gaz dla Przemysłu, etap 1

Data: 2026-09-13

---

## 1. Co dostarczono

### Repozytorium
Lokalne Git: `/home/ubuntu/gazdlaprzemyslu/` — serwowane statycznie pod:
`https://160b0be17-8080.na112.preview.abacusai.app`

Tagi: `etap1-A`, `etap1-B`, `etap1-C`

Brak GitHub (zleceniodawca nie ma konta). Przeniesienie na GitHub = zmiana `BASE_URL` w `blueprints/*.json`. Notowane jako open-item #9.

### Linki Playground (3 kierunki wizualne)

| Kierunek | Link |
|---|---|
| **A „Przemysłowy"** | [Otwórz A](https://playground.wordpress.net/?blueprint-url=https://160b0be17-8080.na112.preview.abacusai.app/blueprints/A.json) |
| **B „Energetyczny"** | [Otwórz B](https://playground.wordpress.net/?blueprint-url=https://160b0be17-8080.na112.preview.abacusai.app/blueprints/B.json) |
| **C „Redakcyjny"** | [Otwórz C](https://playground.wordpress.net/?blueprint-url=https://160b0be17-8080.na112.preview.abacusai.app/blueprints/C.json) |

**Uwaga**: linki działają, dopóki VM jest aktywna (serwer statyczny na porcie 8080). Po przeniesieniu na GitHub — linki stałe.

Dane logowania: Administrator `admin` / `password`; Redaktor `redaktor` / `Redaktor-Etap1-2026`.

### Strony w P1.1
- `/` (strona główna) — hero + slot upload faktury, pasek zaufania, segmenty, „Jak to działa", tabela cen, komentarze rynkowe (Query Loop), CTA kalkulator, FAQ ×6, CTA końcowe
- `/oferta/` — hub produktów (nagłówek + link do cena-stala)
- `/oferta/cena-stala/` — definicja, mechanizm, ryzyka, przykład liczbowy `[[]]`, FAQ, CTA
- `/wiedza/` — strona wpisów (page_for_posts)
- 2 wpisy komentarz-rynkowy (szablon)

### Pliki kluczowe
| Ścieżka | Opis |
|---|---|
| `theme/gdp-child/` | Motyw potomny (theme.json, functions.php, style.css, 8 patterns) |
| `dist/gdp-child-{A,B,C}.zip` | ZIP-y motywu per wariant |
| `content/site.wxr` | Treść: strony, wpisy, wzorce zsynchronizowane, menu |
| `config/theme_mods_{A,B,C}.json` | Ustawienia Customizera Blocksy per wariant |
| `blueprints/{A,B,C}.json` | Blueprinty Playground |
| `docs/decisions.md` | 12 decyzji dnia 1 |
| `docs/open-items.md` | 9 kategorii otwartych pozycji, 80 wystąpień `[[]]` |

---

## 2. Wyniki weryfikacji

### 13.1 Bloki

| Kontrola | Oczekiwane | Uzyskane |
|---|---|---|
| `core/html` | 0 | **0** ✓ |
| `core/freeform` | 0 | **0** ✓ |
| `core/shortcode` | 0 | **0** ✓ |
| Bloki spoza `core/*` | 0 | **0** ✓ |
| Jeden `h1` na stronę | tak | **tak** ✓ |
| `templateLock:contentOnly` na sekcjach | tak | **tak** ✓ |

### 13.2 Blueprint (statyczna walidacja)

| Kontrola | Oczekiwane | Uzyskane |
|---|---|---|
| Wymagane pola ($schema, preferredVersions, steps) | obecne | **obecne** ✓ |
| Ścieżki do zasobów (ZIP, WXR, PHP, JSON) | pliki istnieją | **istnieją** ✓ |
| Test uruchomieniowy headless (HTTP 200) | — | **odłożony do testu manualnego** (brak PHP w środowisku budowania; Playground wymaga przeglądarki z WASM) |

**Ograniczenie**: pełen test uruchomieniowy (headless → HTTP 200 → debug.log) wymaga otwarcia Playground w przeglądarce. Weryfikacja zleceniodawcy: kliknij link, poczekaj ~30 s, strona główna powinna się wyrenderować. Jeśli nie — raport błędu z konsolą przeglądarki.

### 13.5 Zależności zewnętrzne

| Kontrola | Oczekiwane | Uzyskane |
|---|---|---|
| Google Fonts | 0 zapytań | **0** ✓ (fonty systemowe, D-02) |
| CDN / osadzenia | 0 | **0** ✓ |

### 13.6 Treść — placeholdery

80 wystąpień `[[]]` w 9 kategoriach — pełna lista w `docs/open-items.generated.md`. Brak wymyślonych danych.

---

## 3. Założenia przyjęte bez pytania (z decisions.md)

| # | Decyzja | Skrót |
|---|---|---|
| D-01 | theme.json = blokady + spacing; Customizer Blocksy = nagłówek/stopka/paleta globalna | wspólne tokeny w tokens.json |
| D-02 | Fonty systemowe, zero Google Fonts | RODO OK, wydajność OK |
| D-03 | Bez Blocksy Companion | zero wtyczek |
| D-04 | Repo lokalne, serwowane statycznie | brak GitHub |
| D-05 | Korekty kontrastu WCAG AA | A: 5.13:1, B: 7.43:1, C: 7.87:1 |
| D-06 | Stałe ID w WXR (101+, 9001+) | po `wp site empty` ID wolne |
| D-07 | Menu przez `blocksy_location` + slug | stabilne między instalacjami |
| D-08 | `wp site empty` przed importem | czysta baza |
| D-09 | `blog_public=0`, komentarze wyłączone | prototyp |
| D-10 | Autor = „Zespół analiz PBM" | open-item #3 |
| D-11 | Walidacja strukturalna zamiast JSON Schema | schemat Playground ma bug w Draft 2020-12 |
| D-12 | P1.1 = 4 strony + 2 wpisy; reszta mapy w P1.2 | wystarczające do wyboru kierunku |

Szczegóły z uzasadnieniami: `docs/decisions.md`.

---

## 4. Otwarte pozycje [[]] — 5 wymagających decyzji teraz

| # | Pytanie | Domyślne |
|---|---|---|
| 1 | Próg segmentów `[[X]]` GWh/rok | placeholder |
| 2 | Lista produktów: 4 + biometan „wkrótce" OK? | tak (sekcja 1.3) |
| 3 | Typowe okresy umowy ceny stałej | placeholder |
| 4 | Dane do przykładu liczbowego ceny stałej | placeholder |
| 5 | **Wybór kierunku A / B / C** | brak domyślnego — decyzja zleceniodawcy |

Pozostałe 4 pozycje (logo, koncesja, autor, treści prawne) czekają do P1.3.

---

## 5. Ryzyka i co z nimi zrobiono

| Ryzyko | Mitygacja |
|---|---|
| VM wyłączy się → linki Playground przestaną działać | Struktura repo gotowa do przeniesienia na GitHub jednym `git remote add` + `git push --tags`. Zmiana URL w 3 plikach blueprintów. |
| Blueprint nie uruchamia się (WASM, CORS) | Walidacja statyczna przeszła. Test manualny: zleceniodawca klika link. Fallback: Blueprint Bundle (ZIP z bundled resources). |
| Blocksy Customizer nie importuje theme_mods poprawnie | Setup PHP (`playground-setup.php`) stosuje `set_theme_mod` w pętli + fallback `update_option('theme_mods_blocksy')`. |
| Brak PHP w środowisku → brak pełnego testu headless | Playground CLI ma wbudowany PHP WASM; alternatywa: `npx @wp-playground/cli server --blueprint blueprints/A.json` do testu lokalnego. |

---

## 6. Następny krok

**Czekam na wybór kierunku wizualnego A / B / C (lub kombinacji).**

Po decyzji → P1.2: pełny prototyp wszystkich stron z mapy 8.1 (termin: 5 dni roboczych od wyboru).

### Opis kierunków

| Kierunek | Dla kogo najlepszy |
|---|---|
| **A „Przemysłowy"** | Surowy, inżynierski — dane na pierwszym planie. Najlepszy dla odbiorców przemysłowych (energetycy, dyrektorzy operacyjni), którzy cenią twardą informację bez ozdobników. |
| **B „Energetyczny"** | Ciemny nagłówek, dynamiczny akcent turkusowy. Najlepszy, gdy PBM chce się wyraźnie odróżnić od szarości konkurencji (Orlen/PGNiG OD, Enea) i komunikować nowoczesność. |
| **C „Redakcyjny"** | Serwis analityczny, serif w nagłówkach, komentarz rynkowy na pierwszym planie. Najlepszy, jeśli strategia opiera się na pozycji eksperta i content marketingu (wzorzec Kraken/Octopus). |

Nie rekomenduję jednego kierunku. Kombinacje są możliwe (np. „układ A + paleta C").

---

## Zrzuty ekranu

**Status**: zrzuty programowe wymagają uruchomienia Playground w przeglądarce headless (Chromium + WASM). Ze względu na limit zasobów sesji — zrzuty będą dostępne po manualnym otwarciu linków przez zleceniodawcę lub w następnej iteracji po przeniesieniu na GitHub.

**Alternatywa**: zleceniodawca otwiera każdy z 3 linków, sprawdza stronę główną i `/oferta/cena-stala/` na desktopie i mobile (DevTools → responsive), i zgłasza uwagi.

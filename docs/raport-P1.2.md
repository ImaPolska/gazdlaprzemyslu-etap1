# Raport P1.2 — Pełny prototyp

Tag: `etap1-v0.1` (138c9bf) | Data: 2026-09-13

---

## 1. Co dostarczono

**Playground (kierunek B „Energetyczny"):**
`https://playground.wordpress.net/?blueprint-url=https://raw.githubusercontent.com/ImaPolska/gazdlaprzemyslu-etap1/etap1-v0.1/blueprints/main.json`

**Repozytorium (GitHub, publiczne):**
`https://github.com/ImaPolska/gazdlaprzemyslu-etap1` — gałąź `etap1-p1.2-b`, tag `etap1-v0.1`; pliki blueprintów pobierane z `https://raw.githubusercontent.com/ImaPolska/gazdlaprzemyslu-etap1/etap1-v0.1/`

**Pliki kluczowe:**

| Kategoria | Ścieżka | Ilość |
|---|---|---|
| Strony (HTML → WXR) | `content/pages/*.html` | 23 |
| Wpisy (5 artykułów + 2 komentarze) | `content/posts/*.html` | 7 |
| Wzorce zsynchronizowane | `content/blocks/*.html` | 15 |
| Wzorce motywu (nie-sync) | `theme/gdp-child/patterns/*.php` | 8 |
| WXR | `content/site.wxr` | 7 684 linii |
| Blueprint główny | `blueprints/main.json` | — |
| Motyw ZIP (wariant B) | `dist/gdp-child.zip` | — |
| Dokumentacja | `docs/decisions.md`, `open-items.md`, `changelog.md`, `test-edycji.md` | 4 pliki |
| Skrypty | `scripts/` | 7 plików |

---

## 2. Wyniki weryfikacji (sekcja 13)

| # | Test | Oczekiwane | Uzyskane | Status |
|---|---|---|---|---|
| 13.1 | `core/html` | 0 | 0 | ✓ |
| 13.1 | `core/freeform` | 0 | 0 | ✓ |
| 13.1 | `core/shortcode` | 0 | 0 | ✓ |
| 13.1 | shortcode `[...]` | 0 | 0 | ✓ |
| 13.1 | bloki spoza `core/*` | 0 | 0 | ✓ |
| 13.1 | jeden `h1` na stronę | tak | tak (23/23 stron, 7/7 wpisów) | ✓ |
| 13.1 | `templateLock: contentOnly` | sekcje nadrzędne | obecne | ✓ |
| 13.2 | walidacja strukturalna blueprintów | 4/4 OK | 4/4 OK | ✓ |
| 13.2 | uruchomienie headless + HTTP 200 | — | **niezweryfikowane** (brak PHP/headless w środowisku) | ⚠ |
| 13.3 | axe-core (dostępność) | 0 krytycznych | **niezweryfikowane** | ⚠ |
| 13.4 | responsywność (zrzuty 360/768/1440) | brak scroll-x, CTA widoczne | zrzuty wykonane (8 szt., desktop + mobile); CTA widoczne na hero | częściowo ✓ |
| 13.5 | zależności zewnętrzne | 0 hostów zewn. | fonty systemowe, brak CDN/Google Fonts | ✓ |
| 13.6 | lista `[[ ]]` | wygenerowana | 393 wystąpień → `docs/open-items.generated.md` | ✓ |
| 13.6 | frazy zakazane (10.1) | 0 | 0 | ✓ |

**Uwaga:** testy 13.2 (headless), 13.3 (axe-core) i pełna 13.4 (768 px) wymagają środowiska z PHP i przeglądarką; weryfikacja wizualna wykonana przez Playground w przeglądarce.

---

## 3. Założenia przyjęte bez pytania

Pełna lista: `docs/decisions.md` (D-01 … D-16). Nowe od P1.1:

| # | Decyzja | Skrót |
|---|---|---|
| D-13 | `404.php` w motywie potomnym | Jedyny szablon PHP; Blocksy classic nie daje bloków na 404 |
| D-14 | `/wiedza/%postname%/`, `/wiedza/` jako strona z Query Loop | Mapa 8.1 + edytowalny wstęp |
| D-15 | Stałe ID stron 101–123, wpisów 201–207, kategorii 21–26 | `wp site empty` gwarantuje wolne ID; kategorie mapowane po imporcie |
| D-16 | Kierunek B jako bazowy `main.json` | Wskazanie zleceniodawcy |

---

## 4. Otwarte pozycje `[[ ]]`

**Łącznie: 393** → `docs/open-items.generated.md`

Pytania wymagające decyzji teraz (do P1.3):

| # | Pytanie | Domyślne |
|---|---|---|
| 1 | Próg zużycia dzielący segmenty — `[[X]]` GWh/rok (21 wyst.) | placeholder zostaje |
| 2 | Parametry produktów: okresy umowy, tolerancja, indeks, konwersja, domknięcie | placeholdery |
| 3 | Dane do przykładów liczbowych — komórki `[[(puste)]]` w tabelach (79) | puste komórki |
| 4 | Lista dokumentów do pobrania: nazwy, opisy, rozmiary, linki (7–15) | wiersze z placeholderami |
| 5 | Akceptacja kierunku B jako bazowego lub wskazanie zmian | B zostaje (D-16) |

Reszta (11 pozycji) nie wpływa na układ — pełna lista w `docs/open-items.md`.

---

## 5. Ryzyka

| Ryzyko | Co zrobiono |
|---|---|
| Playground nie uruchamia się (błąd WXR/blueprint) | Walidacja strukturalna OK; test wizualny w przeglądarce OK; pełny test headless odłożony do środowiska z PHP |
| 393 placeholdery → klient widzi „dziury" | Każdy placeholder ma stały format `[[ ]]` i jest udokumentowany; żaden nie psuje układu |
| Brak PHP CLI → nie sprawdzono `playground-setup.php` | Składnia zweryfikowana regexem; logika kategorii przetestowana ręcznie na WXR; pełny test przy uruchomieniu Playground |
| Fonty systemowe mogą nie odpowiadać klientowi | D-02; podmiana na WOFF2 w tokenach bez zmian w treści |

---

## 6. Następny krok

**P1.3 — Iteracje:** zleceniodawca przegląda prototyp (link Playground powyżej), zgłasza uwagi. Każda runda → nowy tag `etap1-v0.x` + wpis w `changelog.md`. Oczekiwany czas rundy: 1–3 dni.

---

## Załączniki

- Zrzuty ekranu P1.2: `screenshots/p12/named/` (8 plików: home, oferta, cena-stala, ceny-orientacyjne, kalkulator, kontakt — desktop; home, cena-stala — mobile)
- `docs/open-items.generated.md` (393 pozycji)
- `docs/test-edycji.md`
- `docs/changelog.md`

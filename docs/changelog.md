# Changelog

## P1.2 — 2026-09-13 — tag `etap1-v0.1`
- Pełny prototyp wszystkich stron z mapy 8.1 (23 strony): nowe `/wgraj-fakture/`, `/oferta/cena-indeksowana-tge/`, `/oferta/model-transzowy/`, `/oferta/umowa-kompleksowa-msp/`, `/oferta/biometan/` (wkrótce), `/ceny-orientacyjne/`, `/kalkulator-wypowiedzenia/`, `/analiza-umowy/`, `/dla-kogo/` (+ `/przemysl/`, `/msp/`), `/dla-doradcow/`, `/dla-agentow-ai/`, `/o-nas/`, `/dokumenty/`, `/kontakt/`, `/polityka-prywatnosci/`, `/regulamin/`, `/komentarz-rynkowy/`; przepisane huby `/oferta/` i `/wiedza/` (Query Loop, kategorie, pole szukania).
- Wiedza: 5 artykułów w 4 kategoriach (zmiana sprzedawcy, umowy i wypowiedzenia, sprzedaż rezerwowa, ceny i rynek) plus komentarz rynkowy i biometan/raportowanie — łącznie 6 kategorii (ID 21–26 w WXR, mapowane na realne ID w `playground-setup.php`).
- Struktura adresów: `/wiedza/%postname%/` dla wpisów, `/wiedza/kategoria/<slug>/` dla archiwów kategorii; `/wiedza/` jest zwykłą stroną (Query Loop), nie `page_for_posts`.
- `scripts/build-wxr.py`: słownik kategorii, ID stron 101–123 i wpisów 201–207, nagłówki `Kategoria:` / `Skrót:` w plikach wpisów.
- `blueprints/main.json` (kierunek B jako bazowy), walidacja 4 blueprintów OK; `dist/gdp-child.zip` = wariant B.
- Motyw: `404.php` (jedyny szablon PHP poza `functions.php`), nowe klasy CSS P1.2 w `style.css` (hero z formularzem, uwagi, „wkrótce”, sekcje formularzy, nagłówek artykułu, źródła, dokumenty, kontakt, kategorie, proces, kanał AI, 404).
- Weryfikacja: `verify-blocks.py` — same zera, każda strona ma jeden `h1`; WXR 59 pozycji (10 wp_block, 23 strony, 7 wpisów, 19 pozycji menu), 8 termów; 393 placeholdery `[[ ]]` w `docs/open-items.generated.md`; wszystkie linki wewnętrzne `href="/…"` prowadzą do istniejących adresów.
- Niezweryfikowane w środowisku budowania: składnia PHP `playground-setup.php` i `404.php` (brak PHP), uruchomienie Playground (brak przeglądarki headless).
- Dokumentacja: README, decisions (D-13…D-16), open-items, test-edycji.

## P1.1 — 2026-09-13 — tagi `etap1-A`, `etap1-B`, `etap1-C`
- Trzy kierunki wizualne: `theme/variants/{A,B,C}` (theme.json + variant.css), `config/theme_mods_{A,B,C}.json`, `dist/gdp-child-{A,B,C}.zip`.
- Blueprinty `blueprints/{A,B,C}.json`: pl_PL, Blocksy, gdp-child, import WXR, konfiguracja przez `playground-setup.php`, konto `redaktor`.
- Treść: strony start, oferta, cena-stala, wiedza; wpisy komentarz-rynkowy-1, -2; 10 wzorców zsynchronizowanych; 5 widgetów stopki; menu główne i prawne.
- Wzorce motywu (`patterns/*.php`, 8 szt., `templateLock: contentOnly`): hero produktu, jak to działa, dla kogo, ryzyka i ograniczenia, przykład liczbowy, tabela porównawcza, nagłówek artykułu, źródła.
- Weryfikacja 13.1: `scripts/verify-blocks.py` — same zera, każda strona ma jeden `h1`; 80 placeholderów `[[ ]]` w `docs/open-items.generated.md`.
- Weryfikacja 13.2 (część statyczna): `scripts/validate-blueprints.py` — OK dla A/B/C.
- Dokumentacja: README, decisions, open-items, test-edycji.

## P1.0 — 2026-09-13
- Inicjalizacja repozytorium, struktura katalogów wg sekcji 12 instrukcji.
- Tokeny projektowe `config/tokens.json`, generator `scripts/build-theme-json.py`.
- Motyw potomny `gdp-child` (style.css, functions.php, theme.json).
- Decyzje dnia 1: D-01…D-04 w `docs/decisions.md`.

- P1.1 (2026-09-13, uzupełnienie): warstwa wizualna – klasy CSS w blokach (gdp-hero, gdp-hero-form, gdp-trust-bar, gdp-segments/gdp-card, gdp-steps/gdp-step, gdp-price-table, gdp-faq, gdp-cta-final, gdp-surface, gdp-product-hero, gdp-section, gdp-risks, gdp-example), rozbudowany style.css, przepisane warianty A/B/C, płynna typografia (clamp) w theme.json; przebudowa WXR i ZIP.

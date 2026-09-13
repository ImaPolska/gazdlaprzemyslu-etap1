# Changelog

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

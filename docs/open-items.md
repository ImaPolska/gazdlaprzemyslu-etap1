# Otwarte pozycje `[[ ]]` i pytania do zleceniodawcy

Stan na 2026-09-13 (P1.1). Pełna, generowana lista wszystkich wystąpień z lokalizacją: `docs/open-items.generated.md`
(80 wystąpień; odtwarzasz ją poleceniem `python3 scripts/verify-blocks.py`).

## Pytania wymagające decyzji teraz (maks. 5)

| # | Pytanie | Gdzie w prototypie | Domyślne, jeśli brak odpowiedzi |
|---|---|---|---|
| 1 | Próg zużycia dzielący segmenty (GWh/rok) — wartość `[[X]]` | wzorzec segmentów, hero na stronie głównej, tabela porównawcza w `/oferta/`, FAQ | placeholder zostaje; nie wpływa na układ |
| 2 | Lista produktów: potwierdzenie czterech (cena stała, indeksowana, hybryda, spot) i biometanu „wkrótce” | `/oferta/`, menu główne, stopka „Oferta” | domyślne z sekcji 1.3 instrukcji |
| 3 | Typowe okresy umowy i tolerancja odbioru dla ceny stałej — `[[typowe okresy umowy]]`, `[[tolerancja]]` | `/oferta/cena-stala/` (mechanizm, FAQ) | placeholder zostaje |
| 4 | Przykład liczbowy dla ceny stałej: dane wejściowe do tabeli (wolumen, cena, okres) | `/oferta/cena-stala/` — sekcja „Przykład liczbowy” (9 pustych komórek) | tabela z `[[(puste)]]` |
| 5 | Wybór kierunku wizualnego A / B / C (lub kombinacji: np. układ A + kolory C) | całość | brak — decyzja P1.1 |

## Pozycje, które czekają (bez wpływu na P1.1)

| # | Pozycja | Wpływ, jeśli brak | Kiedy potrzebne |
|---|---|---|---|
| 1 | Logo i kolory firmowe PBM / „Gaz dla Przemysłu” | Palety robocze A/B/C, logo tekstowe | P1.3 |
| 2 | Numer koncesji OPG, dane rejestrowe PBM (adres, NIP, KRS, kapitał) | `[[ ]]` w stopce „Dane spółki” i `/o-nas/` | P1.3 |
| 3 | Autor komentarza rynkowego | Placeholder „Zespół analiz PBM” | P1.3 |
| 4 | Treści komentarzy rynkowych: `[[data]]`, `[[komentarz]]`, `[[od]]`–`[[do]]`, `[[jednostka]]` | Dwa artykuły w formacie docelowym z placeholderami | P1.2 (5 artykułów) |
| 5 | Treści prawne: polityka prywatności, regulamin, zgody RODO (`[[treść zgody dostarczy zleceniodawca]]` — 8 miejsc przy formularzach), okres retencji | Placeholdery | etap 3 |
| 6 | Weryfikacja prawna odwołań do Prawa energetycznego (`[[do weryfikacji prawnej: art. 4j ust. 3b …]]`) i link do tekstu jednolitego (isap) | Zaznaczone `[[ ]]` | P1.3 |
| 7 | Opis aktywów Grupy (źródła, magazyny, sieć) i zdjęcia (opcjonalnie) | Placeholdery jednolite | P1.3 |
| 8 | Model współpracy z doradcą, terminy odpowiedzi (`[[model współpracy]]`, `[[termin]]`) | Placeholdery w slotach | P1.2 |
| 9 | URL repozytorium: własne zleceniodawcy (GitHub) czy agenta | Repo agenta serwowane statycznie (D-04) | P1.0 — przyjęto domyślne |

## Zestawienie wystąpień wg placeholdera (80)

| Placeholder | Liczba | Znaczenie |
|---|---|---|
| `[[ ]]` | 51 | puste pole do uzupełnienia (komórki tabel, wartości liczbowe w slotach) |
| `[[X]]` | 15 | próg segmentu GWh/rok |
| `[[data]]` | 10 | data notowania / aktualizacji |
| `[[treść zgody dostarczy zleceniodawca]]` | 8 | RODO przy każdym formularzu |
| `[[komentarz]]`, `[[komentarz: …]]` | 14 | treść komentarza rynkowego |
| pozostałe (`[[Y]]`, `[[tytuł]]`, `[[od]]`, `[[do]]`, `[[termin]]`, `[[rok]]`, `[[jednostka]]`, `[[link]]`, `[[okres retencji]]`, `[[model współpracy]]`, prawne) | — | szczegóły w liście generowanej |

Uwaga: liczby w tabeli zestawienia liczą wystąpienia w plikach źródłowych `content/` (strony, wpisy, wzorce);
lista generowana liczy wystąpienia po rozwinięciu odwołań do wzorców, dlatego suma może się różnić od 80 — źródłem prawdy jest lista generowana.

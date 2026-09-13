# Otwarte pozycje `[[ ]]` i pytania do zleceniodawcy

Stan na 2026-09-13 (P1.2). Pełna, generowana lista wszystkich wystąpień z lokalizacją: `docs/open-items.generated.md`
(393 wystąpienia po rozwinięciu wzorców; odtwarzasz ją poleceniem `python3 scripts/verify-blocks.py`).

## Pytania wymagające decyzji teraz (maks. 5)

| # | Pytanie | Gdzie w prototypie | Domyślne, jeśli brak odpowiedzi |
|---|---|---|---|
| 1 | Próg zużycia dzielący segmenty (GWh/rok) — wartość `[[X]]` (21 wystąpień) | segmenty, hero, `/dla-kogo/`, `/przemysl/`, `/msp/`, tabela porównawcza w `/oferta/`, FAQ | placeholder zostaje; nie wpływa na układ |
| 2 | Parametry produktów: `[[typowe okresy umowy]]`, `[[tolerancja]]`, `[[nazwa indeksu]]`, `[[zasady konwersji]]`, `[[zasada domknięcia]]` | `/oferta/cena-stala/`, `/oferta/cena-indeksowana-tge/`, `/oferta/model-transzowy/`, `/oferta/umowa-kompleksowa-msp/` | placeholdery zostają |
| 3 | Dane do przykładów liczbowych (wolumen, cena, okres) — komórki `[[(puste)]]` w tabelach (79) | sekcje „Przykład liczbowy” na stronach produktów, tabela cen orientacyjnych, kalkulator | tabele z pustymi komórkami |
| 4 | Lista dokumentów do pobrania: nazwy plików, `[[opis dokumentu]]`, `[[rozmiar]]`, `[[link do PDF]]` (po 7–15) | `/dokumenty/`, stopka, `/wgraj-fakture/` | wiersze z placeholderami; struktura listy gotowa |
| 5 | Akceptacja kierunku B jako bazowego (`main.json`) lub wskazanie zmian (kolory, zaokrąglenia, typografia) | całość | B zostaje (D-16) |

## Pozycje, które czekają (bez wpływu na układ)

| # | Pozycja | Wpływ, jeśli brak | Kiedy potrzebne |
|---|---|---|---|
| 1 | Logo i kolory firmowe PBM / „Gaz dla Przemysłu” | Paleta robocza B, logo tekstowe | P1.3 |
| 2 | Numer koncesji OPG, dane rejestrowe PBM (adres, NIP, KRS, kapitał), dane kontaktowe (telefon, e-mail, godziny) | `[[ ]]` w stopce „Dane spółki”, `/o-nas/`, `/kontakt/`, `/regulamin/` | P1.3 |
| 3 | Autor komentarza rynkowego, `[[imię i nazwisko]]`, `[[rola: …]]` w zespole | Placeholder „Zespół analiz PBM”, lista zespołu w `/o-nas/` | P1.3 |
| 4 | Treści komentarzy rynkowych: `[[data]]` (37), `[[komentarz]]`, `[[od]]`–`[[do]]`, `[[jednostka]]`, `[[rok]]` | Dwa komentarze w formacie docelowym; strona `/komentarz-rynkowy/` z Query Loop | P1.3 |
| 5 | Treści prawne: polityka prywatności, regulamin (`[[treść dostarczy zleceniodawca]]` — 20), zgody RODO (`[[treść zgody dostarczy zleceniodawca]]` — 10 slotów formularzy), `[[okres retencji]]` | Placeholdery; struktura sekcji gotowa | etap 3 |
| 6 | Weryfikacja prawna odwołań do Prawa energetycznego (`[[do weryfikacji prawnej: …]]` — 39) i link do tekstu jednolitego (`[[link do tekstu jednolitego, isap.sejm.gov.pl]]` — 6) | Zaznaczone `[[ ]]` w artykułach Wiedzy i na stronach produktów | P1.3 |
| 7 | Opis aktywów Grupy IMA (źródła, magazyny, sieć) i zdjęcia (opcjonalnie) | Placeholdery jednolite w `/o-nas/` | P1.3 |
| 8 | Model współpracy z doradcą, terminy odpowiedzi (`[[model współpracy]]`, `[[termin]]` — 10), przykład kalkulacji prowizji | Placeholdery w `/dla-doradcow/`, slotach formularzy | P1.3 |
| 9 | Biometan: zakres oferty, terminy, zasady raportowania — bez obietnic; strona `/oferta/biometan/` oznaczona „wkrótce” | Strona informacyjna z placeholderami | etap 2 |
| 10 | Kanał dla agentów AI (`/dla-agentow-ai/`): zakres danych, format, warunki dostępu | Opis procesu z placeholderami | etap 2 |
| 11 | Treść strony 404 (`theme/gdp-child/404.php`) — statyczna, nie do edycji przez redaktora | Krótki tekst domyślny | P1.3 (jeśli inny tekst) |
| 12 | URL repozytorium: własne zleceniodawcy (GitHub) czy agenta | Repo agenta serwowane statycznie (D-04) | P1.0 — przyjęto domyślne |

## Zestawienie wystąpień wg placeholdera (393, lista generowana)

| Placeholder | Liczba | Znaczenie |
|---|---|---|
| `[[(puste)]]` | 79 | pusta komórka tabeli / wartość liczbowa w slocie |
| `[[data]]` | 37 | data notowania, aktualizacji tabeli cen, publikacji |
| `[[do weryfikacji prawnej]]`, `[[do weryfikacji prawnej: …]]` | 39 | odwołania do Prawa energetycznego i terminów ustawowych |
| `[[X]]` | 21 | próg segmentu GWh/rok |
| `[[treść dostarczy zleceniodawca]]` | 20 | sekcje prawne, opisy firmy |
| `[[rozmiar]]`, `[[link do PDF]]`, `[[opis dokumentu]]` | 37 | lista dokumentów |
| `[[treść zgody dostarczy zleceniodawca]]` | 10 | RODO przy każdym slocie formularza |
| `[[termin]]` | 10 | terminy odpowiedzi / realizacji |
| `[[tolerancja]]`, `[[typowe okresy umowy]]`, `[[nazwa indeksu]]`, `[[zasady konwersji]]` | 23 | parametry produktów |
| `[[okres retencji]]` | 6 | polityka prywatności, formularze |
| pozostałe (`[[od]]`, `[[do]]`, `[[rok]]`, `[[komentarz]]`, `[[link]]`, `[[imię i nazwisko]]`, `[[rola: …]]`, `[[przykład kalkulacji — …]]`, `[[model współpracy]]`, `[[lista operatorów z GUD-K]]`, `[[zasada domknięcia]]`, inne) | ok. 110 | szczegóły w liście generowanej |

Uwaga: liczby liczą wystąpienia po rozwinięciu odwołań do wzorców zsynchronizowanych (tak jak lista generowana), dlatego
placeholdery ze wzorców (np. RODO, zastrzeżenie cen) występują wielokrotnie — uzupełnienie wzorca uzupełnia je wszędzie naraz.

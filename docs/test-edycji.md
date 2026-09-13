# Test edycji dla zleceniodawcy (sekcja 14)

Test wykonujesz w instancji Playground uruchomionej z linku w `README.md`. Nie potrzebujesz znajomości WordPressa.
Zrzuty ekranu: `[[zrzut — do uzupełnienia po uruchomieniu Playground]]` (dodane w P1.2 po teście uruchomieniowym).

## Logowanie

1. W tej samej karcie, w której otworzyła się strona, dopisz do adresu `/wp-admin/` i naciśnij Enter.
2. Jeśli widzisz panel administratora, w prawym górnym rogu kliknij „Witaj, admin” → „Wyloguj się”.
3. Zaloguj się jako: login `redaktor`, hasło `Redaktor-Etap1-2026`.

## Operacja 1 — zmiana tekstu (oczekiwane: trzy kliknięcia)

1. W górnym pasku kliknij „Gaz dla Przemysłu” → „Odwiedź witrynę”, a na stronie głównej w górnym pasku kliknij „Edytuj stronę”.
2. Kliknij nagłówek w sekcji hero (największy tekst u góry). Kursor pojawi się w tekście — zmień treść.
3. Kliknij „Aktualizuj” w prawym górnym rogu. Otwórz stronę główną ponownie — nowy nagłówek jest widoczny.

Oczekiwane: żadnych pytań o układ, kolory ani szerokość. Jeśli edytor pyta o cokolwiek poza treścią, zgłoś to.

`[[zrzut — do uzupełnienia po uruchomieniu Playground]]`

## Operacja 2 — dodanie akapitu i tabeli 3×3 w artykule

1. Panel → „Wpisy” → „Jak zmienić sprzedawcę gazu w firmie: kolejność kroków i terminy” (kliknij tytuł).
2. Kliknij pod drugim nagłówkiem w treści (koniec akapitu) i naciśnij Enter — pojawia się nowy, pusty akapit. Wpisz zdanie.
3. Naciśnij Enter, wpisz `/tabela` i wybierz „Tabela”. Ustaw 3 kolumny, 3 wiersze → „Utwórz tabelę”. Wpisz cokolwiek w komórki.
4. Kliknij „Aktualizuj”. Otwórz artykuł na froncie.

Oczekiwane: tabela wygląda tak samo jak tabele istniejące (te same linie, odstępy, krój) bez ustawiania stylów.

`[[zrzut — do uzupełnienia po uruchomieniu Playground]]`

## Operacja 3 — próba zmiany układu

Jako `redaktor`:
1. Otwórz stronę główną do edycji. Kliknij w sekcję „Jak to działa” (dowolny jej element).
2. Spróbuj ją usunąć (menu z trzema kropkami → „Usuń”) albo przesunąć kolumny w hero (strzałki przy bloku).

Oczekiwane: opcje usunięcia sekcji i przesuwania kolumn nie są dostępne; możesz zmieniać wyłącznie tekst i obrazy w sekcjach.

Jako `admin` (wyloguj się, zaloguj `admin` / `password`):
3. Otwórz stronę główną do edycji. Kliknij sekcję „Jak to działa” → strzałki „w górę / w dół” przesuwają całą sekcję.
4. Spróbuj przesunąć kolumnę wewnątrz hero — nie da się, dopóki nie klikniesz ikony kłódki na sekcji i świadomie jej nie odblokujesz.

Oczekiwane: sekcje można przestawiać jako całość; wnętrze sekcji jest zablokowane (`templateLock: contentOnly`) do czasu odblokowania.

`[[zrzut — do uzupełnienia po uruchomieniu Playground]]`

## Operacja 4 (bonus) — propagacja wzorca „Zastrzeżenie cen”

Jako `admin`:
1. Panel → „Wygląd” → „Edytor” → „Wzorce” → „Moje wzorce” → „Zastrzeżenie cen” (albo: na dowolnej stronie kliknij blok zastrzeżenia → „Edytuj oryginał”).
2. Zmień jedno słowo w tekście zastrzeżenia (np. dopisz „(test)” na końcu). Kliknij „Zapisz”.
3. Sprawdź stronę główną, `/oferta/cena-stala/`, `/ceny-orientacyjne/` (slot tabeli cen) i stopkę.

Oczekiwane: zmieniony tekst jest widoczny wszędzie, gdzie występuje zastrzeżenie, bez edycji tych stron.

Po teście przywróć tekst pierwotny (krok 1–2, usuń dopisek) — wzorzec zastrzeżenia ma brzmienie ustalone w sekcji 10.4 instrukcji.

`[[zrzut — do uzupełnienia po uruchomieniu Playground]]`

## Wynik

Jeśli którakolwiek z operacji 1–3 wymagała więcej kroków niż opisano lub edytor zapytał o układ, etap 1 nie jest zakończony —
zgłoś, w którym kroku i co się pojawiło.

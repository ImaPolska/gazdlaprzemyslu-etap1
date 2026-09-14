# -*- coding: utf-8 -*-
"""Treść stron: narzędzia (M2, M3), segmenty, kanały (doradcy, agenci AI), wiedza, komentarz, o nas, dokumenty, kontakt, prawne."""
from gdp_blocks import *  # noqa

PAGES = {}

KOLEJNOSC = 'Skutki błędnego wypowiedzenia, czyli sprzedaż rezerwowa albo kary umowne, ponosi odbiorca. Dlatego PBM stosuje jedną kolejność: najpierw umowa z PBM, potem pełnomocnictwo, dopiero potem wypowiedzenie obecnej umowy w jej terminie i zgłoszenie zmiany sprzedawcy do operatora.'

# ---------------------------------------------------------------- /kalkulator-wypowiedzenia/
PAGES['kalkulator-wypowiedzenia'] = [
    hero('Kalkulator terminu wypowiedzenia umowy na gaz',
         'Kalkulator wylicza ostatni dzień, w którym możesz skutecznie złożyć wypowiedzenie albo sprzeciw wobec automatycznego przedłużenia, żeby umowa zakończyła się w planowanym terminie. Potrzebujesz trzech danych z umowy: daty jej końca, okresu wypowiedzenia i treści klauzuli prolongacyjnej. Wynik możesz zapisać jako przypomnienie.',
         [('Oblicz termin', '#kalkulator')], name='Nagłówek strony'),
    sec('Slot: kalkulator wypowiedzenia', h('Kalkulator', anchor='kalkulator', size='m'), ref('slot-kalkulator-wypowiedzenia')),
    sec('Skąd wziąć dane z umowy',
        h('Skąd wziąć dane z umowy'),
        table(['Dane', 'Gdzie szukać w umowie', 'Na co uważać'], [
            ['Data końca umowy', 'Paragraf „Okres obowiązywania” albo pierwsza strona umowy; czasem załącznik cenowy', 'Umowa może kończyć się z końcem roku gazowego (30 września), nie kalendarzowego [[do weryfikacji]]'],
            ['Okres wypowiedzenia', 'Paragraf „Rozwiązanie umowy” albo ogólne warunki umowy (OWU)', 'Liczony w miesiącach ze skutkiem na koniec miesiąca kalendarzowego albo w dniach; sprawdź, od kiedy biegnie'],
            ['Klauzula prolongacyjna', 'Zdanie o „automatycznym przedłużeniu” albo „przedłużeniu na kolejny okres, jeżeli żadna ze stron nie złoży oświadczenia”', 'Termin na sprzeciw bywa inny niż okres wypowiedzenia, np. 3 miesiące przed końcem umowy'],
            ['Forma oświadczenia', 'OWU albo paragraf o doręczeniach', 'Pisemna, czasem z podpisem osób reprezentujących; liczy się data doręczenia, nie wysłania'],
        ]),
        p('Nie masz umowy pod ręką? Wystarczy faktura: odczytamy z niej sprzedawcę i poprosimy o kopię umowy na kolejnym etapie. <a href="/analiza-umowy/">Prześlij umowę do analizy</a>, a wyliczymy termin za Ciebie.'),
        bg='surface'),
    sec('Ostrzeżenia prawne',
        h('Zanim złożysz wypowiedzenie'),
        ul(['Kalkulator pomaga zaplanować termin, ale nie zastępuje lektury umowy. Wynik zależy od poprawności wprowadzonych danych.',
            'Nie wypowiadaj umowy przed czasem. Umowa na czas oznaczony może przewidywać koszty wcześniejszego rozwiązania (art. 4j ust. 3a Prawa energetycznego).',
            'Liczy się data doręczenia oświadczenia sprzedawcy, nie data wysłania. Zachowaj potwierdzenie.',
            'Jeżeli umowa wygaśnie, a operator nie otrzyma zgłoszenia nowej umowy, trafisz do sprzedaży rezerwowej. Jej cena może być znacząco wyższa od rynkowej [[źródło: URE]].',
            KOLEJNOSC])),
    sec('CTA: analiza umowy',
        h('Wolisz, żebyśmy sprawdzili umowę za Ciebie'),
        p('Prześlij umowę. Odczytamy termin, okres wypowiedzenia i klauzulę prolongacyjną, a człowiek zweryfikuje wynik przed wysłaniem do Ciebie.'),
        buttons([('Prześlij umowę do analizy', '/analiza-umowy/'), ('Wgraj fakturę', '/wgraj-fakture/', True)]),
        bg='surface', pad='80'),
    sources([SRC['pe_4j'], SRC['kc'], SRC['ure']]),
]

# ---------------------------------------------------------------- /analiza-umowy/
PAGES['analiza-umowy'] = [
    hero('Analiza umowy na gaz: okno wyjścia i wypowiedzenie',
         'Prześlij obecną umowę na gaz, a odczytamy z niej termin obowiązywania, okres wypowiedzenia, klauzulę prolongacyjną, pasmo tolerancji wolumenu, koszty wcześniejszego rozwiązania i sprzedawcę rezerwowego. Wynik weryfikuje człowiek. Dostajesz kartę „okna wyjścia” i, jeśli zdecydujesz się na umowę z PBM, gotowe wypowiedzenie do złożenia we właściwym terminie.',
         [('Prześlij umowę', '#analiza')], name='Nagłówek strony'),
    sec('Slot: analiza umowy', h('Prześlij umowę', anchor='analiza', size='m'), ref('slot-analiza-umowy')),
    sec('Proces',
        h('Jak przebiega analiza'),
        steps([
            ('Przesyłasz umowę', 'PDF albo skan umowy z ogólnymi warunkami i załącznikiem cenowym.'),
            ('Odczytujemy sześć elementów', 'Termin, okres wypowiedzenia, klauzula prolongacyjna, tolerancja wolumenu, koszty wcześniejszego rozwiązania, sprzedawca rezerwowy.'),
            ('Weryfikacja przez człowieka', 'Specjalista PBM sprawdza odczyt z treścią umowy. Nic nie wychodzi do Ciebie bez tej weryfikacji.'),
            ('Karta okna wyjścia', 'Dostajesz jedną stronę z terminami i tym, co trzeba zrobić, żeby zmienić sprzedawcę bez kosztów i bez sprzedaży rezerwowej.'),
            ('Wypowiedzenie we właściwym terminie', 'Jeśli podpiszesz umowę z PBM i pełnomocnictwo, przygotujemy wypowiedzenie i złożymy je w terminie z karty. Nie wcześniej.'),
        ]),
        bg='surface'),
    sec('Co robimy i czego nie robimy',
        h('Co robimy i czego nie robimy'),
        two(
            [h3('Robimy'), check(['Odczytujemy i objaśniamy zapisy Twojej umowy', 'Wyliczamy terminy i pokazujemy, skąd wynikają', 'Weryfikujemy wynik przez człowieka przed wysłaniem', 'Składamy wypowiedzenie w terminie, na podstawie pełnomocnictwa, po podpisaniu umowy z PBM'])],
            [h3('Nie robimy'), ul(['Nie sugerujemy rozwiązania umowy przed czasem', 'Nie składamy wypowiedzenia bez podpisanej umowy z PBM i pełnomocnictwa', 'Nie świadczymy porad prawnych; w spornych zapisach rekomendujemy konsultację z prawnikiem', 'Nie przekazujemy Twojej umowy podmiotom trzecim'])],
        ),
        p(KOLEJNOSC)),
    sec('FAQ',
        h('Pytania o analizę umowy'),
        faq([
            ('Czy analiza jest płatna?', 'Nie. Analiza i karta okna wyjścia są bezpłatne i nie zobowiązują Cię do podpisania umowy.'),
            ('Ile trwa?', 'Wynik dostaniesz w ciągu [[czas]] roboczych od przesłania czytelnej umowy.'),
            ('Kto czyta moją umowę?', 'Narzędzie do ekstrakcji [[opis w etapie 4]] i specjalista PBM. Dokument przechowujemy przez [[okres retencji]], szczegóły w <a href="/polityka-prywatnosci/">polityce prywatności</a>.'),
            ('Co, jeśli w umowie są koszty wcześniejszego rozwiązania?', 'Pokażemy je na karcie i zaplanujemy zmianę sprzedawcy na termin, w którym nie występują.'),
        ]),
        bg='surface'),
    sources([SRC['pe_4j'], SRC['pe_5aa'], SRC['kc']]),
    cta_end(bg=None),
]

# ---------------------------------------------------------------- /dla-kogo/
PAGES['dla-kogo'] = [
    hero('Dla kogo jest Gaz dla Przemysłu',
         'Obsługujemy firmy, dla których gaz jest istotnym kosztem: od piekarni i suszarni po zakłady zużywające setki GWh rocznie. Ścieżka zależy od wolumenu. Mniejsza firma dostaje ofertę w 24 godziny bez wizyty handlowca, duży zakład dostaje opiekuna i model dopasowany do profilu produkcji.',
         None, name='Nagłówek strony'),
    sec('Segmenty', ref('wzorzec-segmenty')),
    sec('Porównanie ścieżek',
        h('Dwie ścieżki, jedna zasada'),
        table(['Element', 'MŚP (do [[X]] GWh rocznie)', 'Przemysł (powyżej [[X]] GWh rocznie)'], [
            ['Start', 'Wgranie faktury', 'Wgranie faktury albo rozmowa z opiekunem'],
            ['Oferta', 'W 24 godziny, e-mailem', 'Po analizie profilu, z rekomendacją modelu'],
            ['Modele ceny', 'Stała, indeksowana', 'Stała, indeksowana, transzowy'],
            ['Umowa', 'Kompleksowa albo sprzedaży', 'Sprzedaży, wiele punktów poboru'],
            ['Kontakt', 'E-mail, telefon na życzenie', 'Opiekun i zespół analiz'],
            ['Zasada wypowiedzenia', 'Najpierw umowa z PBM, potem wypowiedzenie w terminie', 'Ta sama'],
        ]),
        bg='surface'),
    cta_end(bg=None),
]

# ---------------------------------------------------------------- /dla-kogo/przemysl/
PAGES['przemysl'] = [
    hero('Gaz dla zakładów przemysłowych',
         'Jeśli Twój zakład zużywa od kilku do kilkuset GWh gazu rocznie, koszt paliwa jest jedną z największych pozycji w rachunku wyników. Dostajesz opiekuna, analizę profilu zużycia z faktur i model ceny dopasowany do planu produkcji: stały, indeksowany albo transzowy. Decyzje o cenie podejmujesz na danych, nie na telefonie od handlowca.',
         [('Porozmawiaj z opiekunem', '/kontakt/'), ('Wgraj fakturę', '/wgraj-fakture/', True)], crumb_text=crumb('Dla kogo', '/dla-kogo/', 'Przemysł'), name='Hero segmentu'),
    sec('Problemy segmentu',
        h('Co słyszymy od energetyków zakładowych'),
        cards([
            {'title': 'Cena ustalona w złym momencie', 'text': 'Umowa podpisana pod presją terminu, na szczycie notowań, na dwa lata. Model transzowy rozkłada ten moment na kilka decyzji.'},
            {'title': 'Sezonowość i odchylenia wolumenu', 'text': 'Kary za niedobór albo nadwyżkę zużycia. Ustalamy pasmo tolerancji na podstawie historii z faktur, nie planu sprzedaży.'},
            {'title': 'Wiele punktów poboru, wiele terminów', 'text': 'Różne daty końca umów w różnych lokalizacjach. Analiza umów porządkuje terminy w jednym harmonogramie.'},
            {'title': 'Raportowanie emisji', 'text': 'CSRD i ETS wymagają danych o zużyciu i emisji per lokalizacja. Przygotowujemy raport Scope 1 per punkt poboru (wkrótce).'},
        ], wide=True)),
    sec('Dopasowane produkty',
        h('Dopasowane modele ceny'),
        table(['Twój profil', 'Model', 'Dlaczego'], [
            ['Stabilne zużycie, budżet roczny, brak zespołu zakupowego', '<a href="/oferta/cena-stala/">Cena stała</a>', 'Jedna liczba w budżecie, brak decyzji w trakcie umowy'],
            ['Zespół zakupów śledzi rynek, akceptujecie zmienność', '<a href="/oferta/cena-indeksowana-tge/">Cena indeksowana TGE</a>', 'Płacisz cenę rynkową plus stałą marżę'],
            ['Duży wolumen, chcesz uśrednić cenę zakupu', '<a href="/oferta/model-transzowy/">Model transzowy</a>', 'Kilka decyzji zamiast jednej, średnia ważona transz'],
            ['Raportujesz emisje i szukasz paliwa o niższym śladzie', '<a href="/oferta/biometan/">Biometan (wkrótce)</a>', 'Biometan z instalacji Grupy IMA, bez obietnic terminów'],
        ]),
        bg='surface'),
    sec('Proces',
        h('Jak wygląda współpraca'),
        steps([
            ('Analiza profilu', 'Wgrywasz faktury z wszystkich punktów poboru albo przesyłasz zestawienie. Odczytujemy profil i terminy umów.'),
            ('Rekomendacja modelu', 'Opiekun przedstawia pasma cen w każdym modelu i rekomendację z uzasadnieniem. Decyzja jest Twoja.'),
            ('Umowa i pełnomocnictwo', 'Podpisujesz umowę na wybrany model. Dopiero potem wypowiadamy obecne umowy w ich terminach i zgłaszamy zmianę do operatorów.'),
            ('Dostawy i przegląd', 'Gaz płynie tą samą siecią. Co [[okres]] przeglądamy z Tobą zużycie, odchylenia i rynek.'),
        ])),
    sec('FAQ',
        h('Pytania zakładów przemysłowych'),
        faq([
            ('Czy PBM ma wystarczającą skalę, żeby obsłużyć zakład zużywający kilkaset GWh?', 'PBM należy do Grupy IMA Polska, która prowadzi własne instalacje przemysłowe i energetyczne [[aktywa]]. Koncesja na obrót paliwami gazowymi: [[numer koncesji]]. Limity wolumenu podamy w ofercie.'),
            ('Czy mogę rozdzielić wolumen między modele?', 'Tak, np. część wolumenu bazowego po cenie stałej, część sezonową po cenie indeksowanej [[warunki]].'),
            ('Jak wygląda zabezpieczenie płatności?', 'Zależnie od wolumenu i oceny ryzyka: [[formy zabezpieczeń]]. Warunki ustalamy indywidualnie.'),
            ('Kto jest moim opiekunem?', '[[imię i nazwisko, stanowisko]], kontakt: [[e-mail, telefon]].'),
        ]),
        bg='surface'),
    sec('CTA końcowe', h('Porozmawiaj z opiekunem'), p('Umów rozmowę o profilu zużycia Twojego zakładu albo zacznij od wgrania faktury.'), buttons([('Porozmawiaj z opiekunem', '/kontakt/'), ('Wgraj fakturę', '/wgraj-fakture/', True)]), pad='80'),
]

# ---------------------------------------------------------------- /dla-kogo/msp/
PAGES['msp'] = [
    hero('Gaz dla mniejszych firm',
         'Prowadzisz piekarnię, suszarnię, szklarnię, zakład przetwórstwa albo galwanizernię i płacisz za gaz więcej, niż byś chciał. Wgraj ostatnią fakturę. W 24 godziny dostaniesz ofertę z ceną stałą albo indeksowaną, bez wizyty handlowca. Zmianę sprzedawcy załatwimy za Ciebie w terminie Twojej obecnej umowy.',
         [('Wgraj fakturę', '/wgraj-fakture/'), ('Zobacz pasma cen', '/ceny-orientacyjne/', True)], crumb_text=crumb('Dla kogo', '/dla-kogo/', 'MŚP'), name='Hero segmentu'),
    sec('Problemy segmentu',
        h('Co słyszymy od właścicieli firm'),
        cards([
            {'title': 'Nie wiem, czy płacę za dużo', 'text': 'Porównaj cenę gazu z faktury z naszymi pasmami cen orientacyjnych. Jeśli jesteś powyżej pasma, warto sprawdzić ofertę.'},
            {'title': 'Nie mam czasu na formalności', 'text': 'Jedna faktura wystarczy do oferty. Umowę podpisujesz elektronicznie [[potwierdzić]], resztą zajmujemy się my na podstawie pełnomocnictwa.'},
            {'title': 'Boję się przerwy w dostawie', 'text': 'Nie ma przerwy. Ten sam operator, ta sama sieć, ten sam gazomierz. Zmienia się tylko wystawca faktury za gaz.'},
        ])),
    sec('Dopasowane produkty',
        h('Co dla Ciebie przygotujemy'),
        table(['Chcesz', 'Wybierz', 'Co to znaczy'], [
            ['Wiedzieć z góry, ile zapłacisz', '<a href="/oferta/cena-stala/">Cena stała</a>', 'Jedna stawka za MWh przez cały okres umowy'],
            ['Płacić cenę rynkową', '<a href="/oferta/cena-indeksowana-tge/">Cena indeksowana TGE</a>', 'Cena zmienia się z indeksem giełdowym plus stała marża'],
            ['Jedną fakturę za gaz i dystrybucję', '<a href="/oferta/umowa-kompleksowa-msp/">Umowa kompleksowa</a>', 'Jeżeli PBM nie ma generalnej umowy dystrybucyjnej z Twoim operatorem, podpiszesz osobno umowę dystrybucyjną; pomożemy w tym'],
        ]),
        bg='surface'),
    sec('Proces',
        h('Jak to działa'),
        steps([
            ('Wgrywasz fakturę', 'PDF albo zdjęcie. Odczytujemy taryfę, zużycie i sprzedawcę.'),
            ('Dostajesz ofertę w 24 godziny', 'Pasmo ceny, założenia i lista dokumentów do umowy.'),
            ('Podpisujesz umowę i pełnomocnictwo', 'Dopiero potem wypowiadamy obecną umowę w jej terminie i zgłaszamy zmianę do operatora.'),
            ('Płacisz mniej albo przewidywalnie', 'Gaz płynie bez przerwy. Zmienia się faktura.'),
        ])),
    sec('Ochrona MŚP',
        h('Twoje prawa jako mniejszej firmy'),
        p('Jeżeli jesteś mikro-, małym albo średnim przedsiębiorcą, sprzedawca musi wskazać w umowie na czas oznaczony sposób wyliczenia strat, którymi może Cię obciążyć za wcześniejsze rozwiązanie umowy (art. 4j ust. 3a–3b Prawa energetycznego, w brzmieniu obowiązującym od 21 lipca 2026 r. [[do weryfikacji prawnej]]). Więcej w <a href="/wiedza/art-4j-ust-3b-prawa-energetycznego-msp/">bazie wiedzy</a>.'),
        bg='surface'),
    sec('FAQ',
        h('Pytania mniejszych firm'),
        faq([
            ('Od jakiego zużycia opłaca się zmiana sprzedawcy?', 'Nie ma sztywnego progu. Porównaj cenę gazu z faktury z pasmem dla swojego profilu na stronie <a href="/ceny-orientacyjne/">ceny orientacyjne</a>. Oferta jest bezpłatna.'),
            ('Czy muszę mieć księgowego albo prawnika do zmiany?', 'Nie. Umowa i pełnomocnictwo to dwa dokumenty. Terminy wyliczamy za Ciebie i pokazujemy, skąd wynikają.'),
            ('Co z moim obecnym sprzedawcą?', 'Wypowiadamy umowę w jej terminie na podstawie pełnomocnictwa. Nie wcześniej, żeby nie narazić Cię na koszty.'),
            ('Czy dostanę fakturę za gaz i dystrybucję razem?', 'Tak, jeśli PBM ma generalną umowę dystrybucyjną z Twoim operatorem. Jeśli nie, podpiszesz osobno umowę dystrybucyjną; pomożemy w tym.'),
        ])),
    cta_end(),
]

# ---------------------------------------------------------------- /dla-doradcow/
PAGES['dla-doradcow'] = [
    hero('Dla doradców energetycznych i brokerów',
         'Obsługujesz portfel firm i szukasz sprzedawcy gazu, który odpowiada w 24 godziny, pokazuje jawne pasma cen i nie obchodzi Cię w relacji z klientem. Współpracujemy z doradcami na zasadach [[model współpracy: prowizja / stawka za punkt poboru / inny]]. Zgłoś się, a przygotujemy warunki dla Twojego portfela.',
         [('Zgłoś się', '#formularz')], name='Nagłówek strony'),
    sec('Model współpracy',
        h('Model współpracy'),
        table(['Element', 'Zasada'], [
            ['Wynagrodzenie doradcy', '[[model: prowizja od wolumenu / stawka za punkt poboru / inny]]'],
            ['Relacja z klientem', 'Klient pozostaje Twoim klientem. PBM kontaktuje się z nim w zakresie umowy i dostaw, nie prowadzi sprzedaży innych produktów bez Twojej wiedzy'],
            ['Oferty', 'Zbiorcze zapytania dla wielu punktów poboru, odpowiedź w [[czas]]'],
            ['Dokumenty', 'Wzory umów, pełnomocnictw i wypowiedzeń do pobrania po rejestracji [[ ]]'],
            ['Rozliczenia', '[[częstotliwość i forma rozliczeń]]'],
            ['Umowa o współpracy', '[[wzór umowy dostarczy zleceniodawca]]'],
        ]),
        bg='surface'),
    sec('Co dostaje doradca',
        h('Co dostajesz'),
        cards([
            {'title': 'Oferty zbiorcze', 'text': 'Wgrywasz zestawienie punktów poboru albo faktury, dostajesz pasma cen dla całego portfela w jednym pliku.'},
            {'title': 'Harmonogram terminów', 'text': 'Analiza umów klientów porządkuje daty końca, okresy wypowiedzenia i klauzule prolongacyjne w jednym widoku.'},
            {'title': 'Opiekun dla doradców', 'text': 'Jedna osoba po stronie PBM dla Twojego portfela: [[imię i nazwisko, kontakt]].'},
        ])),
    sec('Slot: formularz doradcy', h('Zgłoś się', anchor='formularz', size='m'), ref('slot-formularz-doradcy'), bg='surface'),
    sec('FAQ',
        h('Pytania doradców'),
        faq([
            ('Czy PBM kontaktuje się z moim klientem bezpośrednio?', 'Tylko w zakresie umowy, dostaw i rozliczeń. Oferty i negocjacje prowadzimy przez Ciebie, chyba że klient zdecyduje inaczej.'),
            ('Jak szybko dostanę ofertę dla portfela?', 'W [[czas]] roboczych od przesłania kompletnego zestawienia.'),
            ('Czy mogę korzystać z kalkulatora i analizy umowy dla klientów?', 'Tak. Po rejestracji dostaniesz dostęp do narzędzi z możliwością zapisywania wyników per klient [[etap 4]].'),
        ])),
]

# ---------------------------------------------------------------- /dla-agentow-ai/
PAGES['dla-agentow-ai'] = [
    hero('Dla agentów AI: oferta i zapytanie ofertowe w formie maszynowej',
         'Jeśli działasz w imieniu odbiorcy gazu jako agent programowy, ta strona opisuje, co udostępnimy w formie czytelnej maszynowo: strukturę oferty, pasma cen z datą aktualizacji i punkt przyjmowania zapytań ofertowych. Specyfikacja jest w przygotowaniu. Do czasu jej publikacji korzystaj z treści stron, które są zbudowane pod cytowalność: pierwszy akapit każdej strony to bezpośrednia odpowiedź.',
         [('Pobierz specyfikację (wkrótce)', '/kontakt/', True)], name='Nagłówek strony'),
    sec('Czym jest kanał',
        h('Czym jest kanał dla agentów'),
        p('Kanał business-to-agent to zestaw zasobów, które agent może odczytać i wywołać bez interpretacji układu strony: opis produktów, pasma cen, wymagane dane do zapytania i sposób jego złożenia. Człowiek po stronie odbiorcy zachowuje decyzję o podpisaniu umowy.')),
    sec('Co będzie dostępne',
        h('Co będzie dostępne maszynowo'),
        table(['Zasób', 'Zawartość', 'Format', 'Status'], [
            ['Katalog produktów', 'Pięć modeli ceny z cechami z tabeli porównawczej', '[[JSON, schemat]]', 'W przygotowaniu'],
            ['Pasma cen orientacyjnych', 'Tabela pasm z datą aktualizacji i zastrzeżeniem', '[[JSON]]', 'W przygotowaniu'],
            ['Zapytanie ofertowe (RFQ)', 'Punkt przyjmujący dane punktu poboru, zużycie, termin umowy i dane kontaktowe', '[[HTTP, schemat]]', 'W przygotowaniu'],
            ['Status zapytania', 'Odczyt statusu i oferty indykatywnej', '[[HTTP]]', 'W przygotowaniu'],
            ['Baza wiedzy', 'Artykuły z pierwszym akapitem jako odpowiedzią, spisem treści i źródłami', 'HTML, kanał RSS', 'Dostępne'],
        ]),
        bg='surface'),
    sec('Zasady',
        h('Zasady korzystania'),
        ul(['Agent działa w imieniu zidentyfikowanego odbiorcy; zapytanie zawiera dane firmy i osoby uprawnionej do kontaktu.',
            'Oferta indykatywna nie jest ofertą w rozumieniu Kodeksu cywilnego; ofertę wiążącą i umowę podpisuje człowiek.',
            'Pasma cen zawierają datę aktualizacji i zastrzeżenie; cytuj je razem.',
            'Limity zapytań, uwierzytelnienie i warunki użycia: [[do ustalenia w etapie 4]].']),
        ),
    sec('Specyfikacja (placeholder)',
        h('Specyfikacja'),
        group(p('Specyfikacja katalogu, pasm cen i punktu RFQ: <span class="gdp-placeholder">[[link do specyfikacji, po publikacji]]</span>'), p('Kontakt techniczny: <span class="gdp-placeholder">[[adres e-mail]]</span>'), cls='gdp-karta', name='Specyfikacja (slot)'),
        bg='surface'),
    cta_end(bg=None),
]

# ---------------------------------------------------------------- /wiedza/ (strona wpisów, treść w Blocksy nadpisana listą wpisów – zostawiamy sekcje kategorii)
PAGES['wiedza'] = [
    hero('Baza wiedzy o gazie dla firm',
         'Krótkie odpowiedzi na pytania energetyków zakładowych, dyrektorów finansowych i właścicieli firm: jak zmienić sprzedawcę, jak policzyć termin wypowiedzenia, kiedy grozi sprzedaż rezerwowa, który model ceny pasuje do profilu zużycia i co zmienia prawo. Każdy artykuł zaczyna się od odpowiedzi, kończy źródłami.',
         None, name='Nagłówek strony'),
    sec('Wyszukiwanie', search()),
    sec('Kategorie',
        h('Kategorie'),
        cards([
            {'title': 'Zmiana sprzedawcy', 'text': 'Kolejność kroków, terminy operatora, pełnomocnictwo.', 'button': ('Zobacz artykuły', '/category/zmiana-sprzedawcy/')},
            {'title': 'Umowy i wypowiedzenia', 'text': 'Okres wypowiedzenia, klauzula prolongacyjna, koszty wcześniejszego rozwiązania.', 'button': ('Zobacz artykuły', '/category/umowy-i-wypowiedzenia/')},
            {'title': 'Ceny i rynek', 'text': 'Modele ceny, indeksy TGE, składniki faktury.', 'button': ('Zobacz artykuły', '/category/ceny-i-rynek/')},
        ]),
        cards([
            {'title': 'Biometan i raportowanie', 'text': 'CSRD, ETS, emisje Scope 1 z gazu, biometan.', 'button': ('Zobacz artykuły', '/category/biometan-i-raportowanie/')},
            {'title': 'Sprzedaż rezerwowa', 'text': 'Kiedy grozi, ile kosztuje, jak z niej wyjść.', 'button': ('Zobacz artykuły', '/category/sprzedaz-rezerwowa/')},
            {'title': 'Komentarz rynkowy', 'text': 'Notowania TGE, decyzje URE i zmiany przepisów, z autorem i datą.', 'button': ('Zobacz komentarze', '/komentarz-rynkowy/')},
        ]),
        bg='surface'),
    sec('Najnowsze wpisy', h('Najnowsze artykuły'), query(cat=None, per_page=6, columns=3, query_id=31)),
    cta_end(),
]

# ---------------------------------------------------------------- /komentarz-rynkowy/
PAGES['komentarz-rynkowy'] = [
    hero('Komentarz rynkowy',
         'Krótkie komentarze o tym, co w danym tygodniu zmieniło się na rynku gazu i co to znaczy dla umowy odbiorcy przemysłowego: notowania TGE, decyzje Prezesa URE, zmiany przepisów. Każdy wpis ma datę, autora i datę ostatniej aktualizacji. Nie publikujemy prognoz cen.',
         None, name='Nagłówek strony'),
    sec('Lista wpisów', query(cat='komentarz-rynkowy', per_page=10, columns=2, query_id=21, author=True)),
    sec('Subskrypcja (slot)',
        h('Otrzymuj komentarz e-mailem'),
        form_card('Subskrypcja komentarza rynkowego', 'Jeden e-mail tygodniowo, bez ofert handlowych. Rezygnacja jednym kliknięciem.',
                  [field('E-mail', 'imie.nazwisko@firma.pl')], 'Subskrybuj', name='Subskrypcja (slot)'),
        bg='surface'),
    cta_end(bg=None),
]

# ---------------------------------------------------------------- /o-nas/
PAGES['o-nas'] = [
    hero('O PBM i Grupie IMA Polska',
         'PBM Sp. z o.o. sprzedaje paliwa gazowe klientom biznesowym pod marką Gaz dla Przemysłu. Należy do Grupy IMA Polska, która prowadzi działalność w przemyśle biotechnologicznym i energetyce odnawialnej: bioetanol, alkohol etylowy, biogaz, biometan. Koncesja na obrót paliwami gazowymi: [[numer i data koncesji]].',
         [('Kontakt', '/kontakt/')], name='Nagłówek strony'),
    sec('PBM',
        h('PBM Sp. z o.o.'),
        two(
            [p('Sprzedawca paliw gazowych dla firm. Model działania: oferta z faktury w 24 godziny, jawne pasma cen, zmiana sprzedawcy w terminie obecnej umowy, weryfikacja dokumentów przez człowieka.'),
             ul(['Siedziba: [[adres]]', 'KRS: [[ ]], NIP: [[ ]], REGON: [[ ]]', 'Kapitał zakładowy: [[ ]]', 'Koncesja OPG: [[numer, data, organ]]'])],
            [h3('Czego nie robimy'), ul(['Nie wypowiadamy umów klientów przed terminem', 'Nie publikujemy prognoz cen', 'Nie obiecujemy oszczędności bez analizy faktury', 'Nie sprzedajemy danych z faktur i umów'])],
        )),
    sec('Grupa IMA Polska',
        h('Grupa IMA Polska'),
        p('Grupa łączy przemysł biotechnologiczny z energetyką odnawialną. Własne instalacje dają PBM dostęp do biogazu i biometanu, które przygotowujemy jako uzupełnienie oferty gazu ziemnego.'),
        table(['Aktywo', 'Lokalizacja', 'Zakres'], [
            ['[[nazwa instalacji]]', '[[miejscowość]]', '[[bioetanol / alkohol etylowy / biogaz / biometan]]'],
            ['[[nazwa instalacji]]', '[[miejscowość]]', '[[ ]]'],
            ['[[nazwa instalacji]]', '[[miejscowość]]', '[[ ]]'],
        ], caption='Listę aktywów uzupełni zleceniodawca.'),
        bg='surface'),
    sec('Zespół',
        h('Zespół'),
        cards([
            {'title': '[[imię i nazwisko]]', 'texts': ['[[stanowisko]]', '[[jedno zdanie o zakresie odpowiedzialności]]']},
            {'title': '[[imię i nazwisko]]', 'texts': ['[[stanowisko]]', '[[jedno zdanie o zakresie odpowiedzialności]]']},
            {'title': '[[imię i nazwisko]]', 'texts': ['[[stanowisko]]', '[[jedno zdanie o zakresie odpowiedzialności]]']},
        ]),
        helper('Bez zdjęć stockowych. Zdjęcia zespołu dostarczy zleceniodawca albo sekcja pozostanie tekstowa.')),
    sec('Zasady',
        h('Jak pracujemy'),
        cols(
            col(h3('Terminy przed obietnicami'), p('Najpierw sprawdzamy, kiedy możesz zmienić sprzedawcę bez kosztów. Potem rozmawiamy o cenie.')),
            col(h3('Liczby ze źródłem'), p('Każda liczba na stronie ma źródło albo jest oznaczona jako do uzupełnienia. Indeksy TGE i taryfy URE linkujemy do publikacji.')),
            col(h3('Człowiek weryfikuje'), p('Narzędzia odczytują faktury i umowy. Zanim coś do Ciebie trafi, sprawdza to człowiek.')),
        ),
        bg='surface'),
    cta_end(bg=None),
]

# ---------------------------------------------------------------- /dokumenty/
DOKUMENTY = [
    ('Koncesja na obrót paliwami gazowymi (OPG)', 'Decyzja Prezesa URE'),
    ('Cennik paliw gazowych dla odbiorców biznesowych', 'Cennik'),
    ('Struktura paliw gazowych i wpływ na środowisko', 'Informacja ustawowa'),
    ('Regulamin serwisu gazdlaprzemyslu.pl', 'Regulamin'),
    ('Ogólne warunki umowy sprzedaży paliw gazowych', 'OWU'),
    ('Ogólne warunki umowy kompleksowej', 'OWU'),
    ('Wzór pełnomocnictwa do zmiany sprzedawcy', 'Wzór'),
    ('Polityka prywatności i informacja o przetwarzaniu danych', 'RODO'),
    ('Decyzje Prezesa URE dotyczące PBM', 'Decyzje'),
    ('Wykaz sprzedawców rezerwowych u operatorów', 'Informacja'),
]
PAGES['dokumenty'] = [
    hero('Dokumenty',
         'Dokumenty wymagane przepisami i potrzebne do zawarcia umowy: koncesja, cennik dla odbiorców biznesowych, informacja o strukturze paliw, ogólne warunki umów, wzory pełnomocnictw, polityka prywatności i decyzje Prezesa URE. Każdy wiersz zawiera nazwę, datę i plik PDF.',
         None, name='Nagłówek strony'),
    sec('Lista dokumentów',
        table(['Dokument', 'Rodzaj', 'Data publikacji', 'Plik'], [[n, r, '[[data]]', '<a href="/kontakt/">PDF [[plik]]</a>'] for n, r in DOKUMENTY],
              caption='Pliki dostarczy zleceniodawca. Wiersz tabeli jest wzorcem „wiersz dokumentu”.')),
    sources([SRC['pe'], SRC['ure']], updated='[[data]]', author='PBM Sp. z o.o.'),
]

# ---------------------------------------------------------------- /kontakt/
PAGES['kontakt'] = [
    hero('Kontakt',
         'Najszybsza droga do oferty to wgranie faktury. Jeśli wolisz rozmowę albo masz pytanie o umowę, napisz lub zadzwoń. Odpowiadamy w dni robocze w godzinach [[godziny]].',
         [('Wgraj fakturę', '/wgraj-fakture/')], name='Nagłówek strony'),
    sec('Dane i formularz',
        two(
            [h('Dane kontaktowe'),
             group(p('<strong>PBM Sp. z o.o.</strong>', cls='gdp-dane-podmiotu'), p('[[ulica i numer]]<br>[[kod pocztowy, miejscowość]]'), p('Telefon: [[numer]]<br>E-mail: [[adres]]'), p('Godziny: [[dni i godziny]]'), p('KRS [[ ]] · NIP [[ ]] · REGON [[ ]]', cls='gdp-tekst-pomocniczy'), cls='gdp-karta', name='Dane podmiotu'),
             h3('Dla doradców', size='s'), p('Osobna ścieżka i formularz na stronie <a href="/dla-doradcow/">dla doradców</a>.'),
             h3('Dane osobowe', size='s'), p('Kontakt w sprawach danych: [[adres IOD]]. <a href="/polityka-prywatnosci/">Polityka prywatności</a>.')],
            [form_card('Napisz do nas', 'Odpowiemy w [[czas]] roboczych.',
                       [field('Imię i nazwisko', 'Jan Kowalski'), field('Firma i NIP', 'Nazwa firmy, 10 cyfr'), field('E-mail i telefon', 'imie.nazwisko@firma.pl, +48'), field('Temat', 'Oferta / umowa / faktura / inne'), field('Wiadomość', 'Opisz krótko, czego dotyczy pytanie')],
                       'Wyślij', name='Formularz kontaktowy (slot)')],
        )),
    sec('Mapa (placeholder)',
        h('Jak do nas trafić', size='m'),
        group(p('<span class="gdp-placeholder">[[mapa: bez osadzeń zewnętrznych w etapie 1; docelowo statyczny obraz albo osadzenie zgodne z polityką prywatności]]</span>'), p('[[wskazówki dojazdu, parking, wejście]]'), cls='gdp-karta', name='Mapa (placeholder)'),
        bg='surface'),
]

# ---------------------------------------------------------------- prawne
def _prawna(title, lead_text, sekcje):
    out = [hero(title, lead_text, None, name='Nagłówek strony')]
    inner = []
    for s in sekcje:
        inner.append(h(s))
        inner.append(p('[[treść dostarczy zleceniodawca]]'))
    out.append(sec('Treść dokumentu', *inner))
    out.append(sec('Aktualizacja', helper('Ostatnia aktualizacja: [[data]] · Wersja: [[ ]]'), pad='50'))
    return out


PAGES['polityka-prywatnosci'] = _prawna('Polityka prywatności',
    'Dokument opisuje, jakie dane przetwarzamy w serwisie i w procesie ofertowania (dane z faktur i umów, dane kontaktowe), w jakim celu, na jakiej podstawie, jak długo i jakie masz prawa. Treść dostarczy zleceniodawca; poniżej struktura sekcji.',
    ['Administrator danych', 'Zakres i źródła danych', 'Cele i podstawy prawne przetwarzania', 'Dane z faktur i umów', 'Okres przechowywania', 'Odbiorcy danych', 'Prawa osób, których dane dotyczą', 'Pliki cookie i narzędzia analityczne', 'Zmiany polityki'])

PAGES['regulamin'] = _prawna('Regulamin serwisu',
    'Regulamin określa zasady korzystania z serwisu gazdlaprzemyslu.pl, w tym z narzędzi: wgrania faktury, kalkulatora terminu wypowiedzenia i analizy umowy, a także charakter ofert indykatywnych. Treść dostarczy zleceniodawca; poniżej struktura sekcji.',
    ['Postanowienia ogólne', 'Definicje', 'Usługi świadczone w serwisie', 'Oferta indykatywna a oferta wiążąca', 'Narzędzia: kalkulator i analiza umowy', 'Odpowiedzialność', 'Reklamacje', 'Własność intelektualna', 'Postanowienia końcowe'])

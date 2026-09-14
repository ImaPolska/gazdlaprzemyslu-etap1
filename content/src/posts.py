# -*- coding: utf-8 -*-
"""Treść 5 artykułów bazy wiedzy i 2 komentarzy rynkowych (szablony)."""
from gdp_blocks import *  # noqa

POSTS = {}

PRAWNA = '[[do weryfikacji prawnej]]'


def meta(kategoria):
    return helper('Kategoria: %s · Ostatnia aktualizacja: [[data]] · Autor: [[imię i nazwisko, stanowisko]]' % kategoria)


def psrc(items, updated='[[data]]', author='[[imię i nazwisko, stanowisko]]'):
    li = []
    for it in items:
        if isinstance(it, tuple):
            txt, url = it
            li.append('%s – <a href="%s">%s</a>' % (txt, url, url.replace('https://', '').replace('www.', '').rstrip('/')) if url else '%s – [[link]]' % txt)
        else:
            li.append(it)
    return group(h('Źródła', size='m'), ul(li), helper('Ostatnia aktualizacja: %s · Autor: %s' % (updated, author)), cls='gdp-karta', name='Źródła i aktualizacja')


def spis(entries):
    return group(h('Spis treści', size='m'), toc(entries), cls='gdp-karta', name='Spis treści')


def zastrz():
    return ref('zastrzezenie-cen')


def cta(text='Sprawdź, ile zapłacisz z fakturą', href='/wgraj-fakture/'):
    return group(h3('Co dalej'), p('Wgraj ostatnią fakturę za gaz. W 24 godziny dostaniesz ofertę, a zmianę sprzedawcy załatwimy w terminie Twojej obecnej umowy.'), buttons([(text, href)]), cls='gdp-karta gdp-karta-wyrozniona', name='CTA')


# ================================================================ 1. Jak zmienić sprzedawcę gazu w firmie
_T1 = [('Kto może zmienić sprzedawcę', 'kto-moze'), ('Kolejność kroków', 'kolejnosc'), ('Ile to trwa', 'ile-trwa'), ('Dokumenty', 'dokumenty'), ('Czego nie robić', 'czego-nie-robic'), ('Najczęstsze pytania', 'faq')]
POSTS['jak-zmienic-sprzedawce-gazu-w-firmie'] = dict(
    title='Jak zmienić sprzedawcę gazu w firmie: kolejność kroków i terminy',
    category='zmiana-sprzedawcy', date='2026-09-10 09:00:00',
    excerpt='Zmiana sprzedawcy gazu w firmie to cztery kroki: nowa umowa, pełnomocnictwo, wypowiedzenie w terminie, zgłoszenie do operatora. Gaz płynie bez przerwy.',
    body=[
        meta('Zmiana sprzedawcy'),
        lead('Zmiana sprzedawcy gazu w firmie odbywa się w czterech krokach: podpisujesz umowę z nowym sprzedawcą, udzielasz mu pełnomocnictwa, on wypowiada obecną umowę w jej terminie i zgłasza zmianę do operatora systemu dystrybucyjnego. Operator ma na jej przeprowadzenie do 21 dni od otrzymania informacji o nowej umowie. Sieć, gazomierz i operator pozostają te same, zmienia się wystawca faktury za gaz.'),
        spis(_T1),
        h('Kto może zmienić sprzedawcę', anchor='kto-moze'),
        p('Każdy odbiorca paliw gazowych ma prawo do zakupu gazu od wybranego sprzedawcy (zasada TPA, art. 4j ust. 1 Prawa energetycznego). Dotyczy to zarówno zakładu przemysłowego z własną umową dystrybucyjną, jak i mniejszej firmy z umową kompleksową. Warunkiem jest, żeby nowy sprzedawca mógł dostarczać gaz do Twojego punktu poboru: albo przez własną generalną umowę dystrybucyjną z Twoim operatorem, albo przez umowę sprzedaży, przy której umowę dystrybucyjną masz osobno.'),
        h('Kolejność kroków', anchor='kolejnosc'),
        p('Kolejność ma znaczenie, bo skutki błędnego wypowiedzenia ponosi odbiorca. Bezpieczna sekwencja wygląda tak:'),
        ol(['<strong>Umowa z nowym sprzedawcą.</strong> Podpisujesz umowę sprzedaży albo kompleksową z datą rozpoczęcia dostaw ustaloną na dzień po zakończeniu obecnej umowy.',
            '<strong>Pełnomocnictwo.</strong> Upoważniasz nowego sprzedawcę do wypowiedzenia obecnej umowy i zgłoszenia zmiany u operatora. Bez pełnomocnictwa te czynności wykonujesz sam.',
            '<strong>Wypowiedzenie obecnej umowy w jej terminie.</strong> Nowy sprzedawca składa wypowiedzenie tak, żeby umowa zakończyła się w planowanym dniu, bez kosztów wcześniejszego rozwiązania. Jeśli umowa ma klauzulę prolongacyjną, składa sprzeciw wobec przedłużenia.',
            '<strong>Zgłoszenie do operatora.</strong> Nowy sprzedawca informuje poprzedniego sprzedawcę i operatora o dniu rozpoczęcia sprzedaży (art. 4j ust. 4a). Operator przeprowadza zmianę w terminie do 21 dni (art. 4j ust. 6) %s.' % PRAWNA]),
        p('Odwrócenie kolejności, czyli wypowiedzenie przed podpisaniem nowej umowy, grozi dwiema rzeczami: umowa wygaśnie, a Ty trafisz do <a href="/wiedza/sprzedaz-rezerwowa-gazu-kiedy-grozi-i-ile-kosztuje/">sprzedaży rezerwowej</a>, albo nowy sprzedawca nie zdąży z ofertą w Twoim oknie i podpiszesz umowę pod presją.'),
        h('Ile to trwa', anchor='ile-trwa'),
        table(['Etap', 'Czas', 'Kto odpowiada'], [
            ['Oferta z faktury', '24 godziny', 'PBM'],
            ['Umowa i pełnomocnictwo', 'Zależy od Ciebie, zwykle kilka dni', 'Ty'],
            ['Analiza obecnej umowy i wyliczenie terminu', '[[czas]]', 'PBM'],
            ['Wypowiedzenie', 'W terminie z Twojej umowy, np. z 1- lub 3-miesięcznym wyprzedzeniem', 'PBM na podstawie pełnomocnictwa'],
            ['Zmiana u operatora', 'Do 21 dni od zgłoszenia (art. 4j ust. 6) %s' % PRAWNA, 'Operator'],
        ], caption='Czas całego procesu wyznacza okres wypowiedzenia obecnej umowy, nie formalności u operatora.'),
        h('Dokumenty', anchor='dokumenty'),
        ul(['Ostatnia faktura za gaz (numer punktu poboru, grupa taryfowa, zużycie)',
            'Obecna umowa z ogólnymi warunkami i załącznikiem cenowym',
            'Dane rejestrowe firmy i osoby uprawnionej do podpisu',
            'Pełnomocnictwo według wzoru nowego sprzedawcy',
            'Przy umowie sprzedaży bez umowy kompleksowej: umowa dystrybucyjna z operatorem albo pomoc w jej zawarciu']),
        h('Czego nie robić', anchor='czego-nie-robic'),
        ul(['Nie wypowiadaj umowy przed podpisaniem nowej. Ryzykujesz sprzedaż rezerwową albo umowę podpisaną pod presją.',
            'Nie wypowiadaj umowy na czas oznaczony przed jej końcem bez sprawdzenia kosztów. Sprzedawca może naliczyć odszkodowanie w granicach określonych w umowie i w art. 4j ust. 3a %s.' % PRAWNA,
            'Nie ignoruj klauzuli prolongacyjnej. Termin na sprzeciw bywa wcześniejszy niż okres wypowiedzenia.',
            'Nie polegaj na dacie wysłania. Liczy się dzień doręczenia oświadczenia sprzedawcy.']),
        h('Najczęstsze pytania', anchor='faq'),
        faq([
            ('Czy będzie przerwa w dostawie gazu?', 'Nie. Zmiana sprzedawcy jest operacją rozliczeniową u operatora. Sieć i gazomierz się nie zmieniają.'),
            ('Czy operator może odmówić zmiany?', 'Operator przeprowadza zmianę, jeżeli zgłoszenie jest kompletne i nowy sprzedawca ma prawo dostarczać gaz do Twojego punktu. Braki formalne wydłużają proces.'),
            ('Czy muszę wymienić gazomierz?', 'Nie z powodu zmiany sprzedawcy. Wymiana urządzeń zależy od operatora i taryfy, nie od sprzedawcy.'),
            ('Co z rozliczeniem u starego sprzedawcy?', 'Stary sprzedawca wystawia fakturę końcową na podstawie odczytu na dzień zmiany. Płacisz za gaz pobrany do tego dnia (art. 4j ust. 3) %s.' % PRAWNA),
        ]),
        cta(),
        psrc([SRC['pe_4j'], SRC['pe_5aa'], SRC['ure'], SRC['psg']]),
    ])

# ================================================================ 2. Okres wypowiedzenia i klauzula prolongacyjna
_T2 = [('Okres wypowiedzenia', 'okres'), ('Klauzula prolongacyjna', 'klauzula'), ('Jak policzyć termin', 'jak-policzyc'), ('Umowa na czas oznaczony a nieoznaczony', 'czas-oznaczony'), ('Najczęstsze błędy', 'bledy')]
POSTS['okres-wypowiedzenia-i-klauzula-prolongacyjna'] = dict(
    title='Okres wypowiedzenia umowy na gaz i klauzula prolongacyjna: jak policzyć termin',
    category='umowy-i-wypowiedzenia', date='2026-09-07 09:00:00',
    excerpt='Okres wypowiedzenia mówi, kiedy umowa się kończy po złożeniu oświadczenia. Klauzula prolongacyjna mówi, do kiedy trzeba się sprzeciwić przedłużeniu. To dwa różne terminy.',
    body=[
        meta('Umowy i wypowiedzenia'),
        lead('Okres wypowiedzenia to czas od doręczenia oświadczenia do zakończenia umowy, zwykle liczony w miesiącach ze skutkiem na koniec miesiąca. Klauzula prolongacyjna to zapis o automatycznym przedłużeniu umowy na kolejny okres, jeżeli w wyznaczonym terminie nie złożysz sprzeciwu. Żeby zmienić sprzedawcę bez kosztów, musisz trafić w oba terminy jednocześnie. <a href="/kalkulator-wypowiedzenia/">Kalkulator</a> wylicza ostatni bezpieczny dzień.'),
        spis(_T2),
        h('Okres wypowiedzenia', anchor='okres'),
        p('Umowa określa okres wypowiedzenia i sposób jego liczenia. Najczęstsze warianty:'),
        table(['Zapis w umowie', 'Co oznacza', 'Przykład (dane ilustracyjne)'], [
            ['„1 miesiąc ze skutkiem na koniec miesiąca kalendarzowego”', 'Oświadczenie doręczone w dowolnym dniu miesiąca kończy umowę z ostatnim dniem następnego miesiąca', 'Doręczone 14 września, umowa kończy się 31 października'],
            ['„3 miesiące ze skutkiem na koniec miesiąca”', 'Jak wyżej, ale trzy pełne miesiące', 'Doręczone 14 września, umowa kończy się 31 grudnia'],
            ['„30 dni od doręczenia”', 'Termin liczony w dniach, bez zaokrąglania do końca miesiąca', 'Doręczone 14 września, umowa kończy się 14 października'],
            ['„ze skutkiem na koniec roku gazowego”', 'Umowa kończy się 30 września, niezależnie od dnia doręczenia, o ile zachowasz wyprzedzenie', 'Sprawdź wymagane wyprzedzenie w umowie'],
        ]),
        p('Liczy się dzień doręczenia oświadczenia sprzedawcy, nie dzień wysłania. Zachowaj potwierdzenie nadania i odbioru.'),
        h('Klauzula prolongacyjna', anchor='klauzula'),
        p('Klauzula prolongacyjna, nazywana też klauzulą automatycznego przedłużenia, brzmi zwykle tak: „Umowa ulega przedłużeniu na kolejny okres [[X]] miesięcy, jeżeli żadna ze stron nie złoży oświadczenia o braku woli jej przedłużenia najpóźniej [[Y]] miesiące przed upływem okresu obowiązywania”. Ważne są trzy elementy:'),
        ul(['<strong>Termin na sprzeciw</strong> (np. 3 miesiące przed końcem umowy). Bywa dłuższy niż okres wypowiedzenia.',
            '<strong>Długość przedłużenia</strong> (np. 12 miesięcy). Po przedłużeniu umowa znów jest na czas oznaczony, z tymi samymi ograniczeniami wyjścia.',
            '<strong>Cena po przedłużeniu.</strong> Sprawdź, czy przedłużenie oznacza cenę z cennika sprzedawcy zamiast ceny z umowy.']),
        h('Jak policzyć termin', anchor='jak-policzyc'),
        ol(['Ustal datę końca umowy z paragrafu o okresie obowiązywania.',
            'Odejmij termin na sprzeciw z klauzuli prolongacyjnej. To ostatni dzień na oświadczenie o braku woli przedłużenia.',
            'Odejmij okres wypowiedzenia od daty końca umowy, uwzględniając zasadę „koniec miesiąca”. To ostatni dzień na wypowiedzenie ze skutkiem na koniec umowy.',
            'Wcześniejsza z dwu dat to Twój ostatni bezpieczny dzień. Zaplanuj doręczenie kilka dni wcześniej.',
            'Jeżeli umowa nie ma klauzuli prolongacyjnej, a jest na czas oznaczony, sprawdź, czy wymaga wypowiedzenia w ogóle; niektóre wygasają z upływem terminu, ale wtedy trzeba na czas zgłosić nową umowę do operatora, żeby nie trafić do sprzedaży rezerwowej.']),
        p('<a href="/kalkulator-wypowiedzenia/">Kalkulator terminu wypowiedzenia</a> wykonuje te kroki za Ciebie. <a href="/analiza-umowy/">Analiza umowy</a> odczytuje dane z dokumentu i weryfikuje je przez człowieka.'),
        h('Umowa na czas oznaczony a nieoznaczony', anchor='czas-oznaczony'),
        table(['Rodzaj umowy', 'Wypowiedzenie', 'Koszty', 'Podstawa'], [
            ['Na czas nieoznaczony', 'W każdym czasie, oświadczeniem, z zachowaniem okresu wypowiedzenia', 'Bez dodatkowych kosztów; płacisz za pobrany gaz', 'art. 4j ust. 3 PE %s' % PRAWNA],
            ['Na czas oznaczony', 'Możliwe, ale umowa może przewidywać odszkodowanie za wcześniejsze rozwiązanie', 'W granicach umowy; dla gospodarstw domowych oraz mikro- i małych przedsiębiorców nie więcej niż bezpośrednie straty sprzedawcy', 'art. 4j ust. 3a PE %s' % PRAWNA],
            ['Na czas oznaczony, MŚP, od 21.07.2026', 'Jak wyżej', 'Sprzedawca musi wskazać w umowie sposób wyliczenia strat', 'art. 4j ust. 3b PE %s' % PRAWNA],
        ]),
        h('Najczęstsze błędy', anchor='bledy'),
        ul(['Liczenie terminu od daty wysłania zamiast doręczenia.',
            'Pominięcie klauzuli prolongacyjnej i spóźniony sprzeciw, przez co umowa przedłuża się o kolejny rok.',
            'Wypowiedzenie umowy na czas oznaczony „na wszelki wypadek” przed jej końcem, z odszkodowaniem.',
            'Wypowiedzenie bez nowej umowy i bez zgłoszenia do operatora, czyli sprzedaż rezerwowa.']),
        cta('Prześlij umowę do analizy', '/analiza-umowy/'),
        psrc([SRC['pe_4j'], SRC['kc'], SRC['ure']]),
    ])

# ================================================================ 3. Sprzedaż rezerwowa
_T3 = [('Kiedy uruchamia się sprzedaż rezerwowa', 'kiedy'), ('Kto jest sprzedawcą rezerwowym', 'kto'), ('Ile kosztuje', 'ile-kosztuje'), ('Jak wyjść ze sprzedaży rezerwowej', 'jak-wyjsc'), ('Jak jej uniknąć', 'jak-uniknac')]
POSTS['sprzedaz-rezerwowa-gazu-kiedy-grozi-i-ile-kosztuje'] = dict(
    title='Sprzedaż rezerwowa gazu: kiedy grozi firmie i ile kosztuje',
    category='sprzedaz-rezerwowa', date='2026-09-03 09:00:00',
    excerpt='Sprzedaż rezerwowa uruchamia się, gdy Twój sprzedawca przestaje sprzedawać gaz albo umowa wygasa bez zgłoszenia nowej. Dla firm cena nie jest taryfowa.',
    body=[
        meta('Sprzedaż rezerwowa'),
        lead('Sprzedaż rezerwowa to awaryjna sprzedaż gazu przez sprzedawcę wskazanego w Twojej umowie dystrybucyjnej albo kompleksowej, uruchamiana przez operatora, gdy dotychczasowy sprzedawca zaprzestał sprzedaży, umowa wygasła bez zgłoszenia nowej albo nowy sprzedawca nie rozpoczął dostaw. Gaz płynie dalej, ale po cenie sprzedawcy rezerwowego, która dla firm nie jest taryfowa i bywa znacząco wyższa niż rynkowa.'),
        spis(_T3),
        h('Kiedy uruchamia się sprzedaż rezerwowa', anchor='kiedy'),
        p('Zgodnie z art. 5aa Prawa energetycznego operator uruchamia sprzedaż rezerwową w trzech sytuacjach %s:' % PRAWNA),
        ol(['Dotychczasowy sprzedawca zaprzestał sprzedaży z przyczyn leżących po jego stronie, np. utracił koncesję albo umowę z operatorem.',
            'Umowa sprzedaży albo kompleksowa wygasła lub została rozwiązana, a Ty nie zgłosiłeś do operatora nowej umowy.',
            'Nowy sprzedawca nie rozpoczął sprzedaży w terminie wskazanym w zgłoszeniu.']),
        p('Dla firmy najczęstszy jest przypadek drugi: wypowiedzenie złożone bez nowej umowy albo umowa na czas oznaczony, która wygasła, zanim nowa została zgłoszona.'),
        h('Kto jest sprzedawcą rezerwowym', anchor='kto'),
        p('Sprzedawcę rezerwowego wskazujesz w umowie dystrybucyjnej albo kompleksowej z listy sprzedawców rezerwowych publikowanej przez operatora i jednocześnie upoważniasz operatora do zawarcia umowy w Twoim imieniu. Jeżeli nie wskazałeś sprzedawcy rezerwowego albo wskazany nie może sprzedawać, operator uruchamia sprzedaż przez sprzedawcę z urzędu (art. 5ab) %s. Umowa ze sprzedawcą rezerwowym zawierana jest na czas nieokreślony, od dnia zaprzestania sprzedaży przez poprzedniego sprzedawcę.' % PRAWNA),
        h('Ile kosztuje', anchor='ile-kosztuje'),
        table(['Odbiorca', 'Cena w sprzedaży rezerwowej', 'Skąd wynika'], [
            ['Gospodarstwo domowe', 'Według taryfy sprzedawcy rezerwowego zatwierdzonej przez Prezesa URE', 'Taryfa URE %s' % PRAWNA],
            ['Firma (odbiorca biznesowy)', 'Według cennika sprzedaży rezerwowej sprzedawcy, bez zatwierdzenia przez URE', 'Cennik sprzedawcy rezerwowego [[link do cennika]]'],
        ], caption='Cenniki sprzedaży rezerwowej publikują sprzedawcy; nie podajemy tu liczb, bo zmieniają się w czasie.'),
        p('W cenniku sprzedaży rezerwowej cena gazu jest zwykle powiązana z notowaniami rynkowymi powiększonymi o narzut. Wysokość narzutu zależy od sprzedawcy. Do tego dochodzą niezmienione opłaty dystrybucyjne. Sprawdź cennik sprzedawcy rezerwowego wskazanego w Twojej umowie dystrybucyjnej [[źródło]].'),
        zastrz(),
        h('Jak wyjść ze sprzedaży rezerwowej', anchor='jak-wyjsc'),
        ol(['Podpisz umowę z wybranym sprzedawcą i udziel mu pełnomocnictwa.',
            'Nowy sprzedawca zgłasza umowę do operatora. Umowa sprzedaży rezerwowej wygasa z dniem rozpoczęcia sprzedaży przez nowego sprzedawcę albo po wypowiedzeniu, według zasad w umowie rezerwowej (typowo miesięczny okres ze skutkiem na koniec następnego miesiąca) %s.' % PRAWNA,
            'Sprawdź fakturę końcową od sprzedawcy rezerwowego z odczytem na dzień zmiany.']),
        p('Im szybciej podpiszesz nową umowę, tym krócej płacisz cenę rezerwową. Oferta z faktury w 24 godziny skraca ten czas.'),
        h('Jak jej uniknąć', anchor='jak-uniknac'),
        check(['Nie wypowiadaj umowy, zanim podpiszesz nową.',
               'Sprawdź w umowie dystrybucyjnej, kto jest Twoim sprzedawcą rezerwowym, i pobierz jego cennik.',
               'Przy umowie na czas oznaczony zaplanuj zgłoszenie nowej umowy do operatora przed dniem wygaśnięcia.',
               'Skorzystaj z <a href="/kalkulator-wypowiedzenia/">kalkulatora terminu</a> albo <a href="/analiza-umowy/">analizy umowy</a>, żeby zobaczyć okno wyjścia na osi czasu.']),
        cta(),
        psrc([SRC['pe_5aa'], SRC['pe_4j'], SRC['ure'], SRC['psg']]),
    ])

# ================================================================ 4. Cena stała czy indeksowana
_T4 = [('Czym się różnią', 'roznice'), ('Porównanie', 'porownanie'), ('Kiedy cena stała', 'kiedy-stala'), ('Kiedy cena indeksowana', 'kiedy-indeksowana'), ('Trzecia droga: transze', 'transze'), ('Jak czytać ofertę', 'jak-czytac')]
POSTS['cena-stala-czy-indeksowana-do-tge'] = dict(
    title='Cena stała czy indeksowana do TGE: który model wybrać dla firmy',
    category='ceny-i-rynek', date='2026-08-27 09:00:00',
    excerpt='Cena stała daje przewidywalny budżet, indeksowana daje cenę rynkową plus stałą marżę. Wybór zależy od tego, kto w firmie i jak często podejmuje decyzję o cenie.',
    body=[
        meta('Ceny i rynek'),
        lead('Cena stała to jedna stawka za MWh na cały okres umowy, ustalona w dniu podpisania na podstawie notowań rynku terminowego TGE. Cena indeksowana zmienia się co miesiąc (albo dobę) z wybranym indeksem TGE, powiększonym o stałą marżę. Cena stała pasuje firmom, które chcą jednej liczby w budżecie. Indeksowana pasuje firmom, które akceptują zmienność i nie chcą płacić premii za ryzyko.'),
        spis(_T4),
        h('Czym się różnią', anchor='roznice'),
        p('W obu modelach punktem odniesienia jest Towarowa Giełda Energii. W cenie stałej sprzedawca kupuje gaz na rynku terminowym z wyprzedzeniem, a ryzyko zmian ceny bierze na siebie, za co w cenie zawiera premię. W cenie indeksowanej gaz rozliczany jest po cenie indeksu z okresu dostawy, a marża sprzedawcy jest stała i jawna. Ryzyko zmienności zostaje po Twojej stronie.'),
        h('Porównanie', anchor='porownanie'),
        table(['Cecha', 'Cena stała', 'Cena indeksowana TGE'], [
            ['Cena za MWh', 'Jedna liczba na cały okres', 'Indeks TGE z okresu dostawy + stała marża'],
            ['Budżet', 'Znany z góry', 'Prognozowany, korygowany co miesiąc'],
            ['Ryzyko wzrostu cen', 'Po stronie sprzedawcy', 'Po Twojej stronie'],
            ['Korzyść ze spadku cen', 'Brak', 'Pełna'],
            ['Premia za ryzyko w cenie', 'Tak, wliczona w stawkę', 'Nie'],
            ['Decyzje w trakcie umowy', 'Brak', 'Brak; opcjonalnie przejście na cenę stałą [[warunki]]'],
            ['Dla kogo', 'Firmy z budżetem rocznym, bez zespołu zakupowego', 'Firmy śledzące rynek, akceptujące zmienność'],
        ]),
        h('Kiedy cena stała', anchor='kiedy-stala'),
        ul(['Planujesz budżet na rok albo dwa i musisz go obronić przed zarządem.',
            'Koszt gazu w produkcie przekłada się na cenę dla Twoich klientów, którą ustalasz z góry.',
            'Nie masz osoby, która będzie śledzić notowania.',
            'Akceptujesz, że w razie spadku cen zapłacisz więcej niż rynek.']),
        h('Kiedy cena indeksowana', anchor='kiedy-indeksowana'),
        ul(['Możesz przenosić zmiany kosztu gazu na klientów albo masz bufor w marży.',
            'Chcesz zapłacić za gaz cenę rynkową bez premii za ryzyko.',
            'Masz zespół zakupów albo doradcę, który śledzi rynek i może zdecydować o zamianie na cenę stałą w wybranym momencie.',
            'Akceptujesz miesięczne wahania faktury.']),
        h('Trzecia droga: transze', anchor='transze'),
        p('Jeżeli Twój wolumen jest duży, a nie chcesz decydować o całej cenie w jednym dniu, <a href="/oferta/model-transzowy/">model transzowy</a> pozwala kupować gaz w kilku częściach w różnych terminach. Cena końcowa to średnia ważona transz. Do zamknięcia ostatniej transzy niekupiony wolumen rozliczany jest po cenie indeksowanej.'),
        h('Jak czytać ofertę', anchor='jak-czytac'),
        ol(['Sprawdź, czy cena zawiera wszystkie składniki: gaz, marżę, koszty bilansowania, opłaty i podatki wskazane w ofercie. Opłaty dystrybucyjne są poza ceną sprzedawcy.',
            'W cenie indeksowanej sprawdź, który indeks TGE jest podstawą i z jakiego okresu (miesiąc przed dostawą, miesiąc dostawy, doba).',
            'Sprawdź pasmo tolerancji wolumenu i koszty odchyleń.',
            'Sprawdź datę ważności oferty. Cena stała jest ważna krótko, bo zależy od dnia notowań.',
            'Porównaj z <a href="/ceny-orientacyjne/">pasmami cen orientacyjnych</a> i z ceną z ostatniej faktury.']),
        zastrz(),
        cta(),
        psrc([SRC['tge'], SRC['ure'], SRC['pe']]),
    ])

# ================================================================ 5. Art. 4j ust. 3b
_T5 = [('Co mówi przepis', 'co-mowi'), ('Kogo dotyczy', 'kogo-dotyczy'), ('Co się zmienia w praktyce', 'praktyka'), ('Jak sprawdzić swoją umowę', 'jak-sprawdzic'), ('Czego przepis nie zmienia', 'czego-nie-zmienia')]
POSTS['art-4j-ust-3b-prawa-energetycznego-msp'] = dict(
    title='Art. 4j ust. 3b Prawa energetycznego: co zmienia dla MŚP przy wypowiedzeniu umowy na gaz',
    category='umowy-i-wypowiedzenia', date='2026-08-20 09:00:00',
    excerpt='Od 21 lipca 2026 r. sprzedawca musi wskazać w umowie na czas oznaczony z MŚP sposób wyliczenia strat, którymi może obciążyć firmę za wcześniejsze rozwiązanie.',
    body=[
        meta('Umowy i wypowiedzenia'),
        lead('Art. 4j ust. 3b Prawa energetycznego, w brzmieniu od 21 lipca 2026 r., zobowiązuje sprzedawcę do wskazania w umowie na czas oznaczony z odbiorcą w gospodarstwie domowym oraz z mikro-, małym i średnim przedsiębiorcą sposobu wyliczenia strat, którymi może obciążyć odbiorcę za wcześniejsze rozwiązanie umowy. Koszt wyjścia z umowy staje się policzalny przed podpisaniem %s.' % PRAWNA),
        spis(_T5),
        h('Co mówi przepis', anchor='co-mowi'),
        p('Podstawą jest art. 4j ust. 3a: odbiorca może wypowiedzieć umowę na czas oznaczony bez ponoszenia kosztów i odszkodowań innych niż wynikające z treści umowy, a w przypadku gospodarstw domowych oraz mikro- i małych przedsiębiorców koszty te nie mogą przewyższać bezpośrednich strat ekonomicznych sprzedawcy. Ust. 3b dodaje obowiązek informacyjny: sposób wyliczenia tych strat musi być w umowie. Przepis wchodzi w życie w dwóch krokach:'),
        table(['Data', 'Zmiana', 'Podstawa'], [
            ['30 kwietnia 2026 r.', 'Sprzedawca wskazuje w umowie maksymalną wysokość kary umownej za wcześniejsze rozwiązanie, nie wyższą niż bezpośrednie straty, oraz sposób jej wyliczenia', 'Dz.U. 2026 poz. 516 %s' % PRAWNA],
            ['21 lipca 2026 r.', 'Obowiązek wskazania sposobu wyliczenia strat obejmuje umowy z odbiorcami w gospodarstwach domowych oraz mikro-, małymi i średnimi przedsiębiorcami', 'art. 4j ust. 3b PE %s' % PRAWNA],
            ['21 lipca 2026 r.', 'Przy umowach na czas oznaczony z gwarancją stałej ceny sprzedawca energii elektrycznej wskazuje maksymalną wysokość odszkodowań (nie dotyczy gazu)', 'art. 4j ust. 3c PE %s' % PRAWNA],
        ], caption='Daty i numery publikacji podlegają weryfikacji prawnej przed publikacją.'),
        h('Kogo dotyczy', anchor='kogo-dotyczy'),
        p('Przepis odwołuje się do definicji z art. 7 ust. 1 pkt 1–3 Prawa przedsiębiorców: mikro-, mały i średni przedsiębiorca. Kryteria to średnioroczne zatrudnienie i obrót lub suma bilansowa z dwóch ostatnich lat obrotowych. Jeżeli Twoja firma mieści się w tych progach, sprzedawca musi w umowie na czas oznaczony wskazać sposób wyliczenia strat. Dla większych przedsiębiorstw koszty wcześniejszego rozwiązania określa wyłącznie umowa %s.' % PRAWNA),
        h('Co się zmienia w praktyce', anchor='praktyka'),
        ul(['Przed podpisaniem umowy wiesz, jak sprzedawca policzy koszt, jeśli zdecydujesz się wyjść wcześniej. Możesz to porównać między ofertami.',
            'Zapisy typu „odszkodowanie w wysokości ustalonej przez sprzedawcę” bez sposobu wyliczenia nie spełniają wymogu przepisu.',
            'Przepis nie znosi kosztów wcześniejszego rozwiązania. Nadal bezpieczniejsze jest wypowiedzenie w terminie umowy, bez odszkodowań.',
            'Umowy zawarte przed wejściem w życie zmian podlegają przepisom przejściowym [[do weryfikacji prawnej: zakres stosowania do umów w toku]].']),
        h('Jak sprawdzić swoją umowę', anchor='jak-sprawdzic'),
        ol(['Ustal, czy umowa jest na czas oznaczony i kiedy została zawarta.',
            'Znajdź paragraf o rozwiązaniu umowy i odszkodowaniach. Sprawdź, czy jest tam sposób wyliczenia, a nie tylko kwota albo odesłanie do cennika.',
            'Sprawdź, czy sposób wyliczenia odnosi się do bezpośrednich strat, np. różnicy między ceną z umowy i ceną rynkową dla niepobranego wolumenu.',
            'Jeżeli zapis jest niejasny, skorzystaj z <a href="/analiza-umowy/">analizy umowy</a>; w spornych przypadkach rekomendujemy konsultację prawną.']),
        h('Czego przepis nie zmienia', anchor='czego-nie-zmienia'),
        ul(['Nie skraca okresu wypowiedzenia i nie znosi klauzul prolongacyjnych.',
            'Nie zwalnia z zapłaty za pobrany gaz.',
            'Nie zastępuje zgłoszenia zmiany sprzedawcy do operatora; bez niego grozi sprzedaż rezerwowa.',
            'Nie jest zachętą do wcześniejszego rozwiązania umowy. PBM planuje zmianę sprzedawcy na termin bez kosztów.']),
        cta('Prześlij umowę do analizy', '/analiza-umowy/'),
        psrc([SRC['pe_4j'], ('Ustawa z dnia 6 marca 2018 r. – Prawo przedsiębiorców, art. 7', 'https://isap.sejm.gov.pl'), SRC['ure']]),
    ])

# ================================================================ komentarze rynkowe (szablony, treść do uzupełnienia)
KOMENTARZE = {
    2001: dict(
        title='Komentarz rynkowy: tydzień [[nr tygodnia]] 2026',
        category='komentarz-rynkowy', date='2026-09-08 09:00:00',
        excerpt='Co zmieniło się na rynku gazu w tym tygodniu i co to znaczy dla umowy odbiorcy przemysłowego. Szablon wpisu; liczby uzupełnia autor.',
        body=[
            helper('Komentarz rynkowy · [[data publikacji]] · Autor: [[imię i nazwisko, stanowisko]]'),
            lead('[[Jedno lub dwa zdania: co wydarzyło się na rynku w tym tygodniu i jaki ma to skutek dla odbiorcy. Bez prognoz.]]'),
            h('Notowania TGE', size='m'),
            table(['Instrument', 'Cena (zł/MWh)', 'Zmiana tydzień do tygodnia'], [
                ['[[np. RDNg, indeks]]', '[[ ]]', '[[ ]]'],
                ['[[np. kontrakt na kolejny rok]]', '[[ ]]', '[[ ]]'],
            ], caption='Źródło: Towarowa Giełda Energii, stan na [[data]].', numeric=True),
            h('Decyzje i przepisy', size='m'),
            ul(['[[decyzja Prezesa URE albo zmiana przepisu, z datą]]', '[[druga pozycja albo usuń]]']),
            h('Co to znaczy dla Twojej umowy', size='m'),
            p('[[Dwa lub trzy zdania odnoszące zmiany do modeli ceny: stała, indeksowana, transze. Bez rekomendacji zakupu.]]'),
            zastrz(),
            psrc([SRC['tge'], SRC['ure']]),
        ]),
    2002: dict(
        title='Komentarz rynkowy: tydzień [[nr tygodnia]] 2026 (drugi szablon)',
        category='komentarz-rynkowy', date='2026-09-01 09:00:00',
        excerpt='Szablon komentarza rynkowego z sekcją o zmianach w przepisach. Liczby i treść uzupełnia autor.',
        body=[
            helper('Komentarz rynkowy · [[data publikacji]] · Autor: [[imię i nazwisko, stanowisko]]'),
            lead('[[Jedno lub dwa zdania: główny temat tygodnia i skutek dla odbiorcy.]]'),
            h('Temat tygodnia', size='m'),
            p('[[Trzy do pięciu zdań opisu wydarzenia ze źródłem.]]'),
            h('Notowania TGE', size='m'),
            table(['Instrument', 'Cena (zł/MWh)', 'Zmiana tydzień do tygodnia'], [['[[ ]]', '[[ ]]', '[[ ]]']], caption='Źródło: Towarowa Giełda Energii, stan na [[data]].', numeric=True),
            h('Co to znaczy dla Twojej umowy', size='m'),
            p('[[Dwa lub trzy zdania. Bez rekomendacji zakupu i bez prognoz.]]'),
            zastrz(),
            psrc([SRC['tge'], SRC['ure']]),
        ]),
}

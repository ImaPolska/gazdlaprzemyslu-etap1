# Test publicznych linków Playground (13.2, „blueprint uruchamia się bez interwencji”)

Data: 2026-09-13. Metoda: przeglądarka Chromium sterowana programowo otwiera
`https://playground.wordpress.net/?blueprint-url=<URL blueprintu>` i co 5 s odpytuje zagnieżdżoną ramkę WordPressa,
aż `body.home` zawiera dokładnie jeden `h1`. Artefakty (blueprint, ZIP motywu, WXR, JSON konfiguracji) serwowane
z tymczasowego publicznego hosta z nagłówkiem `Access-Control-Allow-Origin: *` – identycznie jak `raw.githubusercontent.com`.

| Kierunek | Wynik | Czas do wyrenderowanej strony głównej | `lang` | klasa kierunku | h1 |
|---|---|---|---|---|---|
| A | OK | ≤ 60 s (pierwsze uruchomienie, zimny cache Playground) | pl-PL | `gdp-dir-A` | „Oferta na gaz dla Twojego zakładu w 24 godziny od wgrania faktury” |
| B | OK | 15 s | pl-PL | `gdp-dir-B` | jak wyżej |
| C | OK | 20 s | pl-PL | `gdp-dir-C` | jak wyżej |

Docelowe linki (po publikacji tagów w GitHub) – ta sama treść blueprintu, inny host:

```
https://playground.wordpress.net/?blueprint-url=https://raw.githubusercontent.com/ImaPolska/gazdlaprzemyslu-etap1/etap1-A/blueprints/A.json
https://playground.wordpress.net/?blueprint-url=https://raw.githubusercontent.com/ImaPolska/gazdlaprzemyslu-etap1/etap1-B/blueprints/B.json
https://playground.wordpress.net/?blueprint-url=https://raw.githubusercontent.com/ImaPolska/gazdlaprzemyslu-etap1/etap1-C/blueprints/C.json
```

Po publikacji test powtarza się tym samym skryptem na docelowych adresach; wynik dopisuje się poniżej.

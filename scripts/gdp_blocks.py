"""
Biblioteka budująca markup bloków core (Gutenberg) z prostych wywołań w Pythonie.
Używana przez scripts/build-pages.py do generowania content/pages/*.html i content/posts/*.html.

Zasady (sekcja 5 instrukcji): wyłącznie bloki core/*, sekcje = core/group z metadata.name po polsku
i templateLock=contentOnly, brak inline CSS poza ustawieniami bloków (padding z presetów),
tabele core/table z <thead>, liczby w klasie gdp-liczby.
"""
import json
import re


def _j(attrs):
    return json.dumps(attrs, ensure_ascii=False, separators=(',', ':'))


def _cls(*parts):
    return ' '.join(p for p in parts if p)


def _fs(size):
    return ' has-%s-font-size' % size if size else ''


def _slug(text):
    t = text.lower()
    for a, b in zip('ąćęłńóśźż', 'acelnoszz'):
        t = t.replace(a, b)
    t = re.sub(r'[^a-z0-9]+', '-', t).strip('-')
    return t[:60]


# --- sekcje --------------------------------------------------------------

def sec(name, *inner, bg=None, pad='70', cls=None):
    """Sekcja strony: core/group alignfull, contentOnly, padding z presetów."""
    attrs = {'metadata': {'name': name}, 'templateLock': 'contentOnly', 'align': 'full'}
    if cls:
        attrs['className'] = cls
    attrs['style'] = {'spacing': {'padding': {'top': 'var:preset|spacing|%s' % pad, 'bottom': 'var:preset|spacing|%s' % pad}}}
    classes = _cls('wp-block-group alignfull', cls)
    if bg:
        attrs['backgroundColor'] = bg
        classes += ' has-%s-background-color has-background' % bg
    attrs['layout'] = {'type': 'constrained'}
    body = '\n\n'.join(x for x in inner if x)
    return ('<!-- wp:group %s -->\n<div class="%s" style="padding-top:var(--wp--preset--spacing--%s);padding-bottom:var(--wp--preset--spacing--%s)">%s</div>\n<!-- /wp:group -->'
            % (_j(attrs), classes, pad, pad, body))


def group(*inner, cls=None, name=None, bg=None):
    """Zwykła grupa (bez alignfull), np. karta lub kontener slotu."""
    attrs = {}
    if name:
        attrs['metadata'] = {'name': name}
    if cls:
        attrs['className'] = cls
    classes = _cls('wp-block-group', cls)
    if bg:
        attrs['backgroundColor'] = bg
        classes += ' has-%s-background-color has-background' % bg
    attrs['layout'] = {'type': 'constrained'}
    return '<!-- wp:group %s -->\n<div class="%s">%s</div>\n<!-- /wp:group -->' % (_j(attrs), classes, '\n\n'.join(x for x in inner if x))


# --- tekst ---------------------------------------------------------------

def h(text, level=2, size=None, anchor=None, cls=None):
    attrs = {}
    if level != 2:
        attrs['level'] = level
    if anchor:
        attrs['anchor'] = anchor
    if size:
        attrs['fontSize'] = size
    if cls:
        attrs['className'] = cls
    a = ' %s' % _j(attrs) if attrs else ''
    idattr = ' id="%s"' % anchor if anchor else ''
    return '<!-- wp:heading%s -->\n<h%d class="%s"%s>%s</h%d>\n<!-- /wp:heading -->' % (a, level, _cls('wp-block-heading', cls) + _fs(size), idattr, text, level)


def h1(text):
    return h(text, level=1)


def h3(text, size='m', anchor=None):
    return h(text, level=3, size=size, anchor=anchor)


def p(text, size=None, cls=None, bind=None):
    attrs = {}
    if size:
        attrs['fontSize'] = size
    if cls:
        attrs['className'] = cls
    if bind:
        attrs['metadata'] = {'name': bind, 'bindings': {'__default': {'source': 'core/pattern-overrides'}}}
    a = ' %s' % _j(attrs) if attrs else ''
    classes = _cls(cls) + _fs(size)
    ca = ' class="%s"' % classes.strip() if classes.strip() else ''
    return '<!-- wp:paragraph%s -->\n<p%s>%s</p>\n<!-- /wp:paragraph -->' % (a, ca, text)


def lead(text):
    return p(text, size='m')


def label(text):
    return p(text, cls='gdp-etykieta')


def helper(text):
    return p(text, cls='gdp-tekst-pomocniczy')


def _list(items, ordered=False, cls=None):
    attrs = {}
    if ordered:
        attrs['ordered'] = True
    if cls:
        attrs['className'] = cls
    a = ' %s' % _j(attrs) if attrs else ''
    tag = 'ol' if ordered else 'ul'
    li = '\n\n'.join('<!-- wp:list-item -->\n<li>%s</li>\n<!-- /wp:list-item -->' % i for i in items)
    return '<!-- wp:list%s -->\n<%s class="%s">%s</%s>\n<!-- /wp:list -->' % (a, tag, _cls('wp-block-list', cls), li, tag)


def ul(items):
    return _list(items)


def ol(items):
    return _list(items, ordered=True)


def check(items):
    return _list(items, cls='gdp-lista-check')


def quote(text, cite=None):
    c = '<cite>%s</cite>' % cite if cite else ''
    return '<!-- wp:quote -->\n<blockquote class="wp-block-quote">%s%s</blockquote>\n<!-- /wp:quote -->' % (p(text), c)


def sep():
    return '<!-- wp:separator {"className":"is-style-wide"} -->\n<hr class="wp-block-separator has-alpha-channel-opacity is-style-wide"/>\n<!-- /wp:separator -->'


# --- tabele --------------------------------------------------------------

def table(head, rows, caption=None, numeric=False, wide=None):
    """Tabela z <thead>. Tabele o 4+ kolumnach domyślnie alignwide (D23)."""
    attrs = {'hasFixedLayout': False}
    cls = 'wp-block-table'
    if wide is None:
        wide = len(head) >= 4
    if wide:
        attrs['align'] = 'wide'
        cls += ' alignwide'
    if numeric:
        attrs['className'] = 'gdp-liczby'
        cls += ' gdp-liczby'
    th = ''.join('<th>%s</th>' % c for c in head)
    tb = ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % c for c in r) for r in rows)
    cap = '<figcaption class="wp-element-caption">%s</figcaption>' % caption if caption else ''
    return '<!-- wp:table %s -->\n<figure class="%s"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>%s</figure>\n<!-- /wp:table -->' % (_j(attrs), cls, th, tb, cap)


# --- układ ---------------------------------------------------------------

def col(*inner, cls=None):
    attrs = {'className': cls} if cls else {}
    a = ' %s' % _j(attrs) if attrs else ''
    return '<!-- wp:column%s -->\n<div class="%s">%s</div>\n<!-- /wp:column -->' % (a, _cls('wp-block-column', cls), '\n\n'.join(x for x in inner if x))


def cols(*columns, wide=True):
    attrs = {'align': 'wide'} if wide else {}
    a = ' %s' % _j(attrs) if attrs else ''
    return '<!-- wp:columns%s -->\n<div class="%s">%s</div>\n<!-- /wp:columns -->' % (a, _cls('wp-block-columns', 'alignwide' if wide else None), '\n\n'.join(columns))


def cards(items, wide=True, highlight=None):
    """items: lista dict {label?, title, text|texts, button?: (tekst, href)}. Zwraca kolumny-karty."""
    out = []
    for i, it in enumerate(items):
        inner = []
        if it.get('label'):
            inner.append(label(it['label']))
        inner.append(h3(it['title']))
        for t in it.get('texts', [it.get('text')] if it.get('text') else []):
            inner.append(p(t))
        if it.get('items'):
            inner.append(ul(it['items']))
        if it.get('button'):
            inner.append(buttons([it['button']]))
        cls = 'gdp-karta' + (' gdp-karta-wyrozniona' if highlight == i else '')
        out.append(col(*inner, cls=cls))
    return cols(*out, wide=wide)


def steps(items, wide=True):
    """items: lista (tytuł, opis). Kolumny z numerem kroku."""
    out = []
    for i, (t, d) in enumerate(items, 1):
        out.append(col(p('%02d' % i, cls='gdp-krok-numer'), h3(t), p(d)))
    return cols(*out, wide=wide)


def two(left, right, wide=True):
    """Dwie kolumny z dowolną zawartością (listy bloków)."""
    return cols(col(*left), col(*right), wide=wide)


def button(text, href, outline=False):
    attrs = {'className': 'is-style-outline'} if outline else {}
    a = ' %s' % _j(attrs) if attrs else ''
    return '<!-- wp:button%s -->\n<div class="%s"><a class="wp-block-button__link wp-element-button" href="%s">%s</a></div>\n<!-- /wp:button -->' % (a, _cls('wp-block-button', 'is-style-outline' if outline else None), href, text)


def buttons(items):
    """items: lista (tekst, href) lub (tekst, href, outline)."""
    return '<!-- wp:buttons -->\n<div class="wp-block-buttons">%s</div>\n<!-- /wp:buttons -->' % '\n\n'.join(button(*it) for it in items)


def details(q, a, name=None):
    attrs = {'metadata': {'name': name}} if name else {}
    at = ' %s' % _j(attrs) if attrs else ''
    body = a if a.startswith('<!-- wp:') else p(a)
    return '<!-- wp:details%s -->\n<details class="wp-block-details"><summary>%s</summary>%s</details>\n<!-- /wp:details -->' % (at, q, body)


def faq(items):
    return '\n\n'.join(details(q, a) for q, a in items)


def ref(slug, overrides=None):
    attrs = {'ref': '__BLOCK:%s__' % slug}
    if overrides:
        attrs['content'] = {k: {'content': v} for k, v in overrides.items()}
    return '<!-- wp:block %s /-->' % _j(attrs)


def query(cat=None, per_page=3, columns=3, query_id=11, excerpt=True, author=False):
    q = {'perPage': per_page, 'pages': 0, 'offset': 0, 'postType': 'post', 'order': 'desc', 'orderBy': 'date',
         'author': '', 'search': '', 'exclude': [], 'sticky': 'exclude', 'inherit': False}
    if cat:
        q['taxQuery'] = {'category': ['__CAT:%s__' % cat]}
    attrs = {'queryId': query_id, 'query': q, 'align': 'wide', 'className': 'gdp-komentarze'}
    tpl = ['<!-- wp:post-date {"fontSize":"xs"} /-->', '<!-- wp:post-title {"level":3,"isLink":true,"fontSize":"m"} /-->']
    if excerpt:
        tpl.append('<!-- wp:post-excerpt {"moreText":"Czytaj dalej","excerptLength":24} /-->')
    if author:
        tpl.append('<!-- wp:post-author-name {"fontSize":"xs"} /-->')
    return ('<!-- wp:query %s -->\n<div class="wp-block-query alignwide gdp-komentarze"><!-- wp:post-template {"layout":{"type":"grid","columnCount":%d}} -->\n%s\n<!-- /wp:post-template --></div>\n<!-- /wp:query -->'
            % (_j(attrs), columns, '\n\n'.join(tpl)))


def search(label_text='Szukaj w bazie wiedzy'):
    return ('<!-- wp:search {"label":"%s","showLabel":false,"placeholder":"Np. okres wypowiedzenia","buttonText":"Szukaj","align":"wide"} /-->' % label_text)


# --- atrapy formularzy i placeholdery ----------------------------------

def field(lbl, hint):
    return p(lbl, cls='gdp-etykieta-pola') + '\n\n' + p(hint, cls='gdp-pole')


def file_field(lbl, hint='Przeciągnij plik tutaj albo wybierz z dysku'):
    return p(lbl, cls='gdp-etykieta-pola') + '\n\n' + p(hint, cls='gdp-pole gdp-pole-plik')


def rodo():
    return helper('Zgoda: [[treść zgody dostarczy zleceniodawca]] · <a href="/polityka-prywatnosci/">Polityka prywatności</a>')


def placeholder(text):
    return p('<span class="gdp-placeholder">%s</span>' % text)


def form_card(title, intro, fields, button_text, href='/kontakt/', name='Formularz (slot)'):
    inner = [h3(title), p(intro)] + fields + [buttons([(button_text, href)]), rodo()]
    return group(*inner, cls='gdp-karta', name=name)


# --- moduły stron --------------------------------------------------------

def crumb(parent_title, parent_href, current):
    return label('<a href="%s">%s</a> · %s' % (parent_href, parent_title, current))


def hero(title, lead_text, btns, crumb_text=None, bg='surface', name='Hero'):
    inner = [crumb_text, h1(title), lead(lead_text), buttons(btns) if btns else None]
    return sec(name, *inner, bg=bg, pad='60', cls='gdp-hero gdp-hero-produkt')


def sources(items, updated='[[data]]', author='[[imię i nazwisko, stanowisko]]', name='Źródła i aktualizacja'):
    li = []
    for it in items:
        if isinstance(it, tuple):
            txt, url = it
            li.append('%s – <a href="%s">%s</a>' % (txt, url, url.replace('https://', '').replace('www.', '').rstrip('/')) if url else '%s – [[link]]' % txt)
        else:
            li.append(it)
    return sec(name, h('Źródła', size='m'), ul(li), helper('Ostatnia aktualizacja: %s · Autor: %s' % (updated, author)), pad='50')


def cta_end(bg='surface'):
    return sec('CTA końcowe', ref('cta-wgraj-fakture'), bg=bg, pad='80')


def toc(entries):
    """entries: lista (tekst, anchor)."""
    return ul(['<a href="#%s">%s</a>' % (a, t) for t, a in entries])


def anchor(text):
    return _slug(text)


SRC = {
    'pe': ('Ustawa z dnia 10 kwietnia 1997 r. – Prawo energetyczne (tekst jednolity)', 'https://isap.sejm.gov.pl'),
    'pe_4j': ('Prawo energetyczne, art. 4j (zmiana sprzedawcy, wypowiedzenie umowy)', 'https://isap.sejm.gov.pl'),
    'pe_5aa': ('Prawo energetyczne, art. 5aa–5ab (sprzedaż rezerwowa)', 'https://isap.sejm.gov.pl'),
    'ure': ('Urząd Regulacji Energetyki', 'https://www.ure.gov.pl'),
    'tge': ('Towarowa Giełda Energii, Rynek Terminowy Towarowy gazu i indeksy', 'https://tge.pl'),
    'psg': ('Polska Spółka Gazownictwa, Instrukcja Ruchu i Eksploatacji Sieci Dystrybucyjnej', 'https://www.psgaz.pl'),
    'kc': ('Kodeks cywilny (przepisy o zobowiązaniach umownych)', 'https://isap.sejm.gov.pl'),
    'uodo': ('Urząd Ochrony Danych Osobowych', 'https://uodo.gov.pl'),
    'kobize': ('Krajowy Ośrodek Bilansowania i Zarządzania Emisjami', 'https://www.kobize.pl'),
    'csrd': ('Dyrektywa (UE) 2022/2464 (CSRD) i standardy ESRS', 'https://eur-lex.europa.eu'),
    'ets': ('Dyrektywa 2003/87/WE (EU ETS) i ustawa o systemie handlu uprawnieniami do emisji', 'https://eur-lex.europa.eu'),
    'red': ('Dyrektywa (UE) 2018/2001 (RED II/III), kryteria zrównoważonego rozwoju biometanu', 'https://eur-lex.europa.eu'),
}

#!/usr/bin/env python3
"""
Weryfikacja 13.6: zbiera wszystkie placeholdery [[ ]] z treści (content/site.A.wxr – treść jest wspólna
dla kierunków), widgetów stopki (config/footer.json), wzorców (theme/gdp-child/patterns) i theme mods,
z lokalizacją (strona › sekcja). Zapisuje docs/open-items.md oraz sprawdza zakazane frazy z sekcji 10.1.

    python3 scripts/open-items.py [--out docs/open-items.md]
"""
import glob
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NS = {'content': 'http://purl.org/rss/1.0/modules/content/', 'wp': 'http://wordpress.org/export/1.2/'}
PLACEHOLDER = re.compile(r'\[\[(.*?)\]\]', re.S)
FORBIDDEN = ['w dzisiejszych czasach', 'kompleksowe rozwiązania', 'lider rynku', 'innowacyjn', 'game-changer', '!']
TAG = re.compile(r'<[^>]+>')


def sections(content):
    """Dzieli treść na sekcje nadrzędne (core/group z metadata.name) → [(nazwa, tekst)]."""
    token = re.compile(r'<!--\s+(/?)wp:([a-z0-9-]+/)?([a-z0-9-]+)(\s+(\{.*?\}))?\s+(/)?-->', re.S)
    out, depth, cur, start = [], 0, '(poza sekcją)', 0
    for m in token.finditer(content):
        closing, _, name, _, attrs, selfclose = m.groups()
        if not closing and depth == 0:
            nm = '(sekcja bez nazwy)'
            if attrs:
                try:
                    nm = json.loads(attrs).get('metadata', {}).get('name', nm)
                except json.JSONDecodeError:
                    pass
            cur, start = nm, m.start()
        if closing:
            depth -= 1
            if depth == 0:
                out.append((cur, content[start:m.end()]))
        elif not selfclose:
            depth += 1
        elif depth == 0:
            out.append((cur, content[m.start():m.end()]))
    return out or [('(całość)', content)]


def main():
    out_path = os.path.join(ROOT, 'docs', 'open-items.md')
    if '--out' in sys.argv:
        out_path = sys.argv[sys.argv.index('--out') + 1]
    items = OrderedDict()  # tekst placeholdera → lista lokalizacji
    forbidden_hits = []

    def scan(where, content):
        for sec, body in sections(content):
            text = TAG.sub(' ', body)
            for ph in PLACEHOLDER.findall(text):
                key = '[[%s]]' % ' '.join(ph.split())
                items.setdefault(key, []).append('%s › %s' % (where, sec))
            plain = PLACEHOLDER.sub('', text).lower()
            for f in FORBIDDEN:
                if f in plain:
                    forbidden_hits.append('%s › %s: „%s”' % (where, sec, f))

    tree = ET.parse(os.path.join(ROOT, 'content', 'site.A.wxr'))
    for item in tree.getroot().iter('item'):
        kind = item.find('wp:post_type', NS).text
        title = item.find('title').text or ''
        label = {'page': 'Strona', 'post': 'Wpis', 'wp_block': 'Wzorzec zsynchronizowany'}.get(kind, kind)
        scan('%s „%s”' % (label, title), item.find('content:encoded', NS).text or '')
        if kind != 'wp_block':
            scan('%s „%s” (tytuł)' % (label, title), title)
    footer = json.load(open(os.path.join(ROOT, 'config', 'footer.json'), encoding='utf-8'))
    for k, v in footer['widgets'].items():
        scan('Stopka › %s' % k, v)
    for php in sorted(glob.glob(os.path.join(ROOT, 'theme', 'gdp-child', 'patterns', '*.php'))):
        scan('Wzorzec (niezsynchronizowany) %s' % os.path.basename(php), open(php, encoding='utf-8').read().split('?>', 1)[-1])
    mods = json.load(open(os.path.join(ROOT, 'config', 'theme_mods_C.json'), encoding='utf-8'))
    scan('Customizer (theme mods, np. pasek górny C)', json.dumps(mods, ensure_ascii=False))
    for f in ('README.md',):
        p = os.path.join(ROOT, f)
        if os.path.exists(p):
            pass  # dokumentacja nie jest treścią serwisu

    lines = ['# Otwarte pozycje – dane do uzupełnienia przez zleceniodawcę', '',
             'Wygenerowano skryptem `scripts/open-items.py` z treści serwisu (etap 1). Każdy wpis to placeholder `[[ ]]`, '
             'który w treści zastąpisz własnymi danymi. Liczby, ceny, numery koncesji i fakty nie zostały wymyślone.', '',
             'Łącznie unikalnych placeholderów: **%d**, wystąpień: **%d**.' % (len(items), sum(len(v) for v in items.values())), '',
             '| # | Placeholder | Wystąpienia | Lokalizacja (strona › sekcja) |', '|---|---|---|---|']
    for i, (k, locs) in enumerate(sorted(items.items(), key=lambda kv: -len(kv[1])), 1):
        uniq = list(OrderedDict.fromkeys(locs))
        shown = '; '.join(uniq[:4]) + (' … (+%d)' % (len(uniq) - 4) if len(uniq) > 4 else '')
        lines.append('| %d | `%s` | %d | %s |' % (i, k.replace('|', '\\|'), len(locs), shown.replace('|', '\\|')))
    lines += ['', '## Zakazane frazy (sekcja 10.1)', '']
    if forbidden_hits:
        lines += ['- ' + h for h in forbidden_hits]
    else:
        lines.append('Brak wystąpień fraz z listy zakazanych (w tym wykrzykników) w treści serwisu.')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    open(out_path, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print('placeholdery: %d unikalnych, %d wystąpień; zakazane frazy: %d → %s' % (len(items), sum(len(v) for v in items.values()), len(forbidden_hits), out_path))
    for h in forbidden_hits:
        print('  -', h)
    sys.exit(1 if forbidden_hits else 0)


if __name__ == '__main__':
    main()

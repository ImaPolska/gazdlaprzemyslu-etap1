#!/usr/bin/env python3
"""
Weryfikacja 13.1 – bloki. Przechodzi post_content wszystkich page/post/wp_block w plikach WXR
(content/site.*.wxr) oraz wzorce PHP (theme/gdp-child/patterns/*.php) i treść widgetów stopki (config/footer.json).

Raportuje: core/html, core/freeform, core/shortcode, wzorzec shortcode [a-z_]+, bloki spoza core/*
(oczekiwane 0,0,0,0,0), a dodatkowo: dokładnie jeden h1 na stronę, templateLock:contentOnly
na każdej sekcji nadrzędnej strony.

    python3 scripts/verify-blocks.py [--json docs/verify/blocks.json]
Kod wyjścia 1 przy jakimkolwiek naruszeniu.
"""
import glob
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NS = {'content': 'http://purl.org/rss/1.0/modules/content/', 'wp': 'http://wordpress.org/export/1.2/'}

BLOCK_OPEN = re.compile(r'<!--\s+wp:([a-z0-9-]+/)?([a-z0-9-]+)(\s+(\{.*?\}))?\s+(/)?-->', re.S)
# Shortcode: [nazwa ...] – z wyłączeniem placeholderów [[ ]] i pustych nawiasów.
SHORTCODE = re.compile(r'(?<!\[)\[([a-z_]+)(\s[^\]]*)?\](?!\])')
FREEFORM_HINT = re.compile(r'<!--\s+wp:freeform')


def parse_blocks(content):
    """Zwraca listę (name, attrs, depth) dla każdego otwarcia bloku oraz listę bloków najwyższego poziomu."""
    blocks, top = [], []
    depth = 0
    pos = 0
    token = re.compile(r'<!--\s+(/?)wp:([a-z0-9-]+/)?([a-z0-9-]+)(\s+(\{.*?\}))?\s+(/)?-->', re.S)
    for m in token.finditer(content):
        closing, ns, name, _, attrs, selfclose = m.groups()
        full = (ns or 'core/') + name
        if closing:
            depth -= 1
            continue
        a = {}
        if attrs:
            try:
                a = json.loads(attrs)
            except json.JSONDecodeError:
                a = {'__parse_error__': True}
        blocks.append((full, a, depth))
        if depth == 0:
            top.append((full, a))
        if not selfclose:
            depth += 1
    return blocks, top


def count_freeform(content):
    """Liczy fragmenty niebiałego tekstu poza blokami (na głębokości 0)."""
    token = re.compile(r'<!--\s+(/?)wp:([a-z0-9-]+/)?([a-z0-9-]+)(\s+(\{.*?\}))?\s+(/)?-->', re.S)
    depth, last_end, count = 0, 0, 0
    for m in token.finditer(content):
        closing, _, _, _, _, selfclose = m.groups()
        if depth == 0 and content[last_end:m.start()].strip():
            count += 1
        if closing:
            depth -= 1
        elif not selfclose:
            depth += 1
        if depth == 0:
            last_end = m.end()
    if content[last_end:].strip() and depth == 0:
        count += 1
    return count


def strip_block_text(content):
    """Treść bez komentarzy blokowych i bez markupu – do wyszukiwania shortcode'ów."""
    no_comments = re.sub(r'<!--.*?-->', '', content, flags=re.S)
    return no_comments


def check_item(kind, title, content):
    res = {'kind': kind, 'title': title, 'core/html': 0, 'core/freeform': 0, 'core/shortcode': 0, 'shortcode_pattern': 0,
           'non_core': [], 'h1': None, 'sections_without_lock': [], 'parse_errors': 0}
    blocks, top = parse_blocks(content)
    for name, attrs, depth in blocks:
        if name == 'core/html':
            res['core/html'] += 1
        elif name == 'core/freeform':
            res['core/freeform'] += 1
        elif name == 'core/shortcode':
            res['core/shortcode'] += 1
        if not name.startswith('core/'):
            res['non_core'].append(name)
        if attrs.get('__parse_error__'):
            res['parse_errors'] += 1
    # Treść luzem poza blokami najwyższego poziomu = klasyczny blok (core/freeform).
    res['core/freeform'] += count_freeform(content)
    res['shortcode_pattern'] = len(SHORTCODE.findall(strip_block_text(content)))
    if kind == 'page':
        res['h1'] = len(re.findall(r'<h1[\s>]', content))
        for name, attrs in top:
            if name == 'core/group' and attrs.get('templateLock') != 'contentOnly':
                res['sections_without_lock'].append(attrs.get('metadata', {}).get('name', '(bez nazwy)'))
            elif name != 'core/group':
                res['sections_without_lock'].append('%s (nie jest core/group)' % name)
    return res


def items_from_wxr(path):
    tree = ET.parse(path)
    for item in tree.getroot().iter('item'):
        kind = item.find('wp:post_type', NS).text
        title = item.find('title').text or ''
        content = item.find('content:encoded', NS).text or ''
        yield kind, title, content


def main():
    out_json = None
    if '--json' in sys.argv:
        out_json = sys.argv[sys.argv.index('--json') + 1]
    report = {'files': {}, 'totals': {'core/html': 0, 'core/freeform': 0, 'core/shortcode': 0, 'shortcode_pattern': 0, 'non_core': 0},
              'violations': []}
    sources = []
    for wxr in sorted(glob.glob(os.path.join(ROOT, 'content', 'site.*.wxr'))):
        sources.append((os.path.relpath(wxr, ROOT), list(items_from_wxr(wxr))))
    patterns = []
    for php in sorted(glob.glob(os.path.join(ROOT, 'theme', 'gdp-child', 'patterns', '*.php'))):
        body = open(php, encoding='utf-8').read().split('?>', 1)[-1]
        patterns.append(('pattern', os.path.basename(php), body))
    sources.append(('theme/gdp-child/patterns', patterns))
    footer = json.load(open(os.path.join(ROOT, 'config', 'footer.json'), encoding='utf-8'))
    sources.append(('config/footer.json', [('widget', k, v) for k, v in footer['widgets'].items()]))

    for src, items in sources:
        rows = []
        for kind, title, content in items:
            r = check_item(kind, title, content)
            rows.append(r)
            for k in ('core/html', 'core/freeform', 'core/shortcode', 'shortcode_pattern'):
                report['totals'][k] += r[k]
                if r[k]:
                    report['violations'].append('%s › %s: %s = %d' % (src, title, k, r[k]))
            report['totals']['non_core'] += len(r['non_core'])
            if r['non_core']:
                report['violations'].append('%s › %s: bloki spoza core: %s' % (src, title, ', '.join(sorted(set(r['non_core'])))))
            if r['parse_errors']:
                report['violations'].append('%s › %s: błędne JSON atrybutów bloku (%d)' % (src, title, r['parse_errors']))
            if kind == 'page':
                if r['h1'] != 1:
                    report['violations'].append('%s › %s: h1 = %s (oczekiwane 1)' % (src, title, r['h1']))
                if r['sections_without_lock']:
                    report['violations'].append('%s › %s: sekcje bez templateLock:contentOnly: %s' % (src, title, ', '.join(r['sections_without_lock'])))
        report['files'][src] = {'items': len(rows), 'pages': sum(1 for r in rows if r['kind'] == 'page'),
                                'posts': sum(1 for r in rows if r['kind'] == 'post'), 'wp_block': sum(1 for r in rows if r['kind'] == 'wp_block')}

    t = report['totals']
    print('13.1 Bloki – core/html: %d, core/freeform: %d, core/shortcode: %d, shortcode [a-z_]+: %d, spoza core/*: %d (oczekiwane 0, 0, 0, 0, 0)'
          % (t['core/html'], t['core/freeform'], t['core/shortcode'], t['shortcode_pattern'], t['non_core']))
    for src, f in report['files'].items():
        print('  %s: %d elementów (stron %d, wpisów %d, wzorców zsynchronizowanych %d)' % (src, f['items'], f['pages'], f['posts'], f['wp_block']))
    if report['violations']:
        print('NARUSZENIA:')
        for v in report['violations']:
            print('  -', v)
    else:
        print('  h1: dokładnie jeden na każdej stronie; templateLock: contentOnly na każdej sekcji nadrzędnej – OK')
    if out_json:
        os.makedirs(os.path.dirname(out_json), exist_ok=True)
        json.dump(report, open(out_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    sys.exit(1 if report['violations'] else 0)


if __name__ == '__main__':
    main()

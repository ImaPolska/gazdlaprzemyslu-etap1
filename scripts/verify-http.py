#!/usr/bin/env python3
"""
Weryfikacja 13.2 (część HTTP): sprawdza kod odpowiedzi dla wszystkich URL z mapy serwisu
(strony z content/pages.json, wpisy, archiwa kategorii, /wiedza/) na działającym Playground,
a następnie czyta debug.log (jeżeli podano --debug-log) i raportuje notice/warning.

    python3 scripts/verify-http.py --base http://127.0.0.1:9400 --dir A [--debug-log tmp/out/debug.log] [--json docs/verify/http-A.json]
Kod wyjścia 1 przy kodzie != 200 albo wpisach w debug.log.
"""
import argparse
import http.cookiejar
import json
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sitemap_urls():
    d = json.load(open(os.path.join(ROOT, 'content', 'pages.json'), encoding='utf-8'))
    by_slug = {p['slug']: p for p in d['pages']}
    urls = []
    for p in d['pages']:
        if p['slug'] == 'start':
            urls.append('/')
            continue
        parts = [p['slug']]
        parent = p.get('parent')
        while parent:
            parts.insert(0, parent)
            parent = by_slug[parent].get('parent')
        urls.append('/' + '/'.join(parts) + '/')
    for c in d['categories']:
        urls.append('/category/%s/' % c['slug'])
    for post in d['posts']:
        urls.append('/wiedza/%s/' % post['slug'])
    return urls


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default='http://127.0.0.1:9400')
    ap.add_argument('--dir', default='')
    ap.add_argument('--debug-log', default='')
    ap.add_argument('--json', default='')
    a = ap.parse_args()
    base = a.base.rstrip('/')
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    # Pierwsze wejście: auto-login Playground (302), potem czyścimy ciasteczka – test jako gość.
    opener.open(base + '/', timeout=120).read()
    cj.clear()
    results = []
    for path in sitemap_urls():
        try:
            r = opener.open(base + path, timeout=120)
            code = r.getcode()
            body = r.read().decode('utf-8', 'replace')
            final = r.geturl()
        except urllib.error.HTTPError as e:
            code, body, final = e.code, '', e.geturl()
        h1 = body.count('<h1')
        results.append({'url': path, 'status': code, 'final': final.replace(base, ''), 'h1': h1})
        print('%s %-40s h1=%d%s' % (code, path, h1, '' if final.replace(base, '') == path else ' -> ' + final.replace(base, '')))
    bad = [r for r in results if r['status'] != 200]
    log_lines = []
    if a.debug_log:
        if os.path.exists(a.debug_log):
            log_lines = [l for l in open(a.debug_log, encoding='utf-8', errors='replace').read().splitlines() if l.strip()]
        print('debug.log: %d wpisów' % len(log_lines))
        for l in log_lines[:40]:
            print('  ', l[:300])
    summary = {'direction': a.dir, 'total': len(results), 'ok': len(results) - len(bad), 'not_200': bad,
               'debug_log_entries': len(log_lines), 'debug_log': log_lines[:200], 'results': results}
    print('HTTP 200: %d/%d' % (summary['ok'], summary['total']))
    if a.json:
        os.makedirs(os.path.dirname(a.json), exist_ok=True)
        json.dump(summary, open(a.json, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    sys.exit(1 if bad or log_lines else 0)


if __name__ == '__main__':
    main()

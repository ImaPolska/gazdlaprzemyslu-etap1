#!/usr/bin/env python3
"""
Zrzuty ekranu (desktop 1440×900, mobile 360×800, pełna strona) z działającej instancji Playground.

    python3 scripts/screenshot.py --base http://127.0.0.1:9400 --dir A --out docs/screens
Tworzy: {out}/{dir}-start-desktop.png, {dir}-start-mobile.png, {dir}-cena-stala-desktop.png, {dir}-cena-stala-mobile.png
Dodatkowo (do QA, nie do raportu): --extra dodaje zrzuty kadru hero (viewport) i menu mobilnego.
"""
import argparse
import os
import sys

from playwright.sync_api import sync_playwright



def _pages():
    """Mapa nazwa -> ścieżka z content/pages.json (strony wg hierarchii, wpisy pod /wiedza/)."""
    import json
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    d = json.load(open(os.path.join(root, 'content', 'pages.json'), encoding='utf-8'))
    by_slug = {p['slug']: p for p in d['pages']}
    out = {'start': '/'}
    for p in d['pages']:
        if p['slug'] == 'start':
            continue
        parts, parent = [p['slug']], p.get('parent')
        while parent:
            parts.insert(0, parent)
            parent = by_slug[parent].get('parent')
        out[p['slug']] = '/' + '/'.join(parts) + '/'
    for post in d['posts']:
        out[post['slug']] = '/wiedza/%s/' % post['slug']
    return out


PAGES = _pages()
VIEWPORTS = {'desktop': (1440, 900), 'mobile': (360, 800)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default='http://127.0.0.1:9400')
    ap.add_argument('--dir', required=True)
    ap.add_argument('--out', default='docs/screens')
    ap.add_argument('--extra', action='store_true')
    ap.add_argument('--pages', default='start,cena-stala')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for vp, (w, h) in VIEWPORTS.items():
            ctx = browser.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1, locale='pl-PL',
                                      is_mobile=(vp == 'mobile'), has_touch=(vp == 'mobile'))
            page = ctx.new_page()
            page.on('console', lambda m: errors.append('console[%s] %s' % (m.type, m.text)) if m.type == 'error' else None)
            page.on('pageerror', lambda e: errors.append('pageerror %s' % e))
            # Pierwsze wejście wykonuje auto-login Playground; potem czyścimy ciasteczka,
            # aby zrzuty pokazywały widok niezalogowanego gościa (bez paska admina).
            page.goto(a.base + '/', wait_until='networkidle', timeout=120000)
            ctx.clear_cookies()
            for name in a.pages.split(','):
                path = PAGES[name]
                page.goto(a.base + path, wait_until='networkidle', timeout=120000)
                page.add_style_tag(content='#wpadminbar{display:none!important} html{margin-top:0!important}')
                page.evaluate('document.documentElement.classList.remove("gdp-scrolled")')
                page.wait_for_timeout(600)
                # Wymuś załadowanie fontów.
                page.evaluate('document.fonts.ready')
                out = os.path.join(a.out, '%s-%s-%s.png' % (a.dir, name, vp))
                page.screenshot(path=out, full_page=True)
                print('zrzut:', out)
                if a.extra:
                    page.evaluate('window.scrollTo(0,0)')
                    page.wait_for_timeout(300)
                    page.screenshot(path=os.path.join(a.out, 'qa-%s-%s-%s-hero.png' % (a.dir, name, vp)), full_page=False)
                    if vp == 'mobile' and name == 'start':
                        trig = page.locator('[data-id="trigger"] button, .ct-header-trigger').first
                        if trig.count():
                            trig.click()
                            page.wait_for_timeout(700)
                            page.screenshot(path=os.path.join(a.out, 'qa-%s-menu-mobile.png' % a.dir), full_page=False)
            ctx.close()
        browser.close()
    if errors:
        print('BŁĘDY KONSOLI:')
        for e in errors:
            print(' ', e)
    else:
        print('konsola: bez błędów')


if __name__ == '__main__':
    main()

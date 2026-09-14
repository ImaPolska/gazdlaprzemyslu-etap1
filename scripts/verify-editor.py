#!/usr/bin/env python3
"""Otwiera edytor bloków dla wskazanych stron na lokalnym Playground i liczy ostrzeżenia o nieprawidłowych blokach.
    python3 scripts/verify-editor.py --base http://127.0.0.1:9400 --ids 1001,1004,1018
"""
import argparse, sys
from playwright.sync_api import sync_playwright
ap = argparse.ArgumentParser(); ap.add_argument('--base', default='http://127.0.0.1:9400'); ap.add_argument('--ids', default='1001,1004')
a = ap.parse_args(); bad = 0
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={'width': 1440, 'height': 900}); page = ctx.new_page()
    page.goto(a.base + '/', wait_until='domcontentloaded', timeout=120000)  # auto-login
    for pid in a.ids.split(','):
        page.goto('%s/wp-admin/post.php?post=%s&action=edit' % (a.base, pid), wait_until='domcontentloaded', timeout=180000)  # edytor odpytuje REST cyklicznie, networkidle nie nastąpi
        page.wait_for_selector('iframe[name="editor-canvas"], .block-editor-block-list__layout', timeout=120000)
        page.wait_for_timeout(4000)
        # Zamknij ewentualny modal powitalny.
        for fr in [page] + page.frames:
            try:
                n = fr.locator('.block-editor-warning, .block-editor-block-list__block.has-warning').count()
            except Exception:
                n = 0
            if n:
                bad += n; print('strona %s: %d ostrzeżeń w %s' % (pid, n, 'ramce' if fr is not page else 'dokumencie'))
        blocks = 0
        for fr in page.frames:
            try: blocks = max(blocks, fr.locator('[data-block]').count())
            except Exception: pass
        print('strona %s: bloków w edytorze %d, ostrzeżeń %d' % (pid, blocks, bad))
        page.screenshot(path='tmp/qa/editor-%s.png' % pid)
    b.close()
sys.exit(1 if bad else 0)

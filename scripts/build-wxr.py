#!/usr/bin/env python3
"""
Buduje pliki WXR (WordPress eXtended RSS 1.2) z treści w content/.

Użycie:
    python3 scripts/build-wxr.py            # content/site.A.wxr, site.B.wxr, site.C.wxr
    python3 scripts/build-wxr.py A          # tylko jeden kierunek

Trzy pliki różnią się wyłącznie sekcją hero strony głównej (content/pages/start.hero.{A,B,C}.html).
Odwołania do wzorców zsynchronizowanych ("ref":"__BLOCK:slug__") i kategorii ("__CAT:slug__")
rozwiązuje po imporcie scripts/apply-config.php (ID po imporcie nie są gwarantowane).
"""
import json
import os
import sys
from datetime import datetime
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, 'content')
MANIFEST = json.load(open(os.path.join(CONTENT, 'pages.json'), encoding='utf-8'))

SITE_URL = 'https://gazdlaprzemyslu.pl'  # tylko do pól WXR; Playground zapisuje własny host
AUTHOR = {'login': 'redaktor', 'email': 'redaktor@example.invalid', 'display': 'Zespół analiz PBM'}
NOW = '2026-09-13 12:00:00'


def cdata(text):
    return '<![CDATA[' + text.replace(']]>', ']]]]><![CDATA[>') + ']]>'


def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read().strip()


def stub_content(page):
    """Strona robocza: jeden H1, akapit z zakresem P1.2, opcjonalnie slot i CTA."""
    parts = []
    inner = []
    inner.append('<!-- wp:heading {"level":1} -->\n<h1 class="wp-block-heading">%s</h1>\n<!-- /wp:heading -->' % escape_html(page['title']))
    inner.append('<!-- wp:paragraph {"fontSize":"m"} -->\n<p class="has-m-font-size">Strona robocza etapu 1. Zakres w P1.2: %s</p>\n<!-- /wp:paragraph -->' % escape_html(page['stub']))
    parts.append(section('Nagłówek strony', inner, bg='surface', pad='60'))
    if page.get('slot'):
        parts.append(section('Slot', ['<!-- wp:block {"ref":"__BLOCK:%s__"} /-->' % page['slot']]))
    if page.get('query'):
        q = ('<!-- wp:query {"queryId":21,"query":{"perPage":10,"pages":0,"offset":0,"postType":"post","order":"desc","orderBy":"date","author":"","search":"","exclude":[],"sticky":"exclude","inherit":false,"taxQuery":{"category":["__CAT:%s__"]}},"align":"wide","className":"gdp-komentarze"} -->\n'
             '<div class="wp-block-query alignwide gdp-komentarze"><!-- wp:post-template {"layout":{"type":"grid","columnCount":3}} -->\n'
             '<!-- wp:post-date {"fontSize":"xs"} /-->\n\n<!-- wp:post-title {"level":2,"isLink":true} /-->\n\n<!-- wp:post-excerpt {"moreText":"Czytaj komentarz","excerptLength":24} /-->\n'
             '<!-- /wp:post-template --></div>\n<!-- /wp:query -->') % page['query']
        parts.append(section('Lista wpisów', [q]))
    if page['slug'] not in ('polityka-prywatnosci', 'regulamin', 'wiedza'):
        parts.append(section('CTA końcowe', ['<!-- wp:block {"ref":"__BLOCK:cta-wgraj-fakture__"} /-->'], bg='surface', pad='80'))
    return '\n\n'.join(parts)


def escape_html(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def section(name, inner, bg=None, pad='70'):
    attrs = {'metadata': {'name': name}, 'templateLock': 'contentOnly', 'align': 'full',
             'style': {'spacing': {'padding': {'top': 'var:preset|spacing|%s' % pad, 'bottom': 'var:preset|spacing|%s' % pad}}}}
    cls = 'wp-block-group alignfull'
    if bg:
        attrs['backgroundColor'] = bg
        cls += ' has-%s-background-color has-background' % bg
    attrs['layout'] = {'type': 'constrained'}
    return ('<!-- wp:group %s -->\n<div class="%s" style="padding-top:var(--wp--preset--spacing--%s);padding-bottom:var(--wp--preset--spacing--%s)">%s</div>\n<!-- /wp:group -->'
            % (json.dumps(attrs, ensure_ascii=False, separators=(',', ':')), cls, pad, pad, '\n\n'.join(inner)))


def post_content(direction):
    """Zwraca listę item-ów (dict) dla WXR."""
    items = []
    by_slug = {p['slug']: p for p in MANIFEST['pages']}

    # 1. Wzorce zsynchronizowane (najpierw, żeby importer miał je przed stronami).
    for b in MANIFEST['blocks']:
        items.append({
            'id': b['id'], 'title': b['title'], 'slug': b['slug'], 'type': 'wp_block', 'status': 'publish',
            'content': read(os.path.join(CONTENT, 'blocks', b['file'])), 'parent': 0, 'date': NOW, 'meta': {'wp_pattern_sync_status': ''},
        })

    # 2. Strony.
    for p in MANIFEST['pages']:
        if 'file' in p:
            content = read(os.path.join(CONTENT, 'pages', p['file']))
            if '__HERO__' in content:
                hero = read(os.path.join(CONTENT, 'pages', 'start.hero.%s.html' % direction))
                content = content.replace('__HERO__', hero)
        else:
            content = stub_content(p)
        parent = by_slug[p['parent']]['id'] if p.get('parent') else 0
        items.append({'id': p['id'], 'title': p['title'], 'slug': p['slug'], 'type': 'page', 'status': 'publish',
                      'content': content, 'parent': parent, 'date': NOW, 'menu_order': p.get('menu_order', 0)})

    # 3. Wpisy: artykuły bazy wiedzy i szablony komentarzy (treść z content/posts/<file>, generowana przez build-pages.py).
    for post in MANIFEST['posts']:
        body = read(os.path.join(CONTENT, 'posts', post['file']))
        items.append({'id': post['id'], 'title': post['title'], 'slug': post['slug'], 'type': 'post', 'status': 'publish',
                      'content': body, 'excerpt': post['excerpt'], 'parent': 0, 'date': post['date'], 'category': post['category']})
    return items


def item_xml(it):
    cats = {c['slug']: c for c in MANIFEST['categories']}
    dt = datetime.strptime(it['date'], '%Y-%m-%d %H:%M:%S')
    link = SITE_URL + ('/wiedza/' if it['type'] == 'post' else '/') + it['slug'] + '/'
    xml = ['\t<item>',
           '\t\t<title>%s</title>' % cdata(it['title']),
           '\t\t<link>%s</link>' % link,
           '\t\t<pubDate>%s</pubDate>' % dt.strftime('%a, %d %b %Y %H:%M:%S +0000'),
           '\t\t<dc:creator>%s</dc:creator>' % cdata(AUTHOR['login']),
           '\t\t<guid isPermaLink="false">%s/?p=%d</guid>' % (SITE_URL, it['id']),
           '\t\t<description></description>',
           '\t\t<content:encoded>%s</content:encoded>' % cdata(it['content']),
           '\t\t<excerpt:encoded>%s</excerpt:encoded>' % cdata(it.get('excerpt', '')),
           '\t\t<wp:post_id>%d</wp:post_id>' % it['id'],
           '\t\t<wp:post_date>%s</wp:post_date>' % cdata(it['date']),
           '\t\t<wp:post_date_gmt>%s</wp:post_date_gmt>' % cdata(it['date']),
           '\t\t<wp:post_modified>%s</wp:post_modified>' % cdata(it['date']),
           '\t\t<wp:post_modified_gmt>%s</wp:post_modified_gmt>' % cdata(it['date']),
           '\t\t<wp:comment_status>%s</wp:comment_status>' % cdata('closed'),
           '\t\t<wp:ping_status>%s</wp:ping_status>' % cdata('closed'),
           '\t\t<wp:post_name>%s</wp:post_name>' % cdata(it['slug']),
           '\t\t<wp:status>%s</wp:status>' % cdata(it['status']),
           '\t\t<wp:post_parent>%d</wp:post_parent>' % it['parent'],
           '\t\t<wp:menu_order>%d</wp:menu_order>' % it.get('menu_order', 0),
           '\t\t<wp:post_type>%s</wp:post_type>' % cdata(it['type']),
           '\t\t<wp:post_password>%s</wp:post_password>' % cdata(''),
           '\t\t<wp:is_sticky>0</wp:is_sticky>']
    if it.get('category'):
        c = cats[it['category']]
        xml.append('\t\t<category domain="category" nicename="%s">%s</category>' % (c['slug'], cdata(c['name'])))
    for k, v in it.get('meta', {}).items():
        xml.append('\t\t<wp:postmeta>\n\t\t\t<wp:meta_key>%s</wp:meta_key>\n\t\t\t<wp:meta_value>%s</wp:meta_value>\n\t\t</wp:postmeta>' % (cdata(k), cdata(v)))
    xml.append('\t</item>')
    return '\n'.join(xml)


def build(direction):
    items = post_content(direction)
    head = ['<?xml version="1.0" encoding="UTF-8" ?>',
            '<!-- Gaz dla Przemysłu – etap 1 – kierunek %s. Plik generowany: scripts/build-wxr.py -->' % direction,
            '<rss version="2.0" xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:wfw="http://wellformedweb.org/CommentAPI/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:wp="http://wordpress.org/export/1.2/">',
            '<channel>',
            '\t<title>Gaz dla Przemysłu</title>',
            '\t<link>%s</link>' % SITE_URL,
            '\t<description>PBM Sp. z o.o., Grupa IMA Polska</description>',
            '\t<pubDate>Sun, 13 Sep 2026 12:00:00 +0000</pubDate>',
            '\t<language>pl-PL</language>',
            '\t<wp:wxr_version>1.2</wp:wxr_version>',
            '\t<wp:base_site_url>%s</wp:base_site_url>' % SITE_URL,
            '\t<wp:base_blog_url>%s</wp:base_blog_url>' % SITE_URL,
            '\t<wp:author><wp:author_id>2</wp:author_id><wp:author_login>%s</wp:author_login><wp:author_email>%s</wp:author_email><wp:author_display_name>%s</wp:author_display_name><wp:author_first_name>%s</wp:author_first_name><wp:author_last_name>%s</wp:author_last_name></wp:author>'
            % (cdata(AUTHOR['login']), cdata(AUTHOR['email']), cdata(AUTHOR['display']), cdata(''), cdata(''))]
    for c in MANIFEST['categories']:
        head.append('\t<wp:category><wp:term_id>%d</wp:term_id><wp:category_nicename>%s</wp:category_nicename><wp:category_parent>%s</wp:category_parent><wp:cat_name>%s</wp:cat_name></wp:category>'
                    % (c['id'], cdata(c['slug']), cdata(''), cdata(c['name'])))
    head.append('\t<generator>gdp/build-wxr.py</generator>')
    body = [item_xml(it) for it in items]
    out = '\n'.join(head + body + ['</channel>', '</rss>', ''])
    path = os.path.join(CONTENT, 'site.%s.wxr' % direction)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(out)
    print('WXR: %s (%d elementów, %d KB)' % (os.path.relpath(path, ROOT), len(items), len(out.encode()) // 1024))


if __name__ == '__main__':
    dirs = sys.argv[1:] or ['A', 'B', 'C']
    for d in dirs:
        build(d)

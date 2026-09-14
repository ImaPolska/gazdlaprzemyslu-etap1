#!/usr/bin/env python3
"""
Generuje markup bloków core z treści źródłowej w Pythonie (content/src/*.py) przy użyciu scripts/gdp_blocks.py.

Wyjście:
    content/pages/<slug>.html   – strony (sekwencja sekcji core/group, contentOnly)
    content/posts/<slug>.html   – artykuły bazy wiedzy i szablony komentarzy
Manifest content/pages.json jest źródłem listy stron; skrypt dopisuje pole "file" stronom, dla których istnieje treść,
oraz aktualizuje sekcję "posts" (tytuł, slug, kategoria, data, excerpt, file) na podstawie content/src/posts.py.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
sys.path.insert(0, os.path.join(ROOT, 'content', 'src'))

import pages_oferta  # noqa: E402
import pages_narzedzia  # noqa: E402
import posts as posts_src  # noqa: E402

CONTENT = os.path.join(ROOT, 'content')
MANIFEST_PATH = os.path.join(CONTENT, 'pages.json')


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text.strip() + '\n')


def main():
    manifest = json.load(open(MANIFEST_PATH, encoding='utf-8'))
    pages = {}
    pages.update(pages_oferta.PAGES)
    pages.update(pages_narzedzia.PAGES)

    by_slug = {p['slug']: p for p in manifest['pages']}
    unknown = sorted(set(pages) - set(by_slug))
    if unknown:
        sys.exit('Nieznane slugi stron (brak w pages.json): %s' % unknown)

    for slug, sections in pages.items():
        write(os.path.join(CONTENT, 'pages', slug + '.html'), '\n\n'.join(s for s in sections if s))
        by_slug[slug]['file'] = slug + '.html'
        by_slug[slug].pop('stub', None)

    # Wpisy: artykuły + szablony komentarzy.
    posts = []
    next_id = 2101
    for slug, post in posts_src.POSTS.items():
        write(os.path.join(CONTENT, 'posts', slug + '.html'), '\n\n'.join(post['body']))
        posts.append({'id': next_id, 'slug': slug, 'title': post['title'], 'category': post['category'],
                      'date': post['date'], 'excerpt': post['excerpt'], 'file': slug + '.html'})
        next_id += 1
    for pid, post in posts_src.KOMENTARZE.items():
        slug = 'komentarz-rynkowy-szablon-%d' % (pid - 2000)
        write(os.path.join(CONTENT, 'posts', slug + '.html'), '\n\n'.join(post['body']))
        posts.append({'id': pid, 'slug': slug, 'title': post['title'], 'category': post['category'],
                      'date': post['date'], 'excerpt': post['excerpt'], 'file': slug + '.html'})
    manifest['posts'] = sorted(posts, key=lambda x: x['date'], reverse=True)

    with open(MANIFEST_PATH, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write('\n')
    missing = [p['slug'] for p in manifest['pages'] if 'file' not in p]
    print('strony z treścią: %d/%d%s' % (len(manifest['pages']) - len(missing), len(manifest['pages']), ('; bez treści: %s' % missing) if missing else ''))
    print('wpisy: %d (artykuły %d, szablony komentarzy %d)' % (len(posts), len(posts_src.POSTS), len(posts_src.KOMENTARZE)))


if __name__ == '__main__':
    main()

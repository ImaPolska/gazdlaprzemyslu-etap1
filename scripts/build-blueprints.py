#!/usr/bin/env python3
"""
Generuje blueprinty WordPress Playground dla kierunków A/B/C.

    python3 scripts/build-blueprints.py --base https://raw.githubusercontent.com/ORG/REPO/etap1-{d}/ --out blueprints/{d}.json
    python3 scripts/build-blueprints.py --base http://127.0.0.1:8777/ --out blueprints/dev/{d}.json [--debug]

{d} w --base i --out jest podmieniane na literę kierunku. --debug dodaje WP_DEBUG/WP_DEBUG_LOG (weryfikacja 13.2).
Hasło użytkownika redaktor: --password (domyślnie zapisane w docs/decisions.md).
"""
import argparse
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def blueprint(direction, base, debug, password, landing='/'):
    def url(path):
        return base.replace('{d}', direction) + path

    def write(dst, path):
        return {'step': 'writeFile', 'path': dst, 'data': {'resource': 'url', 'url': url(path)}}

    steps = [
        # Polski interfejs WP i Blocksy (pakiet językowy z translate.wordpress.org; wymaga features.networking).
        {'step': 'setSiteLanguage', 'language': 'pl_PL'},
        {'step': 'installTheme', 'themeData': {'resource': 'wordpress.org/themes', 'slug': 'blocksy'}, 'options': {'activate': False}},
        {'step': 'installTheme', 'themeData': {'resource': 'url', 'url': url('dist/gdp-child-%s.zip' % direction)}, 'options': {'activate': True}},
        {'step': 'setSiteOptions', 'options': {
            'blogname': 'Gaz dla Przemysłu',
            'blogdescription': 'PBM Sp. z o.o., Grupa IMA Polska',
            'permalink_structure': '/%postname%/',
            'timezone_string': 'Europe/Warsaw',
            'date_format': 'j.m.Y',
            'time_format': 'H:i',
            'blog_public': '0',
            'default_comment_status': 'closed',
            'default_ping_status': 'closed',
            'fresh_site': '0',
        }},
        {'step': 'wp-cli', 'command': 'wp user create redaktor redaktor@example.invalid --role=editor --display_name="Redaktor" --user_pass=%s' % password},
        {'step': 'wp-cli', 'command': 'wp post delete 1 2 3 --force'},
        {'step': 'mkdir', 'path': '/wordpress/gdp-config'},
        write('/wordpress/gdp-config/theme_mods.json', 'config/theme_mods_%s.json' % direction),
        write('/wordpress/gdp-config/menus.json', 'config/menus.json'),
        write('/wordpress/gdp-config/footer.json', 'config/footer.json'),
        write('/wordpress/gdp-config/apply-theme-mods.php', 'scripts/apply-theme-mods.php'),
        write('/wordpress/gdp-config/apply-config.php', 'scripts/apply-config.php'),
        {'step': 'runPHP', 'code': "<?php require '/wordpress/wp-load.php'; require '/wordpress/gdp-config/apply-theme-mods.php';"},
        {'step': 'importWxr', 'file': {'resource': 'url', 'url': url('content/site.%s.wxr' % direction)}, 'importer': 'default'},
        {'step': 'runPHP', 'code': "<?php require '/wordpress/wp-load.php'; require '/wordpress/gdp-config/apply-config.php';"},
    ]
    bp = {
        '$schema': 'https://playground.wordpress.net/blueprint-schema.json',
        'meta': {
            'title': 'Gaz dla Przemysłu – etap 1 – kierunek %s' % direction,
            'description': 'Blocksy (wordpress.org) + motyw potomny gdp-child, bloki core, bez wtyczek. Kierunek wizualny %s.' % direction,
            'author': 'gdp',
        },
        'preferredVersions': {'php': '8.3', 'wp': 'latest'},
        'features': {'networking': True},
        'landingPage': landing,
        'login': True,
        'steps': steps,
    }
    if debug:
        bp['constants'] = {'WP_DEBUG': True, 'WP_DEBUG_LOG': '/gdp-out/debug.log', 'WP_DEBUG_DISPLAY': False}
        # Katalog /gdp-out montujesz z hosta: --mount=tmp/out:/gdp-out (scripts/dev-server.sh).
    return bp


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--debug', action='store_true')
    ap.add_argument('--password', default='Redaktor-Etap1-2026')
    ap.add_argument('--landing', default='/')
    ap.add_argument('dirs', nargs='*', default=['A', 'B', 'C'])
    a = ap.parse_args()
    for d in a.dirs:
        out = os.path.join(ROOT, a.out.replace('{d}', d))
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, 'w', encoding='utf-8') as f:
            json.dump(blueprint(d, a.base, a.debug, a.password, a.landing), f, ensure_ascii=False, indent=2)
            f.write('\n')
        print('blueprint:', os.path.relpath(out, ROOT))

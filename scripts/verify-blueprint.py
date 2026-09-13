#!/usr/bin/env python3
"""
Weryfikacja 13.2 (część schematu): walidacja blueprintów wobec
https://playground.wordpress.net/blueprint-schema.json (JSON Schema).

    python3 scripts/verify-blueprint.py blueprints/A.json blueprints/B.json ... [--schema tmp/blueprint-schema.json]
Schemat jest pobierany, jeżeli plik lokalny nie istnieje. Kod wyjścia 1 przy błędzie walidacji.
Wymaga: pip install jsonschema
"""
import json
import os
import sys
import urllib.request

import jsonschema

SCHEMA_URL = 'https://playground.wordpress.net/blueprint-schema.json'


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    schema_path = 'tmp/blueprint-schema.json'
    if '--schema' in sys.argv:
        schema_path = sys.argv[sys.argv.index('--schema') + 1]
    if not os.path.exists(schema_path):
        os.makedirs(os.path.dirname(schema_path) or '.', exist_ok=True)
        urllib.request.urlretrieve(SCHEMA_URL, schema_path)
    schema = json.load(open(schema_path, encoding='utf-8'))
    validator = jsonschema.Draft7Validator(schema)
    failed = False
    for path in args:
        bp = json.load(open(path, encoding='utf-8'))
        errors = sorted(validator.iter_errors(bp), key=lambda e: list(e.path))
        steps = len(bp.get('steps', []))
        if errors:
            failed = True
            print('%s: BŁĄD (%d), kroków: %d' % (path, len(errors), steps))
            for e in errors[:10]:
                print('   -', '/'.join(str(p) for p in e.path), e.message[:200])
        else:
            print('%s: zgodny ze schematem, kroków: %d' % (path, steps))
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()

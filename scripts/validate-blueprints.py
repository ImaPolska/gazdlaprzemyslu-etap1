#!/usr/bin/env python3
"""Lekka walidacja blueprintów WordPress Playground (A/B/C).

Pełna walidacja schematu JSON (jsonschema) nie działa w tym środowisku,
bo oficjalny schemat Playground nie jest zgodny z metaschematem Draft 2020-12
używanym przez bibliotekę python-jsonschema. Ten skrypt sprawdza więc to,
co da się sprawdzić deterministycznie:

- poprawny JSON,
- znane nazwy kroków i wymagane pola każdego kroku,
- obecność kluczy `landingPage`, `preferredVersions`, `steps`,
- spójność odwołań do plików repozytorium (dist/*.zip, content/site.wxr,
  scripts/playground-setup.php) — czy pliki istnieją lokalnie.

Użycie: python3 scripts/validate-blueprints.py
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLUEPRINTS = ["A", "B", "C"]

# nazwa kroku -> wymagane pola (wg schematu Playground, stan 2026-09)
REQUIRED = {
    "setSiteLanguage": ["language"],
    "installTheme": ["themeData"],
    "installPlugin": ["pluginData"],
    "importWxr": ["file"],
    "writeFile": ["path", "data"],
    "runPHP": ["code"],
    "wp-cli": ["command"],
    "setSiteOptions": ["options"],
    "login": [],
    "activateTheme": ["themeFolderName"],
    "defineWpConfigConsts": ["consts"],
    "mkdir": ["path"],
    "rm": ["path"],
    "cp": ["fromPath", "toPath"],
    "mv": ["fromPath", "toPath"],
    "runSql": ["sql"],
    "importWordPressFiles": ["wordPressFilesZip"],
    "enableMultisite": [],
    "resetData": [],
    "unzip": ["zipFile", "extractToPath"],
    "activatePlugin": ["pluginPath"],
    "updateUserMeta": ["meta", "userId"],
    "setSiteLanguage ": ["language"],
}

RESOURCE_KEYS = {"url", "path", "slug", "wordPressInstallPath", "resource"}


def check_resource(name, value, errors, warnings):
    if not isinstance(value, dict):
        errors.append(f"{name}: odwołanie do pliku musi być obiektem, jest {type(value).__name__}")
        return
    res = value.get("resource")
    if res not in {"url", "wordpress.org/themes", "wordpress.org/plugins", "vfs", "literal", "git:directory"}:
        errors.append(f"{name}: nieznany typ resource '{res}'")
        return
    if res == "url":
        url = value.get("url", "")
        if not url.startswith("https://"):
            errors.append(f"{name}: URL musi zaczynać się od https:// ({url})")
        m = re.search(r"/(dist|content|scripts|blueprints)/(.+)$", url)
        if m:
            local = os.path.join(ROOT, m.group(1), m.group(2))
            if not os.path.exists(local):
                errors.append(f"{name}: brak lokalnego pliku {os.path.relpath(local, ROOT)} dla {url}")
    elif res == "wordpress.org/themes" and not value.get("slug"):
        errors.append(f"{name}: brak slug motywu")


def validate(letter):
    path = os.path.join(ROOT, "blueprints", f"{letter}.json")
    errors, warnings = [], []
    try:
        with open(path, encoding="utf-8") as fh:
            bp = json.load(fh)
    except Exception as exc:  # noqa: BLE001
        return [f"niepoprawny JSON: {exc}"], warnings

    for key in ("landingPage", "preferredVersions", "steps"):
        if key not in bp:
            errors.append(f"brak klucza '{key}'")
    if "$schema" not in bp:
        warnings.append("brak klucza '$schema' (zalecany)")

    steps = bp.get("steps", [])
    if not isinstance(steps, list) or not steps:
        errors.append("'steps' musi być niepustą listą")
        return errors, warnings

    for i, step in enumerate(steps, 1):
        name = step.get("step")
        label = f"krok {i} ({name})"
        if name not in REQUIRED:
            errors.append(f"{label}: nieznana nazwa kroku")
            continue
        for field in REQUIRED[name]:
            if field not in step:
                errors.append(f"{label}: brak wymaganego pola '{field}'")
        for key in ("themeData", "pluginData", "file", "wordPressFilesZip", "zipFile"):
            if key in step:
                check_resource(f"{label}.{key}", step[key], errors, warnings)
        if name == "writeFile" and isinstance(step.get("data"), dict):
            check_resource(f"{label}.data", step["data"], errors, warnings)
        if name == "runPHP" and "<?php" not in step.get("code", ""):
            errors.append(f"{label}: kod PHP musi zaczynać się od '<?php'")
        if name == "wp-cli":
            cmd = step.get("command", "")
            if isinstance(cmd, str) and not cmd.startswith("wp "):
                errors.append(f"{label}: komenda musi zaczynać się od 'wp '")

    # sprawdzenie kolejności: motyw nadrzędny przed potomnym, WXR po motywie
    names = [s.get("step") for s in steps]
    if "importWxr" in names and "installTheme" in names:
        if names.index("importWxr") < max(i for i, n in enumerate(names) if n == "installTheme"):
            warnings.append("importWxr wykonuje się przed instalacją motywu — sprawdź kolejność")
    return errors, warnings


def main():
    total_errors = 0
    for letter in BLUEPRINTS:
        errors, warnings = validate(letter)
        status = "OK" if not errors else "BŁĘDY"
        print(f"[{status}] blueprints/{letter}.json")
        for w in warnings:
            print(f"    ostrzeżenie: {w}")
        for e in errors:
            print(f"    błąd: {e}")
        total_errors += len(errors)
    print()
    print("WYNIK:", "OK (wszystkie blueprinty przeszły kontrolę strukturalną)" if total_errors == 0 else f"{total_errors} błędów")
    print("Uwaga: to nie jest pełna walidacja schematem JSON ani test uruchomieniowy w Playground.")
    return 0 if total_errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

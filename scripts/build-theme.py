#!/usr/bin/env python3
"""Buduje theme.json motywu gdp-child dla wskazanego kierunku (A/B/C) i pakuje motyw do dist/gdp-child-<X>.zip.

Użycie: python3 scripts/build-theme.py A [--no-zip]

Źródła:
  theme/gdp-child/theme.base.json       – wspólne blokady, skale, style
  theme/gdp-child/variants/<X>/tokens.json – paleta, fonty, promienie (sekcja "meta" nie trafia do theme.json)
Wynik:
  theme/gdp-child/theme.json            – złożony plik (commitowany dla kierunku bieżącego)
  dist/gdp-child-<X>.zip                – ZIP z katalogiem gdp-child/ (bez variants/ i theme.base.json)
"""
import json, sys, os, shutil, zipfile, copy

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEME = os.path.join(ROOT, "theme", "gdp-child")


def deep_merge(base, over):
    """Słowniki łączone rekurencyjnie; listy i skalary z wariantu zastępują bazę."""
    out = copy.deepcopy(base)
    for k, v in over.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def rel_luminance(hex_color):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    def lin(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast(a, b):
    la, lb = rel_luminance(a), rel_luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def check_contrast(palette):
    p = {c["slug"]: c["color"] for c in palette}
    pairs = [("contrast", "base"), ("contrast", "surface"), ("base", "primary"), ("primary", "base"), ("base", "contrast")]
    problems = []
    for fg, bg in pairs:
        ratio = contrast(p[fg], p[bg])
        if ratio < 4.5:
            problems.append(f"{fg} na {bg}: {ratio:.2f}:1 < 4.5:1")
    return problems


def build(direction, make_zip=True):
    base = json.load(open(os.path.join(THEME, "theme.base.json"), encoding="utf-8"))
    tokens = json.load(open(os.path.join(THEME, "variants", direction, "tokens.json"), encoding="utf-8"))
    meta = tokens.pop("meta", {})
    merged = deep_merge(base, tokens)
    problems = check_contrast(merged["settings"]["color"]["palette"])
    if problems:
        print("KONTRAST – błędy:", *problems, sep="\n  ")
        sys.exit(1)
    with open(os.path.join(THEME, "theme.json"), "w", encoding="utf-8") as fh:
        json.dump(merged, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    # znacznik kierunku dla functions.php (odczyt bez parsowania theme.json)
    with open(os.path.join(THEME, "direction.txt"), "w", encoding="utf-8") as fh:
        fh.write(direction + "\n")
    print(f"theme.json zbudowany dla kierunku {direction} ({meta.get('name','')})")
    if not make_zip:
        return
    dist = os.path.join(ROOT, "dist")
    os.makedirs(dist, exist_ok=True)
    zip_path = os.path.join(dist, f"gdp-child-{direction}.zip")
    skip_dirs = {"variants"}
    skip_files = {"theme.base.json", ".DS_Store"}
    # Do ZIP trafiają tylko katalogi fontów używane w theme.json tego kierunku.
    used_fonts = set()
    for fam in merged["settings"]["typography"].get("fontFamilies", []):
        for face in fam.get("fontFace", []):
            for src in face.get("src", []):
                used_fonts.add(src.replace("file:./", "").split("/")[2])
    fonts_dir = os.path.join(THEME, "assets", "fonts")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for dirpath, dirnames, filenames in os.walk(THEME):
            dirnames[:] = [d for d in dirnames if d not in skip_dirs]
            if os.path.dirname(dirpath) == fonts_dir and os.path.basename(dirpath) not in used_fonts:
                dirnames[:] = []
                continue
            for fn in sorted(filenames):
                if fn in skip_files:
                    continue
                full = os.path.join(dirpath, fn)
                arc = os.path.join("gdp-child", os.path.relpath(full, THEME))
                zf.write(full, arc)
    print(f"ZIP: {os.path.relpath(zip_path, ROOT)} ({os.path.getsize(zip_path)//1024} KB)")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args or args[0] not in ("A", "B", "C"):
        print(__doc__)
        sys.exit(2)
    build(args[0], make_zip="--no-zip" not in sys.argv)

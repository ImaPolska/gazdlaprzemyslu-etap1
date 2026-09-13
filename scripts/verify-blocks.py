#!/usr/bin/env python3
"""
Weryfikacja automatyczna (sekcja 13.1 i 13.6 instrukcji) na źródłach treści w repo:
  content/pages/*.html, content/posts/*.html, content/blocks/*.html, theme/gdp-child/patterns/*.php
oraz na wygenerowanym content/site.wxr.

Raportuje:
  - liczbę core/html, core/freeform, core/shortcode, wzorców shortcode [a-z_]+ i bloków spoza core/*  (oczekiwane: 0 0 0 0 0)
  - liczbę <h1> na każdej stronie (oczekiwane: dokładnie 1 na page; 0 w wp_block i post, bo H1 daje tytuł wpisu)
  - czy każda sekcja nadrzędna (blok najwyższego poziomu core/group) ma templateLock:contentOnly
  - zakazane frazy z sekcji 10.1, wykrzykniki i emoji w treści
  - listę wszystkich [[ ]] z lokalizacją → docs/open-items.generated.md

Uruchom: python3 scripts/verify-blocks.py            (kod wyjścia 1, jeśli którykolwiek licznik ≠ 0)
"""
import html as htmllib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BANNED = ["w dzisiejszych czasach", "kompleksowe rozwiązania", "lider rynku", "innowacyjn", "game-changer"]
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF]")
BLOCK_OPEN_RE = re.compile(r"<!--\s*wp:([a-z0-9-]+/)?([a-z0-9-]+)(\s+(\{.*?\}))?\s*(/)?-->", re.S)
SHORTCODE_RE = re.compile(r"(?<!\[)\[([a-z_]+)(?:\s[^\]]*)?\](?!\])")
PLACEHOLDER_RE = re.compile(r"\[\[(.*?)\]\]", re.S)


def strip_meta_comment(text: str) -> str:
    m = re.match(r"\s*<!--(.*?)-->\s*", text, re.S)
    if m and "wp:" not in m.group(1):
        return text[m.end():]
    return text


def strip_php_header(text: str) -> str:
    return re.sub(r"^<\?php.*?\?>\s*", "", text, flags=re.S)


def text_only(markup: str) -> str:
    """Tekst widoczny: bez komentarzy bloków i tagów, z rozkodowanymi encjami."""
    no_comments = re.sub(r"<!--.*?-->", " ", markup, flags=re.S)
    no_tags = re.sub(r"<[^>]+>", " ", no_comments)
    return htmllib.unescape(no_tags)


def analyse(name: str, kind: str, markup: str, report: dict, open_items: list):
    counts = report["liczniki"]
    top_level_depth = 0
    depth = 0
    top_groups = []
    for m in BLOCK_OPEN_RE.finditer(markup):
        ns, block, attrs_raw, self_closing = m.group(1), m.group(2), m.group(4), m.group(5)
        full = (ns or "core/") + block
        if not full.startswith("core/"):
            counts["bloki spoza core/*"] += 1
            report["szczegoly"].append(f"{name}: blok spoza core: {full}")
        if full == "core/html":
            counts["core/html"] += 1
        if full == "core/freeform":
            counts["core/freeform"] += 1
        if full == "core/shortcode":
            counts["core/shortcode"] += 1
        if depth == 0:
            attrs = {}
            if attrs_raw:
                try:
                    attrs = json.loads(attrs_raw)
                except json.JSONDecodeError:
                    report["szczegoly"].append(f"{name}: niepoprawny JSON atrybutów w {full}")
            if full == "core/group":
                top_groups.append((attrs.get("metadata", {}).get("name", "(bez nazwy)"), attrs.get("templateLock")))
            elif full != "core/block":
                report["szczegoly"].append(f"{name}: blok najwyższego poziomu nie jest grupą ani wzorcem: {full}")
        if not self_closing:
            depth += 1
    # zamknięcia
    for _ in re.finditer(r"<!--\s*/wp:", markup):
        depth -= 1

    for gname, lock in top_groups:
        report["sekcje"] += 1
        if lock != "contentOnly":
            counts["sekcje bez templateLock:contentOnly"] += 1
            report["szczegoly"].append(f"{name}: sekcja „{gname}” bez templateLock:contentOnly (jest: {lock})")

    visible = text_only(markup)
    # shortcode-y tylko w tekście widocznym (żeby nie łapać JSON-a atrybutów ani [[ ]])
    visible_no_ph = PLACEHOLDER_RE.sub(" ", visible)
    for sm in SHORTCODE_RE.finditer(visible_no_ph):
        counts["wzorzec shortcode [a-z_]+"] += 1
        report["szczegoly"].append(f"{name}: możliwy shortcode: [{sm.group(1)}]")

    h1 = len(re.findall(r"<h1[\s>]", markup))
    report["h1"][name] = h1
    # page: dokładnie 1; wp_block/post/widget: 0 (H1 daje tytuł wpisu); pattern hero: 1, pozostałe wzorce: 0
    if kind == "pattern":
        expected = 1 if name.startswith("pattern:hero") else 0
    else:
        expected = 1 if kind == "page" else 0
    if h1 != expected:
        counts["strony z liczbą h1 ≠ oczekiwanej"] += 1
        report["szczegoly"].append(f"{name}: liczba h1 = {h1}, oczekiwano {expected}")

    low = visible.lower()
    for phrase in BANNED:
        if phrase in low:
            counts["zakazane frazy (10.1)"] += 1
            report["szczegoly"].append(f"{name}: zakazana fraza „{phrase}”")
    if "!" in visible:
        counts["wykrzykniki"] += visible.count("!")
        report["szczegoly"].append(f"{name}: wykrzyknik w treści ({visible.count('!')})")
    if EMOJI_RE.search(visible):
        counts["emoji"] += 1
        report["szczegoly"].append(f"{name}: emoji w treści")

    # [[ ]] z lokalizacją (sekcja = ostatnia grupa najwyższego poziomu przed placeholderem)
    for pm in PLACEHOLDER_RE.finditer(markup):
        before = markup[: pm.start()]
        sections = re.findall(r'"metadata":\{"name":"([^"]+)"', before)
        section = sections[-1] if sections else "—"
        open_items.append((kind, name, section, pm.group(1).strip() or "(puste)"))


def main() -> int:
    report = {
        "liczniki": {
            "core/html": 0, "core/freeform": 0, "core/shortcode": 0, "wzorzec shortcode [a-z_]+": 0,
            "bloki spoza core/*": 0, "strony z liczbą h1 ≠ oczekiwanej": 0,
            "sekcje bez templateLock:contentOnly": 0, "zakazane frazy (10.1)": 0, "wykrzykniki": 0, "emoji": 0,
        },
        "sekcje": 0, "h1": {}, "szczegoly": [],
    }
    open_items = []
    sources = []
    for p in sorted((ROOT / "content" / "pages").glob("*.html")):
        sources.append((f"page:{p.stem}", "page", strip_meta_comment(p.read_text(encoding="utf-8"))))
    for p in sorted((ROOT / "content" / "posts").glob("*.html")):
        sources.append((f"post:{p.stem}", "post", strip_meta_comment(p.read_text(encoding="utf-8"))))
    for p in sorted((ROOT / "content" / "blocks").glob("*.html")):
        kind = "widget" if p.stem.startswith("stopka-") else "wp_block"
        sources.append((f"{kind}:{p.stem}", kind, strip_meta_comment(p.read_text(encoding="utf-8"))))
    for p in sorted((ROOT / "theme" / "gdp-child" / "patterns").glob("*.php")):
        sources.append((f"pattern:{p.stem}", "pattern", strip_php_header(p.read_text(encoding="utf-8"))))

    for name, kind, markup in sources:
        if kind == "widget":
            # widgety stopki: bloki luźne (nagłówek + lista), bez wymogu grupy nadrzędnej
            markup_for_groups = f'<!-- wp:group {{"metadata":{{"name":"Widget"}},"templateLock":"contentOnly"}} -->{markup}<!-- /wp:group -->'
            analyse(name, kind, markup_for_groups, report, open_items)
        else:
            analyse(name, kind, markup, report, open_items)

    # WXR: dodatkowa kontrola na wyniku końcowym
    wxr = ROOT / "content" / "site.wxr"
    if wxr.exists():
        w = wxr.read_text(encoding="utf-8")
        for needle, key in (("wp:html ", "core/html"), ("wp:freeform", "core/freeform"), ("wp:shortcode", "core/shortcode")):
            n = w.count(f"<!-- {needle}")
            if n:
                report["liczniki"][key] += n
                report["szczegoly"].append(f"site.wxr: {needle} × {n}")
        non_core = set(re.findall(r"<!--\s*wp:([a-z0-9-]+)/[a-z0-9-]+", w)) - {"core"}
        if non_core:
            report["liczniki"]["bloki spoza core/*"] += len(non_core)
            report["szczegoly"].append(f"site.wxr: przestrzenie nazw spoza core: {sorted(non_core)}")
        if "{{" in w:
            report["szczegoly"].append("site.wxr: nierozwiązany placeholder {{...}}")
            report["liczniki"]["bloki spoza core/*"] += 1

    # --- raport ---
    print("Weryfikacja bloków (sekcja 13.1 / 13.6)")
    print(f"Źródła: {len(sources)} plików, sekcji nadrzędnych: {report['sekcje']}")
    print("\n| Kontrola | Oczekiwane | Uzyskane |\n|---|---|---|")
    for k, v in report["liczniki"].items():
        print(f"| {k} | 0 | {v} |")
    print("\nh1 na stronę:")
    for k, v in report["h1"].items():
        if k.startswith("page:"):
            print(f"  {k}: {v}")
    if report["szczegoly"]:
        print("\nSzczegóły:")
        for s in report["szczegoly"]:
            print("  -", s)

    # --- open items ---
    out = ROOT / "docs" / "open-items.generated.md"
    out.parent.mkdir(exist_ok=True)
    lines = ["# Lista `[[ ]]` w treści (generowana)", "",
             "Plik generowany przez `scripts/verify-blocks.py`; nie edytuj ręcznie. Komentarz i pytania do zleceniodawcy: `docs/open-items.md`.", "",
             f"Łącznie wystąpień: {len(open_items)}", "",
             "| # | Typ | Plik | Sekcja | Placeholder |", "|---|---|---|---|---|"]
    for i, (kind, name, section, text) in enumerate(open_items, 1):
        lines.append(f"| {i} | {kind} | {name.split(':', 1)[1]} | {section} | `[[{text}]]` |")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\n[[ ]]: {len(open_items)} wystąpień → {out.relative_to(ROOT)}")

    failed = sum(report["liczniki"].values())
    print("\nWYNIK:", "OK (same zera)" if failed == 0 else f"BŁĄD ({failed} odchyleń)")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Składa content/pages/*.html, content/blocks/*.html, content/posts/*.html i config/menus.json
w plik content/site.wxr (WXR 1.2) oraz config/widgets.json (widgety blokowe stopki Blocksy).

Zasady:
  - wzorce zsynchronizowane (wp_block) mają stałe ID 9001–9010; strony odwołują się do nich
    przez {{ref:slug}} → <!-- wp:block {"ref":9001} /--> ; importer WordPressa zachowuje ID
    (import_id), więc odwołania działają po imporcie w świeżej instancji Playground;
  - kategorie mają w WXR stałe term_id 21–26 (TERM_IDS); importer NIE gwarantuje zachowania ID
    terminów, dlatego {{term:slug}} jest poprawiane po imporcie przez scripts/playground-setup.php
    (mapa slug → ID z WXR musi być zgodna z TERM_IDS poniżej);
  - metadane strony (tytuł, slug, rodzic) są w komentarzu HTML na początku pliku
    (linie "Tytuł:", "Strona: /sciezka/ (slug: x, rodzic: y)"); metadane wpisu: "Tytuł:",
    "Kategoria: slug", "Skrót: ..." (brak Kategoria → komentarz-rynkowy);
  - ID stron 101–123 i wpisów 201–207 są stałe (PAGE_IDS / POST_IDS): kolejność = menu_order.

Uruchom: python3 scripts/build-wxr.py
"""
import datetime as dt
import json
import pathlib
import re
import sys
from xml.sax.saxutils import escape

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
SITE_URL = "https://playground.wordpress.net"
AUTHOR_LOGIN = "admin"
NOW = dt.datetime(2026, 9, 13, 10, 0, 0)  # stała data: powtarzalny plik WXR między buildami

# Stałe ID wzorców zsynchronizowanych (kolejność = sekcja 9.1 instrukcji)
BLOCK_IDS = {
    "cta-wgraj-fakture": 9001,
    "slot-upload-faktury": 9002,
    "slot-tabela-cen": 9003,
    "slot-kalkulator-wypowiedzenia": 9004,
    "slot-analiza-umowy": 9005,
    "slot-formularz-doradcy": 9006,
    "wzorzec-segmenty": 9007,
    "pasek-zaufania": 9008,
    "zastrzezenie-cen": 9009,
    "faq-produkt": 9010,
}
BLOCK_TITLES = {
    "cta-wgraj-fakture": "CTA: wgraj fakturę",
    "slot-upload-faktury": "Slot: upload faktury",
    "slot-tabela-cen": "Slot: tabela cen",
    "slot-kalkulator-wypowiedzenia": "Slot: kalkulator wypowiedzenia",
    "slot-analiza-umowy": "Slot: analiza umowy",
    "slot-formularz-doradcy": "Slot: formularz doradcy",
    "wzorzec-segmenty": "Wzorzec: segmenty",
    "pasek-zaufania": "Pasek zaufania",
    "zastrzezenie-cen": "Zastrzeżenie cen",
    "faq-produkt": "FAQ: produkt",
}
# kategorie: slug -> (term_id w WXR, nazwa, opis)
CATEGORIES = {
    "komentarz-rynkowy": (21, "Komentarz rynkowy", "Co dzieje się z ceną gazu na TGE i co to znaczy dla Twojej umowy. Autor i data przy każdym wpisie."),
    "zmiana-sprzedawcy": (22, "Zmiana sprzedawcy", "Kolejność kroków, terminy, pełnomocnictwo, zgłoszenie do operatora."),
    "umowy-i-wypowiedzenia": (23, "Umowy i wypowiedzenia", "Okres wypowiedzenia, klauzula prolongacyjna, art. 4j Prawa energetycznego."),
    "ceny-i-rynek": (24, "Ceny i rynek", "Cena stała, indeks TGE, transze; z czego składa się cena na fakturze."),
    "biometan-i-raportowanie": (25, "Biometan i raportowanie", "Biometan z aktywów Grupy, certyfikacja, Scope 1 i CSRD bez obietnic."),
    "sprzedaz-rezerwowa": (26, "Sprzedaż rezerwowa", "Kiedy grozi, jak jej uniknąć, co robić, gdy już trwa."),
}
TERM_IDS = {slug: v[0] for slug, v in CATEGORIES.items()}
# strony: slug -> ID (rodzic musi być zdefiniowany przed dzieckiem; kolejność = menu_order)
PAGE_IDS = {
    "start": 101, "oferta": 102, "cena-stala": 103, "wiedza": 104,
    "wgraj-fakture": 105, "cena-indeksowana-tge": 106, "model-transzowy": 107,
    "umowa-kompleksowa-msp": 108, "biometan": 109, "ceny-orientacyjne": 110,
    "kalkulator-wypowiedzenia": 111, "analiza-umowy": 112, "dla-kogo": 113, "przemysl": 114,
    "msp": 115, "dla-doradcow": 116, "dla-agentow-ai": 117, "o-nas": 118, "dokumenty": 119,
    "kontakt": 120, "polityka-prywatnosci": 121, "regulamin": 122, "komentarz-rynkowy": 123,
}
# wpisy: slug pliku -> ID (kolejność = data publikacji rosnąco, co 7 dni wstecz od NOW)
POST_IDS = {
    "komentarz-rynkowy-1": 201, "komentarz-rynkowy-2": 202,
    "jak-zmienic-sprzedawce-gazu-w-firmie": 203,
    "okres-wypowiedzenia-i-klauzula-prolongacyjna": 204,
    "sprzedaz-rezerwowa-gazu": 205,
    "cena-stala-czy-indeksowana-do-tge": 206,
    "art-4j-ust-3b-prawa-energetycznego-msp": 207,
}
MENU_TERM_ID_START = 31
MENU_ITEM_ID_START = 301
FOOTER_WIDGETS = {  # id widgetu blokowego -> plik
    "ct-footer-sidebar-1": "stopka-oferta.html",
    "ct-footer-sidebar-2": "stopka-narzedzia.html",
    "ct-footer-sidebar-3": "stopka-wiedza.html",
    "ct-footer-sidebar-4": "stopka-kontakt.html",
    "ct-footer-sidebar-5": "stopka-dane-spolki.html",
}


def read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_leading_comment(html: str) -> tuple[str, dict]:
    """Zdejmuje komentarz z metadanymi na początku pliku i zwraca (treść, meta)."""
    meta = {}
    m = re.match(r"\s*<!--(.*?)-->\s*", html, re.S)
    if m and "wp:" not in m.group(1):
        header = m.group(1)
        html = html[m.end():]
        t = re.search(r"Tytuł:\s*(.+)", header)
        if t:
            meta["title"] = t.group(1).strip()
        s = re.search(r"slug:\s*([a-z0-9-]+)", header)
        if s:
            meta["slug"] = s.group(1)
        p = re.search(r"rodzic:\s*([a-z0-9-]+)", header)
        if p:
            meta["parent"] = p.group(1)
        c = re.search(r"Kategoria:\s*([a-z0-9-]+)", header)
        if c:
            meta["category"] = c.group(1)
        e = re.search(r"Skrót:\s*(.+)", header)
        if e:
            meta["excerpt"] = e.group(1).strip()
    return html.strip() + "\n", meta


def substitute(html: str, where: str) -> str:
    def ref(m):
        slug = m.group(1)
        if slug not in BLOCK_IDS:
            sys.exit(f"[błąd] {where}: nieznany wzorzec {{{{ref:{slug}}}}}")
        return str(BLOCK_IDS[slug])

    def term(m):
        slug = m.group(1)
        if slug not in TERM_IDS:
            sys.exit(f"[błąd] {where}: nieznana kategoria {{{{term:{slug}}}}}")
        return str(TERM_IDS[slug])

    html = re.sub(r"\{\{ref:([a-z0-9-]+)\}\}", ref, html)
    html = re.sub(r"\{\{term:([a-z0-9-]+)\}\}", term, html)
    if "{{" in html:
        sys.exit(f"[błąd] {where}: nierozwiązany placeholder {{{{...}}}}")
    return html


def cdata(s: str) -> str:
    return "<![CDATA[" + s.replace("]]>", "]]]]><![CDATA[>") + "]]>"


def item(*, post_id, title, slug, post_type, content, status="publish", parent=0, menu_order=0,
         terms=(), metas=(), date=NOW, excerpt=""):
    date_s = date.strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "\t<item>",
        f"\t\t<title>{cdata(title)}</title>",
        f"\t\t<link>{SITE_URL}/?p={post_id}</link>",
        f"\t\t<pubDate>{date.strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>",
        f"\t\t<dc:creator>{cdata(AUTHOR_LOGIN)}</dc:creator>",
        f"\t\t<guid isPermaLink=\"false\">{SITE_URL}/?p={post_id}</guid>",
        "\t\t<description></description>",
        f"\t\t<content:encoded>{cdata(content)}</content:encoded>",
        f"\t\t<excerpt:encoded>{cdata(excerpt)}</excerpt:encoded>",
        f"\t\t<wp:post_id>{post_id}</wp:post_id>",
        f"\t\t<wp:post_date>{cdata(date_s)}</wp:post_date>",
        f"\t\t<wp:post_date_gmt>{cdata(date_s)}</wp:post_date_gmt>",
        f"\t\t<wp:post_modified>{cdata(date_s)}</wp:post_modified>",
        f"\t\t<wp:post_modified_gmt>{cdata(date_s)}</wp:post_modified_gmt>",
        "\t\t<wp:comment_status>closed</wp:comment_status>",
        "\t\t<wp:ping_status>closed</wp:ping_status>",
        f"\t\t<wp:post_name>{cdata(slug)}</wp:post_name>",
        f"\t\t<wp:status>{cdata(status)}</wp:status>",
        f"\t\t<wp:post_parent>{parent}</wp:post_parent>",
        f"\t\t<wp:menu_order>{menu_order}</wp:menu_order>",
        f"\t\t<wp:post_type>{cdata(post_type)}</wp:post_type>",
        "\t\t<wp:post_password><![CDATA[]]></wp:post_password>",
        "\t\t<wp:is_sticky>0</wp:is_sticky>",
    ]
    for domain, nicename, name in terms:
        lines.append(f"\t\t<category domain=\"{domain}\" nicename=\"{nicename}\">{cdata(name)}</category>")
    for k, v in metas:
        lines.append("\t\t<wp:postmeta>")
        lines.append(f"\t\t\t<wp:meta_key>{cdata(k)}</wp:meta_key>")
        lines.append(f"\t\t\t<wp:meta_value>{cdata(v)}</wp:meta_value>")
        lines.append("\t\t</wp:postmeta>")
    lines.append("\t</item>")
    return "\n".join(lines)


def build() -> int:
    items = []
    terms_xml = []

    # --- kategorie ---
    for slug, (tid, name, desc) in CATEGORIES.items():
        terms_xml.append(
            "\t<wp:category>\n"
            f"\t\t<wp:term_id>{tid}</wp:term_id>\n"
            f"\t\t<wp:category_nicename>{cdata(slug)}</wp:category_nicename>\n"
            "\t\t<wp:category_parent><![CDATA[]]></wp:category_parent>\n"
            f"\t\t<wp:cat_name>{cdata(name)}</wp:cat_name>\n"
            f"\t\t<wp:category_description>{cdata(desc)}</wp:category_description>\n"
            "\t</wp:category>"
        )

    # --- wzorce zsynchronizowane (wp_block) ---
    for slug, pid in BLOCK_IDS.items():
        path = CONTENT / "blocks" / f"{slug}.html"
        html, _ = strip_leading_comment(read(path))
        html = substitute(html, str(path))
        if f'"ref":{pid}' in html:
            sys.exit(f"[błąd] {slug}: wzorzec odwołuje się do samego siebie")
        items.append(item(post_id=pid, title=BLOCK_TITLES[slug], slug=slug, post_type="wp_block",
                          content=html))

    # --- strony ---
    pages_meta = {}
    for slug, pid in PAGE_IDS.items():
        path = CONTENT / "pages" / f"{slug}.html"
        html, meta = strip_leading_comment(read(path))
        meta.setdefault("slug", slug)
        pages_meta[slug] = meta
        html = substitute(html, str(path))
        parent = PAGE_IDS[meta["parent"]] if meta.get("parent") else 0
        items.append(item(post_id=pid, title=meta.get("title", slug), slug=slug, post_type="page",
                          content=html, parent=parent, menu_order=list(PAGE_IDS).index(slug)))

    # --- wpisy (komentarze rynkowe + artykuły wiedzy) ---
    post_files = sorted((CONTENT / "posts").glob("*.html"))
    for path in post_files:
        if path.stem not in POST_IDS:
            sys.exit(f"[błąd] {path}: brak stałego ID w POST_IDS")
    for path in sorted(post_files, key=lambda q: POST_IDS[q.stem]):
        html, meta = strip_leading_comment(read(path))
        html = substitute(html, str(path))
        n = POST_IDS[path.stem] - 200
        cat_slug = meta.get("category", "komentarz-rynkowy")
        if cat_slug not in CATEGORIES:
            sys.exit(f"[błąd] {path}: nieznana kategoria {cat_slug}")
        title = meta.get("title", path.stem)
        if title.startswith("Komentarz rynkowy:"):  # robocze komentarze bez tytułu: numeracja jak w P1.1
            title = f"Komentarz rynkowy {n}: [[tytuł]]"
        items.append(item(
            post_id=POST_IDS[path.stem],
            title=title,
            slug=path.stem,
            post_type="post",
            content=html,
            date=NOW - dt.timedelta(days=7 * (len(post_files) - n)),
            excerpt=meta.get("excerpt", "[[komentarz: skrót do 25 słów]]"),
            terms=[("category", cat_slug, CATEGORIES[cat_slug][1])],
        ))

    # --- menu (nav_menu + nav_menu_item) ---
    menus = json.loads(read(ROOT / "config" / "menus.json"))["menus"]
    menu_term_id = MENU_TERM_ID_START
    menu_item_id = MENU_ITEM_ID_START
    for menu in menus:
        terms_xml.append(
            "\t<wp:term>\n"
            f"\t\t<wp:term_id>{menu_term_id}</wp:term_id>\n"
            "\t\t<wp:term_taxonomy><![CDATA[nav_menu]]></wp:term_taxonomy>\n"
            f"\t\t<wp:term_slug>{cdata(menu['slug'])}</wp:term_slug>\n"
            "\t\t<wp:term_parent><![CDATA[]]></wp:term_parent>\n"
            f"\t\t<wp:term_name>{cdata(menu['name'])}</wp:term_name>\n"
            "\t</wp:term>"
        )
        order = 0

        def add_item(entry, parent_item_id):
            nonlocal menu_item_id, order
            order += 1
            this_id = menu_item_id
            menu_item_id += 1
            metas = [
                ("_menu_item_type", "custom"),
                ("_menu_item_menu_item_parent", str(parent_item_id)),
                ("_menu_item_object_id", str(this_id)),
                ("_menu_item_object", "custom"),
                ("_menu_item_target", ""),
                ("_menu_item_classes", 'a:1:{i:0;s:0:"";}'),
                ("_menu_item_xfn", ""),
                ("_menu_item_url", entry["url"]),
            ]
            items.append(item(post_id=this_id, title=entry["title"], slug=f"menu-{this_id}", post_type="nav_menu_item",
                              content="", menu_order=order, metas=metas,
                              terms=[("nav_menu", menu["slug"], menu["name"])]))
            for child in entry.get("children", []):
                add_item(child, this_id)

        for entry in menu["items"]:
            add_item(entry, 0)
        menu_term_id += 1

    # --- WXR ---
    head = f"""<?xml version="1.0" encoding="UTF-8" ?>
<!--
  Gaz dla Przemysłu – etap 1 – treść prototypu.
  Plik generowany: python3 scripts/build-wxr.py (nie edytuj ręcznie; źródło w content/).
-->
<rss version="2.0"
\txmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
\txmlns:content="http://purl.org/rss/1.0/modules/content/"
\txmlns:wfw="http://wellformedweb.org/CommentAPI/"
\txmlns:dc="http://purl.org/dc/elements/1.1/"
\txmlns:wp="http://wordpress.org/export/1.2/"
>
<channel>
\t<title>Gaz dla Przemysłu</title>
\t<link>{SITE_URL}</link>
\t<description>PBM Sp. z o.o., Grupa IMA Polska</description>
\t<pubDate>{NOW.strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
\t<language>pl-PL</language>
\t<wp:wxr_version>1.2</wp:wxr_version>
\t<wp:base_site_url>{SITE_URL}</wp:base_site_url>
\t<wp:base_blog_url>{SITE_URL}</wp:base_blog_url>
\t<wp:author>
\t\t<wp:author_id>1</wp:author_id>
\t\t<wp:author_login>{cdata(AUTHOR_LOGIN)}</wp:author_login>
\t\t<wp:author_email><![CDATA[admin@example.invalid]]></wp:author_email>
\t\t<wp:author_display_name><![CDATA[Zespół analiz PBM]]></wp:author_display_name>
\t\t<wp:author_first_name><![CDATA[]]></wp:author_first_name>
\t\t<wp:author_last_name><![CDATA[]]></wp:author_last_name>
\t</wp:author>
"""
    wxr = head + "\n".join(terms_xml) + "\n\t<generator>gazdlaprzemyslu/scripts/build-wxr.py</generator>\n" + "\n".join(items) + "\n</channel>\n</rss>\n"
    out = CONTENT / "site.wxr"
    out.write_text(wxr, encoding="utf-8")

    # walidacja XML
    import xml.dom.minidom
    xml.dom.minidom.parseString(wxr.encode("utf-8"))

    # --- widgety blokowe stopki (config/widgets.json; wgrywane przez playground-setup.php) ---
    widgets = {}
    for sidebar, fname in FOOTER_WIDGETS.items():
        html, _ = strip_leading_comment(read(CONTENT / "blocks" / fname))
        widgets[sidebar] = substitute(html, fname)
    (ROOT / "config" / "widgets.json").write_text(
        json.dumps({"_meta": {"opis": "Treść widgetów blokowych stopki Blocksy (ct-footer-sidebar-N → markup bloków). Generowane z content/blocks/stopka-*.html przez scripts/build-wxr.py."},
                    "sidebars": widgets}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"[ok] {out.relative_to(ROOT)}: {len(items)} elementów "
          f"({len(BLOCK_IDS)} wp_block, {len(PAGE_IDS)} page, {len(post_files)} post, {menu_item_id - MENU_ITEM_ID_START} nav_menu_item), "
          f"{len(terms_xml)} terminów; config/widgets.json: {len(widgets)} sidebarów")
    return 0


if __name__ == "__main__":
    sys.exit(build())

#!/usr/bin/env python3
"""
Generuje z config/tokens.json:
  - theme/variants/<X>/theme.json           (tokeny + blokady dla edytora)
  - config/theme_mods_<X>.json              (Customizer Blocksy: paleta, typografia, nagłówek, stopka)

Jedno źródło prawdy dla kolorów i fontów = config/tokens.json.
Uruchom: python3 scripts/build-theme-json.py
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOKENS = json.loads((ROOT / "config" / "tokens.json").read_text(encoding="utf-8"))
SHARED = TOKENS["shared"]
FOOTER_STRUCTURE = json.loads((ROOT / "config" / "footer_structure.json").read_text(encoding="utf-8"))


def font_stack(key: str) -> str:
    return SHARED["fonts"][key]


def theme_json(variant_key: str, v: dict) -> dict:
    colors = v["colors"]
    palette = [
        {"slug": slug, "name": SHARED["colorNames"][slug], "color": colors[slug]}
        for slug in ["base", "contrast", "primary", "secondary", "surface", "line", "success", "warning"]
    ]
    button_bg = colors["primary"]
    return {
        "$schema": "https://schemas.wp.org/trunk/theme.json",
        "version": 3,
        "title": f"Gaz dla Przemysłu – kierunek {variant_key}: {v['name']}",
        "settings": {
            "appearanceTools": False,
            "useRootPaddingAwareAlignments": False,
            "layout": {
                "contentSize": SHARED["layout"]["contentSize"],
                "wideSize": SHARED["layout"]["wideSize"],
            },
            "color": {
                "custom": False,
                "customGradient": False,
                "customDuotone": False,
                "defaultPalette": False,
                "defaultGradients": False,
                "defaultDuotone": False,
                "background": True,
                "text": True,
                "link": True,
                "palette": palette,
                "gradients": [],
                "duotone": [],
            },
            "typography": {
                "fluid": True,
                "customFontSize": False,
                "defaultFontSizes": False,
                "dropCap": False,
                "fontStyle": False,
                "fontWeight": False,
                "letterSpacing": False,
                "lineHeight": False,
                "textDecoration": False,
                "textTransform": False,
                "writingMode": False,
                "fontFamilies": [
                    {"slug": "heading", "name": "Nagłówki", "fontFamily": font_stack(v["heading"])},
                    {"slug": "body", "name": "Tekst", "fontFamily": font_stack(v["body"])},
                    {"slug": "mono", "name": "Liczby (mono)", "fontFamily": font_stack("mono")},
                ],
                "fontSizes": SHARED["fontSizes"],
            },
            "spacing": {
                "customSpacingSize": False,
                "defaultSpacingSizes": False,
                "blockGap": True,
                "margin": True,
                "padding": True,
                "units": ["px", "rem", "%"],
                "spacingSizes": SHARED["spacing"],
            },
            "border": {"color": False, "radius": False, "style": False, "width": False},
            "shadow": {"defaultPresets": False, "presets": []},
            "dimensions": {"aspectRatio": False, "minHeight": False},
            "position": {"sticky": False},
            "background": {"backgroundImage": False},
            "blocks": {
                "core/table": {"typography": {"fontFamilies": [
                    {"slug": "mono", "name": "Liczby (mono)", "fontFamily": font_stack("mono")}
                ]}},
                "core/cover": {"color": {"custom": False}},
            },
        },
        "styles": {
            "color": {"background": "var(--wp--preset--color--base)", "text": "var(--wp--preset--color--contrast)"},
            "typography": {
                "fontFamily": "var(--wp--preset--font-family--body)",
                "fontSize": "var(--wp--preset--font-size--s)",
                "lineHeight": "1.6",
            },
            "spacing": {"blockGap": "var(--wp--preset--spacing--40)"},
            "elements": {
                "heading": {
                    "typography": {
                        "fontFamily": "var(--wp--preset--font-family--heading)",
                        "fontWeight": v["headingWeight"],
                        "letterSpacing": v["headingLetterSpacing"],
                        "lineHeight": "1.2",
                    },
                    "color": {"text": "var(--wp--preset--color--contrast)"},
                },
                "h1": {"typography": {"fontSize": "var(--wp--preset--font-size--xxl)", "lineHeight": "1.1"}},
                "h2": {"typography": {"fontSize": "var(--wp--preset--font-size--xl)"}},
                "h3": {"typography": {"fontSize": "var(--wp--preset--font-size--l)"}},
                "h4": {"typography": {"fontSize": "var(--wp--preset--font-size--m)"}},
                "link": {
                    "color": {"text": f"var(--wp--preset--color--{v['link']})"},
                    "typography": {"textDecoration": "underline"},
                    ":hover": {"color": {"text": f"var(--wp--preset--color--{v['linkHover']})"}},
                },
                "button": {
                    "color": {"background": button_bg, "text": v["buttonText"]},
                    "typography": {"fontFamily": "var(--wp--preset--font-family--body)", "fontWeight": "600"},
                    "spacing": {"padding": {"top": "0.85rem", "bottom": "0.85rem", "left": "1.5rem", "right": "1.5rem"}},
                    "border": {"radius": v["radius"]},
                    ":hover": {"color": {"background": "var(--wp--preset--color--secondary)", "text": v["buttonTextHover"]}},
                    ":focus": {"color": {"background": "var(--wp--preset--color--secondary)", "text": v["buttonTextHover"]}},
                },
            },
            "blocks": {
                "core/table": {"typography": {"fontSize": "var(--wp--preset--font-size--xs)"}},
                "core/details": {"typography": {"fontSize": "var(--wp--preset--font-size--s)"}},
                "core/separator": {"color": {"text": "var(--wp--preset--color--line)"}},
            },
        },
    }


def color_value(color: str) -> dict:
    return {"default": {"color": color}}


def typography(family: dict, size: str, line_height: str, extra: dict | None = None) -> dict:
    t = {
        "family": family["family"],
        "variation": family["variation"],
        "size": size,
        "line-height": line_height,
        "letter-spacing": "0em",
        "text-transform": "none",
        "text-decoration": "none",
    }
    if extra:
        t.update(extra)
    return t


def theme_mods(variant_key: str, v: dict) -> dict:
    c = v["colors"]
    order = SHARED["blocksyPaletteOrder"]  # color1..color8
    palette = {}
    for i, slug in enumerate(order, start=1):
        palette[f"color{i}"] = {
            "color": c[slug],
            "variable": f"theme-palette-color-{i}",
            "title": f"{SHARED['colorNames'][slug]} ({slug})",
        }

    def pal(slug: str) -> str:
        return f"var(--theme-palette-color-{order.index(slug) + 1})"

    dark = v["darkHeader"]
    header_bg = c["surface"] if dark else c["base"]
    header_text = c["base"] if dark else c["contrast"]
    header_hover = c["primary"] if dark else c["primary"]

    header_placements = {
        "current_section": "type-1",
        "sections": [
            {
                "id": "type-1",
                "mode": "placements",
                "settings": {
                    "has_transparent_header": "no",
                    "has_sticky_header": "no",
                },
                "items": [
                    {
                        "id": "logo",
                        "values": {
                            "has_site_title": "yes",
                            "has_site_title_link": "yes",
                            "has_tagline": "no",
                            "logo_position": "left",
                            "siteTitleColor": {"default": {"color": header_text}, "hover": {"color": header_hover}},
                            "siteTitle": typography(v["blocksyHeading"], "20px", "1.2"),
                        },
                    },
                    {
                        "id": "menu",
                        "values": {
                            "menu": "blocksy_location",
                            "header_menu_type": "type-1",
                            "headerMenuItemsGap": "24px",
                            "menuFontColor": {
                                "default": {"color": header_text},
                                "hover": {"color": header_hover},
                                "active": {"color": header_hover},
                            },
                            "headerDropdownFontColor": {
                                "default": {"color": c["contrast"]},
                                "hover": {"color": c["primary"]},
                            },
                            "headerDropdownBackground": {"default": {"color": c["base"]}, "hover": {"color": c["base"]}},
                            "headerMenuFont": typography(v["blocksyBody"], "15px", "1.3", {"variation": "n5"}),
                        },
                    },
                    {
                        "id": "button",
                        "values": {
                            "header_button_type": "type-1",
                            "header_button_size": "small",
                            "header_button_text": "Wgraj fakturę",
                            "header_button_open": "link",
                            "header_button_link": "/wgraj-fakture/",
                            "header_button_target": "no",
                            "header_button_nofollow": "no",
                            "button_aria_label": "Wgraj fakturę i otrzymaj ofertę w 24 godziny",
                            "headerButtonFontColor": {
                                "default": {"color": v["buttonText"]},
                                "hover": {"color": v["buttonTextHover"]},
                            },
                            "headerButtonForeground": {
                                "default": {"color": c["primary"]},
                                "hover": {"color": c["secondary"]},
                            },
                            "headerButtonFont": typography(v["blocksyBody"], "15px", "1.3", {"variation": "n6"}),
                            "headerCtaRadius": {
                                "desktop": {"top": v["radius"], "right": v["radius"], "bottom": v["radius"], "left": v["radius"], "linked": True}
                            },
                        },
                    },
                    {
                        "id": "trigger",
                        "values": {
                            "trigger_label_visibility": "none",
                            "triggerIconColor": {"default": {"color": header_text}, "hover": {"color": header_hover}},
                        },
                    },
                    {
                        "id": "offcanvas",
                        "values": {
                            "side_panel_position": "right",
                            "offcanvasBackground": {"default": {"color": header_bg}},
                            "menu_close_button_type": "type-1",
                        },
                    },
                    {
                        "id": "mobile-menu",
                        "values": {
                            "menu": "blocksy_location",
                            "mobile_menu_type": "type-1",
                            "mobileMenuColor": {
                                "default": {"color": header_text},
                                "hover": {"color": header_hover},
                                "active": {"color": header_hover},
                            },
                            "mobileMenuFont": typography(v["blocksyHeading"], "18px", "1.5"),
                        },
                    },
                    {
                        "id": "middle-row",
                        "values": {
                            "headerRowWidth": "fixed",
                            "headerRowHeight": {"desktop": 72, "tablet": 64, "mobile": 60},
                            "headerRowBackground": {
                                "background_type": "color",
                                "backgroundColor": {"default": {"color": header_bg}},
                            },
                            "headerRowBottomBorder": {
                                "width": 1,
                                "style": "solid",
                                "color": {"color": c["line"]},
                            },
                        },
                    },
                ],
                "desktop": [
                    {"id": "top-row", "placements": [{"id": "start", "items": []}, {"id": "middle", "items": []}, {"id": "end", "items": []}, {"id": "start-middle", "items": []}, {"id": "end-middle", "items": []}]},
                    {"id": "middle-row", "placements": [{"id": "start", "items": ["logo"]}, {"id": "middle", "items": ["menu"]}, {"id": "end", "items": ["button"]}, {"id": "start-middle", "items": []}, {"id": "end-middle", "items": []}]},
                    {"id": "bottom-row", "placements": [{"id": "start", "items": []}, {"id": "middle", "items": []}, {"id": "end", "items": []}, {"id": "start-middle", "items": []}, {"id": "end-middle", "items": []}]},
                    {"id": "offcanvas", "placements": [{"id": "start", "items": []}]},
                ],
                "mobile": [
                    {"id": "top-row", "placements": [{"id": "start", "items": []}, {"id": "middle", "items": []}, {"id": "end", "items": []}, {"id": "start-middle", "items": []}, {"id": "end-middle", "items": []}]},
                    {"id": "middle-row", "placements": [{"id": "start", "items": ["logo"]}, {"id": "middle", "items": []}, {"id": "end", "items": ["button", "trigger"]}, {"id": "start-middle", "items": []}, {"id": "end-middle", "items": []}]},
                    {"id": "bottom-row", "placements": [{"id": "start", "items": []}, {"id": "middle", "items": []}, {"id": "end", "items": []}, {"id": "start-middle", "items": []}, {"id": "end-middle", "items": []}]},
                    {"id": "offcanvas", "placements": [{"id": "start", "items": ["mobile-menu"]}]},
                ],
            }
        ],
    }

    footer_bg = c["surface"] if not dark else c["surface"]
    footer_text = c["contrast"] if not dark else c["base"]
    footer_link_hover = c["primary"]

    footer_placements = {
        "current_section": "type-1",
        "sections": [
            {
                "id": "type-1",
                "mode": "columns",
                "rows": [
                    {"id": "top-row", "columns": FOOTER_STRUCTURE["rows"]["top-row"]},
                    {"id": "middle-row", "columns": FOOTER_STRUCTURE["rows"]["middle-row"]},
                    {"id": "bottom-row", "columns": FOOTER_STRUCTURE["rows"]["bottom-row"]},
                ],
                "items": [
                    {
                        "id": "top-row",
                        "values": {
                            "footerRowWidth": "fixed",
                            "items_per_row": "4",
                            "footerRowBackground": {"background_type": "color", "backgroundColor": {"default": {"color": footer_bg}}},
                            "rowFontColor": {
                                "default": {"color": footer_text},
                                "link_initial": {"color": footer_text},
                                "link_hover": {"color": footer_link_hover},
                            },
                            "footerWidgetsTitleColor": {"default": {"color": footer_text}},
                            "footerWidgetsTitleFont": typography(v["blocksyHeading"], "16px", "1.3"),
                            "footerRowTopDivider": {"width": 1, "style": "solid", "color": {"color": c["line"]}},
                        },
                    },
                    {
                        "id": "middle-row",
                        "values": {
                            "footerRowWidth": "fixed",
                            "items_per_row": "1",
                            "footerRowBackground": {"background_type": "color", "backgroundColor": {"default": {"color": footer_bg}}},
                            "rowFontColor": {
                                "default": {"color": footer_text},
                                "link_initial": {"color": footer_text},
                                "link_hover": {"color": footer_link_hover},
                            },
                            "footerRowTopDivider": {"width": 1, "style": "solid", "color": {"color": c["line"]}},
                        },
                    },
                    {
                        "id": "bottom-row",
                        "values": {
                            "footerRowWidth": "fixed",
                            "items_per_row": "2",
                            "2_columns_layout": "2fr 1fr",
                            "footerRowBackground": {"background_type": "color", "backgroundColor": {"default": {"color": footer_bg}}},
                            "rowFontColor": {
                                "default": {"color": footer_text},
                                "link_initial": {"color": footer_text},
                                "link_hover": {"color": footer_link_hover},
                            },
                            "footerRowTopDivider": {"width": 1, "style": "solid", "color": {"color": c["line"]}},
                        },
                    },
                    {"id": "widget-area-1", "values": {"widget": "ct-footer-sidebar-1", "horizontal_alignment": "left"}},
                    {"id": "widget-area-2", "values": {"widget": "ct-footer-sidebar-2", "horizontal_alignment": "left"}},
                    {"id": "widget-area-3", "values": {"widget": "ct-footer-sidebar-3", "horizontal_alignment": "left"}},
                    {"id": "widget-area-4", "values": {"widget": "ct-footer-sidebar-4", "horizontal_alignment": "left"}},
                    {"id": "widget-area-5", "values": {"widget": "ct-footer-sidebar-5", "horizontal_alignment": "left"}},
                    {
                        "id": "menu",
                        "values": {
                            "menu": "blocksy_location",
                            "menu_items_direction": "horizontal",
                            "footerMenuAlignment": "left",
                            "footerMenuFontColor": {"default": {"color": footer_text}, "hover": {"color": footer_link_hover}},
                            "footerMenuFont": typography(v["blocksyBody"], "14px", "1.5"),
                        },
                    },
                    {
                        "id": "copyright",
                        "values": {
                            "copyright_text": "© {current_year} PBM Sp. z o.o. Grupa IMA Polska.",
                            "footerCopyrightAlignment": "right",
                            "copyrightColor": {"default": {"color": footer_text}, "link_initial": {"color": footer_text}, "link_hover": {"color": footer_link_hover}},
                            "copyrightFont": typography(v["blocksyBody"], "14px", "1.5"),
                        },
                    },
                ],
                "settings": {"footer_container_structure": "fixed", "has_reveal_effect": "no"},
            }
        ],
    }

    heading_font = v["blocksyHeading"]
    body_font = v["blocksyBody"]

    mods = {
        "_meta": {
            "kierunek": variant_key,
            "nazwa": v["name"],
            "generator": "scripts/build-theme-json.py",
            "uwaga": "Wartości zgodne z config/tokens.json. Import: scripts/playground-setup.php (set_theme_mod dla każdego klucza poza _meta).",
        },
        # --- Paleta globalna Blocksy (te same wartości co theme.json; slugi edytora pochodzą z theme.json) ---
        "colorPalette": palette,
        "fontColor": color_value(pal("contrast")),
        "headingColor": color_value(pal("contrast")),
        "linkColor": {"default": {"color": pal(v["link"])}, "hover": {"color": pal(v["linkHover"])}},
        "border": {"width": 1, "style": "solid", "color": {"default": {"color": pal("line")}}},
        "buttonColor": {"default": {"color": pal("primary")}, "hover": {"color": pal("secondary")}},
        "buttonTextColor": {"default": {"color": v["buttonText"]}, "hover": {"color": v["buttonTextHover"]}},
        "buttonRadius": {"desktop": {"top": v["radius"], "right": v["radius"], "bottom": v["radius"], "left": v["radius"], "linked": True}},
        "site_background": {"background_type": "color", "backgroundColor": {"default": {"color": pal("base")}}},
        # --- Typografia globalna: wyłącznie fonty systemowe (zero Google Fonts) ---
        "rootTypography": typography(body_font, "17px", "1.6"),
        "h1Typography": typography(heading_font, "clamp(2.5rem, 5vw, 4rem)", "1.1", {"letter-spacing": v["headingLetterSpacing"]}),
        "h2Typography": typography(heading_font, "clamp(2rem, 3.5vw, 3rem)", "1.15", {"letter-spacing": v["headingLetterSpacing"]}),
        "h3Typography": typography(heading_font, "clamp(1.5rem, 2.5vw, 2.25rem)", "1.2"),
        "h4Typography": typography(heading_font, "20px", "1.3"),
        "h5Typography": typography(heading_font, "18px", "1.3"),
        "h6Typography": typography(heading_font, "16px", "1.3"),
        "buttons": typography(body_font, "16px", "1.2", {"variation": "n7"}),
        # --- Układ ---
        "maxSiteWidth": 1200,
        "contentAreaSpacing": {"desktop": "0px", "tablet": "0px", "mobile": "0px"},
        "narrowContainerWidth": 760,
        # --- Strony: bez tytułu Blocksy (H1 jest w treści), pełna szerokość, bez paska bocznego ---
        "single_page_hero_enabled": "no",
        "single_page_structure": "type-4",
        "single_page_content_style": "wide",
        "single_page_has_share_box": "no",
        "single_page_has_featured_image": "no",
        # --- Wpisy (komentarz rynkowy, artykuły): wąska kolumna czytania, tytuł + autor + data ---
        "single_blog_post_hero_enabled": "yes",
        "single_blog_post_structure": "type-3",
        "single_blog_post_content_style": "boxed",
        "single_blog_post_has_share_box": "no",
        "single_blog_post_has_author_box": "no",
        "single_blog_post_has_featured_image": "no",
        # --- Archiwa (kategoria komentarz-rynkowy, /wiedza/) ---
        "blog_structure": "type-3",
        # --- Menu: lokalizacje Blocksy (slugi menu; scripts/playground-setup.php zamienia je na term_id po imporcie WXR) ---
        "_nav_menu_locations_by_slug": {"menu_1": "glowne", "footer": "prawne", "menu_mobile": "glowne"},
        # --- Header / Footer Builder ---
        "header_placements": header_placements,
        "footer_placements": footer_placements,
        # --- Inne ---
        "has_back_top": "no",
        "emoji_scripts": "no",
    }
    return mods


def main() -> int:
    for key, v in TOKENS["variants"].items():
        out_dir = ROOT / "theme" / "variants" / key
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "theme.json").write_text(json.dumps(theme_json(key, v), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (ROOT / "config" / f"theme_mods_{key}.json").write_text(
            json.dumps(theme_mods(key, v), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"[ok] kierunek {key}: theme/variants/{key}/theme.json, config/theme_mods_{key}.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())

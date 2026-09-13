#!/usr/bin/env python3
"""
Generuje config/theme_mods_{A,B,C}.json – ustawienia Customizera Blocksy (theme mods) dla kierunku.

Źródłem prawdy dla kolorów i fontów jest theme.json (variants/X/tokens.json). Ten skrypt tylko
odzwierciedla te same wartości w Header/Footer Builderze Blocksy, żeby nagłówek i stopka
(renderowane przez Blocksy, nie przez bloki) miały tę samą paletę. Nie wprowadza nowych kolorów.

Użycie: python3 scripts/build-theme-mods.py [A|B|C ...]
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VARIANTS = os.path.join(ROOT, 'theme', 'gdp-child', 'variants')
OUT = os.path.join(ROOT, 'config')

SKIP = 'CT_CSS_SKIP_RULE'
FONT_BODY = 'var(--wp--preset--font-family--body)'
FONT_HEAD = 'var(--wp--preset--font-family--heading)'


def color(c):
    return {'color': c}


def bg(c):
    return {'background_type': 'color', 'backgroundColor': {'default': color(c)}}


def border(c, width=1, style='solid'):
    return {'width': width, 'style': style, 'color': color(c)}


def typo(family, size, weight='n4', lh='1.4', transform='none', ls='0em'):
    return {'family': family, 'variation': weight, 'size': size, 'line-height': lh,
            'letter-spacing': ls, 'text-transform': transform, 'text-decoration': 'none'}


def spacing(v):
    return {'top': v, 'left': v, 'right': v, 'bottom': v, 'linked': True}


def build(direction):
    tokens = json.load(open(os.path.join(VARIANTS, direction, 'tokens.json'), encoding='utf-8'))
    pal = {p['slug']: p['color'] for p in tokens['settings']['color']['palette']}
    meta = tokens['meta']
    dark_header = meta.get('header') == 'dark'
    hover = meta['hover']
    radius = meta.get('radius_button', '0px')

    header_bg = pal['contrast'] if dark_header else pal['base']
    header_fg = pal['base'] if dark_header else pal['contrast']
    header_line = 'rgba(255,255,255,0.14)' if dark_header else pal['line']
    header_accent = pal['secondary'] if dark_header else pal['primary']

    logo = {'id': 'logo', 'values': {
        'has_site_title': 'yes', 'has_tagline': 'no',
        'siteTitleColor': {'default': color(header_fg), 'hover': color(header_accent)},
        'siteTitleFont': typo(FONT_HEAD, '22px', 'n7', '1.2', 'none', '-0.01em'),
    }}
    menu = {'id': 'menu', 'values': {
        'menu': 'glowne',
        'headerMenuFont': typo(FONT_BODY, '15px', 'n5', '1.3'),
        'menuFontColor': {'default': color(header_fg), 'hover': color(header_accent), 'active': color(header_accent)},
        'headerDropdownBackground': bg(pal['base']),
        'headerDropdownFontColor': {'default': color(pal['contrast']), 'hover': color(pal['primary']), 'active': color(pal['primary'])},
        'headerDropdownFont': typo(FONT_BODY, '15px', 'n4', '1.4'),
        'headerDropdownRadius': spacing(radius),
        'headerDropdownTopOffset': 8,
        'headerDropdownShadow': {'enable': True, 'h_offset': 0, 'v_offset': 8, 'blur': 24, 'spread': -6, 'inset': False, 'color': color('rgba(15,23,42,0.18)')},
    }}
    button = {'id': 'button', 'values': {
        'header_button_text': 'Wgraj fakturę', 'header_button_link': '/wgraj-fakture/',
        'header_button_type': 'type-1', 'header_button_size': 'small',
        'headerButtonForeground': {'default': color(pal['primary']), 'hover': color(hover)},
        'headerButtonFontColor': {'default': color('#FFFFFF'), 'hover': color('#FFFFFF')},
        'headerButtonFont': typo(FONT_BODY, '15px', 'n6', '1.2'),
        'headerCtaRadius': spacing(radius),
        'visibility': {'desktop': True, 'tablet': False, 'mobile': False},
    }}
    button_mobile = {'id': 'button~mobcta', 'values': dict(button['values'], header_button_text='Oferta w 24 h',
                                                          visibility={'desktop': False, 'tablet': True, 'mobile': True})}
    trigger = {'id': 'trigger', 'values': {
        'triggerIconColor': {'default': color(header_fg), 'hover': color(header_accent)},
        'mobile_menu_trigger_type': 'type-1', 'trigger_has_label': 'no',
    }}
    offcanvas = {'id': 'offcanvas', 'values': {
        'offcanvasBackground': bg(pal['contrast']),
        'menu_close_button_color': {'default': color(pal['base']), 'hover': color(pal['secondary'])},
    }}
    mobile_menu = {'id': 'mobile-menu', 'values': {
        'menu': 'glowne',
        'mobileMenuFont': typo(FONT_HEAD, '20px', 'n6', '1.3'),
        'mobileMenuColor': {'default': color(pal['base']), 'hover': color(pal['secondary']), 'active': color(pal['secondary'])},
    }}
    middle_row = {'id': 'middle-row', 'values': {
        'headerRowHeight': 76,
        'headerRowBackground': bg(header_bg),
        'headerRowBottomBorder': border(header_line),
        'headerRowShadow': {'enable': False, 'h_offset': 0, 'v_offset': 10, 'blur': 20, 'spread': 0, 'inset': False, 'color': color('rgba(41,51,61,0.1)')},
    }}

    desktop_rows = [
        {'id': 'top-row', 'placements': [{'id': 'start', 'items': []}, {'id': 'middle', 'items': []}, {'id': 'end', 'items': []}]},
        {'id': 'middle-row', 'placements': [{'id': 'start', 'items': ['logo']}, {'id': 'middle', 'items': []}, {'id': 'end', 'items': ['menu', 'button']}]},
        {'id': 'bottom-row', 'placements': [{'id': 'start', 'items': []}, {'id': 'middle', 'items': []}, {'id': 'end', 'items': []}]},
    ]
    mobile_rows = [
        {'id': 'top-row', 'placements': [{'id': 'start', 'items': []}, {'id': 'middle', 'items': []}, {'id': 'end', 'items': []}]},
        {'id': 'middle-row', 'placements': [{'id': 'start', 'items': ['logo']}, {'id': 'middle', 'items': []}, {'id': 'end', 'items': ['button~mobcta', 'trigger']}]},
        {'id': 'bottom-row', 'placements': [{'id': 'start', 'items': []}, {'id': 'middle', 'items': []}, {'id': 'end', 'items': []}]},
        {'id': 'offcanvas', 'placements': [{'id': 'start', 'items': ['mobile-menu']}]},
    ]
    items = [logo, menu, button, button_mobile, trigger, offcanvas, mobile_menu, middle_row]

    if meta.get('topbar'):
        desktop_rows[0]['placements'][0]['items'] = ['text']
        items.append({'id': 'text', 'values': {
            'header_text': 'Komentarz rynkowy: [[data]] — <a href="/komentarz-rynkowy/">[[tytuł]]</a>',
            'headerTextFont': typo(FONT_BODY, '14px', 'n4', '1.3'),
            'headerTextColor': {'default': color(pal['base']), 'link_initial': color(pal['base']), 'link_hover': color(pal['secondary'])},
        }})
        items.append({'id': 'top-row', 'values': {
            'headerRowHeight': 38,
            'headerRowBackground': bg(pal['contrast']),
            'headerRowBottomBorder': border('rgba(255,255,255,0.1)', 1, 'none'),
        }})

    header_placements = {'sections': [{
        'id': 'type-1', 'mode': 'placements',
        'desktop': desktop_rows, 'mobile': mobile_rows,
        'items': items, 'settings': [],
    }]}

    footer_fg = pal['base']
    footer_placements = {'sections': [{
        'id': 'type-1', 'mode': 'columns',
        'rows': [
            {'id': 'top-row', 'columns': [['widget-area-1'], ['widget-area-2'], ['widget-area-3'], ['widget-area-4']]},
            {'id': 'middle-row', 'columns': [['widget-area-5']]},
            {'id': 'bottom-row', 'columns': [['copyright'], ['menu']]},
        ],
        'items': [
            {'id': 'top-row', 'values': {'footerRowWidth': 'fixed', 'footerRowSpacing': {'top': '64px', 'bottom': '40px', 'left': '0px', 'right': '0px', 'linked': False},
                                         'footerRowColumnsSpacing': 32, 'footerRowTopDivider': border('rgba(255,255,255,0.1)', 1, 'none')}},
            {'id': 'middle-row', 'values': {'footerRowWidth': 'fixed', 'footerRowSpacing': {'top': '24px', 'bottom': '24px', 'left': '0px', 'right': '0px', 'linked': False},
                                            'footerRowTopDivider': border('rgba(255,255,255,0.14)', 1, 'solid'), 'footerRowTopDividerFullWidth': 'no'}},
            {'id': 'bottom-row', 'values': {'footerRowWidth': 'fixed', 'footerRowSpacing': {'top': '20px', 'bottom': '24px', 'left': '0px', 'right': '0px', 'linked': False},
                                            'footerRowTopDivider': border('rgba(255,255,255,0.14)', 1, 'solid'), 'footerRowColumnsVerticalAlign': 'center'}},
            {'id': 'copyright', 'values': {
                'copyright_text': '© {current_year} PBM Sp. z o.o., Grupa IMA Polska',
                'copyrightFont': typo(FONT_BODY, '14px', 'n4', '1.4'),
                'copyrightColor': {'default': color('rgba(255,255,255,0.72)'), 'link_initial': color(footer_fg), 'link_hover': color(pal['secondary'])},
            }},
            {'id': 'menu', 'values': {
                'menu': 'prawne', 'footer_menu_horizontal_alignment': 'flex-end',
                'footerMenuFont': typo(FONT_BODY, '14px', 'n4', '1.4'),
                'footerMenuFontColor': {'default': color('rgba(255,255,255,0.72)'), 'hover': color(footer_fg), 'active': color(footer_fg)},
            }},
        ] + [
            {'id': 'widget-area-%d' % i, 'values': {
                'widget_area_colors': {'default': color(footer_fg), 'link_initial': color('rgba(255,255,255,0.78)'), 'link_hover': color(pal['secondary'])},
                'widgetsTitleFont': typo(FONT_HEAD, '15px', 'n7', '1.3'),
                'widgetsFont': typo(FONT_BODY, '15px', 'n4', '1.6'),
            }} for i in range(1, 6)
        ],
        'settings': {
            'footerBackground': bg(pal['contrast']),
        },
    }]}

    mods = {
        # Paleta – kolejność zgodna z mapowaniem w docs/decisions.md.
        'colorPalette': {
            'color1': color(pal['primary']), 'color2': color(hover), 'color3': color(pal['contrast']), 'color4': color(pal['contrast']),
            'color5': color(pal['line']), 'color6': color(pal['surface']), 'color7': color(pal['base']), 'color8': color(pal['base']),
            'current_palette': 1, 'palettes': [],
        },
        'fontColor': {'default': color(pal['contrast'])},
        'linkColor': {'default': color(pal['primary']), 'hover': color(hover)},
        'headingColor': {'default': color(pal['contrast'])},
        'buttonColor': {'default': color(pal['primary']), 'hover': color(hover)},
        'buttonTextColor': {'default': color('#FFFFFF'), 'hover': color('#FFFFFF')},
        'buttonRadius': spacing(radius),
        'buttonMinHeight': 48,
        'buttonTypography': typo(FONT_BODY, '16px', 'n6', '1.2'),
        # Typografia – rodziny z theme.json, rozmiary fluid też z theme.json (tu tylko rodziny i wagi).
        'rootTypography': typo(FONT_BODY, '17px', 'n4', '1.55'),
        'h1Typography': typo(FONT_HEAD, '48px', 'n7', '1.1', 'none', '-0.02em'),
        'h2Typography': typo(FONT_HEAD, '34px', 'n7', '1.15', 'none', '-0.02em'),
        'h3Typography': typo(FONT_HEAD, '24px', 'n6', '1.25'),
        'h4Typography': typo(FONT_HEAD, '20px', 'n6', '1.3'),
        'h5Typography': typo(FONT_HEAD, '17px', 'n6', '1.3'),
        'h6Typography': typo(FONT_HEAD, '15px', 'n6', '1.3'),
        # Układ.
        'maxSiteWidth': 1200,
        'narrowContainerWidth': 760,
        'contentAreaSpacing': 'none',
        'single_page_hero_enabled': 'no',
        # Archiwum /wiedza/ nie ma treści strony, więc h1 dostarcza hero Blocksy (tylko tytuł).
        'blog_hero_enabled': 'yes',
        'blog_hero_section': 'type-1',
        'blog_hero_alignment': 'left',
        'blog_hero_elements': [
            {'id': 'custom_title', 'enabled': True, 'heading_tag': 'h1'},
            {'id': 'custom_description', 'enabled': False},
            {'id': 'custom_meta', 'enabled': False},
            {'id': 'breadcrumbs', 'enabled': False},
        ],
        'single_page_structure': 'type-4',
        'single_page_content_area_spacing': 'none',
        'single_page_has_comments': 'no',
        'has_back_top': 'no',
        'has_breadcrumbs': 'no',
        'site_background': bg(pal['base']),
        'blog_post_structure': 'grid',
        'blog_columns': 3,
        'has_reading_progress': 'no',
        # Header / footer builder.
        'header_placements': header_placements,
        'footer_placements': footer_placements,
        'footer_type': 'type-1',
        'footer_has_reveal': 'no',
        # Menu (lokalizacje ustawia apply-config.php po utworzeniu menu).
        'gdp_direction': direction,
    }
    path = os.path.join(OUT, 'theme_mods_%s.json' % direction)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(mods, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print('theme mods:', os.path.relpath(path, ROOT))


if __name__ == '__main__':
    for d in (sys.argv[1:] or ['A', 'B', 'C']):
        build(d)

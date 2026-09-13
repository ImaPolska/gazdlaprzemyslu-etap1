<?php
/**
 * Konfiguracja instancji po imporcie WXR (krok runPHP w blueprints/*.json).
 *
 * Blueprint zapisuje ten plik (writeFile) jako /wordpress/gdp-setup.php i uruchamia:
 *   <?php define('GDP_BASE', 'https://…/'); define('GDP_VARIANT', 'A'); require '/wordpress/gdp-setup.php';
 *
 * Kroki:
 *  1. theme_mods Blocksy z config/theme_mods_<X>.json (set_theme_mod dla każdego klucza poza „_…”)
 *  2. lokalizacje menu Blocksy (menu_1, menu_mobile, footer) → term_id menu po slugu
 *  3. strona główna (start) i strona wpisów (wiedza)
 *  4. widgety blokowe stopki z config/widgets.json (ct-footer-sidebar-1..5)
 *  5. poprawka ID kategorii komentarz-rynkowy w Query Loop (importer nie zachowuje ID terminów)
 *  6. wp_pattern_sync_status: wzorce mają być zsynchronizowane (pusta meta = synced)
 *
 * Skrypt jest idempotentny: można go uruchomić ponownie bez skutków ubocznych.
 * Ten sam plik wykorzystuje scripts/restore-on-host.sh (etap 2) przez `wp eval-file`.
 */

if (!defined('ABSPATH')) {
    require_once '/wordpress/wp-load.php';
}
if (!defined('GDP_BASE')) {
    define('GDP_BASE', getenv('GDP_BASE') ?: '');
}
if (!defined('GDP_VARIANT')) {
    define('GDP_VARIANT', getenv('GDP_VARIANT') ?: 'A');
}

function gdp_log($msg) {
    echo '[gdp-setup] ' . $msg . "\n";
}

/** Pobiera JSON z GDP_BASE (URL) albo z lokalnego katalogu repo (GDP_BASE jako ścieżka). */
function gdp_fetch_json($relative) {
    $source = rtrim(GDP_BASE, '/') . '/' . ltrim($relative, '/');
    if (preg_match('#^https?://#', $source)) {
        $response = wp_remote_get($source, ['timeout' => 60]);
        if (is_wp_error($response)) {
            gdp_log('błąd pobierania ' . $source . ': ' . $response->get_error_message());
            return null;
        }
        $body = wp_remote_retrieve_body($response);
    } else {
        $body = @file_get_contents($source);
    }
    if (!$body) {
        gdp_log('pusty plik: ' . $source);
        return null;
    }
    $data = json_decode($body, true);
    if (!is_array($data)) {
        gdp_log('niepoprawny JSON: ' . $source . ' (' . json_last_error_msg() . ')');
        return null;
    }
    return $data;
}

// 0. Motyw potomny musi być aktywny (Blocksy zapisuje mody pod theme_mods_gdp-child przy aktywnym potomnym).
$theme = wp_get_theme();
gdp_log('aktywny motyw: ' . $theme->get('Name') . ' (' . get_stylesheet() . ')');

// 1. theme_mods Blocksy
$mods = gdp_fetch_json('config/theme_mods_' . GDP_VARIANT . '.json');
$count = 0;
if ($mods) {
    foreach ($mods as $key => $value) {
        if (substr($key, 0, 1) === '_') {
            continue; // _meta, _nav_menu_locations_by_slug
        }
        set_theme_mod($key, $value);
        $count++;
    }
}
gdp_log('theme_mods: ustawiono ' . $count . ' kluczy dla kierunku ' . GDP_VARIANT);

// 2. lokalizacje menu
$locations = [];
$by_slug = isset($mods['_nav_menu_locations_by_slug']) ? $mods['_nav_menu_locations_by_slug']
    : ['menu_1' => 'glowne', 'menu_mobile' => 'glowne', 'footer' => 'prawne'];
foreach ($by_slug as $location => $slug) {
    $menu = get_term_by('slug', $slug, 'nav_menu');
    if ($menu) {
        $locations[$location] = (int) $menu->term_id;
    } else {
        gdp_log('brak menu o slugu ' . $slug . ' (lokalizacja ' . $location . ')');
    }
}
set_theme_mod('nav_menu_locations', $locations);
gdp_log('nav_menu_locations: ' . json_encode($locations));

// 3. strona główna i strona wpisów
$front = get_page_by_path('start');
$posts_page = get_page_by_path('wiedza');
update_option('show_on_front', 'page');
if ($front) {
    update_option('page_on_front', $front->ID);
    gdp_log('page_on_front = ' . $front->ID);
} else {
    gdp_log('brak strony „start”');
}
if ($posts_page) {
    update_option('page_for_posts', $posts_page->ID);
    gdp_log('page_for_posts = ' . $posts_page->ID);
} else {
    gdp_log('brak strony „wiedza”');
}

// 4. widgety blokowe stopki
$widgets = gdp_fetch_json('config/widgets.json');
if ($widgets && isset($widgets['sidebars'])) {
    $widget_block = get_option('widget_block', []);
    if (!is_array($widget_block)) {
        $widget_block = [];
    }
    $sidebars_widgets = get_option('sidebars_widgets', []);
    if (!is_array($sidebars_widgets)) {
        $sidebars_widgets = [];
    }
    // usuń poprzednie widgety gdp z sidebarów stopki (idempotencja)
    foreach ($widgets['sidebars'] as $sidebar_id => $markup) {
        $sidebars_widgets[$sidebar_id] = [];
    }
    $next = 100;
    foreach ($widget_block as $k => $v) {
        if (is_int($k) && $k >= $next) {
            $next = $k + 1;
        }
    }
    foreach ($widgets['sidebars'] as $sidebar_id => $markup) {
        $widget_block[$next] = ['content' => $markup];
        $sidebars_widgets[$sidebar_id][] = 'block-' . $next;
        $next++;
    }
    $widget_block['_multiwidget'] = 1;
    // Blocksy rejestruje sidebary stopki tylko dla kolumn obecnych w footer_placements — te są już ustawione w kroku 1.
    if (!isset($sidebars_widgets['array_version'])) {
        $sidebars_widgets['array_version'] = 3;
    }
    update_option('widget_block', $widget_block);
    update_option('sidebars_widgets', $sidebars_widgets);
    gdp_log('widgety stopki: ' . count($widgets['sidebars']) . ' sidebarów');
}

// 5. ID kategorii komentarz-rynkowy w Query Loop
$cat = get_category_by_slug('komentarz-rynkowy');
if ($cat) {
    $real = (int) $cat->term_id;
    $pages = get_posts(['post_type' => ['page', 'wp_block'], 'posts_per_page' => -1, 'post_status' => 'any']);
    $fixed = 0;
    foreach ($pages as $p) {
        if (strpos($p->post_content, '"taxQuery":{"category":[') === false) {
            continue;
        }
        $new = preg_replace('/"taxQuery":\{"category":\[\d+\]\}/', '"taxQuery":{"category":[' . $real . ']}', $p->post_content);
        if ($new !== $p->post_content) {
            wp_update_post(['ID' => $p->ID, 'post_content' => $new]);
            $fixed++;
        }
    }
    gdp_log('komentarz-rynkowy term_id = ' . $real . '; poprawiono stron: ' . $fixed);
} else {
    gdp_log('brak kategorii komentarz-rynkowy');
}

// 6. wzorce zsynchronizowane: brak meta wp_pattern_sync_status = synced (WordPress 6.3+)
$blocks = get_posts(['post_type' => 'wp_block', 'posts_per_page' => -1, 'post_status' => 'any']);
foreach ($blocks as $b) {
    delete_post_meta($b->ID, 'wp_pattern_sync_status');
}
gdp_log('wp_block: ' . count($blocks) . ' wzorców zsynchronizowanych');

// 7. porządki
update_option('blocksy_ext_activation_notice_dismissed', 'yes');
update_option('blocksy_db_version', '2.1.57');
delete_option('fresh_site');
flush_rewrite_rules();
gdp_log('gotowe');

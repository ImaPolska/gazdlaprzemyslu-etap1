<?php
/**
 * Eksport aktualnych theme_mods Blocksy do JSON (po ręcznych zmianach w Customizerze).
 *
 * Użycie (WP-CLI, w katalogu instalacji WordPress):
 *   wp eval-file /sciezka/do/repo/scripts/export-theme-mods.php > config/theme_mods_A.json
 *
 * Użycie w WordPress Playground (krok runPHP lub konsola PHP w Playground):
 *   require '/wordpress/wp-load.php'; require '/wordpress/gdp-export.php';
 *   — wynik trafia na standardowe wyjście; skopiuj go do config/theme_mods_<X>.json w repozytorium.
 *
 * Skrypt nie zapisuje nic w bazie danych. Klucze zaczynające się od „_" są zarezerwowane
 * na metadane repozytorium i nie pochodzą z WordPressa.
 */

if (!defined('ABSPATH')) {
    require_once '/wordpress/wp-load.php';
}

$mods = get_theme_mods();
if (!is_array($mods)) {
    $mods = [];
}
ksort($mods);

$export = [
    '_meta' => [
        'wyeksportowano' => gmdate('c'),
        'motyw'          => get_stylesheet(),
        'motyw_nadrzedny'=> get_template(),
        'zrodlo'         => 'scripts/export-theme-mods.php',
    ],
];

// nav_menu_locations zapisujemy po slugach menu, bo ID terminów różnią się między instalacjami
$by_slug = [];
foreach ((array) ($mods['nav_menu_locations'] ?? []) as $location => $term_id) {
    $term = get_term((int) $term_id, 'nav_menu');
    if ($term && !is_wp_error($term)) {
        $by_slug[$location] = $term->slug;
    }
}
$export['_nav_menu_locations_by_slug'] = $by_slug;
unset($mods['nav_menu_locations']);

// klucze niestabilne między instalacjami (ID załączników, klucze wewnętrzne WordPressa)
foreach (['custom_logo', 'header_image', 'header_image_data', 'background_image', 'sidebars_widgets'] as $volatile) {
    unset($mods[$volatile]);
}

$export += $mods;

echo json_encode($export, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), "\n";

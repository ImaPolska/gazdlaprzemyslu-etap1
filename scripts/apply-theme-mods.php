<?php
/**
 * Wgrywa ustawienia Customizera Blocksy (theme mods) z pliku JSON.
 * Uruchamiane krokiem runPHP w blueprincie po aktywacji motywu potomnego.
 * Plik: GDP_CONFIG_DIR/theme_mods.json (domyślnie /wordpress/gdp-config/theme_mods.json).
 */
if (! defined('ABSPATH')) {
	require_once '/wordpress/wp-load.php';
}
$config_dir = defined('GDP_CONFIG_DIR') ? GDP_CONFIG_DIR : '/wordpress/gdp-config';
$file       = $config_dir . '/theme_mods.json';
if (! file_exists($file)) {
	echo "brak pliku theme_mods.json\n";
	exit(1);
}
$mods = json_decode(file_get_contents($file), true);
if (! is_array($mods)) {
	echo "nieprawidłowy JSON\n";
	exit(1);
}
foreach ($mods as $key => $value) {
	set_theme_mod($key, $value);
}
// Blocksy cache'uje dynamiczne CSS w transientach – wyczyść.
delete_transient('blocksy_dynamic_styles_descriptor');
if (function_exists('blocksy_manager') && isset(blocksy_manager()->db)) {
	blocksy_manager()->db->wipe_cache();
}
wp_cache_flush();
echo 'theme mods: ' . count($mods) . " kluczy\n";

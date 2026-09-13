<?php
/**
 * Eksport ustawień Customizera Blocksy (theme mods) do JSON – zasada „nic nie istnieje tylko w instancji”.
 * Uruchomienie w Playground CLI (runPHP) albo przez WP-CLI:
 *   wp eval-file scripts/export-theme-mods.php > config/theme_mods_X.json
 * Bez argumentów wypisuje JSON na stdout; z GDP_EXPORT_PATH zapisuje do pliku.
 */
if ( ! defined( 'ABSPATH' ) ) {
	require_once getenv( 'GDP_WP_PATH' ) ? rtrim( getenv( 'GDP_WP_PATH' ), '/' ) . '/wp-load.php' : '/wordpress/wp-load.php';
}
$mods = get_theme_mods();
if ( ! is_array( $mods ) ) {
	$mods = array();
}
// Pomijamy klucze WP niebędące ustawieniami Blocksy (nav_menu_locations odtwarza apply-config.php z config/menus.json).
foreach ( array( 'nav_menu_locations', 'custom_css_post_id', 'sidebars_widgets' ) as $skip ) {
	unset( $mods[ $skip ] );
}
ksort( $mods );
$json = json_encode( $mods, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES );
$path = getenv( 'GDP_EXPORT_PATH' );
if ( $path ) {
	file_put_contents( $path, $json . "\n" );
	echo "zapisano: $path\n";
} else {
	echo $json . "\n";
}

<?php
/**
 * Gaz dla Przemysłu – motyw potomny Blocksy (gdp-child).
 *
 * Zasady: brak treści w szablonach PHP; tylko konfiguracja edytora, style, blokady ról.
 */

if (! defined('ABSPATH')) {
	exit;
}

define('GDP_CHILD_VERSION', '0.1.0');

/**
 * Kierunek wizualny zbudowany do tego ZIP-a (A/B/C) – zapisany przez scripts/build-theme.py.
 */
function gdp_direction() {
	static $dir = null;
	if ($dir === null) {
		$file = get_stylesheet_directory() . '/direction.txt';
		$dir  = file_exists($file) ? trim((string) file_get_contents($file)) : 'A';
		if (! in_array($dir, ['A', 'B', 'C'], true)) {
			$dir = 'A';
		}
	}
	return $dir;
}

/**
 * Style i skrypty frontu.
 */
add_action('wp_enqueue_scripts', function () {
	wp_enqueue_style(
		'gdp-child',
		get_stylesheet_uri(),
		['ct-main-styles'],
		GDP_CHILD_VERSION
	);
	wp_enqueue_script(
		'gdp-header',
		get_stylesheet_directory_uri() . '/assets/js/header.js',
		[],
		GDP_CHILD_VERSION,
		['strategy' => 'defer', 'in_footer' => true]
	);
}, 20);

/**
 * Te same style w edytorze bloków.
 */
add_action('after_setup_theme', function () {
	add_theme_support('editor-styles');
	add_editor_style('style.css');
	add_theme_support('post-thumbnails');
	register_nav_menus([
		'menu_1' => 'Menu główne (nagłówek)',
		'footer' => 'Menu stopki (linki prawne)',
	]);
});

/**
 * Klasa kierunku na <body> – pozwala różnicować drobne detale w style.css bez zmiany treści.
 */
add_filter('body_class', function ($classes) {
	$classes[] = 'gdp-dir-' . gdp_direction();
	return $classes;
});
add_filter('admin_body_class', function ($classes) {
	return $classes . ' gdp-dir-' . gdp_direction();
});

/**
 * Fonty wyłącznie self-hosted: Blocksy nie ładuje nic z Google Fonts.
 */
add_filter('blocksy:typography:google:use-remote', '__return_false');
add_filter('blocksy:typography:google:enabled', '__return_false');

/**
 * Kategoria wzorców "gdp" (wzorce nie-zsynchronizowane w patterns/*.php).
 */
add_action('init', function () {
	register_block_pattern_category('gdp', [
		'label'       => 'Gaz dla Przemysłu',
		'description' => 'Startery sekcji serwisu gazdlaprzemyslu.pl',
	]);
	// Domyślne wzorce core i zdalne wzorce z wordpress.org nie są potrzebne redaktorowi.
	remove_theme_support('core-block-patterns');
}, 9);
add_filter('should_load_remote_block_patterns', '__return_false');

/**
 * Blokady dla roli Redaktor:
 *  - nie może odblokowywać bloków (canLockBlocks = false),
 *  - strony (page) mają blokadę contentOnly na poziomie dokumentu: zmienia teksty, obrazy i linki,
 *    nie usuwa/przesuwa sekcji. Wpisy (post) pozostają w pełni edytowalne.
 * Administrator: może przesuwać całe sekcje; wnętrze sekcji chroni templateLock=contentOnly w treści.
 */
function gdp_user_is_layout_admin() {
	return current_user_can('manage_options');
}

add_filter('block_editor_settings_all', function ($settings, $context) {
	if (! gdp_user_is_layout_admin()) {
		$settings['canLockBlocks'] = false;
		$settings['codeEditingEnabled'] = false;
		if (isset($context->post) && $context->post instanceof WP_Post && $context->post->post_type === 'page') {
			$settings['templateLock'] = 'contentOnly';
		}
	}
	return $settings;
}, 10, 2);

add_filter('register_post_type_args', function ($args, $post_type) {
	if ($post_type === 'page' && is_admin() && ! gdp_user_is_layout_admin()) {
		$args['template_lock'] = 'contentOnly';
	}
	return $args;
}, 10, 2);

/**
 * Redaktor nie widzi bloków, które nie są potrzebne w tym serwisie (m.in. core/html, core/freeform, core/shortcode).
 */
add_filter('allowed_block_types_all', function ($allowed, $context) {
	$blocked = ['core/html', 'core/freeform', 'core/shortcode', 'core/code', 'core/preformatted', 'core/embed', 'core/rss', 'core/tag-cloud', 'core/calendar', 'core/archives', 'core/legacy-widget', 'core/widget-group'];
	if ($allowed === true || ! is_array($allowed)) {
		$registry = WP_Block_Type_Registry::get_instance()->get_all_registered();
		$allowed  = array_keys($registry);
	}
	return array_values(array_diff($allowed, $blocked));
}, 10, 2);

/**
 * Tabele: kontener z przewijaniem poziomym na wąskich ekranach (klasa dodawana przy renderze, nie w treści).
 */
add_filter('render_block_core/table', function ($content) {
	if (strpos($content, 'gdp-tabela-scroll') === false) {
		$content = preg_replace('/<figure class="wp-block-table/', '<figure class="wp-block-table gdp-tabela-scroll', $content, 1);
	}
	return $content;
});

/**
 * Polskie etykiety dostępności Blocksy, których nie ma w pakiecie językowym pl_PL.
 * Dotyczy tylko frontu (aria-label), nie treści redakcyjnych.
 */
add_filter( 'gettext_blocksy', function ( $translation, $text ) {
	static $pl = array(
		'Close drawer'         => 'Zamknij panel',
		'Expand dropdown menu' => 'Rozwiń menu',
		'Offcanvas modal'      => 'Menu boczne',
		'Menu'                 => 'Menu',
		'Back to top'          => 'Do góry',
		'Search'               => 'Szukaj',
		'Read more'            => 'Czytaj dalej',
		'Continue reading'     => 'Czytaj dalej',
		'Skip to content'      => 'Przejdź do treści',
		'Skip to main content' => 'Przejdź do treści',
	);
	return isset( $pl[ $text ] ) ? $pl[ $text ] : $translation;
}, 10, 2 );

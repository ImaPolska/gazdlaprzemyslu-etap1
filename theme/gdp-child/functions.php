<?php
/**
 * Gaz dla Przemysłu – motyw potomny Blocksy (gdp-child).
 *
 * Zasady etapu 1:
 * - żadnej treści w PHP (treść żyje w post_content i w Customizerze),
 * - style wyłącznie w theme.json / style.css / assets/css/variant.css,
 * - zero zasobów zewnętrznych (fonty systemowe, brak Google Fonts).
 *
 * @package gdp-child
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'GDP_CHILD_VERSION', '0.1.0' );

/**
 * Style: rodzic → potomny → wariant kierunku (A/B/C) → fonty self-hosted (jeśli są).
 */
function gdp_child_enqueue_styles() {
	$child_uri  = get_stylesheet_directory_uri();
	$child_path = get_stylesheet_directory();

	wp_enqueue_style( 'blocksy-parent-style', get_template_directory_uri() . '/style.css', array(), GDP_CHILD_VERSION );

	wp_enqueue_style(
		'gdp-child-style',
		$child_uri . '/style.css',
		array( 'blocksy-parent-style' ),
		GDP_CHILD_VERSION
	);

	// Plik wariantu jest wstrzykiwany przez scripts/build-theme-zip.sh.
	if ( file_exists( $child_path . '/assets/css/variant.css' ) ) {
		wp_enqueue_style(
			'gdp-child-variant',
			$child_uri . '/assets/css/variant.css',
			array( 'gdp-child-style' ),
			GDP_CHILD_VERSION
		);
	}

	// Fonty self-hosted (WOFF2) – w etapie 1 plik zawiera wyłącznie stos systemowy.
	if ( file_exists( $child_path . '/assets/fonts/fonts.css' ) ) {
		wp_enqueue_style(
			'gdp-child-fonts',
			$child_uri . '/assets/fonts/fonts.css',
			array(),
			GDP_CHILD_VERSION
		);
	}
}
add_action( 'wp_enqueue_scripts', 'gdp_child_enqueue_styles', 20 );

/**
 * Te same style w edytorze bloków (podgląd zgodny z frontem).
 */
function gdp_child_editor_styles() {
	add_theme_support( 'editor-styles' );
	add_editor_style( 'style.css' );
	if ( file_exists( get_stylesheet_directory() . '/assets/css/variant.css' ) ) {
		add_editor_style( 'assets/css/variant.css' );
	}
	if ( file_exists( get_stylesheet_directory() . '/assets/fonts/fonts.css' ) ) {
		add_editor_style( 'assets/fonts/fonts.css' );
	}
}
add_action( 'after_setup_theme', 'gdp_child_editor_styles', 20 );

/**
 * Twardy zakaz Google Fonts: Blocksy nie zbuduje ani nie wstawi <link> do fonts.googleapis.com.
 * (Blocksy 2.x: filtr sprawdzany w FontsManager::load_dynamic_google_fonts i load_editor_fonts.)
 */
add_filter( 'blocksy:typography:google:use-remote', '__return_false' );

/**
 * Kategoria wzorców „Gaz dla Przemysłu” dla wzorców z katalogu patterns/.
 */
function gdp_child_register_pattern_category() {
	if ( function_exists( 'register_block_pattern_category' ) ) {
		register_block_pattern_category(
			'gdp',
			array(
				'label'       => __( 'Gaz dla Przemysłu', 'gdp-child' ),
				'description' => __( 'Sekcje startowe serwisu gazdlaprzemyslu.pl', 'gdp-child' ),
			)
		);
	}
}
add_action( 'init', 'gdp_child_register_pattern_category', 9 );

/**
 * Blokady układu:
 * - Administrator może odblokowywać bloki i przesuwać sekcje (canLockBlocks = true),
 * - Redaktor (i każda rola bez manage_options) nie widzi opcji odblokowania,
 *   więc templateLock:contentOnly na sekcjach jest dla niego ostateczny.
 */
function gdp_child_block_editor_settings( $settings ) {
	$is_admin = current_user_can( 'manage_options' );

	$settings['canLockBlocks']          = $is_admin;
	$settings['canUpdateBlockBindings'] = $is_admin;

	// Redaktor nie edytuje CSS/kodu w edytorze.
	if ( ! $is_admin ) {
		$settings['codeEditingEnabled'] = false;
	}

	return $settings;
}
add_filter( 'block_editor_settings_all', 'gdp_child_block_editor_settings', 20 );

/**
 * Redaktor nie może edytować wzorców zsynchronizowanych (wp_block) – zmiana w jednym
 * miejscu propaguje się na cały serwis, więc to kompetencja Administratora.
 */
function gdp_child_restrict_wp_block_editing( $caps, $cap, $user_id, $args ) {
	if ( 'edit_post' !== $cap || empty( $args[0] ) ) {
		return $caps;
	}
	$post = get_post( $args[0] );
	if ( $post && 'wp_block' === $post->post_type && ! user_can( $user_id, 'manage_options' ) ) {
		$caps[] = 'do_not_allow';
	}
	return $caps;
}
add_filter( 'map_meta_cap', 'gdp_child_restrict_wp_block_editing', 10, 4 );

/**
 * Tabele: automatyczne wyrównanie liczb do prawej.
 * Komórka, której treść jest liczbą (z jednostką lub placeholderem [[ ]]), otrzymuje klasę .num.
 * Bez inline CSS – klasa jest stylowana w style.css.
 */
function gdp_child_table_numeric_cells( $block_content, $block ) {
	if ( 'core/table' !== $block['blockName'] || false === strpos( $block_content, '<td' ) ) {
		return $block_content;
	}

	return preg_replace_callback(
		'#<td([^>]*)>(.*?)</td>#s',
		static function ( $m ) {
			$text = trim( wp_strip_all_tags( $m[2] ) );
			$is_number = (bool) preg_match( '/^[\-\+]?\d[\d\s\.,]*\s*(%|zł|PLN|GWh|MWh|kWh|m³|m3|zł\/MWh|PLN\/MWh)?$/u', $text );
			$is_placeholder = (bool) preg_match( '/^\[\[.*\]\]\s*(%|zł|PLN|GWh|MWh|kWh|zł\/MWh|PLN\/MWh)?$/u', $text );
			if ( ! $is_number && ! $is_placeholder ) {
				return $m[0];
			}
			if ( preg_match( '/class="([^"]*)"/', $m[1], $c ) ) {
				if ( false !== strpos( $c[1], 'num' ) ) {
					return $m[0];
				}
				$attrs = str_replace( $c[0], 'class="' . $c[1] . ' num"', $m[1] );
			} else {
				$attrs = $m[1] . ' class="num"';
			}
			return '<td' . $attrs . '>' . $m[2] . '</td>';
		},
		$block_content
	);
}
add_filter( 'render_block', 'gdp_child_table_numeric_cells', 10, 2 );

/**
 * Tabele: kontener z przewijaniem poziomym na mobile (bez łamania kolumn).
 * Blok core/table renderuje <figure class="wp-block-table"> – dodajemy klasę pomocniczą.
 */
function gdp_child_table_scroll_container( $block_content, $block ) {
	if ( 'core/table' !== $block['blockName'] ) {
		return $block_content;
	}
	return str_replace( 'class="wp-block-table', 'class="gdp-table-scroll wp-block-table', $block_content );
}
add_filter( 'render_block', 'gdp_child_table_scroll_container', 11, 2 );

/**
 * Rok dynamiczny w stopce: Blocksy obsługuje {current_year} w tekście copyright.
 * Dodatkowo udostępniamy ten sam token w blokach akapitu (stopka = widgety blokowe).
 */
function gdp_child_current_year_token( $block_content, $block ) {
	if ( 'core/paragraph' !== $block['blockName'] || false === strpos( $block_content, '{current_year}' ) ) {
		return $block_content;
	}
	return str_replace( '{current_year}', gmdate( 'Y' ), $block_content );
}
add_filter( 'render_block', 'gdp_child_current_year_token', 10, 2 );

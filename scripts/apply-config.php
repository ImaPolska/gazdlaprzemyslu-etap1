<?php
/**
 * Konfiguracja po imporcie WXR (krok runPHP w blueprincie).
 *
 * 1. Rozwiązuje placeholdery "__BLOCK:slug__" (ref wzorca zsynchronizowanego) i "__CAT:slug__" (ID kategorii)
 *    w post_content stron, wpisów, wzorców i w treści widgetów.
 * 2. Tworzy menu z config/menus.json i przypisuje lokalizacje Blocksy.
 * 3. Wstawia kolumny stopki jako widgety blokowe (config/footer.json).
 * 4. Ustawia stronę główną (get_page_by_path('start')); wpisy pod /wiedza/<slug>/, /wiedza/ to zwykła strona.
 *
 * Pliki JSON są zapisywane przez blueprint do katalogu GDP_CONFIG_DIR (domyślnie /wordpress/gdp-config).
 * Skrypt jest idempotentny: ponowne uruchomienie nie duplikuje menu ani widgetów.
 */

if (! defined('ABSPATH')) {
	require_once '/wordpress/wp-load.php';
}

$config_dir = defined('GDP_CONFIG_DIR') ? GDP_CONFIG_DIR : '/wordpress/gdp-config';
$log        = [];

// ---------------------------------------------------------------------------
// 1. Placeholdery ref / kategorii
// ---------------------------------------------------------------------------
$block_ids = [];
foreach (get_posts(['post_type' => 'wp_block', 'numberposts' => -1, 'post_status' => 'any']) as $b) {
	$block_ids[$b->post_name] = (int) $b->ID;
}
$cat_ids = [];
foreach (get_terms(['taxonomy' => 'category', 'hide_empty' => false]) as $t) {
	$cat_ids[$t->slug] = (int) $t->term_id;
}

function gdp_resolve_placeholders($content, $block_ids, $cat_ids, &$missing) {
	$content = preg_replace_callback('/"ref":"__BLOCK:([a-z0-9-]+)__"/', function ($m) use ($block_ids, &$missing) {
		if (! isset($block_ids[$m[1]])) {
			$missing[] = 'block:' . $m[1];
			return $m[0];
		}
		return '"ref":' . $block_ids[$m[1]];
	}, $content);
	$content = preg_replace_callback('/"__CAT:([a-z0-9-]+)__"/', function ($m) use ($cat_ids, &$missing) {
		if (! isset($cat_ids[$m[1]])) {
			$missing[] = 'cat:' . $m[1];
			return $m[0];
		}
		return (string) $cat_ids[$m[1]];
	}, $content);
	return $content;
}

$missing = [];
$updated = 0;
foreach (get_posts(['post_type' => ['page', 'post', 'wp_block'], 'numberposts' => -1, 'post_status' => 'any']) as $p) {
	if (strpos($p->post_content, '__BLOCK:') === false && strpos($p->post_content, '__CAT:') === false) {
		continue;
	}
	$new = gdp_resolve_placeholders($p->post_content, $block_ids, $cat_ids, $missing);
	if ($new !== $p->post_content) {
		global $wpdb;
		$wpdb->update($wpdb->posts, ['post_content' => $new], ['ID' => $p->ID]);
		clean_post_cache($p->ID);
		$updated++;
	}
}
$log['placeholders_updated_posts'] = $updated;
$log['placeholders_missing']       = array_values(array_unique($missing));

// Wzorce zsynchronizowane: status synchronizacji (pusty = zsynchronizowany).
foreach ($block_ids as $slug => $id) {
	delete_post_meta($id, 'wp_pattern_sync_status');
}

// ---------------------------------------------------------------------------
// 2. Menu
// ---------------------------------------------------------------------------
$menus_file = $config_dir . '/menus.json';
if (file_exists($menus_file)) {
	$menus     = json_decode(file_get_contents($menus_file), true);
	$locations = get_theme_mod('nav_menu_locations', []);
	foreach ($menus['menus'] as $menu) {
		$existing = wp_get_nav_menu_object($menu['slug']);
		if ($existing) {
			wp_delete_nav_menu($existing->term_id);
		}
		$menu_id = wp_create_nav_menu($menu['name']);
		if (is_wp_error($menu_id)) {
			$log['menu_error_' . $menu['slug']] = $menu_id->get_error_message();
			continue;
		}
		wp_update_term($menu_id, 'nav_menu', ['slug' => $menu['slug']]);
		$order = 1;
		$add_items = function ($items, $parent_id) use (&$add_items, $menu_id, &$order) {
			foreach ($items as $item) {
				$page    = get_page_by_path(trim($item['url'], '/'));
				$args    = [
					'menu-item-title'     => $item['title'],
					'menu-item-status'    => 'publish',
					'menu-item-position'  => $order++,
					'menu-item-parent-id' => $parent_id,
				];
				if ($page) {
					$args['menu-item-type']      = 'post_type';
					$args['menu-item-object']    = 'page';
					$args['menu-item-object-id'] = $page->ID;
				} else {
					$args['menu-item-type'] = 'custom';
					$args['menu-item-url']  = home_url($item['url']);
				}
				$item_id = wp_update_nav_menu_item($menu_id, 0, $args);
				if (! empty($item['children']) && ! is_wp_error($item_id)) {
					$add_items($item['children'], $item_id);
				}
			}
		};
		$add_items($menu['items'], 0);
		foreach ($menu['locations'] as $loc) {
			$locations[$loc] = (int) $menu_id;
		}
		$log['menu_' . $menu['slug']] = (int) $menu_id;
	}
	set_theme_mod('nav_menu_locations', $locations);
}

// ---------------------------------------------------------------------------
// 3. Widgety stopki
// ---------------------------------------------------------------------------
$footer_file = $config_dir . '/footer.json';
if (file_exists($footer_file)) {
	$footer   = json_decode(file_get_contents($footer_file), true);
	$blocks   = get_option('widget_block', []);
	$sidebars = get_option('sidebars_widgets', []);
	// Usuń poprzednie widgety blokowe z obszarów stopki (idempotencja).
	foreach ($footer['widgets'] as $sidebar_id => $content) {
		if (! empty($sidebars[$sidebar_id])) {
			foreach ($sidebars[$sidebar_id] as $wid) {
				if (preg_match('/^block-(\d+)$/', $wid, $m)) {
					unset($blocks[(int) $m[1]]);
				}
			}
		}
		$sidebars[$sidebar_id] = [];
	}
	$next = 2;
	foreach (array_keys($blocks) as $k) {
		if (is_int($k) && $k >= $next) {
			$next = $k + 1;
		}
	}
	foreach ($footer['widgets'] as $sidebar_id => $content) {
		$content       = gdp_resolve_placeholders($content, $block_ids, $cat_ids, $missing);
		$blocks[$next] = ['content' => $content];
		$sidebars[$sidebar_id][] = 'block-' . $next;
		$next++;
	}
	$blocks['_multiwidget'] = 1;
	update_option('widget_block', $blocks);
	update_option('sidebars_widgets', $sidebars);
	$log['footer_widgets'] = count($footer['widgets']);
}

// ---------------------------------------------------------------------------
// 4. Strona główna i strona wpisów
// ---------------------------------------------------------------------------
$front = get_page_by_path('start');
if ($front) {
	update_option('show_on_front', 'page');
	update_option('page_on_front', $front->ID);
	$log['page_on_front'] = $front->ID;
}
// /wiedza/ jest zwykłą stroną (hub bazy wiedzy z treścią), wpisy mają adresy /wiedza/<slug>/ (D21).
update_option('page_for_posts', 0);
update_option('permalink_structure', '/wiedza/%postname%/');
update_option('category_base', 'category'); // jawnie, żeby archiwa były pod /category/<slug>/, nie /wiedza/category/
update_option('blog_public', 0);
update_option('timezone_string', 'Europe/Warsaw');
update_option('date_format', 'j.m.Y');
update_option('WPLANG', 'pl_PL');

// ---------------------------------------------------------------------------
// 5. Autor wpisów: importer Playground przypisuje treść bieżącemu użytkownikowi (admin).
//    Wpisy dostają dedykowanego użytkownika „autor” (rola Author) z nazwą-placeholderem (D25),
//    żeby meta Blocksy i blok Autor w Query Loop pokazywały [[ ]], a nie „admin”.
// ---------------------------------------------------------------------------
$autor_id = username_exists('autor');
if (!$autor_id) {
	$autor_id = wp_insert_user([
		'user_login'   => 'autor',
		'user_pass'    => wp_generate_password(24),
		'user_email'   => 'autor@example.invalid',
		'display_name' => '[[Imię i nazwisko autora]]',
		'role'         => 'author',
	]);
}
if ($autor_id && !is_wp_error($autor_id)) {
	$moved = 0;
	foreach (get_posts(['post_type' => 'post', 'post_status' => 'any', 'numberposts' => -1, 'fields' => 'ids']) as $pid) {
		wp_update_post(['ID' => $pid, 'post_author' => $autor_id]);
		$moved++;
	}
	$log['posts_reassigned_to_autor'] = $moved;
}

flush_rewrite_rules();
delete_transient('blocksy_dynamic_styles_descriptor');
if (function_exists('blocksy_manager') && isset(blocksy_manager()->db)) {
	blocksy_manager()->db->wipe_cache();
}
wp_cache_flush();

echo json_encode($log, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT), "\n";

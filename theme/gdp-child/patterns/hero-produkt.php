<?php
/**
 * Title: Hero produktu
 * Slug: gdp/hero-produkt
 * Categories: gdp
 * Description: Nagłówek strony produktu: ścieżka, tytuł H1, definicja (do 60 słów), dwa przyciski.
 * Block Types: core/group
 * Viewport Width: 1400
 */
?>
<!-- wp:group {"metadata":{"name":"Hero produktu"},"templateLock":"contentOnly","align":"full","className":"gdp-hero gdp-hero-produkt","style":{"spacing":{"padding":{"top":"var:preset|spacing|60","bottom":"var:preset|spacing|60"}}},"backgroundColor":"surface","layout":{"type":"constrained"}} -->
<div class="wp-block-group alignfull gdp-hero gdp-hero-produkt has-surface-background-color has-background" style="padding-top:var(--wp--preset--spacing--60);padding-bottom:var(--wp--preset--spacing--60)"><!-- wp:paragraph {"className": "gdp-etykieta"} -->
<p class="gdp-etykieta"><a href="/oferta/">Oferta</a> · [[nazwa produktu]]</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level": 1} -->
<h1 class="wp-block-heading">[[Nazwa produktu]] dla firm</h1>
<!-- /wp:heading -->

<!-- wp:paragraph {"fontSize": "m"} -->
<p class="has-m-font-size">[[Definicja produktu w maksymalnie 60 słowach: co to jest, dla kogo, jaka zasada rozliczenia.]]</p>
<!-- /wp:paragraph -->

<!-- wp:buttons -->
<div class="wp-block-buttons"><!-- wp:button -->
<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="/wgraj-fakture/">Wgraj fakturę</a></div>
<!-- /wp:button -->

<!-- wp:button {"className":"is-style-outline"} -->
<div class="wp-block-button is-style-outline"><a class="wp-block-button__link wp-element-button" href="/oferta/">Porównaj modele ceny</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons --></div>
<!-- /wp:group -->

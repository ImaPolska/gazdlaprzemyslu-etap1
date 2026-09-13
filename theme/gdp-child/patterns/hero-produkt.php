<?php
/**
 * Title: Hero produktu
 * Slug: gdp/hero-produkt
 * Categories: gdp
 * Block Types: core/group
 * Description: Nagłówek strony produktu: H1, odpowiedź w jednym akapicie (do 60 słów), przycisk CTA i mikrodowód. Jedna sekcja = jedna grupa z blokadą contentOnly.
 * Keywords: hero, produkt, oferta
 */
?>
<!-- wp:group {"metadata":{"name":"Hero produktu"},"templateLock":"contentOnly","align":"full","className":"gdp-sekcja gdp-hero","layout":{"type":"constrained","contentSize":"1200px"}} -->
<div class="wp-block-group alignfull gdp-sekcja gdp-hero">
<!-- wp:paragraph {"fontSize":"xs","className":"gdp-etykieta"} -->
<p class="gdp-etykieta has-xs-font-size">Oferta dla firm</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":1} -->
<h1 class="wp-block-heading">Nazwa produktu</h1>
<!-- /wp:heading -->

<!-- wp:paragraph {"fontSize":"m"} -->
<p class="has-m-font-size">Jedno zdanie odpowiedzi: co ten produkt daje Twojej firmie i kiedy ma sens. Maksymalnie 60 słów.</p>
<!-- /wp:paragraph -->

<!-- wp:buttons -->
<div class="wp-block-buttons">
<!-- wp:button -->
<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="/wgraj-fakture/">Wgraj fakturę</a></div>
<!-- /wp:button -->
</div>
<!-- /wp:buttons -->

<!-- wp:paragraph {"fontSize":"xs","className":"gdp-mikrodowod"} -->
<p class="gdp-mikrodowod has-xs-font-size">Oferta w 24 godziny od przesłania faktury. Bez zobowiązań.</p>
<!-- /wp:paragraph -->
</div>
<!-- /wp:group -->

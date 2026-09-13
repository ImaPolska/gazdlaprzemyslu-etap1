<?php
/**
 * Title: Przykład liczbowy
 * Slug: gdp/przyklad-liczbowy
 * Categories: gdp
 * Description: Tabela przykładu z placeholderami i miejscem na zastrzeżenie cen.
 * Block Types: core/group
 * Viewport Width: 1400
 */
?>
<!-- wp:group {"metadata":{"name":"Przykład liczbowy"},"templateLock":"contentOnly","align":"full","style":{"spacing":{"padding":{"top":"var:preset|spacing|70","bottom":"var:preset|spacing|70"}}},"backgroundColor":"surface","layout":{"type":"constrained"}} -->
<div class="wp-block-group alignfull has-surface-background-color has-background" style="padding-top:var(--wp--preset--spacing--70);padding-bottom:var(--wp--preset--spacing--70)"><!-- wp:heading -->
<h2 class="wp-block-heading">Przykład liczbowy</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Przykład dla zakładu o zużyciu [[ ]] MWh rocznie. Wartości uzupełnia PBM.</p>
<!-- /wp:paragraph -->

<!-- wp:table {"className": "gdp-liczby"} -->
<figure class="wp-block-table gdp-liczby"><table><thead><tr><th>Pozycja</th><th>Wartość</th><th>Jednostka</th></tr></thead><tbody><tr><td>Zużycie roczne</td><td>[[ ]]</td><td>MWh</td></tr><tr><td>Cena gazu</td><td>[[ ]]</td><td>zł/MWh netto</td></tr><tr><td>Koszt gazu w roku</td><td>[[ ]]</td><td>zł netto</td></tr><tr><td>Razem w roku</td><td>[[ ]]</td><td>zł netto</td></tr></tbody></table><figcaption class="wp-element-caption">Przykład ilustruje strukturę kosztu, nie ofertę.</figcaption></figure>
<!-- /wp:table -->

<!-- wp:paragraph {"className": "gdp-zastrzezenie"} -->
<p class="gdp-zastrzezenie">Prezentowane pasma cen mają charakter orientacyjny i nie stanowią oferty w rozumieniu art. 66 Kodeksu cywilnego. Warunki określa indywidualna oferta i umowa.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:group -->

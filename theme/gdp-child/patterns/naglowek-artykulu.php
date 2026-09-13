<?php
/**
 * Title: Nagłówek artykułu (baza wiedzy)
 * Slug: gdp/naglowek-artykulu
 * Categories: gdp
 * Block Types: core/group
 * Post Types: post
 * Description: Wstęp-odpowiedź (do 60 słów), autor, data aktualizacji i spis treści jako lista linków. Zgodne z sekcją 10.2 instrukcji (AEO).
 * Keywords: artykuł, wstęp, spis treści
 */
?>
<!-- wp:group {"metadata":{"name":"Nagłówek artykułu"},"templateLock":"contentOnly","className":"gdp-naglowek-artykulu","layout":{"type":"constrained","contentSize":"760px"}} -->
<div class="wp-block-group gdp-naglowek-artykulu">
<!-- wp:paragraph {"fontSize":"m","className":"gdp-wstep"} -->
<p class="gdp-wstep has-m-font-size">Bezpośrednia odpowiedź na pytanie z tytułu. Maksymalnie 60 słów, bez wstępu, bez opisu firmy.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph {"fontSize":"xs","className":"gdp-meta"} -->
<p class="gdp-meta has-xs-font-size">Autor: [[ ]] · Ostatnia aktualizacja: [[data]]</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2,"fontSize":"s"} -->
<h2 class="wp-block-heading has-s-font-size">W tym artykule</h2>
<!-- /wp:heading -->

<!-- wp:list {"ordered":true} -->
<ol class="wp-block-list">
<!-- wp:list-item -->
<li><a href="#sekcja-1">Pierwsza sekcja</a></li>
<!-- /wp:list-item -->
<!-- wp:list-item -->
<li><a href="#sekcja-2">Druga sekcja</a></li>
<!-- /wp:list-item -->
<!-- wp:list-item -->
<li><a href="#zrodla">Źródła</a></li>
<!-- /wp:list-item -->
</ol>
<!-- /wp:list -->
</div>
<!-- /wp:group -->

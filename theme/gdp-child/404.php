<?php
/**
 * Szablon 404 (nadpisuje blocksy/404.php).
 *
 * Wyjątek od zasady „treść tylko w blokach” (decyzja D-13): WordPress nie pozwala przypisać
 * strony blokowej do błędu 404 bez wtyczki, a motyw klasyczny Blocksy nie ma edytora szablonów.
 * Treść ograniczona do minimum: nagłówek, jedno zdanie, dwa przyciski. Bez wykrzykników.
 *
 * @package gdp-child
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();
?>

<div class="ct-container gdp-404" data-vertical-spacing="top:bottom">
	<article class="gdp-404__tresc">
		<h1 class="wp-block-heading"><?php esc_html_e( 'Tej strony nie ma', 'gdp-child' ); ?></h1>
		<p><?php esc_html_e( 'Adres jest błędny albo strona została przeniesiona. Najszybsza droga do oferty to przesłanie faktury.', 'gdp-child' ); ?></p>
		<div class="wp-block-buttons is-layout-flex">
			<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="<?php echo esc_url( home_url( '/wgraj-fakture/' ) ); ?>"><?php esc_html_e( 'Wgraj fakturę', 'gdp-child' ); ?></a></div>
			<div class="wp-block-button is-style-outline"><a class="wp-block-button__link wp-element-button" href="<?php echo esc_url( home_url( '/' ) ); ?>"><?php esc_html_e( 'Strona główna', 'gdp-child' ); ?></a></div>
		</div>
	</article>
</div>

<?php
get_footer();

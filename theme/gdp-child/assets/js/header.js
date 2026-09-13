/* Nagłówek sticky z redukcją wysokości po przewinięciu (Blocksy free nie ma tej funkcji). */
(function () {
	var root = document.documentElement;
	var threshold = 40;
	var ticking = false;
	function update() {
		ticking = false;
		var scrolled = (window.scrollY || root.scrollTop) > threshold;
		if (scrolled !== root.classList.contains('gdp-scrolled')) {
			root.classList.toggle('gdp-scrolled', scrolled);
		}
	}
	window.addEventListener('scroll', function () {
		if (!ticking) {
			ticking = true;
			window.requestAnimationFrame(update);
		}
	}, { passive: true });
	update();
})();

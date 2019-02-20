/*!
 * Determine if an element is in the viewport
 * (c) 2017 Chris Ferdinandi, MIT License, https://gomakethings.com
 * @param  {Node}    elem The element
 * @return {Boolean}      Returns true if element is in the viewport
 */
var isInViewport = function (elem) {
	var distance = elem.getBoundingClientRect();
	return (
		distance.top >= 0 &&
		distance.left >= 0 &&
		distance.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
		distance.right <= (window.innerWidth || document.documentElement.clientWidth)
	);
};



document.addEventListener('DOMContentLoaded', () => {

    var klaus = document.getElementsByTagName("nav");
    Velocity(klaus, { opacity: [1, 0] }, {duration: 1000, easing: 'ease-in'} );


  // Get all "navbar-burger" elements
  const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

  // Check if there are any navbar burgers
  if ($navbarBurgers.length > 0) {

    // Add a click event on each of them
    $navbarBurgers.forEach($el => {
      $el.addEventListener('click', function () {

        // Get the target from the "data-target" attribute
        const target = $el.dataset.target;
        const $target = document.getElementById(target);

        // Toggle the class on both the "navbar-burger" and the "navbar-menu"
        $el.classList.toggle('is-active');
        //$target.classList.toggle('is-active');
        var sideMenu = document.getElementById("sideMenu");
        if (sideMenu.style.display === "none") {
            Velocity(sideMenu, { transform: [ "translate(0)", "translate(100%)" ], opacity: [ 1, 0 ], display: ['block', 'none'] }, 150, "ease-out")
          } else {
            Velocity(sideMenu, { transform: ["translate(100%)", "translate(0)"], opacity: [ 0, 1 ], display: ['none', 'block'] }, 150, "ease-in")
          }
      });
    });
  }
});

/**
 * Simulate a click event.
 * @public
 * @param {Element} elem  the element to simulate a click on
 * example:
var someLink = document.querySelector('a');
simulateClick(someLink);
 */
 /*
var simulateClick = function (elem) {
	// Create our event (with options)
	var evt = new MouseEvent('click', {
		bubbles: true,
		cancelable: true,
		view: window
	});
	// If cancelled, don't dispatch our event
	var canceled = !elem.dispatchEvent(evt);
};*/



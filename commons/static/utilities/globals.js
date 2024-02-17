


	// G E N E R A L

	var NULLTEXT = '';
	var MOBILE   = 0;       var DESKTOP = 1;
	var NO		 = 0;		var YES     = 1;
	var OFF		 = 0;		var ON      = 1;
	var CLOSED	 = 0;		var OPEN    = 1;
	var LEFT	 = 0;		var RIGHT   = 1;
	var PLINE	 = 'P';		var CLINE   = 'C';

	// const ENGLISH	= 0;    ... see locale.js
    // const FRENCH		= 1;    ... see locale.js

    let Device       = DESKTOP;
    let DisplayMode  = DESKTOP;
    let CurrentPanel = 1;
	let Width 	     = window.screen.width;
	var ASPECT	     = Width / window.screen.height;
	var ZOOMSCALE	 = ( Width > 1919 ? 1.00 : ( Width > 1535 ? 1.25  : 1.50 ) );	// breakpoints for responsive single file css specification

    const System     = {};

        function dadaw() {
        alert('what the heck?')
        //Img = document.createElement('img')
        //Img.src = {{ Dislikes }}
    }

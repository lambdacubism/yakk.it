
/*	   C O N T R O L  B A R	   */

// TSX : import { Config, Locale, DateTime, changeDaytimeMode } 		from "../../_i/utilities";
// TSX : import { imgLOGOsrc, imgNOONsrc, imgSUNSETsrc }  				from '../../_i/images';

function none() {
   //... create control bar function labels/handlers
    Locale.changeLanguage( ENGLISH );
    let Span	= [];
    let Handler = [ 'crex()', 'MI()', 'showUV()',  'dummyX()',  'findx()',  'rulex()', 'hideNote01()',  'sticker()',  'run()' ];
    for ( let i=0; i<9; i++ ) {
        Span.push( document.createElement('span') );
        Span[i].id          = 'SPAN' + i;
        Span[i].innerHTML   = Locale.cthControlBarLabel[i] + '&nbsp; '.repeat(8);
        Span[i].onclick     = function() { eval( Handler[i] );  };
        BarDIV.appendChild( Span[i] );
    }
}

function redisplayBarLabels( Language ) {
    Locale.changeLanguage( Language );
    alert(System.ControlBar.children.length)
    for( let i=0; i<System.ControlBar.children.length-1; i++ )
        alert( Locale.cthControlBarLabel[i] )
}

// TSX : export const DUMMYControlBar = 0

    function swipe( E ) {
        let Swipe = ''
		let  x1 = 0, x2 = 0;
		E.onmousedown = dragMouseDown;

		function dragMouseDown( e ) {
			e.preventDefault();
			x2              = e.clientX;
			E.onmouseup     = closeDragElement;
			E.onmousemove   = dragElement;
	    }
        function dragElement( e ) {
			e.preventDefault();
			if ( e.clientX > x2 ) {
				x1 = x2 - e.clientX;
				Swipe = LEFT;
			}
			else {
    			x2 = e.clientX;
    			Swipe = RIGHT;
    		}
		}
        function closeDragElement() {
            swipePanel( Swipe )
            E.onmouseup   = null;
//???       E.onmousedown = null;
            E.onmousemove = null;
        }
    }

    function swipePanel( Swipe ) {
        for( let p=0; p<3; p++ )
            ; //System.Panel[p].style.zIndex = '10';
        System.Panel[1].style.zIndex = '11';

        if ( Swipe == LEFT ) {
            if      ( CurrentPanel == 2 )   { System.Panel[1].style.zIndex = '12';      CurrentPanel = 1;   }
            else if ( CurrentPanel == 1 )   { System.Panel[0].classList.add('slidetoright'); System.Panel[0].style.animationName = 'slidetoright';  System.Panel[0].style.zIndex = '12';      CurrentPanel = 0;   }
            else if ( CurrentPanel == 0 )   { System.Panel[0].classList.add('slidetoright'); System.Panel[0].style.animationName = 'slidetoright';  System.Panel[0].style.zIndex = '12';      CurrentPanel = 0;   }
        }
        else {
            if      ( CurrentPanel == 0 )   { System.Panel[1].style.zIndex = '12';      CurrentPanel = 1;   }
            else if ( CurrentPanel == 1 )   { System.Panel[2].classList.add('slidetoleft'); System.Panel[2].style.animationName = 'slidetoleft';  System.Panel[2].style.zIndex = '12';      CurrentPanel = 2;   }
            else if ( CurrentPanel == 2 )   { System.Panel[2].classList.add('slidetoleft'); System.Panel[2].style.animationName = 'slidetoleft';  System.Panel[2].style.zIndex = '12';      CurrentPanel = 2;   }
        }
    }


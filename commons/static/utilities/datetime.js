

/*	 D A T E   T I M E 	   */


//  displays on the upper LHS the weekday (and month) in a designated language using the Locale object

// TSX : import { Locale  }  					from "../../_i/utilities";

function xcreateDateTime() {

    DIV                         = document.createElement('div')
    DIV.classList.add('fCNT');
    DIV.style.cssText		    = 'position:absolute; z-index:300; opacity:0.9; top:2.6%; left:0.6%; width:3.6%; text-align:center; font-size:0.65vw; line-height:0.85vw; ';
    DIV.Date				    = document.createElement('span');
    Space					    = document.createElement('span');
    Space.style.cssText	        = 'padding:1px; color:#f00';
    //Month				        = document.createElement('span');	//Month.style.cssText	= 'display:none';
    DIV.Weekday			        = document.createElement('span');
    DIV.Time				    = document.createElement('span');
    DIV.Time.style.cssText	    = 'font-size:0.9vw; color:#f00';
    DIV.appendChild( DIV.Date );
    DIV.appendChild( Space );
    //DIV.appendChild( Month );
    DIV.appendChild( DIV.Weekday );
    DIV.appendChild( document.createElement('br') );
    DIV.appendChild( DIV.Time );
    document.body.appendChild( DIV );
    DIV.clock = clock;

    function clock() {

        let DT	                = new Date();
        let Hours               = DT.getHours() + 1;

        DIV.Date.innerText	    = '' + DT.getDate();
        //Month.innerText	    = Locale.cthMonth[ DT.getMonth() ] + 10;		// january is 0, february is 1, ...
        DIV.Weekday.innerText	= Locale.cthWeekday[ DT.getDay() ];
        DIV.Time.innerText		= addZero ( Hours == 0 ? 23 : Hours-1 ) + ':' + addZero(DT.getMinutes() );

        //let MonthCap 		    = [ 31,28,31,30,31,30,31,31,30,31,30,31 ];
        //DayOffset 		    = ( ()=>{ let Off = 0; for( let i=0; i < MonthN; i++ ) Off += MonthCap[ MonthN-1 ]; return (Off + parseInt(Day)) } )();

        function addZero( T ) { return (  T < 10 ? '0' + T.toString() : T.toString() ) }
    }

    return DIV;
}

// TSX : export { DateTime }


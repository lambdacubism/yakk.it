

/*	 L O C A L E	   */

const ENGLISH		        = 0;
const FRENCH		        = 1;

const ControlBarLabel		= [ ['new','neuve', 'yeni'], ['MI','frMI'], ['UV','frUV'], ['I/O','frI/O'], ['find','trouvez'], ['AST','frAST'], ['colormark','couleur'], ['sticker','etiquette'], ['run','marchez'] ];
const Month					= [ ['january','janvier'], ['february','février'], ['march','mars'], ['april','avril'], ['may','mai'], ['june','juin'], ['july','juillet'],  ['august','août'], ['september','septembre'], ['october','octobre'], ['november','november'], ['december', 'décembre'] ];
const Weekday				= [ ['SUN','DIM'], ['MON','LUN'], ['TUE','MAR'], ['WED','MER'], ['THU','JEU'], ['FRI','VEN'], ['SAT','SAM'] ];

class locale {
	cthLanguage 			= ENGLISH;     // : number 	= ENGLISH;
	cthControlBarLabel		= [];          // : string[]	= [];
	cthMonth				= [];          // : string[]	= [];
	cthWeekday				= [];          // : string[]	= [];

	constructor () {
	}

	changeLanguage( cthLanguage ) {
		this.cthLanguage			= cthLanguage;
		this.cthControlBarLabel		= ControlBarLabel.map( function( Value )	 { return Value[ cthLanguage ]; } );
		this.cthMonth				= Month.map( function( Value ) 				 { return Value[ cthLanguage ]; } );
		this.cthWeekday				= Weekday.map( function( Value ) 			 { return Value[ cthLanguage ]; } );
	}
}

const Locale = new locale();
Locale.changeLanguage( ENGLISH );

// TSX : export { Locale }



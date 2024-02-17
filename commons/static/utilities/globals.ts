

/*    G L O B A L S    !!! NOT a MODULE  !!!    */

var Counter = 0;
	//

	// G E N E R A L
	var NULLTEXT : string = '';
	var NO		 : number = 0;		var YES   : number = 1;
	var OFF		 : number = 0;		var ON    : number = 1;
	var CLOSED	 : number = 0;		var OPEN  : number = 1;
	var LEFT	 : number = 0;		var RIGHT : number = 1;
	var PLINE	 : string = 'P';	var CLINE : string = 'C';
	
	let Width 		= window.screen.width;
	var ASPECT		= Width / window.screen.height;
	var ZOOMSCALE	= ( Width > 1919 ? 1.00 : ( Width > 1535 ? 1.25  : 1.50 ) );	// breakpoints for responsive single file css specification
																					// used by numeric image dimensions

	// E D I T O R
	var LineHeightFactor	: number = 4;
	var CommentFontFamily	: string = 'Times Roman';
	var CommentFontSize		: string = '1.2em';
	var OUT					: number = OFF;
	var zColor				: string = '';

	var NUMERAL				: string = '0';
	var TEXTUAL				: string = '1';
	var CODE				: string = '2';
	
	var SOT					: number = 0;											// when moving forward/backwards
	var EOT					: number = 1;											// when moving backward !!!
	var FCOT				: number = 2;											// when moving backward !!!
	var MT					: number = 3;											// when moving forward/backward
	
	// locus ( editor + transfuser + keyword )
	var BASE				: string = '0';
	var UR					: string = '1';
	var LR					: string = '2';
	var LL					: string = '3';
	var UL					: string = '4';
	var MID					: string = '0';
	var SUPER				: string = 'u';
	var SUPERSUPER			: string = 'v';
	var SUB					: string = 'd';
	var SUBSUB				: string = 'e';

	

	// T R A N S F U S E R
	var DEBUG 				: number = OFF;
	var EditLayer			: string = 'L1';

	

/*
	style style : position > z-index > visibility > opacity > background

	index 0		"CANVAS"

	index 20-30	CONTROLBAR	21		control bar
					22		logo
					22		input
					22		daytime switch

	index		talk zone	10
	index		hide zone	11

	index 1-16	UVAREA		-		base
					1		border (shadow1)		lower than 11 aline, bline, liner
					1		border (shadow2)		lower than 11 aline, bline, liner
					15		thin dark area (hemline)	higher than 11 aline, bline, liner
					16		content dark area		higher than 11 aline, bline, liner

	index 10-15	EDITAREA	-		base
					11		cline
					12		vertical split
					13		aline, liner
					13		LN (line number)
					14		LNsVeil
					14		LNsSensor
					14		slider

	index 20	MONITORS	20		HTML monitor
					20		symbols monitor


	index 100	popups		14


	index 200	stickers	14/15 > 10	sticker				when passivized (transparently), the sticker goes underneath aline (cline)

	index		MODULE		

	index		LHS menu
	index		RHS menu

			timeline	15		timeline guidelines		higher than LNsVeil
					16		timeline points
*/


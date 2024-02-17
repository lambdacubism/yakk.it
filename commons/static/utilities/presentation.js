	


/*	P R E S E N T A T I O N		*/
	
/* this is the only module (hopefuly) that makes use of the BACKDOOR SCOPING, i.e., accesses other 
   classes' presentation (css) properties directly through the DOM mechanism
   
   consequently, the id's have to be "handcrafted" into the calling routines making their maintenance
   also prone to poor synchronization although it is a one time effort and of low frequency
*/

// TSX : import { alrt, Config, setElementProperty, setClassProperty }    	from "../../_i/utilities";
// TSX : import { Cth }    							from "../../_i/editor";

//  let BUG_BUG_BUG = Cth;	// ????????????!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


function changeDaytimeMode( Mode ) {	//: string )

	//... background
	setElementProperty( 'BODY',       '--dnBACKGROUNDBODY',       Mode + 'BACKGROUNDBODY' )

	//... control bar(s)
	setElementProperty( 'CONTROLBAR0', '--dnBACKGROUNDCONTROLBAR', Mode + 'BACKGROUNDCONTROLBAR' )
	setElementProperty( 'CONTROLBAR0', '--dnFONTCONTROLBAR',       Mode + 'FONTCONTROLBAR' )
	setElementProperty( 'CONTROLBAR0', '--dnSHADOWBLACK',          Mode + 'SHADOWBLACK' )
	setElementProperty( 'CONTROLBAR1', '--dnBACKGROUNDCONTROLBAR', Mode + 'BACKGROUNDCONTROLBAR' )
	setElementProperty( 'CONTROLBAR1', '--dnFONTCONTROLBAR',       Mode + 'FONTCONTROLBAR' )
	setElementProperty( 'CONTROLBAR1', '--dnSHADOWBLACK',          Mode + 'SHADOWBLACK' )
    setElementProperty( 'CONTROLBAR2', '--dnBACKGROUNDCONTROLBAR', Mode + 'BACKGROUNDCONTROLBAR' )
	setElementProperty( 'CONTROLBAR2', '--dnFONTCONTROLBAR',       Mode + 'FONTCONTROLBAR' )
	setElementProperty( 'CONTROLBAR2', '--dnSHADOWBLACK',          Mode + 'SHADOWBLACK' )


	// noon/sunset switch
	if ( Mode == '--d' )
		Config.DaytimeMode = '--d';
	else
		Config.DaytimeMode = '--n';

    //... panels
	setElementProperty( 'MASK0',         '--dnBACKGROUNDPANELLR',    Mode + 'BACKGROUNDPANELLR' )
	setElementProperty( 'MASK1',         '--dnBACKGROUNDPANELC',     Mode + 'BACKGROUNDPANELC' )
	setElementProperty( 'MASK2',         '--dnBACKGROUNDPANELLR',    Mode + 'BACKGROUNDPANELLR' )


    return;

    //...  popups
    setElementProperty( 'MODULESBASE',   '--dnPopups',     Mode + 'POPUPS' )
    setElementProperty( 'MODULESBASE',   '--dnShadow2',    Mode + 'SHADOW2' )
    setElementProperty( 'MODULESARROWS', '--dnFontPOPUP',  Mode + 'FONTPOPUP' )
    setElementProperty( 'MODULES',       '--dnFontPOPUP',  Mode + 'FONTPOPUP' )

    setElementProperty( 'CHANNELBASE',   '--dnPopups',     Mode + 'POPUPS' )
    setElementProperty( 'CHANNELBASE',   '--dnShadow2',    Mode + 'SHADOW2' )

    setClassProperty( 'popu', '--dnPopups',   Mode + 'POPUPS' )

	//... adjust font color changes for modules list (editor.js)
	for ( let ithModule = 0; ithModule < 9; ithModule++ ) {		//ModulesMasterArray.length; ithModule++ ) {
		setElementProperty( 'ML' + ithModule.toString(), '--dnFontPOPUP', Mode + 'FONTPOPUPh');
		setElementProperty( 'ML' + ithModule.toString(), '--dnFontPOPUP', Mode + 'FONTPOPUP' );
	}
	//... adjust font color changes for arrow labels (editor.js)
	setElementProperty( 'PREVMODULE', '--dnFontPOPUP', Mode + 'FONTPOPUPh');	setElementProperty( 'PREVMODULE', '--dnFontPOPUP', Mode + 'FONTPOPUP');
	setElementProperty( 'NEXTMODULE', '--dnFontPOPUP', Mode + 'FONTPOPUPh');	setElementProperty( 'NEXTMODULE', '--dnFontPOPUP', Mode + 'FONTPOPUP');

	//... adjust opacity for arrows (editor.js)
	setElementProperty( 'MODULESLEFTARROW', '--dnOpacity1', Mode + 'OPACITY1h');	setElementProperty( 'MODULESLEFTARROW', '--dnOpacity1', Mode + 'OPACITY1');
	setElementProperty( 'MODULESRIGHTARROW','--dnOpacity1', Mode + 'OPACITY1h');	setElementProperty( 'MODULESRIGHTARROW','--dnOpacity1', Mode + 'OPACITY1');

	//... MI
	setElementProperty( 'MIRESPONSE', '--dnFont3', Mode + 'FONT3' );

	setClassProperty( 'fCMM', '--dnFONTCOMMENTS',   Mode + 'FONTCOMMENTS' );
}


// TSX : export { changeDaytimeMode }
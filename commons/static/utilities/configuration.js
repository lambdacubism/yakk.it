

/*    C O N F I G U R A T I O N		*/


//  all preference (configuration) parameters are maintained in a single object
class configuration {

	DaytimeMode; 	//: string;
	Monitoring;  	//: number;
	
	constructor() {
		this.DaytimeMode = '--n';								// night mode	('--d' for day mode)
		this.Monitoring  = 1;
	}	
}
const Config  = new configuration();


// TSX : export { Config }
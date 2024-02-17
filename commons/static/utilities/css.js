


function setElementProperty( Element, Property, Parameter) {	
	document.getElementById(Element).style.setProperty( Property,  getComputedStyle(document.documentElement).getPropertyValue(Parameter) )
}

function setClassProperty( Class, Property, NewValue) {
	
	const Elements = document.getElementsByClassName( Class );
	for(let i=0; i<Elements.length; i++) {
		Elements[i].style.setProperty( Property, getComputedStyle( document.documentElement ).getPropertyValue( NewValue ) )
	}
}

/*
function css( Element : HTMLElement, Style : CSSStyleDeclaration ) {
	for (const property in Style)
		Element.style[ property ] = Style[ property ];
}*/



// TSX : export { setElementProperty, setClassProperty }



	function getAccount( AccountNr ) {
		fetch(
			'/' + 'getAccount', {
				method  : 'POST',
				headers : { 'Accept' : 'application/json', 'Content-Type' : 'application/json', 'X-CSRFToken' : csrfToken },
				//body    : '{"' + 'dummy' + '":' + '"dummy"' + '}'
				body    : '{"' + 'AccountNr' + '":' + '"' + AccountNr + '"'+ '}'
			}
		)
	   .then(( Response ) =>  Response.text()  )
	   .then( ( ResponseText ) => { document.getElementById( 'ACCOUNTS' ).innerHTML = ResponseText } )
	}

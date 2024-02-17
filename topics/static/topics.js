	/* ............ topic ..................................................................................... */

	function createTopic(  ) {

		//... check eligibility !!!!!!!!!!!!!!!
		//... check compliance : if everything is completed ( "submitted"! )
		NewTopicCategory = "NEW CATEGORY"
		NewTopicTitle 	 = "NEW TOPIC"
		NewTopicStatus 	 = "NEW STATUS"
		FirstYakk 		 = 'let there be light!...'

		fetch(
			'/' + 'createTopic', {
				method  : 'POST',
				headers : { 'Accept' : 'application/json', 'Content-Type' : 'application/json', 'X-CSRFToken' : csrfToken },
				body    : '{"' + 'NewTopicCategory' + '":' + '"' + NewTopicCategory + '"' +  ', "' +  'NewTopicTitle' + '":' + '"' + NewTopicTitle + '"' + ', "' + 'NewTopicStatus' + '":' + '"' + NewTopicStatus + '"' + ', "' + 'FirstYakk' + '":' + '"' + FirstYakk + '"' + '}'
			}
		)
	   .then(( Response ) =>  Response.text()  )
	   .then( ( ResponseText ) => { document.getElementById( 'YAKKS' ).innerHTML = ResponseText } )
	}

	function getTopics( TopicNr ) {
		fetch(
			'/' + 'getTopics', {
				method  : 'POST',
				headers : { 'Accept' : 'application/json', 'Content-Type' : 'application/json', 'X-CSRFToken' : csrfToken },
				//body    : '{"' + 'dummy' + '":' + '"dummy"' + '}'
				body    : '{"' + 'TopicNr' + '":' + '"' + TopicNr + '"'+ '}'
			}
		)
	   .then(( Response ) =>  Response.text()  )
	   .then( ( ResponseText ) => { document.getElementById( 'TOPICS' ).innerHTML = ResponseText } )
	   //.then( ( ResponseText ) => { alert('so far'); dadaw() } )
	}


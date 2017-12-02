var listOfEvents = [] ;
var elements = [];

function eventsExtractor(){
	var eachEvent = {};
    var matchTime = document.querySelector('#VenueDetails').innerText.split(' - ')[2] + document.querySelector('#VenueDetails').innerText.split(' - ')[3].split(" (")[0];
    var matchTeams  = document.querySelector('#teamHomeName').innerHTML.split(">")[1].split(" <")[0] + ":" + document.querySelector("#teamAwayName").innerHTML.split(">")[1].split(" <")[0];
    elements = document.querySelectorAll('#commentary li');
	var num ;
	for(num = 1 ; num < elements.length ; num++){
		eachEvent = { relativeTime : elements[num].innerHTML.split('time">')[1].split(' </div')[0],
		eventComment : elements[num].innerHTML.split('comment">')[1].split('<br>')[0]};
		listOfEvents.push(eachEvent);
	}
	sendEvents(listOfEvents,matchTime,matchTeams);

}

function sendEvents(eventsList,matchTime,matchTeams){
	var xhr = new XMLHttpRequest();
	var url = "http://localhost:3000/events/sendEvents";
	xhr.open("POST", url, true);
	xhr.setRequestHeader("Content-type", "application/json");
	xhr.onreadystatechange = function () {
	    if (xhr.readyState === 4 && xhr.status === 200) {
	        var response = xhr.responseText;
	        if(response !== null){
	        	console.log('- ' + response.length + ' events extracted successfully');
	        	console.log(response.matchId);
	        }
	    }
	};
	xhr.send(JSON.stringify({eventsList:eventsList,matchId:matchId,matchTime:matchTime,matchTeams:matchTeams}));
}


eventsExtractor(1);

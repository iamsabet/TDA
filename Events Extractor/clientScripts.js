var listOfEvents = [] ;
var elements = [];

function eventsExtractor(matchId){
	var eachEvent = {};
    var matchTime = document.querySelector('#VenueDetails').innerText.split(' - ')[2] + " - " +  document.querySelector('#VenueDetails').innerText.split(' - ')[3].split(" (")[0];
    console.log(matchTime);
    var matchTeams  = document.querySelector('#teamHomeName').innerHTML.split(">")[1].split(" <")[0] + "-" + document.querySelector("#teamAwayName").innerHTML.split(">")[1].split(" <")[0];
    elements = document.querySelectorAll('#commentary li');
	var num ;
    var penalties = true;
    var lastEventTime = 0;
    var firstHalfExtra = 2;
    var p = 0;
	for(num = elements.length-1  ; num > -1 ; num--){

        var eventTime = elements[num].innerHTML.split('time">')[1].split(' </div')[0];
            console.log(eventTime);
            if(eventTime === ""){
                if(penalties){
                    if(p % 3 === 0) {
                        lastEventTime++;
                    }
                    p++;
                    eventTime = lastEventTime;
                }
            }
            else {
                if (eventTime.split("+").length > 1) {
                    eventTime = parseInt(eventTime.split("+")[0]) + parseInt(eventTime.split("+")[1]);
                    if (eventTime > 90 && eventTime <= 105) {
                        eventTime = parseInt(eventTime) + 15 + 5;
                    }
                    else if (eventTime > 105) {
                        eventTime = parseInt(eventTime) + 15 + 10;
                    }
                    lastEventTime = eventTime;
                }//
                else {
                    eventTime = parseInt(eventTime);
                    if (parseInt(eventTime) > 45 && parseInt(eventTime) <= 90) {
                        eventTime = parseInt(eventTime) + 15;

                    }
                    else if (parseInt(eventTime) > 90 && parseInt(eventTime) <= 105) {
                        eventTime = parseInt(eventTime) + 15 + 5;
                    }
                    else if (parseInt(eventTime) > 105) {
                        eventTime = parseInt(eventTime) + 15 + 10;
                        penalties = true;
                    }
                    lastEventTime = eventTime;

                }
            }
        eachEvent = { relativeTime : eventTime,
            eventComment : elements[num].innerHTML.split('comment">')[1].split('<br>')[0]};
        listOfEvents.push(eachEvent);
	}
	sendEvents(listOfEvents,matchId,matchTime,matchTeams);

}

function sendEvents(eventsList,matchId,matchTime,matchTeams){
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
	console.log(matchTime);
	xhr.send(JSON.stringify({eventsList:eventsList,matchId:matchId,matchTime:matchTime,matchTeams:matchTeams}));
}


eventsExtractor(4);




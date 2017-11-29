var listOfEvents = [] ;
var elements = [];
function eventsExtractor(){
	var eachEvent = {};
	elements = document.querySelectorAll('#commentary li');
	var num ;
	for(num = 1 ; num < elements.length ; num++){
		eachEvent = { relativeTime : elements[num].innerHTML.split('time">')[1].split(' </div')[0],
		eventComment : elements[num].innerHTML.split('comment">')[1].split('<br>')[0]};
		listOfEvents.push(eachEvent);
	}
	sendEvents(listOfEvents,function(matchId){
		var matchTime = document.querySelector('#VenueDetails').innerText.split(' - ')[2] + document.querySelector('#VenueDetails').innerText.split(' - ')[3].split(" (")[0];
		var teams  = document.querySelector('#teamHomeName') + ":" + document.querySelector("#teamAwayName");
        sendMatchInfo(matchTime,teams,matchId);
	});

}

function sendEvents(eventsList,callback){
	var xhr = new XMLHttpRequest();
	var url = "http://localhost:3000/events/sendEvents";
	xhr.open("POST", url, true);
	xhr.setRequestHeader("Content-type", "application/json");
	xhr.onreadystatechange = function () {
	    if (xhr.readyState === 4 && xhr.status === 200) {
	        var response = xhr.responseText;
	        if(response !== null){
	        	console.log('- ' + eventsList.length + ' events extracted successfully');
                callback(response);
	        }
	    }
	};
	xhr.send(JSON.stringify({eventsList:eventsList}));
}
function sendMatchInfo(time,teams,matchId){
    var xhr = new XMLHttpRequest();
    var url = "http://localhost:3000/events/sendInfo";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = xhr.responseText;
            if(response === true){
                console.log('- ' + list.length + ' events extracted successfully');
            }
        }
    };
    xhr.send(JSON.stringify({matchTime:time,matchTeams:teams,matchId:matchId}));
}

eventsExtractor();

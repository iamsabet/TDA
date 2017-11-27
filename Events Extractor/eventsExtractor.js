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
	sendData(listOfEvents);
}

function sendData(eventsList){
	var xhr = new XMLHttpRequest();
	var url = "http://localhost:3000/events/sendData";
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
	xhr.send(JSON.stringify({eventsList:eventsList}));
}


eventsExtractor();

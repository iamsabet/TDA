var express = require('express');
var router = express.Router();
var cors = require('cors');
var randomstring = require("randomstring");
var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017/twitsDb";

MongoClient.connect(url, function(err, db) {
    console.log("connected to db");
});
router.all('/', function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "http://www.uefa.com");
    res.header("Access-Control-Allow-Headers", "X-Requested-With");
    res.header("Access-Control-Allow-Methods", "POST GET");
    res.header("X-Frame-Options", "ALLOWALL");
    res.header("Access-Control-Allow-Credentials", "true");
    next();
});
router.use(cors({origin: 'http://www.uefa.com'}));
router.post("/",cors(), function (req, res) {
    console.log("asb");
    
});
router.post("/sendEvents",cors(), function (req, res) {

    MongoClient.connect(url, function (err, db) {
        var eventsList = req.body["eventsList"];
        var matchTeams = req.body["matchTeams"];
        var matchDate  = req.body["matchTime"];
        var matchTime = req.body["matchTime"].split(" - ")[0].toString();
        var matchId = req.body["matchId"];
        var date = new Date ( Date.parse("2016-07-10T16:30+00:00") );  // 21:00 16 jul - france vs por
        var options = {
            weekday: "long", year: "numeric", month: "short",
            day: "numeric", hour: "2-digit", minute: "2-digit"
        };
        date.toLocaleTimeString("en-us", options);
        var eventmiliSecondsTime = date.getTime();
        console.log(eventmiliSecondsTime);
        for (var x = 0 ; x < eventsList.length ; x++) {
            var event = {};
            var comment = eventsList[x].eventComment;
            var splitedComment = comment.split(')');
            event.matchId = matchId;
            event.eventName = splitedComment[1] || null;
            event.subject = splitedComment[0] + ')' || null;
            event.eventKey = splitedComment[1] || null;
            if (splitedComment.length === 2) {
                event.object = null;
                var key = comment.split('.')[0].split(' ')[comment.split('.')[0].split(' ').length - 1];
                if (key === 'goal') {
                    event.eventKey = 'effort';
                }
                else if (key === 'target') {
                    event.eventKey = 'miss';
                }
                else if (key === 'corner') {
                    event.eventKey = 'corner';
                }
                else if (key === 'offside') {
                    event.eventKey = 'offside';
                }
                else if (key === 'free-kick') {
                    event.eventKey = 'free-kicks';
                }
                else if (key === 'shot') {
                    event.eventKey = 'blocks';
                }
                else if (key === 'blocked') {
                    event.eventKey = 'blocked';
                }
                else if (key === 'scores!</span>') {
                    event.eventKey = 'score';
                    event.subject = event.subject.split('b">')[1];
                }
                else if (key === 'save') {
                    event.eventKey = 'save';
                }
            }
            else if (splitedComment.length === 3) {
                if (comment.split('foul').length === 2) {
                    event.object = splitedComment[1].split('on ')[1] + ')';
                    event.eventKey = 'foul';
                }
                if (comment.split('cautioned').length === 2) {
                    event.eventKey = 'yellowCard';
                    event.object = event.subject.split('b">')[1];
                    event.subject = 'referee';
                }
            }
            console.log(eventsList[x].relativeTime);
            event.matchTeams = matchTeams;
            event.matchTime  =  matchDate; // France GMT+1;
            event.relativeTime = eventsList[x].relativeTime;
            event.eventTime = ((eventsList[x].relativeTime*60000) + eventmiliSecondsTime); //
                console.log(JSON.stringify(event) + '\n');

                if (err) throw err;
                db.collection("events").insertOne(event, function (err, res) {
                    if (err) throw err;

            });
            if(x === eventsList.length - 1){
                res.send({matchId:matchId,length:eventsList.length});
            }
        }
    });
});

router.get("/plot",cors(), function (req, res) {
    console.log("asb");
    MongoClient.connect(url, function (err, db) {
        if(err) throw err;
        console.log("asb2");
        console.log(db);
        db.collection("twits").find({
            "twitmiliSeconds": {
                "$gt": 1468108920000,
                "$lt": 1468118160000
            }
        }, function (err,list) {
            var tweets = list;
            console.log(list);
            var lastStep = 1468108920000;
            var minutes = 0;
            var lastMode = 0;
            var twitsCounter = 0;
            var twitNumbers = [];
            var eventCounter = 0;
            var eventList = [];
            var axis = [0];
            for (var tweet in tweets) {
                if ((tweet["twitmiliSeconds"] - lastStep) > 60000) {
                    minutes += 1;
                    axis.push(minutes);
                    twitNumbers.push(twitsCounter);
                    lastStep += 60000;
                    twitsCounter = 0;
                }
                else {
                    twitsCounter += 1;
                    lastPlace = 0;
                    eventTimeLine = [];
                    y = 0;
                }
                if(y === tweets.length -1) {
                    for (var x = 0; x < minutes; x++) {

                        db.collection("events").find({"relativeTime": x}, function (err, res) {
                            var eventList = res;
                            for (var event in eventList) {
                                if (event["relativeTime"]) {
                                    eventTimeLine.push({
                                        "eventTime": x,
                                        "name": event["eventName"],
                                        "subject": event["subject"],
                                    });
                                }
                            }
                        });
                        if (x === minutes - 1) {
                            res.send({"axis": axis, "twitNumbers": twitNumbers, "eventTimeLines": eventTimeLine});
                        }
                    }
                }
                y++;
            }
        });
    });
});
module.exports = router;

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
router.get("/",cors(), function (req, res) {
        res.send('hellow');
});
router.post("/sendEvents",cors(), function (req, res) {

    MongoClient.connect(url, function (err, db) {
        var eventsList = req.body["eventsList"];
        var matchTeams = req.body["matchTeams"];
        var matchDate  = req.body["matchTime"];
        var matchTime = req.body["matchTime"].split(" - ")[0].toString();
        var matchId = req.body["matchId"];
        console.log(matchTime);
        var dateStrings = matchTime.split("/");
        var newTime = dateStrings[2] + "-"+ dateStrings[1] + "-"+dateStrings[0];
        var date = new Date(Date.parse(newTime+"T01:01+05:00"));
        var eventSecondsTime = date.getTime()/1000;
        console.log();
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
            event.eventTime = ((eventsList[x].relativeTime*60) + eventSecondsTime); //
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


module.exports = router;

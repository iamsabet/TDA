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

        var matchId = randomstring.generate({
            length: 10,
            charset: 'alphabetic'
        });
    MongoClient.connect(url, function (err, db) {
        var eventsList = req.body["eventsList"];
        var matchId = req.body["matchId"];
        var matchTeams = req.body["matchTeams"];
        var matchTime = req.body["matchTime"];
        console.log(matchId , matchTime ,matchTeams);
        for (var x = 0 ; x < eventsList.length ; x++) {
            var event = {};
            var comment = eventsList[x].eventComment;
            var splitedComment = comment.split(')');
            event.id = 1;
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
            event.matchTeams = matchTeams;
            event.matchTime  = matchTime;
            event.relativeTime = eventsList[x].relativeTime;
            console.log(JSON.stringify(event) + '\n');

                if (err) throw err;
                db.collection("events").insertOne(event, function (err, res) {
                    if (err) throw err;
                    console.log("1 event inserted");
            });
            if(x === eventsList.length - 1){
                res.send({matchId:matchId,length:eventsList.length});
            }
        }
    });
});


module.exports = router;

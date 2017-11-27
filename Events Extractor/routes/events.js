var express = require('express');
var router = express.Router();
var cors = require('cors');
var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017/eventsDb";
MongoClient.connect(url, function(err, db) {

});

router.use(cors({origin: 'http://www.uefa.com'}));
router.get("/",cors(), function (req, res) {
        res.send('hellow');
});
router.post("/sendData",cors(), function (req, res) {
        if (err) throw err;
        console.log('kirekhar');
        console.log(req.body['eventsList']);
        var eventsList = req.body.eventsList;
        for (x in eventsList) {
            var event = {};
            var comment = eventsList[x].eventComment;
            var splitedComment = comment.split(')');

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
            event.relativeTime = eventsList[x].relativeTime;
            console.log(JSON.stringify(event) + '\n');
            MongoClient.connect(url, function (err, db) {
                if (err) throw err;
                db.collection("customers").insertOne(event, function (err, res) {
                    if (err) throw err;
                    console.log("1 document inserted");
                    db.close();
                });
            });
        }
        res.send(true);
});


router.get("/test",function (req, res) {
    con.connect(function (err) {
        if(err) throw err;
        con.query("SELECT * FROM englandWalesEvents WHERE relativeTime = '60'", function (err, result, fields) {
            if (err) throw err;
            console.log(result);
        });
    });
});
module.exports = router;

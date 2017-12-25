var express = require('express');
var router = express.Router();
var cors = require('cors');
var randomstring = require("randomstring");
var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017/twitsDb";
/* GET home page. */

router.get("/",cors(), function (req, res) {
    res.render("plot.html");
});
router.post("/",cors(), function (req, res) {
    MongoClient.connect(url, function (err, db) {
        var matchId = req.body["matchId"];
        console.log(matchId);
        db.collection("plots").findOne({"matchId":Number.parseInt(matchId)},{"matchId":1,"matchTeams": 1, "negs": 1, "poses": 1, "classedTweets": 1, "events": 1},function(err,result){
            if(err) throw err;
            if(result){
                console.log(result["matchTeams"]);
                res.send(result);
            }
            else {
                res.send(false);
            }
        });
    });
});

module.exports = router;

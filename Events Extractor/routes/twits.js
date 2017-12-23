var express = require('express');
var router = express.Router();
var cors = require('cors');
var randomstring = require("randomstring");
var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017/twitsDb";
/* GET home page. */
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

});

module.exports = router;

var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var http = require('http');
var index = require('./routes/index');
var events = require('./routes/events');
var requestIp = require('request-ip');
let mysql = require('mysql');
let cors = require('cors');

let con = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "admin",
    database:'tda_db'
});

let app = express();
// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');
app.engine('html', function(str, options) {
    return function(locals) {
        return str;
    };
});
// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'));
app.use(requestIp.mw());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.use("/", express.static(__dirname + '/client'));
app.use('/', index);
app.use('/events', events);

// catch 404 and forward to error handler
app.use(function (req, res, next) {

});
// con.connect(function(err) {
//     if (err) throw err;
//     console.log("Connected!");
//     con.query("CREATE DATABASE TDA", function (err, result) {
//         if (err) throw err;
//         console.log("Database created");
//     });
// });

// con.connect(function(err) {
//     if(err) throw err;
//     console.log("Connected!"); // teams name table
//     var sql = "CREATE TABLE englandWalesEvents (eventName VARCHAR(255),eventKey VARCHAR(255),subject VARCHAR(255) ,object VARCHAR(255),relativeTime VARCHAR(255))";
//     con.query(sql, function (err, result) {
//         if (err) throw err;
//         console.log("Table created");
//     });
// });

//
// con.connect(function(err) {
//     if (err) throw err;
//     var sql = "DROP TABLE englandWalesEvents";
//     con.query(sql, function (err, result) {
//         if (err) throw err;
//         console.log("Table deleted");
//     });
// });
module.exports = app;


'use strict'

var express = require('express');
var nodeJSServer = express();


nodeJSServer.use(function (req, res, next) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    res.setHeader('Access-Control-Allow-Credentials', true);
    next();
});

nodeJSServer.get('/login/', function (req, res) {
    var MongoClient = require('mongodb').MongoClient;
    var url = "mongodb://localhost:27017/database";

    console.log(req);
    var name = req.query.name;
    var pswd = req.query.password
    MongoClient.connect(url,(err,database) =>{ 
        const userDb = database.db('database')
        userDb.collection('users').find({"user.nickname": name, "user.password":pswd}).toArray(function(err, result) {
            if (err) throw err;
            console.log(result);
            res.send(result);
            console.log("User found");
        });
    });
});

nodeJSServer.get('/updateLastPaper/', function (req, res) {
    var MongoClient = require('mongodb').MongoClient;
    var url = "mongodb://localhost:27017/database";
    console.log(req);
    var user = req.query.user;
    var paper = req.query.paper;
    MongoClient.connect(url,(err,database) =>{ 
        const userDb = database.db('database')
        var myquery = { "user.nickname": user };
        userDb.collection("users").updateOne(myquery, { $set: {"user.lastpaper" : paper}}, function(err, res) {
            if (err) throw err;
            console.log("1 document updated");
        });     
    });
});

nodeJSServer.get('/getFirstRecomendation/', function (req, res) {
    var MongoClient = require('mongodb').MongoClient;
    var url = "mongodb://localhost:27017/database";
    console.log(req);
    var user = req.query.user;
    var lastPaper = -1;
    MongoClient.connect(url,(err,database) =>{ 
        const userDb = database.db('database')
        console.log("Finding last paper from "+user);
        userDb.collection('users').find({"user.nickname": user}).toArray(function(err, result) {
            if (err) throw err;
            console.log(result);
            user = result[0];
            lastPaper = user.user["lastpaper"];//.user.lastPaper;
            console.log("Last paper");
            console.log(lastPaper);
            if (lastPaper > 0){
                var url = 'http://127.0.0.1:5000/similarity?doc_id='+lastPaper;
                const options = {  
                url: url,
                method: 'GET',
                    headers: {
                        'Accept': 'application/json',
                        'Accept-Charset': 'utf-8',
                        'access-control-allow-origin': '*',
                        'User-Agent': 'my-reddit-client'
                    }
                }

                const request = require("request");         
                request.get(options, (error, response, body) => {
                let json = JSON.parse(body);
                console.log(req);
                var papers = json;//.slice(1,4);
                var i = 0;
                var ids = []
                for (i = 1; i < papers.length; ++i){
                    ids.push(papers[i].id);
                }
                userDb.collection('papers').find({"paper.id": { $in : ids }}).toArray(function(err, result) {
                    if (err) throw err;
                    console.log(result);
                    res.send(result);
                });
                });
            }       
        });
    });
});

nodeJSServer.get('/', function (req, res) {
    var url = 'http://127.0.0.1:5000/similarity?doc_id='+req.query.doc;
    const options = {  
    url: url,
    method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Accept-Charset': 'utf-8',
            'access-control-allow-origin': '*',
            'User-Agent': 'my-reddit-client'
        }
    }

    const request = require("request");

    
    request.get(options, (error, response, body) => {
    let json = JSON.parse(body);
    console.log(req);
    console.log('Gensim on '+req.query.doc);
    res.send(json);
    });
});

nodeJSServer.listen(3000, function () {
  console.log('ScyFlix server running on port 3000!');
});


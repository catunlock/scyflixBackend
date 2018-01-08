
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

nodeJSServer.get('/query/', function (req, res) {
    var MongoClient = require('mongodb').MongoClient;
    var url = "mongodb://localhost:27017/database";
    console.log(req);
    var text = req.query.text;
    var autor = req.query.autor;
    var from = req.query.from;
    var to = req.query.to;
    if (autor != undefined || text != undefined || from != undefined || to != undefined) {   
        var url = 'http://127.0.0.1:5000/search?query='+text;
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
            console.log(json.length + ' papers found');
            console.log("Performing query:");
            console.log("Autor = "+autor);
            console.log("Text = "+text);
            console.log("From = "+from);
            console.log("To = "+to);   
            var index = 0;
            var ret = [];
            //FILTRADO POR AUTOR
            if (autor != undefined){
                autor = autor.toUpperCase();
                for (index = 0; index < json.length; ++index){
                    if (json[index].author.toUpperCase().includes(autor)){
                        ret.push(json[index]);
                        console.log(json[index].author);
                    }
                }
                json = ret;
            }
            //FILTRADO POR FECHA
            //2018-01-08
            var filtroFecha = false;
            if (from != undefined){
            	from = new Date(from);
            	filtroFecha = true;
            }else from = new Date('1900-01-01'); //Rango ridiculamente amplio

            if (to != undefined){
            	to = new Date(to);
            	filtroFecha = true;
            }else to = new Date('2900-01-01'); //Rango ridiculamente amplio

            if (filtroFecha){
            	console.log('Search papers from '+from+' to '+to);
            	var ret = [];
                for (index = 0; index < json.length; ++index){
                    if (new Date(json[index].published) >= from && new Date(json[index].published) <= to){
                        ret.push(json[index]);
                    }
                }
                json = ret;
            }
            console.log(json.length + ' papers returned');
            res.send(json);
        });
    }
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
                    console.log("IDS "+papers[i].id);
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

nodeJSServer.get('/getThreeSimilar/', function (req, res) {
    var MongoClient = require('mongodb').MongoClient;
    var url = "mongodb://localhost:27017/database";
    console.log(req);
    var lastPaper = req.query.paper;
    MongoClient.connect(url,(err,database) =>{ 
        const userDb = database.db('database')
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
            console.log("IDS "+papers[i].id);
        }
        userDb.collection('papers').find({"paper.id": { $in : ids }}).toArray(function(err, result) {
            if (err) throw err;
            console.log(result);
            res.send(result);
        });
        });       
    });
});

nodeJSServer.get('/getSimilarFromPdf/', function (req, res) {
    var MongoClient = require('mongodb').MongoClient;
    var url = "mongodb://localhost:27017/database";
    console.log(req);
    var path = req.query.file;
    MongoClient.connect(url,(err,database) =>{ 
        const userDb = database.db('database')
        var url = 'http://127.0.0.1:5000/getSimilarFromPdf?file='+path;
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
            console.log("IDS "+papers[i].id);
        }
        userDb.collection('papers').find({"paper.id": { $in : ids }}).toArray(function(err, result) {
            if (err) throw err;
            console.log(result);
            res.send(result);
        });
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


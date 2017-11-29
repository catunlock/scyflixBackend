
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

nodeJSServer.get('/', function (req, res) {
    //res.send('Hello World!');

    
    const options = {  
    url: 'http://127.0.0.1:5000/similarity',
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
    res.send(json);
    });
});

nodeJSServer.listen(3000, function () {
  console.log('Example app listening on port 3000!');
});


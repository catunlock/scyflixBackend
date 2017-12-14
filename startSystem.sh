#!/bin/bash
mongod &
nodejs ./webServer/nodeJSServer.js &
cd doc2vec
python3 scyflix_rest.py

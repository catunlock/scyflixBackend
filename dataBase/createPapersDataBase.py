#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient
from datetime import datetime

client = MongoClient()
db = client.database
#creamos la colección con un paper ficticio 

result = db.papers.insert_one(
    {
    	#formato para guardar papers en base de datos
        "paper": {
            "id": "10",
            "title": "Como sumar 2 + 1",
            "pdf": "/anyRoute/123456.pdf",
            "image": "/anyRoute/123456.jpg",
            "date":datetime.today()
        }
    })
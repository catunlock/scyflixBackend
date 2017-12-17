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
            "id": "501",
            "title": "Como sumar 2 + 1",
            "pdf": "/home/segmentation-fault/uni/PAE/scyflixBackend/webPage/pdfs/1711.10566.pdf",
            "image": "/home/segmentation-fault/uni/PAE/scyflixBackend/webPage/images/1711.10566.jpg",
            "date":datetime.today()
        }
    })

result = db.papers.insert_one(
    {
    	#formato para guardar papers en base de datos
        "paper": {
            "id": "406",
            "title": "Que pasa pajaro",
            "pdf": "/home/segmentation-fault/uni/PAE/scyflixBackend/webPage/pdfs/1711.10574.pdf",
            "image": "/home/segmentation-fault/uni/PAE/scyflixBackend/webPage/images/1711.10574.jpg",
            "date":datetime.today()
        }
    })

result = db.papers.insert_one(
    {
    	#formato para guardar papers en base de datos
        "paper": {
            "id": "588",
            "title": "Hola amigos",
            "pdf": "/home/segmentation-fault/uni/PAE/scyflixBackend/webPage/pdfs/1711.10768.pdf",
            "image": "/home/segmentation-fault/uni/PAE/scyflixBackend/webPage/images/1711.10768.jpg",
            "date":datetime.today()
        }
    })
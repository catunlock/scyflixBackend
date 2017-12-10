#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient
client = MongoClient()
db = client.database

#creamos la colección con un usuario master

result = db.users.insert_one(
    {
        "user": {
            "nickname": "Admin",
            "password": "123456",
            "lastpaper": "10",
        }
    })
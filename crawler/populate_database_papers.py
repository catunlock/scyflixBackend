#!/usr/bin/env python3
from pathlib import Path
import xml.etree.ElementTree as ET
import os

from pymongo import MongoClient
from datetime import datetime

# Find by categori:
# db.getCollection('papers').find({categories: {$eq: {name:'cs.CR'}}})

# Finb by summary:
# db.getCollection('papers').find({'summary': {$regex: ".*has.*"}})

# Create index
# db.papers.createIndex({"title":"text", "summary":"text", "content":"text"})



# Search
# db.papers.find({$text: {$search: "Fractional Moments"}}, {score: {$meta: "textScore"}}).sort({score:{$meta:"textScore"}})

INDEX_PATH = "./index/"
PAPERS_PATH = "./papers/"

PAPERS_STORAGE = "/home/sunlock/txt_papers/"

LABELS = set(["cs.AI", "cs.CR", "cs.CV", "cs.DB", "cs.LG"])



def populate_index_file(path_file):
    print("Populating:", str(path_file))
    tree = ET.parse(str(path_file))
    root = tree.getroot()

    file_name = PAPERS_PATH + str(path_file.parents[0]) + "/"
    if not os.path.exists(file_name):
        os.makedirs(file_name)

    entries = []



    for entry in root.iter('{http://www.w3.org/2005/Atom}entry'):

        properties = dict()
        properties['categories'] = []
        skip = False

        for c in entry:

            if c.tag == '{http://www.w3.org/2005/Atom}id':
                id = c.text.split('/')[-1]
                properties['id'] = id

                try:
                    with open(PAPERS_STORAGE + id + ".txt") as paper_file:
                        content = paper_file.read()
                        properties['content'] = content
                except FileNotFoundError:
                    print("File not found:" + PAPERS_STORAGE + id + ".txt")
                    file_pendings.write(id+'\n')
                    skip = True

            
            if c.tag == '{http://www.w3.org/2005/Atom}link':
                if 'type' in c.attrib and c.attrib['type'] == 'application/pdf':
                    properties['link_pdf'] = c.attrib['href']

            if c.tag == '{http://www.w3.org/2005/Atom}category':
                label = c.attrib['term'].strip('\n')

                if label in LABELS:
                    properties['categories'].append({'name': label})

            if c.tag == '{http://www.w3.org/2005/Atom}updated':
                properties['updated'] = c.text

            if c.tag == '{http://www.w3.org/2005/Atom}published':
                properties['published'] = c.text

            if c.tag == '{http://www.w3.org/2005/Atom}title':
                properties['title'] = c.text

            if c.tag == '{http://www.w3.org/2005/Atom}summary':
                properties['summary'] = c.text

            if c.tag == '{http://www.w3.org/2005/Atom}author':
                properties['author'] = c[0].text

            if c.tag == '{http://arxiv.org/schemas/atom}comment':
                properties['comment'] = c.text

        if not skip:
            entries.append(properties)


    print(entries)

    client = MongoClient()
    db = client.database

    db.papers.insert(entries)
    print("Get of bd:", db.papers.find_one())

    print("Creating index.")
    result = db.papers.create_index([('title', 'text'), ('summary', 'text'), ('content', 'text')])
    print("Result:", result)

def travel_index(path_file):
    print("Entering directory:" + str(path_file))
    if path_file.is_dir():
        for p in path_file.iterdir():
            if p.is_dir():
                travel_index(p)
            else:
                populate_index_file(p)
    else:
        populate_index_file(path_file)

def main():
    global file_pendings
    file_pendings = open('notyetdownloaded.txt', 'w')
    travel_index(Path(INDEX_PATH))
    file_pendings.close()

if __name__ == "__main__":
    main()
from flask import Flask, request
import json
from gensim.models import Doc2Vec

# some_file.py
import sys

from gensim_similarity import GensimSimilarity, GensimCorpus
from kmeans_doc2vec import extract_clusters
from pymongo import MongoClient

app = Flask(__name__)

train_file = 'cs.AI.txt'
model_file = 'cs.AI.model'


@app.route('/')
def hello_world():
    user = request.args.get('user', 10)
    jn = {"Alberto" : 10, "Marc" : user}

    return app.response_class(
        response=json.dumps(jn, separators=(',', " : "), indent=4),
        status=200,
        mimetype='application/json')


@app.route('/similarity')
def similarity():
    doc_id = request.args.get('doc_id', '')
    cosa = gs.generate_json_similars(doc_id)
    print(cosa)
    return app.response_class(
        response=json.dumps(cosa, separators=(',', " : "), indent=4),
        status=200,
        mimetype='application/json')

@app.route('/similarity_text')
def similarity_text():
    str_text = str(request.args.get('text', ""))
    cosa = gs.generate_json_similars_from_text(str_text)
    print(cosa)
    return app.response_class(
        response=json.dumps(cosa, separators=(',', " : "), indent=4),
        status=200,
        mimetype='application/json')

@app.route('/kmeans')
def kmeans():
    num_clusters = int(request.args.get('num_clusters', 20))
    max_keywords = int(request.args.get('max_keywords', 20))

    cosa = extract_clusters(num_clusters, max_keywords)
    return app.response_class(
        response=json.dumps(cosa, separators=(',', " : "), indent=4),
        status=200,
        mimetype='application/json')

@app.route('/search')
def search():
    query = request.args.get('query', '')
    print("Query:", query)
    result = db.papers.find({'$text': {'$search': query}}, {'score': {'$meta': 'textScore'}}).sort([('score', {'$meta':'textScore'})])
    lista = []
    for r in result:
        print("result:", r)
        r['_id'] = str(r['_id'])
        lista.append(r)

    print(lista[0])

    return app.response_class(
        response=json.dumps(lista, separators=(',', " : "), indent=4),
        status=200,
        mimetype='application/json')


if __name__ == '__main__':
    global gs
    corpus_train = GensimCorpus()
    corpus_train.read_corpus_from_file(train_file)

    model = Doc2Vec.load(model_file)

    gs = GensimSimilarity(model, corpus_train)

    client = MongoClient()
    db = client.database

    app.run()

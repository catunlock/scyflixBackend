import nltk, math, codecs
from gensim.models import Doc2Vec
from gensim.models import tfidfmodel
from gensim.corpora.dictionary import Dictionary
import gensim.corpora.dictionary
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords
from nltk.cluster.kmeans import KMeansClusterer
import re
from nltk.corpus import stopwords
import collections
from tutorial_gensim import read_corpus
from pymongo import MongoClient

# Set file names for train and test data

category_list = ['cs.AI', 'cs.CR', 'cs.CV', 'cs.DB', 'cs.LG']
path_papers = "/home/xaloc/computer_science_magpie_full/"

def do_kmeans(vectors, NUM_CLUSTERS = 40):

    print("Clustering documents with k-means for", NUM_CLUSTERS, "clusters.")

    kclusterer = KMeansClusterer(NUM_CLUSTERS,avoid_empty_clusters=True, distance=nltk.cluster.util.cosine_distance, repeats=25)
    assigned_clusters = kclusterer.cluster(vectors, assign_clusters=True)


    print("Clasifiying documents")

    # Clasificando los documentas en cada cluster
    clusters = dict()
    for i in range(len(assigned_clusters)):
        if assigned_clusters[i] not in clusters:
            clusters[assigned_clusters[i]] = []

        clusters[assigned_clusters[i]].append((i, train_corpus[i], vectors[i]))

    return clusters


def preprocess(list_words):
    words = []
    for word in list_words:
        if re.match("^[A-Za-z]*$", word) and len(word) > 2:
            words.append(word)

    return words

def remove_stopwords(stopwords, list_words):
    words = []
    for word in list_words:
        word = word.lower()
        if word not in stopwords:
            words.append(word)

    return words


def filter_doc(d):
    words = d.split()

    words = preprocess(words)

    stops = set(stopwords.words("english"))
    words = remove_stopwords(stops, words)

    return words


def tf_idf(cluster, max_keywords=20):
    cluster_corpus = []

    for id_doc, tagged_document, weights in cluster:
        with open(path_papers + index_corpus[id_doc], 'r') as doc_file:
            cluster_corpus.append(doc_file.read())  #gensim.utils.simple_preprocess

    texts = []
    for d in cluster_corpus:
        texts.append(filter_doc(d))

    # remove words that appear only once
    from collections import defaultdict

    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    texts = [[token for token in text if frequency[token] > 1] for text in texts]

    cdic = Dictionary(texts)

    corpus = [cdic.doc2bow(text) for text in texts]

    tfidf = tfidfmodel.TfidfModel(corpus)


    result_words = []
    for i in range(len(corpus)):
        for w, v in tfidf[corpus[i]]:
            result_words.append((v, cdic[w]))

    result_words.sort()
    result_words = result_words[-40:]

    return result_words


def prepare_to_json(clusters, db, max_keywords):
    result = dict()

    print("Doing tf_idf of the common words of the clusters.")
    for id_cluster, c in clusters.items():
        id_cluster = str(id_cluster)
        result[id_cluster] = {}
        result[id_cluster]['keywords'] = tf_idf(c, max_keywords)
        result[id_cluster]['documents'] = []
        for (id_doc, _, _) in c:
            arxiv_id = index_corpus[id_doc][:-4]
            paper = {}
            paper['id'] = arxiv_id
            paper['title'] = ''
            paper['published'] = ''

            try:
                paper_db = db.papers.find_one({'id': arxiv_id})
                print("Paper encontrado")
                paper['title'] = paper_db['title']
                paper['published'] = paper_db['published']
            except TypeError:
                print("No encontrado")


            result[id_cluster]['documents'].append(paper)

    return result


def extract_clusters(category, db, NUM_CLUSTERS = 40, max_keywords=20):
    print("File for training:", category + '.txt')
    model = Doc2Vec.load(category + '.model')

    print("Loading documents.")

    # list of documents prepareds for train and test.
    global index_corpus, train_corpus
    index_corpus, train_corpus = read_corpus(category + '.txt')


    print("Inferring vectors of documents.")

    vectors = list()
    for doc in train_corpus:
        vectors.append(model.infer_vector(doc.words))


    clusters = do_kmeans(vectors, NUM_CLUSTERS)

    return prepare_to_json(clusters, db, max_keywords)


def update_papers_db(db, clusters):
    for id_cluster, cluster in clusters.items():
        try:
            for doc_id in cluster['documents']:
                print("Cluster", id_cluster, "doc_id", doc_id)

                paper = db.papers.find_one({'id':doc_id})

                paper['cluster_id'] = id_cluster
                paper['cluster_words'] = cluster['keywords']
                print("Paper:", paper)

                db.papers.replace_one({'id':doc_id}, paper)

        except TypeError:
            print(cluster)

if __name__ == "__main__":

    client = MongoClient()
    db = client.database

    for c in category_list:
        print("Extracting clusters of: ", c)

        clusters = extract_clusters(c, db)
        print(clusters)



        db.clusters.delete_one({'category': c})
        db.clusters.insert({'category': c, 'clusters':clusters})

        update_papers_db(db, clusters)
        #db.papers.find(


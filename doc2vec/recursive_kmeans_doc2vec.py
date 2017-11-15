import nltk, math, codecs
from gensim.models import Doc2Vec
from nltk.cluster.kmeans import KMeansClusterer
import re
from nltk.corpus import stopwords
import collections

from tutorial_gensim import read_corpus

# Set file names for train and test data

train_file = 'cs.AI.txt'
test_file = 'cs.AI_test.txt'

def recursive_kmeans(docs, kclusterer ):

    if len(docs) == 2:
        return docs

    cluster_assignations = kclusterer.cluster(docs, assign_clusters=True)

    sub_docs1 = []
    sub_docs2 = []

    print("Cluster assignation:", cluster_assignations)

    for i in cluster_assignations:
        if i == 0:
            sub_docs1.append(docs[i])
        elif i == 1:
            sub_docs2.append(docs[i])

    print("sub_docs1", len(sub_docs1))
    print("sub_docs2", len(sub_docs2))

    t = dict()
    t['r_docs'] = recursive_kmeans(sub_docs1, kclusterer)
    t['l_docs'] = recursive_kmeans(sub_docs2, kclusterer)

    return t


def do_kmeans_recursive():

    print("File for training:", train_file)
    print("File for test:", test_file)

    #data = <sparse matrix that you would normally give to scikit>.toarray()
    fname = "cs.AI.model"
    model = Doc2Vec.load(fname)

    print("Loading documents.")

    # list of documents prepareds for train and test.
    index_corpus, train_corpus = read_corpus(train_file)
    index_test, test_corpus = read_corpus(test_file, tokens_only=True)


    print("Inferring vectors of documents.")

    vectors = list()
    for doc in train_corpus:
        vectors.append(model.infer_vector(doc.words))

    print("Clustering documents with k-means until 2 documents per cluster.")

    kclusterer = KMeansClusterer(2, avoid_empty_clusters=True, distance=nltk.cluster.util.cosine_distance, repeats=25)
    recursive_kmeans(vectors, kclusterer)


if __name__ == "__main__":
    do_kmeans_recursive()
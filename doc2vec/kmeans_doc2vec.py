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

def do_kmeans(NUM_CLUSTERS = 20):

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

    # Obtener topic con las palabras mas comunes.

    print("Obtaining names")

    results = {}
    for id_cluster, list_documents in clusters.items():
        words = []
        docs = []

        for doc in list_documents:
            docs.append(index_corpus[doc[0]])
            for word in doc[1].words:
                words.append(word)

        count = collections.Counter(words)
        print(count.most_common()[:5])

        results[id_cluster] = (count.most_common()[:5], docs)


    print("Kmeans done")
    return results

if __name__ == "__main__":
    do_kmeans()
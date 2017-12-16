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

# Set file names for train and test data

train_file = 'cs.AI.txt'
test_file = 'cs.AI_test.txt'
model_file = "cs.AI.model"
path_papers = "/home/xaloc/computer_science_magpie/"

def do_kmeans(vectors, NUM_CLUSTERS = 20):

    print("Clustering documents with k-means for", NUM_CLUSTERS, "clusters.")

    kclusterer = KMeansClusterer(NUM_CLUSTERS,avoid_empty_clusters=True, distance=nltk.cluster.util.cosine_distance, repeats=25)
    assigned_clusters = kclusterer.cluster(vectors, assign_clusters=True)


    print("Clasifiying documents")

    # Clasificando los documentas en cada cluster
    clusters = dict()
    for i in range(len(assigned_clusters)):
        if assigned_clusters[i] not in clusters:
            clusters[assigned_clusters[i]] = []

        # TODO: Cambiar el train_corpus o el vector por el texto de verdad en el mismo formato claro.
        clusters[assigned_clusters[i]].append((i, train_corpus[i], vectors[i]))

    return clusters


def common_words(clusters):
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
        print(count.most_common()[:20])

        results[id_cluster] = (count.most_common()[:40], docs)

    print("Kmeans done")
    return results

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


def tf_idf(cluster):
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

    from pprint import pprint  # pretty-printer
    pprint(texts)


    cdic = Dictionary(texts)



    corpus = [cdic.doc2bow(text) for text in texts]


    tfidf = tfidfmodel.TfidfModel(corpus)


    print("TEST TFIDF:")

    result_clusters = {}
    for i in range(len(corpus)):
        result_clusters[i] = []
        for w, v in tfidf[corpus[i]]:
            result_clusters[i].append((v, cdic[w]))

        result_clusters[i].sort()

    pprint(result_clusters)


if __name__ == "__main__":

    print("File for training:", train_file)
    print("File for test:", test_file)

    #data = <sparse matrix that you would normally give to scikit>.toarray()

    model = Doc2Vec.load(model_file)

    print("Loading documents.")

    # list of documents prepareds for train and test.
    global index_corpus, train_corpus
    index_corpus, train_corpus = read_corpus(train_file)


    print("Inferring vectors of documents.")

    vectors = list()
    for doc in train_corpus:
        vectors.append(model.infer_vector(doc.words))


    clusters = do_kmeans(vectors, NUM_CLUSTERS=20)

    print("Doing tf_idf of the common words of the clusters.")
    for id_cluster, c in clusters.items():
        tf_idf(c)

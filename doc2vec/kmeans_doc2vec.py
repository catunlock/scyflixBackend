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
path_papers = "/home/sunlock/computer_science_magpie_full/"

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


def prepare_to_json(clusters, max_keywords):
    result = dict()

    print("Doing tf_idf of the common words of the clusters.")
    for id_cluster, c in clusters.items():
        result[id_cluster] = {}
        result[id_cluster]['keywords'] = tf_idf(c, max_keywords)
        result[id_cluster]['documents'] = []
        for (id_doc, _, _) in c:
            result[id_cluster]['documents'].append(index_corpus[id_doc])

    return result

def extract_clusters(NUM_CLUSTERS = 40, max_keywords=20):
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


    clusters = do_kmeans(vectors, NUM_CLUSTERS)

    return prepare_to_json(clusters, max_keywords)

if __name__ == "__main__":
    print(extract_clusters())


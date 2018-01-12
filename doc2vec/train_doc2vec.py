import gensim
import collections
import smart_open
import random
from gensim.models.doc2vec import TaggedDocument, Doc2Vec

# Set file names for train and test data

corpus_list = ['cs.AI', 'cs.CR', 'cs.CV', 'cs.DB', 'cs.LG', 'cs.ALL']

"""
read the file line-by-line, The file is a corpus and each line is a document, pre-process each line using a simple gensim pre-processing tool, and return a list of words. 
"""

def read_corpus(fname, tokens_only=False):

    index = dict()
    with smart_open.smart_open(fname, encoding='utf-8') as f:

        corpus = enumerate(eval(f.read()))
        documents = list()

        for i, c in corpus:
            index[i] = c[0]
            doc = c[1]
            if tokens_only:
                documents.append(gensim.utils.simple_preprocess(doc))
            else:
                # For training data, add tags
                documents.append(gensim.models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(doc), [i]))

    return (index, documents)


def train_corpus(corpus_name):
    # list of documents prepareds for train and test.
    index_corpus, train_corpus = list(read_corpus(corpus_name + '.txt'))


    #iter = 1, because we keep training ourselves :)
    model = Doc2Vec(size=100, dbow_words= 1, dm=0, iter=1,  window=5, seed=1337, min_count=5, workers=4,alpha=0.025, min_alpha=0.025)

    # vocabulary is a dictionary (accessible via model.wv.vocab) of all of the unique words extracted from the training corpus along with the count
    # (e.g., model.wv.vocab['penalty'].count for counts for the word penalty
    model.build_vocab(train_corpus)


    for epoch in range(10):
        print("epoch "+str(epoch))
        model.train(train_corpus, total_examples=len(train_corpus), epochs=1)
        model.save(corpus_name + '.model')
        model.alpha -= 0.002  # decrease the learning rate
        model.min_alpha = model.alpha  # fix the learning rate, no decay

def main():
    for corpus_name in corpus_list:
        train_corpus(corpus_name)

if __name__ == "__main__":
    main()
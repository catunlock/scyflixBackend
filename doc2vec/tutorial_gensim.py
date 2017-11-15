import gensim
import collections
import smart_open
import random

# Set file names for train and test data

train_file = 'cs.AI.txt'
test_file = 'cs.AI_test.txt'

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

"""
        for i, line in enumerate(f):
            if tokens_only:
                yield gensim.utils.simple_preprocess(line)
            else:
                # For training data, add tags
                yield gensim.models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(doc), [file])
"""

if __name__ == "__main__":
    print("File for training:", train_file)
    print("File for test:", test_file)

    # list of documents prepareds for train and test.
    index_corpus, train_corpus = read_corpus(train_file)
    index_test, test_corpus = read_corpus(test_file, tokens_only=True)

    print("Train Corpus:", train_corpus[1])

    # Entrenamos un modelo con vector de 50 palabras y iterando sobre el corpus 55 veces,
    # Ponemos el minimum word count to 2 in order to give higher frequency words more weighting.
    # Model accuracy can be improved by increasing the number of iterations but this generally increases the training time. (sobretodo en modelos pequeños)
    model = gensim.models.doc2vec.Doc2Vec(size=50, min_count=2, iter=55)

    # vocabulary is a dictionary (accessible via model.wv.vocab) of all of the unique words extracted from the training corpus along with the count
    # (e.g., model.wv.vocab['penalty'].count for counts for the word penalty
    print("Building vocabulary")
    model.build_vocab(train_corpus)

    # Train the model.
    print("Training model ...", end='')
    model.train(train_corpus, total_examples=model.corpus_count, epochs=model.iter)
    print("done")

    # Assessing Model
    print("Assesing model")

    # Primero vamos a hacer ver como que los datos de entrenamiento no los ha visto nuestro modelo y ver cuantos acierta consigo mismo.

    ranks = []
    second_ranks = []
    for doc_id in range(len(train_corpus)):
        inferred_vector = model.infer_vector(train_corpus[doc_id].words)

        # print("doc_id:", doc_id)
        sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))
        rank = [docid for docid, sim in sims].index(doc_id)

        # print("sims:", sims)
        # print("rank:", rank)

        ranks.append(rank)
        second_ranks.append(sims[1])

        # print("\n\n")
    # Resultados
    print(collections.Counter(ranks))

    print('Document ({}): «{}»\n'.format(doc_id, ' '.join(train_corpus[doc_id].words)))
    print(u'SIMILAR/DISSIMILAR DOCS PER MODEL %s:\n' % model)
    for label, index in [('MOST', 0), ('MEDIAN', len(sims) // 2), ('LEAST', len(sims) - 1)]:
        print(u'%s %s: «%s»\n' % (label, sims[index], ' '.join(train_corpus[sims[index][0]].words)))

    # Testing the model
    ###################

    # Pick a random document from the test corpus and infer a vector from the model
    doc_id = random.randint(0, len(test_corpus))
    inferred_vector = model.infer_vector(test_corpus[doc_id])
    sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))

    # Compare and print the most/median/least similar documents from the train corpus
    print('Test Document ({}): «{}»\n'.format(doc_id, ' '.join(test_corpus[doc_id])))
    print(u'SIMILAR/DISSIMILAR DOCS PER MODEL %s:\n' % model)
    for label, index in [('MOST', 0), ('MEDIAN', len(sims) // 2), ('LEAST', len(sims) - 1)]:
        print(u'%s %s: «%s»\n' % (label, sims[index], ' '.join(train_corpus[sims[index][0]].words)))


import os
import gensim
import collections
import smart_open
import random
import textract
from gensim.models import Doc2Vec
from util_make_corpus_from_clasified import process_doc


# Set file names for train and test data

train_file = 'cs.AI.txt'
test_file = 'cs.AI_test.txt'
model_file = 'cs.AI.model'

papers_path = '/home/xaloc/computer_science_magpie/'
"""
read the file line-by-line, The file is a corpus and each line is a document, pre-process each line using a simple gensim pre-processing tool, and return a list of words. 
"""


class GensimSimilarity:
    def __init__(self, model, corpus):
        self.model = model
        self.corpus = corpus


    def getSimilarity(self, doc_id):
        test_corpus = self.corpus.getTaggedDocuments()
        inferred_vector = self.model.infer_vector(test_corpus[doc_id].words)
        return self.model.docvecs.most_similar([inferred_vector], topn=len(self.model.docvecs))


    def getSimilarityText(self, str_text):
        print("Searching similar papers to: ", str_text)
        inferred_vector = self.model.infer_vector(str_text)
        return self.model.docvecs.most_similar([inferred_vector], topn=len(self.model.docvecs))

    def getSimilarityFromFile(self, file_path):
        file_path = file_path.strip('"')
        print("Get similarity from file:", file_path)
        if os.path.isfile(file_path):

            text = textract.process(file_path).decode('utf-8')
            return self.generate_json_similars_from_text(text)
        else:
            return {'Error': 'File not found'}

    def asses_model(self):
        ranks = []

        train_corpus = self.corpus.getTaggedDocuments()

        for doc_id in range(len(train_corpus)):
            inferred_vector = self.model.infer_vector(train_corpus[doc_id].words)

            sims = self.model.docvecs.most_similar([inferred_vector], topn=len(self.model.docvecs))
            rank = [docid for docid, sim in sims].index(doc_id)

            ranks.append(rank)

        return collections.Counter(ranks)


    def size(self):
        return self.corpus.size()

    def getDocument(self, id):
        return self.corpus.getTaggedDocuments()[id]

    def accessIndex(self, id):
        return self.corpus.accessIndex(id)

    def generate_json_similars(self, doc_id):
        # {"patata" : [tal, cual, ...]}
        result = []
        id_paper = self.corpus.accessIndex(doc_id)
        print("ID_PAPER:", id_paper)
        sims = self.getSimilarity(id_paper)[0:20]
        for id, prob in sims:
            entry = {}
            entry["id"] = str(id)
            entry["arxiv"] = str(self.accessIndex(id))
            entry["file_path"] = papers_path + str(self.accessIndex(id))[:-4] + '.pdf'
            entry["document"] = self.getDocument((id))
            (a,b) = self.getDocument((id))
            #para mostrar los datos me va mejor no tener un TaggedDocument y que me vengan como lista de strings
            entry["document"] = str(a)
            entry["prob"] = str(prob)
            result.append(entry)

        return result

    def generate_json_similars_from_text(self, str_text):
        result = []
        sims = self.getSimilarityText(str_text)[0:20]
        for id, prob in sims:
            entry = {}
            entry["id"] = str(id)
            entry["arxiv"] = str(self.accessIndex(id))
            entry["file_path"] = papers_path + str(self.accessIndex(id))[:-4] + '.pdf'
            entry["document"] = self.getDocument((id))
            (a, b) = self.getDocument((id))
            # para mostrar los datos me va mejor no tener un TaggedDocument y que me vengan como lista de strings
            entry["document"] = str(a)
            entry["prob"] = str(prob)
            result.append(entry)

        return result

class GensimCorpus:
    def __init__(self):
        self.index = dict()
        self.documents = list()

    def read_corpus_from_file(self, fname, tokens_only=False):
        self.index = dict()
        with smart_open.smart_open(fname, encoding='utf-8') as f:

            corpus = enumerate(eval(f.read()))
            self.documents = list()

            for i, c in corpus:
                self.index[i] = c[0][:-4]
                self.index[c[0][:-4]] = i
                doc = c[1]
                self.documents.append(gensim.models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(doc), [i]))


    def getTaggedDocuments(self):
        return self.documents


    def size(self):
        return len(self.documents)

    def accessIndex(self, id):
        return self.index[id]



if __name__ == "__main__":
    print("File for training:", train_file)
    print("File for test:", test_file)

    corpus_train = GensimCorpus()
    corpus_train.read_corpus_from_file(train_file)

    model = Doc2Vec.load(model_file)

    gs = GensimSimilarity(model, corpus_train)

    #Assesment the quality of the model
    #print(gs.asses_model())

    # Pick a random document from the test corpus and infer a vector from the model
    doc_id = random.randint(0, gs.size())

    print("Test:", corpus_train.accessIndex("0504058v1"))

    sims = gs.getSimilarity(doc_id)

    # Compare and print the most/median/least similar documents from the train corpus
    print('Test Document ({}): «{}»\n'.format(doc_id, ' '.join(gs.getDocument(doc_id).words)))
    print(u'SIMILAR/DISSIMILAR DOCS PER MODEL %s:\n' % model)
    for index in range(20):
        print(u'%s %s: «%s»\n' % (sims[index], gs.accessIndex(sims[index][0]), ' '.join(gs.getDocument(sims[index][0]).words)))


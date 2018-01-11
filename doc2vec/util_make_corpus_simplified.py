import os
from shutil import copyfile
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import concurrent.futures

f_input = '/home/sunlock/classifier/papers_clasified/'
f_labels = 'computer_science_labels'
f_output = 'corpus'

corpus_list = ['cs.AI', 'cs.CR', 'cs.CV', 'cs.DB', 'cs.LG']

def preprocess(list_words):
    for word in list_words:
        if re.match("^[A-Za-z]*$", word) and len(word) > 2:
            yield word

def stemm(stemmer, list_words):
    for word in list_words:
        yield stemmer.stem(word)

def lemmatize(lemmatizer, list_words):
    for word in list_words:
        yield lemmatizer.lemmatize(word)

def remove_stopwords(stopwords, list_words):
    for word in list_words:
        word = word.lower()
        if word not in stopwords:
            yield word

def process_doc(doc):
    list_words = doc.split(" ")
    #list_words = preprocess(list_words)

    #stops = set(stopwords.words("english"))
    #list_words = remove_stopwords(stops, list_words)

    #stemmer = PorterStemmer()
    #list_words = stemm(stemmer, list_words)

    #lemmatizer = WordNetLemmatizer()
    #list_words = lemmatize(lemmatizer, list_words)

    return " ".join(list_words).replace('\n', ' ')


def make_corpus(corpus_name):
    corpus = []
    for file in os.listdir(f_input + corpus_name):
        print("Procesing file:", file)
        with open(f_input + corpus_name + '/' + file, 'r', encoding='utf-8') as f_doc:
            doc = process_doc(f_doc.read())
            corpus.append((file, doc))

    print("Elementos en el corpus:", len(corpus))
    if not os.path.exists(f_output):
        os.makedirs(f_output)

    with open(corpus_name + '.txt', 'w', encoding='utf-8') as f_corpus:
        print("Writing corpus of", corpus_name)
        f_corpus.write('[')
        for (f, paper) in corpus:
            f_corpus.write('("' + f + '", "' + paper + '"),')
            f_corpus.write('\n')
        f_corpus.write(']')

def main():

    nltk.download('stopwords')
    nltk.download('wordnet') 

    for corpus_name in corpus_list:
        make_corpus(corpus_name)

if __name__ == "__main__":
    main()



import os
from shutil import copyfile
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import concurrent.futures

f_input = 'computer_science_classified'
f_labels = 'computer_science_labels'
f_output = 'corpus'


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
    
def main():

    nltk.download('stopwords')
    nltk.download('wordnet') 
   
    corpus = dict()
    category = 'cs.AI'

    for file in os.listdir(f_input + '/' + category):
        print("Procesing file:", file)
        file_lab = f_labels + '/' + file[:-4] + '.lab'
        if os.path.isfile(file_lab):
            with open(file_lab, 'r') as f_lab:
                labels = f_lab.readlines()
                for l in labels:
                    l = l.strip('\n')
                    if not l in corpus:
                        corpus[l] = []

                    with open(f_input + '/' + category + '/' + file, 'r', encoding='utf-8') as f_doc:
                        doc = process_doc(f_doc.read())
                        corpus[l].append((file,doc))
   
    print("Elementos en el corpus:", len(corpus))
    if not os.path.exists(f_output):
        os.makedirs(f_output)

    for key, value in corpus.items():
        with open(f_output + '/' + key + '.txt', 'w', encoding='utf-8') as f_corpus:
            f_corpus.write('[')
            for (f ,paper) in value:
                f_corpus.write('("' +  f + '", "' + paper + '"),')
                f_corpus.write('\n')
            f_corpus.write(']')

if __name__ == "__main__":
    main()



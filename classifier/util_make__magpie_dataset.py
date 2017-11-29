import os
from shutil import copyfile
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
import concurrent.futures
from multiprocessing import Manager,Pool,Lock

f_input = 'mini_computer_science_magpie'
f_output = 'processed_' + f_input

def preprocess(list_words):
    for word in list_words:
        if re.match("^[A-Za-z]*$", word) and len(word) > 3:
            yield word

def stemm(stemmer, list_words):
    for word in list_words:
        yield stemmer.stem(word)

def remove_stopwords(stopwords, list_words):
    for word in list_words:
        word = word.lower()
        if word not in stopwords:
            yield word

def process_doc(doc):
    list_words = doc.split(" ")
    list_words = preprocess(list_words)

    #list_words = remove_stopwords(stops, list_words)

    #stemmer = LancasterStemmer()
    #list_words = stemm(stemmer, list_words)

    doc = doc.replace('\n', ' ')
    return " ".join(list_words)
    
def process_file(file):
    print("Procesing file:", file)
    file_lab = f_input + '/' + file[:-4] + '.lab'

    copyfile(file_lab, f_output + '/' + file[:-4] + '.lab')

    with open(f_input + '/' + file, 'r', encoding='utf-8') as f_doc:
        doc = process_doc(f_doc.read())
        with open(f_output + '/' + file, 'w', encoding='utf-8') as f_dest:
            f_dest.write(doc)

def main():
    global stops

    nltk.download('stopwords')
    stops = set(stopwords.words("english"))

    if not os.path.exists(f_output):
        os.makedirs(f_output)

    for file in os.listdir(f_input):
        process_file(file)


if __name__ == "__main__":
    main()


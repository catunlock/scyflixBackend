import textract
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
import re
from joblib import Parallel, delayed
import multiprocessing

stopwords = set(stopwords.words("english"))
stemmer = LancasterStemmer()

path_pdf = 'papers/index/Computer Science/'
path_output = path_pdf

def remove_stopwords(list_words):
    processed_word_list = []
    for word in list_words:
        word = word.lower()
        if word not in stopwords:
            processed_word_list.append(word)
    
    return processed_word_list

def stemm(list_words):
    stemmed_words = []

    for word in list_words:
        stemmed_word = stemmer.stem(word)
        print(stemmed_word)
        stemmed_words.append(stemmed_word)

    return stemmed_words

def preprocess(list_words):
    processed_word_list = []
    for word in list_words:
        if re.match("^[A-Za-z]*$", word):
            processed_word_list.append(word)
    
    return processed_word_list

def processInput(f):
    if f.split('.')[-1] == 'pdf':
        print ("Processing", f)
        try:

            extracted = textract.process(path_pdf+f)
            if extracted != None:
                list_words = extracted.decode("utf8").split(" ")
                #print(list_words)

                #list_words = preprocess(list_words)

                #list_words = remove_stopwords(list_words)
                #print(list_words)
                #list_words = stemm(list_words)
                #print(list_words)

                output_file = open(path_output+f[:-4]+".txt", 'w')
                output_file.write(" ".join(list_words))
                output_file.close()
                print("Success.")
            else:
                print("Failed por None!")
        except TypeError:
            print("TypeError!")
        except textract.exceptions.ShellError:
            print("Failed!")

def main():
    nltk.download('stopwords')

    num_cores = multiprocessing.cpu_count()
    results = Parallel(n_jobs=num_cores)(delayed(processInput)(f) for f in os.listdir(path_pdf))

        
    
if __name__ == "__main__":
    main()
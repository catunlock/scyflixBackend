from magpie import Magpie
import sys, glob, os

def main():
    magpie = Magpie(
        keras_model='./model.h5',word2vec_model='./embeddings',scaler='./scaler')
    magpie.labels = ['computer vision', 'cryptography', 'machine learning']
    os.chdir("./test")
    for file in glob.glob("*.txt"):
        print(file)
        results  = magpie.predict_from_file(file)
        print(results)

if __name__ == "__main__":
    main()

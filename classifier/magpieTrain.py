import os
from magpie import Magpie

data = 'papers_magpie/'

def load_labels():
    labels = []
    with open('categories.txt', 'r') as label_files:
        lines = label_files.readlines()
        for l in lines:
            labels.append(l)

    return labels

def train_magpie(model):
    print
    "Training vectors..."
    model.init_word_vectors(data, vec_dim=100)

    labels = load_labels()
    print
    labels

    print
    "Training labels..."
    model.train(data, labels, test_ratio=0.2, nb_epochs=30)

    print
    "Saving..."
    model.save_word2vec_model('./embeddings', overwrite=True)
    model.save_scaler('./scaler', overwrite=True)
    model.save_model('./model.h5', overwrite=True)


try:
    magpie = Magpie(keras_model='model.h5', word2vec_model='embeddings', scaler='scaler')
    train_magpie(magpie)
except Exception:
    print("Unable to load the model, training again.")
    magpie = Magpie()
    train_magpie(magpie)


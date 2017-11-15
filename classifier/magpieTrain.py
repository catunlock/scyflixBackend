import os
from magpie import MagpieModel

data = 'computer_science_magpie/'

def load_labels():
    labels = []
    with open('categories.txt', 'r') as label_files:
        lines = label_files.readlines()
        for l in lines:
            labels.append(l)

    return labels

magpie = MagpieModel()

print "Training vectors..."
magpie.init_word_vectors(data, vec_dim=100)


labels = load_labels()
print labels

print "Training labels..."
magpie.train(data, labels, test_ratio=0.2, nb_epochs=30)

print "Saving..."
magpie.save_word2vec_model('./embeddings' , overwrite=True)
magpie.save_scaler('./scaler', overwrite=True)
magpie.save_model('./model.h5')


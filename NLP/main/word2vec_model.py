from gensim.models import word2vec
import os
import pandas as pd
import numpy as np
from gensim.models.word2vec import Word2Vec
path = os.getcwd().split("\\")
root_dir = path[:-1]
root_dir = '/'.join(root_dir)
data_path = root_dir + '/data'
data_path = data_path + '/processed_data2.csv'


if __name__ == '__main__':
    sentences = []
    print("Converting to Word2Vector ... ")

    model = Word2Vec.load('models/VNCorpus2.bin')

    model.save(root_dir + '/models/word2vec.bin')
    print("Done")
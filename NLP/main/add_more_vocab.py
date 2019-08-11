from gensim.models import word2vec
from gensim.models.word2vec import Word2Vec
import pandas as pd
import numpy as np

df = pd.read_csv('../data/processed_data2.csv', usecols=[1])
df = df.values
df = np.array(df)
df = df.reshape((1,-1))[0]

model = Word2Vec.load('../models/VNCorpus4.bin')


model.build_vocab(df[0], update=True)

model.save('../models/VNCorpus4.bin')

print("Done :)")
import keras
import numpy as np
import pandas as pd
import os

from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import LabelEncoder
from NLP.main.preprocessor import Preprocessor as CustomPreprocessor
from gensim.models.word2vec import Word2Vec
from gensim.models import KeyedVectors


class TextClassifier:
    def __init__(self, word2vec_dict, model_path, max_length=20, n_epochs=15, batch_size=6, n_class=8):
        self.word2vec = word2vec_dict
        self.max_length = max_length
        self.word_dim = self.word2vec.vector_size
        self.n_epochs = n_epochs
        self.batch_size = batch_size
        self.model_path = model_path
        self.n_class = n_class
        self.model = None

    def build_model(self, input_dim):
        """
        Build model structure
        :param input_dim: input dimension max_length x word_dim
        :return: Keras model
        """
        model = Sequential()

        model.add(LSTM(64, return_sequences=True, input_shape=input_dim))
        model.add(Dropout(0.2))
        model.add(LSTM(32))
        model.add(Dense(self.n_class, activation="softmax"))

        model.compile(loss=keras.losses.categorical_crossentropy,
                      optimizer=keras.optimizers.Adadelta(),
                      metrics=['accuracy'])
        return model

    def train(self, X, y):
        """
        Training with data X, y
        :param X: 3D features array, number of samples x max length x word dimension
        :param y: 2D labels array, number of samples x number of class
        :return:
        """
        self.model = self.build_model(input_dim=(X.shape[1], X.shape[2]))
        self.model.fit(X, y, batch_size=self.batch_size, epochs=self.n_epochs)
        self.model.save_weights(self.model_path)

    def predict(self, X):
        """
        Predict for 3D feature array
        :param X: 3D feature array, converted from string to matrix
        :return: label array y as 2D-array
        """
        if self.model is None:
            self.load_model()
        y = self.model.predict(X)
        return y

    def classify(self, sentences, label_dict=None):
        """
        Classify sentences
        :param sentences: input sentences in format of list of strings
        :param label_dict: dictionary of label ids and names
        :return: label array
        """
        X = self.tokenize_sentences(sentences)
        X = self.word_embed_sentences(X, max_length=self.max_length)
        y = self.predict(np.array(X))
        y = np.argmax(y, axis=1)
        labels = []
        for lab_ in y:
            if label_dict is None:
                labels.append(lab_)
            else:
                labels.append(label_dict[lab_])
        return labels

    def load_model(self):
        """
        Load model from file
        :return: None
        """
        self.model = self.build_model((self.max_length, self.word_dim))
        self.model.load_weights(self.model_path)

    def load_data(self, data_path):
        """
        Load data
        :param data_path: list of paths to files or directories
        :param load_method: method to load (from file or from directory)
        :return: 3D-array X and 2D-array y
        """
        df = pd.read_csv(data_path, encoding='utf-8', usecols=[1, 2])
        X = df.values[:, 0]
        y = df.values[:, 1]
        Encoder = LabelEncoder()
        y = Encoder.fit_transform(y)
        self.n_class = len(set(list(y)))
        y_train = np.zeros((len(y), self.n_class), dtype="float")
        for idx, val in enumerate(y):
            y_train[idx][val] = 1
        y = y_train
        X = self.tokenize_sentences(X)
        X = self.word_embed_sentences(X, max_length=self.max_length)
        return np.array(X), np.array(y)

    # helper
    def word_embed_sentences(self, sentences, max_length=20):
        """
        Helper method to convert word to vector
        :param sentences: input sentences in list of strings format
        :param max_length: max length of sentence you want to keep, pad more or cut off
        :return: embedded sentences as a 3D-array
        """
        embed_sentences = []
        for sent in sentences:
            embed_sent = []
            for word in sent:
                if word.lower() in self.word2vec:
                    embed_sent.append(self.word2vec[word.lower()])
                else:
                    embed_sent.append(np.zeros(shape=(self.word_dim,), dtype=float))
            if len(embed_sent) > max_length:
                embed_sent = embed_sent[:max_length]
            elif len(embed_sent) < max_length:
                embed_sent = np.concatenate((embed_sent, np.zeros(shape=(max_length - len(embed_sent),
                                                                         self.word_dim), dtype=float)),
                                            axis=0)
            embed_sentences.append(embed_sent)
        return embed_sentences

    def tokenize_sentences(self, sentences):
        p = CustomPreprocessor()
        return p.tokenize_list_sentences(sentences)

    def get_label(self, data_path):
        df = pd.read_csv(data_path, encoding='utf-8', usecols=[1, 2])
        X = df.values[:, 0]
        y = df.values[:, 1]
        labels = y
        Encoder = LabelEncoder()
        y = np.array(Encoder.fit_transform(y))
        y = np.concatenate((np.array(y).reshape(-1, 1), np.array(labels).reshape(-1, 1)), axis=1)
        label_dict = {}
        for row in y:
            if row[0] in label_dict:
                pass
            else:
                label_dict[row[0]] = row[1]
        print(label_dict)
        return label_dict


if __name__ == '__main__':
    path = os.getcwd().split("\\")
    root_dir = path[:-1]
    root_dir = '/'.join(root_dir)
    data_path = root_dir + '/data'
    data_path = data_path + '/processed_data.csv'



    word2vec_model = Word2Vec.load('../models/VNCorpus3.bin')
    keras_text_classifier = TextClassifier(word2vec_dict=word2vec_model, model_path='../models/sentiment_model2.h5',
                                           max_length=20, n_epochs=20)
    X, y = keras_text_classifier.load_data(data_path)
    # keras_text_classifier.train(X, y)
    labels = keras_text_classifier.get_label(data_path)
    test_sentence = ['hello', 'chào tạm biệt', 'tạm biệt nha', 'cảm ơn', 'cân bằng phản ứng sau']

    test = keras_text_classifier.classify(test_sentence, label_dict=labels)
    print(test)

import pandas as pd
import os
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
# from src.transformer.feature_transformer import FeatureTransformer
from sklearn.preprocessing import LabelEncoder
import numpy as np
from sklearn import model_selection, naive_bayes, svm

path = os.getcwd().split("\\")
root_dir = path[:-1]
root_dir = '/'.join(root_dir)
data_path = root_dir + '/data'
# output_path = data_path + '/processed_data.txt'
data_path = data_path + '/processed_data.csv'

if __name__ == '__main__':
    df = pd.read_csv(data_path, names=["feature", 'label'])
    X_train = df['feature'].values
    y_train = df['label'].values
    y = y_train
    # print(y_train)
    # Encoding label to categories 0,1,2,...
    Encoder = LabelEncoder()
    y_train = Encoder.fit_transform(y_train)

    y = np.concatenate((np.array(y_train).reshape(-1, 1), np.array(y).reshape(-1, 1)), axis=1)
    # print(label_dict)

    label_dict = {}
    for row in y:
        if row[0] in label_dict:
            pass
        else:
            label_dict[row[0]] = row[1]

    print(label_dict)
    # Vectorize the words using TF-IDF Vectorize
    Tfidf_vectorize = TfidfVectorizer(max_features=5000)
    Tfidf_vectorize.fit(df['feature'].values)

    X_train_vectorized = Tfidf_vectorize.transform(X_train)

    # Naive Bayes algorithm
    Naive = MultinomialNB()
    Naive.fit(X_train_vectorized, y_train)

    predict = Naive.predict(Tfidf_vectorize.transform(['thank you'
                                                       '']))
    print(predict)

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.io import mmwrite, mmread
import pickle

data = pd.read_csv('./result_.csv')

Tfidf = TfidfVectorizer()
Tfidf_matrix = Tfidf.fit_transform(data['mergeStr'].values.astype('U'))

with open('./tfidf.pickle', 'wb') as f:
    pickle.dump(Tfidf, f)

mmwrite('./tfidf.mtx', Tfidf_matrix)
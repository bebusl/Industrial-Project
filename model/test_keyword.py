import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle


data = pd.read_csv('./result_.csv')

Tfidf_matrix = mmread('./tfidf_book_summary.mtx').tocsr()
with open('./tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)

sentence = "레디스 백엔드"

sentence_vec = Tfidf.transform([sentence])
cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)

simScore = [x for x in enumerate(cosine_sim[-1]) if x[1] > 0]
simScore = sorted(simScore, key=lambda x:x[-1], reverse=True)

simScore = simScore[0:len(simScore)]
books = [i[0] for i in simScore]

i = 0
for book in books:
    print(data.iloc[book, 0], simScore[i])
    i += 1
print(len(books), len(data))
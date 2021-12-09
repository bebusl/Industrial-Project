import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle

if __name__ == "__main__":
    data = pd.read_csv('./data/result.csv')

    print("서적 데이터 로딩 완료")

    Tfidf_matrix = mmread('./model/tfidf.mtx').tocsr()
    with open('./model/tfidf.pickle', 'rb') as f:
        Tfidf = pickle.load(f)

    print("TF-IDF 모델 로딩 완료")

    while True:
        sentence = input("검색 : ")  # "레디스 백엔드"

        sentence_vec = Tfidf.transform([sentence])
        cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)

        simScore = [x for x in enumerate(cosine_sim[-1]) if x[1] > 0]
        simScore = sorted(simScore, key=lambda x:x[-1], reverse=True)

        simScore = simScore[0:len(simScore)]
        books = [i[0] for i in simScore]

        for i, book in enumerate(books[:40]):
            print(data.iloc[book, 0], simScore[i])


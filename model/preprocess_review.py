import glob
import pandas as pd
import re
from soynlp.normalizer import repeat_normalize


def load_file():
    path = "./dataset/data_*.csv"
    file_list = glob.glob(path)

    df = pd.DataFrame()
    for file in file_list:
        temp = pd.read_csv(file)
        df = pd.concat([df, temp])

    return df


def clean(review):
    try:
        review = re.sub('<.+?> *', '', review)
        review = re.sub('[^A-Za-z0-9가-힣x ]', '', review)
        review = review.strip()
        review = repeat_normalize(review, num_repeats=2)
    except Exception as e:
        return None

    if len(review.split()) < 4:
        return None

    return review


def preprocess(df):
    df = df.loc[:, 'review'].apply(clean)  # 전처리
    df = df.dropna(axis=0)  # 빈 리뷰 제거

    return df


if __name__ == "__main__":
    df = load_file()
    df = preprocess(df)

    print("총 리뷰 수", df.shape[0])

    df.to_csv("./output/reviews.txt", index=False, header=False)

import pandas as pd
from konlpy.tag import Okt
import re


def clean(sentence):
    if not isinstance(sentence, str):
        return ""

    if sentence[-2:] == "접기":
        sentence = sentence[:-2]

    sentence = re.sub('[^가-힣 | ' ']', '', sentence)
    return sentence


okt = Okt()

data = pd.read_csv("./data.csv")
stopwords = pd.read_csv("./stopwords.csv", encoding='CP949', header=None)
aStopwords = list(stopwords.iloc[:, 0])

size = data.shape[0]
aMergeStr = []

for i in range(size):
    intro = data.iloc[i, 1]
    contents = data.iloc[i, 2]

    mergeStr = clean(intro) + ' ' + clean(contents)

    tokens = okt.nouns(mergeStr)

    words = []
    for token in tokens:
        if token not in aStopwords:  # 불용어 제외
            words.append(token)

    aMergeStr.append(' '.join(words))

data['mergeStr'] = aMergeStr

data.to_csv("./result.csv", index=False)

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

size = data.shape[0]
aMergeStr = []

for i in range(size):
    title, intro, contents = data.iloc[i, 0], data.iloc[i, 1], data.iloc[i, 2]

    mergeStr = clean(title) + ' ' + clean(intro) + ' ' + clean(contents)

    tokens = okt.nouns(mergeStr)

    aMergeStr.append(' '.join(tokens))

data['mergeStr'] = aMergeStr

data.to_csv("./result.csv", index=False)

import pandas as pd
from konlpy.tag import Okt
import re

okt = Okt()

data = pd.read_csv("./data.csv")
stopwords = pd.read_csv("./stopwords.csv", encoding='CP949', header=None)
aStopwords = list(stopwords.iloc[:, 0])

size = data.shape[0]
aMergeStr = []

for i in range(size):
    intro = data.iloc[i, 1]
    contents = data.iloc[i, 2]

    if not isinstance(intro, str):
        intro = ""
    else:
        if intro[-2:] == "접기":
            intro = intro[:-2]

    if not isinstance(contents, str):
        contents = ""
    else:
        if contents[-2:] == "접기":
            contents = contents[:-2]

    mergeStr = intro + ' ' + contents

    filteredStr = re.sub('[^가-힣 | ' ']', '', mergeStr)

    tokens = okt.nouns(filteredStr)

    words = []
    for token in tokens:
        if token not in aStopwords:  # 불용어 제외
            words.append(token)

    aMergeStr.append(' '.join(words))

data['mergeStr'] = aMergeStr

data.to_csv("./result.csv", index=False)

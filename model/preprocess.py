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


def func(title, intro, contents):
    mergeStr = clean(title) + ' ' + clean(intro) + ' ' + clean(contents)

    tokens = okt.nouns(mergeStr)

    filtered_tokens = list(set(tokens))

    return ' '.join(filtered_tokens)


okt = Okt()

data = pd.read_csv("./output/merge_data2.csv", header=0)

data['mergeStr'] = data[['title', 'intro', 'contents']].apply(lambda x:func(x[0], x[1], x[2]), axis=1)

data.to_csv("./output/result.csv", index=False, encoding='utf-8-sig')

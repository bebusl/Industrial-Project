import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle

import requests
from bs4 import BeautifulSoup

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from model.absa.absa_layer import BertABSATagger
from transformers import AutoTokenizer
import torch
from torch.utils.data import DataLoader, TensorDataset, SequentialSampler
import numpy as np
from model.absa.glue_utils import ABSAProcessor, SeqInputFeatures, InputExample
from model.absa.seq_utils import tag2ts
import re
import kss

def get_comment_review(item_id): #요거는 db에 저장된 거 활용해야 함.
    comment_review = []
    try:

        is_orderer = 1  # 2일 경우 전체, 1일 경우 구매자
        url = f"https://www.aladin.co.kr/ucl/shop/product/ajax/GetCommunityListAjax.aspx?ProductItemId={item_id}&itemId={item_id}&pageCount=100&communitytype=CommentReview&nemoType=-1&page=1&startNumber=1&endNumber=10&sort=2&IsOrderer={is_orderer}&BranchType=1&IsAjax=true&pageType=0"

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        boxs = soup.find_all(class_="blog_list3")
        for box in boxs:
            try:
                value = box.find("a").get_text(strip=True)
                comment_review.append(value.replace("이 글에는 스포일러가 포함되어 있습니다. 보시겠습니까?회색 영역을 클릭하면 내용을 확인할 수 있습니다.", ""))
            except Exception as e:
                print(book, e)

    except Exception as e:
        print(book, e)

    return comment_review

def convert_examples_to_seq_features(examples, label_list, tokenizer,
                                     cls_token_at_end=False, pad_on_left=False, cls_token='[CLS]',
                                     sep_token='[SEP]', pad_token=0, sequence_a_segment_id=0,
                                     sequence_b_segment_id=1, cls_token_segment_id=1, pad_token_segment_id=0,
                                     mask_padding_with_zero=True):
    # feature extraction for sequence labeling
    label_map = {label: i for i, label in enumerate(label_list)}
    features = []
    max_seq_length = -1
    examples_tokenized = []
    for (ex_index, example) in enumerate(examples):
        tokens_a = []
        labels_a = []
        evaluate_label_ids = []
        words = example.text_a.split(' ')
        wid, tid = 0, 0
        for word in words:
            subwords = tokenizer.tokenize(word)
            tokens_a.extend(subwords)
            # if label != 'O':
            #     labels_a.extend([label] + ['EQ'] * (len(subwords) - 1))
            # else:
            #     labels_a.extend(['O'] * len(subwords))
            labels_a.extend(['O'] * len(subwords))
            evaluate_label_ids.append(tid)
            wid += 1
            # move the token pointer
            tid += len(subwords)
        # print(evaluate_label_ids)
        assert tid == len(tokens_a)
        evaluate_label_ids = np.array(evaluate_label_ids, dtype=np.int32)

        examples_tokenized.append((tokens_a, labels_a, evaluate_label_ids))
        if len(tokens_a) > max_seq_length:
            max_seq_length = len(tokens_a)
    # count on the [CLS] and [SEP]
    max_seq_length += 2
    # max_seq_length = 128
    for ex_index, (tokens_a, labels_a, evaluate_label_ids) in enumerate(examples_tokenized):
        # tokens_a = [x.replace('▁', '') for x in tokens_a]
        # print(tokens_a)
        # tokens_a = tokenizer.tokenize(example.text_a)

        # Account for [CLS] and [SEP] with "- 2"
        # for sequence labeling, better not truncate the sequence
        # if len(tokens_a) > max_seq_length - 2:
        #    tokens_a = tokens_a[:(max_seq_length - 2)]
        #    labels_a = labels_a
        tokens = tokens_a + [sep_token]
        segment_ids = [sequence_a_segment_id] * len(tokens)
        labels = labels_a + ['O']
        if cls_token_at_end:
            # evaluate label ids not change
            tokens = tokens + [cls_token]
            segment_ids = segment_ids + [cls_token_segment_id]
            labels = labels + ['O']
        else:
            # right shift 1 for evaluate label ids
            tokens = [cls_token] + tokens
            segment_ids = [cls_token_segment_id] + segment_ids
            labels = ['O'] + labels
            evaluate_label_ids += 1
        input_ids = tokenizer.convert_tokens_to_ids(tokens)
        input_mask = [1 if mask_padding_with_zero else 0] * len(input_ids)
        # Zero-pad up to the sequence length.
        padding_length = max_seq_length - len(input_ids)
        # print("Current labels:", labels)
        label_ids = [label_map[label] for label in labels]

        # pad the input sequence and the mask sequence
        if pad_on_left:
            input_ids = ([pad_token] * padding_length) + input_ids
            input_mask = ([0 if mask_padding_with_zero else 1]
                          * padding_length) + input_mask
            segment_ids = ([pad_token_segment_id] *
                           padding_length) + segment_ids
            # pad sequence tag 'O'
            label_ids = ([0] * padding_length) + label_ids
            # right shift padding_length for evaluate_label_ids
            evaluate_label_ids += padding_length
        else:
            # evaluate ids not change
            input_ids = input_ids + ([pad_token] * padding_length)
            input_mask = input_mask + \
                         ([0 if mask_padding_with_zero else 1] * padding_length)
            segment_ids = segment_ids + \
                          ([pad_token_segment_id] * padding_length)
            # pad sequence tag 'O'
            label_ids = label_ids + ([0] * padding_length)
        assert len(input_ids) == max_seq_length
        assert len(input_mask) == max_seq_length
        assert len(segment_ids) == max_seq_length
        assert len(label_ids) == max_seq_length

        features.append(
            SeqInputFeatures(input_ids=input_ids,
                             input_mask=input_mask,
                             segment_ids=segment_ids,
                             label_ids=label_ids,
                             evaluate_label_ids=evaluate_label_ids))

    print("maximal sequence length is", max_seq_length)
    return features


def load_and_cache_examples(tokenizer, reviews):
    processor = ABSAProcessor()

    label_list = processor.get_labels('BIEOS')

    examples = []
    sample_id = 0
    for review in reviews:
        guid = "%s-%s" % ('test', sample_id)
        text_a = ' '.join([word.replace("#", "")
                           for word in tokenizer.tokenize(review)])
        examples.append(InputExample(
            guid=guid, text_a=text_a, text_b=[], label=[]))
        sample_id += 1

    features = convert_examples_to_seq_features(examples=examples, label_list=label_list, tokenizer=tokenizer,
                                                cls_token_at_end=False,
                                                cls_token=tokenizer.cls_token,
                                                sep_token=tokenizer.sep_token,
                                                cls_token_segment_id=0,
                                                pad_on_left=False,
                                                pad_token_segment_id=0)
    total_words = []
    for input_example in examples:
        text = input_example.text_a
        total_words.append(text.split(' '))

    # Convert to Tensors and build dataset
    all_input_ids = torch.tensor(
        [f.input_ids for f in features], dtype=torch.long)
    all_input_mask = torch.tensor(
        [f.input_mask for f in features], dtype=torch.long)
    all_segment_ids = torch.tensor(
        [f.segment_ids for f in features], dtype=torch.long)

    all_label_ids = torch.tensor(
        [f.label_ids for f in features], dtype=torch.long)
    # used in evaluation
    all_evaluate_label_ids = [f.evaluate_label_ids for f in features]
    dataset = TensorDataset(all_input_ids, all_input_mask,
                            all_segment_ids, all_label_ids)
    return dataset, all_evaluate_label_ids, total_words


"""
데이터 저장부분 수정 : db에[[키워드1],[키워드2],[키워드3]] 으로 저장되던 것을 
                     {"키워드1":{POS: , NEU, NEG},"키워드2":{POS, NEU, NEG}}형태로 접근하기 쉽게 만듦
"""


def analysis(model, dataloader, evaluate_label_ids, total_words):
    result = {}
    idx = 0
    absa_label_vocab = {'O': 0, 'EQ': 1, 'B-POS': 2, 'I-POS': 3, 'E-POS': 4, 'S-POS': 5, 'B-NEG': 6,
                        'I-NEG': 7, 'E-NEG': 8, 'S-NEG': 9, 'B-NEU': 10, 'I-NEU': 11, 'E-NEU': 12, 'S-NEU': 13}
    absa_id2tag = {}
    for k in absa_label_vocab:
        v = absa_label_vocab[k]
        absa_id2tag[v] = k

    for batch in dataloader:
        batch = tuple(t.to('cpu') for t in batch) #gpu쓸거면 t.to('cuda')로 변경
        try:
            with torch.no_grad():
                inputs = {'input_ids': batch[0],
                          'attention_mask': batch[1],
                          'token_type_ids': batch[2],
                          'labels': batch[3]}
                outputs = model(**inputs)
                logits = outputs[1]
                preds = np.argmax(logits.detach().cpu().numpy(), axis=-1)
                label_indices = evaluate_label_ids[idx]
                pred_labels = preds[0][label_indices]
                words = total_words[idx]
                assert len(words) == len(pred_labels)
                pred_tags = [absa_id2tag[label] for label in pred_labels]

                p_ts_sequence = tag2ts(ts_tag_sequence=pred_tags)
                for t in p_ts_sequence:
                    beg, end, sentiment = t
                    aspect = ''.join(words[beg:end + 1])

                    if aspect in result:
                        result[aspect][sentiment] += 1
                    else:
                        result[aspect] = {}
                        result[aspect]['POS'] = 0
                        result[aspect]['NEG'] = 0
                        result[aspect][sentiment] = 1
                idx += 1
        except Exception as e:
            pass

    keywords = {}
    for key, value in result.items():
        keywords[key] = value

    return result


if __name__ == "__main__":
    data = pd.read_csv('./model/result.csv')

    print("서적 데이터 로딩 완료")

    Tfidf_matrix = mmread('./model/tfidf.mtx').tocsr()
    with open('./model/tfidf.pickle', 'rb') as f:
        Tfidf = pickle.load(f)

    print("TF-IDF 모델 로딩 완료")

    model_class = BertABSATagger
    tokenizer_class = AutoTokenizer

    model = model_class.from_pretrained("./model/absa/checkpoint-100/")
    tokenizer = tokenizer_class.from_pretrained("beomi/kcbert-base")

    device = torch.device("cpu")  # cuda
    model.to(device)  # cuda
    model.eval()

    kss.split_sentences("로딩")

    while True:
        sentence = input("검색 : ") # "레디스 백엔드"

        sentence_vec = Tfidf.transform([sentence])
        cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)

        simScore = [x for x in enumerate(cosine_sim[-1]) if x[1] > 0]
        simScore = sorted(simScore, key=lambda x:x[-1], reverse=True)

        simScore = simScore[0:len(simScore)]
        books = [i[0] for i in simScore]

        i = 0
        ## 여기까지가 유사한 책 찾기
        for book in books[:10]:
            print(data.iloc[book, 0], simScore[i])
            reviews = get_comment_review(data.iloc[book, 3])
            # 여기서 리뷰르ㅡㄹ 긁어옴
            
            ## 여기서부터 전처리 책 n권당 review를 저장해야겠쥬?! 이 밑이 그럼 모델에 넣어서 분석하는 곳!
            if len(reviews) > 0:
                reviewList = []
                reviews = re.sub('<.+?> *', '', str(reviews))
                reviews = re.sub('[^A-Za-z0-9가-힣x ]', '', reviews)
                reviews = ' '.join(reviews.split())
                for review in kss.split_sentences(reviews):
                    if len(review) < 20:
                        continue
                    reviewList.append(review)
                print("내가 알고싶은 부분",reviewList)
                dataset, evaluate_label_ids, total_words = load_and_cache_examples(
                    tokenizer, reviewList)
                sampler = SequentialSampler(dataset)

                dataloader = DataLoader(dataset, sampler=sampler, batch_size=1)

                result = analysis(model, dataloader,
                                        evaluate_label_ids, total_words)
                print(result)

            i += 1

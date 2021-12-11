from torch.utils import data
from kafka import KafkaConsumer, KafkaProducer
import os
import numpy as np
import torch
import konlpy.tag
from glue_utils import ABSAProcessor, SeqInputFeatures, InputExample
from transformers import AutoTokenizer
from absa_layer import BertABSATagger
from torch.utils.data import DataLoader, TensorDataset, SequentialSampler
from seq_utils import tag2ts
import re
import emoji
from soynlp.normalizer import repeat_normalize
import time
from dotenv import load_dotenv
import pymongo
import urllib.parse
from bson.objectid import ObjectId
from bson.dbref import DBRef


def clean(x):
    x = pattern.sub(' ', x)
    x = url_pattern.sub('', x)
    x = x.strip()
    x = repeat_normalize(x, num_repeats=2)
    return x


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
    #max_seq_length = 128
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
        #print("Current labels:", labels)
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
    test = []

    absa_id2tag = {}
    for k in absa_label_vocab:
        v = absa_label_vocab[k]
        absa_id2tag[v] = k

    for batch in dataloader:
        batch = tuple(t.to('cpu') for t in batch)
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
                test.append({})
                for t in p_ts_sequence:
                    beg, end, sentiment = t
                    aspect = ''.join(words[beg:end+1])
                    if aspect in result:
                        result[aspect][sentiment] += 1
                    else:
                        result[aspect] = {}
                        result[aspect]['POS'] = 0
                        result[aspect]['NEU'] = 0
                        result[aspect]['NEG'] = 0
                        result[aspect][sentiment] = 1

                    if aspect in test[idx]:
                        test[idx][aspect][sentiment] += 1
                    else:
                        test[idx][aspect] = {}
                        test[idx][aspect]['POS'] = 0
                        test[idx][aspect]['NEU'] = 0
                        test[idx][aspect]['NEG'] = 0
                        test[idx][aspect][sentiment] = 1
                idx += 1
        except:
            pass

    keywords={}
    for key, value in result.items():
        keywords[key]=value

    return test, keywords


if __name__ == '__main__':
    username = urllib.parse.quote_plus('root')
    password = urllib.parse.quote_plus('root')

    load_dotenv('../.env')
    MONGO_MAIN_DB_URL = os.getenv('MONGO_MAIN_DB_URL')
    client = pymongo.MongoClient(
        "mongodb://%s:%s@mongo" % (username, password))

    emojis = ''.join(emoji.UNICODE_EMOJI.keys())
    pattern = re.compile(f'[^ .,?!/@$%~％·∼()\x00-\x7Fㄱ-ㅣ가-힣{emojis}]+')
    url_pattern = re.compile(
        r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)')

    model_class = BertABSATagger
    tokenizer_class = AutoTokenizer

    model = model_class.from_pretrained("./checkpoint-100/")
    tokenizer = tokenizer_class.from_pretrained("beomi/kcbert-base")

    device = torch.device("cpu")  # cuda
    model.to(device)  # cuda
    model.eval()

    Okt = konlpy.tag.Okt()

    producer = KafkaProducer(bootstrap_servers='kafka:9093')
    consumer = KafkaConsumer(
        'analysis',
        bootstrap_servers=['kafka:9093'],
        auto_offset_reset='latest',
        enable_auto_commit=True
    )

    print(consumer)

    for message in consumer:
        message = message.value
        keywordId = message.decode()
        print(keywordId)

        start = time.time()

        mydb = client['psa']
        searchKeywords = mydb['searchkeywords']
        productDetails = mydb['productdetails']
        analyses = mydb['analysis']
        reviewDetails = mydb['reviewdetails']

        searchKeyword = searchKeywords.find_one({"_id": ObjectId(keywordId)})
        products = searchKeyword['products']

        for productRef in searchKeyword['products']:
            product = mydb.dereference(productRef)
            reviews = mydb.dereference(product["reviews"])

            review_list = []
            for i in reviews['reviews']:
                review_ = mydb.dereference(i)
                review_list.append(review_["review"])
            dataset, evaluate_label_ids, total_words = load_and_cache_examples(
                tokenizer, review_list)
            sampler = SequentialSampler(dataset)

            dataloader = DataLoader(dataset, sampler=sampler, batch_size=1)

            test, result = analysis(model, dataloader,
                              evaluate_label_ids, total_words)
            
            index = 0
            for i in reviews['reviews']:
                if len(test[index]) > 0:
                    review_ = mydb.dereference(i)
                    myquery = {"_id": review_['_id']}
                    newvalues = {"$set": {"analysis": test[index]}}
                    reviewDetails.update(myquery, newvalues)

                index += 1

            print("최종", result)
            
            #같은 키워드인데 조사가 붙었을 경우 처리
            result_ = {}

            for key,value in result.items():
                try:
                    keyword = Okt.nouns(key)[0]
                    if keyword in result_ :
                        result_[keyword]["POS"] = result_[keyword]["POS"]+value["POS"]
                        result_[keyword]["NEU"] = result_[keyword]["NEU"]+value["NEU"]
                        result_[keyword]["NEG"] = result_[keyword]["NEG"]+value["NEG"]
                    else:
                        result_[keyword]={}
                        result_[keyword]["POS"] = value["POS"]
                        result_[keyword]["NEU"] = value["NEU"]
                        result_[keyword]["NEG"] = value["NEG"]
                except:
                    print("키워드 처리과정 에러 발생"+ str(Okt.nouns(key)))
                    pass

            data = {
                "result": result_
            }

            anaysisId = analyses.insert(data)

            myquery = {"_id": product['_id']}
            newvalues = {"$set": {"analysis": DBRef(
                collection='analysis', id=anaysisId)}}

            productDetails.update(myquery, newvalues)

        print("걸린시간 %d초" % (time.time() - start))

        producer.send('result', value=str(keywordId).encode())

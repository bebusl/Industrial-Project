from collections import MutableSequence
from celery import Celery,chord,group
from kombu import Queue
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
import requests
from bs4 import BeautifulSoup
import time
from celery.result import allow_join_result

broker_url = 'amqp://localhost'

app= Celery('tasks',backend='redis://',broker=broker_url)

app.conf.task_default_queue = 'general'

app.conf.task_queues=(
    Queue('general',routing_key='tasks.#'),
    Queue('crawl',routing_key='crawl.#'),
)

Tfidf_matrix = mmread('./model/tfidf.mtx').tocsr()
Tfidf = ""
with open('./model/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)

@app.task
def merge_text(texts):
    rtn = []
    for i in texts:
        rtn.append(i)
    return rtn

@app.task
def crawl(books):
    _id = books[0]
    item_id=books[1]
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
                print(item_id, e)

    except Exception as e:
        print(item_id, e)

    return {"_id":_id,"item_id":item_id,"reviews":comment_review}



@app.task
def find_books(searchKeyword):
    global Tfidf_matrix, Tfidf
    sentence = searchKeyword
    sentence_vec = Tfidf.transform([sentence])
    cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)

    simScore = [x for x in enumerate(cosine_sim[-1]) if x[1] > 0]
    simScore = sorted(simScore, key=lambda x:x[-1], reverse=True)

    simScore = simScore[0:len(simScore)]
    books = [i[0] for i in simScore]
  
    #print(books[0:10] if len(books)>10 else books)
    result = books[0:20] if len(books)>20 else books
    return result
        
@app.task
def multi(searchKeyword):
    """
    1. 유사도 책찾기
    2. 서브 태스크 만들어 n개의 워커에서 동시에 크롤링 병렬 처리
    3. 서브 태스크 만들어 m개의 워커에서 리뷰 분할하여 처리
    """
    books = find_books(searchKeyword)
    return books

    
    return books




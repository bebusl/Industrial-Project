import requests
from bs4 import BeautifulSoup
import time
import math
import pandas as pd
import multiprocessing

from urllib3.exceptions import NewConnectionError


def get_book(book):
    book_list = None
    try:
        res = requests.get(book)

        if res.status_code == 200:
            book_info = BeautifulSoup(res.text, 'html.parser')

            isbn = book_info.find(id="wa_product_top1_wa_Top_BtnSet1_hd_ISBN").get("value")
            isbn13 = book_info.find("meta", property="books:isbn").get("content")
            item_id = book.split("=")[-1]
            title = book_info.find(class_="Ere_bo_title").get_text(strip=True)

            is_orderer = 1  # 2일 경우 전체, 1일 경우 구매자
            url = f"https://www.aladin.co.kr/ucl/shop/product/ajax/GetCommunityListAjax.aspx?ProductItemId={item_id}&itemId={item_id}&pageCount=100&communitytype=CommentReview&nemoType=-1&page=1&startNumber=1&endNumber=10&sort=2&IsOrderer={is_orderer}&BranchType=1&IsAjax=true&pageType=0"

            comment_review = []

            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            boxs = soup.find_all(class_="blog_list3")
            for box in boxs:
                try:
                    value = box.find("a").get_text(strip=True)
                    comment_review.append(value.replace("이 글에는 스포일러가 포함되어 있습니다. 보시겠습니까?회색 영역을 클릭하면 내용을 확인할 수 있습니다.", ""))
                except Exception as e:
                    print(book, e)

            if len(comment_review) == 0:
                return book_list
            if isbn is None:
                isbn = ''
            if isbn13 is None:
                isbn13 = ''
            if item_id is None:
                item_id = ''

            book_list = { "title": title, 'isbn': isbn, 'isbn13': isbn13, 'itemId': item_id, "commentReview": comment_review }

        else:
            print("실패", book)
    except NewConnectionError as e:
        print(book, e)
    except:
        pass

    return book_list


def get_books(data):
    page, cid = data
    url = f'https://www.aladin.co.kr/shop/wbrowse.aspx?BrowseTarget=List&ViewRowsCount=100&ViewType=Detail&PublishMonth=0&SortOrder=2&page={page}&Stockstatus=1&PublishDay=84&CID={cid}'
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        book_list = []

        for test in soup.find_all(class_="bo3"):
            url = test.get("href")
            book_list.append(url)

        return book_list

    return None


if __name__ == "__main__":
    totals = [3200, 6600, 16600, 3300, 6800, 48000, 7500, 19000, 39800, 33900, 27800, 10600, 3400, 6800, 11500, 8600,
              16600, 15800, 6900, 9000, 25000, 2200, 4300, 7100]
    cidList = [1230, 55890, 170, 2105, 987, 8257, 2551, 798, 1, 1383, 1108, 55889, 1196, 74, 517, 1322, 13789, 656, 336,
               112011, 1237, 2030, 1137, 351]

    thread = 8

    for i in range(len(cidList)):
        start = time.time()
        cid = cidList[i]
        total = totals[i]
        data = {'title': [], 'isbn': [], 'isbn13': [], 'itemId': [], 'commentReview': []}
        totalPage = math.ceil(total / 100)

        book_list = []
        inputs = []
        for page in range(1, totalPage + 1):
            inputs.append([page, cid])

        pool = multiprocessing.Pool(thread)
        for result in pool.map(get_books, inputs):
            if result is not None:
                book_list.extend(result)

        print("parse book list_" + str(cid), time.time() - start)

        pool = multiprocessing.Pool(thread)
        for result in pool.map(get_book, book_list):
            if result is not None:
                data["title"].append(result["title"])
                data["isbn"].append(result["isbn"])
                data["isbn13"].append(result["isbn13"])
                data["itemId"].append(result["itemId"])
                data["commentReview"].append(result["commentReview"])

        print("final_" + str(cid), time.time() - start)
        df = pd.DataFrame(data)
        df.to_csv("../model/dataset/comment_review_data_" + str(cid) + ".csv", index=False, encoding='utf-8-sig', errors="ignore")

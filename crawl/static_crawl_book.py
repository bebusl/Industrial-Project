import requests
from bs4 import BeautifulSoup
import time
import math
import pandas as pd
import multiprocessing


def get_books(book):
    book_list = None
    try:
        res = requests.get(book)

        if res.status_code == 200:
            book_info = BeautifulSoup(res.text, 'html.parser')

            isbn = book_info.find(id="wa_product_top1_wa_Top_BtnSet1_hd_ISBN").get("value")
            isbn13 = book_info.find("meta", property="books:isbn").get("content")
            itemid = book.split("=")[-1]
            title = book_info.find(class_="Ere_bo_title").get_text(strip=True)
            intro = ""
            contents = ""
            url = "https://www.aladin.co.kr/shop/product/getContents.aspx?ISBN=" + isbn + "&name=Introduce&type=0&date=0"
            headers = {'Referer': book}

            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            boxs = soup.find_all(class_="Ere_prod_mconts_box")
            for box in boxs:
                try:
                    name = box.find(class_="Ere_prod_mconts_LL").text
                    if name == "목차":
                        contents = box.find(class_="Ere_prod_mconts_R").get_text(strip=True)
                    if name == "책소개":
                        intro = box.find(class_="Ere_prod_mconts_R").get_text(strip=True)
                except Exception as e:
                    print(book, e)

            book_list = { "title": title, 'isbn': isbn, 'isbn13': isbn13, 'itemId': itemid, "contents": contents, "intro": intro }

        else:
            print("실패", book)
    except Exception as e:
        print(book, e)

    return book_list


if __name__ == "__main__":
    totals = [3200, 6600, 16600, 3300, 6800, 48000, 7500, 19000, 39800, 33900, 27800, 10600, 3400, 6800, 11500, 8600, 16600, 15800, 6900, 9000, 25000, 2200, 4300, 7100]
    cidList = [1230, 55890, 170, 2105, 987, 8257, 2551, 798, 1, 1383, 1108, 55889, 1196, 74, 517, 1322, 13789, 656, 336, 112011, 1237, 2030, 1137, 351]
    count = 60
    thread = 4

    for i in range(len(cidList)):
        cid = cidList[i]
        total = totals[i]
        data = {'title': [], 'isbn': [], 'isbn13': [], 'itemId': [], 'intro': [], 'contents': []}
        totalPage = math.ceil(total / count)
        temp = total
        for page in range(1, totalPage + 1):
            start = time.time()
            url = f'https://www.aladin.co.kr/shop/wbrowse.aspx?BrowseTarget=List&ViewRowsCount={count}&ViewType=Detail&PublishMonth=0&SortOrder=2&page={page}&Stockstatus=1&PublishDay=84&CID={cid}'
            response = requests.get(url)

            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                bookList = []

                for test in soup.find_all(class_="bo3"):
                    url = test.get("href")
                    bookList.append(url)
                    temp -= 1
                    if temp <= 0:
                        break

                pool = multiprocessing.Pool(thread)
                for result in pool.map(get_books, bookList):
                    data["title"].extend(result["title"])
                    data["isbn"].extend(result["isbn"])
                    data["isbn13"].extend(result["isbn13"])
                    data["itemId"].extend(result["itemId"])
                    data["intro"].extend(result["intro"])
                    data["contents"].extend(result["contents"])

                print(str(cid), temp, "/", "total", time.time() - start)

        print("final_" + str(cid), time.time() - start)
        df = pd.DataFrame(data)
        df.to_csv("../model/dataset/book_data_" + str(cid) + ".csv", index=False, encoding='utf-8-sig')

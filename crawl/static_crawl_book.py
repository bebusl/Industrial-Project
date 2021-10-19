import requests
from bs4 import BeautifulSoup
import time
import math
import pandas as pd
import multiprocessing


def get_books(book):
    book_list = {'title': [], 'intro': [], 'contents': []}
    res = requests.get(book)

    if res.status_code == 200:
        book_info = BeautifulSoup(res.text, 'html.parser')

        isbn2 = book_info.find(id="CoverMainImage").get("src")[-16:-6]
        title = book_info.find(class_="Ere_bo_title").get_text(strip=True)
        intro = ""
        contents = ""
        url = "https://www.aladin.co.kr/shop/product/getContents.aspx?ISBN="+isbn2+"&name=Introduce&type=0&date=7"
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
                print(e)

        book_list["title"].append(title)
        book_list["contents"].append(contents)
        book_list["intro"].append(intro)

    else:
        print("실패", book)

    return book_list


if __name__ == "__main__":
    total = 1000
    cidList = [1230, 55890, 170, 2105, 987, 8257, 2551, 798, 1108, 55889, 1196, 74, 517, 1322, 13789, 656, 336, 112011, 2913, 1237, 2030, 1137, 50246, 76000, 76001]
    count = 60
    thread = 8
    totalPage = math.ceil(total / count)
    start = time.time()

    for cid in cidList:
        data = {'title': [], 'intro': [], 'contents': []}
        temp = total
        for page in range(1, totalPage + 1):
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
                    data["intro"].extend(result["intro"])
                    data["contents"].extend(result["contents"])

                print(str(cid), temp, "/", "total", time.time() - start)

        print("final_" + str(cid), time.time() - start)
        df = pd.DataFrame(data)
        df.to_csv("./data_" + str(cid) + ".csv", index=False, encoding='utf-8-sig')

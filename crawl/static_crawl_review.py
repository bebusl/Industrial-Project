import requests
from bs4 import BeautifulSoup
import time
import math
import pandas as pd
import multiprocessing


def get_review(isbn, base):
    reviews = []
    review_url = 'https://www.aladin.co.kr/shop/product/getcontents.aspx?name=MyReview&ISBN=' + isbn + '&Page=1&PageSize=10&IsOrderer=1&Sort=2'
    headers = {'Referer': base}

    review_res = requests.get(review_url, headers=headers)

    paper_ids = []

    if review_res.status_code == 200:
        review_html = review_res.text
        review_soup = BeautifulSoup(review_html, 'html.parser')

        if review_soup is not None:
            for box in review_soup.find_all(class_="blog_list3"):
                for div in box.find_all("div"):
                    try:
                        paper_id = div["id"]
                        if "_" in paper_id:
                            paper_id = int(paper_id.split("_")[1])
                            if paper_id not in paper_ids:
                                paper_ids.append(paper_id)
                    except Exception as e:
                        # print(e)
                        pass

            url2 = "https://www.aladin.co.kr/ucl/shop/product/ajax/viewmypaperall_v2.aspx?IsMore=1&communityType=MyReview"

            for id in paper_ids:
                params = {"paperid": id}
                res = requests.get(url2, params=params)
                if res.status_code == 200:
                    html = res.text
                    soup = BeautifulSoup(html, 'html.parser')
                    review = soup.get_text(strip=True)
                    reviews.append(review)
                else:
                    print("실패", base, id)

    return reviews


def get_book(book):
    res = requests.get(book)

    if res.status_code == 200:
        book_info = BeautifulSoup(res.text, 'html.parser')
        title = book_info.find(class_="Ere_bo_title").get_text(strip=True)
        infos = book_info.find(class_="conts_info_list1")

        if infos is not None:
            for info in infos.find_all("li"):
                txt = info.text

                if "ISBN" in txt:
                    isbn = txt.split(":")[1][1:]
                    review = get_review(isbn, book)
                    return {'title':title, 'review': review}

    else:
        print("실패", book)

    return None


if __name__ == "__main__":
    total = 25
    cidList = [1230, 55890, 170, 2105, 987, 8257, 2551, 798, 1, 1383, 1108, 55889, 1196, 74, 517, 1322, 13789, 656, 336, 112011,
               1237, 2030, 1137, 351]
    count = 25
    thread = 4
    totalPage = math.ceil(total / count)

    for cid in cidList:
        start = time.time()
        data = {'title': [], 'review': []}
        temp = total
        for page in range(1, totalPage + 1):
            url = f'https://www.aladin.co.kr/shop/wbrowse.aspx?BrowseTarget=List&ViewRowsCount={count}&ViewType=Detail&PublishMonth=0&SortOrder=2&page={page}&Stockstatus=1&PublishDay=84&CID={cid}'
            response = requests.get(url)
            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                book_list = []
                for test in soup.find_all(class_="bo3"):
                    url = test.get("href")
                    book_list.append(url)
                    temp -= 1
                    if temp <= 0:
                        break

                pool = multiprocessing.Pool(thread)
                for result in pool.map(get_book, book_list):
                    if result is not None:
                        review = result['review']
                        data["title"].extend([result['title']] * len(review))
                        data["review"].extend(review)

                print(str(cid), temp, "/", "total", time.time() - start)

        df = pd.DataFrame(data)
        df.to_csv("./data_" + str(cid) + ".csv", index=False, encoding='utf-8-sig')
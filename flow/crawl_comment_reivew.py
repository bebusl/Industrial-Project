import requests
from bs4 import BeautifulSoup


def get_comment_review(item_id):
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

    return comment_review


if __name__ == "__main__":
    print(get_comment_review(275874708))

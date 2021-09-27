from selenium import webdriver
import time
from selenium.webdriver import ActionChains
import math
import pandas as pd
from selenium.common.exceptions import NoSuchElementException

def getIndex(driver, content):
    elements = driver.find_elements_by_class_name("Ere_prod_mconts_LS")
    index = 0
    for element in elements:
        if element.text == content:
            return index
        index += 1
    return -1

def getBook(driver, bookIdx, data):
    book = driver.find_element_by_xpath(
        f'//div[{bookIdx + 1}][@class="ss_book_box"]//*[@class="ss_book_list"]//li/a')
    book.click()

    try:
        title = driver.find_element_by_class_name("Ere_bo_title").text
    except NoSuchElementException:
        return False  # 재시도 해라 마!

    try:
        event = driver.find_element_by_id('swiper_itemEvent')
        action.move_to_element(event).perform()
    except:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2)")
        time.sleep(0.3)

    try:
        # 목차에 더보기 버튼이 있을 때
        hasTOCMore = driver.find_element_by_id("div_TOC_All")

        driver.execute_script("javascript:fn_show_introduce_TOC('TOC')")
    except:
        pass


    elements = driver.find_elements_by_class_name("Ere_prod_mconts_R")
    introIndex = getIndex(driver, "책소개")
    contentsIndex = getIndex(driver, "목차")

    intro = elements[introIndex].text.replace("\n", " ")
    contents = elements[contentsIndex].text.replace("\n", " ")

    driver.back()

    if introIndex > 0 and contentsIndex == -1:
        print(title, "목차 가져오기 실패")
        data['title'].append(title)
        data['intro'].append(intro)
        data['contents'].append("")
    elif introIndex == -1 and contentsIndex > 0:
        print(title, "소개 가져오기 실패")
        data['title'].append(title)
        data['intro'].append("")
        data['contents'].append(contents)
    elif introIndex == -1 and contentsIndex == -1:
        print(title, "소개/목차 가져오기 실패")
    else:
        data['title'].append(title)
        data['intro'].append(intro)
        data['contents'].append(contents)

    return True

chromedriver = 'C:/Temp/chromedriver.exe'
driver = webdriver.Chrome(chromedriver)
driver.implicitly_wait(1)
action = ActionChains(driver)

total = 10
temp = total
cidList = [1]
totalPage = math.ceil(total / 25)

start = time.time()

data = {'title': [], 'intro': [], 'contents': []}

for cid in cidList:
    for page in range(1, totalPage + 1):
        url = f'https://www.aladin.co.kr/shop/wbrowse.aspx?BrowseTarget=List&ViewRowsCount=25&ViewType=Detail&PublishMonth=0&SortOrder=2&page={page}&Stockstatus=1&PublishDay=84&CID={cid}'
        driver.get(url)

        for bookIdx in range(25):
            if temp <= 0:
                break
            temp -= 1

            retryCount = 5
            while retryCount > 0:
                if getBook(driver, bookIdx, data):
                    break
                retryCount -= 1
                print("재시도", retryCount, page, bookIdx)

            if retryCount == 0:
                print("수집 실패", page, bookIdx)

            if temp % 10 == 0:
                print(temp, "/", total, time.time() - start)

driver.close()

print("final", time.time() - start)

df = pd.DataFrame(data)
df.to_csv("C:/Users/ghks0/Desktop/Project/Industrial-Project/crawl/data.csv", index=False, encoding='utf-8-sig')
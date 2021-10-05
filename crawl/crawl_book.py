from selenium import webdriver
import time
from selenium.webdriver import ActionChains
import math
import pandas as pd
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException
from selenium.webdriver.common.keys import Keys

def getBook(driver, bookIdx, data):
    try:
        book = driver.find_element_by_xpath(
            f'//div[{bookIdx + 1}][@class="ss_book_box"]//*[@class="ss_book_list"]//li/a')
        try:
            book.click()
        except:
            book.send_keys(Keys.ENTER)

        try:
            event = driver.find_element_by_id('swiper_itemEvent')
            action = ActionChains(driver)
            action.move_to_element(event).perform()
        except:
            return True


        try:
            title = driver.find_element_by_class_name("Ere_bo_title").text
        except NoSuchElementException:
            return False  # 재시도 해라 마!

        try:
            # 목차에 더보기 버튼이 있을 때
            hasTOCMore = driver.find_element_by_id("div_TOC_All")

            driver.execute_script("javascript:fn_show_introduce_TOC('TOC')")
        except:
            pass

        intro = ""
        contents = ""

        subtitles = driver.find_elements_by_class_name("Ere_prod_mconts_LS")
        for subtitle in subtitles:
            try:
                element = subtitle.find_element_by_xpath(".//following-sibling::div[@class='Ere_prod_mconts_R']")
                if subtitle.text == "책소개":
                    intro = element.text.replace("\n", " ")
                elif subtitle.text == "목차":
                    contents = element.text.replace("\n", " ")
            except:
                pass

        driver.back()

        if intro == "" and contents == "":
            print(title, "소개/목차 가져오기 실패")
        else:
            data['title'].append(title)
            data['intro'].append(intro)
            data['contents'].append(contents)

    except UnexpectedAlertPresentException: # 19세 미만 로그인 필요 경고
        print("UnexpectedAlertPresentException")
        pass

    return True

chromedriver = 'C:/Temp/chromedriver.exe'
driver = webdriver.Chrome(chromedriver)
driver.implicitly_wait(1)
action = ActionChains(driver)

total = 1000
cidList = [1230, 55890, 170, 2105, 987, 8257, 2551, 798, 1108, 55889, 1196, 74, 517, 1322, 13789, 656, 336, 112011, 2913, 1237, 2030, 1137, 50246, 76000, 76001]
totalPage = math.ceil(total / 25)
start = time.time()

for cid in cidList:
    data = {'title': [], 'intro': [], 'contents': []}
    temp = total
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
                print(cid, temp, "/", total, time.time() - start)
    print("final_" + str(cid), time.time() - start)
    df = pd.DataFrame(data)
    df.to_csv("./data_" + str(cid) + ".csv", index=False, encoding='utf-8-sig')

driver.close()
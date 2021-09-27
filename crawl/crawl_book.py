from selenium import webdriver
import time
from selenium.webdriver import ActionChains
import math

def getIndex(driver, content):
    elements = driver.find_elements_by_class_name("Ere_prod_mconts_LS")
    index = 0
    for element in elements:
        if element.text == content:
            return index
        index += 1
    return -1

chromedriver = 'C:/Temp/chromedriver.exe'
driver = webdriver.Chrome(chromedriver)
driver.implicitly_wait(1)
action = ActionChains(driver)

total = 10
cidList = [1]
totalPage = math.ceil(total / 25)

start = time.time()

for cid in cidList:
    for page in range(1, totalPage + 1):
        url = f'https://www.aladin.co.kr/shop/wbrowse.aspx?BrowseTarget=List&ViewRowsCount=25&ViewType=Detail&PublishMonth=0&SortOrder=2&page={page}&Stockstatus=1&PublishDay=84&CID={cid}'
        driver.get(url)

        for bookIdx in range(25):

            if total <= 0:
                break
            total -= 1

            book = driver.find_element_by_xpath(
                f'//div[{bookIdx + 1}][@class="ss_book_box"]//*[@class="ss_book_list"]//li/a')
            book.click()

            title = driver.find_element_by_class_name("Ere_bo_title").text

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2)")

            try:
                # 목차에 더보기 버튼이 있을 때
                hasTOCMore = driver.find_element_by_id("div_TOC_All")

                driver.execute_script("javascript:fn_show_introduce_TOC('TOC')")
            except:
                pass

            time.sleep(0.3)

            elements = driver.find_elements_by_class_name("Ere_prod_mconts_R")
            introIndex = getIndex(driver, "책소개")
            contentsIndex = getIndex(driver, "목차")

            intro = elements[introIndex].text.replace("\n", " ")
            contents = elements[contentsIndex].text.replace("\n", " ")

            print(title)
            print(intro)
            print(contents)

            driver.back()

driver.close()

print("final", time.time() - start)
from selenium import webdriver
import time
from selenium.webdriver import ActionChains

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

start = time.time()

for id in [279336165]:
    driver.get('https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=' + str(id))

    title = driver.find_element_by_class_name("Ere_bo_title").text

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2)")

    time.sleep(0.3)

    elements = driver.find_elements_by_class_name("Ere_prod_mconts_R")
    introIndex = getIndex(driver, "책소개")
    contentsIndex = getIndex(driver, "목차")

    intro = elements[introIndex].text.replace("\n", " ")
    contents = elements[contentsIndex].text.replace("\n", " ")

    print(title)
    print(intro)
    print(contents)

driver.close()

print("final", time.time() - start)
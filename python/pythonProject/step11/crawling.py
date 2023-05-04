# https://m.place.naver.com/place/list?query=%20%EC%B9%B4%ED%8E%98%20&x=127.014331803826&y=37.6486262922504&keywordFilter=rank%5E%EA%B0%80%EA%B9%8C%EC%9A%B4&level=top&sortingOrder=distance&bounds=126.6598993%3B37.4464614%3B127.3190789%3B37.6750708&zoomLevel=11
import time
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



search = '카페'
latitude = 37.552438063498
longitude = 126.921375976802
key = '가까운'

url = f'https://m.place.naver.com/place/list?query={search}&x={longitude}&y={latitude}&keywordFilter=rank{key}&level=top&sortingOrder=distance'
driver = webdriver.Chrome("C:/Users/Kiot/PycharmProjects/chromedriver_win32/chromedriver.exe")
driver.implicitly_wait(3)
driver.get(url)
time.sleep(3)

add_list = []
li_list = driver.find_elements_by_css_selector('#_list_scroll_container > div > div > div:nth-child(2) > ul> li')
add_element = driver.find_elements_by_class_name('vcshc')  # 요소 선택
i = 0

while True:
    time.sleep(0.1)
    # element = driver.find_elements_by_class_name('vcshc')
    # if len(add_element) != len(element):
    #     print("html 변화 감지")
    #     add_element = driver.find_elements_by_class_name('vcshc')
    # time.sleep(1)
    if i != 20:
        name = driver.find_element_by_css_selector(
            f'#_list_scroll_container > div > div > div:nth-child(2) > ul > li:nth-child({i + 1}) > div > div > a:nth-child(1) > div > div > span.place_bluelink.YwYLL')
        print(name.text)
        # address = driver.find_element_by_xpath(
        #     f'//*[@id="_list_scroll_container"]/div/div/div[2]/ul/li[{i + 1}]/div[1]/div/div/div/div/div[1]')
        address = driver.find_element_by_css_selector(f'#_list_scroll_container > div > div > div:nth-child(2) > ul > li:nth-child({i+1}) > div > div > div > div > span:nth-child(2) > a > span.hClKF')
        address = re.sub('도로명|복사', '', address.text)
        if address:
            print("도로명 주소:", address)
        else:
            print("도로명 없음")

        distance = driver.find_element_by_css_selector(f"#_list_scroll_container > div > div > div:nth-child(2) > ul > li:nth-child({i+1}) > div > div > div > div > span.Q8Zql.M_ePl").text
        if "." in distance:
            print("거리 초과")
            break
        print("문자형 거리:", distance, "---")
        distance = int(distance[:-1])
        if distance > 500:
            print("거리 초과")
            break
        print("거리(m): ", distance)
        # add = driver.find_element_by_css_selector('#_list_scroll_container > div > div > div:nth-child(2) > ul > li > div> div> div > div > div > div:nth-child(1)')
        # add = re.sub('도로명|복사', '', add.text)

    driver.find_element_by_tag_name('body').send_keys(Keys.DOWN)
    time.sleep(0.1)
    driver.find_element_by_tag_name('body').send_keys(Keys.DOWN)
    time.sleep(0.1)
    driver.find_element_by_tag_name('body').send_keys(Keys.DOWN)
    time.sleep(0.1)
    driver.find_element_by_tag_name('body').send_keys(Keys.DOWN)
    time.sleep(0.1)
    if i%4 == 0:
        driver.find_element_by_tag_name('body').send_keys(Keys.DOWN)
        time.sleep(0.1)
    if i%50 == 0:
        driver.find_element_by_tag_name('body').send_keys(Keys.DOWN)
        time.sleep(0.1)
        driver.find_element_by_tag_name('body').send_keys(Keys.DOWN)
        time.sleep(0.1)
    if i%100 == 0:
        driver.find_element_by_tag_name('body').send_keys(Keys.DOWN)
        time.sleep(0.1)
    i += 1
    print('횟수: ', i)

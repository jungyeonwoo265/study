from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import csv
import time

# 매장 검색어
add_list = ['서울특별시', '경기도', '인천광역시', '강원도', '광주광역시', '대전광역시',
            '대구광역시', '부산광역시', '충청북도', '충청남도', '전라남도', '전라북도',
            '경상북도', '경상남도', '제주특별자치도', '세종특별자치시', '울산광역시',
            '서울', '경기', '인천', '강원', '광주', '대전', '대구', '부산', '울산'
            , '세종', '경남', '경북', '전남', '전북', '충남', '충북', '제주']

# 메가커피 메장찾기 페이지 이동
driver = webdriver.Chrome("C:/Users/Kiot/PycharmProjects/chromedriver_win32/chromedriver.exe")
driver.implicitly_wait(3)
driver.get("https://www.mega-mgccoffee.com/store/find/")
time.sleep(2)

# 저장할 CSV파일 생성
f = open('megacafe.csv', 'w', newline='')
f.close()

# 매장찾기 검색창 선정
search = driver.find_element_by_css_selector('#store_search')

name_list = []
addre_list = []

for i in add_list:
    # 검색창안의 검색어 지우기
    search.clear()
    time.sleep(0.2)
    # 검색창에 검색어 입력
    search.send_keys(i)
    search.send_keys(Keys.ENTER)
    time.sleep(2)

    # 검색어로 불러와진 지점 정보 저장
    names = driver.find_elements_by_css_selector('#store_search_list > li > a > div > div > b')
    address = driver.find_elements_by_css_selector('#store_search_list > li > a > div > div.cont_text_inner.cont_text_info')
    # 검색정보 매칭 확인
    if len(names) == len(address):
        for j in range(len(names)):
            # 주소에서 쓸모 없는 자료 제거를 위해 split 사용
            # addre = address[j].text
            addre = address[j].text.split(',')[0]
            # 구 주소 제거
            addre = addre.split("(")[0]
            name = names[j].text
            # 주소에서 "-"의 수량을 확인
            count = addre.count('-')
            # "-"가 2개 이상인 경우(전화번호가 있는경우)
            if count > 1:
                # 주소를 뒤어서 부터 1글자씩 확인
                for k in range(len(addre)):
                    wored = addre[-(k+1)]
                    # 공백 문자가 나오면 문자열 슬라이싱으로 전화번호 제거
                    if wored == ' ':
                        addre = addre[:-(k+1)]
                        break
            # 주소를 조건으로 중복된 검색자료 거르기
            if addre not in addre_list:
                print(count, name, addre)
                name_list.append(name)
                addre_list.append(addre)

                result = []
                mega = [names[j].text, addre]
                result.append(mega)
                f = open('megacafe.csv', 'a', newline='')
                wr = csv.writer(f)
                wr.writerows(result)
                f.close()
    else:
        print('길이 다름')
print("지점: ", len(name_list), "주소: ", len(addre_list))

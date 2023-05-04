import time, random, re
import requests
from bs4 import BeautifulSoup
import pymysql


def apt_juso(keyword):
    ## 주소 추출하기
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    }
    url = f'https://www.juso.go.kr/support/AddressMainSearch.do?currentPage=1&countPerPage=10&&searchType=\
    TOTAL&searchKeyword={keyword}&firstSort=none&ablYn=Y&synnYn=N'

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    roed_juso = soup.find('div', class_='subejct_1').find('span', class_='roadNameText').text
    road = re.sub('&nbsp;|\t|\r|\n', '', roed_juso).strip().replace('  ', ' ')
    print(road)

    jibeon_juso = soup.find('div', class_='subejct_2').find('span', class_='roadNameText').text
    jibeon = re.sub('&nbsp;|\t|\r|\n', '', jibeon_juso).strip().replace('  ', ' ')
    print(jibeon)

    time.sleep(random.uniform(0.5, 1))
    return jibeon


conn = pymysql.connect(host='10.10.21.105', user='network', password='aaaa', db='franchise', port=3306, charset='utf8')
cur = conn.cursor()
cur.execute("SELECT road_addr, ji_addr FROM `daegu_element` where ji_addr=is Null;")
row = cur.fetchall()
print(row)
for i in range(len(row)):
    if row[i][1] == ():
        try:
            juso_keyword = row[i][0]
            change = apt_juso(juso_keyword)
            cur.execute(f"update `j_parking_info(ok)` set ji_addr='{change}' where road_addr = '{juso_keyword}'")
        except AttributeError as e:
            print(e)
# conn.commit()
conn.close()
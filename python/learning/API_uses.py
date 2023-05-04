import requests
import xmltodict as xmltodict
import math
import time

content = []

start_time = time.time()
key = 'cbbbb410eb3d4bfa88e79a9172862f'
url = f'http://www.incheon.go.kr/dp/openapi/data?apicode=10&page=1&key={key}'
data_total = int(xmltodict.parse(requests.get(url).content)['data']['totalCount'])
total_page = math.ceil(data_total/10)
for page in range(1, total_page+1):
    url = f'http://www.incheon.go.kr/dp/openapi/data?apicode=10&page={page}&key={key}'
    content = requests.get(url).content
    dict = xmltodict.parse(content)
    data = dict['data']
    date_item = data['list']['item']
    for value in date_item:
        data_listnum = value['listNum']
        data_year = value['histYear']
        data_month = value['histDate'][0]+value['histDate'][1]
        data_day=value['histDate'][2]+value['histDate'][3]
        date_summary = value['summary']
        print(f'등록 NO: {data_listnum}, '
              f'년월일: {data_year}년 {data_month}월 {data_day}일, '
              f'내용: {date_summary}')

end_time = time.time()
print('실행시간: ', end_time - start_time, '초')

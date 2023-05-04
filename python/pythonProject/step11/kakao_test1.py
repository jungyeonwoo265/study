import requests
import pymysql
import time


# 검색 위치를 중심으로 num_x,num_y로 지정한 수로 나누어 검색을 진행하는 코드
def overlapped_data(keyword, start_x, start_y, next_x, next_y, num_x, num_y):
    overlapped_result = []

    # num_x 만큼 x축(경도) 검색 범위를 나눈다.
    for i in range(1, num_x+1):
        end_x = start_x + next_x
        init_start_y = start_y
        #  num_y 만큼 y축(위도) 검색 범위를 나눈다.
        for j in range(1, num_y+1):
            end_y = init_start_y + next_y
            # api 1회 받는 개수 45개의 제한을 해결 하기위한 함수 사용
            each_result = whole_region(keyword, start_x, init_start_y, end_x, end_y)
            # 검색 결과를 저장
            overlapped_result.extend(each_result)
            init_start_y = end_y
        start_x = end_x

    return overlapped_result


#  API 1회 다운 개수 45개 제한을 해결하기 위한 함수
def whole_region(keyword, start_x, start_y, end_x, end_y):
    # print(start_x, start_y, end_x, end_y)
    page_num = 1
    all_data_list = []

    while True:
        # 카카오 API 접속
        url = "https://dapi.kakao.com/v2/local/search/category.json"
        # 검색 조건 설정
        params = {'category_group_code': keyword, 'page': page_num,
                  'rect': f'{start_x},{start_y},{end_x},{end_y}'}
        # REST API 키 등록
        headers = {"Authorization": "KakaoAK 325a909d711a84d1ae24f0d331d5d066"}
        # 검색
        resp = requests.get(url, params=params, headers=headers)
        # 검색 수량 확인
        try:
            search_count = resp.json()['meta']['total_count']
        except KeyError:
            print('카카오API 다운로드 용량 제한')
            time.sleep(79200)
            continue

        # 검색 수량이 45개 초과인 경우
        if search_count > 45:
            # 검색 범위를 4등분 하여 다시 검색
            dividing_x = (start_x + end_x)/2
            dividing_y = (start_y + end_y)/2
            all_data_list.extend(whole_region(keyword, start_x, start_y, dividing_x, dividing_y))
            all_data_list.extend(whole_region(keyword, dividing_x, start_y, end_x, dividing_y))
            all_data_list.extend(whole_region(keyword, start_x, dividing_y, dividing_x, end_y))
            all_data_list.extend(whole_region(keyword, dividing_x, dividing_y, end_x, end_y))
            return all_data_list
        # 검색 수량이 45 이하인 경우
        else:
            # 검색 결과가 있는경우
            if resp.json()['meta']['is_end']:
                all_data_list.extend(resp.json()['documents'])
                return all_data_list
            # 검색 결과가 없는 경우
            else:
                page_num += 1
                all_data_list.extend(resp.json()['documents'])

# DB 에서 메가커피 지점명,위도,경도 받아오기
conn = pymysql.connect(host='10.10.21.105', port=3306, user='network', password='aaaa', db='franchise')
c = conn.cursor()
c.execute(f"select store,longitude,Latitude from mega_add;")
temp_db = c.fetchall()
conn.close()

stime = time.time()
# for n in range(10):
for n in range(1637, len(temp_db)):
    result = []
    print(f'-----------------{temp_db[n][0]}--------------------')
    # 1km = 위도,경도 차 약 0.011 이다.
    start_x = float(temp_db[n][1]) - 0.0055
    start_y = float(temp_db[n][2]) - 0.0055
    # 검색 범위를 11X11로 나누겠다.
    num_x = 11
    num_y = 11
    # 검색범위를 나눈 만큼 위도 경도 0.001X0.001(약 90m X 90m) 단위로 검색
    # 검색 범위 11x0.001 = 0.011 = 약1km
    next_x = 0.001
    next_y = 0.001
    # category_group_code
    a_list = ['CE7']
    # a_list 의 내역 검색
    for x in a_list:
        # 범위 검색
        overlapped_result = overlapped_data(x, start_x, start_y, next_x, next_y, num_x, num_y)
        # 검색 결과 list에 저장
        for i in overlapped_result:
            temp = [temp_db[n][0], i['place_name'], i['road_address_name']]
            # print(temp)
            result.append(temp)
    print('검색수: ', len(result))
    print('검색 지점:', n, '/', len(temp_db))
    for info in result:
        c.execute(f"insert into mega_around_cafe values ('{info[0]}', '{info[1]}', '{info[2]}');")
        conn.commit()
    print('DB 저장')
    etime = time.time()
    print(f"경과 시간 {etime-stime:.2f}")

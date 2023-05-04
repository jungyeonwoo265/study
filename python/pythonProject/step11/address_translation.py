import csv
import requests
import pymysql
f = open('megacafe.csv', 'r', encoding='utf-8')
mega_list=[]
rdr = csv.reader(f)
for line in rdr:
    mega_list.append(line)
f.close()
for i in range(len(mega_list)):
    result = ""
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + f"{mega_list[i][1]}"  # 카카오 api 서버스를 이용하여 접근
    rest_api_key = ''  # 사용자 api key
    header = {'Authorization': 'KakaoAK ' + rest_api_key}
    r = requests.get(url, headers=header)
    conn = pymysql.connect(host='10.10.21.105', user='network', password='aaaa', db='franchise')
    cur = conn.cursor()
    if r.status_code == 200:  # 정보를 오류없이 받아왔다면
        if len(r.json()['documents']) != 0:  # 길이가 0이 아니라면
            try:
                result_address = r.json()["documents"][0]["address"]
                result = (result_address["y"], result_address["x"])  # 좌표 정보에 접근
                # print(mega_list)
                print(f"======================================='{mega_list[i][0]}', '{mega_list[i][1]}', '{result[0]}', '{result[1]}'")
                cur.execute(f"insert into mega_add(store, store_add, Latitude, longitude) values ('{mega_list[i][0]}', '{mega_list[i][1]}', '{result[0]}', '{result[1]}')")
                conn.commit()
            except:
                print("==========================================정보없음=============")
                print(f"======================================'{mega_list[i][0]}', '{mega_list[i][1]}', 'None', 'None'")
                cur.execute(f"insert into mega_add(store, store_add, Latitude, longitude) values ('{mega_list[i][0]}', '{mega_list[i][1]}', 'None', 'None')")
                conn.commit()
        else:
            print("==========================================엥왜안됨?1111=============")
            print(
                f"======================================'{mega_list[i][0]}', '{mega_list[i][1]}', 'None', 'None'")
            cur.execute(
                f"insert into mega_add(store, store_add, Latitude, longitude) values ('{mega_list[i][0]}', '{mega_list[i][1]}', 'None', 'None')")
            conn.commit()

    else:
        print("=====================엥왜안됨?2222========")
        cur.execute(
            f"insert into mega_add(store, store_add, Latitude, longitude) values ('{mega_list[i][0]}', '{mega_list[i][1]}', 'None', 'None')")
        conn.commit()




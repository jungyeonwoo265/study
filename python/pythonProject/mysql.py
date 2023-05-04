import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', password='0000', charset='utf8') #DB 연결
cur = conn.cursor() #디폴트 커서 생성

sql ='CREATE DATABASE kobis;'
cur.execute(sql)
conn.commit()

conn.close() #연결 닫기

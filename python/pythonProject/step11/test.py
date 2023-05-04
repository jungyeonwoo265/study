import pymysql
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib
import platform

conn = pymysql.connect(host='10.10.21.105', port=3306, user='network', password='aaaa', db='franchise')
c = conn.cursor()

c.execute(f"select max(cafes) , max(banks) from (select store, count(bank) as banks from mega_around_bank group by store) as a left join (select store, count(cafe_name) as cafes from mega_around_cafe group by store) as b on a.store = b.store;")
max_store = c.fetchone()

c.execute(f"select a.store, ifnull(cafes,0) , ifnull(banks,0) from (SELECT store FROM mega_add where store_add like '서울%') as a left join (select a.store, cafes , banks from (select store, count(bank) as banks from mega_around_bank group by store) as a left join (select store, count(cafe_name) as cafes from mega_around_cafe group by store) as b on a.store = b.store) as b on a.store = b.store;")
store_nums = c.fetchall()

conn.close()

# Window
if platform.system() == 'Windows':
    matplotlib.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin': # Mac
    matplotlib.rc('font', family='AppleGothic')
else: #linux
    matplotlib.rc('font', family='NanumGothic')

# 그래프에 마이너스 표시가 되도록 변경
matplotlib.rcParams['axes.unicode_minus'] = False

max_cafe = (max_store[0]//100 + 1) * 100
max_bank = (max_store[1]//100 + 1) * 100

store = []
cafe = []
bank = []
nums = []

for i in store_nums:
    cafe_ratio = i[1]/max_cafe
    bank_ratio = i[2]/max_bank
    if cafe_ratio <= 0.7 and cafe_ratio > 0.1 and bank_ratio <= 0.3 and bank_ratio > 0.2:
        store.append(i[0])
        cafe.append(cafe_ratio)
        bank.append(bank_ratio)

df = pd.DataFrame({'cafe': cafe, 'bank': bank}, index=store)

fig, ax = plt.subplots(figsize=(19, 9))
bar_width = 0.25

index = np.arange(len(store))

b1 = plt.bar(index, df['cafe'], bar_width, alpha=0.4, color='red', label='cafe')
b2 = plt.bar(index + bar_width, df['bank'], bar_width, alpha=0.4, color='blue', label='bank')

# x축 위치를 정 가운데로 조정하고 x축의 텍스트를 year 정보와 매칭
plt.xticks(np.arange(bar_width, len(store) + bar_width, 1), store)

plt.xlabel('store', size=13)
plt.ylabel('nums', size=13)
plt.legend()
plt.show()

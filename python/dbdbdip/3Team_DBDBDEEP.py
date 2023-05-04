import pymysql as p
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager, rc
import pandas as pd

form_class = uic.loadUiType("inquiry.ui")[0]


class check(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('초등학교 인원')
        # DB 연결
        self.conn = p.connect(host='localhost', port=3306, user='root', password='00000000',
                              db='3teamnew', charset='utf8')
        self.c = self.conn.cursor()
        font_path = "c:\windows\Fonts\gulim.ttc"
        font = font_manager.FontProperties(fname=font_path).get_name()
        rc('font', family=font)
        # self.research_btn.clicked.connect(self.research)
        self.table.doubleClicked.connect(self.update)
        self.add_btn.clicked.connect(self.add_col)
        self.back_btn.clicked.connect(self.back)
        self.delete_btn.clicked.connect(self.delete_sel)
        self.stick_btn.clicked.connect(self.stick)
        # 연우형거 취합하는중
        self.csv = list()
        self.db = 'elementary'
        self.header = '*'
        self.where = ''
        self.join = ''
        self.table_header1()
        self.title = self.checkBox.text()
        self.research_btn.clicked.connect(self.search)
        self.checkBox.stateChanged.connect(self.choice_db)
        self.checkBox_2.stateChanged.connect(self.choice_db)
        self.checkBox_3.stateChanged.connect(self.choice_db)
        self.btn_graph.clicked.connect(self.graph)
        self.btn_graph_line.clicked.connect(self.graph2)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def delete_sel(self):
        year_list = ['', '2016', '2017', '2018', '2019', '2020', '2021']
        if len(self.csv_list) > 1:
            self.ro = self.table.currentIndex().row() + 1
            self.col = self.table.currentIndex().column()
        else:
            self.ro = self.table.currentIndex().row()
            self.col = self.table.currentIndex().column()
        self.c.execute("set SQL_SAFE_UPDATES = 0")
        year = self.combo_year.currentText()
        if year == "선택안함":
            self.c.execute(
                f'update elementary set {year_list[self.col]}년 = "-" WHERE 행정구역별 ="{self.csv_list[self.ro][0]}"')
        else:
            self.c.execute(f'update elementary set {year}년 = "-" WHERE 행정구역별 ="{self.csv_list[self.ro][0]}"')
        self.c.execute("set SQL_SAFE_UPDATES = 1")
        self.conn.commit()

    def back(self):
        self.c.execute('ALTER TABLE elementary DROP COLUMN `2021년`')
        self.conn.commit()

    def add_col(self):
        self.c.execute('select * from elementary')
        temp_list = self.c.fetchone()
        if len(temp_list) < 7:
            self.c.execute('ALTER TABLE elementary ADD COLUMN `2021년` TEXT NULL DEFAULT NULL AFTER `2020년`')
            self.c.execute('update elementary set 2021년=case WHEN 행정구역별="행정구역별" THEN 2021 WHEN 행정구역별="전국" \
                    THEN "2672340" WHEN 행정구역별="서울특별시" THEN "399435" WHEN 행정구역별="부산광역시" THEN "153921" WHEN 행정구역별="대구광역시" \
                    THEN "121308" WHEN 행정구역별="인천광역시" THEN "155271" WHEN 행정구역별="광주광역시" THEN "84998" WHEN 행정구역별="대전광역시" \
                    THEN "77884" WHEN 행정구역별="울산광역시" THEN "66919" WHEN 행정구역별="세종특별자치시" THEN "30726" WHEN 행정구역별="경기도" \
                    THEN "763912"  WHEN 행정구역별="강원도" THEN "72373" WHEN 행정구역별="충청북도" THEN "84263" WHEN 행정구역별="충청남도" \
                    THEN "118771" WHEN 행정구역별="전라북도" THEN "92914" WHEN 행정구역별="전라남도" THEN "91229" WHEN 행정구역별="경상북도" \
                    THEN "127912" WHEN 행정구역별="경상남도" THEN "189176"  WHEN 행정구역별="제주특별자치도" THEN "41328"  END')
        self.conn.commit()

    def update(self):
        year_list = ['', '2016', '2017', '2018', '2019', '2020', '2021']
        if len(self.csv_list) > 1:
            self.ro = self.table.currentIndex().row() + 1
            self.col = self.table.currentIndex().column()
        else:
            self.ro = self.table.currentIndex().row()
            self.col = self.table.currentIndex().column()
        sung = self.liner.text()
        # year=['2016년','2017년','2018년','2019년','2020년']
        self.c.execute("set SQL_SAFE_UPDATES = 0")
        year = self.combo_year.currentText()
        if year == "선택안함":
            self.c.execute(
                f'update elementary set {year_list[self.col]}년 = "{sung}" WHERE 행정구역별 ="{self.csv_list[self.ro][0]}"')
        else:
            self.c.execute(f'update elementary set {year}년 = "{sung}" WHERE 행정구역별 ="{self.csv_list[self.ro][0]}"')
        self.c.execute("set SQL_SAFE_UPDATES = 1")
        self.conn.commit()

    def stick(self):

        self.c.execute('SELECT * FROM elementary_ratio')
        self.ele = self.c.fetchall()

        self.c.execute('SELECT * FROM new_marry_ratio')
        self.couple = self.c.fetchall()

        self.c.execute('SELECT * FROM solo')
        self.individual = self.c.fetchall()
        area = []
        # 비율
        percent = []
        for i in range(1, 19):
            h = self.ele[i][0]
            k = self.ele[i][1]
            area.append(h)
            percent.append(k)

        percent_two = []
        for i in range(1, 19):
            co1 = self.couple[i][1]
            percent_two.append(co1)

        percent_three = []
        for i in range(1, 19):
            indi1 = self.individual[i][1]
            percent_three.append(indi1)
        plt.rc('font', size=6)
        plt.figure(figsize=(15, 12))
        conv_list1 = list(map(float, percent))
        conv_list2 = list(map(float, percent_two))
        conv_list3 = list(map(float, percent_three))
        df = pd.DataFrame({'초등학생 비율': conv_list1, '혼인율': conv_list2, '1인가구 비율': conv_list3}, index=area)
        bar_width = 0.2
        index = np.arange(18)
        b1 = plt.bar(index, df['초등학생 비율'], bar_width, alpha=0.4, color='b', label='초등학생 비율')
        b2 = plt.bar(index + bar_width, df['혼인율'], bar_width, alpha=0.4, color='g', label='혼인율')
        b3 = plt.bar(index + 2 * bar_width, df['1인가구 비율'] / 4, bar_width, alpha=0.4, color='r', label='1인가구 비율')

        plt.xticks(np.arange(bar_width, len(area) + bar_width, 1), area)
        plt.xlabel('지역', size=10)
        plt.ylabel('인구수별 비율', size=10)
        plt.legend()
        plt.show()

    def search(self):
        if type(self.db) == str:
            self.condition1()
            self.single_search()
        else:
            self.condition2()
            self.multi_search()

    def condition1(self):
        city = self.combo_nation.currentText()
        year = self.combo_year.currentText()
        if city == '선택안함' and year == '선택안함':
            self.header = '*'
            self.join = ''
            self.where = ''
        elif year == '선택안함':
            self.header = '*'
            self.join = ''
            self.where = f'where 행정구역별 = "{city}"'
        elif city == '선택안함':
            self.header = f'행정구역별 , {year}년'
            self.join = ''
            self.where = ''
        else:
            self.header = f'행정구역별 , {year}년'
            self.join = ''
            self.where = f'where 행정구역별 = "{city}"'
        self.table_header1()

    def single_search(self):
        self.c.execute(f'select {self.header} from {self.db} {self.where};')
        self.table_show()

    def condition2(self):
        city = self.combo_nation.currentText()
        year = self.combo_year.currentText()
        # 2개
        # select / a.행정구역별, a.2016년, b.2016년 / from elementary as a
        # / inner join new_marry as b on a.행정구역별 = b.행정구역별 / where a.행정구역별 ='경기도';

        if len(self.db) == 2:
            if city == '선택안함':
                self.header = f'{self.db[0]}.행정구역별, {self.db[0]}.{year}년, {self.db[1]}.{year}년'
                self.join = f'inner join {self.db[1]} on {self.db[0]}.행정구역별 = {self.db[1]}.행정구역별'
                self.where = f''
            else:
                self.header = f'{self.db[0]}.행정구역별, {self.db[0]}.{year}년, {self.db[1]}.{year}년'
                self.join = f'inner join {self.db[1]} on {self.db[0]}.행정구역별 = {self.db[1]}.행정구역별'
                self.where = f'where {self.db[1]}.행정구역별 = "{city}"'

        # 3개
        # select / a.행정구역별, a.2016년, b.2016년, c.2016년 / from elementary as a
        # / inner join new_marry as b on a.행정구역별 = b.행정구역별
        # inner join solo as c on b.행정구역별 = c.행정구역별 / where a.행정구역별 ='경기도';

        else:
            if city == '선택안함':
                self.header = f'{self.db[0]}.행정구역별, {self.db[0]}.{year}년, {self.db[1]}.{year}년, {self.db[2]}.{year}년'
                self.join = f'inner join {self.db[1]} on {self.db[0]}.행정구역별 = {self.db[1]}.행정구역별 ' \
                            f'inner join {self.db[2]} on {self.db[1]}.행정구역별 = {self.db[2]}.행정구역별'
                self.where = f''
            else:
                self.header = f'{self.db[0]}.행정구역별, {self.db[0]}.{year}년, {self.db[1]}.{year}년, {self.db[2]}.{year}년'
                self.join = f'inner join {self.db[1]} on {self.db[0]}.행정구역별 = {self.db[1]}.행정구역별 ' \
                            f'inner join {self.db[2]} on {self.db[1]}.행정구역별 = {self.db[2]}.행정구역별'
                self.where = f'where {self.db[1]}.행정구역별 = "{city}"'
        self.table_header2()

    def multi_search(self):
        self.c.execute(f'select {self.header} from {self.db[0]} {self.join} {self.where};')
        self.table_show()

    def table_show(self):
        csv_list = self.c.fetchall()
        city = self.combo_nation.currentText()
        if city == '선택안함':
            self.table.setRowCount(len(csv_list) - 1)
            self.table.setColumnCount(len(csv_list[0]))
            for i in range(len(csv_list) - 1):
                for j in range(len(csv_list[0])):
                    try:
                        self.table.setItem(i, j, QTableWidgetItem(f'{int(csv_list[i + 1][j]): ,}'))
                    except ValueError:
                        self.table.setItem(i, j, QTableWidgetItem(csv_list[i + 1][j]))
        else:
            self.table.setRowCount(len(csv_list))
            self.table.setColumnCount(len(csv_list[0]))
            for i in range(len(csv_list)):
                for j in range(len(csv_list[0])):
                    try:
                        self.table.setItem(i, j, QTableWidgetItem(f'{int(csv_list[i][j]): ,}'))
                    except ValueError:
                        self.table.setItem(i, j, QTableWidgetItem(csv_list[i][j]))

        for i in range(len(csv_list[0])):
            try:
                self.table.setHorizontalHeaderItem(i, QTableWidgetItem(f'{int(self.csv[0][i])}년'))
            except ValueError:
                self.table.setHorizontalHeaderItem(i, QTableWidgetItem(self.csv[0][i]))

    def table_header1(self):
        self.c.execute(f'select {self.header} from {self.db};')
        self.csv = self.c.fetchall()

    def table_header2(self):
        self.c.execute(f'select {self.header} from {self.db[0]} {self.join};')
        self.csv = self.c.fetchall()

    ## 추가한부분
    # 그래프 생성을 위하여 gui의 체크박스의 상태에 따라 어떤 DB를 선택할 것인자 선택해주는 메서드
    def choice_graphdb(self):
        box1 = self.checkBox.isChecked()
        box2 = self.checkBox_2.isChecked()
        box3 = self.checkBox_3.isChecked()
        if box1 and box2 and box3:
            self.graphdb = []
            self.graphdb.append('elementary_ratio')
            self.graphdb.append('new_marry_ratio')
            self.graphdb.append('solo')
            if self.combo_year.itemText(0) == '선택안함':
                self.combo_year.removeItem(0)
        elif box1 and box2:
            self.graphdb = []
            self.graphdb.append('elementary_ratio')
            self.graphdb.append('solo')
            self.graphname1 = "초등학생수 비율"
            self.graphname2 = "1인 가구 수 비율"
            if self.combo_year.itemText(0) == '선택안함':
                self.combo_year.removeItem(0)
        elif box1 and box3:
            self.graphdb = []
            self.graphdb.append('elementary_ratio')
            self.graphdb.append('new_marry_ratio')
            self.graphname1 = "초등학생수 비율"
            self.graphname2 = "신혼부부 수 비율"
            if self.combo_year.itemText(0) == '선택안함':
                self.combo_year.removeItem(0)
        elif box2 and box3:
            self.graphdb = []
            self.graphdb.append('new_marry_ratio')
            self.graphdb.append('solo')
            self.graphname1 = "신혼부부 수 비율"
            self.graphname2 = "1인가구 수 비율"
            if self.combo_year.itemText(0) == '선택안함':
                self.combo_year.removeItem(0)
        elif self.checkBox.isChecked():
            self.db = 'elementary'
            self.graphdb = 'elementary_ratio'
            self.title = self.checkBox.text()
            if self.combo_year.itemText(0) != '선택안함':
                self.combo_year.insertItem(0, '선택안함')
        elif self.checkBox_2.isChecked():
            self.db = 'solo'
            self.graphdb = 'solo'
            self.title = self.checkBox_2.text()
            if self.combo_year.itemText(0) != '선택안함':
                self.combo_year.insertItem(0, '선택안함')
        elif self.checkBox_3.isChecked():
            self.db = 'new_marry'
            self.graphdb = 'new_marry_ratio'
            self.title = self.checkBox_3.text()
            if self.combo_year.itemText(0) != '선택안함':
                self.combo_year.insertItem(0, '선택안함')
        else:
            self.checkBox.toggle()
            self.db = 'elementary'
            self.graphdb = 'elementary_ratio'
            self.title = self.checkBox.text()
            if self.combo_year.itemText(0) != '선택안함':
                self.combo_year.insertItem(0, '선택안함')

    def choice_db(self):
        box1 = self.checkBox.isChecked()
        box2 = self.checkBox_2.isChecked()
        box3 = self.checkBox_3.isChecked()
        if box1 and box2 and box3:
            self.db = list()
            self.title = list()
            self.db.append('elementary')
            self.db.append('solo')
            self.db.append('new_marry')
            self.title.append(self.checkBox.text())
            self.title.append(self.checkBox_2.text())
            self.title.append(self.checkBox_3.text())
            if self.combo_year.itemText(0) == '선택안함':
                self.combo_year.removeItem(0)
        elif box1 and box2:
            self.db = list()
            self.title = list()
            self.db.append('elementary')
            self.db.append('solo')
            self.title.append(self.checkBox.text())
            self.title.append(self.checkBox_2.text())
            if self.combo_year.itemText(0) == '선택안함':
                self.combo_year.removeItem(0)
        elif box1 and box3:
            self.db = list()
            self.title = list()
            self.db.append('elementary')
            self.db.append('new_marry')
            self.title.append(self.checkBox.text())
            self.title.append(self.checkBox_3.text())
            if self.combo_year.itemText(0) == '선택안함':
                self.combo_year.removeItem(0)
        elif box2 and box3:
            self.db = list()
            self.title = list()
            self.db.append('solo')
            self.db.append('new_marry')
            self.title.append(self.checkBox_2.text())
            self.title.append(self.checkBox_3.text())
            if self.combo_year.itemText(0) == '선택안함':
                self.combo_year.removeItem(0)
        elif self.checkBox.isChecked():
            self.db = str
            self.title = str
            self.db = 'elementary'
            self.title = self.checkBox.text()
            if self.combo_year.itemText(0) != '선택안함':
                self.combo_year.insertItem(0, '선택안함')
        elif self.checkBox_2.isChecked():
            self.db = str
            self.title = str
            self.db = 'solo'
            self.title = self.checkBox_2.text()
            if self.combo_year.itemText(0) != '선택안함':
                self.combo_year.insertItem(0, '선택안함')
        elif self.checkBox_3.isChecked():
            self.db = str
            self.title = str
            self.db = 'new_marry'
            self.title = self.checkBox_3.text()
            if self.combo_year.itemText(0) != '선택안함':
                self.combo_year.insertItem(0, '선택안함')
        else:
            self.db = str
            self.title = str
            self.db = 'elementary'
            self.title = self.checkBox.text()
            if self.combo_year.itemText(0) != '선택안함':
                self.combo_year.insertItem(0, '선택안함')

    def graph(self):
        self.choice_db()
        year = self.combo_year.currentText()
        label_city = list()
        label_value = list()
        label_value2 = list()
        label_value3 = list()
        wedgeprops = {'width': 0.7, 'edgecolor': 'w', 'linewidth': 2}
        if type(self.db) == str:
            if year == '선택안함':
                year = 2016
            if self.db == 'solo':
                self.db = 'solo_num'
            self.c.execute(f'select 행정구역별, {year}년 from {self.db}')
            num_list = self.c.fetchall()
            for i in range(len(num_list)):
                if i > 1:
                    label_city.append(num_list[i][0])
            for i in range(len(num_list)):
                if i > 1:
                    label_value.append(num_list[i][1])
            plt.pie(label_value, labels=label_city, autopct='%.1f%%', startangle=90,
                    counterclock=False, wedgeprops=wedgeprops)
            plt.title(f'{self.title} ({year}년)')
            plt.show()

        else:
            if 'solo' in self.db:
                self.db[self.db.index('solo')] = 'solo_num'
            self.condition2()
            self.c.execute(f'select {self.header} from {self.db[0]} {self.join}')
            num_list = self.c.fetchall()
            for i in range(len(num_list)):
                if i > 1:
                    label_city.append(num_list[i][0])
            for i in range(len(num_list)):
                if i > 1:
                    label_value.append(num_list[i][1])
            for i in range(len(num_list)):
                if i > 1:
                    label_value2.append(num_list[i][2])
            label_list = [label_value, label_value2]

            if len(self.db) == 3:
                for i in range(len(num_list)):
                    if i > 1:
                        label_value3.append(num_list[i][3])
                label_list.append(label_value3)

            plt.figure(figsize=(19, 9.5))
            for i in range(len(label_list)):
                plt.subplot(1, len(label_list), i + 1)
                plt.pie(label_list[i], labels=label_city, autopct='%.1f%%', startangle=90,
                        counterclock=False, wedgeprops=wedgeprops)
                plt.title(f'{self.title[i]} ({year}년)')
            plt.show()

    ## 추가한 부분
    def graph2(self):
        self.choice_graphdb()
        city = self.combo_nation.currentText()
        year = self.combo_year.currentText()
        label_year = list()
        label_people = list()
        graphlist1 = []
        graphlist2 = []
        graphlist3 = []
        if city == '선택안함':
            city = '전국'
        if type(self.db) == str:
            self.c.execute(f'select * from {self.graphdb} where 행정구역별 = "{city}"')
            num_list = self.c.fetchall()
            for i in range(len(num_list[0])):
                if i != 0:
                    label_people.append(num_list[0][i])
            x = ['2016년', '2017년', '2018년', '2019년', '2020년']
            plt.plot(x, label_people, 'r')
            plt.title(f'{self.title} ({city})')
            plt.show()

        elif len(self.graphdb) == 2:
            self.header = f'{self.graphdb[0]}.행정구역별, {self.graphdb[0]}.{year}년, {self.graphdb[1]}.{year}년'
            self.join = f'inner join {self.graphdb[1]} AS B on A.행정구역별 = B.행정구역별'
            self.where = f'where A.행정구역별 = "{city}"'
            self.c.execute(f'select A.*,B.2016년,B.2017년,B.2018년,B.2019년,B.2020년 \
                                    from {self.graphdb[0]} AS A {self.join} {self.where};')
            graphlist = self.c.fetchall()
            for i in range(len(graphlist[0])):
                if i >= 1 and i < 6:
                    graphlist1.append(graphlist[0][i])
                elif i >= 6:
                    graphlist2.append(graphlist[0][i])
            conv_list1 = list(map(float, graphlist1))
            conv_list2 = list(map(float, graphlist2))

            x = ['2016년', '2017년', '2018년', '2019년', '2020년']
            fig = plt.figure(figsize=(12, 5))
            ax = fig.add_subplot(111)
            ax.plot(x, conv_list1, 'r', label=f"{self.graphname1}")
            plt.legend(loc='center left')
            plt.ylim([int(min(conv_list1) - 1), int(max(conv_list1) + 1)])
            for i, v in enumerate(x):
                plt.text(v, conv_list1[i], conv_list1[i],  # 좌표 (x축 = v, y축 = y[0]..y[1], 표시 = y[0]..y[1])
                         fontsize=9,
                         color='blue',
                         horizontalalignment='center',  # horizontalalignment (left, center, right)
                         verticalalignment='bottom')  # verticalalignment (top, center, bottom)
            ax2 = ax.twinx()
            ax2.plot(x, conv_list2, 'b', label=f"{self.graphname2}")
            plt.ylim([int(min(conv_list2) - 1), int(max(conv_list2) + 1)])
            for i, v in enumerate(x):
                plt.text(v, conv_list2[i], conv_list2[i],  # 좌표 (x축 = v, y축 = y[0]..y[1], 표시 = y[0]..y[1])
                         fontsize=9,
                         color='black',
                         horizontalalignment='center',  # horizontalalignment (left, center, right)
                         verticalalignment='bottom')  # verticalalignment (top, center, bottom)
            plt.legend(loc='right')
            plt.title(f"{city}")
            plt.show()
        else:
            self.join = f'inner join {self.graphdb[1]} AS B on A.행정구역별 = B.행정구역별 ' \
                        f'inner join {self.graphdb[2]} AS C on B.행정구역별 = C.행정구역별'
            self.where = f'where A.행정구역별 = "{city}"'
            self.c.execute(f'select A.*,B.2016년,B.2017년,B.2018년,B.2019년,B.2020년 \
                                   ,C.2016년,C.2017년,C.2018년,C.2019년,C.2020년\
                                    from {self.graphdb[0]} AS A {self.join} {self.where};')
            graphlist = self.c.fetchall()
            for i in range(len(graphlist[0])):
                if i >= 1 and i < 6:
                    graphlist1.append(graphlist[0][i])
                elif i >= 6 and i < 11:
                    graphlist2.append(graphlist[0][i])
                elif i >= 11:
                    graphlist3.append(graphlist[0][i])
            conv_list1 = list(map(float, graphlist1))  # 초등생
            conv_list2 = list(map(float, graphlist2))  # 신혼부부
            conv_list3 = list(map(float, graphlist3))  # 1인가구수
            x = ['2016년', '2017년', '2018년', '2019년', '2020년']
            fig = plt.figure(figsize=(12, 5))
            ax = fig.add_subplot(111)

            ax.plot(x, conv_list1, 'r', label="초등학생 비율")
            for i, v in enumerate(x):
                plt.text(v, conv_list1[i], conv_list1[i],  # 좌표 (x축 = v, y축 = y[0]..y[1], 표시 = y[0]..y[1])
                         fontsize=9,
                         color='blue',
                         horizontalalignment='left',  # horizontalalignment (left, center, right)
                         verticalalignment='bottom')  # verticalalignment (top, center, bottom)

            ax.plot(x, conv_list2, 'g', label="신혼부부 비율")
            for i, v in enumerate(x):
                plt.text(v, conv_list2[i], conv_list2[i],  # 좌표 (x축 = v, y축 = y[0]..y[1], 표시 = y[0]..y[1])
                         fontsize=9,
                         color='black',
                         horizontalalignment='center',  # horizontalalignment (left, center, right)
                         verticalalignment='bottom')  # verticalalignment (top, center, bottom)
            plt.legend(loc='center left')
            ax2 = ax.twinx()
            ax2.plot(x, conv_list3, 'b', label='1인가구 비율')
            plt.ylim([int(min(conv_list3) - 2), int(max(conv_list3) + 1)])
            for i, v in enumerate(x):
                plt.text(v, conv_list3[i], conv_list3[i],  # 좌표 (x축 = v, y축 = y[0]..y[1], 표시 = y[0]..y[1])
                         fontsize=9,
                         color='magenta',
                         horizontalalignment='right',  # horizontalalignment (left, center, right)
                         verticalalignment='bottom')  # verticalalignment (top, center, bottom)
            plt.legend(loc='right')
            plt.title(f"{city}")
            plt.show()


if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    myWindow = check()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()

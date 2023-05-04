import pymysql as p
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

form_class = uic.loadUiType("inquiry.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # DB 연결
        # self.conn = p.connect(host='127.0.0.1', port=3306, user='root', password='0000', db='3team', charset='utf8')
        # self.c = self.conn.cursor()
        self.connect_db()

        # matplotlib 한글 폰트 패치
        font_path = "c:\\windows\\Fonts\\gulim.ttc"
        font = font_manager.FontProperties(fname=font_path).get_name()
        rc('font', family=font)

        # 테이블 위젯 수정 불가및 헤드 자동 길이 맞춤
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.변수 초기화 및 선언
        self.csv = list()
        self.db = 'elementary'
        self.header = '*'
        self.where = ''
        self.join = ''
        self.title = self.checkBox.text()

        # 메서드 와 시그널 연결
        self.research_btn.clicked.connect(self.search)
        self.checkBox.stateChanged.connect(self.choice_db)
        self.checkBox_2.stateChanged.connect(self.choice_db)
        self.checkBox_3.stateChanged.connect(self.choice_db)
        self.btn_graph.clicked.connect(self.graph)

    def connect_db(self):
        self.conn = p.connect(host='127.0.0.1', port=3306, user='root', password='0000', db='3team', charset='utf8')
        self.c = self.conn.cursor()

    # 검색 기능
    def search(self):
        if type(self.db) == str:
            self.condition1()
            self.single_search()
        else:
            self.condition2()
            self.multi_search()

    # 1개의 DB를 검색 할때 조건에 따른 SQL 문법 조건 셋팅
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

    # 1개의 DB를 검색 할때 DB의 내용을 불러와 테이블 위젯에 보여 주기
    def single_search(self):
        self.c.execute(f'select {self.header} from {self.db} {self.where};')
        self.table_show()

    # 2개, 3개의 DB 자료를 검색 할때 조건에 따른 SQL 문법 조건 셋팅
    def condition2(self):
        city = self.combo_nation.currentText()
        year = self.combo_year.currentText()
        # 2개
        # select / a.행정구역별, a.2016년, b.2016년 / from / elementary as a
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
        # select / a.행정구역별, a.2016년, b.2016년, c.2016년 / from / elementary as a
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

    # 2,3개의 DB를 검색 할때 DB의 내용을 불러와 테이블 위젯에 보여 주기
    def multi_search(self):
        self.c.execute(f'select {self.header} from {self.db[0]} {self.join} {self.where};')
        self.table_show()

    # 불러온 DB의 내용을 테이블 위젯에 보여 주기
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

    # 1개의 DB 자료 에서 조건에 맏는 header 값를 받기 위한 자료
    def table_header1(self):
        self.c.execute(f'select {self.header} from {self.db};')
        self.csv = self.c.fetchall()

    # 2,3개의 DB 자료 에서 조건에 맏는 header 값를 받기 위한 자료
    def table_header2(self):
        self.c.execute(f'select {self.header} from {self.db[0]} {self.join};')
        self.csv = self.c.fetchall()

    # 1,2,3개의 DB를 선택 하는 조건 에서 자료를 받기 위한 변수 선언
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

    # 파이 차트 보여 주기
    def graph(self):
        self.choice_db()
        year = self.combo_year.currentText()
        label_city = list()
        label_value = list()
        label_value2 = list()
        label_value3 = list()
        graph_style = {'width': 0.7, 'edgecolor': 'w', 'linewidth': 2}
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
                    print(type(num_list[i][1]))
            plt.pie(label_value, labels=label_city, autopct='%.1f%%', startangle=90,
                    counterclock=False, wedgeprops=graph_style)
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
                plt.subplot(1, len(label_list), i+1)
                plt.pie(label_list[i], labels=label_city, autopct='%.1f%%', startangle=90,
                        counterclock=False, wedgeprops=graph_style)
                plt.title(f'{self.title[i]} ({year}년)')
            plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()

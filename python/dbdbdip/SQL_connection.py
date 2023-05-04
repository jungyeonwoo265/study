import pymysql as p
import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSignal, QObject, QEvent

form_class = uic.loadUiType('./inquiry.ui')[0]  # 페이지 UI불러옴


class Main(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.conn = p.connect(host='localhost', port=3306, user='root', password='0000',
                         db='3Team', charset='utf8')
        self.c = self.conn.cursor()
        self.research_btn.clicked.connect(self.searchmethod)

    def cellclicked(self,row,column):
        self.row = row
        self.column = column
    def searchmethod(self):
        checkbox_count = 0
        self.tablename1=''
        self.tablename2=''
        if self.checkBox.isChecked() == True:
            checkbox_count +=1
            self.tablename = 'elementary'
        if self.checkBox_2.isChecked() == True:
            checkbox_count += 1
            self.tablename = 'new_marry'
        if self.checkBox_3.isChecked() == True:
            checkbox_count += 1
            self.tablename = 'solo'
        if checkbox_count ==1:
            self.search()
        elif checkbox_count == 2:
            if self.checkBox.isChecked() == True and self.checkBox_2.isChecked()==True:
                self.tablename1='elementary'
                self.tablename2='new_marry'
            elif self.checkBox_2.isChecked() == True and self.checkBox_3.isChecked()==True:
                self.tablename1 = 'new_marry'
                self.tablename2 = 'solo'
            elif self.checkBox.isChecked() == True and self.checkBox_3.isChecked()==True:
                self.tablename1 = 'elementary'
                self.tablename2 = 'solo'
            self.search2()
        else :
            self.search3()
    def search2(self):
        self.table.clearContents()
        nation = self.combo_nation.currentText()
        year = self.combo_year.currentText()
        if nation == '선택안함':
            self.c.execute(f'SELECT A.행정구역별,A.{year}년,B.{year}년 FROM {self.tablename1} AS A \
                            JOIN {self.tablename2} AS B ON A.행정구역별 = B.행정구역별 WHERE A.행정구역별 !="행정구역별"')
            self.Header = ['행정구역별', year]  ## 수정요망 테이블 이름에 맞게 TEXT 들어갈 예정
        else:
            self.c.execute(f'SELECT A.행정구역별,A.{year}년,B.{year}년 FROM {self.tablename1} AS A \
                            JOIN {self.tablename2} AS B ON A.행정구역별 = B.행정구역별 WHERE A.행정구역별 = "{nation}"')
            self.Header = ['행정구역별',year] ## 수정요망 테이블 이름에 맞게 TEXT 들어갈 예정
        Searchlist = self.c.fetchall()

        # 테이블 위젯의 행과 열에 데이터 넣어줌
        self.table.setRowCount(len(Searchlist))
        self.table.setColumnCount(len(Searchlist[0]))
        print(Searchlist)
        for i in range(len(Searchlist)):
            for j in range(len(Searchlist[i])):
                # i번째 줄의 j번째 칸에 데이터를 넣어줌
                if type(Searchlist) == str :
                    self.table.setItem(i, j, QTableWidgetItem(Searchlist[i][j]))
                else :
                    self.table.setItem(i, j, QTableWidgetItem(str(Searchlist[i][j])))
        self.table.setHorizontalHeaderLabels(self.Header)

    def search3(self):
        self.table.clearContents()
        nation = self.combo_nation.currentText()
        year = self.combo_year.currentText()
        if nation == '선택안함':
            self.c.execute(f'SELECT A.행정구역별,A.{year}년,B.{year}년,C.{year}년 FROM elementary AS A \
                            INNER JOIN new_marry AS B ON A.행정구역별 = B.행정구역별 INNER JOIN solo AS C \
                            ON B.행정구역별 = C.행정구역별 WHERE A.행정구역별 !="행정구역별"')
        else:
            self.c.execute(f'SELECT A.행정구역별,A.{year}년,B.{year}년,C.{year}년 FROM elementary AS A \
                            INNER JOIN new_marry AS B ON A.행정구역별 = B.행정구역별 INNER JOIN solo AS C \
                            ON B.행정구역별 = C.행정구역별 WHERE A.행정구역별 = "{nation}"')

        Searchlist = self.c.fetchall()

        # 테이블 위젯의 행과 열에 데이터 넣어줌
        self.table.setRowCount(len(Searchlist))
        self.table.setColumnCount(len(Searchlist[0]))
        print(Searchlist)
        for i in range(len(Searchlist)):
            for j in range(len(Searchlist[i])):
                # i번째 줄의 j번째 칸에 데이터를 넣어줌
                if type(Searchlist) == str :
                    self.table.setItem(i, j, QTableWidgetItem(Searchlist[i][j]))
                else :
                    self.table.setItem(i, j, QTableWidgetItem(str(Searchlist[i][j])))
        # self.table.setHorizontalHeaderLabels(self.Header)
    def search(self):
        self.table.clearContents()
        Searchlist =[]
        nation = self.combo_nation.currentText()
        year = self.combo_year.currentText()
        self.c.execute(f'SELECT * FROM {self.tablename}')
        self.Header = list(map(str, self.c.fetchone()))
        if year == '선택안함' and nation =='선택안함':
            self.c.execute(f'SELECT * FROM {self.tablename} WHERE 행정구역별 != "행정구역별"')
        elif nation == '선택안함':
            self.c.execute(f'SELECT 행정구역별,{year}년 FROM {self.tablename}')
            self.Header = ['행정구역별', year]
        elif year == '선택안함':
            self.c.execute(f'SELECT* FROM {self.tablename} WHERE 행정구역별 LIKE "%{nation}%"')
        else:
            self.c.execute(f'SELECT 행정구역별,{year}년 FROM {self.tablename} WHERE 행정구역별 LIKE "%{nation}%"')
            self.Header = ['행정구역별',year]
        Searchlist = self.c.fetchall()

        # 테이블 위젯의 행과 열에 데이터 넣어줌
        self.table.setRowCount(len(Searchlist))
        self.table.setColumnCount(len(Searchlist[0]))
        print(Searchlist)
        for i in range(len(Searchlist)):
            for j in range(len(Searchlist[i])):
                # i번째 줄의 j번째 칸에 데이터를 넣어줌
                if type(Searchlist) == str :
                    self.table.setItem(i, j, QTableWidgetItem(Searchlist[i][j]))
                else :
                    self.table.setItem(i, j, QTableWidgetItem(str(Searchlist[i][j])))

        self.table.setHorizontalHeaderLabels(self.Header)



    def Search2(self):
        self.tableWidget.clearContents()
        Searchlist =[]
        searchtext = self.comboBox_3.currentText()

        # DB 생성 (오토 커밋)
        conn = sqlite3.connect("Shop2.db", isolation_level=None)
        # 커서 획득
        c = conn.cursor()
        c.execute(f'SELECT * FROM Gwangju WHERE 상권업종소분류코드 LIKE "%{searchtext}%"')
        Searchlist = c.fetchall()
        c.close()
        if Searchlist == [] :
            return
        # 테이블 위젯의 행과 열에 데이터 넣어줌
        self.tableWidget.setRowCount(len(Searchlist))
        self.tableWidget.setColumnCount(len(Searchlist[0]))
        for i in range(len(Searchlist)):
            for j in range(len(Searchlist[i])):
                # i번째 줄의 j번째 칸에 데이터를 넣어줌
                self.tableWidget.setItem(i, j, QTableWidgetItem(Searchlist[i][j]))
        self.tableWidget.setHorizontalHeaderLabels(self.Header)




    def combobox(self):
        self.comboBox_2.clear()
        CB_String = self.comboBox_1.currentText()
        # DB 생성 (오토 커밋)
        conn = sqlite3.connect("Shop2.db", isolation_level=None)
        Codelist=[]
        # 커서 획득
        c = conn.cursor()
        c.execute(f'SELECT DISTINCT 중분류코드 FROM Shop_Code WHERE 중분류코드 LIKE "%{CB_String}%"')
        Codelist = c.fetchall()
        Codelist.sort()
        print(Codelist)
        c.close()
        for x in Codelist :
            self.comboBox_2.addItem(x[0])
        self.ChangeLabel()

    def ChangeLabel(self):
        CB_String = self.comboBox_1.currentText()
        conn = sqlite3.connect("Shop2.db", isolation_level=None)
        Codelist = []
        # 커서 획득
        c = conn.cursor()
        c.execute(f'SELECT 대분류코드,대분류명 FROM CodeView2 WHERE 대분류코드 LIKE "%{CB_String}%"')
        Codelist = c.fetchall()
        self.label.setText(Codelist[0][1])
        c.close()

    def ChangeLabel2(self):
        CB_String = self.comboBox_2.currentText()
        conn = sqlite3.connect("Shop2.db", isolation_level=None)
        Codelist = []
        # 커서 획득
        c = conn.cursor()
        c.execute(f'SELECT 중분류코드,중분류명 FROM CodeView WHERE 중분류코드 LIKE "%{CB_String}%"')
        Codelist = c.fetchall()
        self.label_2.setText(Codelist[0][1])
        c.close()


    def combobox2(self):
        self.comboBox_3.clear()
        CB_String = self.comboBox_2.currentText()
        # DB 생성 (오토 커밋)
        conn = sqlite3.connect("Shop2.db", isolation_level=None)
        Codelist=[]
        # 커서 획득
        c = conn.cursor()
        c.execute(f'SELECT DISTINCT 소분류코드 FROM Shop_Code WHERE 소분류코드 LIKE "%{CB_String}%"')
        Codelist = c.fetchall()
        Codelist.sort()
        c.close()
        for x in Codelist :
            self.comboBox_3.addItem(x[0])
        self.ChangeLabel2()
    def ChangeLabel3(self):
        CB_String = self.comboBox_3.currentText()
        conn = sqlite3.connect("Shop2.db", isolation_level=None)
        Codelist = []
        # 커서 획득
        c = conn.cursor()
        c.execute(f'SELECT 소분류코드,소분류명 FROM CodeView3 WHERE 소분류코드 LIKE "%{CB_String}%"')
        Codelist = c.fetchall()
        self.label_3.setText(Codelist[0][1])
        c.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    print("test")

    mainWindow = Main()  # 상동
    mainWindow.show()
    app.exec_()






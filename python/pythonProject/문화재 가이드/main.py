import csv
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from reserve import Reserve
from login import Login

form_class = uic.loadUiType("Cultural Heritage_main.ui")[0]

class WindowClass(QMainWindow, form_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.Gwangyang.clicked.connect(self.gwangyang)          # 지역 버튼 클릭시 해당되는 csv 파일 테이블 위젯에 띄우기
        self.Haenam.clicked.connect(self.haenam)
        self.Sunchang.clicked.connect(self.sunchang)

        self.tableWidget.doubleClicked.connect(self.reserve)    # 위젯의 요소를 더블 클릭시 예약창 띄우기
        self.login.clicked.connect(self.login_p)                # 로그인 버튼 클릭시 로그인창 띄우기

        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)                  # 테이블 위젯 수정 불가
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)       # 테이블 위젯 헤더 정렬
        self.user.setText('')   # 유저 로그인 상태 표시 라벨 공백처리
        self.id = False         # 로그인 없이 예약창 들어가지 않게 하기위해 False 선언
        self.column = 5         # 테이블 위젯 열수

    def reserve(self): # 예약창 불러오기
        if self.id:
            self.res = Reserve()
            name, address = self.set_res()
            self.res.name_set(name)
            self.res.address_set(address)
            self.res.id_set(self.id)
            self.res.exec_()
        else:
            QMessageBox.about(self, '안내창', '로그인을 하세요')

    def login_p(self):  # 로그인 / 로그아웃을 위한 함수
        if self.id:
            self.user.setText('')
            self.login.setText('로그인')
            self.id = False
        else:
            self.log = Login()
            self.log.login_Button.clicked.connect(self.login_s)
            self.log.exec_()

    def set_res(self):  # 예약창에 문화재 이름, 소재지 전달을 위한 함수
        res_list = list()
        row = self.tableWidget.currentRow()
        for i in range(self.column):
            res_list.append(self.tableWidget.item(row, i).text())
        return res_list[0], res_list[4]


    def g(self):        # 광양시 문화재 리스트에 넣기
        list_G = list()
        with open('전라남도 광양시_문화재_20220727.csv', 'r') as f:
            list1 = csv.reader(f)
            for i in list1:
                list_G.append(i)
        return list_G

    def h(self):        # 해남군 문화재 리스트에 넣기
        list_G = list()
        with open('전라남도 해남군_문화재_20220406.csv', 'r') as f:
            list1 = csv.reader(f)
            for i in list1:
                list_G.append(i)
        return list_G

    def s(self):        # 순창군 문화재 리스트에 넣기
        list_G = list()
        with open('전라북도_순창군_문화재현황_20160630.csv', 'r') as f:
            list1 = csv.reader(f)
            for i in list1:
                list_G.append(i)
        return list_G

    def login_s(self):      # 로그인 완료후 메인창에 값 가져오기
        self.id = self.log.id
        self.user.setText(self.id+'님 안녕하세요')
        self.login.setText('로그아웃')
        self.log.close()

    def gwangyang(self):    # 테이블 위젯에 요소 추가
        # 이름 4,지정 1,분류 2,번호 3,소재지 6
        self.tableWidget.clearContents()
        list_G = self.g()
        self.tableWidget.setRowCount(len(list_G)-1)
        self.tableWidget.setColumnCount(self.column)
        for i in range(1, len(list_G)):
            self.tableWidget.setItem(i-1, 0, QTableWidgetItem(list_G[i][4]))
            self.tableWidget.setItem(i-1, 1, QTableWidgetItem(list_G[i][1]))
            self.tableWidget.setItem(i-1, 2, QTableWidgetItem(list_G[i][2]))
            self.tableWidget.setItem(i-1, 3, QTableWidgetItem(list_G[i][3]))
            self.tableWidget.setItem(i-1, 4, QTableWidgetItem(list_G[i][6]))

    def haenam(self):    # 테이블 위젯에 요소 추가
        # 이름 1,지정 4,분류 5,번호 3,소재지 9
        self.tableWidget.clearContents()
        list_G = self.h()
        self.tableWidget.setRowCount(len(list_G)-1)
        self.tableWidget.setColumnCount(self.column)
        for i in range(1, len(list_G)):
            self.tableWidget.setItem(i-1, 0, QTableWidgetItem(list_G[i][1]))
            self.tableWidget.setItem(i-1, 1, QTableWidgetItem(list_G[i][4]))
            self.tableWidget.setItem(i-1, 2, QTableWidgetItem(list_G[i][5]))
            self.tableWidget.setItem(i-1, 3, QTableWidgetItem(list_G[i][3]))
            self.tableWidget.setItem(i-1, 4, QTableWidgetItem(list_G[i][9]))

    def sunchang(self):    # 테이블 위젯에 요소 추가
        # 이름 2,지정 0,분류 1,번호 4,소재지 5
        self.tableWidget.clearContents()
        list_G = self.s()
        self.tableWidget.setRowCount(len(list_G)-1)
        self.tableWidget.setColumnCount(self.column)
        for i in range(1, len(list_G)):
            self.tableWidget.setItem(i-1, 0, QTableWidgetItem(list_G[i][2]))
            self.tableWidget.setItem(i-1, 1, QTableWidgetItem(list_G[i][0]))
            self.tableWidget.setItem(i-1, 2, QTableWidgetItem(list_G[i][1]))
            self.tableWidget.setItem(i-1, 3, QTableWidgetItem(list_G[i][4]))
            self.tableWidget.setItem(i-1, 4, QTableWidgetItem(list_G[i][5]))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
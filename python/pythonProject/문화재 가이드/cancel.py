import csv
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("cancel.ui")[0]

# id = 'qqqq'
# id = 'wwww'

class cancelclass(QDialog, form_class) :
    def __init__(self, us_id):
        super().__init__()
        self.setupUi(self)
        self.col = 5        # 테이블 위젯의 열수
        self.set_id(us_id)  # 아이디값을 받아오기 위한 함수

        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)              # 테이블 위젯의 요소 수정 불가
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)   # 테이블 위젯의 헤더 요소의 길이로 정렬

        self.pushButton.clicked.connect(self.cancel_list)       # 예약 취소

    def show_list(self):    # 테이블 위젯에 요소 넣기
        if self.res_list:
            self.tableWidget.setRowCount(len(self.res_list))
            self.tableWidget.setColumnCount(self.col)
            for i in range(len(self.res_list)):
                for j in range(self.col):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(self.res_list[i][j]))
        else:
            QMessageBox.about(self, '안내창', '예약내역이 없습니다.')
            self.close()

    def cancel_list(self):      #예약 취소
        res_list1 = list()
        count = 0
        cho = self.tableWidget.currentRow()
        cancel = self.res_list.pop(cho)
        with open('reservation_list.csv', 'r') as f:
            csv_list = csv.reader(f)
            for i in csv_list:
                res_list1.append(i)
        with open('reservation_list.csv', 'w', newline='') as f:
            can_list = csv.writer(f)
            for i in res_list1:
                if cancel != i and not count:
                    can_list.writerow(i)
                elif count:
                    can_list.writerow(i)
                else:
                    count = 1
        self.read_csv()

    def read_csv(self):     # csv 파일 읽어 리스트에 넣기
        self.res_list = list()
        with open('reservation_list.csv', 'r') as f:
            csv_list = csv.reader(f)
            for i in csv_list:
                if self.id in i:
                    self.res_list.append(i)
        self.show_list()

    def set_id(self, id):   # 아이디 셋팅
        self.id = id
        self.read_csv()

# if __name__ == "__main__" :
#     app = QApplication(sys.argv)
#     myWindow = cancelclass()
#     myWindow.show()
#     myWindow.show_list()
#     app.exec_()
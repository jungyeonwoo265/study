import csv
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
from cancel import cancelclass

form_class = uic.loadUiType("CulturalHeritage.ui")[0]

#------------연결시 주석처리
# name = 'aaa'
# address = 'bbb'
# id = 'ccc'
# id = 'ddd'
#------------------------

class Reserve(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.calendarWidget.clicked.connect(self.select_date)       # 캘린더 위젯의 날짜 데이터 가져오기
        self.reserve_pb.clicked.connect(self.reservation)           # 예약하기
        self.cancel_pb.clicked.connect(self.cancel_page)            # 예약취소하기
        self.home_pb.clicked.connect(self.gohome)                   # 메인창으로 가기

        # 예약에 필요한 값 초기화
        self.date = self.calendarWidget.selectedDate()
        self.today = self.calendarWidget.selectedDate()
        self.res_date = str(self.date.year()) + '/' + str(self.date.month()) + '/' + str(self.date.day())
        self.time1.setChecked(True)

        #--------------------연결시 주석처리
        # self.name_set(name)
        # self.address_set(address)
        # self.id_set(id)
        #---------------------------------
        self.hide_date()    # 캘린더 위젯 선택 제한 하기

    def hide_date(self):    # 예약 가능 날짜를 제한하는 함수 , 당일 예약 불가, 오늘 부터 100일후 까지만 예약 가능
        self.maxday = self.today.addDays(100)
        self.calendarWidget.setDateRange(self.today.addDays(1), self.maxday)

    def select_date(self):      # 캘린더 위젯 에서 선택한 날짜를 문자열 로 저장
        self.date = self.calendarWidget.selectedDate()
        self.res_date = str(self.date.year()) + '/' + str(self.date.month()) + '/' + str(self.date.day())
        self.set_reserve()

    def set_reserve(self):      # 시간대 별 예약 인원 라벨을 셋팅 하기
        res1 = self.reserve1_text()
        res2 = self.reserve2_text()
        res3 = self.reserve3_text()
        self.reserve1.setText(str(res1))
        self.reserve2.setText(str(res2))
        self.reserve3.setText(str(res3))

    def reserve1_text(self):    # 1번째 시간대 예약 인원 합계 구하기
        res = 0
        with open('reservation_list.csv', 'r') as f:
            res_list = csv.reader(f)
            for i in res_list:
                if self.res_date in i and self.name in i and self.address in i:
                    if self.time1.text() in i:
                        res += int(i[4])
        return res

    def reserve2_text(self):    # 2번째 시간대 예약 인원 합계 구하기
        res = 0
        with open('reservation_list.csv', 'r') as f:
            res_list = csv.reader(f)
            for i in res_list:
                if self.res_date in i and self.name in i and self.address in i:
                    if self.time2.text() in i:
                        res += int(i[4])
        return res

    def reserve3_text(self):    # 3번째 시간대 예약 인원 합계 구하기
        res = 0
        with open('reservation_list.csv', 'r') as f:
            res_list = csv.reader(f)
            for i in res_list:
                if self.res_date in i and self.name in i and self.address in i:
                    if self.time3.text() in i:
                        res += int(i[4])
        return res

    def reservation(self):      # 예약 하기, 30인 초과 하여 예약 하지 못하게 하기, 주말은 쉬는날 안내하기
        if self.date.dayOfWeek() < 6:
            count = self.count_spinBox.text()
            res_time = ''
            res = 0
            if self.time1.isChecked():
                res_time = self.time1.text()
                res = self.reserve1_text()
            elif self.time2.isChecked():
                res_time = self.time2.text()
                res = self.reserve2_text()
            elif self.time3.isChecked():
                res_time = self.time3.text()
                res = self.reserve3_text()

            if res+int(count) <= 30:
                word = self.name + ',' + self.address + ',' + self.res_date + ',' + res_time + ',' + count + ',' + self.id + '\n'
                with open('reservation_list.csv', 'a', newline='') as f:
                    f.write(word)
                self.set_reserve()
                QMessageBox.about(self, '안내창', '예약이 완료 되었습니다.')
            else:
                QMessageBox.about(self, '안내창', '정원 초과 입니다. 인원 또는 시간을 변경 하세요.')

        else:
            QMessageBox.about(self, '안내창', '주말입니다. 예약 날짜를 변경 하세요.')

    def cancel(self):       # 로그인 아이디 로 예약건 전부 취소 하기 (사용 하지 않음)
        cancel_count = 0
        reservation = list()
        # haed_list =['문화재', '소재지', '날짜', '시간', '예약 인원', '회원 아이디']
        with open('reservation_list.csv', 'r') as f:
            res_list = csv.reader(f)
            for i in res_list:
                if self.id not in i and '' not in i and i:
                    reservation.append(i)
                if self.id in i:
                    cancel_count = 1
        with open('reservation_list.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            if reservation:
                for i in reservation:
                    writer.writerow(i)
        self.set_reserve()
        if cancel_count:
            QMessageBox.about(self, '안내창', '예약이 취소 되었습니다.')
        else:
            QMessageBox.about(self, '안내창', '예약 이력이 없습니다.')

    def cancel_page(self):  # 예약 취소 창 띄우기
        self.can = cancelclass(self.id)
        self.can.exec_()

    def gohome(self):   # 예약창 닫기
        self.close()

    def name_set(self, name):   # 문화재 이름 받아 오기
        self.name = name

    def address_set(self, address):     # 문화재 소재지 받아 오기
        self.address = address

    def id_set(self, id):   # 로그인 아이디 받아 오기
        self.id = id

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     myWindow = Reserve()
#     myWindow.show()
#     app.exec_()
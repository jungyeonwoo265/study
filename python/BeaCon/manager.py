import sys

from PyQt5.QtGui import QTextCharFormat
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pymysql as p
from user import User

form_class = uic.loadUiType("manager.ui")[0]


class Manager(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # DB 연결
        self.conn = p.connect(host='127.0.0.1', port=3306, user='root', password='0000', db='step6', charset='utf8')
        self.c = self.conn.cursor()
        self.conn.close()

        # user 클래스 메서드 활용 - 날짜에 따른 DB 조회및 수정
        # 수업 있는지 확인 하고 당일 출석부 만들고 전날 출석 결과 판정 하기
        self.user = User()
        self.user.check_schecule()
        self.user.result()
        self.user.roster()

        # self.변수 초기화 및 선언
        self.date = 'curdate()'
        self.name = str
        self.cal = list()
        # self.set_information("이상복")

        # 메서드 호출
        self.reset_page3()
        self.reset_page4()

        # 시그널 - 메서드
        self.cb_menu.currentIndexChanged.connect(self.page_move)
        self.pb_home_page2.clicked.connect(self.go_home)
        self.pb_home_page3.clicked.connect(self.go_home)
        self.pb_home_page4.clicked.connect(self.go_home)
        self.pb_delet_page2.clicked.connect(self.notice_del)
        self.pb_input_page2.clicked.connect(self.notice_input)
        self.cb_name.currentIndexChanged.connect(self.tableset_page3)
        self.pb_input_page3.clicked.connect(self.input_page3)
        self.pb_delet_page3.clicked.connect(self.output_page3)
        self.table_page4.cellClicked.connect(self.message)
        self.le_input_page4.returnPressed.connect(self.input_message)
        self.pb_delet_page4.clicked.connect(self.output_message)

    # 메세지 삭제 하기
    def output_message(self):
        text = self.list_page4.currentItem()
        if text:
            text = text.text()
            message = text.split('/')
            self.open_db()
            self.c.execute(
                f'delete from messenger where 보냄="{self.name}" and 시간="{message[1].strip()}" and 날짜={self.date};')
            self.conn.commit()
            self.conn.close()
            self.message()

    # 메세지 등록 하기
    def input_message(self):
        name = self.table_page4.currentItem()
        if name:
            text = self.le_input_page4.text()
            if text:
                name = name.text()
                self.le_input_page4.clear()
                self.open_db()
                self.c.execute(f'insert into messenger values '
                               f'({self.date},"{self.name}", "{name}", curtime(), "{text}", "n");')
                self.conn.commit()
                self.conn.close()
                self.message()

    # 메신저 내용 보여 주기
    def message(self):
        name = self.table_page4.currentItem().text()
        if name:
            self.list_page4.clear()
            self.open_db()
            self.c.execute(f'select 보냄, 시간, 내용 from messenger where 날짜 > subdate({self.date},1)'
                           f'and (보냄 ="{name}" or 받음="{name}") order by 날짜;')
            message = self.c.fetchall()
            for i in message:
                self.list_page4.addItem(f'{i[0]} / {i[1]} / {i[2]}')
            self.conn.close()

    # 메신저 명단 보여 주기
    def reset_page4(self):
        self.open_db()
        self.c.execute(f'select name from user;')
        name = self.c.fetchall()
        self.table_page4.setRowCount(len(name))
        self.table_page4.setColumnCount(len(name[0]))
        self.table_page4.setHorizontalHeaderItem(0, QTableWidgetItem("이름"))
        for i, le in enumerate(name):
            for j, v in enumerate(le):
                self.table_page4.setItem(i, j, QTableWidgetItem(v))
        self.conn.close()

    # 일정 삭제 하기 및 삭제 일정 캘린더 색 변경
    def output_page3(self):
        row = self.table_page3.currentRow()
        if row >= 0:
            name = self.cb_name.currentText()
            date = self.table_page3.item(row, 0).text()
            text = self.table_page3.item(row, 1).text()
            # 캘린드 스타일 변경
            style1 = QTextCharFormat()
            style1.setBackground(Qt.white)
            cal_st = QDate.fromString(date, "yyyy-MM-dd")
            self.calendar_page3.setDateTextFormat(cal_st, style1)
            # 일정 지우기
            self.open_db()
            self.c.execute(f'delete from calendar where 일정 ="{date}" and 내역 = "{text}" and 이름 = "{name}";')
            self.conn.commit()
            self.conn.close()
            self.tableset_page3()

    # page3 일정 추가 하기
    def input_page3(self):
        text = self.le_input_page3.text()
        date = self.calendar_page3.selectedDate().toString('yyyy-MM-dd')
        name = self.cb_name.currentText()
        self.open_db()
        if text:
            self.c.execute(f'insert into calendar values (now(),"{name}", "{date}", "{text}");')
        self.conn.commit()
        self.conn.close()
        self.le_input_page3.clear()
        self.tableset_page3()

    # page3 달력및 리스트 보기
    def tableset_page3(self):
        # 학생 이름 변경시 캘린더에 남는 배경색 지우기
        style1 = QTextCharFormat()
        style1.setBackground(Qt.white)
        if self.cal:
            for i in self.cal:
                self.calendar_page3.setDateTextFormat(i, style1)
        self.cal = list()
        self.open_db()
        name = self.cb_name.currentText()
        # 리스트 보기
        self.c.execute(f'select count(*) from calendar where 이름 ="{name}"')
        num = self.c.fetchone()[0]
        if num:
            # 캘린더 스타일 변경
            style2 = QTextCharFormat()
            style2.setBackground(Qt.yellow)
            self.c.execute(f'select 일정, 내역 from calendar where 이름 ="{name}" '
                           f'and 일정 > subdate({self.date},1) order by 일정')
            cal = self.c.fetchall()
            self.table_page3.setRowCount(len(cal))
            self.table_page3.setColumnCount(len(cal[0]))
            for idx, le in enumerate(cal):
                cal_st = QDate.fromString(le[0], "yyyy-MM-dd")
                self.calendar_page3.setDateTextFormat(cal_st, style2)
                self.cal.append(cal_st)
                for j, v in enumerate(le):
                    self.table_page3.setItem(idx, j, QTableWidgetItem(v))
        else:
            self.table_page3.clear()
            self.table_page3.setRowCount(0)
            self.table_page3.setColumnCount(0)
        self.conn.close()

    # 콤보 박스 이름 셋팅
    def reset_page3(self):
        self.open_db()
        self.c.execute(f'select name from user;')
        name = self.c.fetchall()
        for i in name:
            self.cb_name.addItem(i[0])
        self.conn.close()

    # 공지 올리기
    def notice_input(self):
        text = self.le_input_page2.text()
        if text:
            self.open_db()
            self.c.execute(f'update notice set 상태 ="n" where 상태 ="y"')
            self.conn.commit()
            self.c.execute(f'insert into notice values("{self.name}",{self.date},curtime(),"{text}","y")')
            self.conn.commit()
            self.conn.close()
            self.notice()

    # 공지 내리기
    def notice_del(self):
        self.open_db()
        self.c.execute(f'update notice set 상태 ="n" where 상태 ="y"')
        self.conn.commit()
        self.conn.close()
        self.notice()

    # page2 공지 내역 표시
    def notice(self):
        self.open_db()
        self.c.execute(f'select 작성자, 날짜, 내용, if(상태="y", "공지중", "공지내림") from notice;')
        noti = self.c.fetchall()
        self.table_page2.setRowCount(len(noti))
        self.table_page2.setColumnCount(len(noti[0]))
        for i, le in enumerate(noti):
            for j, v in enumerate(le):
                self.table_page2.setItem(i, j, QTableWidgetItem(v))
        self.conn.close()
        self.early()

    # 현재 공지 띄우기
    def early(self):
        self.open_db()
        self.c.execute('select count(*) from notice where 상태 = "y";')
        count = self.c.fetchone()
        if count[0]:
            self.c.execute('select 내용 from notice where 상태 = "y";')
            noti = self.c.fetchone()[0]
            self.lb_notice.setText(noti)
        else:
            self.lb_notice.setText('')
        self.conn.close()


    # page1 출석 확인 명단 만들기
    def attendance(self):
        self.open_db()
        self.c.execute(f'select count(*) from schedule where 날짜 = {self.date};')
        check = self.c.fetchone()
        self.check_class = check[0]
        if self.check_class:
            header = ['이름', '입실', '외출', '복귀', '퇴실']
            self.c.execute(f'select 이름, 입실, 외출, 복귀, 퇴실 from attendance where 날짜 = {self.date}')
            atten = self.c.fetchall()
            self.table_page1.setRowCount(len(atten))
            self.table_page1.setColumnCount(len(atten[0]))
            for i, le in enumerate(atten):
                for j, v in enumerate(le):
                    self.table_page1.setItem(i, j, QTableWidgetItem(v))
            for i, v in enumerate(header):
                self.table_page1.setHorizontalHeaderItem(i, QTableWidgetItem(v))
        self.conn.close()

    # 각 페이지 이동 및 셋팅
    def page_move(self):
        page = self.cb_menu.currentText()
        self.cb_menu.setCurrentIndex(0)
        if page == '...':
            self.attendance()
            self.stackedWidget.setCurrentIndex(0)
        elif page == '전체 공지':
            self.notice()
            self.stackedWidget.setCurrentIndex(1)
        elif page == '학생 일정':
            self.tableset_page3()
            self.stackedWidget.setCurrentIndex(2)
        elif page == '메신저':
            self.stackedWidget.setCurrentIndex(3)

    # 홈 화면으로 이동
    def go_home(self):
        self.stackedWidget.setCurrentIndex(0)

    # main.py 에서 관리자 이름 가져 오기
    def set_information(self, name):
        self.name = name

    # DB 오픈하기
    def open_db(self):
        self.conn = p.connect(host='127.0.0.1', port=3306, user='root', password='0000', db='step6', charset='utf8')
        self.c = self.conn.cursor()


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     myWindow = Manager()
#     myWindow.show()
#     app.exec_()

import sys

from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QTextCharFormat
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pymysql as p
from schedule import Schedule

form_class = uic.loadUiType("user.ui")[0]


class User(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # DB 연결
        self.conn = p.connect(host='127.0.0.1', port=3306, user='root', password='0000', db='step6', charset='utf8')
        self.c = self.conn.cursor()
        self.conn.close()

        # self.변수 초기화 및 선언
        # page1
        self.check_class = False
        self.time = 'curtime()'
        self.date = 'curdate()'
        self.name = str
        self.state = tuple
        self.reset()
        self.schadule = Schedule()
        # main.py 연결시 주석 처리
        # self.set_information('임홍선')

        # 시그널 - 메서드
        self.cb_menu.currentIndexChanged.connect(self.page_move)
        self.pb_home_page2.clicked.connect(self.go_home)
        self.pb_home_page3.clicked.connect(self.go_home)
        self.pb_home_page4.clicked.connect(self.go_home)
        self.pb_home_page5.clicked.connect(self.go_home)
        self.pb_check.clicked.connect(self.check)
        self.pb_check.clicked.connect(self.push_chang)
        self.pb_outing.clicked.connect(self.outing)
        self.pb_outing.clicked.connect(self.push_chang)
        self.pb_input.clicked.connect(self.input_page4)
        self.pb_delet_page4.clicked.connect(self.output_page4)
        self.le_input_page5.returnPressed.connect(self.input_page5)
        self.pb_delet_page5.clicked.connect(self.output_page5)

    # page5 메세지 삭제
    def output_page5(self):
        text = self.list_page5.currentItem()
        if text:
            text = text.text()
            message = text.split('/')
            self.open_db()
            self.c.execute(f'delete from messenger where 보냄="{self.name}" and 시간="{message[1].strip()}" and 날짜={self.date};')
            self.conn.commit()
            self.conn.close()
            self.reset_page5()

    # page5 메세지 등록
    def input_page5(self):
        text = self.le_input_page5.text()
        self.le_input_page5.clear()
        if text:
            self.open_db()
            self.c.execute(f'insert into messenger values ({self.date},"{self.name}", "이상복", curtime(), "{text}", "n");')
            self.conn.commit()
            self.conn.close()
        self.reset_page5()

    # page5 이동시 초기화
    def reset_page5(self):
        self.list_page5.clear()
        self.open_db()
        self.c.execute(f'select 보냄, 시간, 내용 from messenger where 날짜 > subdate({self.date},1) and (보냄 ="{self.name}" or 받음="{self.name}") order by 날짜;')
        message = self.c.fetchall()
        for i in message:
            self.list_page5.addItem(f'{i[0]} / {i[1]} / {i[2]}')
        self.conn.close()

    # 페이지4 이동시 초기화
    def reset_page4(self):
        self.open_db()
        # 캘리더 제한하기
        self.c.execute(f'select {self.date},max(날짜) from schedule;')
        date = self.c.fetchone()
        day1 = QDate.fromString(str(date[0]), "yyyy-MM-dd")
        day2 = QDate.fromString(date[1], "yyyy-MM-dd")
        self.calendar_page4.setDateRange(day1, day2)
        self.conn.close()
        self.tableset_page4()

    # page4 일정 삭제 하기
    def output_page4(self):
        row = self.table_page4.currentRow()
        if row >= 0:
            date = self.table_page4.item(row, 0).text()
            text = self.table_page4.item(row, 1).text()
            style1 = QTextCharFormat()
            style1.setBackground(Qt.white)
            cal_st = QDate.fromString(date, "yyyy-MM-dd")
            self.calendar_page4.setDateTextFormat(cal_st, style1)
            self.open_db()
            self.c.execute(f'delete from calendar where 일정 ="{date}" and 내역 = "{text}" and 이름 = "{self.name}";')
            self.conn.commit()
            self.conn.close()
            self.tableset_page4()

    # page4 일정 추가 버튼 누를면 일정 추가 하고 리스트 보기 셋팅
    def input_page4(self):
        text = self.le_input_page4.text()
        date = self.calendar_page4.selectedDate().toString('yyyy-MM-dd')
        self.open_db()
        if text:
            self.c.execute(f'insert into calendar values (now(),"{self.name}", "{date}", "{text}");')
        self.conn.commit()
        self.conn.close()
        self.le_input_page4.clear()
        self.tableset_page4()

    # page4 리스트 보기 table widget 셋팅 + 캘린더 스타일 변경 추가
    def tableset_page4(self):
        self.open_db()
        # 리스트 보기
        self.c.execute(f'select count(*) from calendar where 이름 ="{self.name}" and 일정 > subdate({self.date},1)')
        num = self.c.fetchone()[0]
        if num:
            # 캘린더 스타일 변경
            style1 = QTextCharFormat()
            style1.setBackground(Qt.yellow)
            self.c.execute(f'select 일정, 내역 from calendar where 이름 ="{self.name}" '
                           f'and 일정 > subdate({self.date},1) order by 일정')
            cal = self.c.fetchall()
            self.table_page4.setRowCount(len(cal))
            self.table_page4.setColumnCount(len(cal[0]))
            for idx, le in enumerate(cal):
                cal_st = QDate.fromString(le[0], "yyyy-MM-dd")
                self.calendar_page4.setDateTextFormat(cal_st, style1)
                for j, v in enumerate(le):
                    self.table_page4.setItem(idx, j, QTableWidgetItem(v))
        else:
            self.table_page4.clear()
            self.table_page4.setRowCount(0)
            self.table_page4.setColumnCount(0)
        self.conn.close()

    # 페이지3 이동시 초기화
    def reset_page3(self):
        self.open_db()
        # 출석일 구하기
        self.c.execute(f'select count(*) from attendance where 이름 = "{self.name}" and 출석="y";')
        attendance = self.c.fetchone()[0]
        self.c.execute(f'select count(*) from (select 날짜 from schedule group by 날짜) as t;')
        total = self.c.fetchone()[0]
        self.lb_attendance_rate_page3.setText(f'{attendance}/{total}')
        # 리스트 보여주기
        self.c.execute(f'select 날짜, if(출석 ="y", "출석", "결석") from attendance where 이름 ="{self.name}";')
        p3_calendar = self.c.fetchall()
        self.table_page3.setRowCount(len(p3_calendar))
        self.table_page3.setColumnCount(len(p3_calendar[0]))
        for idx, le in enumerate(p3_calendar):
            for j, v in enumerate(le):
                self.table_page3.setItem(idx, j, QTableWidgetItem(v))
        # 캘린더 제한 하기
        self.c.execute(f'select min(날짜),max(날짜) from attendance where 이름 ="{self.name}";')
        date = self.c.fetchone()
        day1 = QDate.fromString(date[0], "yyyy-MM-dd")
        day2 = QDate.fromString(date[1], "yyyy-MM-dd")
        self.calendar_page3.setDateRange(day1, day2)
        # 캘린더 스타일 변경하기
        style1 = QTextCharFormat()
        style1.setForeground(Qt.black)
        style1.setBackground(Qt.yellow)
        style2 = QTextCharFormat()
        style2.setForeground(Qt.black)
        style2.setBackground(Qt.red)
        for i in p3_calendar:
            if i[1] == '출석':
                cal_st = QDate.fromString(i[0], "yyyy-MM-dd")
                self.calendar_page3.setDateTextFormat(cal_st, style1)
            elif i[1] == '결석':
                cal_st = QDate.fromString(i[0], "yyyy-MM-dd")
                self.calendar_page3.setDateTextFormat(cal_st, style2)
        self.conn.close()

    # 페이지2 이동시 초기화
    def reset_page2(self):
        self.open_db()
        # 출석, 지각, 조퇴, 외출, 결석 수 구하기
        self.c.execute(f'select count(*) from attendance where 이름 = "{self.name}" and 출석="y";')
        attendance = self.c.fetchone()[0]
        self.lb_attendance_page2.setText(f'{attendance}')
        self.c.execute(f'select count(*) from attendance where 이름 = "{self.name}" and "17:00:00"-입실 < 8;')
        self.lb_tardy_num.setText(str(self.c.fetchone()[0]))
        self.c.execute(f'select count(*) from attendance where 이름 = "{self.name}" and 조퇴="y";')
        self.lb_leave_early_page2.setText(str(self.c.fetchone()[0]))
        self.c.execute(f'select count(*) from attendance where 이름 = "{self.name}" and 외출!="";')
        self.lb_outing_page2.setText(str(self.c.fetchone()[0]))
        self.c.execute(f'select count(*) from attendance where 이름 = "{self.name}" and 결석="y";')
        absent = self.c.fetchone()[0]
        self.lb_absent_page2.setText(f'{absent}')
        self.lb_total_absent_num.setText(f'{absent}')
        # 나의 출석률, 과정 진행률 구하기
        self.c.execute(f'select count(*) from (select 날짜 from schedule group by 날짜) as t;')
        total = self.c.fetchone()[0]
        self.c.execute(f'select count(*) from attendance where 이름 = "{self.name}";')
        num = self.c.fetchone()[0]
        self.lb_attendance_rate_page2.setText('%0.1f%%(%d/%d)'%((attendance/total*100), attendance, total))
        self.lb_progress.setText('%0.1f%%(%d/%d)'%((num/total*100), num, total))
        self.bar_attendance.setValue(int(attendance/total*100))
        self.bar_progress.setValue(int(num/total*100))
        self.conn.close()

    # 오늘 수업이 있는지 확인
    def check_schedule(self):
        self.open_db()
        self.c.execute(f'select count(*) from schedule where 날짜 = {self.date};')
        check = self.c.fetchone()
        self.check_class = check[0]
        self.conn.close()

    # 날짜를 기준 으로 수업이 있고 출석부 명단이 없는 경우 출석부 명단 추가
    def roster(self):
        if self.check_class:
            self.open_db()
            self.c.execute(f'select count(*) from attendance where 날짜 = {self.date};')
            today = self.c.fetchone()
            self.c.execute(f'select count(*) from user;')
            user = self.c.fetchone()
            self.c.execute(f'select name from user;')
            user_name = self.c.fetchall()
            if today < user:
                self.c.execute(f'delete from attendance where 날짜 ={self.date} and 퇴실 = "" and 결석 ="n";')
                for i in user_name:
                    self.c.execute(f"insert into attendance values "
                                   f"({self.date}, '{i[0]}', '', '', '', '', 'n','n','n')")
            self.conn.commit()
            self.conn.close()

    # 전날의 출결 결과를 DB에 저장
    def result(self):
        self.open_db()
        self.c.execute(f'select count(*) from attendance where 날짜 = subdate({self.date},1)')
        count = self.c.fetchone()
        if count[0]:
            self.c.execute(f'select name from user;')
            user_name = self.c.fetchall()
            for i in user_name:
                self.c.execute(f'select 퇴실, "16:00:00"-입실, "17:00:00"- 퇴실 '
                               f'from attendance where 날짜 = subdate({self.date},1) and 이름 = "{i[0]}";')
                data = self.c.fetchone()
                # 수업 4시간 이상, 일찍 퇴실, 퇴실을 찍지 않은 경우
                if data[1] >= 4 and data[2] > 0 and data[0] != "":
                    self.c.execute(f'update attendance set 조퇴="y" where 날짜 = subdate({self.date},1) and 이름 = "{i[0]}";')
                # 정상 퇴실, 수업 4시간 이상, 퇴실을 찍지 않은 경우
                elif data[0] >= '17:01:00' and data[1] >= 4 and data[0] != "":
                    self.c.execute(f'update attendance set 출석="y" where 날짜 = subdate({self.date},1) and 이름 = "{i[0]}";')
                # 나머진 결석 처리
                else:
                    self.c.execute(f'update attendance set 결석="y" where 날짜 = subdate({self.date},1) and 이름 = "{i[0]}";')
            self.conn.commit()
        self.conn.close()

    # page1 의 초기 셋팅
    def reset(self):
        self.lb_notice.setText('')
        self.lb_state.setText('입실전')
        self.check_schedule()
        self.roster()
        self.result()
        self.time_set()
        self.early()

    # 외출 버튼 클릭시 DB에 시간 저장
    def outing(self):
        self.open_db()
        if self.lb_comeback.text() == '':
            self.c.execute(f'update attendance set 외출 = {self.time} where 이름 = "{self.name}" and 날짜 = {self.date};')
        self.conn.commit()
        self.conn.close()

    # 출석 체크시 DB에 시간 저장
    def check(self):
        state = self.pb_check.text()
        self.open_db()
        if state == '입실':
            self.c.execute(f'update attendance set 입실 = {self.time} where 이름 = "{self.name}" and 날짜 = {self.date};')
        elif state == '복귀':
            self.c.execute(f'update attendance set 복귀 = {self.time} where 이름 = "{self.name}" and 날짜 = {self.date};')
        elif state == '퇴실':
            self.c.execute(f'update attendance set 퇴실 = {self.time} where 이름 = "{self.name}" and 날짜 = {self.date};')
        self.conn.commit()
        self.conn.close()
        if state == '입실':
            self.schadule.show()

    # 출석 체크를 위해 시간및 버튼의 텍스트 변경
    def push_chang(self):
        if self.check_class:
            self.open_db()
            self.c.execute(f'select 입실, 외출, 복귀, 퇴실 from attendance where 날짜 = {self.date} and 이름 = "{self.name}";')
            self.state = self.c.fetchone()
            self.lb_entrance.setText(self.state[0])
            self.lb_outing.setText(self.state[1])
            self.lb_comeback.setText(self.state[2])
            self.lb_leave.setText(self.state[3])
            # 입실 체크 전인 경우
            if self.state[0] == '':
                self.lb_state.setText('입실전')
                self.pb_outing.hide()
                self.pb_check.show()
            # 퇴실한 경우
            elif self.state[3] != '':
                self.lb_state.setText('퇴실')
                self.pb_outing.hide()
                self.pb_check.hide()
            # 외출 중인 경우
            elif self.state[1] != '' and self.state[2] == '':
                self.lb_state.setText('외출')
                self.pb_check.setText('복귀')
                self.pb_outing.hide()
            # 외출후 복귀 한 경우
            elif self.state[1] != '' and self.state[2] != '':
                self.lb_state.setText('입실')
                self.pb_check.setText('퇴실')
                self.pb_outing.hide()
                self.conn.commit()
            # 입실한 경우
            elif self.state[0] != '':
                self.lb_state.setText('입실')
                self.pb_check.setText('퇴실')
                self.pb_outing.show()
            self.conn.close()
        else:
            self.lb_state.setText('수업 없음')
            self.pb_outing.hide()
            self.pb_check.show()
            self.lb_entrance.setText('')
            self.lb_outing.setText('')
            self.lb_comeback.setText('')
            self.lb_leave.setText('')

    # 전체 공지
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

    # 금일 수업 시간 라벨에 넣기
    def time_set(self):
        if self.check_class:
            self.open_db()
            self.c.execute(f'select min(시간), max(시간) from schedule where 날짜 = {self.date};')
            date = self.c.fetchone()
            mindate = date[0]
            maxdate = date[1]
            self.c.execute(f'select {self.date};')
            today = self.c.fetchone()
            self.lb_training.setText(f'{today[0]} {mindate.split("~")[0]} ~ {maxdate.split("~")[1]}')
            self.conn.close()
        else:
            self.lb_training.setText(f'')

    # 홈 에서 다른 스텍 으로 이동 하기
    def page_move(self):
        page = self.cb_menu.currentText()
        self.cb_menu.setCurrentIndex(0)
        if page == '...':
            self.push_chang()
            self.stackedWidget.setCurrentIndex(0)
        elif page == '나의 출결 및 진도 현황':
            self.reset_page2()
            self.stackedWidget.setCurrentIndex(1)
        elif page == '나의출석보기':
            self.reset_page3()
            self.stackedWidget.setCurrentIndex(2)
        elif page == '개인 일정':
            self.reset_page4()
            self.stackedWidget.setCurrentIndex(3)
        elif page == '메신저':
            self.reset_page5()
            self.stackedWidget.setCurrentIndex(4)

    # 홈 이외의 창에서 홈 버튼을 누르면 홈 으로 이동
    def go_home(self):
        self.stackedWidget.setCurrentIndex(0)

    # mani.py 에서 사용자 이름 가져 오기
    def set_information(self, name):
        self.name = name

    # DB 연결 하기
    def open_db(self):
        self.conn = p.connect(host='127.0.0.1', port=3306, user='root', password='0000', db='step6', charset='utf8')
        self.c = self.conn.cursor()


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     myWindow = User()
#     myWindow.show()
#     app.exec_()

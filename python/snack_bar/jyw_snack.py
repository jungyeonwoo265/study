
import sys

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pymysql as p
import datetime as dt
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread
import time
import random

snack_bar = uic.loadUiType("snack_bar.ui")[0]
matplotlib.rc('font', family='Malgun Gothic')

# db 연결용 정보
hos = 'localhost'
use = 'root'
pw = '0000'


class Thread(QThread):
    def __init__(self, windowclass):
        super().__init__(windowclass)
        self.p = windowclass
        self.requesr_list = list()
        self.show_question()
        # self.refill_detail()
        self.p.show_inventory()
        self.p.max_sales()

    def open_db(self):
        self.conn = p.connect(host=hos, user=use, password=pw, db='snack', charset='utf8')
        self.c = self.conn.cursor()

    # 주문 금액 재무db에 저장하기
    def income(self):
        self.open_db()
        self.c.execute(f"select sum(금액), min(시간) from request where 주문번호 = '{self.store}';")
        income = self.c.fetchall()[0]
        self.c.execute(f"select 잔액 from finance order by 주문번호 desc")
        balance = self.c.fetchone()[0]
        if income[0]:
            self.c.execute(
                f"insert into finance values ({self.store},'{self.user[0]}님 구매',{income[0]},0,{balance + int(income[0])},'{income[1]}')")
            self.conn.commit()
        self.conn.close()

    # 주문 상품 bom 재고 차감
    def deduction(self):
        self.open_db()
        for v in self.requesr_list:
            self.c.execute(f"select 재료, 수량*{v[1]} as 소모량 from bom where 상품명='{v[0]}';")
            consumption = self.c.fetchall()
            for i in consumption:
                self.c.execute(f"update inventory set 수량 = 수량 - {i[1]} where 재료 ='{i[0]}';")
                self.conn.commit()
        self.conn.close()
        self.ordering()
        self.p.max_sales()

    # 식재료 자동 구매 기능
    def ordering(self):
        self.open_db()
        self.c.execute(
            f'select a.재료, if(max(a.수량)*10 > min(b.수량), "구매", "보류"), min(b.단가) '
            f'from bom a left join inventory b on a.재료 = b.재료 group by 재료;')
        article = self.c.fetchall()
        article_list = list()
        # 재료 구매 list 작성 및 재료 구매 쿼리문 작성
        for i in article:
            if i[1] == '구매':
                self.c.execute(f'update inventory set 수량 = 수량 + 구매량 where 재료 ="{i[0]}";')
                article_list.append([i[0], i[2]])
                self.conn.commit()
        # 재무표에 구매 list 추가
        if article_list:
            for i in article_list:
                self.c.execute(f'SELECT 주문번호, 잔액 FROM finance order by 주문번호 desc;')
                fin = self.c.fetchone()
                self.c.execute(
                    f'insert into finance values("{fin[0] + 1}","{i[0]}구매",0,{i[1]},{fin[1] - i[1]},now());')
                self.conn.commit()
            # 재고현황 및 재료 발주내역 수정
            self.p.show_inventory()
            self.refill_detail()
            # 재료 구매 알람
            self.p.auto_refill.show()
            time.sleep(2)
            self.p.auto_refill.hide()
        self.conn.close()

    # 재료 발주 내역 보여 주기
    def refill_detail(self):
        self.p.inventorylist_2.setRowCount(0)
        self.c.execute(f'select 주문번호, 내역, 시간 from finance where 지출 != 0 and 시간 > curdate() order by 주문번호 desc;')
        refill_list = self.c.fetchall()
        self.p.inventorylist_2.setRowCount(len(refill_list))
        self.p.inventorylist_2.setColumnCount(len(refill_list[0]))
        self.p.inventorylist_2.setHorizontalHeaderLabels(['주문번호', '내역', '시간'])
        for i in range(len(refill_list)):
            for j in range(len(refill_list[i])):
                self.p.inventorylist_2.setItem(i, j, QTableWidgetItem(str(refill_list[i][j])))


    # 문의사항(댓글) 자동등록 기능
    def comment(self):
        com = ['잘먹을게요',
               '많이파세요',
               '좋은 재료 쓰시나봐요',
               '다시 구매 합니다.',
               '혹시 서비스 있나요?']
        self.time = dt.datetime.now()
        self.today = self.time.strftime('%Y-%m-%d %H:%M:%S')
        self.open_db()
        # 로그인된 고객의 아이디와 문의내용을 저장시켜준다
        for i in self.requesr_list:
            # 주문번호, 상품,. 아이디, 내용, 시간, 답변
            self.c.execute(f"insert into question values"
                           f"('{self.store}','{i[0]}','{self.user[0]}','{random.choice(com)}','{self.today}','');")
        self.conn.commit()
        self.conn.close()
        # 문의한 내용을 바로 보여주기
        self.show_question()
        # 문의 등록 알람
        self.p.question_auto.show()
        time.sleep(2)
        self.p.question_auto.hide()

    # 문의 게시판 갱신
    def show_question(self):
        self.open_db()
        self.c.execute("select * from snack.question;")
        self.questionlist = self.c.fetchall()
        if self.questionlist:
            self.p.manager_question_view.setRowCount(len(self.questionlist))
            self.p.manager_question_view.setColumnCount(len(self.questionlist[0]))
            self.p.manager_question_view.setHorizontalHeaderLabels(['주문번호', '상품', '아이디', '내용', '시간', '답변'])
            for i in range(len(self.questionlist)):
                for j in range(len(self.questionlist[i])):
                    self.p.manager_question_view.setItem(i, j, QTableWidgetItem(str(self.questionlist[i][j])))
            self.p.manager_question_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.conn.close()

    # 테스트 기능 (자동 주문 및 자동 댓글 작성)
    def run(self):
        while True:
            print(1)
            self.requesr_list = list()
            menu_list = list()
            self.open_db()
            # 메뉴 제품명, 가격 불러오기
            self.c.execute(f"select 상품, 단가 from menu")
            menu = self.c.fetchall()
            # 중복 메뉴 석택을 없애기 위해 list로 변경
            for i in menu:
                menu_list.append([i[0], i[1]])
            # 랜덤 으로 주문 종류수 선택
            menu_num = random.randint(1, len(menu))
            # 주문서 만들기
            for i in range(menu_num):
                # 중복되지 않게 랜덤 으로 메뉴 선택하기
                menu_infor = random.choice(menu_list)
                menu_list.pop(menu_list.index(menu_infor))
                # 랜덤 으로 메뉴 수량 구하기
                order_num = random.randrange(1, 4)
                # request_list [제품명, 수량 , 가격]
                self.requesr_list.append([menu_infor[0], order_num, menu_infor[1]])
            # 주문번호 구하기
            self.open_db()
            self.c.execute(f'select 주문번호 from finance order by 주문번호 desc;')
            self.store = self.c.fetchone()[0] + 1
            # 랜덤 으로 아이디 선택
            self.c.execute(f'select 아이디 from user where 사업자 = "개인";')
            name = self.c.fetchall()
            self.user = random.choice(name)
            # 주문 내역 등록하기
            for i, v in enumerate(self.requesr_list):
                self.c.execute(f"insert into request values('{self.store}','{self.user[0]}','{v[0]}','{v[1]}','{v[2]}', now());")
            self.conn.commit()
            self.conn.close()
            # 주문 알람
            self.p.order_alram.show()
            time.sleep(2)
            self.p.order_alram.hide()
            # 수입 등록
            self.income()
            # 재고 차감
            self.deduction()
            # 문의사항 등록
            self.comment()
            num = random.randrange(10, 15)
            time.sleep(num)


class WindowClass(QMainWindow, snack_bar):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 첫 페이지 고정
        self.stackedWidget.setCurrentIndex(0)
        # 테스트 기능 동장
        self.thread_action()
        # 로그인후 들어가기 버튼 클릭시 주문창으로 이동
        self.mainpage_button.clicked.connect(self.mainpage)
        # 첫 페이지의 회원가입 버튼클릭시 회원가입창으로 이동
        self.signup_main_button.clicked.connect(self.signup_page)
        # 회원가입 페이지속 취소 버튼클릭시 첫 화면으로 이동
        self.signup_cancle_button.clicked.connect(self.homepage)
        # 회원가입 페이지속 확인 버튼클릭시 로그인화면으로 이동
        self.signup_confirm_button.clicked.connect(self.signup)
        # 회원가입 페이지속 중복확인 버튼클릭시 중복확인함수 실행
        self.overlap_button.clicked.connect(self.double_check)

        # 구매자가 문의하기 페이지속 문의하기 버튼클릭시 게시글 업로드
        self.question_add_button.clicked.connect(self.show_combo)
        # 구매자가 문의하기 페이지속 취소하기 버튼클릭시 메인화면으로 이동
        self.question_cancle_button.clicked.connect(self.mainpage)
        # 구매자의 장바구니 속 취소버튼 클릭시 메인페이지로 이동
        self.payment_cancle_button.clicked.connect(self.mainpage)
        # 구매자의 메인페이지속 문의하기 버튼클릭시 문의게시판으로 이동
        self.question_button.clicked.connect(self.question)
        # 구매자의 메인페이지속 장바구니 버튼클릭시 장바구니 게시판으로 이동
        self.shopping_button.clicked.connect(self.shopping_basket)
        # 구매자의 장바구니페이지속 취소 버튼클릭시 메인페이지로 이동
        self.payment_cancle_button.clicked.connect(self.mainpage)
        # 구매자의 메인페이지속 로그아웃 버튼클릭시 로그인화면으로 이동
        self.logout_main_button.clicked.connect(self.homepage)
        # 구매자의 장바구니속 테이블위젯 클릭시 삭제를 위한 함수실행-------------
        self.tableWidget_2.cellDoubleClicked.connect(self.del_request)
        self.shopping_list_del.clicked.connect(self.del_request)
        # 구매자의 장바구니속 주문하기 버튼클릭시 주문서로 이동시키는 함수실행
        self.payment_button.clicked.connect(self.purchase)

        # 관리자메인페이지의 문의함보기 버튼클릭시 문의하기 게시판으로 이동
        self.manager_question.clicked.connect(self.question_view)
        # 관리자 문의하기테이블위젯속 셀 클릭시 내용호출을 위한 함수실행 ----------------
        self.manager_question_view.cellClicked.connect(self.cellclicked_event)
        self.manager_question_view.cellDoubleClicked.connect(self.cellclicked_event)
        # 관리자의 문의하기 게시판속 삭제하기 버튼클릭시 게시글삭제함수 실행
        self.manager_sales_del.clicked.connect(self.manager_question_del)
        # 관리자의 문의하기 게시판속 답변달기 버튼클릭시 게시글추가함수 실행
        self.manager_sales_add.clicked.connect(self.manager_question_add)
        # 관리자의 문의하기 게시판 속 취소 버튼클릭시 관리자메인페이지 이동
        self.logout_manager_button_3.clicked.connect(self.manager_page)

        # 관리자메인페이지속 매출확인 버튼클릭시 매출확인 게시판으로 이동
        self.manager_sales.clicked.connect(self.showgraph)
        # 관리자매출확인페이지속 취소 버튼클릭시 관리자메인페이지로 이동
        self.salesback_button.clicked.connect(self.show_back_b)

        # 관리자메인페이지속 재고관리 버튼클릭시 재고관리 게시판으로 이동
        self.manager_inventory.clicked.connect(self.inventory_view)
        # 관리자재고관리페이지속 취소버튼 클릭시 관리자메인 페이지로 이동
        self.back_button.clicked.connect(self.manager_page)

        # 관리자의 메인페이지속 로그아웃 버튼클릭시 로그인화면으로 이동
        self.logout_manager_button.clicked.connect(self.homepage)

        # 새메뉴에 필요한 재료 넣는 리스트인데 메서드에 넣으면 거기 메서드갈때마다 초기화되서 과감히 init에 넣음
        self.store_ingredient = []
        # 신제품추가 버튼가면 신제품페이지로 이동
        self.manager_sales_2.clicked.connect(self.adde_screen)
        # 기존 메뉴 재료들 검색
        self.food_search.clicked.connect(self.add_food)
        # 신메뉴에 들어갈 재료 더블클릭시 단위랑 재료이름 옆으로 들어감
        self.ingredient.cellDoubleClicked.connect(self.add_ingredient)
        # 아래에 재료 추가됨
        self.add_btn.clicked.connect(self.plus_ingredient)
        # 뒤로가기로 관리자 페이지 처음으로 이동함
        self.cancel_btn.clicked.connect(self.clearMode)
        # 신메뉴 등록됨
        self.confirm_btn.clicked.connect(self.confirm_food)
        # 알람 라벨 숨기기
        self.order_alram.hide()
        self.auto_refill.hide()
        self.question_auto.hide()

    # 스레드 동작(테스트 기능 및 알람, 게시판 실시간 수정)
    def thread_action(self):
        t = Thread(self)
        t.start()

    # 홈페이지 첫화면
    def homepage(self):
        self.stackedWidget.setCurrentIndex(0)
        self.id_check.clear()
        self.name_check.clear()
        self.pw_check.clear()
        self.pw2_check.clear()
        self.add_check.clear()
        self.phon_check.clear()
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.kimbap_plus.setValue(0)
        self.tuna_kimbap_plus_2.setValue(0)
        self.Cheese_kimbap_plus_2.setValue(0)
        self.bokki_plus_3.setValue(0)
        self.rabokki_plus_3.setValue(0)
        self.Cheese_bokki_plus.setValue(0)
        self.pig_Stew_plus_3.setValue(0)
        self.tuna_Stew_plus.setValue(0)
        self.tableWidget_2.clear()
        self.stackedWidget.setCurrentIndex(0)

    # db 연결 메서드
    def open_db(self):
        self.conn = p.connect(host=hos, user=use, password=pw, db='snack', charset='utf8')
        self.c = self.conn.cursor()

    # 회원가입 메서드
    def signup(self):
        # 빈칸 확인
        if self.id_check.text() == '' or self.name_check.text() == '' or self.pw_check.text() == '' or \
                self.pw2_check.text() == '' or self.add_check.text() == '' or self.phon_check.text() == '':
            QMessageBox.critical(self, "에러", "빈칸을 전부 입력해주세요")
        # 비밀번호, 비밀번호 확인 비교
        elif self.pw_check.text() != self.pw2_check.text():
            QMessageBox.critical(self, "에러", "비밀번호와 비밀번호확인이 일치하지 않습니다.")
        # 아이디 중복 체크 유무 확인
        elif bool(self.login_okay) == False:
            QMessageBox.critical(self, "에러", "중복확인을 해주세요")
        # 사업자, 개인 선택 유무 확인
        elif bool(self.buyer_Confirm_button.isChecked()) == False and bool(
                self.seller_Confirm_button.isChecked()) == False:
            QMessageBox.critical(self, "에러", "사업자 또는 개인 선택해주세요")
        # 입력 상태 양호
        else:
            information = 'a'
            # 개인 선택
            if self.buyer_Confirm_button.isChecked():
                information = self.buyer_Confirm_button.text()
            # 사업자 선택
            elif self.seller_Confirm_button.isChecked():
                information = self.seller_Confirm_button.text()
            # user db에 회원정보 등록
            self.open_db()
            self.c.execute(f'INSERT INTO user (아이디, 비밀번호, 이름, 주소, 전화번호, 사업자) VALUES'
                           f' ("{self.id_check.text()}", "{self.pw_check.text()}", "{self.name_check.text()}",'
                           f' "{self.add_check.text()}", "{self.phon_check.text()}", "{information}")')
            self.conn.commit()
            self.conn.close()
            QMessageBox.information(self, "확인", "회원가입에 성공하셨습니다")
            # 회원 가입 lineedit 초기화
            self.id_check.clear()
            self.name_check.clear()
            self.pw_check.clear()
            self.pw2_check.clear()
            self.add_check.clear()
            self.phon_check.clear()
            # 로그인 페이지로 이동
            self.stackedWidget.setCurrentIndex(0)

    # id 중복 확인
    def double_check(self):
        self.open_db()
        # 아이디 중복 확인
        self.c.execute(f'SELECT 아이디 FROM user WHERE 아이디 = "{self.id_check.text()}"')
        checking = self.c.fetchall()
        self.conn.close()
        # 아이디 미입력
        if self.id_check.text() == '':
            QMessageBox.critical(self, "에러", "아이디를 입력해주세요")
        # 아이디 중복
        elif checking != ():
            QMessageBox.critical(self, "에러", "중복된 아이디 입니다")
        # 아이디 사용 가능
        else:
            QMessageBox.information(self, "확인", "사용가능한 아이디입니다")
            self.login_okay = True
            # 아이디 lineedit에 내용 변경시 다시 중복 확인하게 하기
            self.id_check.textChanged.connect(self.signup_page)

    # 회원가입 페이지 이동
    def signup_page(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.login_okay = False
        self.stackedWidget.setCurrentIndex(1)


    # 로그인 하기 및 개인, 사업자 초기 화면 이동
    def mainpage(self):
        self.open_db()
        self.c.execute(f'SELECT 아이디, 사업자 FROM user WHERE'
                       f' 아이디 = "{self.lineEdit.text()}" and 비밀번호 = "{self.lineEdit_2.text()}"')
        self.login_infor = self.c.fetchall()
        self.conn.close()
        if self.login_infor == ():
            QMessageBox.critical(self, "에러", "아이디나 비밀번호가 틀립니다.")
        else:
            if self.login_infor[0][1] == '개인':
                QtWidgets.QMessageBox.about(self, " ", "개인회원은 사용할수없습니다.")
                self.stackedWidget.setCurrentIndex(0)
            elif self.login_infor[0][1] == '사업자':
                self.manager_page()

    # 개인 문의하기 게시판
    def question(self):
        pass
        # self.stackedWidget.setCurrentIndex(3)
        # self.open_db()
        # self.c.execute("select 주문번호,아이디,내용,시간,답변 from snack.question;")
        # self.questionlist = self.c.fetchall()
        # if self.questionlist:
        #     self.QandA_list.setRowCount(len(self.questionlist))
        #     self.QandA_list.setColumnCount(len(self.questionlist[0]))
        #     self.QandA_list.setHorizontalHeaderLabels(['주문번호', '아이디', '내용', '시간', '답변'])
        #     for i in range(len(self.questionlist)):
        #         for j in range(len(self.questionlist[i])):
        #             self.QandA_list.setItem(i, j, QTableWidgetItem(str(self.questionlist[i][j])))
        #     # self.QandA_list.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        #     self.QandA_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.conn.close()

    # 개인이 문의하기 게시판에 글 등록 하기
    def question_add(self):
        pass
    #     self.time = dt.datetime.now()
    #     self.today = self.time.strftime('%Y-%m-%d %H:%M:%S')
    #     check = QMessageBox.question(self, ' ', '등록 하겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
    #     # 등록여부를 물어본뒤 ok 버튼을 눌렀을때
    #     if check == QMessageBox.Yes:
    #         self.open_db()
    #         # 로그인된 고객의 아이디와 문의내용을 저장시켜준다
    #         self.c.execute(f"insert into snack.question (아이디,내용,시간) values "
    #                        f"('{self.login_infor[0][0]}','{self.QandA_lineEdit.text()}','{self.today}')")
    #         self.conn.commit()
    #         QMessageBox.information(self, ' ', '문의가 등록되었습니다.')
    #         # 문의한 내용을 리스트로 바로 보여주기 위한 커서
    #         self.c.execute("select 주문번호,아이디,내용,시간,답변 from snack.question")
    #         self.questionlist = self.c.fetchall()
    #         self.QandA_list.setRowCount(len(self.questionlist))
    #         self.QandA_list.setColumnCount(len(self.questionlist[0]))
    #         self.QandA_list.setHorizontalHeaderLabels(['주문번호', '아이디', '내용', '시간', '답변'])
    #         for i in range(len(self.questionlist)):
    #             for j in range(len(self.questionlist[i])):
    #                 self.QandA_list.setItem(i, j, QTableWidgetItem(str(self.questionlist[i][j])))
    #         self.QandA_list.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    #         self.QandA_lineEdit.clear()
    #
    #     else:
    #         # 문의하기를 취소했을 경우
    #         QMessageBox.information(self, ' ', '상품주문으로 돌아갑니다.')
    #     self.conn.close()

    # 사업자 재고확인하기
    def inventory_view(self):
        self.show_inventory()
        self.stackedWidget.setCurrentIndex(4)

    # 재고 현황 보여주기
    def show_inventory(self):
        head = ['재료', '수량', '단위']
        self.inventorylist.setRowCount(0)
        # self.inventorylist.setColumnCount(0)
        self.open_db()
        self.c.execute(f"select 재료,수량,단위 from inventory;")
        inven = self.c.fetchall()
        self.inventorylist.setRowCount(len(inven))
        self.inventorylist.setColumnCount(len(inven[0]))
        for i, le in enumerate(inven):
            for j, v in enumerate(le):
                self.inventorylist.setItem(i, j, QTableWidgetItem(str(v)))
        for i, v in enumerate(head):
            self.inventorylist.setHorizontalHeaderItem(i, QTableWidgetItem(v))
        self.conn.close()

    # 장바구니
    def shopping_basket(self):
        pass
        # self.total_bill = 0
        # self.request_list = []
        # # 장바구니에서 메뉴고르는 페이지로 돌아왔을때 다 0으로 초기화해주면 다시 고르려는것도 사라지니까 이거 생각좀 해야할듯
        #
        # if self.kimbap_plus.value() != 0:
        #     self.request_list.append(['김밥', str(self.kimbap_plus.value()),
        #                               str(self.kimbap_plus.value() * 9000)])
        # if self.tuna_kimbap_plus_2.value() != 0:
        #     self.request_list.append(['참치김밥', str(self.tuna_kimbap_plus_2.value()),
        #                               str(self.tuna_kimbap_plus_2.value()*11000)])
        # if self.Cheese_kimbap_plus_2.value() != 0:
        #     self.request_list.append(['치즈김밥', str(self.Cheese_kimbap_plus_2.value()),
        #                               str(self.Cheese_kimbap_plus_2.value() * 11000)])
        # if self.bokki_plus_3.value() != 0:
        #     self.request_list.append(['떡볶이', str(self.bokki_plus_3.value()),
        #                               str(self.bokki_plus_3.value() * 15000)])
        # if self.rabokki_plus_3.value() != 0:
        #     self.request_list.append(['라볶이', str(self.rabokki_plus_3.value()),
        #                               str(self.rabokki_plus_3.value() * 17000)])
        # if self.Cheese_bokki_plus.value() != 0:
        #     self.request_list.append(['치즈떡볶이', str(self.Cheese_bokki_plus.value()),
        #                               str(self.Cheese_bokki_plus.value() * 17000)])
        # if self.pig_Stew_plus_3.value() != 0:
        #     self.request_list.append(['돼지김치찌개', str(self.pig_Stew_plus_3.value()),
        #                               str(self.pig_Stew_plus_3.value() * 14000)])
        # if self.tuna_Stew_plus.value() != 0:
        #     self.request_list.append(['참치김치찌개', str(self.tuna_Stew_plus.value()),
        #                               str(self.tuna_Stew_plus.value()*18000)])
        # self.stackedWidget.setCurrentIndex(5)
        # if self.request_list != []:
        #     self.tablesetting()
        # else:
        #     self.bill_result.setText("총액:0원")
        #     self.tableWidget_2.clear()

    # 주문내역 등록하기
    def purchase(self):
        pass
        # now = datetime.now()
        # self.open_db()
        # self.c.execute(f'select 주문번호 from finance order by 주문번호 desc')
        # store = self.c.fetchall()
        # for i in range(len(self.request_list)):
        #     self.c.execute(f'insert into request (주문번호, 아이디, 상품명, 수량, 금액, 시간) values ("{store[0][0]+1}", "{self.login_infor[0][0]}", "{self.request_list[i][0]}", "{self.request_list[i][1]}", "{self.request_list[i][2]}", now())')
        # self.conn.commit()
        # self.conn.close()
        # QMessageBox.information(self, "확인", "주문이 접수되었습니다")
        # self.kimbap_plus.setValue(0)
        # self.tuna_kimbap_plus_2.setValue(0)
        # self.Cheese_kimbap_plus_2.setValue(0)
        # self.bokki_plus_3.setValue(0)
        # self.rabokki_plus_3.setValue(0)
        # self.Cheese_bokki_plus.setValue(0)
        # self.pig_Stew_plus_3.setValue(0)
        # self.tuna_Stew_plus.setValue(0)
        # self.stackedWidget.setCurrentIndex(2)

    # 사업자용 메인화면
    def manager_page(self):
        # 주문 내역 불러 오기
        self.open_db()
        self.c.execute('select * from request')
        list_request = self.c.fetchall()
        self.conn.close()
        # 주문 내역이 있으면
        if list_request != ():
            self.order_confirmation.setRowCount(len(list_request))
            self.order_confirmation.setColumnCount(len(list_request[0]))
            self.order_confirmation.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.order_confirmation.setHorizontalHeaderLabels(['주문번호', '아이디', '상품명', '수량', '금액', '시간'])
            for i in range(len(list_request)):
                for j in range(len(list_request[0])):
                    self.order_confirmation.setItem(i, j, QTableWidgetItem(list_request[i][j]))
        self.stackedWidget.setCurrentIndex(7)

    # 사업자 문의함 확인하기
    def question_view(self):
        self.stackedWidget.setCurrentIndex(8)
        # self.open_db()
        # # 구매자가 남긴 문의게시판을 보여준다
        # self.c.execute("select 주문번호,아이디,내용,시간,답변 from snack.question;")
        # self.questionlist = self.c.fetchall()
        # if self.questionlist:
        #     self.manager_question_view.setRowCount(len(self.questionlist))
        #     self.manager_question_view.setColumnCount(len(self.questionlist[0]))
        #     self.manager_question_view.setHorizontalHeaderLabels(['주문번호', '아이디', '내용', '시간', '답변'])
        #     for i in range(len(self.questionlist)):
        #         for j in range(len(self.questionlist[i])):
        #             self.manager_question_view.setItem(i, j, QTableWidgetItem(str(self.questionlist[i][j])))
        #     # self.manager_question_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        #     self.manager_question_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.conn.close()

    # 장바구니 삭제 하기
    def del_request(self):
        pass
        # QMessageBox.information(self, "확인", "장바구니에서 삭제합니다")
        # list_row = self.tableWidget_2.currentRow()
        # del_list = self.request_list[list_row]
        # cancel_re = int(self.request_list[list_row][1]) - 1
        # if self.request_list[list_row][0] == '김밥':
        #     self.kimbap_plus.setValue(cancel_re)
        #     self.request_list[list_row][2] = str(self.kimbap_plus.value()*9000)
        # elif self.request_list[list_row][0] == '참치김밥':
        #     self.tuna_kimbap_plus_2.setValue(cancel_re)
        #     self.request_list[list_row][2] = str(self.tuna_kimbap_plus_2.value()*11000)
        # elif self.request_list[list_row][0] == '치즈김밥':
        #     self.Cheese_kimbap_plus_2.setValue(cancel_re)
        #     self.request_list[list_row][2] = str(self.Cheese_kimbap_plus_2.value() * 11000)
        # elif self.request_list[list_row][0] == '떡볶이':
        #     self.bokki_plus_3.setValue(cancel_re)
        #     self.request_list[list_row][2] = str(self.bokki_plus_3.value() * 15000)
        # elif self.request_list[list_row][0] == '라볶이':
        #     self.rabokki_plus_3.setValue(cancel_re)
        #     self.request_list[list_row][2] = str(self.rabokki_plus_3.value() * 17000)
        # elif self.request_list[list_row][0] == '치즈떡볶이':
        #     self.Cheese_bokki_plus.setValue(cancel_re)
        #     self.request_list[list_row][2] = str(self.Cheese_bokki_plus.value() * 17000)
        # elif self.request_list[list_row][0] == '돼지김치찌개':
        #     self.pig_Stew_plus_3.setValue(cancel_re)
        #     self.request_list[list_row][2] = str(self.pig_Stew_plus_3.value() * 14000)
        # elif self.request_list[list_row][0] == '참치김치찌개':
        #     self.tuna_Stew_plus.setValue(cancel_re)
        #     self.request_list[list_row][2] = str(self.tuna_Stew_plus.value()*18000)
        # self.request_list[list_row][1] = str(cancel_re)
        # if cancel_re == 0:
        #     self.request_list.remove(del_list)
        # if self.request_list != []:
        #     self.tablesetting()
        # else:
        #     self.bill_result.setText("총액:0원")
        #     self.kimbap_plus.setValue(0)
        #     self.tuna_kimbap_plus_2.setValue(0)
        #     self.Cheese_kimbap_plus_2.setValue(0)
        #     self.bokki_plus_3.setValue(0)
        #     self.rabokki_plus_3.setValue(0)
        #     self.Cheese_bokki_plus.setValue(0)
        #     self.pig_Stew_plus_3.setValue(0)
        #     self.tuna_Stew_plus.setValue(0)
        #     self.tableWidget_2.clear()

    # 장바구니 내용 등록하기
    def tablesetting(self):
        pass
    #     self.total_bill = 0
    #     for i in range(len(self.request_list)):
    #         self.total_bill += int(self.request_list[i][2])
    #     totaltext = "총액:" + str(self.total_bill) + "원"
    #     self.bill_result.setText(totaltext)
    #     self.tableWidget_2.setRowCount(len(self.request_list))
    #     self.tableWidget_2.setColumnCount(len(self.request_list[0]))
    #     self.tableWidget_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
    #     self.tableWidget_2.setHorizontalHeaderLabels(['품목', '개수', '금액'])
    #     self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    #     for i in range(len(self.request_list)):
    #         for j in range(len(self.request_list[0])):
    #             self.tableWidget_2.setItem(i, j, QTableWidgetItem(self.request_list[i][j]))

    # 문의함 갱신시 이를 보연주기 위한 함수
    def show_question(self):
        pass
        self.c.execute("select * from snack.question;")
        self.questionlist = self.c.fetchall()
        self.manager_question_view.setRowCount(len(self.questionlist))
        self.manager_question_view.setColumnCount(len(self.questionlist[0]))
        self.manager_question_view.setHorizontalHeaderLabels(['주문번호', '상품명', '아이디', '내용', '시간', '답변'])
        for i in range(len(self.questionlist)):
            for j in range(len(self.questionlist[i])):
                self.manager_question_view.setItem(i, j, QTableWidgetItem(str(self.questionlist[i][j])))
        # self.manager_question_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.manager_question_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    # 관리자가 구매자 문의에 답변을 남기는경우
    def manager_question_add(self):
        # try:
        #     check = QMessageBox.question(self, ' ', '답변 하겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        #     if check == QMessageBox.Yes:
        #         self.open_db()
        #         self.c.execute(f"update snack.question set 답변 ='{self.manager_line_add.text()}' where 내용 = '{self.cellchoice}'")
        #         self.conn.commit()
        #         QMessageBox.information(self, ' ', '답변이 등록되었습니다.')
        #         self.manager_line_add.clear()
        #         # 답변을 실시간으로 보여주기 위한 커서
        #         self.c.execute("select 주문번호,아이디,내용,시간,답변 from snack.question;")
        #         self.questionlist = self.c.fetchall()
        #         self.manager_question_view.setRowCount(len(self.questionlist))
        #         self.manager_question_view.setColumnCount(len(self.questionlist[0]))
        #         self.manager_question_view.setHorizontalHeaderLabels(['주문번호', '아이디', '내용', '시간', '답변'])
        #         for i in range(len(self.questionlist)):
        #             for j in range(len(self.questionlist[i])):
        #                 self.manager_question_view.setItem(i, j, QTableWidgetItem(str(self.questionlist[i][j])))
        #         # self.manager_question_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        #         self.manager_question_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #
        #     else:
        #         # 답변을 달지 않았을 경우
        #         QMessageBox.information(self, ' ', '문의함으로 돌아갑니다.')
        #     self.conn.close()
        # except:
        #     QtWidgets.QMessageBox.about(self, " ", '등록된 문의가 없습니다')

        # 사업자 답변 등록
        try:
            check = QMessageBox.question(self, ' ', '답변 하겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if check == QMessageBox.Yes:
                self.open_db()
                self.c.execute(f"update snack.question set 답변 ='{self.manager_line_add.text()}' where 주문번호 = '{self.date[0]}' and 상품 ='{self.date[1]}'")
                self.conn.commit()
                QMessageBox.information(self, ' ', '답변이 등록되었습니다.')
                self.manager_line_add.clear()
                # 답변을 실시간으로 보여주기
                self.show_question()

            else:
                # 답변을 달지 않았을 경우
                QMessageBox.information(self, ' ', '문의함으로 돌아갑니다.')
            self.conn.close()

        except:
            QtWidgets.QMessageBox.about(self, " ", '등록된 문의가 없습니다')


    # 구매자가 남긴 문의를 삭제를 하는경우
    def manager_question_del(self):
        # try:
        #     check = QMessageBox.question(self, ' ', '삭제 하겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        #     self.manager_line_add.text()
        #     if check == QMessageBox.Yes:
        #         self.open_db()
        #         self.c.execute(f"delete from snack.question where 내용 = '{self.cellchoice}'")
        #         self.conn.commit()
        #         # 삭제를 실시간으로 보여주기 위한 커서
        #         self.c.execute("select * from snack.question;")
        #         self.questionlist = self.c.fetchall()
        #         self.manager_question_view.setRowCount(len(self.questionlist))
        #         self.manager_question_view.setColumnCount(len(self.questionlist[0]))
        #         self.manager_question_view.setHorizontalHeaderLabels(['주문번호', '상품명', '아이디', '내용', '시간', '답변'])
        #         for i in range(len(self.questionlist)):
        #             for j in range(len(self.questionlist[i])):
        #                 self.manager_question_view.setItem(i, j, QTableWidgetItem(str(self.questionlist[i][j])))
        #         # self.manager_question_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        #         self.manager_question_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #     else:
        #         QMessageBox.information(self, ' ', '문의함으로 돌아갑니다.')
        #     self.conn.close()
        # except:
        #     self.stackedWidget.setCurrentIndex(8)
        #     QtWidgets.QMessageBox.about(self, " ", '등록된 문의가 없습니다')

        # 사업자 문의 삭제
        try:
            check = QMessageBox.question(self, ' ', '삭제 하겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            self.manager_line_add.text()
            if check == QMessageBox.Yes:
                self.open_db()
                self.c.execute(f"delete from snack.question where 주문번호 = '{self.date[0]}' and 상품 ='{self.date[1]}'")
                self.conn.commit()
                # 삭제를 실시간으로 보여주기 위한 커서
                self.show_question()
            else:
                QMessageBox.information(self, ' ', '문의함으로 돌아갑니다.')
            self.conn.close()
        except:
            self.stackedWidget.setCurrentIndex(8)
            QtWidgets.QMessageBox.about(self, " ", '등록된 문의가 없습니다')

    # 셀 클릭내용을 받기위한 이벤트 함수
    # def cellclicked_event(self, row, col):
        # print(row, col)
    # 사업자 답변 등록및 문의 삭제를 위해 테이블위젯 값 받아오기
    def cellclicked_event(self, row):
        self.date = list()
        self.date.append(self.manager_question_view.item(row, 0).text())
        self.date.append(self.manager_question_view.item(row, 1).text())
        # self.data = self.manager_question_view.item(row, col)
        # self.cellchoice = self.data.text()

    # 매출 및 수인익 그래프 ,테이블위젯 보여주기
    def showgraph(self):
        date_list = []
        date_price = []
        date_cost = []
        # 날짜별 수입, 지출 총액 구하기
        self.open_db()
        self.c.execute("select 시간 , sum(수입), sum(지출) from (select date(시간) as 시간, 수입, 지출 from snack.finance) as a group by a.시간")
        self.questionlist = self.c.fetchall()
        # 그래프 생성을 위해 날짜, 수입, 지출 list에 넣기
        for i in range(len(self.questionlist)):
            date_list.append(self.questionlist[i][0])
            # for j in range(len(self.questionlist)):
            date_price.append(self.questionlist[i][1])
            date_cost.append(self.questionlist[i][2])


        # for i in range(len(date_list)):
        #     print(date_list[i])
        #
        # for i in range(len(date_price)):
        #     print(date_price[i])
        #
        # for i in range(len(date_cost)):
        #     print(date_cost[i])
        #
        # print(date_list)
        # print(date_price)
        # print(date_cost)

        # 매출 확인 페이지로 이동
        self.stackedWidget.setCurrentIndex(6)
        # self.open_db()
        # self.c.execute("select 시간 , sum(수입), sum(지출) from (select date(시간) as 시간, 수입, 지출 from snack.finance) as a group by a.시간")
        # self.questionlist = self.c.fetchall()

        # 테이블 위젯으로 날짜별 수입, 지출 보여주기
        self.tableWidget.setRowCount(len(self.questionlist))
        self.tableWidget.setColumnCount(len(self.questionlist[0]))
        self.tableWidget.setHorizontalHeaderLabels(['날짜', '수입', '지출'])
        for i in range(len(self.questionlist)):
            for j in range(len(self.questionlist[i])):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(self.questionlist[i][j])))
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 그래프 생성
        self.fig = plt.Figure()
        # self.figpie = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.verticalLayout.addWidget(self.canvas)
        # 막대, 선그래프 1개에 넣기
        ax = self.fig.add_subplot(111)
        # 꺽은선그래프
        ax.plot(date_list, date_cost, 'r', label="순이익")
        # 막대그래프
        ax.bar(date_list, date_price, label="매출액")
        ax.set_title("매출액, 순수익")
        ax.legend()
        self.canvas.draw()

    # 매출 확인 페이지 -> main 페이지 이동
    def show_back_b(self):
        self.verticalLayout.removeWidget(self.canvas)
        self.manager_page()

    # 고객이 문의 등록하기(콤보 박스 추가)
    def show_combo(self):
        pass
        # check = QMessageBox.question(self, ' ', '등록 하겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        # self.time = dt.datetime.now()
        # self.today = self.time.strftime('%Y-%m-%d %H:%M:%S')
        # productlist = ['-','김밥', '참치김밥', '치즈김밥','떡볶이','라볶이','치즈떡볶이','돼지김치찌개','참치김치찌개']
        # show = self.comboBox.currentText()
        # for i in range(len(productlist)):
        #     if show == productlist[i]:
        #         if check == QMessageBox.Yes:
        #             self.open_db()
        #             # 로그인된 고객의 아이디와 문의내용을 저장시켜준다
        #             self.c.execute(f"insert into snack.question (상품,아이디,내용,시간) values "
        #                            f"('{show}','{self.login_infor[0][0]}','{self.QandA_lineEdit.text()}','{self.today}')")
        #             self.conn.commit()
        #             QMessageBox.information(self, ' ', '문의가 등록되었습니다.')
        #
        #         # 문의한 내용을 리스트로 바로 보여주기 위한 커서
        #         self.c.execute("SELECT * from snack.question")
        #         self.questionlist = self.c.fetchall()
        #         self.QandA_list.setRowCount(len(self.questionlist))
        #         self.QandA_list.setColumnCount(len(self.questionlist[0]))
        #         self.QandA_list.setHorizontalHeaderLabels(['상품','주문번호', '아이디', '내용', '시간', '답변'])
        #         for i in range(len(self.questionlist)):
        #             for j in range(len(self.questionlist[i])):
        #                 self.QandA_list.setItem(i, j, QTableWidgetItem(str(self.questionlist[i][j])))
        #         # self.QandA_list.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        #         self.QandA_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #         self.QandA_lineEdit.clear()

    def clearMode(self):                    # 이건 신메뉴 창에 있는 것들 초기화하려고 만든 메서드
        self.ingredient_name.clear()
        self.newrecipe.clear()
        self.new_name.clear()
        self.price.clear()
        self.label_14.setText("재료이름")
        self.unit_label.setText("")
        self.food_name.clear()
        self.cost_label.setText("원가:0원")
        self.ingredient_list.clear()
        self.manager_page()

    # 레시피 등록 및 원가 계산
    def plus_ingredient(self):
        # 레시피 등록 하기(재료, 수량, 단위 등록)
        if self.label_14.text() == '재료이름':
            QMessageBox.critical(self, '에러', '재료를 선택하세요')
        elif self.ingredient_name.text() == '':
            QMessageBox.critical(self, '에러', '수량을 입력하세요')
        # 테이블 위젯에 레시피 등록
        else:
            add_ingredient_list = [self.label_14.text(), self.ingredient_name.text(), self.unit_label.text()]           # 재료이름, 수량, 단위를 리스트에 넣고
            self.store_ingredient.append(add_ingredient_list)                                                           # init에 만들었던 리스트에 다시 담는다
            # 등록 레시피 테이블 위젯으로 보여주기
            self.newrecipe.setRowCount(len(self.store_ingredient))                                                      # 다시 안담으면 계속 쌓여지지않고 초기화됨
            self.newrecipe.setColumnCount(len(self.store_ingredient[0]))
            self.newrecipe.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.newrecipe.setHorizontalHeaderLabels(['재료', '수량', '단위'])
            for i in range(len(self.store_ingredient)):
                for j in range(len(self.store_ingredient[0])):
                    self.newrecipe.setItem(i, j, QTableWidgetItem(str(self.store_ingredient[i][j])))
            # 원가 계산하기
            self.open_db()
            origin_cost = 0
            # 재료별 원가 구해서 레시피 원가 계산하기
            for i in range(len(self.store_ingredient)):
                self.c.execute(
                    f'select 재료, (단가 / 구매량)*{int(self.store_ingredient[i][1])} 가격 from inventory where 재료 = "{self.store_ingredient[i][0]}"')
                a = self.c.fetchall()
                origin_cost += int(a[0][1])
            self.conn.close()
            self.cost_label.setText("원가:" + str(origin_cost) + "원")                                                   # 위에 원가 계산해서 넣어줌


    # bom db에 신제품 레시피 등록하기
    def confirm_food(self):
        # 신제품 등록시 상품명 중복 확인
        self.open_db()
        self.c.execute(f'select 상품 from menu where 상품 = "{self.new_name.text()}"')                      # 메뉴가 중복되지 않게 메뉴리스트를 비교
        product_name = self.c.fetchall()
        self.conn.close()
        # 신제품 이름을 입력했는지 확인
        if self.new_name.text() == '':
            QMessageBox.critical(self, "에러", "상품명을 입력해주세요")
        # 신제품 가격을 입력했는지 확인
        elif self.price.text() == '':
            QMessageBox.critical(self, "에러", "가격을 입력해주세요")
        # 신제품 이름이 중복되는지 확인
        elif product_name != ():
            QMessageBox.critical(self, "에러", "이미 존재하는 메뉴입니다")
        # 신제품 등록하기
        else:
            self.open_db()                                                                            # 위에 쓴 리스트를 다시 사용해 db에 신메뉴 등록
            for i in range(len(self.store_ingredient)):
                self.c.execute(
                    f'insert into bom (상품명, 재료, 수량, 단위) values ("{self.new_name.text()}", "{self.store_ingredient[i][0]}", "{self.store_ingredient[i][1]}", "{self.store_ingredient[i][2]}")')
                self.conn.commit()
            # menu db에 상품 등록
            self.c.execute(
                f'insert into menu (상품, 단가, 단위) values ("{self.new_name.text()}", "{int(self.price.text())}", "개")')
            self.conn.commit()
            self.c.close()
            QMessageBox.information(self, "확인", "메뉴가 등록되었습니다")
            # 신제품 등록 창 초기화
            self.ingredient_name.clear()
            self.newrecipe.clear()
            self.new_name.clear()
            self.price.clear()
            self.cost_label.setText("원가:0원")
            self.label_14.setText("재료이름")
            self.unit_label.setText("")

    # 레시피에 등록할 재료, 단위 표시하기
    def add_ingredient(self):                           # 이건 라벨들에 이름 넣어주기
        row = self.ingredient.currentRow()
        food_name_e = self.ingredient.item(row, 0).text()
        food_unit = self.ingredient.item(row, 2).text()
        self.label_14.setText(food_name_e)
        self.unit_label.setText(food_unit)
        self.ingredient_name.clear()

    # 신제품 추가 페이지로 이동시 초기화
    def adde_screen(self):
        # 재료 수량, 상품 가격 숫자만 입력하게 제한하기
        self.onlyInt = QIntValidator()                  # 수량과 가격에 int형으로만 적을 수 있게 만드는 코드
        self.ingredient_name.setValidator(self.onlyInt)
        self.price.setValidator(self.onlyInt)
        # 재고 재료,수량,단위 불러오기
        self.open_db()
        self.c.execute('select 재료, 수량, 단위 from inventory')
        input_ingredient = self.c.fetchall()
        self.conn.close()
        # 재고 내역 테이블 위젯에 보여주기
        self.ingredient.setRowCount(len(input_ingredient))
        self.ingredient.setColumnCount(len(input_ingredient[0]))
        self.ingredient.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ingredient.setHorizontalHeaderLabels(['재료', '수량', '단위'])
        for i in range(len(input_ingredient)):
            for j in range(len(input_ingredient[0])):
                self.ingredient.setItem(i, j, QTableWidgetItem(str(input_ingredient[i][j])))
        # 신제품 추가하기 페이지로 이동
        self.stackedWidget.setCurrentIndex(9)

    # 등록된 상품 레시피 검색
    def add_food(self):                                     # 기존 메뉴의 bom검색
        # 상품 레시피 검색
        self.open_db()
        self.c.execute(f'select * from bom where 상품명 = "{self.food_name.text()}"')
        need_ingredient = self.c.fetchall()
        self.conn.close()
        # print(need_ingredient)
        # 테이블 위젯에 상품 레시피 보여주기
        self.ingredient_list.setRowCount(len(need_ingredient))
        self.ingredient_list.setColumnCount(len(need_ingredient[0]) - 1)
        self.ingredient_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ingredient_list.setHorizontalHeaderLabels(['재료', '수량', '단위'])
        for i in range(len(need_ingredient)):
            for j in range(len(need_ingredient[0]) - 1):
                self.ingredient_list.setItem(i, j, QTableWidgetItem(str(need_ingredient[i][j + 1])))

    # 상품 최대 생산 수량 확인
    def max_sales(self):
        self.maximum_list.setRowCount(0)
        # self.maximum_list.setColumnCount(0)
        self.open_db()
        self.c.execute(f'select 상품명, min(b.수량 div a.수량) as 최대생산량  from bom a left join inventory b on a.재료 =b.재료 group by 상품명;')
        max_number = self.c.fetchall()
        self.conn.close()
        self.maximum_list.setRowCount(len(max_number))
        self.maximum_list.setColumnCount(len(max_number[0]))
        self.maximum_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.maximum_list.setHorizontalHeaderLabels(['제품', '최대 판매 수량'])
        for i in range(len(max_number)):
            for j in range(len(max_number[0])):
                self.maximum_list.setItem(i, j, QTableWidgetItem(str(max_number[i][j])))
        self.maximum_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()

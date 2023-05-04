import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pymysql as p
import datetime as dt
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtWidgets

snack_bar = uic.loadUiType("snack_bar.ui")[0]
matplotlib.rc('font', family='Malgun Gothic')

# db 연결용 정보
hos = 'localhost'
use = 'root'
pw = '0000'

class WindowClass(QMainWindow, snack_bar):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 첫 페이지 고정
        self.stackedWidget.setCurrentIndex(0)

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

        # 관리자메인페이지속 신제품추가 버튼클릭시 신제품추가 게시판으로 이동
        self.manager_sales_2.clicked.connect(self.addNew)
        self.cancel_btn.clicked.connect(self.manager_page)


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

    def open_db(self):
        self.conn = p.connect(host=hos, user=use, password=pw, db='snack', charset='utf8')
        self.c = self.conn.cursor()

    def signup(self):
        if self.id_check.text() == '' or self.name_check.text() == '' or self.pw_check.text() == '' or \
                self.pw2_check.text() == '' or self.add_check.text() == '' or self.phon_check.text() == '':
            QMessageBox.critical(self, "에러", "빈칸을 전부 입력해주세요")
        elif self.pw_check.text() != self.pw2_check.text():
            QMessageBox.critical(self, "에러", "비밀번호와 비밀번호확인이 일치하지 않습니다.")
        elif bool(self.login_okay) == False:
            QMessageBox.critical(self, "에러", "중복확인을 해주세요")
        elif bool(self.buyer_Confirm_button.isChecked()) == False and bool(
                self.seller_Confirm_button.isChecked()) == False:

            QMessageBox.critical(self, "에러", "사업자 또는 개인 선택해주세요")
        else:
            information = 'a'
            if self.buyer_Confirm_button.isChecked():
                information = self.buyer_Confirm_button.text()
            elif self.seller_Confirm_button.isChecked():
                information = self.seller_Confirm_button.text()
            self.open_db()
            self.c.execute(f'INSERT INTO user (아이디, 비밀번호, 이름, 주소, 전화번호, `사업자`) VALUES'
                           f' ("{self.id_check.text()}", "{self.pw_check.text()}", "{self.name_check.text()}",'
                           f' "{self.add_check.text()}", "{self.phon_check.text()}", "{information}")')
            self.conn.commit()
            self.conn.close()
            QMessageBox.information(self, "확인", "회원가입에 성공하셨습니다")
            self.id_check.clear()
            self.name_check.clear()
            self.pw_check.clear()
            self.pw2_check.clear()
            self.add_check.clear()
            self.phon_check.clear()
            self.stackedWidget.setCurrentIndex(0)

    def double_check(self):
        self.open_db()
        self.c.execute(f'SELECT 아이디 FROM user WHERE 아이디 = "{self.id_check.text()}"')
        checking = self.c.fetchall()
        self.conn.close()
        if self.id_check.text() == '':
            QMessageBox.critical(self, "에러", "아이디를 입력해주세요")
        elif checking != ():
            QMessageBox.critical(self, "에러", "중복된 아이디 입니다")
        else:
            QMessageBox.information(self, "확인", "사용가능한 아이디입니다")
            self.login_okay = True
            self.id_check.textChanged.connect(self.signup_page)

    # 회원가입 페이지
    def signup_page(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.login_okay = False
        self.stackedWidget.setCurrentIndex(1)

    # 로그인후 가장 먼저 보이는 메뉴 창
    def mainpage(self):
        self.open_db()
        self.c.execute(f'SELECT 아이디, `사업자` FROM user WHERE'
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

    def menu_counting(self):
        self.kimbap_plus.setStep(0)

    # 문의하기 게시판
    def question(self):
        self.stackedWidget.setCurrentIndex(3)
        self.open_db()
        self.c.execute("select 주문번호,아이디,내용,시간,답변 from snack.question;")
        self.questionlist = self.c.fetchall()
        if self.questionlist:
            self.QandA_list.setRowCount(len(self.questionlist))
            self.QandA_list.setColumnCount(len(self.questionlist[0]))
            self.QandA_list.setHorizontalHeaderLabels(['주문번호', '아이디', '내용', '시간', '답변'])
            for i in range(len(self.questionlist)):
                for j in range(len(self.questionlist[i])):
                    self.QandA_list.setItem(i, j, QTableWidgetItem(str(self.questionlist[i][j])))
            # self.QandA_list.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.QandA_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.conn.close()

    # 관리자 재고확인하기
    def inventory_view(self):
        self.show_inventory()
        self.stackedWidget.setCurrentIndex(4)

    # 재고 보여주기
    def show_inventory(self):
        head = ['재료', '수량', '단위']
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

    # 식재료 자동 구매 기능
    def ordering(self):
        self.open_db()
        self.c.execute(
            f'select a.재료, if(max(a.수량) > min(b.수량), "구매", "보류"), min(b.단가) '
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
                self.c.execute(f'insert into finance values("{fin[0]+1}","{i[0]}구매",0,{i[1]},{fin[1]-i[1]},now());')
                self.conn.commit()
        self.conn.close()

    # 장바구니
    def shopping_basket(self):
        self.total_bill = 0
        self.request_list = []
        # 장바구니에서 메뉴고르는 페이지로 돌아왔을때 다 0으로 초기화해주면 다시 고르려는것도 사라지니까 이거 생각좀 해야할듯

        if self.kimbap_plus.value() != 0:
            self.request_list.append(['김밥', str(self.kimbap_plus.value()),
                                      str(self.kimbap_plus.value() * 9000)])
        if self.tuna_kimbap_plus_2.value() != 0:
            self.request_list.append(['참치김밥', str(self.tuna_kimbap_plus_2.value()),
                                      str(self.tuna_kimbap_plus_2.value()*11000)])
        if self.Cheese_kimbap_plus_2.value() != 0:
            self.request_list.append(['치즈김밥', str(self.Cheese_kimbap_plus_2.value()),
                                      str(self.Cheese_kimbap_plus_2.value() * 11000)])
        if self.bokki_plus_3.value() != 0:
            self.request_list.append(['떡볶이', str(self.bokki_plus_3.value()),
                                      str(self.bokki_plus_3.value() * 15000)])
        if self.rabokki_plus_3.value() != 0:
            self.request_list.append(['라볶이', str(self.rabokki_plus_3.value()),
                                      str(self.rabokki_plus_3.value() * 17000)])
        if self.Cheese_bokki_plus.value() != 0:
            self.request_list.append(['치즈떡볶이', str(self.Cheese_bokki_plus.value()),
                                      str(self.Cheese_bokki_plus.value() * 17000)])
        if self.pig_Stew_plus_3.value() != 0:
            self.request_list.append(['돼지김치찌개', str(self.pig_Stew_plus_3.value()),
                                      str(self.pig_Stew_plus_3.value() * 14000)])
        if self.tuna_Stew_plus.value() != 0:
            self.request_list.append(['참치김치찌개', str(self.tuna_Stew_plus.value()),
                                      str(self.tuna_Stew_plus.value()*18000)])
        self.stackedWidget.setCurrentIndex(5)
        if self.request_list != []:
            self.tablesetting()
        else:
            self.bill_result.setText("총액:0원")
            self.tableWidget_2.clear()

    def purchase(self):
        now = datetime.now()
        self.open_db()
        self.c.execute(f'select 주문번호 from finance order by 주문번호 desc')
        store = self.c.fetchall()
        for i in range(len(self.request_list)):
            self.c.execute(f'insert into request (주문번호, 아이디, 상품명, 수량, 금액, 시간) values ("{store[0][0]+1}", "{self.login_infor[0][0]}", "{self.request_list[i][0]}", "{self.request_list[i][1]}", "{self.request_list[i][2]}", now())')
        self.conn.commit()
        self.conn.close()
        QMessageBox.information(self, "확인", "주문이 접수되었습니다")
        self.kimbap_plus.setValue(0)
        self.tuna_kimbap_plus_2.setValue(0)
        self.Cheese_kimbap_plus_2.setValue(0)
        self.bokki_plus_3.setValue(0)
        self.rabokki_plus_3.setValue(0)
        self.Cheese_bokki_plus.setValue(0)
        self.pig_Stew_plus_3.setValue(0)
        self.tuna_Stew_plus.setValue(0)
        self.stackedWidget.setCurrentIndex(2)
        # self.incom()을 위해 추가
        self.store = store[0][0]+1
        self.income()
        # self.deduction()을 위해 추가
        self.deduction()

    # 주문 금액 재무db에 저장하기
    def income(self):
        self.open_db()
        self.c.execute(f"select sum(금액), min(시간) from request where 주문번호 = '{self.store}';")
        income = self.c.fetchall()[0]
        self.c.execute(f"select 잔액 from finance order by 주문번호 desc")
        balance = self.c.fetchone()[0]
        if income[0]:
            self.c.execute(f"insert into finance values ({self.store},'{self.login_infor[0][0]}님 구매',{income[0]},0,{balance+int(income[0])},'{income[1]}')")
            self.conn.commit()
        self.conn.close()

    # 주문 상품 bom 재고 차감
    def deduction(self):
        self.open_db()
        for v in self.request_list:
            self.c.execute(f"select 재료, 수량*{v[1]} as 소모량 from bom where 상품명='{v[0]}';")
            consumption = self.c.fetchall()
            for i in consumption:
                self.c.execute(f"update inventory set 수량 = 수량 - {i[1]} where 재료 ='{i[0]}';")
                self.conn.commit()
        self.conn.close()

    # 관리자용 메인화면
    def manager_page(self):
        self.open_db()
        self.c.execute('select * from request')
        list_request = self.c.fetchall()
        self.conn.close()
        if list_request != ():
            self.order_confirmation.setRowCount(len(list_request))
            self.order_confirmation.setColumnCount(len(list_request[0]))
            self.order_confirmation.setEditTriggers(QAbstractItemView.NoEditTriggers)
            for i in range(len(list_request)):
                for j in range(len(list_request[0])):
                    self.order_confirmation.setItem(i, j, QTableWidgetItem(list_request[i][j]))
        self.stackedWidget.setCurrentIndex(7)

    # 관리자 문의함 확인하기
    def question_view(self):
        self.stackedWidget.setCurrentIndex(8)
        self.open_db()
        # 구매자가 남긴 문의게시판을 보여준다
        self.c.execute("select 주문번호,아이디,내용,시간,답변 from snack.question;")
        self.questionlist = self.c.fetchall()
        if self.questionlist:
            self.manager_question_view.setRowCount(len(self.questionlist))
            self.manager_question_view.setColumnCount(len(self.questionlist[0]))
            self.manager_question_view.setHorizontalHeaderLabels(['주문번호', '아이디', '내용', '시간', '답변'])
            for i in range(len(self.questionlist)):
                for j in range(len(self.questionlist[i])):
                    self.manager_question_view.setItem(i, j, QTableWidgetItem(str(self.questionlist[i][j])))
            # self.manager_question_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.manager_question_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.conn.close()

    def del_request(self):

        QMessageBox.information(self, "확인", "장바구니에서 삭제합니다")
        list_row = self.tableWidget_2.currentRow()
        del_list = self.request_list[list_row]
        cancel_re = int(self.request_list[list_row][1]) - 1
        if self.request_list[list_row][0] == '김밥':
            self.kimbap_plus.setValue(cancel_re)
            self.request_list[list_row][2] = str(self.kimbap_plus.value()*9000)
        elif self.request_list[list_row][0] == '참치김밥':
            self.tuna_kimbap_plus_2.setValue(cancel_re)
            self.request_list[list_row][2] = str(self.tuna_kimbap_plus_2.value()*11000)
        elif self.request_list[list_row][0] == '치즈김밥':
            self.Cheese_kimbap_plus_2.setValue(cancel_re)
            self.request_list[list_row][2] = str(self.Cheese_kimbap_plus_2.value() * 11000)
        elif self.request_list[list_row][0] == '떡볶이':
            self.bokki_plus_3.setValue(cancel_re)
            self.request_list[list_row][2] = str(self.bokki_plus_3.value() * 15000)
        elif self.request_list[list_row][0] == '라볶이':
            self.rabokki_plus_3.setValue(cancel_re)
            self.request_list[list_row][2] = str(self.rabokki_plus_3.value() * 17000)
        elif self.request_list[list_row][0] == '치즈떡볶이':
            self.Cheese_bokki_plus.setValue(cancel_re)
            self.request_list[list_row][2] = str(self.Cheese_bokki_plus.value() * 17000)
        elif self.request_list[list_row][0] == '돼지김치찌개':
            self.pig_Stew_plus_3.setValue(cancel_re)
            self.request_list[list_row][2] = str(self.pig_Stew_plus_3.value() * 14000)
        elif self.request_list[list_row][0] == '참치김치찌개':
            self.tuna_Stew_plus.setValue(cancel_re)
            self.request_list[list_row][2] = str(self.tuna_Stew_plus.value()*18000)
        self.request_list[list_row][1] = str(cancel_re)
        if cancel_re == 0:
            self.request_list.remove(del_list)
        if self.request_list != []:
            self.tablesetting()
        else:
            self.bill_result.setText("총액:0원")
            self.kimbap_plus.setValue(0)
            self.tuna_kimbap_plus_2.setValue(0)
            self.Cheese_kimbap_plus_2.setValue(0)
            self.bokki_plus_3.setValue(0)
            self.rabokki_plus_3.setValue(0)
            self.Cheese_bokki_plus.setValue(0)
            self.pig_Stew_plus_3.setValue(0)
            self.tuna_Stew_plus.setValue(0)
            self.tableWidget_2.clear()

    def tablesetting(self):
        self.total_bill = 0
        for i in range(len(self.request_list)):
            self.total_bill += int(self.request_list[i][2])
        totaltext = "총액:" + str(self.total_bill) + "원"
        self.bill_result.setText(totaltext)
        self.tableWidget_2.setRowCount(len(self.request_list))
        self.tableWidget_2.setColumnCount(len(self.request_list[0]))
        self.tableWidget_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_2.setHorizontalHeaderLabels(['품목', '개수', '금액'])
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for i in range(len(self.request_list)):
            for j in range(len(self.request_list[0])):
                self.tableWidget_2.setItem(i, j, QTableWidgetItem(self.request_list[i][j]))

    # 관리자가 구매자 문의에 답변을 남기는경우
    def manager_question_add(self):
        try:
            check = QMessageBox.question(self, ' ', '답변 하겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if check == QMessageBox.Yes:
                self.open_db()
                self.c.execute(f"update snack.question set 답변 ='{self.manager_line_add.text()}' where 내용 = '{self.cellchoice}'")
                self.conn.commit()
                QMessageBox.information(self, ' ', '답변이 등록되었습니다.')
                self.manager_line_add.clear()
                # 답변을 실시간으로 보여주기 위한 커서
                self.c.execute("select 주문번호,아이디,내용,시간,답변 from snack.question;")
                self.questionlist = self.c.fetchall()
                self.manager_question_view.setRowCount(len(self.questionlist))
                self.manager_question_view.setColumnCount(len(self.questionlist[0]))
                self.manager_question_view.setHorizontalHeaderLabels(['주문번호', '아이디', '내용', '시간', '답변'])
                for i in range(len(self.questionlist)):
                    for j in range(len(self.questionlist[i])):
                        self.manager_question_view.setItem(i, j, QTableWidgetItem(str(self.questionlist[i][j])))
                # self.manager_question_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
                self.manager_question_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            else:
                # 답변을 달지 않았을 경우
                QMessageBox.information(self, ' ', '문의함으로 돌아갑니다.')
            self.conn.close()
        except:
            QtWidgets.QMessageBox.about(self, " ", '등록된 문의가 없습니다')

    # 구매자가 남긴 문의를 삭제를 하는경우
    def manager_question_del(self):
        try:
            check = QMessageBox.question(self, ' ', '삭제 하겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            self.manager_line_add.text()
            if check == QMessageBox.Yes:
                self.open_db()
                self.c.execute(f"delete from snack.question where 내용 = '{self.cellchoice}'")
                self.conn.commit()
                # 삭제를 실시간으로 보여주기 위한 커서
                self.c.execute("select 주문번호,아이디,내용,시간,답변 from snack.question;")
                self.questionlist = self.c.fetchall()
                self.manager_question_view.setRowCount(len(self.questionlist))
                self.manager_question_view.setColumnCount(len(self.questionlist[0]))
                self.manager_question_view.setHorizontalHeaderLabels(['주문번호', '아이디', '내용', '시간', '답변'])
                for i in range(len(self.questionlist)):
                    for j in range(len(self.questionlist[i])):
                        self.manager_question_view.setItem(i, j, QTableWidgetItem(str(self.questionlist[i][j])))
                # self.manager_question_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
                self.manager_question_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            else:
                QMessageBox.information(self, ' ', '문의함으로 돌아갑니다.')
            self.conn.close()
        except:
            self.stackedWidget.setCurrentIndex(8)
            QtWidgets.QMessageBox.about(self, " ", '등록된 문의가 없습니다')

    # 셀 클릭내용을 받기위한 이벤트 함수
    def cellclicked_event(self, row, col):
        self.data = self.manager_question_view.item(row, col)
        self.cellchoice = self.data.text()

    def showgraph(self):
        date_list =[]
        date_price = []
        date_cost = []

        self.open_db()
        self.c.execute("select 시간 , sum(수입), sum(지출) from (select date(시간) as 시간, 수입, 지출 from snack.finance) as a group by a.시간")
        self.questionlist = self.c.fetchall()
        for i in range(len(self.questionlist)):
            date_list.append(self.questionlist[i][0])
            # for j in range(len(self.questionlist)):
            date_price.append(self.questionlist[i][1])
            date_cost.append(self.questionlist[i][2])


        for i in range(len(date_list)):
            print(date_list[i])

        for i in range(len(date_price)):
            print(date_price[i])

        for i in range(len(date_cost)):
            print(date_cost[i])

        print(date_list)
        print(date_price)
        print(date_cost)

        self.stackedWidget.setCurrentIndex(6)
        self.open_db()
        # 삭제를 실시간으로 보여주기 위한 커서
        self.c.execute("select 시간 , sum(수입), sum(지출) from (select date(시간) as 시간, 수입, 지출 from snack.finance) as a group by a.시간")
        self.questionlist = self.c.fetchall()
        self.tableWidget.setRowCount(len(self.questionlist))
        self.tableWidget.setColumnCount(len(self.questionlist[0]))
        self.tableWidget.setHorizontalHeaderLabels(['시간','수입','지출'])
        for i in range(len(self.questionlist)):
            for j in range(len(self.questionlist[i])):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(self.questionlist[i][j])))
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.fig = plt.Figure()
        self.figpie = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.verticalLayout.addWidget(self.canvas)
        ax = self.fig.add_subplot(111)
        # 꺽은선그래프
        ax.plot(date_list, date_cost, 'r', label="순이익")
        # 막대그래프
        ax.bar(date_list, date_price, label="매출액")
        ax.set_title("매출액, 순수익")
        ax.legend()
        self.canvas.draw()

    def show_back_b(self):
        self.verticalLayout.removeWidget(self.canvas)
        self.manager_page()

    def show_combo(self):
        check = QMessageBox.question(self, ' ', '등록 하겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        self.time = dt.datetime.now()
        self.today = self.time.strftime('%Y-%m-%d %H:%M:%S')
        productlist = ['-','김밥', '참치김밥', '치즈김밥','떡볶이','라볶이','치즈떡볶이','돼지김치찌개','참치김치찌개']
        show = self.comboBox.currentText()
        for i in range(len(productlist)):
            if show == productlist[i]:
                if check == QMessageBox.Yes:
                    self.open_db()
                    # 로그인된 고객의 아이디와 문의내용을 저장시켜준다
                    self.c.execute(f"insert into snack.question (상품,아이디,내용,시간) values "
                                   f"('{show}','{self.login_infor[0][0]}','{self.QandA_lineEdit.text()}','{self.today}')")
                    self.conn.commit()
                    QMessageBox.information(self, ' ', '문의가 등록되었습니다.')

                # 문의한 내용을 리스트로 바로 보여주기 위한 커서
                self.c.execute("SELECT * from snack.question")
                self.questionlist = self.c.fetchall()
                self.QandA_list.setRowCount(len(self.questionlist))
                self.QandA_list.setColumnCount(len(self.questionlist[0]))
                self.QandA_list.setHorizontalHeaderLabels(['상품','주문번호', '아이디', '내용', '시간', '답변'])
                for i in range(len(self.questionlist)):
                    for j in range(len(self.questionlist[i])):
                        self.QandA_list.setItem(i, j, QTableWidgetItem(str(self.questionlist[i][j])))
                # self.QandA_list.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
                self.QandA_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.QandA_lineEdit.clear()

    def addNew(self):
        self.stackedWidget.setCurrentIndex(9)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()

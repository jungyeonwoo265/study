import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import urllib.request
from PyQt5 import uic
import webbrowser
import csv
import random
from PyQt5 import QtWidgets
from login import WindowClass
from rental_jangduk import Rental
from lib_2 import SearchBookInfo
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from PyQt5.QtCore import Qt

form_class = uic.loadUiType("title.ui")[0]


class FirstClass(QMainWindow, form_class):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.img()
        self.txt()
        self.rebooks=[]
        self.num=0
        self.id=0
        self.reco.itemClicked.connect(self.test)
        self.pushButton_1.clicked.connect(self.rent)
        self.pushButton_2.clicked.connect(self.eve)
        self.pushButton_3.clicked.connect(self.back)
        self.pushButton_4.clicked.connect(self.login)
        login.login.clicked.connect(self.back2)
        self.pushButton_5.clicked.connect(self.page2)
        self.pushButton_6.clicked.connect(self.page3)
        self.pushButton_7.clicked.connect(self.page1)
        self.pushButton_10.clicked.connect(lambda: webbrowser.open('https://lib.gwangsan.go.kr/JD/scheduleMonth'))
        self.pushButton_8.clicked.connect(self.back)
        self.pushButton_9.clicked.connect(self.back)
        self.pushButton_11.clicked.connect(lambda: webbrowser.open('https://lib.gwangsan.go.kr/JD/board/3/1/read/3371?query='))
        self.pushButton_12.clicked.connect(lambda: webbrowser.open('https://lib.gwangsan.go.kr/JD/board/3/1/read/3338?query='))
        self.pushButton_13.clicked.connect(lambda: webbrowser.open('https://lib.gwangsan.go.kr/JD/board/3/1/read/3323?query='))
        self.pushButton_14.clicked.connect(lambda: webbrowser.open('https://lib.gwangsan.go.kr/JD/board/3/1/read/3322?query='))
        self.pushButton_15.clicked.connect(lambda: webbrowser.open('https://lib.gwangsan.go.kr/JD/board/3/1/read/3310?query='))
        self.pushButton_16.clicked.connect(lambda: webbrowser.open('https://lib.gwangsan.go.kr/JD/board/3/1/read/3305?query='))
        self.pushButton_17.clicked.connect(lambda: webbrowser.open('https://lib.gwangsan.go.kr/JD/board/3/1/read/3304?query='))
        self.stackedWidget.setCurrentIndex(0)
        self.reset.clicked.connect(self.resetb)

    def back(self):
        self.stackedWidget.setCurrentIndex(0)

    def back2(self):
        self.id=login.loginaction()
        login.clear_id()
        if self.id:
            self.name.setText(self.id + "님 안녕하세요")
            self.pushButton_4.setText('로그아웃')
        self.parent().setCurrentIndex(0)

    def page1(self):
        self.stackedWidget.setCurrentIndex(1)

    def page2(self):
        self.stackedWidget.setCurrentIndex(2)

    def page3(self):
        self.stackedWidget.setCurrentIndex(3)

    def img(self):
        urlString = 'https://mblogthumb-phinf.pstatic.net/MjAxODA1MzFfOTMg/MDAxNTI3NzQ4MTAzOTUz.PVuhOVayIGajFEzQvfsH_tt1rV8anmQskKne_N6iPUsg.M-Qk6qMFE-4yDucTFFdBui5iQ2wt4X_INxsSwnl8qL0g.PNG.passdongs/IMG_31052018_152729_0.png?type=w800'
        urlString2 = 'https://lib.gwangsan.go.kr/images/ui/JD/jdlogo.png?1'
        urlString3 = 'https://www.shutterstock.com/image-vector/man-holding-megaphone-speech-bubbles-260nw-2079473878.jpg'
        urlString4 = 'https://lib.gwangsan.go.kr/images/ui/sub/facilitystatus/JD/facilitystatus1_1.jpg'
        urlString5 = 'https://lib.gwangsan.go.kr/images/ui/sub/facilitystatus/JD/facilitystatus1_2.jpg'
        urlString6 = 'https://lib.gwangsan.go.kr/images/ui/sub/facilitystatus/JD/facilitystatus1_3.jpg'
        urlString7 = 'https://lib.gwangsan.go.kr/images/ui/sub/facilitystatus/JD/facilitystatus1_8.jpg'
        urlString8 = 'https://lib.gwangsan.go.kr/images/ui/sub/facilitystatus/JD/facilitystatus1_5.jpg'
        urlString9 = 'https://lib.gwangsan.go.kr/images/ui/sub/facilitystatus/JD/facilitystatus1_6.jpg'
        urlString10 = 'https://lib.gwangsan.go.kr/images/ui/sub/facilitystatus/JD/facilitystatus1_7.jpg'

        urlString11 = 'https://img.freepik.com/premium-photo/blurred-bookshelf-many-old-books-in-a-book-shop-or-library_36051-477.jpg'
        urlString12 = 'https://lib.gwangsan.go.kr/upload/banner/banner2.jpg'
        urlString13 = 'https://lib.gwangsan.go.kr/upload/banner/banner3.jpg'
        urlString14 = 'https://lib.gwangsan.go.kr/upload/banner/banner1.jpg'
        urlString15 = 'https://lib.gwangsan.go.kr/upload/banner/banner5.jpg'
        urlString16 = 'https://lib.gwangsan.go.kr/upload/banner/banner4.jpg'
        urlString17 = 'https://lib.gwangsan.go.kr/upload/banner/banner6.jpg'

        imageFromWeb = urllib.request.urlopen(urlString).read()
        imageFromWeb2 = urllib.request.urlopen(urlString2).read()
        imageFromWeb3 = urllib.request.urlopen(urlString3).read()
        imageFromWeb4 = urllib.request.urlopen(urlString4).read()  # 시설이미지
        imageFromWeb5 = urllib.request.urlopen(urlString5).read()
        imageFromWeb6 = urllib.request.urlopen(urlString6).read()
        imageFromWeb7 = urllib.request.urlopen(urlString7).read()
        imageFromWeb8 = urllib.request.urlopen(urlString8).read()
        imageFromWeb9 = urllib.request.urlopen(urlString9).read()
        imageFromWeb10 = urllib.request.urlopen(urlString10).read()
        imageFromWeb11 = urllib.request.urlopen(urlString11).read()
        imageFromWeb12 = urllib.request.urlopen(urlString12).read()
        imageFromWeb13 = urllib.request.urlopen(urlString13).read()
        imageFromWeb14 = urllib.request.urlopen(urlString14).read()
        imageFromWeb15 = urllib.request.urlopen(urlString15).read()
        imageFromWeb16 = urllib.request.urlopen(urlString16).read()
        imageFromWeb17 = urllib.request.urlopen(urlString17).read()

        qPixmapVar = QPixmap()
        qPixmapVar2 = QPixmap()
        qPixmapVar3 = QPixmap()
        qPixmapVar4 = QPixmap()
        qPixmapVar5 = QPixmap()
        qPixmapVar6 = QPixmap()
        qPixmapVar7 = QPixmap()
        qPixmapVar8 = QPixmap()
        qPixmapVar9 = QPixmap()
        qPixmapVar10 = QPixmap()
        qPixmapVar11 = QPixmap()
        qPixmapVar12 = QPixmap()
        qPixmapVar13 = QPixmap()
        qPixmapVar14 = QPixmap()
        qPixmapVar15 = QPixmap()
        qPixmapVar16 = QPixmap()
        qPixmapVar17 = QPixmap()

        qPixmapVar.loadFromData(imageFromWeb)
        qPixmapVar2.loadFromData(imageFromWeb2)
        qPixmapVar3.loadFromData(imageFromWeb3)
        qPixmapVar4.loadFromData(imageFromWeb4)
        qPixmapVar5.loadFromData(imageFromWeb5)
        qPixmapVar6.loadFromData(imageFromWeb6)
        qPixmapVar7.loadFromData(imageFromWeb7)
        qPixmapVar8.loadFromData(imageFromWeb8)
        qPixmapVar9.loadFromData(imageFromWeb9)
        qPixmapVar10.loadFromData(imageFromWeb10)
        qPixmapVar11.loadFromData(imageFromWeb11)
        qPixmapVar12.loadFromData(imageFromWeb12)
        qPixmapVar13.loadFromData(imageFromWeb13)
        qPixmapVar14.loadFromData(imageFromWeb14)
        qPixmapVar15.loadFromData(imageFromWeb15)
        qPixmapVar16.loadFromData(imageFromWeb16)
        qPixmapVar17.loadFromData(imageFromWeb17)

        self.label_pic.setPixmap(qPixmapVar)
        self.main_pic.setPixmap(qPixmapVar2)
        self.event_pic.setPixmap(qPixmapVar3)
        self.label_11.setPixmap(qPixmapVar4)
        self.label_12.setPixmap(qPixmapVar5)
        self.label_13.setPixmap(qPixmapVar6)
        self.label_14.setPixmap(qPixmapVar7)
        self.label_15.setPixmap(qPixmapVar8)
        self.label_16.setPixmap(qPixmapVar9)
        self.label_17.setPixmap(qPixmapVar10)
        self.backimg.setPixmap(QPixmap(qPixmapVar11).scaled(self.width(), self.height(), Qt.IgnoreAspectRatio))
        self.backimg2.setPixmap(QPixmap(qPixmapVar11).scaled(self.width(), self.height(), Qt.IgnoreAspectRatio))
        self.backimg3.setPixmap(QPixmap(qPixmapVar11).scaled(self.width(), self.height(), Qt.IgnoreAspectRatio))
        self.center.setPixmap(qPixmapVar12)
        self.nation.setPixmap(qPixmapVar13)
        self.gwangsan.setPixmap(qPixmapVar14)
        self.silib.setPixmap(qPixmapVar15)
        self.guklib.setPixmap(qPixmapVar16)
        self.gwangju.setPixmap(qPixmapVar17)
        self.foot.setStyleSheet("background-color: white")
        self.lib1.setStyleSheet("color: white;"
                                "background-color: gray")
        self.event1.setStyleSheet("color: white;"
                                  "background-color: gray")
        self.recommend1.setStyleSheet("color: black;"
                                      "background-color: white")
        self.info1.setStyleSheet("color: white;"
                                 "background-color: gray")

    def txt(self):
        self.label_9.setText("일정 및 행사")
        self.label_2.setText("2023년 1분기 장덕도서관 사물함 신청 안내 ")
        self.label_3.setText("나를 변화시.키.는 글쓰기 후속모임 김글리작가와의 만남 수강생 추가모집")
        self.label_4.setText("제7회 장덕도서관 독후화그리기대회 인증 사진 이벤트 당첨자 발표")
        self.label_5.setText("제7회 장덕도서관 독후화그리기 대회 심사 결과 발표")
        self.label_6.setText("2022년 장덕도서관 희망도서 마감 안내")
        self.label_7.setText("광산구립도서관 학습실 운영시간 변경 안내")
        self.label_8.setText("모두모여 체험공방: 가을편 수강생 모집 안내")
        self.label.setText("            대지 3,304㎡\n\
            건물면적 2,844㎡(철근콘크리트 지하1층에서 지상 5층 규모)\n\
            층별안내\n \
            5층 - 물탱크실, ELEV 기계실\n\
            4층 - 창고, 옥상휴게실\n\
            3층 - 학습실1, 학습실2, 다목적실, 기증(보존)자료실, 소회의실2, 휴게실, 매점\n\
            2층 - 종합자료실, 디지털자료실, 문화교실1, 문화교실2, 소회의실1\n\
            1층 - 어린이자료실, 수유실, 책읽어주는방, 북카페, 전시실, 사무실, 도서관정책관실\n\
            지하1층 - 전기실, 기계실")

    def recommend(self):
        f = open('장덕도서관.csv', 'r')
        rdr = csv.reader(f)
        num = random.randrange(1, 70881)
        for line in rdr:
            if line[0] == str(num):
                return line

    def resetb(self):
        self.reco.clear()
        for i in range(0, 10):
            self.rebooks=(self.recommend())
            self.reco.insertItem(i, str(self.rebooks[4:7]))

    def test(self):
        row = self.reco.currentItem().text()
        rows = row.split(',')
        print(rows)
        path = "chromedriver.exe"  # 개인의 드라이버 경로를 적으세요#
        driver = webdriver.Chrome(path)

        driver.get("https://www.google.com")
        time.sleep(1)

        # step 2. 검색창을 이름으로 찾아서 검색한다.
        element = driver.find_element(By.NAME, "q")  # 검색창 html의 name이 'q'여서 q다
        element.send_keys(list(rows[0:2]))  # 검색 단어를 입력한다
        element.submit()
        time.sleep(10)


    def login(self):
        if not self.id:
            widget.setCurrentIndex(1)
        else:
            self.id = 0
            self.name.setText("")
            self.pushButton_4.setText('로그인')

    def eve(self):
        widget.setCurrentIndex(3)

    def rent(self):
        if self.id:
            rental.name(str(self.id))
            widget.setCurrentIndex(2)

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()

    #WindowClass의 인스턴스 생성
    login = WindowClass()
    rental = Rental()
    lib_2 = SearchBookInfo()
    myWindow = FirstClass()

    #프로그램 화면을 보여주는 코드
    widget.addWidget(myWindow)
    widget.addWidget(login)
    widget.addWidget(rental)
    widget.addWidget(lib_2)

    widget.setFixedHeight(800)
    widget.setFixedWidth(1200)
    widget.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()



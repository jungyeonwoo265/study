import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import csv

form_class = uic.loadUiType("lib_2.ui")[0]

class SearchBookInfo(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Search.clicked.connect(self.search)
        self.Find.returnPressed.connect(self.search)
        self.pushButton.clicked.connect(self.move_main)

    def search(self):
        book_info_s = open("신가도서관.csv", 'r', encoding="cp949")
        books_s = list(csv.reader(book_info_s))
        book_info_s.close()
        book_info_j = open("장덕도서관.csv", 'r', encoding="cp949")
        books_j = list(csv.reader(book_info_j))
        book_info_j.close()
        book_info_c = open("첨단도서관.csv", 'r', encoding="cp949")
        books_c = list(csv.reader(book_info_c))
        book_info_c.close()
        book_info_e = open("이야기꽃도서관.csv", 'r', encoding="cp949")
        books_e = list(csv.reader(book_info_e))
        book_info_e.close()
        rent_info_s = open("RentInfo_신가.csv", 'r', encoding="cp949")
        rented_s = list(csv.reader(rent_info_s))
        rent_info_s.close()
        rent_info_j = open("RentInfo_장덕.csv", 'r', encoding="cp949")
        rented_j = list(csv.reader(rent_info_j))
        rent_info_j.close()
        rent_info_c = open("RentInfo_첨단.csv", 'r', encoding="cp949")
        rented_c = list(csv.reader(rent_info_c))
        rent_info_c.close()
        rent_info_e = open("RentInfo_이야기꽃.csv", 'r', encoding="cp949")
        rented_e = list(csv.reader(rent_info_e))
        rent_info_e.close()
        self.Found.clear()
        find_total =0
        word = str(self.Find.text())
        word = word.strip()
        if word:
            for i in range(len(books_s)):
                find = 0
                if self.Find.text() in books_s[i][4]:
                    self.Found.append(str(books_s[i]))
                    find_total = 1
                    for word in rented_s:
                        if books_s[i][3] in word:
                            find = 1
                    if find == 1:
                        self.Found.append(" - (대여 중, 7일 후 반납)")
                    else:
                        self.Found.append(" - (대여 가능)")

            for i in range(len(books_j)):
                find = 0
                if self.Find.text() in books_j[i][4]:
                    self.Found.append(str(books_j[i]))
                    find_total = 1
                    for word in rented_j:
                        if books_j[i][3] in word:
                            find = 1
                    if find == 1:
                        self.Found.append(" - (대여 중, 7일 후 반납)")
                    else:
                        self.Found.append(" - (대여 가능)")

            for i in range(len(books_c)):
                find = 0
                if self.Find.text() in books_c[i][4]:
                    self.Found.append(str(books_c[i]))
                    find_total = 1
                    for word in rented_c:
                        if books_c[i][3] in word:
                            find = 1
                    if find == 1:
                        self.Found.append(" - (대여 중, 7일 후 반납)")
                    else:
                        self.Found.append(" - (대여 가능)")

            for i in range(len(books_e)):
                find = 0
                if self.Find.text() in books_e[i][4]:
                    self.Found.append(str(books_e[i]))
                    find_total = 1
                    for word in rented_e:
                        if books_e[i][3] in word:
                            find = 1
                    if find == 1:
                        self.Found.append(" - (대여 중, 7일 후 반납)")
                    else:
                        self.Found.append(" - (대여 가능)")
        if find_total == 0:
            self.Found.append("검색 결과를 찾을 수 없음")

    def move_main(self):
        self.Find.clear()
        self.Found.clear()
        self.parent().setCurrentIndex(0)

# if __name__ == "__main__":
#     # QApplication : 프로그램을 실행시켜주는 클래스
#     app = QApplication(sys.argv)
#
#     # WindowClass의 인스턴스 생성
#     myWindow = SearchBookInfo()
#     # 프로그램 화면을 보여주는 코드
#     myWindow.show()
#
#     # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
#     app.exec_()

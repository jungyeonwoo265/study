import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QIcon
import csv

form_Class = uic.loadUiType("rental.ui")[0]

class Rental(QWidget, form_Class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('대여 및 반납')
        self.setWindowIcon(QIcon('book.jpg'))

        self.bt_gohome.clicked.connect(self.movemain)
        self.bt_Search.clicked.connect(self.Search)

        self.bt_rental.clicked.connect(self.rental)
        self.bt_return.clicked.connect(self.Return)
        self.listWidget.clicked.connect(self.showtext)
        self.label.setText('대여 가능 여부')
        self.csv = 'RentInfo_신가.csv'
        self.user_id = 'name'

    def name(self,name):
        self.user_id = name

    def showtext(self):
        book = self.listWidget.currentItem().text()
        check = 0
        with open(self.csv, 'r') as f:
           lines = f.readlines()
        for line in lines:
            if book in line:
                check = 1
        if check == 1:
            self.label.setText('대여 중')
        else:
            self.label.setText('대여 가능')

    def movemain(self):
        self.label.setText('대여 가능 여부')
        self.lineEdit.clear()
        self.listWidget.clear()
        self.parent().setCurrentIndex(0)

    def Search(self):
        self.listWidget.clear()
        idx = self.book_item.currentText()
        Str = self.lineEdit.text()
        if idx == '도서명':
            idx = 4
        elif idx == '저자':
            idx = 5
        find_total = 0
        word = Str.strip()
        with open('신가도서관.csv', 'r') as f:
            Csv = csv.reader(f)
            if word:
                for i in Csv:
                    if Str in i[idx]:
                        book = i[3]+','+i[4]+','+i[5]
                        self.listWidget.addItem(book)
                        find_total = 1
            if not find_total:
                self.label.setText('검색결과 없음')

    def rental(self): # 대여
        books =self.listWidget.currentItem()
        if books != None:
            book = books.text()
            word = book + ',' + self.user_id + '\n'
            check = 0
            with open(self.csv, 'r') as f:
                lines = f.readlines()
            for line in lines:
                if book in line:
                    check =1
            if check != 1:
                with open(self.csv, 'a') as f:
                    f.write(word)
                self.label.setText('대여 완료')
            else:
                self.label.setText('대여 중')
        else:
            return

    def Return(self): # 반납
        books = self.listWidget.currentItem()
        if books != None:
            book = books.text()
            word = book + ',' + self.user_id + '\n'
            with open(self.csv, 'r') as f:
               lines = f.readlines()
            if word in lines:
                with open(self.csv, 'w') as f:
                    for line in lines:
                        if word not in line:
                            f.write(line)
                    self.label.setText('반납 완료')
            else:
                self.label.setText('대여 이력 없음')
        else:
            return
# if __name__ == "__main__" :
#     app = QApplication(sys.argv)
#     myWindow = Rental()
#     myWindow.show()
#     app.exec_()


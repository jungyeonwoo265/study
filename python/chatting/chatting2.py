import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pymysql as p
from PyQt5.QtCore import QThread
import time

form_class = uic.loadUiType("chatting.ui")[0]
name = "정연수"
to = "정연우"


class Thread(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.turn = True

    def open_db(self):
        self.conn = p.connect(host='127.0.0.1', port=3306, user='root', password='0000', db='chatting',
                              charset='utf8')
        self.c = self.conn.cursor()

    def run(self):
        while True:
            self.open_db()
            self.c.execute(f'select count(*) from message')
            num = self.c.fetchone()[0]
            num1 = self.parent.listWidget.count()
            if num != num1:
                self.turn = True
            if self.turn:
                self.parent.listWidget.clear()
                self.c.execute(f'select 보냄,시간,내용 from message')
                message = self.c.fetchall()
                for i in message:
                    self.parent.listWidget.addItem(f'{i[0]} / {i[1]} / {i[2]}')
                self.conn.close()
                self.turn = False
                time.sleep(0.05)
            else:
                self.conn.close()
            self.parent.listWidget.scrollToBottom()
            time.sleep(0.05)


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.thread_action()
        self.label.setText(name)
        self.lineEdit.returnPressed.connect(self.input)

    def thread_action(self):
        t = Thread(self)
        t.start()

    # 채팅 입력
    def input(self):
        text = self.lineEdit.text()
        if text:
            self.open_db()
            self.c.execute(f'insert into message values(curdate(), "{name}", "{to}", curtime(), "{text}","n")')
            self.conn.commit()
            self.conn.close()
        self.lineEdit.clear()

    # DB 연결
    def open_db(self):
        self.conn = p.connect(host='127.0.0.1', port=3306, user='root', password='0000', db='chatting', charset='utf8')
        self.c = self.conn.cursor()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()

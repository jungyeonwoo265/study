import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic


form_class = uic.loadUiType("fff.ui")[0]

class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.stackedWidget.setCurrentIndex(1)
        self.login.clicked.connect(self.loginaction)
        self.join.clicked.connect(self.next_stack)
        self.password.setEchoMode(QLineEdit.Password)
        self.confirmjoin.clicked.connect(self.five)
        self.previous_btn.clicked.connect(self.previous_stack)

    def previous_stack(self):
        self.stackedWidget.setCurrentIndex(1)

    def next_stack(self):
        self.stackedWidget.setCurrentIndex(0)

    def five(self):
        id_2 = self.id_2.text()
        password_2 = self.password_2.text()
        g = self.idread()
        if self.id_2.text() != '' and self.password_2.text() != '' and self.confirm.text() != '' and self.call.text() != '' and self.address.text() != '':
            QMessageBox.information(self, '요건충족', 'dsadsa')
            if id_2 in g:
                QMessageBox.information(self, '중복 오류 아이디', '오류 아이디')
            else:
                QMessageBox.information(self, '올바른 아이디', '사용가능 아이디')
                if self.password_2.text() != self.confirm.text():
                    QMessageBox.information(self, '비밀번호 오류', '오류 비밀번호')
                else:
                    QMessageBox.information(self, '비밀번호가 맞습니다', '맞음 비밀번호')
                    self.idwrite(id_2)

                    self.pswrite(password_2)
                    self.idread()
                    self.psread()
                    self.id_2.clear()
                    self.password_2.clear()
                    self.confirm.clear()
                    self.call.clear()
                    self.address.clear()
        else:
            QMessageBox.information(self, '필수요소', 'sdasdsa')

    def idwrite(self,id_2):
        with open('ID.txt', 'a', encoding='utf8') as f:
            id=f'{id_2}\n'
            f.write(id)
        f.close()

    def pswrite(self,password_2):
        with open('PS.txt', 'a', encoding='utf8') as f:
            ps=f'{password_2}\n'
            f.write(ps)
        f.close()

    def idread(self):
        f = open("ID.txt")
        ist=[]
        while True:
            line = f.readline()
            if not line: break
            line = line.replace('\n', '')
            ist.append(line)
        f.close()
        return ist

    def psread(self):
        f = open("PS.txt")
        pst = []
        while True:
            line = f.readline()
            if not line: break
            line = line.replace('\n', '')
            pst.append(line)
        f.close()
        return pst

    def loginaction(self):
        id=self.id.text()
        password=self.password.text()
        b= self.idread()
        c=self.psread()
        e=[]
        for i in range(0,len(b)):
            d=[b[i],c[i]]
            e.append(d)

        bom=[id, password]
        if bom in e:
            return bom[0]
        else:
            return 0
    def clear_id(self):
        self.id.clear()
        self.password.clear()


# if __name__ == "__main__" :
#     #QApplication : 프로그램을 실행시켜주는 클래스
#     app = QApplication(sys.argv)
#
#     #WindowClass의 인스턴스 생성
#     myWindow = WindowClass()
#
#     #프로그램 화면을 보여주는 코드
#     myWindow.show()
#
#     #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
#     app.exec_()
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtGui import *

form_class = uic.loadUiType('./login.ui')[0]

class Login(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.checkStatus = False
        self.setupUi(self)
        self.id_lineEdit.setText("")
        self.login_SW.setCurrentIndex(1)
        self.login_Button.clicked.connect(self.Login_Check)
        self.signup_Button.clicked.connect(self.MoveSignupPage)
        self.Home1_Button.clicked.connect(self.MoveMainPage)
        self.Home2_Button.clicked.connect(self.MoveMainPage)
        self.join_Button.clicked.connect(self.Sign_Up)
        self.duplication_Button.clicked.connect(self.Double_Check)
        self.agree1_checkBox.toggled.connect(self.Check_Box)
        self.onlyInt = QIntValidator()
        self.phone_lineEdit.setValidator(self.onlyInt)
        self.id_lineEdit.textChanged.connect(self.Double_change)

    def MoveMainPage(self):
        self.close()

    def MoveSignupPage(self):
        self.login_SW.setCurrentIndex(2)
        self.id_lineEdit.clear()
        self.pw_lineEdit.clear()
        self.pw2_lineEdit.clear()
        self.name_lineEdit.clear()
        self.phone_lineEdit.clear()
        self.address_lineEdit.clear()
        self.agree1_checkBox.setChecked(False)
        self.agree2_checkBox.setChecked(False)
        self.agree3_checkBox.setChecked(False)
        self.agree4_checkBox.setChecked(False)

    def MoveLoginPage(self):
        self.login_SW.setCurrentIndex(1)

    def Double_Check(self):
        user = self.id_lineEdit.text()
        dc = 0
        lines = open('Userinfo.txt', 'r', encoding='cp949').read().split('\n')
        for i in range(len(lines)):
            data = lines[i].split('\n')
            if (user + '\n') in lines:
                dc = 1
                break
            elif (user + '\n') not in lines:
                dc = 2
                self.checkStatus = True
                break
            else:
                pass
        if dc == 1:
            QMessageBox.critical(self, "알림", "아이디 중복")
        elif dc == 2:
            QMessageBox.information(self, "알림", "사용 가능한 아이디")

    def Double_change(self):
        self.checkStatus = False

    def Sign_Up(self):
        id = self.id_lineEdit.text()
        pw1 = self.pw_lineEdit.text()
        pw2 = self.pw2_lineEdit.text()
        name = self.name_lineEdit.text()
        phone = self.phone_lineEdit.text()
        address = self.address_lineEdit.text()

        with open('Userinfo.txt', 'a') as f:
            if pw1 != pw2:
                QMessageBox.critical(self, "알림", "비밀번호가 일치하지 않습니다. 다시 확인해주세요")

            elif self.checkStatus == False:
                QMessageBox.critical(self, "알림", "아이디 중복 확인이 안 되어있습니다")

            elif id == '' or pw1 == '' or name == '' or phone == '' or address == '':
                QMessageBox.critical(self, "알림", "정보를 입력하세요")

            else:
                QMessageBox.information(self, "알림", "회원가입 됐습니다")
                f.writelines(f"\n{id},{pw1},{name},{phone},{address}")
                self.login_SW.setCurrentIndex(1)
                self.id_lineEdit.clear()
                self.pw_lineEdit.clear()
                self.pw2_lineEdit.clear()
                self.name_lineEdit.clear()
                self.phone_lineEdit.clear()
                self.address_lineEdit.clear()
                self.agree1_checkBox.setChecked(False)
                self.agree2_checkBox.setChecked(False)
                self.agree3_checkBox.setChecked(False)
                self.agree4_checkBox.setChecked(False)

    def Check_Box(self):
        if self.agree1_checkBox.isChecked() == True:
            self.agree2_checkBox.toggle()
            self.agree3_checkBox.toggle()
            self.agree4_checkBox.toggle()

    def Login_Check (self):
        if self.login_id_lineEdit.text() == "":
            QMessageBox.critical(self, "로그인 오류", "정보를 입력하세요")
            return
        self.id = self.login_id_lineEdit.text()
        pw = self.login_pw_lineEdit.text()
        logined = 0
        lines = open('Userinfo.txt', 'r', encoding='cp949').read().split('\n')
        for i in range(len(lines)):
            list = lines[i].split(',')
            if self.id not in list[0]:
                logined = 1

            elif pw not in list[1]:
                logined = 2
            else:
                logined = 3
                break

        if logined == 1:
            QMessageBox.critical(self, "로그인 오류", "ID 정보가 없습니다. 회원가입 해주세요")
        elif logined == 2:
            QMessageBox.critical(self, "로그인 오류", "비밀번호를 다시 입력하세요")
        elif pw == '':
            QMessageBox.critical(self, "로그인 오류", "비밀번호를 입력하세요")
        else:
            QMessageBox.critical(self, "안내창", "로그인 성공")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     widget = QtWidgets.QStackedWidget()
#     mainWindow = Login()
#     widget.addWidget(mainWindow)
#     widget.setFixedHeight(768)
#     widget.setFixedWidth(1024)
#     widget.show()
#     app.exec_()
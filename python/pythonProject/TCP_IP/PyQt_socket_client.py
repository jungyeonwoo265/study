import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from socket import *
import threading

form_class = uic.loadUiType("GUI.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect(('10.10.21.108', 2500))

        self.calc_button.clicked.connect(self.calculate)

    def calculate(self):
        # global temp
        temp = float(self.entry1.text())
        self.sock.send(str(temp).encode())

    def handlar(self):
        # sock = (self.sock,)
        while True:
            try:
                r_msg = self.sock.recv(1024)
            except:
                pass
            else:
                self.entry2.clear()
                self.entry2.setText(r_msg.decode())
                self.entry1.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    cThread = threading.Thread(target=myWindow.handlar)
    cThread.daemon = True
    cThread.start()
    app.exec_()

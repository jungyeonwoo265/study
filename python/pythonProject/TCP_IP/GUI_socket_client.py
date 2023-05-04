# 섭씨온도를 보내고 화씨온도를 받아 표시하는 GUI 클라이언트 프로그램

from tkinter import *
from socket import *
import threading
import struct


# 전송 버튼을 클릭하면 실행된는 함수
# 섭씨온도 창(entry1)의 값을 읽어 bytes형으로 변환하여 서버에 전송
def calculate():
    global temp
    # 읽어온 섭씨 온도를 화씨 온도로 변환하기 위해 float 형으로 변환
    temp = float(entry1.get())
    # 온도를 문자열로 변환하고 bytes형으로 변환후 서버에 전송
    sock.send(str(temp).encode())


# 스레드 핸들러
# 서버로 부터 화씨 온도를 받아 이를 문자열로 변환하여 화씨온도 창(entry2)에 표시
def handlar(sock):
    while True:
        try:
            r_msg = sock.recv(1024)
        except:
            pass
        else:
            entry2.delete(0, END)
            # 받은 bytes형의 온도를 문자열로 변환후 표시
            entry2.insert(0, r_msg.decode())
            entry1.delete(0, END)

# 소켓을 생성하고 서버로 연결
sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('10.10.21.108', 2500))

# 위젯을 생성하고 배치
root = Tk()
message_label = Label(text='Enter a temperature(c)', font=('Verdana', 16))
entry1 = Entry(font=('Verdana', 16), width=5)

recv_label = Label(text='Temperature in F', font=('Verdana', 16))
entry2 = Entry(font=('Verdana', 16), width=5)

calc_button = Button(text='전송', font=('Verdana', 12), command=calculate)

message_label.grid(row=0, column=0, sticky=W)
recv_label.grid(row=1, column=0, sticky=W)
entry1.grid(row=0, column=1)
entry2.grid(row=1, column=1)
calc_button.grid(row=0, column=2, padx=10, pady=10)

# 스레드르 생성하고 실행
# 스레드 함수로 전달될 인수는 튜블로 구성해야된다. 따라서 args=(sock,)와 같이 전달
cThread = threading.Thread(target=handlar, args=(sock,))
cThread.daemon = True
cThread.start()

# mainloop 함수가 실행되면 제어가 이벤트 루프로 넘어간다.
mainloop()

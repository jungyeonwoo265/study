# echo_client_demo

import socket

port = 2500
address = ('localhost', port)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)

while True:
    msg = input('입력: ')
    s.send(msg.encode())
    r_msg = s.recv(1024)
    if not r_msg:
        break
    print("출력: ", r_msg.decode())


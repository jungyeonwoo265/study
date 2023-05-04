# echo_client_exception

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 2500))

while True:
    msg = input('입력: ')
    if not msg:
        continue

    try:
        s.send(msg.encode())

    except:
        print('연결 종료1')
        break

    try:
        msg = s.recv(1024)
        if not msg:
            print('연결 종료2')
            break
        print(f'출력: {msg.decode()}')

    except:
        print('연결 종료3')
        break

s.close()



# TCP_echoserver.py
# 송수신 예외 처리를 한 에코 서버

from socket import *

port = 2500
bufsize = 1024

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(('10.10.21.108', port))
# 최대 대기 클라이언트 수
sock.listen(5)
print('Waiting for clients...')

c_sock, (r_host, r_port) = sock.accept()
print('connected by', r_host, r_port)

while True:
    try:
        data = c_sock.recv(bufsize)
        # 연결 해제됨
        if not data:
            c_sock.close()
            print('연결이 종료되었습니다.')
            break

    except:
        c_sock.close()
        print('연결이 종료되었습니다.')
        break

    else:
        print(data.decode())

    try:
        c_sock.send(data)

    except:
        c_sock.close()
        print('연결이 종료되었습니다.')
        break
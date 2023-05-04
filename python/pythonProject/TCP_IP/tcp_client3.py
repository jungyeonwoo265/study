# TCP_client.py
# 예외처리를 한 TCP_IP 클라이언트 프로그램
# 실행할 때 서버 주소와 포트를 지정한다.
# 지정하지 않으면 '127.0.0.1'과 2500 사용

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버 주소 입력
svrip = input(("server ip(default: 127.0.0.1):"))
if svrip == "":
    svrip = '127.0.0.1'

# 포트 번호 입력
port = input('port(default : 2500):')
if port == '':
    port = 2500
else:
    port = int(port)

sock.connect((svrip, port))
print('connected to' + svrip)

while True:
    msg = input('sending message: ')

    # 송신 데이터가 없으면 다시 실행
    if not msg:
        continue

    # 데이터 전송
    try:
        sock.send(msg.encode())

    except:
        print('연결이 종료되었습니다.')
        break

    # 데이터 읽기
    try:
        msg = sock.recv(1024)
        if not msg:
            print('연결이 종료되었습니다.')
            break
        print(f'received message: {msg.decode()}')

    except:
        print('연결이 종료되었습니다.')
        break

sock.close()


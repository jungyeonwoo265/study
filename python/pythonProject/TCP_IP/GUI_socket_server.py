# 섭씨온도를 받아 화씨온도로 변환하여 전송하는 TCP 서버 프로그램

import sys
from socket import *

echo_port = 2500
bufsize = 1024

# 사용자가 프로그램을 실행할때 포트를 지정한경우
if len(sys.argv) > 1:
    port = int(eval(sys.argv[1]))
# 사용자가 프로그램을 실행할때 포트를 지정하지 않은 경우
else:
    port = echo_port

# 소켓 생성 및 클라이언트의 연결 요청
s = socket(AF_INET, SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(('10.10.21.108', port))
s.listen(1)

print('Waiting for connection from client')
conn, (remotehost, remoteport) = s.accept()
print('connected by', remotehost, remoteport)

# 클라이언트로 부터 데이터를 수산하고 화씨온도를 계산하여 전송
while True:
    try:
        data = conn.recv(bufsize)
        if not data:
            break
        # 수신 데이터는 bytes형이므로 계산을 위해 float형으로 변환
        data = float(data.decode())
        # 화씨온도 = 9/5 * 섭씨온도 + 32
        data = 9.0/5.0*data+32.0
        # 소수점 첫째 자리 까지의 화씨온도를 문자열로 변환
        data = '{:.1f}'.format(data)
        # 화씨온도를 bytes형으로 변환하여 전송
        conn.send(data.encode())
    except ConnectionResetError:
        break
conn.close()

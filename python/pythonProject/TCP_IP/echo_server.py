# TCP 에코 서버
# 1명의 클라이언트만 서비스

from socket import *

port = 2500

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(('', port))
sock.listen(1)
print('기달려')

c, (r_host, r_port) = sock.accept()
print('연결 ', r_host, r_port)

while True:
    data = c.recv(1024)
    if not data:
        break
    print('메시지: ', data.decode())

    c.send(data)

c.close()
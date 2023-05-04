# echo_server_exception

from socket import *

port = 2500

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(('', port))
sock.listen(5)
print('기달려')

c, (r_host, r_port) = sock.accept()
print('연결: ', r_host, r_port)

while True:
    try:
        data =c.recv(1024)
        if not data:
            c.close()
            print('연결 종료')
            break
    except:
        c.close()
        print('연결 종료')
        break
    else:
        print(data.decode())

    try:
        c.send(data)
    except:
        c.close()
        print('연결 종료')
        break

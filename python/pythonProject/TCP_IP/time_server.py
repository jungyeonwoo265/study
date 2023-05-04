# time_server.py

import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ('', 5000)
sock.bind(address)
sock.listen(5)

while True:
    client, addr = sock.accept()
    print('연결: ', addr)
    client.send(time.ctime(time.time()).encode())
    client.close()


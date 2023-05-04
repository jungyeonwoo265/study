# create_connection

import socket

s = socket.create_connection(('localhost', 2500))

msg = '메시지'
print('보내기: ', msg)
s.sendall(msg.encode())
data = s.recv(1024)
print('받음: ', data.decode())
s.close()

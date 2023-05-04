# threading class를 이용한 TCP_IP 에코 서버 프로그램

import socket, threading

# threading.Thread 서브 클래스
class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.clientAddress = clientAddress
        self.csocket = clientsocket
        print('New socket added: ', self.clientAddress)

    # 데이터를 수신하여 다시 클라이언트에게 보낸다.
    def run(self):
        print('connection from : ', self.clientAddress)

        msg = ''
        while True:
            data = self.csocket.recv(2048)
            msg = data.decode()

            if msg == 'quit':
                break

            print('from client', msg)
            self.csocket.send(bytes(msg, 'UTF-8'))

        print('Client at', self.clientAddress, 'disconnected...')

# 서버 소켓을 생성하고 주소와 결합한다.
host = '10.10.21.108'
port = 2500

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
print('Server started')
print('Waiting for client request...')

#클라이언트 마다 하나의 스레드가 배정된다.
while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()
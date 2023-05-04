# threading 모듈을 이용한 TCP 멀티 채팅 서버 프로그램

from socket import *
from threading import *


class MultiChatServer:
    def __init__(self):
        # 변수 선언
        self.clients = []
        self.final_recived_message = ''
        # 소켓 생성
        self.s_sock = socket(AF_INET, SOCK_STREAM)
        self.ip = '10.10.21.108'
        self.port = 9000
        self.s_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        # 소켓에 주소 부여
        self.s_sock.bind((self.ip, self.port))
        print('클라이언트 대기 중...')
        # 연결을 기다리는 상태
        self.s_sock.listen(100)
        # 함수 호출
        self.accept_client()

    def accept_client(self):
        while True:
            # 연결 클라이언트 소켓을 목록에 추가
            client = c_socket, (ip, port) = self.s_sock.accept()
            # 스레드를 생성하여 데이터를 수신
            if client not in self.clients:
                self.clients.append(client)
            print(ip, ':', str(port), '가 연결되었습니다.')
            cth = Thread(target=self.receive_message, args=(c_socket,))
            cth.start()

    # 데이터를 수신하여 모든 클라이언트에게 전송한다.
    def receive_message(self, c_socket):
        while True:
            print('확인 3')
            # 데이터를 수신
            try:
                incoming_message = c_socket.recv(256)
                if not incoming_message:
                    print('확인1')
                    break
            except:
                continue
                # 모든 클라이언트에게 메시지 전송
            else:
                print('확인2')
                self.final_recived_message = incoming_message.decode('utf-8')
                print(self.final_recived_message)
                self.send_all_clients(c_socket)
        c_socket.close()

    def send_all_clients(self, senders_socket):
        # 클라이언트 list 확인
        for client in self.clients:
            socket, (ip, port) = client
            # 송신 클라이언트가 아니면 메시지 전송
            if socket is not senders_socket:
                try:
                    socket.sendall(self.final_recived_message.encode())
                except:
                    self.clients.remove(client)
                    print(f'{ip}, {port} 연결이 종료되었습니다.')


if __name__=='__main__':
    MultiChatServer()

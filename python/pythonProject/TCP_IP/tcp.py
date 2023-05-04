# _thread를 이용한 TCP_IP 서버 프로그램

from socket import *
import _thread

buffsize = 1024
host_addr = '10.10.21.108'
port = 2500


def response(key):
    return '서버 응답 메시지'


# 클라이언트로 부터 데이터를 읽어 화면에 출력, 응답을 전송
# 서브 스레드
def handler(clientsock, addr):
    while True:
        # 데이터 수신
        data = clientsock.recv(buffsize)
        # 수신 데이터 화면 출력
        print('data: ', repr(data))
        if not data: break
        # 응답 전송
        clientsock.send(response('').encode())
        print('sent: ', repr(response('')))

# TCP_IP 소켓을 생성하고 결합
if __name__ == '__main__':
    addr = (host_addr, port)
    serversock = socket(AF_INET, SOCK_STREAM)
    # 소켓이 종료된 후 소켓 주소 재사용으로 인한 오류 방지를 위해
    # setsockopt 메서드에서 SO_REUSEADDR로 설정
    serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serversock.bind(addr)
    serversock.listen(5)

    # 크라이언트의 접속 요청을 받아 새로운 클라이언트 소켓을 생성한다.
    # 메인 스레드
    while True:
        print('waiting for connection...')
        clientsock, address = serversock.accept()
        print('...connected from: ', address)
        # 스레드 생성 실행
        _thread.start_new_thread(handler, (clientsock, address))


// 소켓 헤더파일을 가져다 쓰기위한 링크
#pragma comment(lib, "ws2_32")
#pragma comment(lib, "libmysql.lib")

#include <iostream>
// 소켓 헤더파일
#include <WinSock2.h>
#include <mysql.h>
#include <thread>
#include <vector>
#include <string>
#include <cstring>
#include <sstream>

#define LOGIN_PORT 7876
#define SCREEN_PORT 7878
#define LOGIN_SIZE 512
#define SCREEN_SIZE 700000

using namespace std;

SOCKET logInServer;
SOCKET screenServer;

// 클라이언트의 정보를 저장할 클래스
class Socket {
public: 
	SOCKET client;
	SOCKADDR_IN client_info = { 0 };
	int client_size = sizeof(client_info);
	int number;
	char grade;
	Socket()
	{
		client = { 0 };
		client_info = { 0 };
		client_size = sizeof(client_info);
		grade = 'n';
	}

	~Socket()
	{
		client = { 0 };
		client_info = { 0 };
		client_size = -1;
		number = -1;
	}
}; 
vector<Socket>l;
vector<Socket>s;

// 클라이언트에게서 오는 데이터 처리할 쓰레드 함수
void recvLogIn(SOCKET sock, int num)
{
	char buf[LOGIN_SIZE];
	cout << num << ".[로그인]" << endl;

	MYSQL Conn;
	MYSQL* ConnPtr = NULL;
	MYSQL_RES* Result;
	MYSQL_ROW Row;
	char query[256];

	while (1)
	{
		// ZeroMemory : 구조체 초기화 매크로 (0으로 채움)
		// ZeroMemory(구조체 주소, 받는 포인터 크기)
		ZeroMemory(&buf, LOGIN_SIZE);
		// recv : 대상 소켓으로부터 보내온 정보를 받는다.
		// recv(소켓, 수신 정보를 담을 배열주소, 그 배열의 크기, flag)
		// send : 대상 소켓에게 정보를 보낸다.
		// send(소켓, 수신 정보를 담을 배열주소, 그 배열의 크기, flag)
		recv(sock, buf, LOGIN_SIZE, 0);
		if (WSAGetLastError())
		{
			cout << num << ".[로그인 종료]" << endl;
			//l.erase(l.begin() + num);
			return;
		}
		cout << num << ".받은메시지 : " << buf << endl;

		istringstream ss(buf);
		string d_buf;
		vector<string>v_buf;
		v_buf.clear();
		while (getline(ss, d_buf, ','))
		{
			v_buf.push_back(d_buf);
		}

		if (v_buf[0] == "LOG_IN")
		{
			// mysql 연결 초기화
			mysql_init(&Conn);

			// DB 연결
			ConnPtr = mysql_real_connect(&Conn, "10.10.21.129", "testuser", "123456", "winform", 3306, NULL, 0);

			// 연결 오류 시 에러 출력
			if (ConnPtr == NULL)
			{
				cout << "MYSQL connection error : " << mysql_error(&Conn);
			}

			string s_query = "select * from winform.user where Id = '";
			s_query += v_buf[1] + "' and Password = '";
			s_query += v_buf[2] + "'";
			const char* a_query = s_query.c_str();
			cout << a_query << endl;

			// 문자열 복사
			strcpy_s(query, (a_query));
			// 쿼리 실행
			mysql_query(ConnPtr, query);
			// 결과값 저장
			Result = mysql_store_result(ConnPtr);
			// row 단위로 저장
			Row = mysql_fetch_row(Result);

			int columns = mysql_num_rows(Result);

			const char* out_buf;
			if (columns != 0)
			{
				// 문자열을 비교하려면 strcmp 를 쓰자
				if (strcmp(Row[2], "student") == 0)
				{
					out_buf = "student";
					l[num].grade = 's';
					s[num].grade = 's';
				}
				else if (strcmp(Row[2], "teacher") == 0)
				{
					out_buf = "teacher";
					l[num].grade = 't';
					s[num].grade = 't';
				}
				else
				{
					out_buf = "strange";
					l[num].grade = 'n';
					s[num].grade = 'n';
				}
			}
			else
			{
				out_buf = "NoData";
				l[num].grade = 'n';
				s[num].grade = 'n';
			}
			send(sock, out_buf, strlen(out_buf), 0);

			// 메모리 해제 / 메모리 누수 방지
			mysql_free_result(Result);

			// 연결 해제
			mysql_close(ConnPtr);
		}
	}
}

void recvScreen(SOCKET sock, int num)
{
	int index = 0;
	char buf[SCREEN_SIZE];
	cout << num << ".[스크린]" << endl;

	while (1)
	{
		int camSize;
		ZeroMemory(&buf, SCREEN_SIZE);

		recv(sock, (char*)&camSize, sizeof(int), 0);
		cout << camSize << endl;
		if (s[num].grade == 't')
		{
			if (s[index].grade == 's')
			{
				send(s[index].client, (char*)camSize, sizeof(int), 0);
				cout << "성공?" << endl;
			}
		}

		recv(sock, buf, camSize, 0);
		if (s[num].grade == 't')
		{
			if (s[index].grade == 's')
			{
				cout << index << "번째 클라이언트에게 전송" << endl;
				send(s[index].client, buf, camSize, 0);
				cout << "진짜 성공?" << endl;
			}
			index++;

			if (index == s.size())
			{
				index = 0;
			}
		}

		if (WSAGetLastError())
		{
			//int error = 0;
			//getsockopt(sock, SOL_SOCKET, SO_ERROR, (char*)error, (int*)sizeof(error));
			cout << WSAGetLastError() << endl;
			cout << num << ".[스크린 종료]" << endl;
			//s.erase(s.begin() + num);
			return;
		}

		//std::this_thread::sleep_for(std::chrono::seconds(50));
	}
}

// 클라이언트를 추가하는 쓰레드 함수
void acceptClients()
{
	int number = 0;
	while (1)
	{
		l.push_back(Socket());
		cout << "로그인 추가" << endl;
		s.push_back(Socket());
		cout << "스크린 추가" << endl;
		// accept : 접속 요청을 수락
		// accept(소켓, 소켓 구성요소 주소체의 주소, 그 구조체의 크기를 담고있는 변수의 주소)
		l[number].client = accept(logInServer, (SOCKADDR*)&l[number].client_info, &l[number].client_size);
		l[number].number = number;
		s[number].client = accept(screenServer, (SOCKADDR*)&s[number].client_info, &s[number].client_size);
		s[number].number = number;
		// thread.detach() : 메인 쓰레드와 무관하게 독립적으로 실행 / 백그라운드로 이동
		thread(recvLogIn, l[number].client, number).detach();
		cout << "로그인 스레드 시작" << endl;
		thread(recvScreen, s[number].client, number).detach();
		cout << "스크린 스레드 시작" << endl;
		number++;
	}
}

int main()
{
	cout << mysql_get_client_info() << endl;

	// WSADATA : Windows의 소켓 초기화 정보를 담는 구조체
	WSADATA wsa;
	// MAKEWORD(2, 2) : MAKEWORD 매크로를 이용해 2.2를 정수로 변환 / 소켓 버전
	WSAStartup(MAKEWORD(2, 2), &wsa);

	// PF_INET : IPV4
	// SOCK_STREAM : 연결지향형 소켓
	// IPPROTO_TCP : TCP (통신규약)
	logInServer = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);
	screenServer = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);

	// 소켓의 구성요소를 담을 구조체 생성 및 값 할당
	// SOCKADDR_IN : 주소정보를 담는 구조체
	// 구조체 초기화
	SOCKADDR_IN addr = { 0 };
	// s_addr : IPV4 Internet address / INADDR_ANY : 현재 컴퓨터의 IP 주소
	addr.sin_addr.s_addr = htonl(INADDR_ANY);
	// port 지정 / htons : host to network short 빅엔디안 방식으로 데이터 변환
	addr.sin_port = htons(LOGIN_PORT);
	// sin_family 는 무조건 AF_INET
	addr.sin_family = AF_INET;

	SOCKADDR_IN addr2 = { 0 };
	addr2.sin_addr.s_addr = htons(INADDR_ANY);
	addr2.sin_port = htons(SCREEN_PORT);
	addr2.sin_family = AF_INET;

	// bind : 소켓에 주소정보를 연결
	// bind(소켓, bind될 소켓에 할당할 주소정보를 담고 있는 구조체의 주소, 구조체의 크기)
	bind(logInServer, (SOCKADDR*)&addr, sizeof(addr));
	bind(screenServer, (SOCKADDR*)&addr2, sizeof(addr2));
	// listen : 소켓을 접속 대기 상태로 만들어 줌
	// SOMAXCONN : 한꺼번에 요청 가능한 최대 접속승인 수
	listen(logInServer, SOMAXCONN);
	listen(screenServer, SOMAXCONN);

	thread(acceptClients).detach();

	while (1); // 메인함수가 끝나지 않도록 한다?

	closesocket(logInServer);
	closesocket(screenServer);
	// WSACleanup() : WSAStartup 을 하면서 지정한 내용을 지운다.
	WSACleanup();

	return 0;
}

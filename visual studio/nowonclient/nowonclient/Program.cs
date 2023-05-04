using System;
using System.Threading;
using System.Linq;
using System.Text;
using System.Net;
using System.Net.Sockets;

namespace Example
{
    class Program
    {
        // 실행 함수
        static void Main(string[] args)
        {
            // 개행 코드
            char CR = (char)0x0D;
            char LF = (char)0x0A;
            // 수신 버퍼
            StringBuilder sb = new StringBuilder();
            // 소켓을 연다.
            using (Socket socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.IP))
            {
                // 로컬의 9090포트로 접속한다.
                socket.Connect(IPAddress.Parse("127.0.0.1"), 9090);
                // 수신을 위한 쓰레드
                ThreadPool.QueueUserWorkItem((_) =>
                {
                    while (true)
                    {
                        // 서버로 오는 메시지를 받는다.
                        byte[] ret = new byte[2];
                        socket.Receive(ret, 2, SocketFlags.None);
                        // 메시지를 unicode로 변환해서 버퍼에 넣는다.
                        sb.Append(Encoding.Unicode.GetString(ret, 0, 2));
                        // 개행 + \n이면 콘솔 출력한다.
                        if (sb.Length >= 4 && sb[sb.Length - 4] == CR && sb[sb.Length - 3] == LF && sb[sb.Length - 2] == '>' && sb[sb.Length - 1] == '\0')
                        {
                            // 버퍼의 메시지를 콘솔에 출력
                            string msg = sb.ToString();
                            Console.Write(msg);
                            // 버퍼를 비운다.
                            sb.Clear();
                        }
                    }
                });
                // 송신을 위한 입력대기
                while (true)
                {
                    // 콘솔 입력 대기
                    string k = Console.ReadLine();
                    byte[] data = Encoding.Unicode.GetBytes(k + "\r\n");
                    // 송신.
                    socket.Send(data, data.Length, SocketFlags.None);
                    // exit 명령어가 오면 종료
                    if ("exit".Equals(k, StringComparison.OrdinalIgnoreCase))
                    {
                        break;
                    }
                }
            }
        }
    }
}
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Net;
using System.Net.Sockets;

namespace cvclient
{
    class Program
    {
        static void Main(string[] args)
        {
            TcpClient tc = new TcpClient("10.10.21.129", 7876);

            NetworkStream stream = tc.GetStream();
            byte[] conn = Encoding.ASCII.GetBytes("Client Connected");
            stream.Write(conn, 0, conn.Length);

            while (true)
            {
                string msg = Console.ReadLine();
                byte[] buff = Encoding.ASCII.GetBytes(msg);

                stream.Write(buff, 0, buff.Length);

                byte[] outbuff = new byte[1024];
                int nbytes = stream.Read(outbuff, 0, outbuff.Length);
                string output = Encoding.ASCII.GetString(outbuff, 0, nbytes);

                Console.WriteLine($"{nbytes} bytes: {output}");

                if (msg == "EndGame")
                {
                    break;
                }
            }

            stream.Close();
            tc.Close();
        }
    }
}

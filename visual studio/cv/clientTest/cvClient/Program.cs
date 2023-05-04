using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Threading;
using System.Net;
using System.Net.Sockets;
using System.IO;

namespace cvClient
{
    static class Program
    {
        internal static bool cl_teacher = false;
        internal static bool cl_student = false;
        internal static bool log_out = false;

        internal static TcpClient logIn;
        internal static NetworkStream logInStream;
        internal static TcpClient screenCl;
        internal static NetworkStream screenStream;

        /// <summary>
        /// 해당 애플리케이션의 주 진입점입니다.
        /// </summary>
        [STAThread]
        static void Main()
        {
            logIn = new TcpClient("10.10.21.108", 7876);
            screenCl = new TcpClient("10.10.21.108", 7878);
            logInStream = logIn.GetStream();
            screenStream = screenCl.GetStream();
            //byte[] conn = Encoding.ASCII.GetBytes("Client Connected");
            //logInStream.Write(conn, 0, conn.Length);

            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new loginForm());

            if (cl_student)
            {
                Application.Run(new studentForm());
            }

            if (cl_teacher)
            {
                Application.Run(new teacherForm());
            }
        }
    }
}

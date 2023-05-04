using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

using System.Threading;
using System.Net;
using System.Net.Sockets;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.IO;


namespace clientTest
{
    public partial class Form1 : Form
    {
        StringBuilder sb;
        Socket socket;
        Thread thread;
        Thread thread_img;
        MemoryStream memoryStream1;

        public Form1()
        {
            InitializeComponent();
            opensock();
            
        }

        ~Form1()
        {
            sb.Clear();
            socket.Close();
            socket.Shutdown(SocketShutdown.Both);
            thread.Abort();
            thread_img.Abort();
            memoryStream1.Close();
        }

        private byte[] SToB(string str)
        {
            byte[] strByte = Encoding.UTF8.GetBytes(str);
            return strByte;
        }

        private string BToS(byte[] byt)
        {
            string str = Encoding.UTF8.GetString(byt);
            return str;
        }

        public void opensock()
        {
            sb = new StringBuilder();
            socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.IP);
            socket.Connect(IPAddress.Parse("127.0.0.1"), 9090);
            Console.WriteLine((IPEndPoint)socket.RemoteEndPoint);

            thread = new Thread(Reading);
            thread.Start();
        }

        public void Reading()
        {
            Console.WriteLine("Reading start");

            byte[] buffer = new byte[1024];
            int bytesRead = 0;
            while (true)
            {
                sb.Clear();
                Array.Clear(buffer, 0, buffer.Length);
                bytesRead = socket.Receive(buffer, 0, buffer.Length, SocketFlags.None);
                if (bytesRead == 0)
                {
                    break;
                }
                Console.WriteLine($"{bytesRead}bytes");
                sb.Append(BToS(buffer));
                try
                {
                    var json = JsonConvert.DeserializeObject<JObject>(sb.ToString());
                    int command = (int)json["command"];
                    Console.WriteLine($"Command: {command}");
                    switch (command)
                    {
                        case 1:
                            string msg = $"{json["name"]} : {json["msg"]}";
                            
                            listBox1.Items.Add(msg);
                            listBox1.TopIndex = listBox1.Items.Count - 1;
                            break;
                        default:
                            break;
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error parsing JSON: {ex.Message}");
                }
            }
        }

        // 채팅
        private void sendmsg()
        {
            messge msg = new messge { command = 1, msg = textBox1.Text, name = textBox2.Text };
            string json = JsonConvert.SerializeObject(msg);
            byte[] sendmsg = SToB(json);
            socket.Send(sendmsg, sendmsg.Length, SocketFlags.None);
            textBox1.Clear();
        }

        // UI 이벤트
        private void textBox1_KeyDown(object sender, KeyEventArgs e)
        {
            if(e.KeyCode == Keys.Enter)
            {
                sendmsg();
            }
        }
        private void button1_Click(object sender, EventArgs e)
        {
            sendmsg();
        }
    }

    public class messge
    {
        public int command { get; set; }
        public string msg { get; set; }
        public string name { get; set; }
    }
}

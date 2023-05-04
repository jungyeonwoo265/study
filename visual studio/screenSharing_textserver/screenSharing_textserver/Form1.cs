using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
// 추가
using System.Threading;
using System.Net;
using System.Net.Sockets;
using System.IO;

namespace screenSharing_textserver
{
    public partial class Form1 : Form
    {
        TcpListener listener1;
        TcpClient client1;
        NetworkStream networkStream1;
        MemoryStream memoryStream1;
        Bitmap bitmap1;
        IPHostEntry iPHostEntry1;
        Thread thread1;

        string serverIP;
        int serverPort;
        byte[] data;
        byte[] dataSizeFromClient;
        int receivedDataSize;
        int expectedDataSize;

        public Form1()
        {
            InitializeComponent();

            pictureBox1.SizeMode = PictureBoxSizeMode.StretchImage;

            serverPort = 9000;
            string hostName = Dns.GetHostName();
            iPHostEntry1 = Dns.GetHostEntry(hostName);
            foreach(IPAddress address in iPHostEntry1.AddressList)
            {
                if(address.AddressFamily == AddressFamily.InterNetwork)
                {
                    serverIP = address.ToString();
                    break;
                }
            }
            listBox1.Items.Add("serverIP: " + serverIP);

            data = new byte[1048576 * 10];

            dataSizeFromClient = new byte[sizeof(int)];
        }

        private void ThreadProc()
        {
            listener1 = new TcpListener(IPAddress.Any, serverPort);
            listener1.Start();

            client1 = listener1.AcceptTcpClient();
            listBox1.Items.Add ("client IP: "+ client1.Client.RemoteEndPoint.ToString().Split(':')[0]);
            networkStream1 = client1.GetStream();

            while(true)
            {
                try
                {
                    receivedDataSize = 0;

                    if(networkStream1.CanRead)
                    {
                        networkStream1.Read(dataSizeFromClient, 0, dataSizeFromClient.Length);
                        expectedDataSize = BitConverter.ToInt32(dataSizeFromClient, 0);
                        //listBox1.Items.Add("Expected data size: " + (expectedDataSize / 1024).ToString() + "Kb");

                        do
                        {
                            receivedDataSize += networkStream1.Read(data, receivedDataSize, expectedDataSize - receivedDataSize);
                        }
                        while (expectedDataSize != receivedDataSize);
                        { 
                        }
                    }
                    memoryStream1 = new MemoryStream(data, 0, receivedDataSize);
                    bitmap1 = new Bitmap(memoryStream1);
                    pictureBox1.Image = bitmap1;
                }
                catch (Exception ex) 
                {
                    listBox1.Items.Add(ex.Message);
                    listBox1.Items.Add(ex.StackTrace);
                    break;
                }
            }
            listener1.Stop();
            client1.Close();
            networkStream1.Close();
            memoryStream1.Close();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            if(thread1 == null || !thread1.IsAlive)
            {
                thread1 = new Thread(new ThreadStart(ThreadProc));
                thread1.Start();
                listBox1.Items.Add("Waiting for a client...");
            }
        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (thread1 != null && thread1.IsAlive)
            {
                listener1.Stop();
                thread1.Abort();
            }
        }
    }
}

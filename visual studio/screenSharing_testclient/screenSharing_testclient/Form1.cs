using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
//추가
using System.Threading;
using System.Net;
using System.Net.Sockets;
using System.IO;

namespace screenSharing_testclient
{
    public partial class Form1 : Form
    {
        TcpClient client1;
        NetworkStream networkstream1;
        MemoryStream memoryStream1;
        Bitmap screen1;
        Thread thread1;

        string serverIP;
        int serverPort;
        byte[] data;
        byte[] dataSizeForServer;
        int screenmode = 0;
        int form_X;
        int form_Y;
        int form_W;
        int form_H;


        public Form1()
        {
            InitializeComponent();

            pictureBox1.SizeMode = PictureBoxSizeMode.StretchImage;
            textBox1.Text = "10.10.21.108";
        }

        private void ThreadProc()
        {
            serverIP = textBox1.Text;
            serverPort = 9000;
            try
            {
                client1 = new TcpClient(serverIP, serverPort);
                networkstream1 = client1.GetStream();
                listBox1.Items.Add("connected to: " + client1.Client.RemoteEndPoint.ToString().Split(':')[0]);
            }
            catch(Exception ex) 
            {
                listBox1.Items.Add(ex.Message);
                listBox1.Items.Add(ex.StackTrace);

                return;
            }
            try
            {
                while(true)
                {
                    if(screenmode == 1)
                        screen1 = GetPartScreen();
                    else
                        screen1 = GetAllScreen();
                    memoryStream1 = new MemoryStream();
                    screen1.Save(memoryStream1, System.Drawing.Imaging.ImageFormat.Png);
                    data = memoryStream1.ToArray();
                    pictureBox1.Image = screen1;

                    if (networkstream1.CanWrite)
                    {
                        dataSizeForServer = BitConverter.GetBytes(data.Length);
                        networkstream1.Write(dataSizeForServer, 0, dataSizeForServer.Length);

                        networkstream1.Write(data, 0, data.Length);
                        //listBox1.Items.Add("Data sent: " + (data.Length / 1024).ToString() + "Kb");
                    }
                    Thread.Sleep(100);
                }
            }
            catch( Exception ex )
            {
                listBox1.Items.Add(ex.Message);
                listBox1.Items.Add(ex.StackTrace);
            }
            client1.Close();
            networkstream1.Close();
            memoryStream1.Close();
        }

        private Bitmap GetAllScreen()
        {
            Bitmap bitmap = new Bitmap(Screen.PrimaryScreen.Bounds.Width, Screen.PrimaryScreen.Bounds.Height);
            Graphics g = Graphics.FromImage(bitmap);
            g.CopyFromScreen(0, 0, 0, 0, bitmap.Size);

            return bitmap;
        }

        private Bitmap GetPartScreen()
        {
            if(this.Top > 0 && this.Left >0)
            {
                if (form_X != this.Width)
                    form_X = this.Width;
                if (form_Y != this.Height)
                    form_Y = this.Height;
                if (form_W != this.Left)
                    form_W = this.Left;
                if (form_H != this.Top)
                    form_H = this.Top;
            }

            Bitmap bitmap = new Bitmap(form_X,form_Y);
            Graphics g = Graphics.FromImage(bitmap);
            g.CopyFromScreen(form_W, form_H, 0, 0, bitmap.Size);

            return bitmap;
        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            Thread_Close();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            screenmode = 0;
            if (thread1 == null || !thread1.IsAlive)
            {
                thread1 = new Thread(new ThreadStart(ThreadProc));
                thread1.Start();
                listBox1.Items.Add("connecting to the server ...");
            }
        }

        private void Thread_Close()
        {
            if (thread1 != null && thread1.IsAlive)
            {
                thread1.Abort();
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            screenmode = 1;
            if (thread1 == null || !thread1.IsAlive)
            {
                thread1 = new Thread(new ThreadStart(ThreadProc));
                thread1.Start();
                listBox1.Items.Add("connecting to the server ...");
            }

        }
    }
}

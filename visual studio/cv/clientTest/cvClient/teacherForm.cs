using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;
using OpenCvSharp;
using System.IO;

namespace cvClient
{
    public partial class teacherForm : Form
    {

        bool isCameraOn;

        Thread thread;
        Thread thread2;
        Mat mat;
        VideoCapture video;

        MemoryStream m_stream;
        Bitmap screen;
        byte[] data;
        byte[] dataSize;

        public teacherForm()
        {
            InitializeComponent();

            pictureBox1.SizeMode = PictureBoxSizeMode.StretchImage;
            button1.Text = "Start";
            isCameraOn = false;

            pictureBox2.SizeMode = PictureBoxSizeMode.StretchImage;

            video_start();

            if (thread2 == null || !thread2.IsAlive)
            {
                thread2 = new Thread(new ThreadStart(screenProc));
                thread2.Start();
            }
        }

        //private void chat(object sender, KeyEventArgs e)
        //{
        //    if (e.KeyCode == Keys.Enter && stream.CanRead == true)
        //    {
        //        byte[] msg = Encoding.ASCII.GetBytes(textBox1.Text);
        //        stream.Write(msg, 0, msg.Length);

        //        textBox1.Text = "";
        //    }

        //    else if(e.KeyCode == Keys.Enter && stream.CanRead == false)
        //    {
        //        textBox1.Text = "";
        //        label1.Text = "DisConnected";
        //    }
        //}

        private void CameraCallback()
        {
            mat = new Mat();
            video = new VideoCapture(0);

            if (!video.IsOpened())
            {
                Text = "Camera open failed!";
                return;
            }

            while (true)
            {
                video.Read(mat);
                if (!mat.Empty())
                {
                    pictureBox1.Image = OpenCvSharp.Extensions.BitmapConverter.ToBitmap(mat);
                }
            }
        }

        private void screenProc()
        {
            while (true)
            {
                screen = GetScreen();
                m_stream = new MemoryStream();
                screen.Save(m_stream, System.Drawing.Imaging.ImageFormat.Png);
                data = m_stream.ToArray();
                pictureBox2.Image = screen;

                if (m_stream.CanWrite)
                {
                    dataSize = BitConverter.GetBytes(data.Length);
                    label1.Text = $"{data.Length}";
                    Program.screenStream.Write(dataSize, 0, dataSize.Length);
                    Thread.Sleep(10);

                    Program.screenStream.Write(data, 0, data.Length);
                }

                Thread.Sleep(40);
            }

            m_stream.Close();
        }

        private void video_start()
        {
            if (thread2 == null || !thread2.IsAlive)
            {
                thread2 = new Thread(new ThreadStart(screenProc));
                thread2.Start();
            }

            if (isCameraOn == false)
            {
                thread = new Thread(new ThreadStart(CameraCallback));

                thread.Start();
                isCameraOn = true;
                button1.Text = "Stop";
            }

            else
            {
                if (video.IsOpened())
                {
                    thread.Abort();
                    video.Release();
                    mat.Release();
                }

                if (thread2 != null && thread2.IsAlive)
                {
                    thread2.Abort();
                }

                isCameraOn = false;
                button1.Text = "Start";
            }
        }

        private void buttonClick(object sender, EventArgs e)
        {
            video_start();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private Bitmap GetScreen()
        {
            Bitmap bitmap = new Bitmap(Screen.PrimaryScreen.Bounds.Width, Screen.PrimaryScreen.Bounds.Height);
            Graphics g = Graphics.FromImage(bitmap);
            g.CopyFromScreen(0, 0, 0, 0, bitmap.Size);
            g.Dispose();

            return bitmap;
        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (thread != null && thread.IsAlive && video.IsOpened())
            {
                thread.Abort();
                video.Release();
                mat.Release();
            }

            if (thread2 != null && thread2.IsAlive)
            {
                thread2.Abort();
            }
        }

        private void buttonLogOut_Click(object sender, EventArgs e)
        {

        }
    }
}

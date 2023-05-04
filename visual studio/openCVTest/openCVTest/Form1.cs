using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using OpenCvSharp;
using OpenCvSharp.Extensions;
using System.Threading;
using System.IO;

namespace openCVTest
{
    public partial class Form1 : Form
    {
        int stopvi = 1;
        Thread t1;
        VideoCapture video;
        Mat frame;

        public Form1()
        {
            InitializeComponent();
            pictureBox1.SizeMode = PictureBoxSizeMode.StretchImage;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            if (t1 == null || !t1.IsAlive)
            {
                stopvi = 1;
                t1 = new Thread(new ThreadStart(showvideo));
                t1.Start();
                Console.WriteLine("스레드시작");
            }
        }

        private void showvideo()
        {
            Console.WriteLine("frame 초기화전");
            frame = new Mat();
            Console.WriteLine("video 초기화전");
            video = new VideoCapture(0);
            Console.WriteLine("try 전");
            try
            {
                Console.WriteLine("카메라 open 전");
                if (!video.IsOpened())
                {
                    MessageBox.Show("카메라 오픈 error");
                    return;
                }
                else
                {
                    Console.WriteLine("카메라 open");
                }

                while(stopvi != 0)
                {
                    video.Read(frame);
                    if(!frame.Empty())
                    {
                        pictureBox1.Image = OpenCvSharp.Extensions.BitmapConverter.ToBitmap(frame);
                    }
                }
            }
            catch(Exception ex)
            {
                MessageBox.Show("카메라 예외 발생: " + ex.Message);
            }
            finally
            {
                if(video != null)
                {
                    frame.Release();
                    video.Release();
                }
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            stopvi = 0;
            t1.Join();

        }
    }
}

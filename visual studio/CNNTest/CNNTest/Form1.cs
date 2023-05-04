using System;
using System.Windows.Forms;
using OpenCvSharp.Extensions;

using OpenCvSharp;

namespace CNNTest
{
    public partial class Form1 : Form
    {
        VideoCapture video;
        Mat frame;
        bool stopvi = false;

        public Form1()
        {
            InitializeComponent();
            pictureBox1.SizeMode = PictureBoxSizeMode.StretchImage;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            frame = new Mat();
            video = new VideoCapture();
            try
            {
                if(!video.IsOpened())
                {
                    MessageBox.Show("카메라 open error");
                    return;
                }
                while(!stopvi)
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
                if (video != null)
                {
                    frame.Release();
                    video.Release();
                }
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            stopvi = true;
        }
    }
}

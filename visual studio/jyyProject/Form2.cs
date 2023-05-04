using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;
using System.Windows.Forms;
using System.IO;

using System.Net.Sockets;
using System.Net;
using System.Diagnostics;
using System.Drawing.Drawing2D;

using OpenCvSharp;
using OpenCvSharp.Extensions;
using System.Runtime.InteropServices.ComTypes;
using Newtonsoft.Json.Linq;
using static System.Net.WebRequestMethods;
using WMPLib;
using MySql.Data.MySqlClient;

namespace jyyProject
{
    public partial class Form2 : Form
    {
        MySqlConnection connection = new MySqlConnection("Server=10.10.21.119;Database=prevention;Uid=jyy;Pwd=0000;");

        WindowsMediaPlayer wmp;
        int plus_speed = 0;
        double rpm_value = 200;
        bool driving = false; // 스피드 멈추게하기위해서

        TcpClient client = new TcpClient();
        Thread videoThread;
        Thread receivedThread;
        VideoCapture videoCapture;
        Mat mat = new Mat();
        NetworkStream stream1;
        string path = "C:\\Users\\Kiot\\source\\repos\\jyyProject\\자동차 사진\\";
        byte receivedByte;
        int closeeye = 0;
        int second = 0;
        System.IO.DirectoryInfo openwindows;
        System.IO.DirectoryInfo closewindows;
        int time = 0;
        bool facedic = true;
        int second1 = 0;
        DateTime startDate;

        public Form2()
        {
            InitializeComponent();
            pictureBox3.Hide();
            pictureBox4.Hide();
            pictureBox5.Hide();
            pictureBox6.Hide();
            Gear.Text = "P";
            Rpm.Text = "200";
            wmp = new WindowsMediaPlayer();
            client.Connect("10.10.21.109", 9000);
            stream1 = client.GetStream();

            driving_cam.SizeMode = PictureBoxSizeMode.StretchImage;
            warning.SizeMode = PictureBoxSizeMode.StretchImage;
            window.SizeMode = PictureBoxSizeMode.StretchImage;

            warning.Image = OpenCvSharp.Extensions.BitmapConverter.ToBitmap(Cv2.ImRead(path + "back22.jpg"));
            window.Image = OpenCvSharp.Extensions.BitmapConverter.ToBitmap(Cv2.ImRead(path + "car.png"));
            closewindows = new System.IO.DirectoryInfo(path + "close_window");
            openwindows = new System.IO.DirectoryInfo(path + "open_window");
            video_start();
            received_data_start();
        }

        private void video_start()
        {
            videoThread = new Thread(new ThreadStart(CameraCallback));
            videoThread.IsBackground = true;
            videoThread.Start();
        }

        private void received_data_start()
        {
            receivedThread = new Thread(new ThreadStart(received_data));
            receivedThread.Start();
        }

        private void received_data()
        {

            try
            {
                while (true)
                {

                    // 한 글자의 숫자를 받기 위해 바이트 배열의 크기를 1로 설정
                    // 수신 버퍼를 생성
                    byte[] buffer = new byte[4];
                    // 소켓을 통해 데이터를 수신
                    int bytesRead = stream1.Read(buffer, 0, buffer.Length);
                    int num = BitConverter.ToInt32(buffer, 0);

                    receivedByte = buffer[0]; // receivedByte 변수 선언
                    Console.WriteLine($"receivedByte: {receivedByte}");
                    int speedint = Convert.ToInt32(speed.Text);
                    if (receivedByte == 0 || receivedByte == 1)
                    {
                        facedic = true;
                    }
                    else
                    {
                        facedic = false;
                    }
                    if (receivedByte == 0 && second < 60)
                    {
                        closeeye = 0;
                        second = 0;
                        hiedpic();
                    }
                    else if (receivedByte == 1 && speedint > 0)
                    {
                        closeeye++;
                    }
                }
            }
            catch
            {
                Console.WriteLine("받은문자오류");
            }
        }

        private void CameraCallback()
        {
            videoCapture = new VideoCapture(0);
            stream1 = client.GetStream();
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();
            int time = 0;
            bool send = true;
            while (true)
            {
                try
                {
                    videoCapture.Read(mat);
                    Bitmap bitmap = BitmapConverter.ToBitmap(mat);
                    driving_cam.Image = bitmap;
                    time = (int)(stopwatch.ElapsedMilliseconds / 100);
                    if (time % 5 == 0 && send)
                    {
                        send = false;
                        byte[] data = mat.ToBytes();
                        stream1.Write(BitConverter.GetBytes(data.Length), 0, 4);
                        stream1.Write(data, 0, data.Length);
                    }
                    else if (time % 5 != 0)
                    {
                        send = true;
                    }
                }
                catch (IOException ex)
                {
                    // 데이터 전송 중 예외 처리
                    Console.WriteLine("데이터 전송 중 예외 발생: " + ex.Message);
                    break;
                    // 필요한 예외 처리 로직 추가
                }
                catch (Exception ex)
                {
                    // 기타 예외 처리
                    Console.WriteLine("예외 발생: " + ex.Message);
                    break;
                    // 필요한 예외 처리 로직 추가
                }

            }
            stopwatch.Stop();
        }

        private void home_Click(object sender, EventArgs e)
        {
            this.Hide();
            Form1 form1 = new Form1();
            form1.ShowDialog();
            this.Close();
        }

        private void check_Click(object sender, EventArgs e)
        {
            pictureBox3.Show();
            pictureBox4.Show();
            pictureBox5.Show();
            pictureBox6.Show();
        }

        private void hiedpic()
        {
            pictureBox3.Hide();
            pictureBox4.Hide();
            pictureBox5.Hide();
            pictureBox6.Hide();
            warning.Image = OpenCvSharp.Extensions.BitmapConverter.ToBitmap(Cv2.ImRead(path + "back22.jpg"));
        }

        private void timer1_Tick(object sender, EventArgs e)    // 1초가 아닌 0.5초로줌
        {
            label3.Text = second.ToString();

            if (second == 20)    // 2초(0.5*8) 졸고있는 사진 표시
            {
                pictureBox3.Show();

            }
            if (second >= 20)
            {
                if (second - 20 < openwindows.GetFiles().Length)
                    window.Image = OpenCvSharp.Extensions.BitmapConverter.ToBitmap(Cv2.ImRead(path + "open_window\\" + openwindows.GetFiles()[second - 20]));
            }

            if (second >= 40)    // 4초(0.5*16) 비상등 표시
            {
                if (second % 10 == 0)    // 짝수초에 비상등 표시
                {
                    warning.Image = OpenCvSharp.Extensions.BitmapConverter.ToBitmap(Cv2.ImRead(path + "back11.jpg"));
                    pictureBox4.Show();
                    pictureBox5.Show();
                }
                else if (second % 10 == 5)    // 홀수초에 비상등 숨김
                {
                    warning.Image = OpenCvSharp.Extensions.BitmapConverter.ToBitmap(Cv2.ImRead(path + "back22.jpg"));
                    pictureBox4.Hide();
                    pictureBox5.Hide();
                }
            }

            if (second >= 60)   // 6초(0.5*24)
            {
                if (wmp.playState != WMPLib.WMPPlayState.wmppsPlaying)
                {
                    pictureBox6.Show();
                    warningSound();
                }
            }
            second++;
        }

        private void warningSound()
        {
            if (wmp.playState != WMPLib.WMPPlayState.wmppsPlaying)
            {
                wmp.URL = path + "warningSound.mp3";
                wmp.controls.play();
            }
        }

        private void timer2_Tick(object sender, EventArgs e)
        {
            if (time % 5 == 0)
                plus_speed--;
            if (!timer1.Enabled && closeeye == 3)
            {
                timer1.Start();
            }
            else if(timer1.Enabled && closeeye == 0 && second < 60)
            {
                timer1.Stop();
            }

            if (driving)
            {
                speedUp();
            }
            else if(!driving)
            {
                speedDown();
            }

            if(plus_speed == 0)
            {
                Gear.Text = "P";
            }
            else
            {
                Gear.Text = "D";
            }

            if(!timer1.Enabled && closeeye <= 3 && !facedic)
            {
                CautionSound();
            }
            time++;
        }
        private void CautionSound()
        {
            if (wmp.playState != WMPLib.WMPPlayState.wmppsPlaying)
            {
                wmp.URL = path + "CautionSound.mp3";
                wmp.controls.play();
            }
        }


        public void speedUp()
        {

            if (plus_speed < 200)  // 속도제한 시키기
            {
                plus_speed += 1;    // 속도 1씩 증가
                speed.Text = plus_speed.ToString();
            }
            if (plus_speed % 25 ==0 && plus_speed !=0)
            {
                rpm_value = 1000 + (plus_speed * 10);
            }
            else
            {
                if(plus_speed <= 25)
                {
                    rpm_value = (int)(rpm_value * 1.1);
                }
                else
                {
                    rpm_value = (int)(rpm_value + (4000 - rpm_value) / 25);
                }
            }

            Rpm.Text = rpm_value.ToString();
        }

        public void speedDown()
        {
            if (plus_speed > 0)  // 속도제한 시키기
            {
                plus_speed -= 1; // 속도 1씩 감소
                speed.Text = plus_speed.ToString();
            }

            if(rpm_value > 200)
            {
                rpm_value = (int)(rpm_value- ((rpm_value-200)/plus_speed)); 
            }
            else
            {
                rpm_value = 200;
            }

            Rpm.Text = rpm_value.ToString();

            if (plus_speed == 0)
            {
                
                timer1.Stop();
                wmp.close();
                second = 0;
                rpm_value = 200;
                Rpm.Text = rpm_value.ToString();
                hiedpic();
                timer3.Start();
                timer2.Stop();
                insertDB();
            }
        }

        private void Accelerator_Click(object sender, EventArgs e)
        {
            if (!timer2.Enabled)
            {
                startDate = DateTime.Now;
                timer2.Start();
            }
            driving = true;
            
        }

        private void Break_Click(object sender, EventArgs e)
        {
            driving = false;
        }

        private void Form2_FormClosed(object sender, FormClosedEventArgs e)
        {
            
            videoThread.Abort();
            receivedThread.Abort();
            stream1.Close();
            client.Close();
        }

        private void insertDB()
        {
           try
            {
                string selectQuery = $"insert into user_info values('{startDate.ToString("yyyy-MM-dd hh:mm:ss")}',now());";
                connection.Open();
                MySqlCommand command = new MySqlCommand(selectQuery, connection);

                if (command.ExecuteNonQuery() == 1)
                {
                    Console.WriteLine("인서트 성공");
                }
                else
                {
                    Console.WriteLine("인서트 실패");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
            finally
            {
                connection.Close();
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            timer1.Start();
        }

        private void timer3_Tick(object sender, EventArgs e)
        {
            second1++;
            if (second1 < closewindows.GetFiles().Length)
            {
                window.Image = OpenCvSharp.Extensions.BitmapConverter.ToBitmap(Cv2.ImRead(path + "close_window\\" + closewindows.GetFiles()[second1]));
            }
            else
            {
                second1 = 0;
                timer3.Stop();
            }
        }
    }
}

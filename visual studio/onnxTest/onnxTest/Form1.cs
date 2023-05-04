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
using Microsoft.ML;
using Microsoft.ML.Data;
using Microsoft.ML.Transforms.Onnx;
using System.Drawing.Imaging;
using Size = OpenCvSharp.Size;

namespace onnxTest
{
    public partial class Form1 : Form
    {
        static string ONNX_MODEL_PATH = "jyw_model.onnx";
        MLContext mlContext = new MLContext();
        int stopvi = 1;
        Thread t1;
        VideoCapture video;
        Mat frame;
        float img;

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
            CascadeClassifier faceCascade = new CascadeClassifier("haarcascade_frontalface_alt.xml");
            CascadeClassifier leftEyeCascade = new CascadeClassifier("haarcascade_lefteye_2splits.xml");
            CascadeClassifier rightEyeCascade = new CascadeClassifier("haarcascade_righteye_2splits.xml");

            //var onnxPredictionPipeline = GetPredictionPipeline(mlContext);
            //var onnxPredictionEngine = mlContext.Model.CreatePredictionEngine<OnnxInput, OnnxOutput>(onnxPredictionPipeline);
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
                    timer1.Start();
                }

                while (stopvi != 0)
                {
                    int leftScour = 0;
                    int rightScour = 0;

                    video.Read(frame);
                    if (!frame.Empty())
                    {
                        Rect[] faces = faceCascade.DetectMultiScale(frame);

                        foreach (var item in faces)
                        {
                            //Cv2.Rectangle(frame, item, Scalar.Red);
                            Rect[] leftEyes = leftEyeCascade.DetectMultiScale(frame);


                            foreach (var leftEye in leftEyes)
                            {
                                //Cv2.Rectangle(frame, leftEye, Scalar.Blue);
                                Mat leftEyeMat = CropFrame(frame, leftEye);
                                leftScour = modelCheck(leftEyeMat);
                                //pictureBox2.Image = OpenCvSharp.Extensions.BitmapConverter.ToBitmap(leftEyeMat);
                                //Thread.Sleep(1000);
                                break;
                            }
                            Rect[] rightEyes = rightEyeCascade.DetectMultiScale(frame);
                            foreach (var rightEye in rightEyes)
                            {
                                //Cv2.Rectangle(frame, rightEye, Scalar.Blue);
                                Mat rightEyeMat = CropFrame(frame, rightEye);
                                //rightScour = modelCheck(rightEyeMat);
                                //pictureBox3.Image = OpenCvSharp.Extensions.BitmapConverter.ToBitmap(rightEyeMat);
                                //Thread.Sleep(1000);
                                break;
                            }
                            break;
                        }

                        //if(leftScour == 1 || rightScour ==1)
                        //    Console.WriteLine("졸음");
                        pictureBox1.Image = OpenCvSharp.Extensions.BitmapConverter.ToBitmap(frame);
                        Console.WriteLine("===================================");
                        //Thread.Sleep(10000);
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("카메라 예외 발생: " + ex.Message);
            }
            finally
            {
                if (video != null)
                {
                    frame.Release();
                    video.Release();
                    t1.Join();
                }
            }
        }
        private void button2_Click(object sender, EventArgs e)
        {
            stopvi = 0;
            t1.Join();
            pictureBox1.Dispose();
        }

        public static Mat CropFrame(Mat frame, Rect rect)
        {
            return new Mat(frame, rect);
        }

        public int modelCheck(Mat mat)
        {
            int scour = 0;
            var onnxPredictionPipeline = GetPredictionPipeline(mlContext);
            var onnxPredictionEngine = mlContext.Model.CreatePredictionEngine<OnnxInput, OnnxOutput>(onnxPredictionPipeline);

            Mat resizeEye = new Mat(34, 26, MatType.CV_32FC3);
            Mat grayEye = new Mat(34, 26, MatType.CV_32FC1);
            Cv2.Resize(mat, resizeEye, new Size(26, 34));
            Cv2.CvtColor(resizeEye, grayEye, ColorConversionCodes.BGR2GRAY);
            Console.WriteLine(grayEye.Rows);
            pictureBox2.Image = OpenCvSharp.Extensions.BitmapConverter.ToBitmap(grayEye);

            var floatArray = new float[grayEye.Total()];

            for (int r = 0; r < grayEye.Rows; r++)
            {
                for (int c = 0; c < grayEye.Cols; c++)
                {
                    floatArray[r * grayEye.Cols + c] = grayEye.At<float>(r, c);

                    if (float.IsNaN(floatArray[r * grayEye.Cols + c]))
                    {
                        Console.WriteLine($"{floatArray[r * grayEye.Cols + c]} -> {img}");
                        //Console.WriteLine(grayEye.At<int>(r, c));
                        //Console.WriteLine((float)grayEye.At<int>(r, c));
                        floatArray[r * grayEye.Cols + c] = img;
                    }
                    else
                    {
                        img = grayEye.At<float>(r, c);
                    }
                }
            }

            var eyeInput = new OnnxInput { image = floatArray };
            var leftprediction = onnxPredictionEngine.Predict(eyeInput);

            Console.WriteLine();
            Console.WriteLine($"SCOUR: {leftprediction.scour.First()}");
            Console.WriteLine();

            if (leftprediction.scour.First() != 0)
                scour = 1;

            return scour;
        }

        static ITransformer GetPredictionPipeline(MLContext mLContext)
        {
            var inputCloumns = new string[]
                {
                    "input_1"
                };
            var outputCloumns = new string[]
                {
                    "activation_1"
                };
            var onnxPredictionPipeline =
                mLContext
                .Transforms
                .ApplyOnnxModel(
                    outputColumnNames: outputCloumns,
                    inputColumnNames: inputCloumns,
                    ONNX_MODEL_PATH);

            var emptyDv = mLContext.Data.LoadFromEnumerable(new OnnxInput[] { });

            return onnxPredictionPipeline.Fit(emptyDv);
        }

    }

    public class OnnxInput
    {
        [ColumnName("input_1")]
        [VectorType(1, 34, 26)]
        public float[] image { get; set; }

    }

    public class OnnxOutput
    {
        [ColumnName("activation_1")]
        public float[] scour { get; set; }
    }


}


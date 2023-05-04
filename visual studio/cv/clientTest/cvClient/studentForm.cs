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
using System.IO;

namespace cvClient
{
    public partial class studentForm : Form
    {
        Thread thread;
        MemoryStream m_stream;
        Bitmap bitmap;

        public studentForm()
        {
            InitializeComponent();

            camBox.SizeMode = PictureBoxSizeMode.StretchImage;
            screenBox.SizeMode = PictureBoxSizeMode.StretchImage;

            thread = new Thread(new ThreadStart(getScreen));
            thread.Start();
        }

        private void getScreen()
        {
            while (true)
            {
                byte[] dataSizeByte = new byte[sizeof(int)];
                Program.screenStream.Read(dataSizeByte, 0, dataSizeByte.Length);
                int dataSize = BitConverter.ToInt32(dataSizeByte, 0);

                byte[] screenImage = new byte[dataSize];
                Program.screenStream.Read(screenImage, 0, screenImage.Length);

                m_stream = new MemoryStream(screenImage, 0, screenImage.Length);
                bitmap = new Bitmap(m_stream);
                screenBox.Image = bitmap;
            }
        }

        private void studentForm_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (thread != null && thread.IsAlive)
            {
                thread.Abort();
            }
            if (m_stream != null)
            {
                m_stream.Close();
            }
        }
    }
}

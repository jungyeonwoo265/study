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
using WMPLib;

namespace AudioTest
{
    public partial class Form1 : Form
    {
        WindowsMediaPlayer wmp;
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            wmp = new WindowsMediaPlayer();
            wmp.URL = "C:\\Users\\Kiot\\Downloads\\sample.mp3";
            wmp.controls.play();
            
        }

        private void button2_Click(object sender, EventArgs e)
        {
            wmp.close();
        }
    }
}

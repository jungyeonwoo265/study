using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace cvClient
{
    public partial class loginForm : Form
    {
        public loginForm()
        {
            InitializeComponent();
        }

        private void buttonJoin_Click(object sender, EventArgs e)
        {
            string user = "LOG_IN," + textId.Text + "," + textPass.Text;
            byte[] conn = Encoding.ASCII.GetBytes(user);
            Program.logInStream.Write(conn, 0, conn.Length);

            byte[] signal = new byte[50];
            Program.logInStream.Read(signal, 0, signal.Length);
            string grade = Encoding.ASCII.GetString(signal);

            if (string.Compare(grade, "teacher") == 0)
            {
                Program.cl_teacher = true;
                this.Close();
            }
            else if (string.Compare(grade, "student") == 0)
            {
                Program.cl_student = true;
                this.Close();
            }
            else
            {
                MessageBox.Show("잘못된 정보");
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            new joinForm().Show();
        }
    }
}

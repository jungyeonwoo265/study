using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WindowsFormsApp2
{
    public partial class sigin : Form
    {

        public sigin()
        {
            InitializeComponent();
            this.db = new G_f.DB();
        }

        G_f.DB db;
        bool idcheck = false;

        private void button1_Click(object sender, EventArgs e)
        {
            if(!this.idcheck)
                MessageBox.Show("ID 중복 확인 누락");
            else if(this.textBox2.Text == "")
                MessageBox.Show("이름 누락");
            else if (this.textBox3.Text == "")
                MessageBox.Show("전화번호 누락");
            else if (this.textBox4.Text == "")
                MessageBox.Show("email 누락");
            else if(this.textBox1.Text != this.textBox6.Text)
                MessageBox.Show("비밀번호 다름");
            else
            {
                string sqlstr = $"select * from sigin";
                DataTable dt = this.db.read(sqlstr);
                int number = dt.Rows.Count + 1;
                string name = this.textBox2.Text;
                string phon = this.textBox3.Text;
                string email = this.textBox4.Text;
                string id = this.textBox5.Text;
                string pw = this.textBox6.Text;
                sqlstr = $"insert into sigin (number, name, phon, email, ID, pW) values ('{number}','{name}','{phon}','{email}','{id}','{pw}');";
                db.insert(sqlstr);
                MessageBox.Show("가입성공");
                this.Hide();
                login showlogin = new login();
                showlogin.Show();
            }
        }

        private void label7_Click(object sender, EventArgs e)
        {
            string id = this.textBox5.Text;
            if (id != "")
            {
                string sqlstr = $"select * from sigin where ID = '{id}'";
                DataTable dt = this.db.read(sqlstr);
                if (dt.Rows.Count == 0)
                {
                    MessageBox.Show("ID 사용가능");
                    this.idcheck = true;
                }
                else
                {
                    MessageBox.Show("ID 중복");
                    this.textBox5.Clear();
                }
            }
            else
                MessageBox.Show("ID 누락");
        }

        private void button2_Click(object sender, EventArgs e)
        {
            this.Hide();
            login showlogin = new login();
            showlogin.Show();
        }
    }
}

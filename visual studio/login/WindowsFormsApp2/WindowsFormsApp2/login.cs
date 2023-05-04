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
    public partial class login : Form
    {
        G_f.DB db;
        public login()
        {
            InitializeComponent();
            this.db = new G_f.DB();
        }

        private void label3_Click(object sender, EventArgs e)
        {
            this.Hide();
            sigin showsigin = new sigin();
            showsigin.Show();
        }

        private void bt_sigin_Click(object sender, EventArgs e)
        {
            string idstr = this.textBox1.Text;
            string pwstr = this.textBox2.Text;
            string sqlstr = $"select * from sigin where ID ='{idstr}' and PW ='{pwstr}';";
            DataTable dt = db.read(sqlstr);
            if (dt.Rows.Count == 0)
                MessageBox.Show("회원 가입 필요");
            else
            {
                MessageBox.Show("로그인 성공");
                this.Hide();
                main showmain = new main();
                showmain.Show();
            }
        }

        private void bt_cencel_Click(object sender, EventArgs e)
        {
            this.Close();
        }
    }
}

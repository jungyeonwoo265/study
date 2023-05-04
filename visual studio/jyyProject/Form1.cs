using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Data.SqlClient;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using MySql.Data.MySqlClient;


namespace jyyProject
{
    public partial class Form1 : Form
    {
        MySqlConnection connection = new MySqlConnection("Server=10.10.21.119;Database=prevention;Uid=jyy;Pwd=0000;");

        public Form1()
        {
            InitializeComponent();
        }

        private void pictureBox2_Click(object sender, EventArgs e)
        {
            Console.WriteLine("시동");
            try
            {
                string selectQuery = "SELECT * FROM prevention.user_info";
                MySqlCommand command = new MySqlCommand(selectQuery, connection);
                connection.Open();
                MySqlDataReader reader = command.ExecuteReader();

                while (reader.Read())
                {
                    int num = reader.GetInt32("num");
                    string name = reader.GetString("name");
                    Console.WriteLine("id: {0}, name: {1}", num, name);

                }
                reader.Close();
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
            finally
            {
                connection.Close();
            }

            this.Hide();
            Form2 form2 = new Form2();
            form2.ShowDialog();
            this.Close();

        }
    }
}

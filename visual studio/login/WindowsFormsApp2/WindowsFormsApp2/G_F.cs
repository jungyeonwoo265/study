using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using MySql.Data.MySqlClient;
using System.Data;
using System.Windows.Forms;

namespace G_f
{
    class DB
    {
        string mysql;
        MySqlConnection conn;

        public DB()
        {
            this.mysql = "Server = localhost; port=3306; Database = testcshap; Uid=root; Pwd=0000";
            this.conn = new MySqlConnection(this.mysql);
            if(conn.State == ConnectionState.Open)
                Console.WriteLine("DB연결");
        }

        public DataTable read(string sqlstr)
        {
            this.conn.Open();
            MySqlCommand sc;
            MySqlDataReader reader;
            DataTable dt = new DataTable();
            sc = new MySqlCommand(sqlstr, conn);
            reader = sc.ExecuteReader();
            dt.Load(reader);
            this.conn.Close();
            return dt;
        }

        public void insert(string sqlstr)
        {
            MySqlCommand sc = new MySqlCommand();
            try
            {
                //this.conn.Open();
                sc.Connection = this.conn;
                sc.CommandText = sqlstr;
                sc.CommandType = CommandType.Text;
                sc.Connection.Open();
                sc.ExecuteNonQuery();
                sc.Connection.Close();
                //this.conn.Close();
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
                sc.Connection.Close();
            }
        }
    }
}

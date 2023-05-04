
namespace cvClient
{
    partial class studentForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.camBox = new System.Windows.Forms.PictureBox();
            this.screenBox = new System.Windows.Forms.PictureBox();
            this.label1 = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.camBox)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.screenBox)).BeginInit();
            this.SuspendLayout();
            // 
            // camBox
            // 
            this.camBox.Location = new System.Drawing.Point(33, 32);
            this.camBox.Name = "camBox";
            this.camBox.Size = new System.Drawing.Size(400, 400);
            this.camBox.TabIndex = 0;
            this.camBox.TabStop = false;
            // 
            // screenBox
            // 
            this.screenBox.Location = new System.Drawing.Point(587, 32);
            this.screenBox.Name = "screenBox";
            this.screenBox.Size = new System.Drawing.Size(600, 600);
            this.screenBox.TabIndex = 1;
            this.screenBox.TabStop = false;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(367, 469);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(38, 12);
            this.label1.TabIndex = 2;
            this.label1.Text = "label1";
            // 
            // studentForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1264, 721);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.screenBox);
            this.Controls.Add(this.camBox);
            this.Name = "studentForm";
            this.Text = "Form1";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.studentForm_FormClosing);
            ((System.ComponentModel.ISupportInitialize)(this.camBox)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.screenBox)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.PictureBox camBox;
        private System.Windows.Forms.PictureBox screenBox;
        private System.Windows.Forms.Label label1;
    }
}
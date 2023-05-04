namespace jyyProject
{
    partial class Form2
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
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form2));
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.Accelerator = new System.Windows.Forms.Button();
            this.Break = new System.Windows.Forms.Button();
            this.label5 = new System.Windows.Forms.Label();
            this.home = new System.Windows.Forms.Button();
            this.check = new System.Windows.Forms.Button();
            this.speed = new System.Windows.Forms.Label();
            this.Rpm = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.button1 = new System.Windows.Forms.Button();
            this.timer1 = new System.Windows.Forms.Timer(this.components);
            this.pictureBox6 = new System.Windows.Forms.PictureBox();
            this.pictureBox3 = new System.Windows.Forms.PictureBox();
            this.pictureBox5 = new System.Windows.Forms.PictureBox();
            this.pictureBox4 = new System.Windows.Forms.PictureBox();
            this.window = new System.Windows.Forms.PictureBox();
            this.pictureBox1 = new System.Windows.Forms.PictureBox();
            this.warning = new System.Windows.Forms.PictureBox();
            this.driving_cam = new System.Windows.Forms.PictureBox();
            this.Gear = new System.Windows.Forms.Label();
            this.timer2 = new System.Windows.Forms.Timer(this.components);
            this.timer3 = new System.Windows.Forms.Timer(this.components);
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox6)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox3)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox5)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox4)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.window)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.warning)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.driving_cam)).BeginInit();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("굴림", 14.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(129)));
            this.label1.Location = new System.Drawing.Point(818, 3);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(69, 19);
            this.label1.TabIndex = 3;
            this.label1.Text = "카메라";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Font = new System.Drawing.Font("굴림", 14.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(129)));
            this.label2.Location = new System.Drawing.Point(631, 524);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(123, 19);
            this.label2.TabIndex = 4;
            this.label2.Text = "비상등(외부)";
            // 
            // Accelerator
            // 
            this.Accelerator.Font = new System.Drawing.Font("굴림", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(129)));
            this.Accelerator.Location = new System.Drawing.Point(12, 421);
            this.Accelerator.Name = "Accelerator";
            this.Accelerator.Size = new System.Drawing.Size(143, 62);
            this.Accelerator.TabIndex = 6;
            this.Accelerator.Text = "가속";
            this.Accelerator.UseVisualStyleBackColor = true;
            this.Accelerator.Click += new System.EventHandler(this.Accelerator_Click);
            // 
            // Break
            // 
            this.Break.Font = new System.Drawing.Font("굴림", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(129)));
            this.Break.Location = new System.Drawing.Point(223, 421);
            this.Break.Name = "Break";
            this.Break.Size = new System.Drawing.Size(141, 62);
            this.Break.TabIndex = 7;
            this.Break.Text = "감속";
            this.Break.UseVisualStyleBackColor = true;
            this.Break.Click += new System.EventHandler(this.Break_Click);
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Font = new System.Drawing.Font("굴림", 14.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(129)));
            this.label5.Location = new System.Drawing.Point(631, 421);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(49, 19);
            this.label5.TabIndex = 11;
            this.label5.Text = "창문";
            // 
            // home
            // 
            this.home.Location = new System.Drawing.Point(423, 509);
            this.home.Name = "home";
            this.home.Size = new System.Drawing.Size(90, 55);
            this.home.TabIndex = 19;
            this.home.Text = "홈";
            this.home.UseVisualStyleBackColor = true;
            this.home.Click += new System.EventHandler(this.home_Click);
            // 
            // check
            // 
            this.check.Location = new System.Drawing.Point(423, 448);
            this.check.Name = "check";
            this.check.Size = new System.Drawing.Size(90, 55);
            this.check.TabIndex = 20;
            this.check.Text = "hide체크";
            this.check.UseVisualStyleBackColor = true;
            this.check.Click += new System.EventHandler(this.check_Click);
            // 
            // speed
            // 
            this.speed.AutoSize = true;
            this.speed.BackColor = System.Drawing.SystemColors.ActiveCaptionText;
            this.speed.Font = new System.Drawing.Font("굴림", 27.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(129)));
            this.speed.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.speed.Location = new System.Drawing.Point(122, 217);
            this.speed.Name = "speed";
            this.speed.Size = new System.Drawing.Size(83, 37);
            this.speed.TabIndex = 22;
            this.speed.Text = "000";
            // 
            // Rpm
            // 
            this.Rpm.AutoSize = true;
            this.Rpm.BackColor = System.Drawing.SystemColors.ActiveCaptionText;
            this.Rpm.Font = new System.Drawing.Font("굴림", 27.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(129)));
            this.Rpm.ForeColor = System.Drawing.SystemColors.ButtonFace;
            this.Rpm.Location = new System.Drawing.Point(588, 217);
            this.Rpm.Name = "Rpm";
            this.Rpm.Size = new System.Drawing.Size(0, 37);
            this.Rpm.TabIndex = 24;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Font = new System.Drawing.Font("굴림", 20F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(129)));
            this.label3.Location = new System.Drawing.Point(69, 509);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(0, 27);
            this.label3.TabIndex = 27;
            // 
            // button1
            // 
            this.button1.Location = new System.Drawing.Point(74, 546);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(75, 23);
            this.button1.TabIndex = 26;
            this.button1.Text = "타이머";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // timer1
            // 
            this.timer1.Tick += new System.EventHandler(this.timer1_Tick);
            // 
            // pictureBox6
            // 
            this.pictureBox6.Image = ((System.Drawing.Image)(resources.GetObject("pictureBox6.Image")));
            this.pictureBox6.Location = new System.Drawing.Point(477, 57);
            this.pictureBox6.Name = "pictureBox6";
            this.pictureBox6.Size = new System.Drawing.Size(28, 31);
            this.pictureBox6.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.pictureBox6.TabIndex = 21;
            this.pictureBox6.TabStop = false;
            // 
            // pictureBox3
            // 
            this.pictureBox3.Image = ((System.Drawing.Image)(resources.GetObject("pictureBox3.Image")));
            this.pictureBox3.Location = new System.Drawing.Point(333, 165);
            this.pictureBox3.Name = "pictureBox3";
            this.pictureBox3.Size = new System.Drawing.Size(155, 89);
            this.pictureBox3.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.pictureBox3.TabIndex = 18;
            this.pictureBox3.TabStop = false;
            // 
            // pictureBox5
            // 
            this.pictureBox5.Image = ((System.Drawing.Image)(resources.GetObject("pictureBox5.Image")));
            this.pictureBox5.Location = new System.Drawing.Point(285, 57);
            this.pictureBox5.Name = "pictureBox5";
            this.pictureBox5.Size = new System.Drawing.Size(32, 30);
            this.pictureBox5.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.pictureBox5.TabIndex = 17;
            this.pictureBox5.TabStop = false;
            // 
            // pictureBox4
            // 
            this.pictureBox4.Image = ((System.Drawing.Image)(resources.GetObject("pictureBox4.Image")));
            this.pictureBox4.Location = new System.Drawing.Point(509, 57);
            this.pictureBox4.Name = "pictureBox4";
            this.pictureBox4.Size = new System.Drawing.Size(32, 30);
            this.pictureBox4.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.pictureBox4.TabIndex = 16;
            this.pictureBox4.TabStop = false;
            // 
            // window
            // 
            this.window.Location = new System.Drawing.Point(773, 392);
            this.window.Name = "window";
            this.window.Size = new System.Drawing.Size(337, 111);
            this.window.TabIndex = 14;
            this.window.TabStop = false;
            // 
            // pictureBox1
            // 
            this.pictureBox1.Image = ((System.Drawing.Image)(resources.GetObject("pictureBox1.Image")));
            this.pictureBox1.Location = new System.Drawing.Point(12, 3);
            this.pictureBox1.Name = "pictureBox1";
            this.pictureBox1.Size = new System.Drawing.Size(800, 383);
            this.pictureBox1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.pictureBox1.TabIndex = 13;
            this.pictureBox1.TabStop = false;
            // 
            // warning
            // 
            this.warning.Location = new System.Drawing.Point(773, 509);
            this.warning.Name = "warning";
            this.warning.Size = new System.Drawing.Size(337, 60);
            this.warning.TabIndex = 12;
            this.warning.TabStop = false;
            // 
            // driving_cam
            // 
            this.driving_cam.Location = new System.Drawing.Point(818, 37);
            this.driving_cam.Name = "driving_cam";
            this.driving_cam.Size = new System.Drawing.Size(292, 349);
            this.driving_cam.TabIndex = 8;
            this.driving_cam.TabStop = false;
            // 
            // Gear
            // 
            this.Gear.AutoSize = true;
            this.Gear.BackColor = System.Drawing.SystemColors.ActiveCaptionText;
            this.Gear.Font = new System.Drawing.Font("굴림", 24F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(129)));
            this.Gear.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.Gear.Location = new System.Drawing.Point(614, 254);
            this.Gear.Name = "Gear";
            this.Gear.Size = new System.Drawing.Size(36, 32);
            this.Gear.TabIndex = 29;
            this.Gear.Text = "P";
            // 
            // timer2
            // 
            this.timer2.Tick += new System.EventHandler(this.timer2_Tick);
            // 
            // timer3
            // 
            this.timer3.Tick += new System.EventHandler(this.timer3_Tick);
            // 
            // Form2
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.SystemColors.ActiveCaption;
            this.ClientSize = new System.Drawing.Size(1122, 576);
            this.Controls.Add(this.Gear);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.button1);
            this.Controls.Add(this.Rpm);
            this.Controls.Add(this.speed);
            this.Controls.Add(this.pictureBox6);
            this.Controls.Add(this.check);
            this.Controls.Add(this.home);
            this.Controls.Add(this.pictureBox3);
            this.Controls.Add(this.pictureBox5);
            this.Controls.Add(this.pictureBox4);
            this.Controls.Add(this.window);
            this.Controls.Add(this.pictureBox1);
            this.Controls.Add(this.warning);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.driving_cam);
            this.Controls.Add(this.Break);
            this.Controls.Add(this.Accelerator);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Name = "Form2";
            this.Text = "Form2";
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox6)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox3)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox5)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox4)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.window)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.warning)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.driving_cam)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Button Accelerator;
        private System.Windows.Forms.Button Break;
        private System.Windows.Forms.PictureBox driving_cam;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.PictureBox warning;
        private System.Windows.Forms.PictureBox pictureBox1;
        private System.Windows.Forms.PictureBox window;
        private System.Windows.Forms.PictureBox pictureBox4;
        private System.Windows.Forms.PictureBox pictureBox5;
        private System.Windows.Forms.PictureBox pictureBox3;
        private System.Windows.Forms.Button home;
        private System.Windows.Forms.Button check;
        private System.Windows.Forms.PictureBox pictureBox6;
        private System.Windows.Forms.Label speed;
        private System.Windows.Forms.Label Rpm;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Button button1;
        private System.Windows.Forms.Timer timer1;
        private System.Windows.Forms.Label Gear;
        private System.Windows.Forms.Timer timer2;
        private System.Windows.Forms.Timer timer3;
    }
}
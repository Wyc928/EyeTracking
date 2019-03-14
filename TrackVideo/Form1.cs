/*
	Author: Wenyu
  Modified by Wang Yongchen
	Version: 1.0
	Date: 3/11/2019
	Function:
	generate a moving ball for pupils to gaze at and output the ball points
*/
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;

namespace TrackVideo
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            CheckForIllegalCrossThreadCalls = false;
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        static string filePath = "F:\\DataSet\\Data\\Ball\\BallOriginalPoints.txt";
        public static void Ball(Form fm)
        {
            System.Drawing.Rectangle ScreenArea = System.Windows.Forms.Screen.GetBounds(fm);
            int width = ScreenArea.Width;
            int height = ScreenArea.Height;
            double speed = 0.2;
            int scale = 50;
            int amount = width * height / scale / scale;
            int[] vpoints = new int[amount];

            for (int i = 0; i < amount; i++)
            {
                vpoints[i] = i;
            }

            System.Drawing.Graphics g = fm.CreateGraphics();
            System.Drawing.Brush bush = new System.Drawing.SolidBrush(System.Drawing.Color.Green);

            System.Random rd = new System.Random();
            int lastW = 0, lastH = 0;
            
            using (StreamWriter sw = new StreamWriter(filePath))
            {
                for (int i = 0; i < amount; i++)
                {
                    int now = rd.Next(0, amount - i);
                    int value = vpoints[now];
                    vpoints[now] = vpoints[amount - 1 - i];

                    int nw = value % (width / scale);
                    int nh = value / (width / scale);
                    //g.FillEllipse(bush, nw * scale, nh * scale, 10, 10);
                    //System.Threading.Thread.Sleep(1000);

                    if (i > 0)
                    {
                        int dis2 = (lastW - nw) * (lastW - nw) + (lastH - nh) * (lastH - nh);
                        double dis = System.Math.Sqrt(dis2);
                        for (double j = 0; j < 1.0f; j += speed / dis)
                        {
                            double w = lastW + j * (nw - lastW);
                            double h = lastH + j * (nh - lastH);
                            g.FillEllipse(bush, (float)w * scale, (float)h * scale, 20, 20);
                            System.Threading.Thread.Sleep(100);
                            g.Clear(fm.BackColor);
                            //add by wangyongchen: output
                            float ball_X = (float)w * scale + 10;
                            float ball_Y = (float)h * scale + 10;
                            long currentTime = GetTimestamp();
                            sw.WriteLine(((int)ball_X).ToString() + "\t" + ((int)ball_Y).ToString() + "\t" + currentTime.ToString());
                            sw.Flush();
                        }
                    }
                    lastW = nw;
                    lastH = nh;
                }
            }
        }
        //add by wangyongchen 
        public static long GetTimestamp()
        {
            TimeSpan ts = DateTime.Now.ToUniversalTime() - new DateTime(1970, 1, 1);
            return (long)ts.TotalMilliseconds; //return time stamp
        }
        bool if_thread_exist = false;
        public System.Threading.Thread th;
        /*
        private void Form1_MouseClick(object sender, MouseEventArgs e)
        {
            th = new System.Threading.Thread(
                delegate() 
                {
                    Ball(this);
                });
            th.Start();
        }
        */
        private void Form1_SpacePress(object sender, KeyPressEventArgs e)
        {
            if (if_thread_exist == false)
            {
                if (e.KeyChar == 32)
                {
                    //add by wang yongchen 
                    if_thread_exist = true;
                    if (File.Exists(filePath))
                    {
                        File.Delete(filePath);
                    }
                    FileStream fs = new FileStream(filePath, FileMode.Create);
                    fs.Close();
                    th = new System.Threading.Thread(
                    delegate ()
                    {
                        Ball(this);
                    });
                    th.Start();
                }
            }
        }
        private void Form1_KeyPress(object sender, KeyPressEventArgs e)
        {
            if (e.KeyChar == 27)
            {
                th.Abort();
                Application.Exit();
            }
        }
    }
}

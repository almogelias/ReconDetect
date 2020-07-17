using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Diagnostics;
using System.IO;

namespace ControlCenter
{
    public partial class AttackSimulatorUserControl : UserControl
    {
        String target;
        String results;
        public AttackSimulatorUserControl()
        {
            InitializeComponent();
        }

        public void retriveTarget(String ipAddr)
        {
            target = ipAddr;
        }

        private String ExecProcess(String attackType,String target, int value)
        {
            if (target != null)
            {
                // clean console screen
                attackConsoleTextBox.Clear();
                //Create process info
                var psi = new ProcessStartInfo();
                psi.FileName = @"C:\Users\Anon\AppData\Local\Programs\Python\Python38-32\python.exe";

                //Provide the Script and arguments
                var script = String.Format("C:\\Scripts\\{0}.py", attackType);
                psi.Arguments = " " + "-u" + " " + $"\"{script}\"" + " " + target + " " + value;
                psi.UseShellExecute = false;
                psi.CreateNoWindow = true;
                psi.RedirectStandardOutput = true;
                psi.RedirectStandardError = true;

                //Excute process and get output
                var error = "";

                try
                {
                    using (var process = Process.Start(psi))
                    {
                        while ((process.StandardOutput.ReadLine()) != null)
                        {
                            
                            StreamReader myStreamReader = process.StandardOutput;

                            attackConsoleTextBox.AppendText(myStreamReader.ReadLine());
                            attackConsoleTextBox.AppendText(Environment.NewLine);
                            attackConsoleTextBox.SelectionStart = attackConsoleTextBox.Text.Length;
                            attackConsoleTextBox.SelectionLength = 0;
                            
                        }
                        error = process.StandardError.ReadToEnd();
                    }
                    if (error != "")
                    {
                        return "Error: \n" + error;
                    }
                    else
                    {
                        return "";
                    }
                }
                catch (Exception e)
                {
                    attackConsoleTextBox.AppendText("Finished process !!!" + "\n");
                    return "";
                }
            }
            else
            {
                MessageBox.Show("No IP address is set", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return "";
            }
        }

        private void AttackSynButton_Click(object sender, EventArgs e)
        {       
            results = ExecProcess(attackSynButton.Text,target,Convert.ToInt32(attackSynAmountText.Text));
            attackConsoleTextBox.Text += results;
            attackConsoleTextBox.SelectionStart = attackConsoleTextBox.Text.Length;
            attackConsoleTextBox.SelectionLength = 0;
        }

        private void AttackScanButton_Click(object sender, EventArgs e)
        {
            results = ExecProcess(attackScanButton.Text, target, Convert.ToInt32(attackPortAmountText.Text));
            attackConsoleTextBox.Text += results;
            attackConsoleTextBox.SelectionStart = attackConsoleTextBox.Text.Length;
            attackConsoleTextBox.SelectionLength = 0;
        }

        private void AttackFileTransButton_Click(object sender, EventArgs e)
        {
            results = ExecProcess(attackFileTransButton.Text, target, Convert.ToInt32(attackFileTransText.Text));
            attackConsoleTextBox.Text += results;
            attackConsoleTextBox.SelectionStart = attackConsoleTextBox.Text.Length;
            attackConsoleTextBox.SelectionLength = 0;
        }

        private void AttackUnknownPortButton_Click(object sender, EventArgs e)
        {
            results = ExecProcess(attackUnknownPortButton.Text, target, Convert.ToInt32(attackUnknownPortText.Text));
            attackConsoleTextBox.Text += results;
            attackConsoleTextBox.SelectionStart = attackConsoleTextBox.Text.Length;
            attackConsoleTextBox.SelectionLength = 0;
        }

        private void AttackDataPayloadButton_Click(object sender, EventArgs e)
        {
            attackConsoleTextBox.Text = "Sending a word with big payload ...";
            attackConsoleTextBox.AppendText(Environment.NewLine);
            results = ExecProcess(attackDataPayloadButton.Text, target, Convert.ToInt32(attackDataPayloadText.Text));
            attackConsoleTextBox.Text += results;
            attackConsoleTextBox.SelectionStart = attackConsoleTextBox.Text.Length;
            attackConsoleTextBox.SelectionLength = 0;
        }

        private void AttackDataButton_Click(object sender, EventArgs e)
        {
            attackConsoleTextBox.Text = "Sending 100 words with delay of 0.2 miliseconds ...";
            attackConsoleTextBox.AppendText(Environment.NewLine);
            results = ExecProcess(attackDataButton.Text, target, Convert.ToInt32(attackDataText.Text));
            attackConsoleTextBox.Text += results;
            attackConsoleTextBox.SelectionStart = attackConsoleTextBox.Text.Length;
            attackConsoleTextBox.SelectionLength = 0;
        }

        private void AttackDataCharButton_Click(object sender, EventArgs e)
        {
            attackConsoleTextBox.Text = "Sending 1 char in payload...";
            attackConsoleTextBox.AppendText(Environment.NewLine);
            results = ExecProcess(attackDataCharButton.Text, target, Convert.ToInt32(attackDataCharText.Text));
            attackConsoleTextBox.Text += results;
            attackConsoleTextBox.SelectionStart = attackConsoleTextBox.Text.Length;
            attackConsoleTextBox.SelectionLength = 0;
        }

        private void AttackBigFileTransButton_Click(object sender, EventArgs e)
        {
            results = ExecProcess(attackBigFileTransButton.Text, target, Convert.ToInt32(attackBigFileTransText.Text));
            attackConsoleTextBox.Text += results;
            attackConsoleTextBox.SelectionStart = attackConsoleTextBox.Text.Length;
            attackConsoleTextBox.SelectionLength = 0;
        }

        private void AttackFileExecButton_Click(object sender, EventArgs e)
        {
            results = ExecProcess(attackFileExecButton.Text, target, Convert.ToInt32(attackFileExecText.Text));
            attackConsoleTextBox.Text += results;
            attackConsoleTextBox.SelectionStart = attackConsoleTextBox.Text.Length;
            attackConsoleTextBox.SelectionLength = 0;
        }
    }
}

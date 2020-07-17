using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Net;
using System.Net.NetworkInformation;


namespace ControlCenter
{
    public partial class Settings : UserControl
    {   
        private String target;
        private bool isAlive = false;
        public Settings()
        {
            InitializeComponent();
        }

        private void TargetSubmit_Click(object sender, EventArgs e)
        {

            String input = targetMaskedTextBox.Text;
            if (input.Contains(" "))
                input = input.Replace(" ", "");
            IPAddress ipAddress;
            if (IPAddress.TryParse(input, out ipAddress))
            {
                PingHost(ipAddress.ToString());
                //IP address has been parsed correctly
                
            }
            else
            {
                MessageBox.Show("Please provide a valid IP address");
            }
        }


        public async void PingHost(string nameOrAddress)
        {
            bool pingable = isAlive = false;
            Ping pinger = null;

            try
            {
                pinger = new Ping();
                PingReply reply = await pinger.SendPingAsync(nameOrAddress);
                pingable = reply.Status == IPStatus.Success;
            }
            catch (PingException)
            {
                // Discard PingExceptions and return false;
                isAlive = pingable;
            }
            finally
            {
                if (pinger != null)
                {
                    pinger.Dispose();
                }
            }

            isAlive = pingable;
            if (!isAlive)
            {
                MessageBox.Show("No ping to host! please submit another ip address", "Host is down", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
            else
            {
                MessageBox.Show("Target submitted", "Submission", MessageBoxButtons.OK, MessageBoxIcon.Information);
                target = nameOrAddress;
            }
        }
        public String getTarget()
        {
            return target;
        }
    }
}

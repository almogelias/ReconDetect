using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace ControlCenter
{
    public partial class ConsoleCenter : Form
    {
        //Move form panel
        int mov;
        int movX;
        int movY;
        String target="";
        
        public ConsoleCenter()
        {
            InitializeComponent();
        }
        private void ConsoleCenter_Load(object sender, EventArgs e)
        {
            this.Location = Screen.AllScreens[0].WorkingArea.Location;
            settings.Hide();
            attackSimulatorUserControl.Hide();
            aboutDescription.Show();
        }

        private void HeaderPanel_MouseDown(object sender, MouseEventArgs e)
        {
            mov = 1;
            movX = e.X;
            movY = e.Y;
        }
        // Moving window 
        private void HeaderPanel_MouseMove(object sender, MouseEventArgs e)
        {
            if (mov == 1)
            {
                this.SetDesktopLocation(MousePosition.X - movX, MousePosition.Y - movY);
            }
        }
        private void HeaderPanel_MouseUp(object sender, MouseEventArgs e)
        {
            mov = 0;
        }

        private void Close_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void Minimize_Click(object sender, EventArgs e)
        {
            this.WindowState = FormWindowState.Minimized;
        }

        // ###### MENU Code ######

        private void SettingsButton_Click(object sender, EventArgs e)
        {
            attackSimulatorUserControl.Hide();
            aboutDescription.Hide();
            settings.Show();
        }

        private void AttackSimulatorButton_Click(object sender, EventArgs e)
        {
            settings.Hide();
            aboutDescription.Hide();
            target = settings.getTarget();
            attackSimulatorUserControl.retriveTarget(target);
            attackSimulatorUserControl.Show();
        }

        private void AboutButton_Click(object sender, EventArgs e)
        {
            attackSimulatorUserControl.Hide();
            settings.Hide();
            aboutDescription.Show();

        }
    }
}

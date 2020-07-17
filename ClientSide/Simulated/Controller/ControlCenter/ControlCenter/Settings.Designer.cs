namespace ControlCenter
{
    partial class Settings
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

        #region Component Designer generated code

        /// <summary> 
        /// Required method for Designer support - do not modify 
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.targetMaskedTextBox = new System.Windows.Forms.MaskedTextBox();
            this.targetSubmit = new System.Windows.Forms.Button();
            this.targetLable = new System.Windows.Forms.Label();
            this.targetGif = new System.Windows.Forms.PictureBox();
            this.targetIPLabel = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.targetGif)).BeginInit();
            this.SuspendLayout();
            // 
            // targetMaskedTextBox
            // 
            this.targetMaskedTextBox.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(41)))), ((int)(((byte)(53)))), ((int)(((byte)(65)))));
            this.targetMaskedTextBox.Font = new System.Drawing.Font("Century Gothic", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.targetMaskedTextBox.ForeColor = System.Drawing.Color.White;
            this.targetMaskedTextBox.Location = new System.Drawing.Point(0, 273);
            this.targetMaskedTextBox.Mask = "000\\.000\\.000\\.000";
            this.targetMaskedTextBox.Name = "targetMaskedTextBox";
            this.targetMaskedTextBox.RightToLeft = System.Windows.Forms.RightToLeft.No;
            this.targetMaskedTextBox.Size = new System.Drawing.Size(208, 33);
            this.targetMaskedTextBox.TabIndex = 8;
            this.targetMaskedTextBox.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // targetSubmit
            // 
            this.targetSubmit.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(41)))), ((int)(((byte)(53)))), ((int)(((byte)(65)))));
            this.targetSubmit.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(41)))), ((int)(((byte)(53)))), ((int)(((byte)(65)))));
            this.targetSubmit.FlatAppearance.BorderSize = 0;
            this.targetSubmit.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.targetSubmit.Font = new System.Drawing.Font("Century Gothic", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.targetSubmit.ForeColor = System.Drawing.Color.White;
            this.targetSubmit.Location = new System.Drawing.Point(450, 271);
            this.targetSubmit.Name = "targetSubmit";
            this.targetSubmit.Size = new System.Drawing.Size(127, 34);
            this.targetSubmit.TabIndex = 5;
            this.targetSubmit.Text = "Submit";
            this.targetSubmit.UseVisualStyleBackColor = false;
            this.targetSubmit.Click += new System.EventHandler(this.TargetSubmit_Click);
            // 
            // targetLable
            // 
            this.targetLable.AutoSize = true;
            this.targetLable.BackColor = System.Drawing.Color.Black;
            this.targetLable.Font = new System.Drawing.Font("Century Gothic", 15.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.targetLable.ForeColor = System.Drawing.Color.White;
            this.targetLable.Location = new System.Drawing.Point(15, 9);
            this.targetLable.Name = "targetLable";
            this.targetLable.Size = new System.Drawing.Size(123, 25);
            this.targetLable.TabIndex = 6;
            this.targetLable.Text = "Target Host";
            // 
            // targetGif
            // 
            this.targetGif.Image = global::ControlCenter.Properties.Resources.norse_attack;
            this.targetGif.Location = new System.Drawing.Point(0, 0);
            this.targetGif.Name = "targetGif";
            this.targetGif.Size = new System.Drawing.Size(577, 325);
            this.targetGif.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.targetGif.TabIndex = 7;
            this.targetGif.TabStop = false;
            // 
            // targetIPLabel
            // 
            this.targetIPLabel.AutoSize = true;
            this.targetIPLabel.BackColor = System.Drawing.Color.Black;
            this.targetIPLabel.Font = new System.Drawing.Font("Century Gothic", 14.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.targetIPLabel.ForeColor = System.Drawing.Color.White;
            this.targetIPLabel.Location = new System.Drawing.Point(16, 249);
            this.targetIPLabel.Name = "targetIPLabel";
            this.targetIPLabel.Size = new System.Drawing.Size(89, 23);
            this.targetIPLabel.TabIndex = 9;
            this.targetIPLabel.Text = "Target IP";
            // 
            // Settings
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.Controls.Add(this.targetIPLabel);
            this.Controls.Add(this.targetMaskedTextBox);
            this.Controls.Add(this.targetSubmit);
            this.Controls.Add(this.targetLable);
            this.Controls.Add(this.targetGif);
            this.Name = "Settings";
            this.Size = new System.Drawing.Size(577, 305);
            ((System.ComponentModel.ISupportInitialize)(this.targetGif)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.MaskedTextBox targetMaskedTextBox;
        private System.Windows.Forms.Button targetSubmit;
        private System.Windows.Forms.Label targetLable;
        private System.Windows.Forms.PictureBox targetGif;
        private System.Windows.Forms.Label targetIPLabel;
    }
}

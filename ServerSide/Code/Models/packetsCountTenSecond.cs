//------------------------------------------------------------------------------
// <auto-generated>
//     This code was generated from a template.
//
//     Manual changes to this file may cause unexpected behavior in your application.
//     Manual changes to this file will be overwritten if the code is regenerated.
// </auto-generated>
//------------------------------------------------------------------------------

namespace WebConsole.Models
{
    using System;
    using System.Collections.Generic;
    
    public partial class packetsCountTenSecond
    {
        public int PacketCountTenID { get; set; }
        public int TimePeriod { get; set; }
        public long startTimeUnixMillisec { get; set; }
        public long endTimeUnixMillisec { get; set; }
        public string Day { get; set; }
        public int packetCount { get; set; }
        public int counterOfSyn { get; set; }
        public int counterOfAck { get; set; }
        public int counterOfPa { get; set; }
        public int counterOfR { get; set; }
        public int counterOfRA { get; set; }
        public int counterOfFin { get; set; }
        public int packetsTotalSize { get; set; }
    }
}

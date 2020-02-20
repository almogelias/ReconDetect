using System;
using System.Runtime.Serialization;

namespace ASPNET_MVC_ChartsModel
{
    //DataContract for Serializing Data - required to serve in JSON format
    [DataContract]
    public class DataPoint
    {
        public DataPoint(double x, double y)
        {
            this.X = x;
            this.Y = y;
        }

        //Explicitly setting the name to be used while serializing to JSON.
        [DataMember(Name = "x")]
        public Nullable<double> X = null;

        //Explicitly setting the name to be used while serializing to JSON.
        [DataMember(Name = "y")]
        public Nullable<double> Y = null;
    }

    public class DataPoints
    {
        public DataPoints(int time, int cSyn, int cPa, int cR, int totalSize)
        {
            this.time = time;
            this.cSyn = cSyn;
            this.cPa = cPa;
            this.cR = cR;
            this.totalSize = totalSize;
        }


        public DataPoints(int time, String service, int cSyn, int cPa, int cR, int totalSize)
        {
            this.time = time;
            this.service = service;
            this.cSyn = cSyn;
            this.cPa = cPa;
            this.cR = cR;
            this.totalSize = totalSize;
        }

        //Explicitly setting the name to be used while serializing to JSON.
        [DataMember(Name = "TimePeriod")]
        public Nullable<int> time = null;
        //Explicitly setting the name to be used while serializing to JSON.
        [DataMember(Name = "Service")]
        public String service = null;
        //Explicitly setting the name to be used while serializing to JSON.
        [DataMember(Name = "CounterOfSyn")]
        public Nullable<int> cSyn = null;
        //Explicitly setting the name to be used while serializing to JSON.
        [DataMember(Name = "CounterOfPayloads")]
        public Nullable<int> cPa = null;
        //Explicitly setting the name to be used while serializing to JSON.
        [DataMember(Name = "CounterOfReset")]
        public Nullable<int> cR = null;
        //Explicitly setting the name to be used while serializing to JSON.
        [DataMember(Name = "TotalSize")]
        public Nullable<int> totalSize = null;
    }

}
using System;
using System.Collections.Generic;
using WebConsole.Models;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using ASPNET_MVC_ChartsModel;
using Newtonsoft.Json;





namespace WebConsole.Controllers

{

    public class HomeController : Controller

    {

        public ContentResult JsonHome(int xStart1 = 0, int yStart1 = 0, int length1 = 1, int xStart2 = 0, int yStart2 = 0, int length2 = 1)

        {

            List<DataPoint> dataPoints1 = new List<DataPoint>();

            List<DataPoint> dataPoints2 = new List<DataPoint>();

            Dictionary<int, List<DataPoint>> Tables = new Dictionary<int, List<DataPoint>>();

            int y1 = yStart1;
            int x1 = xStart1;
            String packetsAnomaly = null;

            int y2 = yStart2;
            int x2 = xStart2;
            String flowAnomaly = null;
            FinalProjectEntities context = new FinalProjectEntities();

            var query1 = context.packetsCountTenSecond.Include("TimePeriod")

               .Select(g => new { name = g.TimePeriod, packetCount = g.packetCount , anomaly = g.Anomaly }).ToList();



            var query2 = context.Flows.Include("TimePeriod")

               .Select(g => new { timePeriod = g.TimePeriod, dstPort = g.dstPort, packetCount = g.counterOfPackets , anomaly = g.Anomaly}).OrderByDescending(u => u.timePeriod).Take(5).ToList();



            int rows1 = query1.Count;

            int rows2 = query2.Count;



            if (rows1 > 30)

            {

                for (int i = rows1 - 30; i < rows1; i++)

                {
                    y1 = query1[i].packetCount;
                    x1 = query1[i].name;
                    packetsAnomaly = query1[i].anomaly.ToString();
                    /* y = y + random.Next(-1, 2); 

                    dataPoints.Add(new DataPoint(xStart + i, y));  

                    */

                    dataPoints1.Add(new DataPoint(x1, y1,packetsAnomaly));
                }

            }

            else

            {

                for (int i = 0; i < rows1; i++)

                {

                    y1 = query1[i].packetCount;
                    x1 = query1[i].name;
                    packetsAnomaly = query1[i].anomaly.ToString();

                    /* y = y + random.Next(-1, 2); 

                    dataPoints.Add(new DataPoint(xStart + i, y));  

                    */

                    dataPoints1.Add(new DataPoint(x1, y1, packetsAnomaly));

                }

            }



            if (rows2 > 30)

            {

                for (int i = rows2 - 30; i < rows2; i++)

                {

                    y2 = query2[i].packetCount;

                    x2 = query2[i].dstPort;
                    flowAnomaly = query2[i].anomaly.ToString();
                    /* y = y + random.Next(-1, 2); 

                    dataPoints.Add(new DataPoint(xStart + i, y));  

                    */

                    dataPoints2.Add(new DataPoint(x2, y2, flowAnomaly));

                }

            }

            else

            {

                for (int i = 0; i < rows2; i++)

                {

                    y2 = query2[i].packetCount;

                    x2 = query2[i].dstPort;

                    flowAnomaly = query2[i].anomaly.ToString();
                    /* y = y + random.Next(-1, 2); 

                    dataPoints.Add(new DataPoint(xStart + i, y));  

                    */

                    dataPoints2.Add(new DataPoint(x2, y2, flowAnomaly));

                }

            }

            Tables.Add(1, dataPoints1);

            Tables.Add(2, dataPoints2);

            return Content(JsonConvert.SerializeObject(Tables, _jsonSetting), "application/json");



        }





        public ContentResult JsonNetwork(string sourceEntity = "", string destinationEntity = "",string file="", string service = "")

        {

            String[,] dataPointsGraph;

            FinalProjectEntities context = new FinalProjectEntities();
            /*
            var query = context.Flows.Select(g => new { srcIp = g.srcIpAddr, dstIp = g.dstIpAddr, svc = g.Service }).Where(s => s.svc != "None")

                .OrderByDescending(u => u.svc).GroupBy(v => new { v.srcIp, v.dstIp, v.svc }).Take(20).ToList();

            */
            var query = (from f in context.Flows
                          join p in context.Processes
                           on f.PID equals p.PID
                          select new { f, p }).Select(g => new {
                              srcIp = g.f.srcIpAddr,
                              dstIp = g.f.dstIpAddr,
                              svc = g.f.Service,
                              dstPort = g.f.dstPort,
                              anomaly = g.f.Anomaly,
                              pid = g.p.PID,
                              fileName = g.p.FileName,
                              path = g.p.FilePath,
                              deltaTime = g.p.DeltaTimeMillisec / 100000000
                          }).OrderByDescending(u => u.svc).GroupBy(v => new {
                              v.srcIp, v.dstIp, v.svc ,v.dstPort ,v.fileName , v.anomaly
                          }).Take(20).ToList();


            int rows = query.Count;

            int counter = 0;

            dataPointsGraph = new String[(rows * 3), 3]; //Because there are destIP and srcIP


            for (int i = 0; i < rows; i++)

            {

                sourceEntity = query[i].Key.srcIp;
                if(query[i].Key.fileName == "None")
                {
                    file = "Unknown";
                }
                else
                {
                    file = query[i].Key.fileName;
                }
                dataPointsGraph[i, 0] = sourceEntity;
                dataPointsGraph[i, 1] = file;
                dataPointsGraph[i, 2] = query[i].Key.anomaly.ToString();
            }
            counter=rows;

            for (int i = counter; i <=(rows*2)-1; i++)
            {
                if (query[i - counter].Key.fileName == "None")
                {
                    file = "Unknown";
                }
                else
                {
                    file = query[i - counter].Key.fileName;
                }
                if(query[i - counter].Key.svc !="None")
                {
                    service = query[i - counter].Key.svc;
                }
                else
                {
                    service = query[i - counter].Key.dstPort.ToString();
                }
                dataPointsGraph[i, 0] = file;
                dataPointsGraph[i, 1] = service;
                dataPointsGraph[i, 2] = query[i - counter].Key.anomaly.ToString();
            }
            counter = (rows * 2);

            for (int i = counter; i <= dataPointsGraph.GetLength(0) - 1; i++)   //Because there are destIP and srcIP

            {
                if(query[i - counter].Key.svc!="None")
                {
                    service = query[i - counter].Key.svc;
                }
                else
                {
                    service = query[i - counter].Key.dstPort.ToString();
                }

                destinationEntity = query[i - counter].Key.dstIp;

                dataPointsGraph[i, 0] = service;
                dataPointsGraph[i, 1] = destinationEntity;
                dataPointsGraph[i, 2] = query[i - counter].Key.anomaly.ToString();
            }
            
            return Content(JsonConvert.SerializeObject(dataPointsGraph, _jsonSetting), "application/json");



        }





        public ContentResult JsonExtention(int SynCount = 0, int PaCount = 0, int Rcount = 0, int TotalCount = 0, int tPeriod = 0)

        {

            List<DataPoints> dataPointsPackets = new List<DataPoints>();

            List<DataPoints> dataPointsFlows = new List<DataPoints>();

            Dictionary<String, List<DataPoints>> Tables = new Dictionary<String, List<DataPoints>>();

            int time = tPeriod;

            String service;

            int dstPort = 0;

            int cSyn = SynCount;

            int cPa = PaCount;

            int cR = Rcount;

            int totalSize = TotalCount;

            String anomalyField = null;

            FinalProjectEntities context = new FinalProjectEntities();

            var query1 = context.packetsCountTenSecond.Include("TimePeriod")

               .Select(g => new {

                   timePeriod = g.TimePeriod,

                   counterOfSyn = g.counterOfSyn,

                   counterOfPa = g.counterOfPa,

                   counterOfR = g.counterOfR,

                   packetsOfTotalSize = g.packetsTotalSize,

                   anomaly = g.Anomaly
               }).ToList();

            
            
            var query2 = context.Flows.Include("Time")
                .Select(g => new {

                   time = g.Time / 1000000,

                   serviceProtocol = g.Service,

                   dstPort = g.dstPort,

                   counterOfSyn = g.counterOfSyn,

                   counterOfPa = g.counterOfPa,

                   counterOfR = g.counterOfR,

                   packetsOfTotalSize = g.packetsTotalSize,

                    anomaly = g.Anomaly

               }).ToList();
            


            int rowsPackets = query1.Count;

            int rowsFlows = query2.Count;

            if (rowsPackets > 30)

            {

                for (int i = rowsPackets - 30; i < rowsPackets; i++)

                {

                    time = query1[i].timePeriod;

                    cSyn = query1[i].counterOfSyn;

                    cPa = query1[i].counterOfPa;

                    cR = query1[i].counterOfR;

                    totalSize = query1[i].packetsOfTotalSize;

                    anomalyField = query1[i].anomaly.ToString();

                    dataPointsPackets.Add(new DataPoints(time, cSyn, cPa, cR, totalSize, anomalyField));

                }

            }

            else

            {

                for (int i = 0; i < rowsPackets; i++)

                {

                    time = query1[i].timePeriod;

                    cSyn = query1[i].counterOfSyn;

                    cPa = query1[i].counterOfPa;

                    cR = query1[i].counterOfR;

                    totalSize = query1[i].packetsOfTotalSize;

                    anomalyField= query1[i].anomaly.ToString();

                    dataPointsPackets.Add(new DataPoints(time, cSyn, cPa, cR, totalSize, anomalyField));

                }

            }

            if (rowsFlows > 30)

            {

                for (int i = rowsFlows - 30; i < rowsFlows; i++)

                {

                    time = Convert.ToInt32(query2[i].time);
                    if(query2[i].serviceProtocol!="None")
                    {
                        service = query2[i].serviceProtocol;
                    }
                    else
                    {
                        service = query2[i].dstPort.ToString();
                    }
                    cSyn = query2[i].counterOfSyn;

                    cPa = query2[i].counterOfPa;

                    cR = query2[i].counterOfR;

                    totalSize = query2[i].packetsOfTotalSize;

                    anomalyField = query2[i].anomaly.ToString();

                    dataPointsFlows.Add(new DataPoints(time, service, cSyn, cPa, cR, totalSize, anomalyField));

                }

            }

            else

            {

                for (int i = 0; i < rowsFlows; i++)

                {

                    time = Convert.ToInt32(query2[i].time);

                    if (query2[i].serviceProtocol != "None")
                    {
                        service = query2[i].serviceProtocol;
                    }
                    else
                    {
                        service = query2[i].dstPort.ToString();
                    }

                    cSyn = query2[i].counterOfSyn;

                    cPa = query2[i].counterOfPa;

                    cR = query2[i].counterOfR;

                    totalSize = query2[i].packetsOfTotalSize;

                    anomalyField = query2[i].anomaly.ToString();

                    dataPointsFlows.Add(new DataPoints(time, service, cSyn, cPa, cR, totalSize, anomalyField));

                }

            }

            Tables.Add("packetsCountTenSeconds", dataPointsPackets);

            Tables.Add("Flows", dataPointsFlows);



            return Content(JsonConvert.SerializeObject(Tables, _jsonSetting), "application/json");

        }


        public ContentResult JsonAnomalies()
        {

            String time;
            String timeToPresent;
            String service;

            List<AnomalyDataPoints> anomalyDataPointsPackets = new List<AnomalyDataPoints>();

            List<AnomalyDataPoints> anomalyDataPointsFlows = new List<AnomalyDataPoints>();

            Dictionary<String, List<AnomalyDataPoints>> Tables = new Dictionary<String, List<AnomalyDataPoints>>();

            FinalProjectEntities context = new FinalProjectEntities();

            var query1 = context.packetsCountTenSecond.Include("TimePeriod")

               .Select(g => new {
                   packetsId = g.PacketCountTenID,
                   time = g.TimePeriod,
                   day = g.Day,
                   totalSize = g.packetsTotalSize,
                   anomaly = g.Anomaly
               }).Where(u=> u.anomaly==1).OrderByDescending(u => u.packetsId).ToList();

            var query2 = (from f in context.Flows
                          join p in context.Processes
                           on f.PID equals p.PID
                          select new { f, p }).Select(g => new {
                              flowId = g.f.FlowID,
                              time = (g.f.Time) / 1000,
                              day = g.f.Day,
                              srcIp = g.f.srcIpAddr,
                              dstIp = g.f.dstIpAddr,
                              svc = g.f.Service,
                              dstPort = g.f.dstPort,
                              totalSize = g.f.packetsTotalSize,
                              anomaly = g.f.Anomaly,
                              pid = g.p.PID,
                              fileName = g.p.FileName,
                              path = g.p.FilePath,
                              deltaTime = g.p.DeltaTimeMillisec / 100000000
                          }).Where(u => u.anomaly == 1).OrderByDescending(u => u.flowId).ToList();
            
            
            

            int rowsPackets = query1.Count;

            int rowsFlows = query2.Count;
            
            if (rowsPackets > 30)

            {
                for (int i = rowsPackets - 30; i < rowsPackets; i++)
                {
                    time = query1[i].time.ToString();
                    timeToPresent = time.Substring(0, 2) + ":" + time.Substring(2, 2) + ":"+time.Substring(4);
                    anomalyDataPointsPackets.Add(new AnomalyDataPoints(Convert.ToInt32(query1[i].packetsId), timeToPresent,
                                                                        query1[i].day,query1[i].totalSize,(query1[i].anomaly).ToString()));
                }

            }

            else

            {

                for (int i = 0; i < rowsPackets; i++)

                {
                    time = query1[i].time.ToString();
                    timeToPresent = time.Substring(0, 2) + ":" + time.Substring(2, 2) + ":" + time.Substring(4);

                    anomalyDataPointsPackets.Add(new AnomalyDataPoints(Convert.ToInt32(query1[i].packetsId), timeToPresent,
                                                                        query1[i].day, query1[i].totalSize, (query1[i].anomaly).ToString()));

                }

            }

            if (rowsFlows > 30)

            {

                for (int i = rowsFlows - 30; i < rowsFlows; i++)

                {

                    time = query2[i].time.ToString();
                    timeToPresent = time.Substring(0, 2) + ":" + time.Substring(2, 2) + ":" + time.Substring(4,2);

                    if (query2[i].svc != "None")
                    {
                        service = query2[i].svc;
                    }
                    else
                    {
                        service = query2[i].dstPort.ToString();
                    }

                    anomalyDataPointsFlows.Add(new AnomalyDataPoints(Convert.ToInt32(query2[i].flowId), timeToPresent, query2[i].day,
                                                                        service,query2[i].totalSize,(query2[i].anomaly).ToString()));

                }

            }

            else

            {

                for (int i = 0; i < rowsFlows; i++)

                {
                    time = query2[i].time.ToString();
                    timeToPresent = time.Substring(0, 2) + ":" + time.Substring(2, 2) + ":" + time.Substring(4,2);


                    if (query2[i].svc != "None")
                    {
                        service = query2[i].svc;
                    }
                    else
                    {
                        service = query2[i].dstPort.ToString();
                    }

                    anomalyDataPointsFlows.Add(new AnomalyDataPoints(Convert.ToInt32(query2[i].flowId), timeToPresent, query2[i].day,
                                                                        service, query2[i].totalSize, (query2[i].anomaly).ToString()));

                }

            }

            Tables.Add("anomalyPacketsTenSeconds", anomalyDataPointsPackets);

            Tables.Add("anomalyFlows", anomalyDataPointsFlows);


            
            return Content(JsonConvert.SerializeObject(Tables, _jsonSetting), "application/json");

        }

        public ContentResult JsonMatrix()
        {
            FinalProjectEntities context = new FinalProjectEntities();
            IDictionary<string, float> Tables = new Dictionary<string, float>();

            float truePositive = context.packetsCountTenSecond.Where(t => t.SimulatorAttack == 1).Where(o => o.Anomaly == 1)
                .Where(p => p.PacketCountTenID != 1).Count() + context.Flows.Where(t => t.SimulatorAttack == 1).Where(o => o.Anomaly == 1)
                .Where(p => p.FlowID != 1).Count();
            float trueNegative = context.packetsCountTenSecond.Where(t => t.SimulatorAttack == null).Where(o => o.Anomaly == 0 || o.Anomaly == null)
                .Where(p => p.PacketCountTenID != 1).Count()+ context.Flows.Where(t => t.SimulatorAttack == null).Where(o => o.Anomaly == 0 || o.Anomaly == null)
                .Where(p => p.FlowID != 1).Count();
            float falsePositive = context.packetsCountTenSecond.Where(t => t.SimulatorAttack == null).Where(o => o.Anomaly == 1)
                .Where(p => p.PacketCountTenID != 1).Count()+ context.Flows.Where(t => t.SimulatorAttack == null).Where(o => o.Anomaly == 1)
                .Where(p => p.FlowID != 1).Count();
            float falseNegative = context.packetsCountTenSecond.Where(t => t.SimulatorAttack == 1).Where(o => o.Anomaly == 0 || o.Anomaly == null)
                .Where(p => p.PacketCountTenID != 1).Count() + context.Flows.Where(t => t.SimulatorAttack == 1).Where(o => o.Anomaly == 0 || o.Anomaly == null)
                .Where(p => p.FlowID != 1).Count();

            Tables.Add("TruePositive", truePositive);
            Tables.Add("TrueNegative", trueNegative);
            Tables.Add("FalsePositive", falsePositive);
            Tables.Add("FalseNegative", falseNegative);
            Tables.Add("Accuracy", (truePositive + trueNegative) / (truePositive+trueNegative+falsePositive+falseNegative));
            Tables.Add("Precision", (truePositive / (truePositive + falsePositive)));
            Tables.Add("Sensitivity", (truePositive / (truePositive + falseNegative)));
            Tables.Add("Specificity", (trueNegative / (trueNegative + falsePositive)));
            Tables.Add("F1", ((2*Tables["Precision"]*Tables["Sensitivity"]) / (Tables["Precision"] + Tables["Sensitivity"])));
            return Content(JsonConvert.SerializeObject(Tables, _jsonSetting), "application/json");
        }

        JsonSerializerSettings _jsonSetting = new JsonSerializerSettings() { NullValueHandling = NullValueHandling.Ignore };


        public ActionResult Index()

        {

            return View();

        }


        public ActionResult Extension()

        {

            return View();

        }

        public ActionResult Anomalies()

        {

            return View();

        }
        public ActionResult Matrix()

        {

            return View();

        }


    }

}